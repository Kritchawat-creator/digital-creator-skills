# 04 — Assembly, subtitles, audio and sync

The episode is built by a Python script, not a GUI editor: the timeline is code, every render is repeatable, and
the same table produces the video, the chapters and the subtitle files.

## 0. Fixed episode format (keep it identical in every episode)

Owner rule "KEEP CONSISTENT" (EP.4): copy the previous episode's `build.py` and `audio_gen.py`; change only the
segments, masters and paths. EP.3 and EP.4 use this section order and **exactly** this label text:

1. Hook clip, banner **"Don't say this!"**, red cross + buzz
2. Title card **"Pudding Goes to London"** / "Episode N · <Topic>" (grey, 70) + sting
3. **"Last time on Pudding..."** + the previous cliffhanger clip
4. Location cards **"At the <place>..."** + story clips (FAST!/SLOW tags, cross/check icons)
5. **"Oh no, Pudding!"** / "But first... let's learn the English!"
6. **"5 Phrases for <topic>"** → per phrase: host take 1 tag `PHRASE i/5 · listen twice`, host take 2 tag
   `PHRASE i/5 · again` (medium crop), card badge `PHRASE i/5` + phrase / "You can also say:" / example (green)
7. **"Common Mistake"** + wrong/right clips + red/green card + 2–4 grammar cards
8. **"<Character>'s Fast English"** / "Can you understand him?" (her? for a female speaker, EP.5 Mabel — the only label that changes) + FAST!/SLOW/NORMAL clips + "= …" card
9. **"Say It With Pudding!"** / "Listen... then say it out loud!" → 5 cards badge `YOUR TURN i/5`, "Now you!",
   voice = host take 2, yellow countdown + 4 ticks
10. **"Quiz Time!"** / "4 questions. Answer before the timer ends!" → `Question N` (6 s countdown) + `Answer`
11. **"Write your answers in the comments!"**
12. **"Watch Again"** / "Now you understand every word!" + replayed story clips (no tags or icons)
13. Cliffhanger clips + host "Find out in episode <n+1>!"
14. End card 16 s **"Next: EP.<n+1> · <Topic>!"** / "Subscribe so you don't miss it!" + sting (end screen here)

Style constants (do not change): NAVY (31,42,68), CREAM (255,246,229), YELLOW (255,201,60), RED (229,72,77),
GREEN (46,173,107); Baloo 2 titles 112/800; Nunito lines /850; subtitle bar navy (31,42,68,215), Nunito 58/800,
wrap 1560, 70 px above the bottom; tag pill top-left (50,44); yellow banner top-centre Baloo 64; icons at
(W−230,300) r130 on clips and (W−200,H−200) r110 on cards; card background = the episode's master blurred 18 under
a 0.72 cream wash; card zoom +4.5 %; 34 px yellow countdown bar; music ×0.30 ducked by `sidechaincompress`; SFX
×0.55; two-pass loudnorm −14 LUFS / TP −1.5 + `alimiter` 0.79; H.264 crf 19, 1920×1080, 30 fps, AAC 192k.

Length budget (EP.5): a three-clip "Last time" recap (≈18 s) instead of one clip (≈7 s) pushed the measured plan to
5:29. Trim in this order: Watch Again to 4 clips, then the last extra grammar card. Keep the 14 sections and labels.
Card background = the episode's own main master blurred (EP.4 `taxi_master`, EP.5 `desk_master`).

Burned text is **English only** (global channel); each segment's `th` goes only into the `.th.srt`. `plan()`
asserts zero Thai characters on screen. Check the render with a 16-frame contact sheet next to the previous
episode's.

## 1. Tooling

- A project venv with `imageio-ffmpeg` (bundles an ffmpeg binary) and `pillow`. No system installs.
- Fonts: Baloo 2 (titles, tags, badges, banners; weight 800) and Nunito (body, subtitles; 800–850), both SIL OFL.
  Variable fonts in Pillow need `set_variation_by_axes([weight])`.
- `audio_gen.py` synthesises the music loop (16 bars, Karplus-Strong plucks, C–G–Am–F, 104 bpm) and the sound
  effects (`ding`, `buzz`, `pop`, `tick`, `whoosh`, `sting`) in pure Python in a few seconds. They are original,
  so there is nothing to license.
