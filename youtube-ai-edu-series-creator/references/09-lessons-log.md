# 09 — Lessons log (EP.1–EP.4) and owner rules

Why each rule in this skill exists. Add a row when a new failure costs time; don't delete old rows.

## 1. Owner rules (standing, in the order they were given)

| # | Rule | Given |
| --- | --- | --- |
| 1 | Work as an expert content creator; keep the concept consistent across the series | EP.1 |
| 2 | Characters are cute and fit the story; the human cast are teens of 15–17 so the series isn't made for kids | EP.1 |
| 3 | No dead air that makes the video boring | EP.1 |
| 4 | No copyright or trademark infringement | EP.1 |
| 5 | Research the AI tool's documentation before building on it | EP.1 |
| 6 | 16:9, horizontal, for YouTube | EP.1 |
| 7 | Watch for lip-sync overlap: two mouths must never move at once. QC properly | EP.1 |
| 8 | Add subtitles | EP.1 |
| 9 | Keep scenes and characters consistent | EP.1, again EP.2 |
| 10 | Write a caption and SEO tags for a worldwide audience | EP.1 |
| 11 | A cute cover, made from Meta AI art; QC the layout; pill text must not overflow | EP.1 |
| 12 | No run-together words in subtitles | EP.1 |
| 13 | No laughing at the end of a scene; cut right after the last word | EP.2 |
| 14 | Subtitles must match the lip movement in time | EP.2 |
| 15 | Read the skills before starting an episode; update them after | EP.3 |
| 16 | Skills are written as `.md` files first, not committed to the shared skills repository | EP.1 |
| 17 | Work files live on E: | standing |
| 18 | Keep a character bible and one `Characters/` folder; every new character gets a sheet before its first clip | EP.4 |
| 19 | Run the episode end to end; don't ask after every step | EP.4 |
| 20 | Global channel: no Thai (non-English) text burned into the video; other languages only as optional tracks | EP.4 |
| 21 | KEEP CONSISTENT: copy the previous episode's `build.py` + `audio_gen.py`; change only the timeline, never the design, music or labels | EP.4 |
| 22 | Read and update skills **only** in the `digital-creator-skills` repository | EP.4 |
| — | Rule 17 now reads: Windows work on E:; Mac work in `~/Documents/Kritchawat-Projects/Series/` | EP.4 |

Decisions the owner made once for the series: "No, it's not made for kids"; altered content "No" with an
AI-note line in the description; upload Private and decide Public per video.

## 2. Incident log

Cost: **R** = a clip regenerated, **RR** = re-render, **UP** = re-upload (the owner drags again and all Studio
steps repeat).

