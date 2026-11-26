# 03 — Clip QC (lip sync, voice, consistency, trims)

Every generated clip is checked before it enters the edit list. The tools show *where* speech is and *whose*
mouth moves. They can't hear words: a person does that (section 5), and YouTube's automatic captions confirm it
after a Private upload (`07`).

## 1. Per-clip routine

1. `sh qc.sh NAME` prints the speech timeline and the voicing line, and writes a 10-frame contact sheet
   (`build/qc_NAME.png`, 1 fps, timestamped). Don't pipe it through `head`: that hides the 5–10 s rows, where
   second takes live.
2. **Read the speech timeline.** `#` = loud in the speech band for that 100 ms, `+` = medium, `.` = quiet. A
   speech segment is a run of `#`.
   **Each row is 5.0 s (50 characters). A run's time = the row label + its character index × 0.1.** Count from
   the row label every time. In EP.3 two second takes were cut from the wrong row and shipped silent in a render.
3. **Read the voicing line** (one character per 40 ms, so each row is 2.0 s): `V` = clear pitch, `u` = unvoiced sound, `.` = quiet. A
   real spoken line shows solid `VVVVVVVV` runs. Scattered `V` means breath, a whisper or no voice, even when
   the speech timeline looks like speech.
4. **Zoom on the faces** for each speech run: `sh zoom.sh NAME START DUR [crop] [rows]` (5 fps, timestamps, crop
   `w:h:x:y` in 1280×720 source pixels). Check that only the scripted speaker's mouth moves. Check the
   **listener** in every frame. A static open "o" or an open grin counts as open.
5. **Check the picture:** on-model details, same background as the master for the whole clip, no cut or zoom,
   no text, no emblem, no banned item, same art style throughout.
6. **Set in and out:** trim the silent lead-in; put the out point right after the last word.
7. **Decide** and record: accepted cuts in `edl.tsv`, everything else in `qc_log.txt`.

Why not `silencedetect`: these clips carry ambience above −32 dB, so it reported nothing useful. The speech
timeline is band-passed (250–3500 Hz) RMS per 100 ms, relative to the clip's own 20th-percentile floor.

```python
# qc_audio.py core
raw = subprocess.run([ff,"-v","error","-i",clip,"-ac","1","-ar","16000","-af","highpass=f=250,lowpass=f=3500","-f","s16le","-"],capture_output=True).stdout
a = array.array("h", raw); step = 1600
vals = [20*math.log10((math.sqrt(sum(x*x for x in a[i:i+step])/step) or 1)/32768) for i in range(0,len(a)-step,step)]
floor = sorted(vals)[len(vals)//5]
line = "".join("#" if v>floor+12 else "+" if v>floor+6 else "." for v in vals)
```

## 2. Decisions

| Finding | Action |
| --- | --- |
| Only the speaker moves, speech clean, solid voicing | PASS, trim to speech ± 0.3 s |
| Extra ad-lib or laugh after the line | PASS-partial: cut before it |
| Listener's mouth opens during the line | FAIL (or keep only the clean part) |
| Weak or scattered voicing; the owner hears breath | FAIL: regenerate with "clear, full, normal-volume speaking voice" |
| Off-model, different background, emblem, real brand, banned item | FAIL: regenerate from the scene master |
| Clip cuts to a different background part-way | PASS-partial only if both looks already appear in the episode; otherwise FAIL |
| A short line shows two speech bursts in its window | Treat it as the line said twice, even if one listen says once. Cut to the first burst and confirm with the word check (`07`) |
| Stamps, thumps or rumble look like speech | Check the picture before treating them as speech |
| Silent lead-in longer than about 1 s | Trim, unless it's a deliberate pause (note it in the log) |

## 3. Per-location consistency

Once a location's clips are accepted:
```sh
$PY montage.py desk L01@5.0 L02f@4.6 L03@4.0 L04b@5.0 B1@1.5   # -> build/montage_desk.png
```
One labelled frame per clip. Compare design details (beak colour, eyes, cap, collar), props, background and
layout. Regenerate the odd one out, or accept a small difference and tell the owner.

Found this way: a grey-beak Biscuit in 3 desk clips and 6 different backgrounds in the first belt clips (EP.2);
a beaded collar in the two-shot against a shimmer band in the solo master (EP.3, accepted and flagged).

Detail drift is easy to miss clip by clip. The montage shows it at once.

## 4. Things the 1 fps sheet won't show

- **Small or profile faces.** Zoom. A listener in profile in a wide shot needs a tight crop of the mouth
  (`sh zoom.sh NAME START DUR 160:110:X:Y 6`). At the normal strip size a small "o" looks closed.
- **An open-mouth smile** on the listener reads as talking.
- **Eyelashes** appear as small flicks at the eye corners; only the zoom strip shows them.
- **Mid-clip morphs:** a character turning to front view, gaining goggle eyes or an emblem.
- Hand-covered whispers are fine: the mouth is hidden.

## 5. The owner listen check

Ask once, in one file. Include:
- the first clip of every new character or new voice,
- every intentionally wrong line (Meta may "fix" it),
- any clip with a weak voicing line,
- slow, word-by-word lines (are all words there?),
- any short line with two speech bursts.

