---
name: ai-video-lipsync-qc
description: Quality-check AI-generated talking clips and the assembled episode - who speaks when, overlapping or open listener mouths, missing or breathy voices, dead air, laughs at clip ends, character/scene drift across clips, accidental trademarks, and audio/video sync of the delivered file. Uses ffmpeg contact sheets, face-zoom strips, a speech-band loudness timeline, a pitch (voicing) check, a cross-clip montage and a per-segment cross-correlation. Use after generating clips with Meta AI, Veo, Runway, Kling or similar, and again on the final render before upload. Triggers: lip sync QC, mouth overlap, contact sheet, speech timeline, clip QC, no voice, consistency check, A/V drift, subtitles don't match lip sync.
---

# AI Video Lip-Sync QC

## When to Use
- Every generated dialogue clip, before it goes into the edit decision list (EDL).
- Choosing in/out trim points that remove silence, ad-libs and laughs.
- Every location once its clips are accepted (cross-clip consistency).
- The delivered episode file, before every upload (A/V sync).

## When NOT to Use
- Checking that the spoken words are exactly right. These tools can't hear words: a person listens, or use YouTube's automatic captions after a Private upload (skill `youtube-studio-upload`).
- Final loudness. Measure that on the delivered file (skill `edu-video-assembly-ffmpeg`).

## Core Workflow
1. `qc.sh NAME` → speech-band timeline (`qc_audio.py`), voicing line (`voicing.py`) and a 10-frame contact sheet (1 fps, timestamped).
2. Read the timeline: `#` = loud speech-band 100 ms, `+` = medium, `.` = quiet. Speech segments = runs of `#`. **Each row is 5.0 s (50 characters); a run's time = the row label + its character index × 0.1.** Count from the row label every time: in EP3 two second takes were cut from the wrong row (5.0–7.0 instead of 7.0–8.7) and shipped silent in a first render.
3. Read the voicing line: a real spoken line shows solid `VVVVVVVV` runs. Only scattered `V` means breath, a whisper or no voice even when the RMS timeline looks like speech.
4. For each speech segment, `zoom.sh NAME START DUR [crop] [rows]` (5 fps, timestamps) and check that **only the scripted speaker's mouth moves**. Check the listener every frame.
5. Set in/out: lead-in trimmed, out point right after the last word (no laugh, chuckle or ad-lib).
6. Decide PASS / PASS-partial / FAIL and log the reason in `edl.tsv` (accepted) or `qc_log.txt` (failures and decisions).
7. Per location, `montage.py TAG CLIP@SEC …` → one labelled frame per accepted clip. Compare design details (beak colour, eyes, cap badge), background and layout across clips. Regenerate any odd one out.
8. Ask the owner to listen to: the first clip of every new character, intentionally wrong lines (Meta may "fix" them), and any clip with a weak voicing line. Batch them into one request with file + seconds.
9. Before rendering: `sync_check.py windows` prints the speech line of every clip window **and every card voice window** in `build.SEGS` and flags `NO SPEECH` (wrong in/out) and `CUT START`/`CUT END` (a `#` in the first/last 100 ms = a word cut off). Fix until 0 flagged.
10. After assembly: `sync_check.py drift out/<episode>.mp4` on the **delivered** file. Every clip segment must show 0 ms (±10) to the last clip. Then `sync_check.py cues` to check subtitle cue starts against speech onsets.

