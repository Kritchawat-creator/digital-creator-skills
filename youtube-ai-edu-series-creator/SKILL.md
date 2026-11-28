---
name: youtube-ai-edu-series-creator
description: End-to-end playbook for producing and publishing one episode of an AI-animated educational story series on YouTube (16:9, about 5 minutes) - episode design from a series plan, consistent characters and scene masters in Meta AI, single-speaker talking clips, lip-sync / voice / consistency QC, timeline-as-code assembly with Python and ffmpeg (lesson cards, sentence-timed burned-in subtitles, original music, loudness, drift-free audio), thumbnail, SEO title, description, tags and translations, copyright / trademark / policy checks, and a YouTube Studio upload with readback and an automatic-captions word check. Use when asked to make the next episode, create a YouTube lesson video with AI, QC lip sync, remove dead air, add subtitles, make a cover, write caption and tags, or upload to YouTube Studio. Triggers: YouTube creator, new episode, EP, Meta AI video, lip sync, dead air, subtitles, srt, thumbnail, cover, SEO tags, YouTube Studio, end screen, playlist, made for kids, copyright, trademark, re-upload.
---

# YouTube AI Educational Series Creator

One skill for the whole job: from the series plan to a Private YouTube upload that has been checked.
It was built from five delivered episodes (*Pudding Goes to London* EP.1–EP.5, November 2026) and replaces five
earlier drafts (`meta-ai-video-production`, `ai-video-lipsync-qc`, `edu-video-assembly-ffmpeg`,
`youtube-ip-safe-ai-content`, `youtube-studio-upload`). Every rule below came from a measured failure or an owner
decision in those episodes; the history is in `references/09-lessons-log.md`.

## When to Use
- Making the next episode of an AI-animated lesson or story series for YouTube (16:9, about 5 minutes).
- Doing one stage of it: script, Meta AI masters and clips, clip QC, assembly, subtitles, thumbnail, SEO metadata,
  Studio upload, or replacing a bad upload.
- Starting a new series with the same method (new cast, new teaching language, new topic).
- Working on macOS or with a fresh Meta AI account (EP.4 moved from Windows to a Mac and to a new Meta AI account;
  `references/10-mac-new-account-and-end-to-end.md`).

## When NOT to Use
- Realistic people, real public figures, or licensed songs. That needs consent and licensing work this skill
  doesn't cover.
- Live-action editing or heavy motion graphics. Use a real editor.
- Legal disputes or takedowns. Escalate to the owner and a lawyer.
- Deciding the audience setting (made for kids), AI disclosure or Public visibility. The owner decides; this skill
  only prepares and applies their decision.
- Shorts / vertical 9:16 clips. Use `tiktok-ai-edu-shorts-creator` (built from Talkoro TikTok EP01, 2026-11-21): it
  covers 9:16 Meta AI masters and clips, macOS QC scripts, the rough cut, cover, SRT and TikTok Studio web.

## Core Workflow

Work through the phases in order. Don't start a phase until the previous gate is met. Run them **end to end
without asking after each step** (owner, 2026-11-21): decide routine QC calls (regenerate, crop, trim, shorten a
line) yourself and log them.

**Series consistency (owner: "KEEP CONSISTENT").** A new episode must look and sound like the previous one. Start
`build.py` and `audio_gen.py` by **copying the previous episode's files** and change only the timeline (clips,
lines, cards), the masters and the paths. Never redesign cards, subtitle bar, colours, fonts, labels, music, SFX or
loudness. The fixed section order and label text are in `references/04-assembly-and-sync.md` §0.

**Global channel (owner, 2026-11-21).** Burn **English only** into the video. Other languages go only into
caption tracks (English uploaded + Thai) and title/description translations (TH, ES, PT, VI, ID).

**Subtitles and translations on every episode (owner, 2026-11-23: "อย่าลืมใส่ subtitle translation").** No episode
goes Public or Scheduled until the Subtitles page shows **English** (uploaded `.en.srt`) and **Thai** (`.th.srt`) both
**Published**, cue count equal to the file, and the title/description translations **TH, ES, PT, VI, ID** all
Published. This is a hard gate in `references/07-studio-upload.md` §4a, even when the owner says "publish now".

| # | Phase | What to do | Gate before moving on | Details |
| --- | --- | --- | --- | --- |
| 0 | Orient | Read the series plan (*Pudding:* the season table, situation / phrases / grammar / cliffhanger per episode, is in Drive `pudding-ep1/docs/channel-plan.md` §5 — the next episode's topic and the cliffhanger come from there, not from memory), the cast bible and `Characters/README.md` (paste prompt blocks word for word), the previous episode's script (its "As-built" section), `qc_log.txt`, upload metadata and **its `build.py`**. Check which machine and which Meta AI account you are on (`10`). Create the episode folder; reuse fonts and scene masters. | You can state the episode's situation, key phrases, grammar point, mistake and cliffhanger, and which masters can be reused. | `01` |
| 1 | Episode design | Write `docs/<series>-epN-script.md`: structure with target times, one-speaker clip table with exact lines, host clips, cards, quiz, continuity and IP table, prompts. | Every spoken line is assigned to exactly one clip and one speaker; every on-screen word is listed. | `01` |
| 2 | IP and policy pre-check | List the banned items for this episode (real names, logos, money, flags…) and put them into every prompt. | The continuity and IP table names specific words and objects, not just "no logos". | `08` |
| 3 | Scene masters | One still image per location in the project's single Meta AI thread: 16:9, detailed background, fixed left/right positions, no text. Make a solo master for any character who speaks to the hero or hosts the lesson. A new speaking character gets a reference sheet (front, side, 6 expressions) in `Characters/` first; the owner picks the design. Name a business only after a web search shows no real one of that name in the city. | Each master is on-model, has no text or emblem, and is saved to `masters/`. | `02` |
| 4 | Clips | One 10-second clip per line, animated from the master, one speaker per clip. Download each clip as it finishes. | Every scripted line has at least one candidate clip. Refusals are logged with the alternative Meta offered. | `02` |
| 5 | Clip QC | For every clip: speech timeline, voicing line, contact sheet, face zoom on the listener, in/out points. Per location: a cross-clip montage. | `edl.tsv` holds one accepted cut per line; `qc_log.txt` holds every failure, refusal and decision. | `03` |
| 6 | Owner listen check | Build one labelled MP4 of the clips a person must hear: new voices, intentional mistakes, weak voicing, lines with two speech bursts. | The owner has answered. Tools can't hear words. | `03` |
| 7 | Assembly | Timeline as code: copy the previous episode's `build.py` (same look), replace the segments. Run `plan` (chapters, burned-text list, glyph check) and `sync_check.py windows`, then render, then check the delivered file: sync, loudness, whole-video contact sheet. | A/V offset 0 ms (±10) at every clip to the end, about −14 LUFS and at most −1 dBTP, no silent cards, burned text spell-checked, **0 non-English characters burned in**, contact sheet matches the previous episode. | `04` |
| 8 | Thumbnail | Dedicated Meta AI art without text, then local text with asserts. Check it at 1280, 320 and 168 px wide. | No text touches a character or leaves its pill; nothing sits in the bottom-right timestamp area. | `05` |
| 9 | Metadata | Write `docs/<series>-epN-upload-metadata.md`: title, description with chapters and links, tags, settings, translations, thumbnail brief. | Chapters come from `build.py plan`; tags are under 500 characters by Studio's counter. | `06` |
| 10 | Upload | **Upload the file yourself** from the owner's Chrome (owner, 2026-11-24): open `/videos/upload?d=ud`, run `scripts/ep6_chrome_tools/studio_upload_video.py <tab> out/<episode>.mp4` (bytes into the page, SHA-256 check, inject into the dialog's file input). Don't ask for a drag and never wait for the owner: upload as soon as QC passes ("อัพโหลด คลิปลง youtube เองได้เลย ไม่ต้องรอฉัน"). Fill details, thumbnail, audience, English subtitles, end screen, Private. Run the automatic-captions word check right after saving, before the slow steps. Then other subtitles, translations, playlist. | Every setting is read back on the edit page, including visibility and the thumbnail picture. The word check matches the burned subtitles. | `07` |
| 11 | Close out | Append "As-built" notes to the script, record the upload in the metadata doc, add new lessons to this skill. | Report sent with URL, duration, loudness, sync and open items. | `09` |