```sh
# listen.txt: one clip per line -> CLIP|in|out|label
# C08|2.5|5.2|Pudding: "How much is it?" - once or twice?
sh listen_check.sh listen.txt out/ep_listen_check.mp4
```
Each part shows its number, clip, seconds and the expected line on screen. Log the answer as
`OWNER LISTEN <date>: …`.

One listen can still be wrong. In EP.3 the owner heard a line once; YouTube's automatic captions showed it
twice, and the upload had to be replaced. For a short line with two bursts, cut to the first burst.

## 5a. Local word check when nobody listens (EP.8)

When the owner asks for no check-ins, run `whisper-cli` (Homebrew) with `~/.cache/whisper/ggml-small.bin` on every accepted
window: `tools/asr.sh NAME in out` (16 kHz mono WAV → transcript). EP.8: 18 of 18 lines read back word for word, including the
intentional mistake ("How to go to the big park") and a slow line in three parts. Expected noise: "Putting an Ollie" for
"Pudding and Ollie", "stream" for "street", sounds in brackets ("(sighs)") outside the speech. It does not replace the
automatic-captions check after upload, which still decides.

**Intentional mistakes:** whisper "repairs" grammar. Check the mistake line's token probabilities (`whisper-cli -ojf`) and prefer
mistakes with an extra content word; a dropped unstressed word ("are", "a") can't be proven (EP.9). `tools/qcset.py NAME:START:END …`
prints the ASR of several clips and stacks their sheets + 5 fps strips in one image.

**Near-identical words (EP.11, bored/boring):** prove them three ways: whisper on the exact window, its token probabilities (0.93–0.99), and the automatic
captions after upload. Reject a take when whisper hears an extra small word in several windows ("I'm **an** interested", p 0.74) and write the line so
it can be proven ("I am interested").

**Eye strip and envelope (EP.12):** `scripts/ep6_chrome_tools/eyez.py NAME:a:b:crop …` = 8 frames of one crop per row (eyes, listener's mouth); `env.py NAME a b` = speech runs with
every gap ≥ 0.2 s (finds the holes to cut and the second take of a line). Round windows to 0.1 s.

**Question tone and stutters (EP.13):** whisper on the exact window decides ("went to a party?" on the whole clip, a plain statement on the cut). Repeated or doubled words ("home
home", a second "do") show in the windowed run; cut before them or retake. `scripts/ep6_chrome_tools/zf.py NAME a b crop` = 9 big frames of the used window, `q.sh NAME` = whisper + speech runs + pitch.

**The word check says nothing about the picture.** EP.8's host clips passed ASR and were uploaded without anyone looking at
them; in one, Biscuit said "It's on your right" while pointing to the viewer's left. Look at a contact sheet of every clip
before upload, host clips included. For left/right/here/there lines, check the gesture against the **viewer's** side, or prompt
the host to keep the wings still. Compare every new character's clips with the sheet (brows, trousers), not only with the master.

## 6. Before and after rendering

These need the episode's `build.py` (see `04`):

| Command | Checks | Expected |
| --- | --- | --- |
| `$PY sync_check.py windows` | Every clip window and every card-voice window in `build.SEGS`. Flags `NO SPEECH` (wrong in/out) and `CUT START` / `CUT END` (a `#` in the first or last 100 ms = a word cut off) | `windows flagged: 0` before every render |
| `$PY sync_check.py drift out/<episode>.mp4` | Audio offset of each clip segment (≥ 1.0 s) in the **delivered** file against its source clip: Pearson correlation of speech envelopes over ±1.5 s | `WORST \|offset\| (r>0.6): 0 ms`, and 0 ms (±10) on every row to the last clip |
| `$PY sync_check.py cues` | Speech timeline of each cued clip with `^` at each subtitle cue start | Each `^` sits just before a speech onset |

Reading the drift rows:
- Trust rows with r > 0.6.
- **A low-r row with a large offset on a short segment is not an artifact.** In EP.3 `+890 ms r=0.38` was a
  silent window. Check it with `windows`.
- **Repeated-phrase false match:** a short take followed directly by a second take of the same phrase can match
  the next segment (`+1220 ms r=0.87`, exactly the 1.3 s segment length). Re-measure with a ±0.4 s window (`PAD = 40` in `sync_check.py`) and
  check that the next segment is 0 ms before calling it drift.
- Never declare "no drift" from an intermediate file. EP.2 measured `body.mp4`, and two drifting uploads shipped.

Save the final table as `sync_measurements.txt`.

## 7. What each check caught

| Check | Caught |
| --- | --- |
| Contact sheet | Trademark text on a screen and a real airport sign (EP.1); a realistic plane shot; background swaps |
| Zoom strip | Listener "o" mouths and open grins, eyelashes on two characters, morphing characters, a teen's small "o" visible only on a 160×110 crop |
| Voicing + owner listening | A teen's lines that were only breath in 3 clips (EP.2) |
| Montage | Grey beak in 3 clips, 6 different backgrounds, collar difference |
| `windows` / `drift` | Two silent second takes (EP.3); audio drifting more than 1.5 s late in two uploaded renders (EP.2) |
| Word check after upload | Two subtitle lines that didn't match the audio (EP.2); a line spoken twice (EP.3) |

Failure counts — EP.1: lip overlap 3, off-model 1, trademark text 1, scene inconsistency 8, refusal 1.
EP.2: off-model or drift 7, listener mouth 4, no audible voice 3, scene inconsistency 6, refusals 4.
