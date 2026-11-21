---
name: youtube-ai-edu-series-creator
description: End-to-end playbook for producing and publishing one episode of an AI-animated educational story series on YouTube (16:9, about 5 minutes) - episode design from a series plan, consistent characters and scene masters in Meta AI, single-speaker talking clips, lip-sync / voice / consistency QC, timeline-as-code assembly with Python and ffmpeg (lesson cards, sentence-timed burned-in subtitles, original music, loudness, drift-free audio), thumbnail, SEO title, description, tags and translations, copyright / trademark / policy checks, and a YouTube Studio upload with readback and an automatic-captions word check. Use when asked to make the next episode, create a YouTube lesson video with AI, QC lip sync, remove dead air, add subtitles, make a cover, write caption and tags, or upload to YouTube Studio. Triggers: YouTube creator, new episode, EP, Meta AI video, lip sync, dead air, subtitles, srt, thumbnail, cover, SEO tags, YouTube Studio, end screen, playlist, made for kids, copyright, trademark, re-upload.
---

# YouTube AI Educational Series Creator

One skill for the whole job: from the series plan to a Private YouTube upload that has been checked.
It was built from three delivered episodes (*Pudding Goes to London* EP.1–EP.3, November 2026) and replaces five
earlier drafts (`meta-ai-video-production`, `ai-video-lipsync-qc`, `edu-video-assembly-ffmpeg`,
`youtube-ip-safe-ai-content`, `youtube-studio-upload`). Every rule below came from a measured failure or an owner
decision in those episodes; the history is in `references/09-lessons-log.md`.

## When to Use
- Making the next episode of an AI-animated lesson or story series for YouTube (16:9, about 5 minutes).
- Doing one stage of it: script, Meta AI masters and clips, clip QC, assembly, subtitles, thumbnail, SEO metadata,
  Studio upload, or replacing a bad upload.
- Starting a new series with the same method (new cast, new teaching language, new topic).

## When NOT to Use
- Realistic people, real public figures, or licensed songs. That needs consent and licensing work this skill
  doesn't cover.
- Live-action editing or heavy motion graphics. Use a real editor.
- Legal disputes or takedowns. Escalate to the owner and a lawyer.
- Deciding the audience setting (made for kids), AI disclosure or Public visibility. The owner decides; this skill
  only prepares and applies their decision.
- Shorts. The channel plan has Short templates, but no Short has been built, so there are no measured lessons yet.

## Core Workflow

Work through the phases in order. Don't start a phase until the previous gate is met.

| # | Phase | What to do | Gate before moving on | Details |
| --- | --- | --- | --- | --- |
| 0 | Orient | Read the series plan, the cast bible, the previous episode's script (its "As-built" section), `qc_log.txt` and upload metadata. Create the episode folder; reuse the venv, fonts and scene masters. | You can state the episode's situation, key phrases, grammar point, mistake and cliffhanger, and which masters can be reused. | `01` |
| 1 | Episode design | Write `docs/<series>-epN-script.md`: structure with target times, one-speaker clip table with exact lines, host clips, cards, quiz, continuity and IP table, prompts. | Every spoken line is assigned to exactly one clip and one speaker; every on-screen word is listed. | `01` |
| 2 | IP and policy pre-check | List the banned items for this episode (real names, logos, money, flags…) and put them into every prompt. | The continuity and IP table names specific words and objects, not just "no logos". | `08` |
| 3 | Scene masters | One still image per location in the project's single Meta AI thread: 16:9, detailed background, fixed left/right positions, no text. Make a solo master for any character who speaks to the hero or hosts the lesson. | Each master is on-model, has no text or emblem, and is saved to `masters/`. | `02` |
| 4 | Clips | One 10-second clip per line, animated from the master, one speaker per clip. Download each clip as it finishes. | Every scripted line has at least one candidate clip. Refusals are logged with the alternative Meta offered. | `02` |
| 5 | Clip QC | For every clip: speech timeline, voicing line, contact sheet, face zoom on the listener, in/out points. Per location: a cross-clip montage. | `edl.tsv` holds one accepted cut per line; `qc_log.txt` holds every failure, refusal and decision. | `03` |
| 6 | Owner listen check | Build one labelled MP4 of the clips a person must hear: new voices, intentional mistakes, weak voicing, lines with two speech bursts. | The owner has answered. Tools can't hear words. | `03` |
| 7 | Assembly | Timeline as code (`build.py`). Run `plan` (chapters, burned-text list, glyph check) and `sync_check.py windows`, then render, then check the delivered file: sync, loudness, whole-video contact sheet. | A/V offset 0 ms (±10) at every clip to the end, about −14 LUFS and at most −1 dBTP, no silent cards, burned text spell-checked. | `04` |
| 8 | Thumbnail | Dedicated Meta AI art without text, then local text with asserts. Check it at 1280, 320 and 168 px wide. | No text touches a character or leaves its pill; nothing sits in the bottom-right timestamp area. | `05` |
| 9 | Metadata | Write `docs/<series>-epN-upload-metadata.md`: title, description with chapters and links, tags, settings, translations, thumbnail brief. | Chapters come from `build.py plan`; tags are under 500 characters by Studio's counter. | `06` |
| 10 | Upload | The owner drags the file into Studio. Fill details, thumbnail, audience, English subtitles, end screen, Private. Run the automatic-captions word check right after saving, before the slow steps. Then other subtitles, translations, playlist. | Every setting is read back on the edit page, including visibility and the thumbnail picture. The word check matches the burned subtitles. | `07` |
| 11 | Close out | Append "As-built" notes to the script, record the upload in the metadata doc, add new lessons to this skill. | Report sent with URL, duration, loudness, sync and open items. | `09` |

