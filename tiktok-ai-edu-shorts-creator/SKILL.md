---
name: tiktok-ai-edu-shorts-creator
description: End-to-end playbook for vertical (9:16) AI-animated English-teaching shorts for TikTok, about 20-30 s, and for keeping a multi-episode series consistent - TikTok-native lesson design (hook in 1-2 s, one point, sound-off text, loop, comment quiz, English only), 9:16 masters and single-speaker 10 s clips in Meta AI web with a character-drift guard and a new location per episode, macOS clip QC (speech timeline, mouth strips, whisper word check, eyeline, logo crops), frame-aligned ffmpeg rough cut with drift check, Meta AI cover with a 3:4 crop check, English SRT, and TikTok Studio web (description, Text overlays, AI label, cover check, Schedule only for an owner-approved slot). Use for the next TikTok/Reels/Shorts lesson, a 9:16 Meta AI short, clip QC, a TikTok rough cut, cover or subtitles, or filling in and scheduling a TikTok Studio post. Triggers: TikTok, tiktok studio, 9:16, short, reels, Talkoro TikTok, Mint Leo, cover TikTok, subtitles, schedule, next episode, series consistency.
---

# TikTok AI Educational Shorts Creator

One skill for one vertical lesson clip, from the script to a TikTok Studio post that is filled in, checked and
**scheduled only for a slot the owner approved** (never posted now on its own). Built from *Talkoro* TikTok EP01
"Open the light?" (2026-11-21, 22.5 s) and refined on EP02-EP05 (F2 solo, F3 meeting, F1 in a café, F4 POV quiz in a lift lobby; 5 posts
scheduled, drift 0 ms on all). It is the vertical sibling of `youtube-ai-edu-series-creator` (16:9, ~5 min), which it reuses for
Meta AI basics; every rule here came from a measured failure or an owner decision, logged in
`references/06-lessons-log.md`.

## When to Use
- Making the next short lesson clip for TikTok (or Reels / YouTube Shorts) with Meta AI characters.
- One stage of it: lesson design, 9:16 masters, clips, clip QC, rough cut, cover, subtitles, TikTok Studio.
- Starting another vertical series with a new cast (swap the bible; the method stays).

## When NOT to Use
- 16:9 long episodes with cards, music and burned subtitles: use `youtube-ai-edu-series-creator`.
- Realistic people, public figures, licensed music or TikTok's built-in sounds over speech.
- Posting now, deleting or changing account settings: the owner does these (or says "yes, post it" in chat).
  Scheduling is in scope only for slots the owner approved in chat.
- Caption / hashtag / posting-time strategy: one unposted episode is no evidence. Revisit after ~3 posts with analytics.

## Core Workflow

| # | Phase | What to do | Gate | Details |
| --- | --- | --- | --- | --- |
| 0 | Orient | Read the series consistency spec (if any), the cast bible (prompt blocks, style block, universal negatives), the series' memory/owner rules, the previous episodes' `qc_log.txt` and shared hand-over notes. Create `epNN-<slug>/` with `clips masters prompts build out cover subtitles`. | You can name the one point, the wrong line, the hook, the comment question and this episode's (new) location. | `01` |
| 1 | Lesson design | Review/improve `script.md`: one point, ≤5 single-speaker lines, hook line first, quiz to lens last (loops back), English-only on-screen text with timings, English caption. Fix shot geometry (who sits/stands, screen direction, props that make the premise true). Check the taught rule is exactly true. Keep `script_v1.md`. | Every line has one clip, one speaker, one master; every on-screen word is listed. | `01` |
| 2 | Masters | One 9:16 still per shot in the project's single Meta AI chat: over-the-shoulder A, reverse B, solo-to-lens C. Say VERTICAL 9:16, name the reference sheet by its look, restate blocks. | Each master is 1152x2048, on-model, no text/logo, saved to `masters/` as .webp + .png; face crops match the canon episodes at the same scale (series montage) BEFORE any clip. | `02` |
| 3 | Clips | One 10 s clip per line, "Animate the vertical <NAME-BY-LOOK> still image…", full character blocks, adult-proportions line, plain-laptop line, closing sentence last. Test the two-character clip first. Download each with curl at once. | Every line has a candidate; refusals logged with Meta's offered alternative. | `02` |
| 4 | Clip QC | `qc.sh`, `mouth.sh` on the speaker, a jaw/cheek strip on the listener seen from behind, `asr.sh` on the cut window and on the tail, logo crops of props, cross-clip montage. | `edl.tsv` has one accepted cut per line; `qc_log.txt` has every fail and decision. | `03` |
| 5 | Rough cut | `build.sh` (frame-aligned, 1080x1920, cuts/concat only), `drift.py` on the delivered file, whisper on the whole cut, last frame of each segment. | 0 ms offset on every segment; all lines present in order; no segment ends on a laugh, grin or closed eyes. | `03` |
| 6 | Owner listen | List new voices, the intentionally wrong line (Meta may "fix" it) and anything borderline with rough-cut timestamps. | Owner answered, or the items are flagged as provisional in the report. | `03` |
| 7 | Cover + subtitles | Cover from Meta AI with its own big English text (spell-check it); sidecar `subtitles/epNN_en.srt` timed on the delivered cut. | Cover text spelled exactly, inside the 3:4 grid crop; SRT cues don't overlap. | `04` |
| 8 | TikTok Studio | Owner drags the MP4 into your pane's upload tab. Then: description (English caption), AI-generated label on, Edit -> Text overlays from the script, cover (owner's Upload cover once, verify by preview + pixels, else frame 0), checks clean. Schedule only for an owner-approved slot. | Read-back done; Schedule pressed only for the approved slot and read back in Studio → Content; never Post now without a yes. | `05` |
| 9 | Close out | Report in the owner's language with files, timestamps to listen to, what is and isn't on the post; add lessons to `06`. | Report sent; skill updated. | `06` |