- Windows console (cp874) can't print "→": run Python with `PYTHONIOENCODING=utf-8`.
- Start from the **previous episode's** `build.py` (latest: `scripts/build_example_ep4_mac.py`, which is EP.3's
  build with the EP.4 timeline): copy it to `build.py` in the episode folder and replace the segments.
- macOS: system `python3` + Pillow and Homebrew ffmpeg work as they are (`FF = "ffmpeg"`, fonts in `fonts/`).
  Homebrew ffmpeg has no `drawtext`/`subtitles`; the build never needed them (text is Pillow PNG overlays).
- Clips from two Meta AI accounts can differ by ~10 dB: EP.4's `clip_gain()` measures each window and
  level-matches it to −18 LUFS before the mix. `sync_check.py` imports it as `build`, so keep that file name.

## 2. Timeline as code

```python
clip(name, t_in, t_out, sub=None, tag=None, banner=None, icon=None, icon_at=0.0, sfx=(), th=None, crop=None)
card(dur, title=None, lines=(), badge=None, icon=None, voice=None, sfx=(), countdown=None, srt=None, th=None)
```

| Argument | Meaning |
| --- | --- |
| `name, t_in, t_out` | The clip file in `clips/` and the accepted window from `edl.tsv` |
| `sub`, `th` | English burned-in subtitle and its Thai text for the `.th.srt` |
| `tag` | A corner tag such as `FAST`, `SLOW`, `NORMAL` (text + colour) |
| `banner` | A top banner ("Don't say this!") |
| `icon`, `icon_at` | `"cross"` or `"check"`, shown from that second |
| `sfx` | `[(name, at_seconds), …]` from `audio/sfx_<name>.wav` |
| `crop` | `"w:h:x:y"` on the 1280×720 source before the upscale. `768:432:100:90` turned a solo wide shot into a medium reverse shot; a 2.5× upscale of flat cartoon art stayed clean |
| `title`, `lines`, `badge` | Card text. `lines` = `[(text, colour, size), …]` |
| `voice` | `(clip, in, out, at)`: play that clip's audio under the card, starting `at` seconds in |
| `countdown` | `(start, length)`: a shrinking bar for quiz and shadowing cards |
| `srt` | Subtitle text for a card when it should differ from title + lines |

**Sentence cues.** A line with pauses gets one subtitle per sentence, not one for the whole clip:
```python
CUES = {"P06": [(0.0, "Pounds?", "ปอนด์?"), (1.7, "Oh no...", "แย่แล้ว..."),
                (4.0, "I don't have any British money!", "ฉันไม่มีเงินอังกฤษเลย!")]}
```
Times are seconds from the clip's in point, set about 0.2 s before each measured speech onset
(`sync_check.py cues`). Each cue becomes its own overlay with `enable='between(t,a,b)'` and its own `.srt` cue.
A whole-line subtitle shown before the words made the owner report "subtitles don't match lip sync".

## 3. Rendering

Each segment is rendered to the same spec so the concat demuxer can `-c copy`:

**1920×1080, 30 fps, yuv420p, PCM s16 48 kHz stereo, `.mov`.** AAC is encoded once, at the very end.

- **Clip segment:** crop (optional) → lanczos upscale to 1080p → overlay a transparent PNG (tag, banner, or the
  subtitle when there are no cues) → one subtitle PNG per cue → timed icon (`enable='gte(t,X)'`) → sound effects
  with `adelay` + `amix normalize=0`.
- **Card segment:** a Pillow PNG over a blurred scene frame with a cream wash; slow zoom with
  `scale=w='…*(1+0.045*t/D)':eval=frame,crop`; countdown with `drawbox w='W*max(0\,1-(t-S)/L)'`; optional voice
  from a clip window.
- Escape commas inside ffmpeg expressions (`max(0\,…)`).
- Same codec parameters in every segment, or concat breaks or desyncs.

**Why PCM:** with AAC in every segment, each segment added about 35 ms of audio delay in the mix step. By 2:20
the audio was more than 1 s late, and two EP.2 uploads shipped that way.

## 4. Audio mix and loudness

