# Skills from the Pudding EP.1–EP.3 sessions

Drafts as .md files for review. **Not added to `ai-work-skills` yet** (the owner asked for md files first).

## Use this one: `youtube-ai-edu-series-creator` (2026-11-21)

> **Owner rule (2026-11-21): read and update skills only in this repository.** Updated after EP.4 "Taxi" (Mac, new
> Meta AI account): fixed episode format and style constants (`references/04` §0), English-only burned text,
> "copy the previous episode's `build.py`", Mac/new-account reference `10`, Studio notes `07` §6a, lessons 18–22.

[youtube-ai-edu-series-creator/SKILL.md](youtube-ai-edu-series-creator/SKILL.md) is the single, reusable skill for
the whole job. It merges the five skills below with the experience of all three episodes.

| Part | Content |
| --- | --- |
| `SKILL.md` | 12-phase workflow with a gate per phase, constraints, decisions, the costliest pitfalls, templates |
| `references/01`–`09` | Episode design · Meta AI generation · clip QC · assembly and sync · thumbnail · SEO metadata · Studio upload · IP and policy · lessons log and owner rules |
| `scripts/` | Path-independent helpers (set `PY`), an example episode build, an example thumbnail, page helpers |

Read `SKILL.md` first, then only the reference for the phase in hand. New lessons go into that skill.

## Superseded (kept for history, not updated any more)

The five folders below are the per-episode drafts the single skill was built from.

| Step in this session | Repeatable? | Skill |
| --- | --- | --- |
| Character sheets → scene masters → single-speaker clips in Meta AI, download via video src | Yes, every episode | [meta-ai-video-production](meta-ai-video-production/SKILL.md) |
| Contact sheets + speech-band timeline to catch mouth overlap, dead air, drift | Yes, every clip | [ai-video-lipsync-qc](ai-video-lipsync-qc/SKILL.md) |
| Copyright/trademark/policy checks (voices, music, fonts, signs, made-for-kids) | Yes, every channel/episode | [youtube-ip-safe-ai-content](youtube-ip-safe-ai-content/SKILL.md) |
| Timeline-as-code assembly: cards, subtitles, original music + ducking, SRT | Yes, every episode | [edu-video-assembly-ffmpeg](edu-video-assembly-ffmpeg/SKILL.md) |
| SEO metadata (titles, tags, chapters, translations) | Partly | Not a skill yet: one episode isn't enough evidence. Revisit after 3 uploads with analytics |
| YouTube Studio upload: reuse details, thumbnail canvas, SRT injection, end screen, translations, playlist, ASR word check, readback | Yes, every episode (the owner drags the file) | [youtube-studio-upload](youtube-studio-upload/SKILL.md) |
| A/V sync and sentence-timed subtitles on the delivered file | Yes, every render | in [ai-video-lipsync-qc](ai-video-lipsync-qc/SKILL.md) and [edu-video-assembly-ffmpeg](edu-video-assembly-ffmpeg/SKILL.md) |

**Updated after EP.2 (2026-11-20):** refusal patterns and Meta's offered alternatives, detailed scene masters, naming the master by its look, solo-host master for lesson clips, voicing check for mute/breathy clips, cross-clip consistency montage, no-laugh trims, two-pass loudnorm, `build.py plan` burned-text dry run, ASR word check before the Studio work, end-screen/translation/playlist Studio notes. New scripts in the skills' `scripts/` folders: `voicing.py`, `zoom.sh`, `montage.py`, `qc_ep2.sh`, `sync_check.py` (QC), `dlimg.sh` (Meta AI), `build_ep2.py`, `thumbnail_ep2.py` (assembly). The A/V drift and sentence-cue fixes, and the new `youtube-studio-upload` skill, came from EP.2's re-uploads. EP.2 project: `E:\claude-work\pudding-ep2\`.

**Updated after EP.3 (2026-11-20):** Meta now refuses an adult character speaking to Pudding in the same frame; accepted alternative = adult-alone still master, cut as shot / reverse shot with `clip(crop=…)`. Reading the RMS rows (each row = 5 s), `sync_check.py windows` (every clip and card-voice window, flags silent or cut-off windows), drift for clips ≥ 1 s and the repeated-phrase false match, glyph check in `build.py plan` (Nunito has no "→"), `listen_check_ep3.sh` (one labelled owner-listen MP4), money-episode IP rules, the AI-note line. New scripts: `listen_check_ep3.sh`, `sync_check.py` (windows mode), `build_ep3.py`, `thumbnail_ep3.py`. EP.3 project: `E:\claude-work\pudding-ep3\`.

Supporting scripts (kept with the project at `E:\claude-work\pudding-ep1\`): `dl.sh`, `qc.sh`, `qc_audio.py`, `audio_gen.py`, `build.py`. When a skill is moved into the repo, copy the relevant scripts into its `scripts/` folder.