The owner is asked at fixed points: downloads/installs, first listen of every new voice, the intentional mistake,
posting now / any slot not yet approved (both publish), deleting anything. Ask early and once: batch the first-voice
check with the upload request and send the check file proactively (EP03: answer in ~3 min).

## Project Context (Talkoro TikTok — project-specific values)

| Item | Value |
| --- | --- |
| Account | @talkoro.learning; separate cast and content from the YouTube channel (never reuse YouTube characters) |
| Audience | Global English learners → caption, hashtags, on-screen text, subtitles **English only** (owner, 2026-11-21) |
| Required hashtags | **Every** description/caption ends with `#fyp #creatorsearchinsight` after the topic tags (owner, 2026-11-21) |
| Series spec | `~/Documents/Kritchawat-Projects/Series/talkoro-tiktok/docs/series-consistency-spec.md` — KEEP EVERYTHING CONSISTENT (owner); §3 location table: a different location every episode |
| Cast & prompt blocks | `~/Documents/Kritchawat-Projects/Series/talkoro-tiktok/docs/character-bible.md` (Mint, Leo, Khun Dao; style block; negatives). The chat link is recorded there, not here |
| Episode folders | `~/Documents/Kritchawat-Projects/Series/talkoro-tiktok/epNN-<slug>/` (EP01 = `ep01-open-the-light/`, the worked example) |
| Tools (macOS) | Homebrew `ffmpeg` (no drawtext), `whisper-cli` + `~/.cache/whisper/ggml-small.bin`, system `python3`, `sips` for .webp→.png |
| Browser | Meta AI and TikTok Studio signed in inside the desktop app's built-in browser pane (no file-upload tool; the owner drags the MP4 in). Each session opens its OWN tab and passes its tabId |
| Schedule slots | Batch approved 2026-11-21: 21 Nov 20:00, then 08:00 and 17:00 daily (ICT); status in `docs/batch-ep02-ep08-plan.md` |

## Constraints

**MUST DO**
- All pictures and video come from Meta AI, including cover text. Locally only cut, concatenate, scale and re-encode.
- One speaker per clip; the listener is seen from behind (OTS) or absent; only the quiz clip looks into the lens.
- Keep one screen direction per character for the whole episode (e.g. Mint looks screen-left, Leo screen-right).
- Restate every character's full prompt block in every prompt, plus "grown-up NN-year-old woman/man, adult
  proportions" for any character who drifts young (Mint: also the adult-face sentence in `02`); end every clip prompt with
  `Nobody laughs. No narration, no music, no laughing`.
- Put "the laptop lid is plain matte silver … NO logo, no mark of any kind" in every prompt with a laptop; check props
  at 4-5 timestamps per clip.
- Whisper-check the intentionally wrong word survives (C1 "open" did).
- Cut every clip right after its last word: every EP01 clip had a sigh or long blink after the line.
- English only on anything viewers read (this series). Reply to the owner in Thai.
- Every TikTok description/caption includes `#fyp` and `#creatorsearchinsight` (owner rule); read them back before Schedule.
- Series: copy the canon prompts word for word; new location each episode; run the cross-episode face/cover
  montage on the masters before any clip and on the final cut; the taught rule must be exactly true.