The owner is asked at fixed points: installs and downloads, the first clip of each new voice, the listen check,
audience and AI disclosure, anything Public, deleting an upload, and changes to an older episode.

## Project Context (Pudding Speaks English — project-specific values)

| Item | Value |
| --- | --- |
| Series | *Pudding Goes to London*, 12 episodes planned; beginner English (CEFR A1–A2) for teens and adults worldwide; not made for kids |
| Cast | Pudding (baby elephant, yellow backpack, no eyelashes), Ploy (Thai teen, mint hoodie), Ollie (British teen, striped scarf), Biscuit (pigeon officer, orange beak, plain navy cap; lesson host), Lily (cat) |
| Format | 1920×1080, 30 fps, about 5 min; clips from Meta AI web (10 s, 1280×720, 24 fps, native speech) |
| Folders | `E:\claude-work\pudding-ep1\` (venv, fonts, `docs\channel-plan.md`, cast bible, these skills), `E:\claude-work\pudding-ep2\`, `E:\claude-work\pudding-ep3\` |
| Per-episode record | `docs\pudding-epN-script.md` and `docs\pudding-epN-upload-metadata.md` hold the video URL, playlist and settings. Read them for IDs; they are not repeated here. |
| Tools | Python venv with `imageio-ffmpeg` and `pillow`; fonts Nunito and Baloo 2 (OFL); Meta AI and YouTube Studio signed in, in the desktop app's browser pane |

Measured results (delivered files re-measured 2026-11-21):

| | EP.1 Airport | EP.2 Lost Bag | EP.3 Changing Money |
| --- | --- | --- | --- |
| Clips downloaded → accepted cuts | 34 → 20 | 43 → 22 | 26 → 21 (2 more refused) |
| Duration | 5:05.2 | 5:05.0 | 5:07.2 |
| Loudness / true peak | −15.7 LUFS / −1.3 dBTP (one-pass) | −14.6 / −1.2 | −14.5 / −1.5 |
| Renders → uploads | not logged → 2 | 3 → 3 | 4 → 2 |
| Why it was re-uploaded | run-together words in a burned subtitle | subtitle text didn't match the audio; then audio drift | a line spoken twice under a once-only subtitle |

Every re-upload came from burned-in text or sync, which YouTube can't replace in place. Phases 6, 7 and the early
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
- Put work files on E: (owner rule): `E:\claude-work\<series>-epN\`.

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
11. **A font without the glyph** ("→" in Nunito) drawing empty boxes. `build.py plan` asserts glyph coverage.
12. **A stale upload dialog** making a video Public.

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
Set: title, description + chapters, 21 tags (415/500), not made for kids, altered content: No, thumbnail,
     EN + TH subtitles, title/description in TH ES PT VI ID, end screen → previous episode + subscribe, playlist
Read back: visibility Private ✓ thumbnail picture ✓ · Word check: every spoken line matches the burned subtitles
Open: <questions for the owner, for example linking this episode from the previous one>
```
