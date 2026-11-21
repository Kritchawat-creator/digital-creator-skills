---
name: edu-video-assembly-ffmpeg
description: Assemble a YouTube language-lesson episode (16:9) from QC'd clips with Python + Pillow + ffmpeg (imageio-ffmpeg), including animated text cards, sentence-timed burned-in subtitles, check/cross icons, countdown bars, original synthesized music ducked under speech, SFX, two-pass loudness, drift-free audio, and EN/TH .srt export. Use when cutting an AI-animated lesson without a GUI editor, or when asked for "no dead air", "add subtitles", "make it 5 minutes", "export srt", "subtitles don't match lip sync", "audio out of sync". Triggers: assemble video, ffmpeg edit, burn subtitles, music ducking, lesson cards, shadowing segment, quiz countdown, A/V drift, loudnorm.
---

# Educational Video Assembly (ffmpeg)

## When to Use
- Turning an EDL of accepted clips into a finished lesson video without CapCut/DaVinci.
- Adding the lesson structure: hook, story, phrases, mistake, fast/slow listening, shadowing, quiz, comprehension replay, cliffhanger, end screen.

## When NOT to Use
- Heavy motion graphics or character re-animation. Use a real NLE/animation tool.

## Core Workflow
1. Tooling in a project venv (no system installs): `imageio-ffmpeg` (bundled ffmpeg binary), `pillow`. Work files on E: (per user rule).
2. **Original audio:** `audio_gen.py` synthesises a 16-bar loop (Karplus-Strong plucks, C-G-Am-F, 104 bpm) and SFX (ding, buzz, pop, tick, whoosh, sting) in pure Python; it runs in a few seconds.
3. **Timeline as code:** `clip(name, in, out, sub, tag, icon, sfx, th)` and `card(dur, title, lines, badge, voice, countdown, sfx, srt, th)` calls build the episode. Each call records English and Thai subtitle text. Clips whose line has pauses get sentence cues from `CUES[name]` = `[(seconds from in point, EN, TH), …]`, set from measured speech onsets (`sync_check.py cues`).
4. **Render each segment** to the same spec (1920×1080, 30 fps, yuv420p, **PCM s16 48 kHz stereo in `.mov`**) so the concat demuxer can `-c copy`. Encode AAC once, at the very end. (AAC per segment made the audio drift late by ~35 ms per segment, >1.5 s by minute 3.)
   - Clip: lanczos upscale 1280×720 → 1080p, overlay a transparent PNG (tag/banner, or the subtitle when there are no cues), one subtitle PNG per cue with `enable='between(t,a,b)'`, timed icon overlay (`enable='gte(t,X)'`), sfx via `adelay` + `amix normalize=0`.
   - Card: Pillow PNG over a blurred scene frame with a cream wash; slow zoom with `scale=w='…*(1+0.045*t/D)':eval=frame,crop`; countdown with `drawbox w='W*max(0,1-(t-S)/L)'`; optional voice taken from a clip's audio.
5. **Music bed:** loop the music → `sidechaincompress` keyed by the dialogue → `amix` → PCM `build/mix.mov`. Then two-pass `loudnorm` (measure JSON → `measured_*` + `linear=true`) → `alimiter=limit=0.79:level=false` → AAC 192k. Music fades in and out.
6. Export `.en.srt` / `.th.srt` from the same segment table (one cue per segment or per sentence cue; identical consecutive Thai lines are merged).
7. Before rendering: `build.py plan` (chapter times + every burned-in string in `build/burned_text.txt` to spell-check + a **glyph check** that fails if Nunito/Baloo 2 lack a character) and `sync_check.py windows` (every clip and card-voice window has speech and no cut-off word).
8. Final QC on the **delivered** file: duration, contact sheet of the whole video, measured LUFS/true peak, `sync_check.py drift` (0 ms to the last clip), and a full watch by the owner. Burned-in text and sync can't be fixed after upload.

## Project Context (Pudding EP1)
- Segment pattern that filled about 5 min without dead air: hook 7 s → title → story about 70 s → "5 phrases" (clip + example card each) → common mistake → fast vs slow listening → shadowing (voice + 2.8 s countdown + ticks) → 3-question quiz (6 s timer + answer with voice) → "Watch again" replay → cliffhanger → 16 s end-screen card.
- Fonts: Baloo 2 (titles, weight 800), Nunito (body/subtitles, 800–850), both OFL.