- Whisper the WHOLE delivered cut after every build and compare word by word with the script.
- Get the cover onto the post before Schedule (scheduled posts can't be edited); verify by preview + pixels.

**MUST NOT DO**
- Press Post or Discard, press Schedule for a slot the owner didn't approve, or navigate/reload the TikTok upload tab
  while work is unsaved.
- Click the AI-generated switch by coordinate (its "Learn more" link navigates away); use the JS helper.
- Burn subtitles or text into the video locally.
- Retry or reword a refused prompt to get around Meta's policy; ask what Meta can make instead.
- Pass a clip on the 1 fps sheet alone: zoom the mouth (speaker) and the cheek/jaw (listener from behind).
- Declare sync from intermediate files: run `drift.py` on the delivered MP4.

## Decision Frameworks
| Finding | Action |
| --- | --- |
| Speaker mouths silently before the audio starts (C1_v2: 1.0-4.4 s silent mouthing) | PASS-partial: cut in ~0.2 s before the speech run, mark for the owner to *watch* the sync |
| Logo appears on a prop (C1_v1 apple shape the whole clip) | FAIL, regenerate with the plain-prop sentence; don't say the brand's shape in the prompt |
| Logo appears only after the line (C4_v1 at 9.5 s) | PASS: it is outside the cut; note it |
| Sigh / long blink / grin after the line | PASS-partial: out point before it (`asr.sh NAME END 10` names the noise) |
| Listener's head turns, jaw moves, or face shows during the line | FAIL that window |
| Natural 1-2 s pause inside one speaker's line | Keep it (reads as thinking); don't jump-cut a single static shot |
| TikTok web fonts don't render ❌ ✓ ✗ | Use words + colour ("…? NO!", green "Turn ON…") |
| A character reads younger/different than in earlier episodes (EP04 café Mint) | Regenerate the masters as brand-new images with the face sentence, then the clips/cover that show that face; keep v1 files |
| Speaker looks down / closes eyes for a whole sentence to the other character | FAIL (eyeline rule); add "KEEPS her eyes open on <B> for the whole line" |
| Silent mouthing or open grin inside/after a short line | Regenerate with "ONE smooth flow … closed-mouth look between words" + "As soon as her last word is said, she closes her mouth" |
| Whole-cut whisper misses a final word | Move that segment's out point later; rebuild; re-run drift + whisper |
| Owner's cover upload: file input 0 but preview shows the cover | Landed — confirm with block 5 pixels, then Schedule |
| Standing scene comes back full-body / a character reads child-sized next to a taller one (EP05) | Regenerate as CLOSE OTS / chest-up, legs out of frame, level eyeline (lessons #58-59) |
| Schedule time picker clicks fall through to Location (EP05) | Scroll the picker columns (1 scroll = 1 step), read inputs, clear Location (#68) |

## Common Pitfalls
- `form_input`/value setters don't reach Meta AI's prompt box: click the visible box and type.
- `cmd+a` does nothing in the browser pane (Meta AI, TikTok description, TikTok editor): select with JS (`scripts/tiktok_studio.js`).
- An unseen 2048x1152 image after a 9:16 request is an old lazy-loaded image, not the result.
- Whisper's word timestamps are rough; trust the speech-band timeline for in/out points, whisper for words.
- The browser pane's emulated viewport (1400x900, needed for TikTok's editor panels) resets when the pane is resized
  or the turn ends: take a new screenshot before clicking by coordinates.
- TikTok's preview is a `<canvas>` (no `<video>`): verify overlays by playing it and zooming at each overlay time.
- TikTok editor preview blank (0x0 stage): zoom menu "100%" → "Zoom to fit". Stroke/Shadow "+" first clicks are
  often swallowed: zoom-check every layer's Style rows.
- A Meta AI image may not load until clicked; the click opens a viewer with its own prompt box — Escape before typing.
- A fix re-prompt can come back as an edit of the last image: say "Create a brand-new image from scratch".

## Output Templates
```
edl.tsv:  C1_v2  4.4  6.7  MINT  "Leo, can you open the light, please?"  PASS-partial (provisional: owner listen) …
qc_log:   C1_v1  FAIL trademark: apple-shaped logo on the laptop lid throughout; fix = plain-prop sentence in every prompt
```
Clip prompt skeleton: `references/02-meta-ai-vertical-generation.md`. Report outline: `references/06-lessons-log.md`.

## Not in this skill (on purpose)
| Kept elsewhere | Why |
| --- | --- |
| EP01-EP04 scripts, prompts, cut times | Episode-specific → `talkoro-tiktok/epNN-*/` (EP04 `ep04-really-like/` = latest F1 worked example, café) |
| Character blocks, chat link | Project data → the cast bible |
| Owner preferences (no laughs, English only, Meta makes all images, never post without approval) | Memory; cited here only as constraints |
| Caption/hashtag strategy, best posting time | No analytics yet |
| Chrome-extension troubleshooting, session hand-offs | One-off environment issues |