The owner is asked only at fixed points: installs and downloads, new character designs, the first clip of each
new voice, the listen check, audience and AI disclosure, anything Public, deleting an upload,
payments, and changes to an older episode.

## Project Context (Pudding Speaks English — project-specific values)

| Item | Value |
| --- | --- |
| Series | *Pudding Goes to London*, 12 episodes planned; beginner English (CEFR A1–A2) for teens and adults worldwide; not made for kids |
| Cast | Pudding (baby elephant, yellow backpack, no eyelashes), Ploy (Thai teen, mint hoodie), Ollie (British teen, striped scarf), Biscuit (pigeon officer, orange beak, plain navy cap; lesson host), Frank (adult red fox, taxi driver, EP.4), Mabel (adult grey goose, hotel receptionist, EP.4–5; small lashes allowed), Lily (adult cream cat, owns the café, plain orange apron, no bow, NO lashes or brows; EP.7 — Ollie works there at weekends, no "aunt"). Sheets in `Characters/` |
| Format | 1920×1080, 30 fps, about 5 min; clips from Meta AI web (10 s, 1280×720, 24 fps, native speech) |
| Folders | Windows (EP.1–3): `E:\claude-work\pudding-ep1\` (venv, fonts, `docs\channel-plan.md`, cast bible), `…\pudding-ep2\`, `…\pudding-ep3\` (also on Drive "Learn English"). Mac (EP.4 on): `~/Documents/Kritchawat-Projects/Series/pudding-speaks-english/` (`Characters/`, `docs/pudding-character-bible.md`, `pudding-ep4/`). |
| Per-episode record | `docs\pudding-epN-script.md` and `docs\pudding-epN-upload-metadata.md` hold the video URL, playlist and settings. Read them for IDs; they are not repeated here. |
| Tools | Windows: Python venv with `imageio-ffmpeg` and `pillow`. macOS: system `python3` + Pillow, Homebrew ffmpeg (no `drawtext`/`subtitles` — the build draws text as Pillow PNG overlays anyway). Fonts Nunito and Baloo 2 (OFL); Meta AI and YouTube Studio signed in, in the desktop app's browser pane |
| Meta AI | EP.1–3: thread "Pudding the baby elephant" (old account). From EP.4: new account, thread meta.ai/prompt/1c05c8c0-… (sheets and masters re-uploaded) |

Measured results (delivered files re-measured 2026-11-21):

| | EP.1 Airport | EP.2 Lost Bag | EP.3 Changing Money | EP.4 Taxi | EP.5 Hotel Check-in |
| --- | --- | --- | --- | --- | --- |
| Clips downloaded → accepted cuts | 34 → 20 | 43 → 22 | 26 → 21 (2 more refused) | 31 → 28 (6 host clips give 2 cuts each), 0 refused | 26 → 26 cuts from 21 clips (5 retakes), 0 refused |
| Duration | 5:05.2 | 5:05.0 | 5:07.2 | 5:11.1 | 5:06.1 |
| Loudness / true peak | −15.7 LUFS / −1.3 dBTP (one-pass) | −14.6 / −1.2 | −14.5 / −1.5 | −14.6 / −1.2 | −14.6 / −1.2 |
| Renders → uploads | not logged → 2 | 3 → 3 | 4 → 2 | 3 → 2 | **1 → 1** |
| Why it was re-uploaded | run-together words in a burned subtitle | subtitle text didn't match the audio; then audio drift | a line spoken twice under a once-only subtitle | Thai burned under every subtitle (channel is global); then a new card design instead of EP.3's ("KEEP CONSISTENT") | — (first episode shipped on one render and one upload: EP.4's `build.py` ported, listen check, `windows`, drift before the drag) |

Every re-upload came from burned-in text, sync or look, which YouTube can't replace in place. Phases 6, 7 and the early
word check in phase 10 exist to catch those before the full Studio work.

## Reference Guide

| File | Read it when |
| --- | --- |
| `references/01-series-and-episode-design.md` | Planning the episode, writing the script doc, filling 5 minutes without dead air |
| `references/02-meta-ai-generation.md` | Making masters and clips, wording prompts, handling refusals, downloading |
| `references/03-clip-qc.md` | Checking a clip, choosing in/out points, the listen check, consistency montage |
| `references/04-assembly-and-sync.md` | Building the timeline, subtitles, audio mix, loudness, sync checks |
| `references/05-thumbnail.md` | Cover art prompt, text layout, size checks |
| `references/06-seo-metadata.md` | Title, description, chapters, tags, translations, settings |
| `references/07-studio-upload.md` | Every Studio step, selectors, the word check, re-uploads |
| `references/08-ip-and-policy.md` | Copyright, trademark, voices, music, fonts, audience, AI tool refusals |
| `references/09-lessons-log.md` | Why each rule exists; owner rules; what each mistake cost |
| `references/10-mac-new-account-and-end-to-end.md` | Working on a Mac, moving to a new Meta AI account, files the browser pane can't move, running end to end |

| Script (`scripts/`) | Use |
| --- | --- |
| `dl.sh NAME URL` · `dlimg.sh PATH URL` | Download a Meta AI clip or image and print its specs |
| `meta_poll.js` | Page helper: wait for the next clip, stop on a refusal |
| `qc.sh NAME` | Speech timeline + voicing line + 10-frame contact sheet |
| `qc_audio.py` · `voicing.py` | The two audio lines on their own |
| `zoom.sh NAME START DUR [crop] [rows]` | 5 fps face strip for the listener's mouth |
| `montage.py TAG NAME@SEC …` | One frame per clip, to compare a location across clips |
| `listen_check.sh LIST OUT.mp4` | One labelled MP4 for the owner to listen to |
| `audio_gen.py` | Original music loop and sound effects, synthesised in Python |
| `build_example_ep3.py` | A complete episode timeline (copy it to `build.py` and replace the segments) |
| `sync_check.py windows` · `drift FILE` · `cues` | Silent or cut-off windows; A/V offset per clip; cue marks |
| `final_qc.sh FILE` | Duration, whole-video contact sheets, loudness |
| `thumbnail_example_ep3.py` | Thumbnail text layout with overflow asserts |
| `studio_inject.js` | Attach a file in Studio without a file picker |
| `build_example_ep4_mac.py` | EP.4 = EP.3's build ported to the Mac with the EP.4 timeline: location crops, two-account level match (`clip_gain`), `plan` asserts 0 Thai characters burned in |
| `dlqc.py NAME URL` · `zoom2.py NAME START END CROP` · `preview.py` | Mac QC: download + speech bursts + 10-frame sheet; 5 fps face strip; labelled preview of all accepted cuts |
| `thumbnail_example_ep4.py` | EP.4 thumbnail in the EP.3 layout |
| `build_example_ep5_mac.py` | EP.5 = EP.4's build with the EP.5 timeline (three-clip recap, card background = the episode's own master); the latest template to copy |
| `listen.py LIST OUT.mp4` · `zoomset.py OUT CROP NAME:START:END …` | Mac listen-check MP4 (labelled parts, −16 LUFS); stacked 5 fps face strips for several clips at once (EP.5) |
| `meta_queue_ep5.js` | Meta AI page helpers (EP.5): paste a prompt into the Lexical box, attach a master by fetch or from localStorage, run a queue of clip prompts unattended and collect the clip URLs |
| `ep6_chrome_tools/` | Driving the owner's own Chrome by AppleScript (EP.6–EP.7): `cjs.py` (JS in a tab), `inject.py` (master into meta.ai localStorage), `meta.py` + `runq.py` (clip queue), `translate_meta.py` (5 title/description translations), `push_file.py` + **`studio_upload_video.py` (the Studio video upload, no drag)** |
| `ep6_chrome_tools/` (EP.8 additions) | `asr.sh NAME in out` (local whisper-cli word check), `runimg.py` (image prompts from `prompts/images.json`, saves to `masters/`), `wait_visible.sh` (wait for a visible, hydrated meta.ai tab + `caffeinate -d`); `meta.py` takes `key1+key2` to attach two images |
| `ep6_chrome_tools/` (EP.9 additions) | `meta.py` rewritten (waits for a running reply, resends on service overload, reload every 4 min, `RESUME=1`), `runq.py` (8 tries), `cjs.py` (45 s timeout), `wait_visible.sh` (checks the lock before touching Chrome), `qcset.py` (ASR + sheet + strip for several clips at once) |
| `ep6_chrome_tools/` (Everyday English EP.1 additions) | `asrp.sh NAME in out` (whisper on a window + token probabilities, proves a mistake word), `activate_meta.sh` (finds the meta.ai tab's index each time; a hard-coded index broke when tabs moved), `stack.py OUT NAME…` (stack several clips' contact sheets) |
| `ep6_chrome_tools/` (Everyday English EP.2 additions) | `kq.sh NAME a b` (two-shot clip QC: whisper, speech runs, speaker + listener mouth strips, full frames); `kq.sh` uses living-room crops and needs `tools/eyez.py` + `build/env.py`, so copy it into an episode folder first. The episode's `Series/family-english/ep02/build.py` has `card(still=png)` (a full-frame still with the cards' zoom) and a default crop for every clip of a location |
| `ep6_chrome_tools/` (Everyday English EP.3 additions) | `splitcheck.py` (whisper EVERY unique window of `build.py` on the whole window + two overlapping halves, flags repeated / missing words: run before every render), `final_pass.py` (redo only the loudnorm + limiter + AAC pass from `build/mix.mov` and print ebur128 I + true peak). The episode's `Series/family-english/ep03/build.py` adds a per-clip default crop dict (`LOC`), a 3-frame-grid assert, `END_TITLE`, quiz options on their own line (`\n`) and limiter 0.70. `kq.sh` now takes the mouth crops from `TC=` / `IC=` (measure them on the master resized to 1280x720 first: the saved PNG is 2048 px) |
| `ep6_chrome_tools/` (Everyday English EP.4 additions) | `grid.py` (one frame per unique window of `build.py` with its crop -> `build/grid.png`), `mkmeta.py` (`build/meta.json` from the metadata doc + chapters from the timeline + the end-card start; asserts the EP number), `w.sh NAME…` (wait for each clip in a runq log, then whisper + speech runs). The episode's `Series/family-english/ep04/build.py` adds `(name, t_in)` CUES keys |
| `ep6_chrome_tools/` (Everyday English EP.16, finale) | `translate_meta2.py` (Studio's NEW Languages page, 28 Nov 2026: Add language -> a `ytcp-dialog` named after the language with two `#textbox` (title, description) + **Update**). Thai subtitles: open the language row's button -> dialog -> Subtitles **Add** -> Upload file -> With timing -> Continue -> file into `input#captions-file-loader` -> Publish. `Series/family-english/ep16/build/_seg.py` has the 15-question finale review quiz (answers = each episode's ORIGINAL correct-line clip as card voice) |
| `ep6_chrome_tools/` (Everyday English EP.13) | No new scripts. `Series/family-english/ep13/build/probe.py` (one Meta send per 15 min during an outage, chained to the rest of the queue); `ep13/tools/make_prompts.py` has BAKERY_NEG (shop bans: no glass case, till, money, prices, menu, signs, lettering on cakes/boxes, other customers) and the indoor REAL wording ('floor line') |
| `ep6_chrome_tools/` (Everyday English EP.12) | `f0g.py` (pure-Python pitch with an octave guard; over-corrects low, use it only to compare clips). `Series/family-english/ep12/build/_seg.py` has `cliff(ring=False)` (replay the cliffhanger without its still) and two voice-over stills (STILLV: Ben over the closed toy box, Grandma over the phone); `tools/make_prompts.py` has `grandma()` (a no-people clip used for its audio only) and `GARDEN_NEG` (outdoor bans) |
| `ep6_chrome_tools/` (Everyday English EP.11) | No new scripts. `Series/family-english/ep11/build/_post.py` fixes the glyph check (compare with the font's .notdef, both fonts); `ep11/build/_seg.py` splits a SLOW line over two windows of one clip (second crop closer) and keeps the EP.10 recap as STILLV |
| `ep6_chrome_tools/` (Everyday English EP.10) | `cardcheck.py` (renders every text card of `build.py` before the render and prints each title/line that wraps), `wordcheck.py` (no probe past a window end: it crashed on a last word timed beyond the window), `activate_meta.sh` (tab guard for a parallel session's Studio tab). The episode's `Series/family-english/ep10/build/_seg.py` uses `STILLV` for a visible character's line (voice over a no-people still) and a 5-question quiz with a word-order question |
| `ep6_chrome_tools/` (Everyday English EP.9) | `wq.sh NAME…` (wait for each clip of a runq log, then `q.sh`), `f0oct.py` (pitch with an octave guard: men only). The episode's `Series/family-english/ep09/build/` has `clip(still=...)` (voice over a still: `_seg.py` STILLV + `_post.py`), `grid.py` showing the still, `mkmeta.py` asserting every chapter >= 10 s, and a pre-render render of every text card (`build/cardcheck.png`: the EP.9 cliff title wrapped) |
| `ep6_chrome_tools/` (Everyday English EP.8) | `wordcheck.py` (whisper `-ml 1` word timings on every window of `build.py`: flags a word longer than max(0.9 s, 0.1 s per letter + 0.2), a fragment, an extra or repeated word, and 0.8 s probes around every word of >= 6 letters; flags EP.7's stuttered "decorations" (1.51 s) and passes the clean retake (0.92 s); run with `splitcheck.py` before every render). The episode's `Series/family-english/ep08/build/_seg.py` lets a PHRASES take 2 / shadow voice come from another clip (`("H5b", a, b)`); `mkmeta.py` merges the cliff-replay chapter into Watch Again |
| `ep6_chrome_tools/` (Everyday English EP.7) | No new scripts. `Series/family-english/ep07/build/_seg.py` adds `QUIET` (per-clip loudness target for no-speech clips, read by `clip_gain` in `_post.py`); `runq.py` takes `QUEUE=prompts/queueN.json` (it loads the queue at start: restart it after a prompt fix); `tools/make_prompts.py` has the DRY v2 rain clause and a no-people LAMP clip prompt |
| `ep6_chrome_tools/` (Everyday English EP.6) | No new scripts. The episode's `Series/family-english/ep06/build.py` is assembled from `build/_pre.py` + `build/_seg.py` (timeline only) + `build/_post.py`; `MX_ICON` sets the cross/buzz just after the mistake; `mkmeta.py` finds the cliff replay by (name, t_in) when a clip has two windows. Content-list readback: count `ytcp-uploads-dialog` (0) first; a generic `ytcp-dialog` "Close" element is always there |
| `ep6_chrome_tools/` (Everyday English EP.5 additions) | `lsbackup.py TAB KEY` (read a meta.ai localStorage key back to `masters/_ls_backup/KEY.webp` before freeing it), `bands.py CLIP a b …` (4-band levels of a window: tells a quiet ambience/'[MUSIC]' bed from speech). The episode's `Series/family-english/ep05/build.py` adds a still cutaway between two windows of one clip (a `("DOGSTILL",)` marker in a story list) and the mistake's cross + buzz placed after the line |
| `ep6_chrome_tools/` (EP.13 additions) | `q.sh NAME…` (whisper + speech runs + pitch in one go), `zf.py NAME a b crop [n]` (big frames of the used window), `sheet.py`, `es_open.py` (re-open the end screen of an uploaded video to read or fix the times) |
| `ep6_chrome_tools/` (EP.12 additions) | `eyez.py` (8-frame eye / mouth strip), `env.py` (speech runs and gaps), `meta.py` (md5 check for images too, "Something went wrong" = service fault) |
| `ep6_chrome_tools/` (EP.11 additions) | `meta.py` (md5 check so an old clip under a new URL is never taken as new; a lost reply is resent after two dead reloads), `runimg.py` (accepts Meta's own "make it again" offer), `asr_window.sh` (whisper per window), `pitch_check.py` (`clip in out` lines on stdin → median pitch, to compare a voice with earlier episodes) |
| `ep6_chrome_tools/` (EP.10 additions) | `studio_steps_ep10.txt` (the complete Studio pass as commands), `st.py` + `es.py` (Studio helpers), `meta.py` (reload 90 s, limit 660 s), `runimg.py` (8 tries on overload), `qcset.py` (several windows of one clip) |

Set `PY` to the venv's Python before running the shell scripts
(`export PY=/e/claude-work/pudding-ep1/.venv/Scripts/python.exe`). They run from the episode folder and expect
`clips/`, `fonts/`, `build/` and `out/` there.

## Code Examples

One episode, in commands (run from the episode folder):
```sh
export PY=/e/claude-work/pudding-ep1/.venv/Scripts/python.exe PYTHONIOENCODING=utf-8
sh dl.sh C02 "<clip url from the Meta AI page>"      # after each generation
sh qc.sh C02                                          # timeline, voicing, sheet -> build/qc_C02.png
sh zoom.sh C02 1.0 4.0 1000:380:120:110 5             # listener's mouth during the line
$PY montage.py counter C02@3.0 C04@2.0 C06@2.0        # same location, same look?
sh listen_check.sh listen.txt out/ep_listen_check.mp4 # owner listens
$PY build.py plan                                     # chapters, burned_text.txt, glyph check
$PY sync_check.py windows                             # expect "windows flagged: 0"
$PY build.py                                          # render
$PY sync_check.py drift out/<episode>.mp4             # expect "WORST |offset| (r>0.6): 0 ms"
sh final_qc.sh out/<episode>.mp4                      # duration, sheets, LUFS, true peak
$PY thumbnail.py                                      # asserts fail if text overflows
```

Clip prompt skeleton (single speaker, animated from a scene master):
```
Animate the same <location> still image again (<describe the master by how it looks: who is LEFT, who is RIGHT,
their fixed details, two background objects>) into a NEW 10-second HORIZONTAL 16:9 video. ONE continuous static
shot, no cuts, no zoom, no new text or signs, same flat cartoon style for the whole video. The background stays
EXACTLY the same as the still image. <Speaker> <small action> and, starting within the first second, says
<manner> in a CLEAR, FULL, NORMAL-VOLUME speaking voice: "<exact line>". ONLY <Speaker> speaks. <Listener> does
NOT speak: lips pressed together the entire video, calm closed-lip smile, only blinks. <Episode's banned items>.
No narration, no music, <quiet ambience>. Nobody laughs. No laughing.
```

Timeline as code:
```python
# (seconds from the clip's in point, English, Thai), set from measured speech onsets
CUES = {"C02": [(0.0, "Hello!", "สวัสดี!"), (1.7, "I'd like to change some money, please.", "ฉันอยากแลกเงินหน่อย")]}
MED = "768:432:100:90"                      # crop of the 1280x720 source -> medium reverse shot
clip("A1", 0.5, 3.0, sub="Where I can change money?", icon="cross", icon_at=1.2, sfx=[("buzz", 1.3)],
     th="ฉันแลกเงินได้ที่ไหน? (เรียงคำผิด)")
clip("C02", 1.0, 5.2, sub="Hello! I'd like to change some money, please.", th="สวัสดี! ฉันอยากแลกเงินหน่อย")
clip("C03", 4.0, 6.7, sub="Sure! How much would you like to change?", tag=FAST, crop=MED, th="…")
card(2.4, title="At the exchange counter...", sfx=[("whoosh", 0)], th="ที่เคาน์เตอร์แลกเงิน...")
card(6.0, badge=("Question 1", NAVY), lines=[L("Put the words in order:  is / How / it / much", NAVY, 76)],
     countdown=(0.8, 5.0), sfx=[("pop", 0.1)] + [("tick", 0.8 + k) for k in range(5)], srt="…", th="…")
card(3.0, badge=("Answer", GREEN), lines=[L("How much is it?", GREEN, 92)], icon="check",
     voice=("H3", 5.8, 6.8, 0.6), sfx=[("ding", 0.1)], srt="How much is it?", th="…")   # voice = (clip, in, out, at)
```

## Constraints

**MUST DO**
- **REAL gate (Owner rule 2026-11-27 (hard gate): "ให้ สัดส่วน element และองค์ประกอบฉาก สมจริง สมมาตร สมเหตุสมผล" — element proportions and scene composition realistic, symmetric/balanced and logical.)** Put a REAL clause in every image and clip prompt (`REAL` in `Series/family-english/ep10/tools/make_prompts.py`) and check every master, `build/grid.png`, contact sheet, insert and thumbnail against: (1) proportions — props, clothes, furniture real size next to the characters; adults clearly taller than children; an older sibling a little taller; (2) bodies — two arms, two hands, five fingers, eyes same size and level, no merged or extra limbs; (3) placement and perspective — nothing floats, nobody stands on furniture, one floor line, clothes hang on a rail or lie flat; (4) layout — furniture against walls, windows/doors plausible, nothing merges; (5) composition — balanced and symmetric, a single subject centred, two characters balanced left/right with meeting eyelines, no crop through a head or hand. Log a `REAL` line per batch in `qc_log.txt`; retake what fails.
- Keep one Meta AI thread per project, and one scene master per location. Name a master by how it looks, never
  by a label in quotes.
- One speaker per clip. State the listener's mouth for the whole clip. Restate each character's distinguishing
  details in every prompt.
- Check the listener's mouth frame by frame during every speech run, and cut each clip right after its last word.
- Keep `edl.tsv` (accepted cuts) and `qc_log.txt` (failures, refusals, owner decisions) as you go.
- Get a person to listen before rendering: tools can see speech, not words.
- Burn subtitles for every spoken line with correct spelling, timed per sentence. Export `.srt` files too.
- Render segments with PCM audio and encode AAC once at the end. Measure sync and loudness on the delivered file.
- Upload Private. Read back every setting after saving. Run the automatic-captions word check before the slow
  Studio steps.
- Record each asset's source and licence, and each upload's state, in the episode docs.
- Put work files where the owner keeps them: Windows `E:\claude-work\<series>-epN\`; Mac `Series/pudding-speaks-english/<series>-epN/`.
- Copy the previous episode's `build.py` and `audio_gen.py` for the look and sound; change only the timeline.
- Burn English only (global channel). `build.py plan` asserts zero Thai characters on screen.
- Re-attach the scene master with every clip prompt in a long or new Meta AI thread (Meta loses access to
  uploaded images after a few turns).
- Plan a crop for any location where the model keeps inventing text (canopy signs, meters) and use it on every
  clip of that location.
- Run `build.py plan` with estimated windows as soon as the timeline is written, and again with measured windows:
  a three-clip "Last time" recap adds ~11 s (EP.5 measured 5:29 → trimmed Watch Again to 4 clips + one grammar card).
- Scheduling Public is the owner's call; when they give a date ("Schedule next Saturday 08:00"), resolve it against
  today's date, check Studio's time zone (GMT+7 local on this channel) and read back the "Video scheduled" text.

**MUST NOT DO**
- Reword or retry a prompt to get around an AI tool's refusal. Ask what it can make instead and accept that.
- Show real names, logos, emblems, flags, banknotes, coins or portraits. Don't prompt "in the style of" anyone.
- Use an AI tool's built-in music or song lip sync, a voice without clear commercial rights, or downloaded music
  without a licence.
- Write words run together to show fast speech, or leave a card silent.
- Declare "no drift" from an intermediate file, or pass a clip from the 1 fps sheet when a face is small.
- Set the audience, AI disclosure or Public visibility, delete an upload, or change an older episode without the
  owner saying so in chat.
- Click through a leftover upload dialog in another tab: its visibility step can have Public preselected.
- Click the pencil on "English (automatic captions)": it opens "Overwrite track" for the uploaded English captions.
- Redesign the episode format (cards, labels, music) without the owner asking for it.
- Commit or push to a skills repository without the owner's permission for that commit.

## Decision Frameworks

| Situation | Decision |
| --- | --- |
| Clip is clean but has an ad-lib or laugh after the line | Trim; don't regenerate |
| Listener's mouth opens, character off-model, background changes, emblem or real brand appears | Regenerate from the master with the missing detail restated |
| Voicing line is scattered, or the owner hears breath instead of words | Regenerate with "clear, full, normal-volume speaking voice" |
| Meta refuses a prompt | Log it, ask "what version would you be able to make instead?", accept the offer, restructure the scene (for example shot / reverse shot) |
| A short line shows two speech bursts in its window | Treat it as said twice: cut to the first burst and confirm with the word check |
| Episode is short of the target length | Add teaching value (examples, extra questions, replay with understanding), never padding or silence |
| "Subtitles don't match lip sync" | Run `sync_check.py drift`. Offset grows → audio pipeline (PCM segments). Offset 0 → subtitle timing (sentence cues) |
| Burned-in text or sync is wrong after upload | Re-render, upload as a new video, the owner deletes the old one |
| Only a caption file is wrong | Edit the SRT in place |
| Licence or right is unclear | Leave the asset out and use an owned or clearly licensed one |
| Previous episode is Private while the new one would link to it | Tell the owner viewers can't open it; let them choose when to link |
| Meta AI thread or account is gone | New thread: upload the sheets, then the masters, by in-page fetch → DataTransfer (`10`); check one clip per recurring voice with the owner |
| The model keeps putting text on a background (sign, meter, screen) | Crop it out for every clip of that location before regenerating more |
| A two-character clip where the listener's mouth moves during part of the line | Keep the clean part and shorten the line; don't splice two takes of a static shot |
| The owner says "keep consistent" | Compare frames with the previous episode side by side; port its code instead of matching by eye |
| A listener's mouth moves during a short exclamation ("Oh no!") in a two-shot | Twice in EP.5, even with "mouth stays shut": drop the exclamation and keep the clean sentence (or give it to an adult-alone/solo shot) |
| A teen with a wet umbrella in the master | Meta adds rain drips running down his face (reads as tears): add "his hair and face are DRY, only the umbrella is wet" to every prompt |
| A location where the hero, a teen and an adult all speak (EP.7 café) | Three masters: teen + hero two-shot for the teen's lines, a hero-only close shot for the hero's lines, an adult-alone shot for the adult's lines (0 listener faults in EP.7) |
| A new adult-alone master in a place that already has a master (EP.8 Walter at the canal) | Attach the place master AND the character sheet in the same prompt (`meta.py key1+key2`); one alone drifts the design, the other drifts the place. If the adult is small in frame, crop every clip of them (`768:432:300:280`) |
| The owner asked for no check-ins, so nobody listens | Word-check every accepted window locally with `whisper-cli` (`~/.cache/whisper/ggml-small.bin`, already on the Mac): `tools/asr.sh NAME in out`; the automatic-captions check after upload still decides |
| A lesson about feelings (bored, tired, excited): the model acts the feeling (EP.11) | Host prompt: "only TEACHES these words: he does not act the feeling … same calm, cheerful teacher face, eyes big, round and fully open". Hero: "calm, friendly, cheerful face", NO yawn, NO worried look. Never name the feeling as an acting note |
| Everybody the hero talks to should meet his eyes | Put the hero LEFT facing right, the teen RIGHT and adults RIGHT, so every reverse shot looks back at him (EP.11) |
| Clip windows and card times | 0.1 s grid only (3 frames at 30 fps); assert `dur*30` is whole, then check 30/1 and duration = plan on the delivered file (EP.12) |
| A recurring voice sounds different | Measure it: `pitch_check.py` on the new clips and on the earlier episode's; retake with a plain voice description ("light, bright, youthful teenage-boy voice, not deep") |
| Starting a NEW series on the same channel from an owner's character sheet (*Everyday English at Home*, 2026-11-26) | New Meta AI thread; attach the sheet once to draw text-free masters per character (zoom for tiny pseudo-text), write a bible with prompt blocks + a style line taken from the sheet (not the old series' style) + reference pitches; port the previous series' `build.py`/`audio_gen.py` unchanged except cast, places, labels; a new playlist from the upload dialog's "New playlist" (match the old playlist's visibility); **no Reuse details** from the other series (it carries its playlist and tags) — set language and radios by hand |
| A family series: parents and young children (*Everyday English at Home* EP.1) | Kids together in one two-shot (hero LEFT), each parent in an adult-alone reverse shot looking down-left at the children out of the picture: 0 refusals in 23 clips. Third-person -s mistake ("Ivy wake up") was provable: whisper p0.79 vs 0.99, auto captions "wake" ×3 |
| A line passes whisper on its whole window (Everyday English EP.2) | Also whisper two overlapping halves of it: whisper-small hid "have have" that YouTube's captions heard (one re-upload). Prompt "every word exactly ONCE (no repeated words, no stutter)" |
| A prop or garment a character is LOOKING FOR is part of the canon outfit (EP.2: Toby's sneakers) | Keep the bible block word for word and crop every two-shot above the feet (`1024:576:128:0`); show the found object in an empty insert still (`card(still=...)` in `build.py`), zoomed for marks and logos |
| A recurring character's line is asked "ONCE" but comes back twice or with a whispered repeat (Everyday English EP.3: T01, T02, T03) | Cut to the first clean take; run `splitcheck.py` on every window before rendering (EP.3: 35 windows, 0 repeats, auto captions agreed) |
| An adult-alone line of two sentences gets a 1.8-4.2 s silent pause even with "only a short pause" (EP.3 N02, N04, N05, B03) | Two windows, the second cropped closer (768:432 on the face) so the jump reads as a cut |
| "VERY FAST ... in one quick breath" for the FAST/SLOW/NORMAL habit (EP.3 B01b) | Meta stays at ~2.7 words/s; don't retake for speed, the tag is relative to the SLOW clip |
| The delivered file's true peak is above -1 dBTP with the previous episode's chain (EP.3: -0.3 with limiter 0.79) | Measure `ebur128=peak=true` on the delivered file every time; limiter 0.70 gave -14.5 LUFS / -1.9 dBTP; `final_pass.py` redoes only the last pass |
| A host clip comes back with one take or a breathy first take (EP.3 H1, H5) | Queue spare host takes inside the main batch; whisper both takes of every host clip |
| A clip is split into two windows and the clip name has sentence cues (Everyday English EP.4 N03) | Key the cues by `(name, t_in)` in `CUES` (build.py `clip()` takes `CUES.get((name, t_in), CUES.get(name))`); then compare every burned cue string with its window's `sub` before rendering |
| A kids two-shot behind a counter/table "hides the feet" in the master (EP.4) | Meta still reframes wider in the clips (a sneaker at the bottom edge): crop every kids clip head-to-waist (`1024:576:128:0`) |
| A recurring child voice comes back ~3 semitones low (EP.4 Toby 296/308 Hz vs 348-444) | `pitch_check.py` on every clip as it lands; retake with "a lively, clear, LIGHT, HIGH little boy's voice (a young child of about six, not deep, not a teenager)" (381/421 Hz) |
| A clip opens with 1-2.5 s of loud breathing/sighs (EP.4 B03, B05, H6) | Whisper short windows (<=1.5 s) to find the first real word ('[BREATHES HEAVILY]' is not speech) before setting the in point |
| A long "Fill the gap" quiz question (EP.4 Q2) | Put "Fill the gap:" on its own line (`\n`) so the quoted sentence stays on one line |
| A translated title is over 100 characters (EP.4 Vietnamese, 101) | Studio drops it silently (no row): shorten it before fe_10 and read all five rows back after a reload |
| An intentional mistake that sounds like a real word pair ("I can to ride" ≈ "I can't ride", Everyday English EP.5) | Never put a buzz/SFX on the mistake: render 1's hook buzz at 0.5 s made whisper hear "I can't ride!". Cross + buzz just AFTER the line; whisper every copy of the mistake in the delivered file (exact segment starts) before upload; auto captions then heard "I can to ride." ×3 |
| `sync_check.py drift` reports +1.3–1.5 s on a short host take with a pop SFX at 0.1 s (EP.5 H4/H5 take 1, r≈0.9) | False peak: compare 50 ms speech envelopes of the source window and the delivered file; if they line up frame for frame, the offset is 0 |
| Studio edit page says "This video is in a draft state" after the upload dialog's Save (EP.5, after Reuse details) | The visibility radio was unset: "Edit draft" → Visibility step → PRIVATE → Save → reload ("Visibility Private"). Check for 'draft state' right after saving |
| A kids master drawn full body (EP.5 park) | Meta keeps that framing in every clip: crop knees-up (`960:540:160:20`) so shoe marks never show; zoom shoes/bike frames of every generated still (pseudo-emblems) and crop them out |
| Children outdoors (park, EP.5) | Open the place on a no-speech family still, say "their mum and dad stand close by, just outside the picture, watching them" in every kids prompt, children stand beside parked bikes (never ride), an animal = no-people master + a silent clip; 0 refusals in 31 clips |
| meta.ai localStorage near the ~5.2M quota (EP.5: 4.94M) | `lsbackup.py` each superseded key to disk (decode check), then remove it; log the size before/after; never touch another series' keys |
| Screen locked or the meta.ai tab hidden at the start | Do script, prompts, `build.py plan`, metadata and thumbnail words offline; start `tools/wait_visible.sh` + the image queue in the background; ask the owner once to unlock (EP.8) |
| An episode about being ill, in a family series with young children (Everyday English EP.6) | The series plan said "in bed with Mum near", the bible bans in-bed / pyjamas / sad children: take the safer rule. Make an ADULT the unwell one (SAID calmly, in an armchair with a plain blanket, day clothes, prompt "he SAYS it, does not act it; clear normal voice, NO coughing, NO hand on his throat"); the child's illness line is a learner's mistake to a parent's teaching question ("what do you say when your head hurts?"). 0 refusals in 27 clips |
| Illness words in the prompts (EP.6) | Meta still adds sneezes/coughs/sniffs before or after the line (4 of 27 clips): whisper the WHOLE clip incl. the gaps (`tools/asrp.sh` on each burst) and keep windows clear of them |
| A rainy-day scene: a master with a rainy window (Everyday English EP.7) | Meta animates rain streaks INSIDE the room (wall, sofa, a child's hair). Prompt "the rain is shown ONLY as a few small STILL raindrops on the window glass, NO falling rain lines anywhere (not outside, not inside); inside everything is dry"; zoom every rain clip at full size (face strips), crop to the cleanest area |
| A calm "lights go out" cliffhanger with children (EP.7) | Test it first; a no-people clip "the floor lamp's light fades off smoothly over one second" works (one of two takes dissolved the lamp: pick the take where it stays); "dim" stills come out only mildly greyer = calm; only an adult speaks in the dim room; "flashlight", never "torch"; 0 refusals |
| A word with a false start ("deca- deca- decorations", EP.7 I02) | Whisper whole + halves and `splitcheck.py` MISS it (a fragment adds no whole word); the automatic captions caught it after upload (one extra render + upload). Before rendering: `whisper-cli -ml 1` on each window, flag any single word > ~0.9 s, whisper 0.8 s sub-windows across long words; prompt "'decorations' said smoothly in one go (no false start)" |
| A no-speech clip (rain, lamp, empty insert) in the timeline (EP.7) | `clip_gain` levels every window to -18 LUFS, so ambience plays as loud as speech (-13.8 LUFS in the mix): give it a lower target (`QUIET = {"L01b": -27}` in `_seg.py`) -> about -20 LUFS |
| New place masters from the character SHEETS + a place picture (Everyday English EP.8: small kids, watercolour look, parents looking like children; 5 of 8 rejected) | Attach the series' own SHOT of the character alone (or first) and ask to change ONLY the background ("same drawing, size, framing, pose"); compare side by side with the previous master before accepting |
| Seated children behind a table (EP.8 craft table) | Meta turned the table see-through after ~1 s in 3 of 11 clips (legs showed), even with "the table stays": crop every kids window head-to-chest (`960:540:160:0`) and check the sheet's bottom row at 0.5 s vs 1.5 s |
| Settling a "lights out" cliffhanger (EP.8) | Use the previous lamp clip's last dim frame (Meta's own output, unedited) as the start image of a no-people "lamp comes back ON" clip; worked first time, QUIET -27 |
| A politeness mistake with correct words ("Give me the glue.", EP.8) | Prompt "exactly these words, NO 'please', NO 'could', GIVE then ME (not 'gimme')"; proof = the absence of please/could in whisper whole + halves and in the auto captions |
| A prop that shares a name with a canon item (EP.8 "Ivy's ribbon" vs her hair bow) | Make the prop a separate object shown only in no-people inserts (present / gone, the second made from the first); restate the canon item in every prompt and never write "X is gone" in a prompt that shows the character |
| A re-upload of your own episode (EP.7) | Swap the new id into the edit-URL scripts and grep for ZERO occurrences of the old id before saving/scheduling; leave the superseded upload Private and undeleted, report it first in the report (owner deletes); re-run the full Studio pass incl. a fresh word check on the new id |
| A story about a screen (Everyday English EP.9: a video call), with a "no screens" ban | Make the call SOUND-ONLY in the story ("the picture isn't working"); show the device only from BEHIND in a no-people still (plain lid, no logo, no keys); never draw the caller. Never name an out-of-frame object in a clip prompt ("the laptop just below the picture"): Meta pulled the camera back to draw it in 3 of 3 clips |
| An unseen speaker (EP.9 Uncle Max, voice only) | Meta voices him in a no-people clip, but changed the picture (closed the laptop lid) and ignored "deep" (4-5 semitones above the dad). Use the clip's AUDIO over the Meta still: `clip(..., still=png)` / `STILLV` in `Series/family-english/ep09/build/_seg.py` + `_post.py` (cards' slow zoom, burned subtitles). Put ALL his lines in ONE clip (two parts with a pause) = one voice; pitch can't prove two clips share a voice (258 -> 151 Hz inside one clip) |
| Kids master with a big empty desk/table in the lower half (EP.9 study) | 6 of 8 clips: pull-back, desk vanishing at ~1 s, legs, Toby's hair curling. A CLOSE kids master (heads to mid-chest, nothing in front) + "the camera stays EXACTLY ... the same CLOSE view ... no desk, no hands, no legs come into the picture; Toby's hair ... NOT curly" held 3 of 3 |
| A negative list that names an allowed decoration (PARTY_NEG "the only decorations are plain paper chains") | Meta ADDS that decoration to pictures that should have none (laptop insert, the thumbnail's empty text side): say "NO decorations of any kind: NO paper chains, ..." there |
| Studio upload "Creating link..." forever, playlists "No playlists available", subtitle/end-screen editors empty (EP.9) | Search the page for "Daily upload limit reached": 10 uploads in 24 h hit it (EP.1-EP.8 + 2 re-uploads). No video is created (nothing in the Content list); leave via the Content list URL. The one-time verification is the owner's; otherwise retry after the oldest upload of the window is 24 h old. One upload per episode; every re-upload counts |
| A character shot that passes the look check but breaks the REAL gate (EP.10: Toby drawn bigger and higher than his older sister; parents placed right of centre for shot/reverse-shot) | Fix the BASE shot with a correction edit ("Ivy a little TALLER, heads the same size" / "stands in the CENTRE, turned a little toward screen-left"), re-make every variant from it, retake every clip of that master; the eyeline still meets because the adult looks down-left from the centre |
| A clothes / dressing-up lesson with young children (Everyday English EP.10) | Never show changing: the child HOLDS the garment up on a hanger in front of the chest, or is ALREADY WEARING it over the canon outfit; visual descriptions never say "try on / put on / take off / change"; add "Both children stay fully dressed in their usual day clothes". Held props held 6 of 6 clips; a worn-over garment drifts back toward the canon outfit after ~5 s, so end those windows by 5 s |
| Several prop variants of one shot (EP.10 small shirt / big cardigan / cardigan that fits) | Accept one base shot, inject it, then make each variant as a ONE-change edit of it ("Keep EVERYTHING exactly ... ONE change only: ..."); faces, framing and background stay identical across the variants |
| A line about a stain, mark, mess or damage spoken by a visible character (EP.10 "There's a stain on Toby's hoodie!") | Meta paints the stain on the speaker and gives a worried face (2 of 2): play the line as the speaker's voice over the no-people still of the object (`STILLV`, the EP.9 unseen-speaker method) |
| A drawn garment or prop shows a tiny label / tag with pseudo-text | Fix with a one-change Meta edit of the injected image ("NO label and NO tag anywhere"), zoom again; never edit pixels yourself |
| Two sessions share one Chrome window (one waits on Studio, one runs Meta) | `activate_meta.sh` refuses to bring meta.ai to the front while the other session's Studio tab is the active tab (logs to `build/guard.log`); activate meta.ai once by hand at the start |
| Stopping a Meta queue early | Kill the PYTHON `runq.py` (pgrep "Python tools/runq.py"), not its `sh -c` wrapper; append "DONE" to its log only after it is dead (a running runq overwrites appended lines). `make_prompts.py` rewrites every `queue*.json`: copy a running queue aside before re-running it |
| A new place made from the previous episode's character shots by changing only the background (Everyday English EP.11) | The old floor/carpet comes along (EP.10's lilac carpet in a playroom whose master has floorboards): compare floor, wall and light with the place master and fix the base with one correction edit before making prop variants or clips |
| A two-shot line of two sentences where the listener opens her mouth during the second, or whisper halves suggest a repeated word (EP.11 T01 / I02) | Keep the clean first sentence, or run `whisper-cli -ml 1` on the WHOLE window: a half that starts inside a word makes whisper invent the whole word again ("Let's... Let's" was one "Let's") |
| `build.py plan` says "glyph check OK" but a card shows empty boxes (EP.11: "→" in Nunito) | The old check compared glyphs with `getmask("")`, which never matches; compare with `getmask("\U0010FFFD")` (.notdef) and check all burned strings against both fonts (`Series/family-english/ep11/build/_post.py`); look at the whole-video contact sheet before every upload |
| Two sessions share one Chrome window, one in Studio, one in Meta (EP.10/EP.11) | Studio's upload dialog and visibility popup stay hidden in a background tab (document.hidden), and Meta needs its tab in front too: take turns, and message the other session the moment your browser batch ends |
| A background-change of a kids shot (Everyday English EP.12) comes back in another SHAPE (3:2, 1920x1280) with the hero nearer the camera (his head bigger than his older sister's) | Check every master's pixel size AND the heads/feet line before injecting; retake with "exactly the same 16:9 shape as the attached picture; standing on ONE line at EXACTLY the SAME distance; X's head NOT bigger" |
| Outdoor adult-alone clips (EP.12 garden) | Meta pulled every adult clip far back (body small, centre x~690 of 1280): measure a full frame of the first clips per place and set the crop then (1024:576:178:0); the previous place's crop left them off-centre |
| A phone in a no-people still, "face down" (EP.12) | A dark grey slab with a port reads as a screen face up: ask for a PALE case back (pale-pink matte rubber case, no dark glass, no port, no lens pattern) |
| An intentional mistake that drops a contraction ("I going to" vs "I'm going to", EP.12) | whisper-small adds a weak 'm (p~0.2) when the window runs into trailing silence (language prior); pick the take that is 'm-free in most windows AND in wordcheck (-ml 1). A cross + BUZZ right at the line's end masked the final 's' ("lights" -> "light") in the delivered file: put MX_ICON after the last fricative and whisper EVERY copy of the mistake in the delivered file at its exact segment start |
| A recurring "voice only" older character (EP.12 Grandma) | Meta gave the same pitch band as the young mum in 4 of 4 takes even with "elderly, seventy-five, low, husky, slow": log it, pick the lowest run medians, no workaround; all her lines in ONE clip; the auto captions confirm the words |
| Every Meta send fails in ~7 s with "Something went wrong" for clips AND images, in the old thread AND a new chat (Everyday English EP.13, 22:30-00:30) | Not a refusal and not the thread: a plain no-attachment prompt told the reason ("the safety check service is temporarily unavailable"). Stop the queue (kill the Python runq/runimg), probe ONE send per 15 min (`ep13/build/probe.py`), chain the rest of the queue behind the probe; owner rule 2026-11-27: on a service error start a NEW chat (re-attach masters every prompt, one test per ~15 min, log each chat id), never for a refusal; log every probe's MODE line |
| FAST / SLOW / NORMAL from Meta (EP.13) | "three parts with a one-second pause" came back at 2.9 w/s = NORMAL (3.0): measure words/s as each lands; "every single word said separately, a pause after EVERY word, about EIGHT seconds" gave 1.5 w/s. A FAST line can hide a stutter ('the- the big') that whole + halves miss: probe ~1 s windows across every pause |
| A NEW older character's sheet from a parent's sheet "for style only" (Everyday English EP.14 Grandma) | v1 came back chibi-child proportions (head ~1/3 of her height); "the mum's grown-up proportions" fixed the body but turned the full-body faces realistic; "bigger chibi head" undid it. What held: a ONE-change edit of the good-body version that changes ONLY the full-body faces ("heads and bodies unchanged"). Check the height in a no-speech still with the whole family on one line, cropped below the knees |
| "Their mum and dad stand close by, just outside the picture" in a kids two-shot (EP.14 station) | Meta drew the parents as headless partial bodies at both frame edges (1 of 6): say "right behind the camera, NOT in the picture (no grown-up's legs, arms or body at the edges)" and crop the edges (SKC `1088:612:76:0`) |
| An elderly character speaking in person (EP.14 Grandma, `VGRAN` "seventy-five, LOW, a little husky, about two words per second") | In-person takes came out 170-235 Hz vs the mum's 242-348 (EP.12's phone takes sat in her band), but with ~2 s pauses between sentences: cut two windows per clip, the second closer. SLOW with ellipses in the quoted line ("Let... me... help...") dropped/duplicated words twice; spell the words out ("LET, then ME, ... 'you' only ONCE") with no ellipses in the quote |
| Every ADULT clip fails after ~7 s with "Something went wrong" (series thread AND a new chat) while kids/host clips render (Everyday English EP.16) | Not a refusal: Meta (plain no-attachment question) called it a render crash on very long prompts. A minimal prompt on the same master rendered first time; SHORT adult prompts (~1.9k chars: character block, centred/alone/look, exact line + manner + voice, ONCE, END, 'nobody cries', a short REAL clause) rendered 37/37. Ask Meta in plain text before burning retries |
| Studio's video Languages page shows "Oops, something went wrong. Retry" where the video-language rows were (28 Nov 2026) | Studio-side, also on older videos: translations still work through Add language -> the language dialog (`translate_meta2.py`); verify EN/TH published from the owner's watch-page source (`captionTracks` vssId `.en` / `.th`); the automatic-captions download is unavailable then (timedtext 502 for private videos) -> log it as open, rely on the delivered-file whisper, never accept auto captions |
| Editing an EXISTING translation (e.g. the coordinator's "Next episode" link) after Studio's 28 Nov 2026 change: the old `ytgn-metadata-editor` never opens | Click the language row's button -> `ytcp-dialog` named after the language (two contenteditable `#textbox`: title, description; "Update"). In a background tab `execCommand('insertText')` does nothing: set only the OLD text node and dispatch an `input` event, check the title is unchanged and the description is EXACT before Update, then reload and re-read every language. Working tool: `Series/family-english/docs/next-links/run2.py` + `tr2.py` (backup / apply / check). The dialog stays open after Update (harmless) |
| A Meta queue sits for hours in `wait_visible.sh` (EP.16: 4 h) | `activate_meta.sh` refused to front meta.ai because OUR OWN Studio tab was active: guard only the other sessions' tabs; check `build/guard.log` whenever a queue stops logging |
| A `nohup ... &` render dies silently after a few segments (EP.16) | Run long renders as a tracked background job (the tool's run_in_background), never a nohup child of a short shell |
| An intentional mistake that whisper's language prior turns into the correct form ("Thank you for come" -> "coming", EP.16) | Sweep ~12 windows per take (start -0.3..0, end +0.1..+0.4) and count readings; every correct take reads the -ing form at 0.99-1.00, pick the take with the most 'come' readings (8/12) and whisper every copy in the delivered file |

## Common Pitfalls

The ones that cost the most, most expensive first:
1. **Burned-in text that disagrees with the audio.** It caused a re-upload in all three episodes. Spell-check
   `build/burned_text.txt`, get the listen check, and run the word check early.
2. **Audio drifting late** when each segment was encoded to AAC before concat (about 35 ms per segment, over 1 s
   after 2:20 in EP.2). Use PCM segments.
3. **Reading the speech timeline from the wrong row.** Each row is 5.0 s. Two second takes shipped silent in an
   EP.3 render. `sync_check.py windows` now catches it.
4. **A clip starting from the wrong image** in the thread (an older, rejected master). Name the master by its
   distinguishing look.
5. **A plain background in the master.** Each clip then invents a different detailed hall. Make the master
   detailed from the start.
6. **Listener reactions that open the mouth:** "surprised", an open grin, looking at something. Ask for lips
   pressed together and a calm face.
7. **Details that aren't restated drift:** eyelashes, beak colour, a badge appearing on a cap.
8. **A mute or breathy clip passing the loudness timeline.** The voicing line and a person's ears catch it.
9. **A thumbnail that didn't stick** because it was set while the video was still processing, and a readback that
   counted image elements instead of looking at the picture.
10. **One-pass `loudnorm`** missing the target, and `linear=true` leaving peaks at 0 dBTP. Use two passes plus a
    limiter.
11. **A font without the glyph** ("→" in Nunito) drawing empty boxes. `build.py plan` asserts glyph coverage, but only against the font's .notdef (`getmask("\U0010FFFD")`): the older `getmask("")` check passed "→" in Everyday English EP.11 and the contact sheet caught it.
12. **A stale upload dialog** making a video Public.
13. **Changing the look between episodes.** EP.4 v2 used a new card design and new music; the owner rejected it
    ("KEEP CONSISTENT") and it cost a re-render and a re-upload. Port the previous `build.py`.
14. **Non-English text burned in on a global channel.** EP.4 v1 carried Thai under every subtitle → re-render and
    re-upload. Keep other languages in caption tracks.
15. **Losing the Meta AI thread** when the account changes. Save every sheet and master as PNG as soon as it is
    accepted (signed image URLs expire in about 4 days).

## Output Templates

Accepted cut (`edl.tsv`, tab-separated) and log lines (`qc_log.txt`):
```
C02   1.0  5.2  PUDDING  Hello! I'd like to change some money, please.  PASS two-shot; listener beak closed verified 5 fps (1.0-5.0); speech 1.2-2.1 / 2.9-4.9
C10   FAIL off-model: Biscuit drawn with eyelashes through the whole line (zoom 3.4-6.2) - regenerate with "NO eyelashes"
C01   REFUSED by Meta AI ("<line>"): "<Meta's reason>". Not reworded. Accepted Meta's offer: <alternative>
OWNER LISTEN 2026-11-20: C08 says the line once -> ...
FINAL RENDER 4: out/<episode>.mp4 5:07.2, -14.5 LUFS, -1.5 dBTP, A/V 0 ms at every clip
```

Final report to the owner:
```
Video: https://youtu.be/<id> (Private) · out/<episode>.mp4 · 5:07 · −14.5 LUFS / −1.5 dBTP · A/V 0 ms at every clip
Clips: 26 generated, 2 refused (alternatives accepted), 21 accepted cuts
Set: title, description + chapters, 22 tags (458/500), not made for kids, altered content: No, thumbnail,
     EN + TH subtitles, title/description in TH ES PT VI ID, end screen → previous episode + subscribe, playlist
Read back: visibility Private ✓ thumbnail picture ✓ · Word check: every spoken line matches the burned subtitles
Open: <questions for the owner, for example linking this episode from the previous one>
```