## Project Context (Pudding EP2, 2026-11-20)
- Same pattern, 5:05, 68 segments, 13 clips with sentence cues (100 EN / 91 TH cues). Delivered: −14.6 LUFS, −1.2 dBTP, A/V 0 ms at every clip.
- It took three uploads: v1 had two subtitle/audio mismatches (caught by YouTube's automatic captions), v2 drifted (owner noticed "after 3 minutes"), v3 fixed both.

## Project Context (Pudding EP3, 2026-11-20)
- 5:07, 79 segments, 12 clips with sentence cues. Delivered: −14.5 LUFS, −1.5 dBTP, A/V 0 ms at every clip ≥ 1 s (fourth render; numbers corrected 2026-11-21 from a re-measure of the delivered file, the earlier −14.6 / −1.2 were EP.2's).
- `clip(..., crop="768:432:100:90")` crops a 1280×720 source before the 1080p upscale. Used to turn Biscuit-alone clips (Meta's alternative after a refusal) into a medium reverse shot so a two-character scene still reads as one conversation. 2.5× upscale of flat cartoon art stays clean.
- Lesson host clips with two takes are cut as **two segments** (take 1 wide, take 2 medium crop or Meta's own close-up), removing 3–5 s of dead air between takes.
- Short-of-target length was filled with teaching cards (prices, more questions, a 4th quiz question), not padding: 4:42 → 5:07.
- First render had two silent second takes (misread RMS rows) and "→" drawn as empty boxes in Nunito card lines. Both are now caught before rendering (`windows`, glyph check).

## Code Examples
```text
[0:a]asplit=2[voice][sc];[1:a]...,volume=0.30,afade=t=in:d=1.5[mus];
[mus][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];
[voice][duck]amix=inputs=2:normalize=0:duration=first[aout]          -> build/mix.mov (pcm_s16le)
loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=…:linear=true,alimiter=limit=0.79:level=false -> AAC 192k
```
```python
# sentence cues (build.py)
CUES = {"P06": [(0.0, "Pounds?", "ปอนด์?"), (1.7, "Oh no...", "แย่แล้ว..."),
                (4.0, "I don't have any British money!", "ฉันไม่มีเงินอังกฤษเลย!")]}
# each cue -> overlay ... enable='between(t,a,b)'; SRT gets one cue per sentence
```

## Constraints
**MUST DO**
- Same codec params in every segment (else concat breaks or desyncs), with PCM audio; one AAC encode at the end.
- Time subtitles to speech: a line with pauses gets sentence cues, never one subtitle for the whole clip.
- Measure sync and loudness on the delivered file, not on `body.*`.
- Escape commas inside ffmpeg expressions (`max(0\,…)`).
- Burn subtitles for every spoken line in language lessons, and upload the .srt files too.

**MUST NOT DO**
- Leave cards silent. Always use music, a pop/tick, or voice.
- Use downloaded music without a licence.

## Decision Frameworks
- Short of the target length → add teaching value (examples, replay with understanding, quiz), not padding or silence.
- Vertical over 3 min counts as long-form, but the owner chose 16:9, which is always long-form.

## Common Pitfalls
- In a language lesson, never write words run together ("Passportpleasepurposeofyourvisit?") to show fast speech. Beginners read it as correct spelling and the owner flagged it as an error. Keep correct text and show speed with a tag (FAST! / SLOW). Burned-in text can't be fixed after upload: YouTube doesn't allow replacing the video file, so this cost a full re-render and re-upload.
- **"Subtitles don't match lip sync" has two causes.** Whole-line subtitles shown before the words (fix: sentence cues) and real A/V drift (fix: PCM segments). Measure with `sync_check.py drift` to tell them apart; EP2 had both.
- `loudnorm` with `linear=true` doesn't limit peaks (0.0 dBTP measured); add `alimiter`.
- `silencedetect` doesn't work with AI clips that have ambience. Use speech-band RMS (see `ai-video-lipsync-qc`).
- Variable fonts in Pillow: call `set_variation_by_axes([weight])`.
- Background builds: pipe through `tail` only at the end, or progress output is hidden.
- **One-pass `loudnorm` misses the target** (EP2: −15.1 LUFS, −0.5 dBTP for a −14 / −1.5 target). Mix to `build/mix.mov` (PCM), measure with `loudnorm=…:print_format=json`, then apply `measured_*` + `linear=true`, and print the delivered file's integrated LUFS and true peak from a final measure pass.
- **Dry run before rendering:** `build.py plan` prints section start times (chapters) and writes every burned-in string (subs, tags, banners, card lines) to `build/burned_text.txt`. Spell-check that list; intentional mistakes must carry a ❌.
- **Burned-in tags must be true of the audio.** "slow → natural" was wrong when the measured second take was as long as the first; use "listen twice" unless the speeds are confirmed.
- **Quiz answer cards must match the voice under them word for word** (e.g. don't play "It's a small yellow bag." under the answer "a small yellow bag"). Pick a voice window that says exactly the card.
- **Thai subtitles:** keep each character's pronoun consistent across episodes (Pudding = ฉัน since EP1).
- Windows console (cp874) can't print "→": run with `PYTHONIOENCODING=utf-8`.
- **Nunito has no "→" glyph** (Baloo 2 does): EP3 card lines showed empty boxes. Use "=" or ":" in body text; `plan` now asserts glyph coverage per font (render the char and compare with the mask of U+E000).
- Typed prices ("£3 = three pounds") on our own cards are fine for a money episode; the no-money rule is about drawn notes/coins/portraits in AI images.
- Thai subtitles: keep Pudding's lines without polite particles (no ครับ), as in EP.1–2; example sentences for the viewer can use ค่ะ/ครับ.
- Glob-free sed on the build file mangled strings once; edit build lines with exact-string replacements and re-run `plan`.

## Output Templates
`out/<slug>.mp4`, `out/<slug>.en.srt`, `out/<slug>.th.srt`, chapters computed from cumulative segment times.