```text
[0:a]asplit=2[voice][sc];[1:a]…,volume=0.30,afade=t=in:d=1.5,afade=t=out…[mus];
[mus][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];
[voice][duck]amix=inputs=2:normalize=0:duration=first[aout]        -> build/mix.mov (pcm_s16le)

pass 1: loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json            -> measured values
pass 2: loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true,
        alimiter=limit=0.79:level=false:attack=3:release=60,aresample=48000   -> AAC 192k, +faststart
```
- The music loops under the whole episode, ducked by the dialogue, with a 1.5 s fade-in and a 3 s fade-out.
- **One-pass `loudnorm` missed the target** (−15.7 LUFS in EP.1; −15.1 LUFS and −0.5 dBTP on EP.2's first render
  for a −14 / −1.5 target). Two passes landed at −14.6 and −14.5.
- **`linear=true` doesn't limit peaks** (0.0 dBTP measured). Add the limiter.
- The script ends by measuring the **delivered** file and printing its integrated loudness and true peak.

## 5. Subtitle files

The same segment table writes `out/<episode>.en.srt` and `.th.srt`: one cue per segment or per sentence cue.
Identical consecutive Thai lines are merged (a slow, word-by-word English line keeps one Thai cue).
Timestamps go through integer milliseconds (`int(round(t*1000))` then `divmod`) to avoid float artifacts such as
`80.9999 → 01:20,000` landing in the wrong cue.

Cue counts: EP.1 63 EN / 63 TH; EP.2 100 / 91; EP.3 106 / 102.

## 6. Checks before rendering

```sh
$PY build.py plan          # no rendering
$PY sync_check.py windows  # expect "windows flagged: 0"
```
`plan` prints the total length and each section's start time (these are the chapters for the description) and
writes every burned-in string to `build/burned_text.txt`: subtitles, tags, banners, card titles and lines, cue
texts. Then:

- **Spell-check that list.** Intentional mistakes must carry a ❌ on screen.
- **Glyph check** (built into `plan`): fails if a font lacks a character. Nunito has no "→" (Baloo 2 does), and
  EP.3 card lines drew empty boxes. Use "=" or ":" in body text.
- **Tags must be true of the audio.** "slow → natural" was wrong when the second take was as long as the first.
  Use "listen twice" unless the speeds are measured.
- **Quiz answer cards must match the voice under them word for word.** Don't play "It's a small yellow bag."
  under the answer "a small yellow bag".
- **Never write words run together** ("Passportpleasepurposeofyourvisit?") to show fast speech. Beginners read
  it as correct spelling; the owner flagged it, and it cost a re-render and re-upload.
- Typed prices on your own cards ("£3 = three pounds") are fine in a money episode. The no-money rule is about
  drawn notes, coins and portraits in AI images (`08`).

## 7. Checks on the delivered file

```sh
$PY build.py                               # render (run long builds in the background; tail the log at the end)
$PY sync_check.py drift out/<episode>.mp4  # 0 ms (±10) on every clip row to the last clip
sh final_qc.sh out/<episode>.mp4           # duration, contact sheets (1 frame / 4 s), LUFS and true peak
```
Then look at the contact sheets: every card readable, no empty boxes, subtitles inside the frame, icons on the
right clips. The owner watches the whole episode before upload. Burned-in text and sync can't be fixed after
upload, because YouTube doesn't allow replacing the video file.

**"Subtitles don't match lip sync" has two causes.** Whole-line subtitles shown before the words (fix: sentence
cues) and real A/V drift (fix: PCM segments). `sync_check.py drift` tells them apart. EP.2 had both.

## 8. Episode numbers

| | EP.1 | EP.2 | EP.3 |
| --- | --- | --- | --- |
| Segments | — | 68 | 79 |
| Clips with sentence cues | 0 | 13 | 12 |
| Delivered loudness / true peak | −15.7 / −1.3 | −14.6 / −1.2 | −14.5 / −1.5 |
| A/V offset on the delivered file | not measured | 0 ms (third render) | 0 ms |
| Renders | not logged | 3 | 4 |

## 9. Small things that cost time

- Keep kept-for-reference renders under a different name (`build/<episode>_r1_bad_….mp4`) so `out/` always holds
  the current candidate.
- Edit build lines with exact-string replacements and re-run `plan`. A broad `sed` on the build file mangled
  strings once.
- Background builds: pipe through `tail` only at the end, or the progress output is hidden.
- Reused cuts from an earlier episode are copied into `clips/` as files (`ep2_P05.mp4`) with that episode's in/out
  points and cues, so the build has no cross-folder dependency.
