# Changelog

All notable changes to this repository will be documented in this file.

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