## Project Context
- **EP1 (2026-11-20):** 34 clips downloaded, 20 accepted. Problems: lip overlap 3, off-model 1, trademark text 1, scene inconsistency 8, refusal 1. `silencedetect` failed (ambience above −32 dB); the band-passed RMS timeline relative to the clip's 20th-percentile floor worked.
- **EP3 (2026-11-20):** 26 clips for 21 accepted. Caught by: zoom strips (eyelashes on Biscuit and Pudding, a teen listener's small "o" mouth seen only on a 160×110 crop of his profile), montage (beaded vs shimmer-band collar between the two-shot and the solo master, accepted and flagged), `windows`/drift (two silent second takes from a misread row; drift showed `+890 ms r=0.38` on one of them).
- **EP2 (2026-11-20):** 43 clips for 22 accepted. Caught by: zoom strips (listener "o" mouth, open grins, morphing characters), voicing + owner listening (a teen boy's lines were only breath in 3 clips), montage (grey-beak Biscuit in 3 desk clips; 6 different backgrounds in the first belt clips), `sync_check.py` (audio drifting up to >1.5 s late in two uploaded renders).

## Reference Guide
| Script | Does | Note |
| --- | --- | --- |
| `qc.sh NAME` | timeline + voicing + contact sheet | EP2 version is `scripts/qc_ep2.sh` |
| `qc_audio.py CLIP` | speech-band RMS per 100 ms | |
| `voicing.py CLIP` | pitch per 40 ms (`V`/`u`/`.`) | catches mute or breathy clips |
| `zoom.sh NAME START DUR [crop] [rows]` | 5 fps face strip | crop `w:h:x:y` in 1280×720 source pixels |
| `montage.py TAG NAME@SEC …` | cross-clip consistency sheet | one frame per accepted clip |
| `sync_check.py drift FILE` | per-segment audio offset vs source clip | Pearson correlation over ±1.5 s; trust rows with r > 0.6 |
| `sync_check.py cues` | speech timeline with subtitle cue marks | imports the episode's `build.py` |
| `sync_check.py windows` | every clip + card-voice window, flags silent / cut-off windows | EP3; run before every render |
| `listen_check.sh` (EP3 folder) | one labelled MP4 of every clip the owner must hear | file, seconds and expected line burned in |

## Code Examples
```sh
# contact sheet with timestamps
ffmpeg -v error -y -i clips/$1.mp4 -vf "fps=1,scale=256:-1,drawtext=fontfile='fonts/Nunito[wght].ttf':text='%{pts\:hms}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x2" -frames:v 1 build/qc_$1.png
# face strip during a speech window (both faces in one crop)
sh zoom.sh L05b 0.6 5.8 1000:380:120:110 7
# consistency montage for one location
python montage.py desk L01@5.0 L02f@4.6 L03@4.0 L04b@5.0 B1@1.5
# A/V sync of the file you are about to upload
python sync_check.py drift out/pudding_ep2.mp4     # expect "WORST |offset| (r>0.6): 0 ms"
```
```python
# qc_audio.py core: speech-band loudness per 100 ms
raw = subprocess.run([ff,"-v","error","-i",clip,"-ac","1","-ar","16000","-af","highpass=f=250,lowpass=f=3500","-f","s16le","-"],capture_output=True).stdout
a = array.array("h", raw); step = 1600
vals = [20*math.log10((math.sqrt(sum(x*x for x in a[i:i+step])/step) or 1)/32768) for i in range(0,len(a)-step,step)]
floor = sorted(vals)[len(vals)//5]
line = "".join("#" if v>floor+12 else "+" if v>floor+6 else "." for v in vals)
```

## Constraints
**MUST DO**
- Verify the *non-speaker's* mouth during every speech run, not just the speaker's. A static open "o" (surprise) or an open grin counts as open.
- Cut every clip right after its last word: no laughs or chuckles at the end of a scene (owner rule).
- Trim silent lead-ins longer than about 1 s unless they're a deliberate dramatic pause (note it in the log).
- Run the montage per location and keep characters and backgrounds consistent across all its clips (owner rule).
- Measure A/V sync on the delivered file before every upload, all the way to the last clip.
- Keep `edl.tsv` (accepted cuts) and `qc_log.txt` (failures, refusals, owner decisions).

**MUST NOT DO**
- Pass a clip on the 1 fps sheet alone when a face is small or in profile during speech. Zoom.
- Treat stamps, thumps or rumble as speech without checking the picture.
- Declare "no drift" from an intermediate file (`body.mp4`). EP2 did this and shipped two drifting uploads.
- Pipe `qc.sh` through `head`: it hides the 5–10 s rows of the voicing line, where second takes live.
- Dismiss a low-r drift row as an artifact. `r < 0.6` with a large offset on a short segment meant a **silent window** (EP3 H1); check it with `windows`.

## Decision Frameworks
| Finding | Action |
| --- | --- |
| Only the speaker moves, speech clean, solid voicing | PASS, trim to speech ± 0.3 s |
| Extra ad-lib or laugh after the line | PASS-partial, cut before it |
| Listener's mouth opens during the line | FAIL (or keep only the clean part) |
| Weak/scattered voicing, owner hears breath | FAIL, regenerate with "clear, full, normal-volume speaking voice" |
| Off-model / different background / emblem / real brand | FAIL, regenerate from the scene master |
| Clip cuts to a different background mid-way | PASS-partial only if both looks already appear in the episode; otherwise FAIL |
| `sync_check` offset grows along the episode | Fix the assembly (PCM segment audio), re-render, re-check before upload |
| Short line shows two speech bursts in its window (EP3 C08) | Treat as the line said twice even if one listen says once: cut to the first burst, confirm with the ASR check |
| Owner says subtitles don't match lip sync, offset is 0 | Subtitle timing: split the line into sentence cues at measured onsets |

## Common Pitfalls
- An open-mouth *smile* on the listener reads as talking. Prompt "lips pressed together, closed-lip smile, no grin, no teeth".
- Asking the listener to look "surprised" opens the mouth into an "o".
- Hand-covered whispers are fine; the mouth is hidden.
- Detail drift is easy to miss clip by clip (beak colour, eyelashes, a badge appearing on a cap). The montage shows it.
- A listener in profile (taxi-queue wide shot) needs a tight crop of the mouth (`zoom.sh NAME START DUR 160:110:X:Y 6`); at the normal strip size a small "o" looks like a closed mouth.
- **Repeated-phrase false match:** a short take followed directly by a second take of the same phrase can match the next segment (EP3 H3: `+1220 ms r=0.87`, exactly the 1.3 s segment length). Re-measure that segment with a ±0.4 s window (0 ms r=0.70) and check the next segment is 0 ms before calling it drift.
- `drift` used to skip segments under 2 s and never checked card voices. It now checks clips ≥ 1.0 s; card voices are covered by `windows`.

## Output Templates
```
S12n  7.4  10.0  BISCUIT  "Welcome to London!"  PASS Biscuit only; Pudding closed-mouth smile verified at 5 fps
O03   FAIL voice (owner listened): Ollie only breathes; voicing scattered V
seg 065 P06  at 275.8s  audio offset +0 ms  r=0.97
```
