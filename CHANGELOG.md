# Changelog

All notable changes to this repository will be documented in this file.

## [2026-11-22] - EP.5 update to the YouTube series skill

### Added
- `youtube-ai-edu-series-creator/scripts/`: `build_example_ep5_mac.py` (latest template: EP.4 build + EP.5
  timeline), `listen.py` (Mac listen-check MP4), `zoomset.py` (stacked 5 fps face strips), `meta_queue_ep5.js`
  (Meta AI page helpers: paste prompts, attach masters, unattended clip queue).

### Changed
- `SKILL.md`: EP.5 results column (1 render, 1 upload), new decisions (listener exclamations, wet-umbrella drips),
  length budget, scheduling only on the owner's date.
- `references/02`: listener and continuity clauses from EP.5; edit-only-the-colour fix for an off-model master.
- `references/04`: Fast English label for a female speaker, length budget for a three-clip recap, card background
  = the episode's own master.
- `references/07`: §6b EP.5 Studio notes (Reuse details, Schedule, end-screen readback and times, thumbnail fonts,
  translations).
- `references/09`: EP.5 incidents and numbers. `references/10`: §6 attaching masters and sending prompts from page JS.

## [2026-11-21] - TikTok shorts skill: EP02-EP04 lessons folded in

### Changed
- `tiktok-ai-edu-shorts-creator/SKILL.md`: scheduling an owner-approved slot is in scope (never Post now); series
  spec + location rule in the project context; new constraints (face/cover montage on masters, whole-cut whisper,
  cover before Schedule), decision rows (character drift, eyeline, silent mouthing, clipped last word, cover check)
  and pitfalls (blank editor preview, swallowed Stroke/Shadow clicks, lazy Meta images, edit-instead-of-new).
- `references/01`: rule-accuracy and new-location checklist items, series consistency, format notes F1-F3.
- `references/02`: page-driving notes (hydration, hidden pane, lazy image viewer), fault→sentence table, character
  drift guard, per-episode location block, cover notes.
- `references/03`: face-crop consistency check, whole-cut whisper word check, 10 fps re-check, CRF 22 upload copy.
- `references/04`: cover-landed check by preview + pixels, frame-0 fallback, Talkoro caption pattern.
- `references/05`: rewritten for the EP04 flow (owner MP4 drag, description clear, AI switch, editor zoom-to-fit,
  font helper, Style re-clicks, cover, schedule picker, read-back in Content).
- `scripts/tiktok_studio.js`: blocks 1b, 2b, `__openFont`/`__pickFont`, 5 (cover pixels), 6 (schedule read-back).
- `scripts/meta_page.js`: block 3 (lazy image + viewer prompt box).
- `references/06-lessons-log.md`: EP04 rows 45-57.

## [2026-11-21] - EP.4 update to the YouTube series skill

### Added
- `youtube-ai-edu-series-creator/references/10-mac-new-account-and-end-to-end.md`: macOS setup, moving to a new
  Meta AI account, files the browser pane can't move, running the episode end to end.
- `youtube-ai-edu-series-creator/scripts/`: `build_example_ep4_mac.py` (EP.3 build + EP.4 timeline, location crops,
  two-account level match, English-only assert), `dlqc.py`, `zoom2.py`, `preview.py`, `thumbnail_example_ep4.py`.

### Changed
- `youtube-ai-edu-series-creator/SKILL.md`: end-to-end rule, series consistency ("KEEP CONSISTENT": copy the
  previous `build.py`), global channel (English only burned in), Mac + new-account context, Frank and Mabel,
  EP.4 results column, new constraints, decisions and pitfalls.
- `references/04-assembly-and-sync.md`: new §0 fixed episode format (section order, label text, style constants);
  Mac tooling notes; start from the previous episode's build.
- `references/07-studio-upload.md`: new §6a EP.4 notes (languages, SRT upload without the picker, end-screen
  times, thumbnail retry, translations, deleting the superseded upload).
- `references/09-lessons-log.md`: owner rules 18–22, EP.4 incidents and numbers.

## [2026-11-21] - TikTok shorts skill

### Added
- `tiktok-ai-edu-shorts-creator/`: vertical (9:16) TikTok lesson-short skill from Talkoro TikTok EP01 — `SKILL.md`,
  `references/01-episode-design.md` … `06-lessons-log.md`, macOS scripts (`qc.sh`, `qc_audio.py`, `voicing.py`,
  `mouth.sh`, `zoom.sh`, `asr.sh`, `build.sh`, `drift.py`, `make_srt.py`, `meta_page.js`, `tiktok_studio.js`).
- `README.md`: section on the new skill with a table of what became skill content and what stays elsewhere.

### Changed
- `youtube-ai-edu-series-creator/SKILL.md`: "When NOT to Use" now points Shorts / 9:16 work to the new skill.

## [2026-11-21] - Initial Commit

### Added
- `youtube-ai-edu-series-creator/`: Consolidated 12-phase reusable skill (`SKILL.md`), phase references (`references/01-series-and-episode-design.md` through `references/09-lessons-log.md`), and helper scripts (`scripts/`).
- Historical superseded draft skills kept for reference:
  - `meta-ai-video-production/`
  - `ai-video-lipsync-qc/`
  - `youtube-ip-safe-ai-content/`
  - `edu-video-assembly-ffmpeg/`
  - `youtube-studio-upload/`
- `README.md`: Overview of the consolidated skill and historical drafts from EP.1–EP.3 sessions.