| EP | What happened | Found by | Cost | Rule it produced |
| --- | --- | --- | --- | --- |
| 1 | Two speakers in one clip: the wrong character's mouth moved | zoom strip | R | One speaker per clip |
| 1 | Hero drawn with eyelashes; a 2.6 s silent gap mid-line | contact sheet | R | Restate fixed details; trim or regenerate gaps |
| 1 | "UK BORDER FORCE", a real airport sign and a cap badge appeared | contact sheet | R | Word-level negatives; blank screens |
| 1 | Desk, seats and hall differed from clip to clip | owner | 8 clips | One scene master per location; fixed left/right |
| 1 | A prompt label in quotes became a sign in the scene | contact sheet | R | Describe the master; never name it in quotes |
| 1 | Meta refused a 16-year-old addressing the camera as teacher | refusal | host changed | Adult or animal host; never work around a refusal |
| 1 | Listener's open-mouth smile during the other's line | zoom strip | R | "closed-mouth smile" for listeners |
| 1 | `silencedetect` found nothing (ambience) | — | time | Speech-band RMS timeline |
| 1 | Loudness −20 LUFS, then −15.7 after one-pass `loudnorm` | measurement | RR | Later: two-pass + limiter |
| 1 | Tags over the limit; a chapter at 00:04 | Studio | edits | Count in Studio; first chapter 00:00 |
| 1 | Thumbnail from a video frame: cut sign, cut ear | owner QC | rework | Dedicated art with empty space for text |
| 1 | Pill text overflowed its background | owner | redo | Size the pill from the ink box; assert |
| 1 | Custom thumbnail blocked | Studio | wait | Channel must be phone-verified |
| 1 | Run-together words in a burned subtitle to show fast speech | owner | RR + UP | Correct spelling + FAST / SLOW tag |
| 1 | End screen needed a video or playlist | Studio | deferred | Add from the second episode on |
| 2 | Master with grey beak, small eyes, wrong cap (two candidates) | review | 2 images | Full design in the master prompt |
| 2 | "VERY FAST in one breath", "Please wait here", "sad and droopy", silent coaching: refused | refusal | script changes | Accept Meta's alternative; design scenes around it |
| 2 | A teen's lines were only breath (3 clips) | owner + voicing | R ×3 | Voicing check; "clear, full, normal-volume voice" |
| 2 | Plain belt master → 6 different halls | montage | all belt clips | Detailed master from the start |
| 2 | Listener asked to look "surprised" held an open mouth; open grins | zoom strip | R ×3 | Lips pressed together; no surprised listener |
| 2 | Beak grey again when the prompt didn't restate it (3 clips) | montage | R ×3 | Restate details in every prompt |
| 2 | Clip started from an older rejected master | zoom strip | R ×2 | Name the master by its look |
| 2 | Character morphed mid-clip and gained a crown badge | zoom strip | R | Any emblem = fail |
| 2 | Laughs at the end of scenes | owner | trims | Rule 13 |
| 2 | Two burned subtitles didn't match the audio | automatic captions | RR + UP | Word check before the Studio work; listen check |
| 2 | Subtitles "didn't match lip sync": whole-line subtitles before the words | owner | RR | Sentence cues |
| 2 | Audio drifted late, about 35 ms per segment (AAC per segment) | owner, then `sync_check` | RR + UP | PCM segments; one AAC encode; measure the delivered file |
| 2 | "No drift" was declared from `body.mp4` | — | the UP above | Never measure an intermediate file |
| 2 | A stale upload dialog in another tab made the video Public | readback | owner kept it | Work in the drop tab; close stale dialogs |
| 3 | Adult speaking to the hero in the two-shot refused; goodbye wave refused | refusal | scene rebuilt | Shot / reverse shot from a solo master |
| 3 | "Another solo version" kept the second character in frame | contact sheet | R ×2 | A still solo master, animated by name |
| 3 | Eyelashes on two characters; a teen's small "o" mouth in profile | tight zoom | R ×3 | Tight crop on profile faces |
| 3 | Background swapped mid-clip on a reused master | contact sheet | R | "background stays EXACTLY the same" |
| 3 | Two second takes cut from the wrong timeline row (silent) | drift row `r=0.38` | RR | Rows are 5 s; `sync_check.py windows` |
| 3 | "→" drawn as empty boxes (Nunito has no glyph) | contact sheet | RR | Glyph check in `plan` |
| 3 | A line spoken twice under a once-only subtitle; the owner had heard it once | automatic captions | RR + UP | Two bursts = said twice; word check right after Save |
| 3 | Custom thumbnail didn't stick (set during processing); readback counted `img` elements | owner | redo | Set on the edit page; read back the picture |
| 4 | Meta AI account changed mid-episode; project thread gone | owner | thread rebuilt | Re-upload sheets + masters by fetch/DataTransfer (`10`) |
| 4 | Meta lost access to uploaded masters after a few turns | refusal text | 1 turn each | Attach the master with every clip prompt |
| 4 | "Taxi Rank" wayfinding sign appeared on the canopy; meter showed "0:10" | background check, contact sheet | R ×3 | Location crops (`RANK`, `WHEEL`) on every clip of that place |
| 4 | Window views turned photo-real ("street slides by") | contact sheet | R | "view outside stays exactly as drawn, flat cartoon" |
| 4 | A teen's jeans turned blue; headphones moved onto his ears | contact sheet | R ×2 | Restate off-master clothing colours and accessory placement |
| 4 | Driver looked down/right instead of at the hero | contact sheet | R | "keeps looking LEFT the whole video" |
| 4 | Both mouths moved during part of a two-shot line | 5 fps zoom | line shortened | Keep the clean part; shorten the line |
| 4 | A made-up hotel name was a real Camden business | web search | rename | Search every invented business name |
| 4 | Thai burned under every subtitle and on cards; the channel is global | owner after upload | RR + UP | Rule 20 |
| 4 | v2 re-render used a new card design and new music instead of EP.3's | owner ("KEEP CONSISTENT") | RR + UP | Rule 21: port the previous `build.py` |
| 4 | Studio pencil on automatic captions = "Overwrite track" | dialog | none (cancelled) | Never edit the automatic track |
| 4 | First thumbnail injection after the upload didn't stick | readback after reload | 1 retry | Inject on a freshly loaded edit page; reload and look |
| 4 | End-screen start time didn't apply until the field lost focus | screenshot | none | Enter, then Tab; check both bars |

## 3. What the numbers say

| | EP.1 | EP.2 | EP.3 | EP.4 |
| --- | --- | --- | --- | --- |
| Clips per accepted cut | 1.7 | 2.0 | 1.2 | 1.1 |
| Refusals | 1 | 4 | 2 | 0 |
| Renders | not logged | 3 | 4 | 3 |
| Uploads | 2 | 3 | 2 | 2 |

- Yield improved once clips had a single character on screen and masters were detailed.
- **No episode has shipped on the first upload.** Each re-upload came from burned-in text or sync, never from
  the picture. The cheapest protection is in this order: spell-check `burned_text.txt`, `windows`, the owner
  listen check, `drift` on the delivered file, and the word check immediately after the first Save.
- EP.4 had no sync or wording re-upload; both of its extra renders came from **format** (Thai on screen, a new
  design). Porting the previous `build.py` and the English-only assert remove both causes.
- A goal for the next episode: one upload.

## 4. Corrections to earlier notes

- The earlier assembly notes gave EP.3 as −14.6 LUFS / −1.2 dBTP. Those were EP.2's numbers. The delivered EP.3
  file measures **−14.5 LUFS / −1.5 dBTP** (re-measured 2026-11-21).
- An EP.2 log line said "no A/V drift (constant +50 ms)". It was measured on an intermediate file and was wrong;
  the uploads drifted. The log carries a CORRECTION line.

## 5. Not built or not measured yet

- Shorts (story Short and spin-offs) and their related-video links.
- Pinned comments, community polls, the season practice marathon.
- Any analytics: titles, tags and thumbnails are untested against real impressions and click-through.
- Lip sync → Text as a fallback voice route: documented by Meta, not used.
- A local speech-recognition check before upload (the word check currently needs a Private upload).
