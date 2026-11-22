# 03 — Clip QC and rough cut (macOS, 9:16)

All scripts run **from the episode folder**: `sh <skill>/scripts/qc.sh C1_v1`. They need `clips/`, write to
`build/` and `out/`, and use Homebrew `ffmpeg` (no `drawtext` filter → tiles carry no burned timestamps; count
them), `whisper-cli` with `~/.cache/whisper/ggml-small.bin` (override with `WHISPER_MODEL`), and system `python3 -I`.
Tested on EP01 from the skill folder: identical QC output, rebuilt cut byte-identical, drift 0 ms.

## Per clip
| Step | Command | Read it like this |
| --- | --- | --- |
| Timeline + voicing + sheet + ASR | `sh qc.sh C1_v2` | Timeline: `#` runs = speech, each row 5.0 s, char = 0.1 s. Voicing: solid `V` = real voice. ASR line gives words and a rough segment time. Sheet `build/qc_NAME.png`: 10 tiles = 0-9 s |
| Find a face crop | `ffmpeg -ss 0 -i clips/C1_v2.mp4 -frames:v 1 -vf crop=200:200:X:Y build/probe.png` | Adjust until the mouth is centred. EP01 Mint in OTS master: `160:110:410:520`; Leo face (reverse): wide crop `380:300:60:380` (he moves) |
| Speaker mouth strip | `sh mouth.sh C1_v2 0 10 160:110:410:520` | 10 tiles per row = 2.0 s. Mouth must move only inside the speech runs |
| Listener from behind | `ffmpeg -ss IN -t DUR -i clips/C1_v2.mp4 -vf "fps=5,crop=260:300:0:420,scale=110:-1,tile=12x2" -frames:v 1 build/leo_jaw.png` | Cheek/stubble edge static, head doesn't turn. A small head shift is fine; jaw motion fails the window |
| Words of the cut / tail noise | `sh asr.sh C3_v1 1.0 5.9` and `sh asr.sh C3_v1 5.8 10` | Exact words incl. intentional mistakes; tails came back "(sighs)" in 4 of 5 clips |
| Prop logos | crop the prop at 4-5 times: `-vf crop=400:200:240:860` (laptop in EP01 OTS) | Any logo inside the cut = FAIL |
| Both faces at 5 fps | `sh zoom.sh C1_v2 0 7.2 720:420:0:240 6` | Overview when the crop is unknown |

Cross-clip montage (one frame per accepted clip, side by side):
```sh
F=""; for x in C1_v2@5.5 C4_v1@4 C2_v1@3 C3_v1@3 C5_v1@3; do n=${x%@*}; t=${x#*@};
  ffmpeg -v error -y -ss $t -i clips/$n.mp4 -frames:v 1 -vf scale=270:-1 build/mf_$n.png; F="$F -i build/mf_$n.png"; done
eval ffmpeg -v error -y $F -filter_complex hstack=5 build/montage.png
```
(zsh: loop over explicit items as above; `for r in "1 3"; set -- $r` does not word-split.)

Character consistency (series): put a 1:1 face crop of each new master next to the same character from the canon
episodes at the same scale (`ffmpeg -i masters/M3_v1.png -vf "crop=440:500:X:Y,scale=300:340"` per image, then
`hstack`). Do it on the masters before any clip (EP04 caught a younger, rounder Mint there) and again on accepted
clips (720p frames: crop the face 1:1, don't judge the 1 fps sheet). Eyeline: a speaker addressing the other
character must look at them for the whole line — eyes closed/looking down for a sentence = FAIL (brief blinks fine).

## In/out rules
- In: ~0.2 s before the first `#` of the line. Out: ~0.2-0.3 s after the last `#`, before any sigh/blink/grin.
- If the mouth moves silently before the audio (C1_v2), the in point goes just before the audio, not the mouth.
- Keep natural pauses inside one speaker's line (C2: 1.6 s pause kept).
- Log every clip in `edl.tsv` (accepted) or `qc_log.txt` (fails, reasons, decisions, provisional items).

## Rough cut
```sh
sh <skill>/scripts/build.sh out/epNN_<slug>_roughcut.mp4
python3 -I <skill>/scripts/drift.py out/epNN_<slug>_roughcut.mp4      # expect 0 ms, r≈1.00 on every segment
python3 -I <skill>/scripts/qc_audio.py out/epNN_<slug>_roughcut.mp4  # whole-cut timeline for SRT timing
ffmpeg -i out/… -af ebur128 -f null - 2>&1 | grep -E "I:|LRA:"      # EP01: -17.9 LUFS, left as is
```
- `build.sh` frame-aligns in/out to 24 fps and pads/trims audio to the video length. The first EP01 build without
  this drifted up to 30 ms by segment 5. `drift.py` uses the same alignment (otherwise it reports a false -20 ms).
- Output: 1080x1920 (720x1280 scaled up, lanczos), H.264 CRF 16, AAC 48 kHz stereo; EP01 = 10.4 MB for 22.5 s.
- Last frame of every segment (`-ss <segment end - 0.06>`): no laugh, open grin or closed eyes. C2's end showed a
  soft teeth smile 0.2 s after the word: accepted and flagged.
- **Whisper the whole delivered cut after every build and compare word by word with the script.** EP04's out point
  6.4 cut the last word "it" (whole-cut whisper: "I really like?"); per-clip checks had passed. Move the out point
  to keep the word (6.6), even if it ends on a smile while finishing it; flag that for the owner.
- Whisper "corrects" short broken phrases ("when finish" → "finished", EP03); if whisper can't confirm a deliberate
  error, put it on the owner listen list instead of regenerating. Before failing a clip for lip-sync seen at 5 fps,
  re-check that window at 10 fps (EP02 C5).
- Keep a CRF 22 copy for a 10 MB upload cap (Claude in Chrome `file_upload`): `out/*_upload_small.mp4`, drift 0 ms.

## Owner listen list (put in the report with rough-cut times)
New voices (first Mint, first Leo), the intentionally wrong line (ask them to *watch* the sync if the source take
had silent mouthing), the quiz clip.
