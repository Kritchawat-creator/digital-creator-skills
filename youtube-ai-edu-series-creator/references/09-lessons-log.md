# 09 — Lessons log (EP.1–EP.5) and owner rules

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
| 23 | Claude uploads the video file to Studio itself through Chrome (`studio_upload_video.py`); never ask the owner to drag ("อัพโหลดไฟล์ได้แล้ว update skill upload ทันที", 2026-11-24; again: "สามารถอัพโหลด คลิปลง youtube เองได้เลย ไม่ต้องรอฉัน") — upload as soon as QC passes, never wait for the owner | EP.7 |

Decisions the owner made once for the series: "No, it's not made for kids"; altered content "No" with an
AI-note line in the description; upload Private and decide Public per video.

## 2. Incident log

Cost: **R** = a clip regenerated, **RR** = re-render, **UP** = re-upload (the file is uploaded again and all Studio
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
| 5 | The thread's uploaded masters (cdn.fbsbx.com) can't be fetched by the meta.ai page (no CORS); localhost is blocked by its CSP; the pane's "+" opens an OS picker; Chrome extension disconnected | fetch errors | ~1 h of workarounds | Generate new masters **in** the thread (t39 URLs are CORS-readable); for an uploaded-only master send its bytes once as base64 chunks with a SHA-256 check and keep them in the page's localStorage (`10` §6) |
| 5 | `execCommand('insertText')` didn't reach Meta AI's prompt box | readback | none | Dispatch a `paste` ClipboardEvent; clear the box with cmd+a / Delete first (`10` §6) |
| 5 | Wet umbrella → Meta drew rain drips running down the teen's face (looks like tears) in 2 desk clips | 5 fps zoom | R ×2 | "his hair and face are DRY, only the umbrella is wet" |
| 5 | Listener's mouth opened during the speaker's short line (D03 end, D07 whole line) | 5 fps zoom | R ×2 | "<Listener>'s mouth stays shut the whole time; he only listens" fixed it |
| 5 | Listener's mouth moved during "Oh no!" in **both** takes (Meta gives exclamations to both characters) | 5 fps zoom | line shortened | Keep the clean sentence; don't write a two-shot line that starts with an exclamation |
| 5 | Plan with measured windows ran 5:29 (three-clip recap) | `build.py plan` | none | Watch Again 7 → 4 clips, 4th grammar card dropped; run `plan` with estimates right after writing the timeline |
| 5 | A desk master came back with Pudding plain grey | master review | 1 edit | Ask Meta to edit only the skin colour of the image it just made ("change ONLY …, keep everything else") |
| 5 | The owner asked to schedule instead of Private ("Schedule เสาร์หน้า 08:00") | owner | none | Schedule panel in the upload dialog: date, time list item, time zone GMT+7; read back "Video scheduled … at 8:00 AM" and the content list |
| 6 | Chrome extension and the Control Chrome MCP's JS call both failed; only `osascript … execute … javascript` worked, and only in the Chrome profile where View > Developer > Allow JavaScript from Apple Events is ticked (the setting is per profile; the season-plan Drive folder lived in another profile) | osascript error text | ~1 h blocked | Drive the owner's Chrome with `tools/cjs.py` (osascript by window id + tab id); tick the setting in the profile that holds meta.ai/Studio (`10` §7) |
| 6 | "New video" detection by "src not seen before" picked up an old lazy-loaded EP.5 clip | contact sheet (wrong scene) | none | New clip = the LAST `video` in DOM order after scrolling to the bottom, compared with the last one before Send |
| 6 | Screen locked → tab hidden → Meta AI replies stopped rendering; a reload never hydrated until unlock | `document.visibilityState`, `IOConsoleLocked` | ~25 min | Keep the screen unlocked while generating (`caffeinate -d` keeps it awake); ask the owner to unlock |
| 6 | Pudding's lines in the hotel-room two-shots moved **Ollie's** mouth (R01 ×2, P02), even with every closed-lips clause; desk two-shots were fine | 5 fps zoom | R ×3 | For the hero's lines in a two-shot that keeps failing, make a hero-ONLY closer shot of the same room and animate from it (passed first try ×2) |
| 6 | Mabel held the key in an orange human hand | contact sheet vs EP.5 | R | "in the grey feathered tip of her wing (a goose wing, NOT a hand)" |
| 6 | End-screen start set with the input value setter showed 4:46:09 but saved the template's 4:42:09 | edit-page readback after reload | none | Type with `execCommand('insertText')` + Enter, one element at a time, then reload and read both elements |
| 6 | Translation editor header check failed for Portuguese/Vietnamese/Indonesian (header text cut at 60 chars) | script log | retry | Check the header with ≥140 chars |
| 6 | Owner: "select file ได้เลย" instead of dragging | owner | none | The 70 MB mp4 can be sent into Studio's `input[type=file]` from page JS: 47 × 1.5 MB base64 chunks over AppleScript (57 s) + SHA-256 check in the page (`tools/push_file.py`) |
| 7 | The season plan on Drive (another Google account) couldn't be opened from Chrome in EP.6 | — | guesswork | The **Google Drive connector** reads `channel-plan.md` directly (search `title contains 'channel-plan'`); read §5 before writing the episode |
| 7 | meta.ai tab hidden (Chrome window behind the Claude app, then the screen locked): the clip finished but `video.currentSrc` never appeared, and after a reload the page never re-hydrated (no `contenteditable`) | `document.hidden`, `screencapture` fails | ~20 min + owner | Keep the meta.ai window **visible on screen**, not only unlocked; the finished clip's URL can be recovered from `document.documentElement.innerHTML` (`…n.mp4` + `\u0026`); `tools/resume.sh` waits for a visible, hydrated tab and restarts the queue |
| 7 | AppleScript `set active tab index` / `set index of window` / `activate` were ignored while the owner's session was idle-locked | readback | none | Ask the owner to click the tab and keep the window on screen |
| 7 | The hidden-tab fallback (newest mp4 in the HTML) was tried before the live `video` src and kept returning the previous clip → 5-min timeouts | runq log | 1 timeout | Order: live `video.currentSrc` first, HTML mp4 second |
| 7 | New adult character's clip drew eyelash flicks + eyebrows not on her sheet (Lily L04) | 5 fps zoom on the eyes | R | "NO eyelashes and NO eyebrows (simple round black dot eyes exactly like the <name> sheet)" |
| 7 | A one-line answer ("For here, please.") started at 0.0 s, first word at risk | speech timeline | R | "waits one second with his mouth closed, then says …" for very short lines |
| 7 | Pudding-only close master for the hero's lines in a public place (café counter) | — | 0 fails | Two-shot only for the teen's lines; hero = close solo master; adult = adult-alone master (3 masters per location) |
| 7 | Owner: "ลากเอง สิ ผ่าน google chrome … มันมีปุ่ม upload" | owner | none | Upload by page JS again (`push_file.py`, 76 MB in 62 s); the owner then made it a standing rule (owner rule 23) |
| 7 | Escape inside the edit-page date picker closed the whole visibility dialog and reset date/time | readback | 1 retry | Close the calendar by clicking elsewhere; choose the time from the `ytcp-time-of-day-picker` list item; read back after reload |
| 8 | Screen locked at the start (IOConsoleLocked=true) and the meta.ai tab was not the active tab; after the owner unlocked, AppleScript `set active tab index of window id W to N` (by index, not by a tab-id loop) brought it to the front | `document.hidden` | ~35 min waiting | Prepare everything offline while locked; start `tools/wait_visible.sh` + the image queue in the background so generation starts the moment the tab is visible; select the tab by index |
| 8 | Adult-alone master in an existing place: with only the place attached the design drifted (Walter on the LEFT, no trousers, pom-pom); with only the sheet attached the place drifted (flat daytime canal) | master review | 2 images | Attach BOTH the place master and the character sheet in one prompt (`meta.py key1+key2`); first try after that |
| 8 | The adult stood small in the wide place master | contact sheet | none | Medium crop on every clip of that character (`768:432:300:280` of 1280×720) instead of regenerating |
| 8 | Lily drew eyebrows again in a new place (park gates), even though her master had none | 5 fps eye crop | R | Keep "NO eyelashes and NO eyebrows … nothing drawn above her eyes" in EVERY Lily prompt, not only after a failure |
| 8 | Owner said no check-ins, so no listen check | — | none | Local word check with `whisper-cli` + `~/.cache/whisper/ggml-small.bin` (already on the Mac) on every accepted window; the automatic-captions check after upload still decides |
| 8 | Studio's time list writes "8:00 AM" with a narrow no-break space; `textContent.trim()==='8:00 AM'` found nothing | JS error | 2 tries | Normalise whitespace (`replace(/[\s\u202f\u00a0]+/g,' ')`) before matching time items |
| 8 | End-screen template card ignored `.click()`; it needed pointer events with coordinates on `.card` | readback (0 items) | 2 tries | Dispatch pointerdown/mousedown/pointerup/mouseup/click with clientX/Y on the template `.card` |
| 8 | Measured plan ran 5:23.9 | `build.py plan` | none | Dropped one overlapping grammar card + one Watch Again clip → 5:16.1 |
| 9 | A mistake line with a missing unstressed word ("Where you from?") couldn't be proven: whisper printed "Where **are** you from?" (p 0.60 for "are"; with a prompt hint "Where you from?") | token probabilities, envelope | script change | Choose intentional mistakes that **add or change a content word** ("Where are you come from?"); ASR and automatic captions can then prove them |
| 9 | Meta drew a brow + whiskers + lash flick on the new character (Rosa) in 4/4 speaking clips although sheet, master and prompt had none; "NO eyebrows" wording made it worse | eye crops | 4 R | For a new character, accept the small detail Meta keeps adding, edit it **into the masters** (one edit prompt each) and write it into the bible; keep the owner rules for old characters |
| 9 | Human-style eyes (white eyeball, lash line) when the adult nods or "tilts her head" | eye crops | R ×3 | "eyes are SOLID BLACK round dots … NO white eyeball, NO iris"; no nod/tilt, head still; waist-up master, not a wide one (a small face gets redrawn) |
| 9 | The word "eyebrow" in the listener's block leaked to the speaker (Lily grew brows) | eye crops | R ×3 | In a two-adult shot describe the other adult only as "exactly as in the attached image"; never name a facial feature that only one of them has |
| 9 | Two-adult clip with one good and one off-model adult | crop test | none | Crop to the good one (`704:396:36:90`) instead of another retake |
| 9 | Meta "media service is overloaded" / "returning no video" / 10-min generations | reply text | ~2 h | Service errors aren't refusals: resend after 75 s; never send while the **Stop** button shows (the prompt stays in the composer and the next one gets NOTEMPTY); reload every 4 min while waiting (`meta.py` rewritten, `RESUME=1`) |
| 9 | Mac lid closed and locked 11:21–18:53 on battery: AppleScript to Chrome hung for minutes, "caffeinate -d" didn't help | `CGSSessionScreenIsLocked`, `AppleClamshellState` | 7.5 h | `wait_visible.sh` checks IOConsoleLocked **before** touching Chrome; `cjs.py` has a 45 s timeout; `caffeinate -dis`; ask the owner for lid open + charger + unlocked in one message. The queue resumed by itself at unlock |
| 9 | EP.8 had been replaced by another session (new id) while EP.9 was being made; the brief still had the old id | two EP.8 cards in the Studio picker → Content list + EP.8 log | none | Before linking or choosing the previous episode, read its `NEXT.txt` / `qc_log.txt` again and check ids in the card HTML (`vi/<id>/`) |
| 9 | Which of two same-titled videos did the end screen save? | Save button | none | Reopen the end screen, re-pick each id: the saved one keeps Save disabled, the other enables it; leave without saving |
| 10 | New character Ned: Meta drew a brow line on the sheet although the prompt said none | sheet review | none | Make that detail canon **at once** (prompt block + bible) and check the first speaking clip alone before queueing the rest: 7 lines, 7 clips, 0 retakes (EP.9 without this: 4 retakes) |
| 10 | Pudding's eyes drew outlined white eyeballs and his skin turned pink during a line | eye crops at 2 times | R | Clause that fixed it: "eyes are SOLID BLACK round dots … NO white eyeball, NO outline around the eye. His skin stays the same soft light GREY as in the attached image for the whole video: not pink, not lavender" |
| 10 | "calm, slightly puzzled face" on "I'm boring" → sad, droopy Pudding (never allowed) | contact sheet | R | Any bored/tired line: "calm, friendly, curious face, eyes wide open, head level, small closed-lip smile before and after (he is cheerful and relaxed)"; never "puzzled", "tired", "bored" as an acting note |
| 10 | Prop edits: "add a BIG bow tie" gave a ribbon bow, then a tie half his height in the wide shot | master review | 2 images | Edit the previous image: "change ONLY the size … the SAME bow tie, three times as wide, NO ribbon ends"; for the second place attach the first edited image too |
| 10 | Host said the line once; host window grew blinds and the clock grew marks mid-clip | speech timeline, 1 fps sheet | R ×2 | "The line is heard TWO times in the video … the window has NO blinds and the round clock face stays plain" |
| 10 | Wings: "bigger/smaller" invite size gestures | — | 0 fails | "keeps both wings still at his sides and does not point or gesture; his feet stay hidden behind the desk" in every host prompt |
| 10 | People walked past outside a shop window in a clip | 2 full frames | none | Crop the window out of every clip of that shot (`960:540:20:150`) |
| 10 | Finished clips only appeared after a page reload; some replies hung 15–20 min | runq log | ~1 h | `meta.py`: reload every 90 s while waiting, give up and resend after 660 s |
| 10 | Two sentence cues were drawn together for one frame when a cue switch fell on a frame boundary (`between()` is inclusive at both ends; same code since EP.3) | 1.5 fps look at the delivered file | RR (before upload) | `enable='gte(t,a)*lt(t,b)'` in the cue overlay |
| 10 | Two halves of a line with a 2–4 s hole | speech timeline | none | Two segments, the second one with a tighter crop (3 times in EP.10) |
| 11 | Host acted the feeling on "I'm bored." / "I'm a bit tired." (half-closed eyes, worried brows, head tilt) | contact sheet | R ×2 | "only TEACHES these words: he does not act the feeling …"; bonus: no brow marks on Biscuit any more |
| 11 | Image replies "I couldn't attach the image. Want me to make it again?" 7 times | reply text, no image in the DOM | 20 min | Accept Meta's own offer in one short message (02 §3) |
| 11 | After a reload the previous clip came back under another URL path (t39 → t58) and was saved as the new one | ASR of the "new" clip | 1 wrong file | `meta.py` compares md5 with every clip on disk |
| 11 | Reply never started (no Stop button, nothing after the prompt) | reload log "false" twice | 10 min | `meta.py` returns OVER after two dead reload checks; queue order is the file's order, not the argument order |
| 11 | Lilac planet grew a ring, colours got stronger | contact sheet | R ×3 | Name the one object that has the detail and forbid it for the others; colour clause |
| 11 | White crescent beside Pudding's eye in the two-shot (3 takes), not in two other lines with the same prompt | eye crops | R ×3 | Acting "leans down a little toward Pudding" + "the grey skin touches the black ball directly all around"; otherwise crop to the speaker |
| 11 | Ollie's voice 150–190 Hz instead of 216–380 | pitch comparison with EP.8–EP.10 | R ×3 | Add the voice description to every Ollie prompt; measure before rendering |
| 11 | Rosa's brow frowned on "I'm a bit tired" | eye crops | R ×2 | "is in a good mood … does not look tired or worried"; "the brow line never moves" |
| 11 | Card text left one word alone on the second line | look at the delivered file | RR (before upload) | Shorten the text; check the wrap of every card in the plan frames |
| 12 | Windows measured in 0.05 s steps (half frames at 30 fps): the concat came out as a 60 fps stream, 0.5 s longer than the sound; `sync_check drift` still said 0 ms because it compares the audio with the plan | `ffprobe` r_frame_rate 60/1 and duration ≠ plan | RR (before upload) | All windows and card times on a 0.1 s grid (in = floor, out = ceil); assert `dur*30` is whole before rendering; check `r_frame_rate` 30/1 and duration = plan on the delivered file |
| 12 | 1.43× close crops hid mouths and the bow tie behind the subtitle bar | look at the delivered file | RR (before upload) | Second-part crop 1024:576 (1.25×), placed so mouth and prop stay above y = 0.8 |
| 12 | Eyes brown instead of black, apples green → red, ear insides pink → peach in warm evening light | eye strip, contact sheet | R ×6 | One clause per drifting object ("PURE BLACK, NOT brown", "the apples stay GREEN", "the insides of his ears stay the same pale PINK") |
| 12 | Returning adults (Frank, Walter, Lily) spoke 40–80 Hz deeper than in their own episode; the host too on one line | pitch check | R ×7 | Never write "deep" or only "warm" for an adult voice: "bright, friendly, lively, not deep"; measure each returning adult against its **own** earlier episode with `pitch_check.py` before queueing the rest |
| 12 | Rosa's eye pointed in 3 of 3 clips from a new master with a bigger, more textured head | eye strip | R ×3 | If two takes fail on the same master, change the master or the speaker, not the wording (the line went to another adult, who was the better partner anyway) |
| 12 | Group shot for the closing line: hero speaking, three silent friends | 5 fps zoom | 0 fails | Master with all mouths closed + "The three friends … are drawn exactly as in the attached image. They do NOT speak …"; passed first try and keeps the hero among friends |
| 12 | A far eye touching the face outline grows a lash flick, and an edit prompt didn't remove it | master review | 2 images | Re-make the master in three-quarter view with "BOTH eyes fully inside the face" from an older good master |
| 12 | `inject.py` SHA MISMATCH "missing value": meta.ai localStorage quota (5.24 MB) full | `QuotaExceededError` | 5 min | Remove old keys whose PNG is on disk, inject again, read the key's length back |
| 12 | "Something went wrong. Please try again." in 7 s on an image with two attachments, and an OLD image taken as the new one | reply text, picture review | 10 min | Service fault: resend later / with one attachment; `meta.py` md5-checks images as well as clips |
| 13 | Master made with the old episode's picture + the newest character picture keeps the OLD drawing style (lavender skin, two brows) | master review | 2 images | One attachment (newest characters), the old place in words |
| 13 | Over-the-shoulder view of an animal friend: realistic pigeon back / missing blouse / looks away from the hero | master review | 4 images | Friend in side view listening, or the friends frame; only the hero speaks |
| 13 | Objects named in the prompt but not in the master grow into the picture (trolleys), travellers and buildings appear behind the windows | 9-frame zoom | 4 clips | Scene text = what is in the master; "EMPTY hall", "ONLY plain pale sky" |
| 13 | SLOW line spoken faster than the FAST line | words per second | 1 clip | "How... was... your..." word by word |
| 13 | Mac at 1 % battery, render throttled, then 9 h asleep and locked | `pmset -g batt` | 9 h | Check power before clips and renders; tell the owner under 30 % |

## 3. What the numbers say

| | EP.1 | EP.2 | EP.3 | EP.4 | EP.5 | EP.6 | EP.7 | EP.8 | EP.9 | EP.10 | EP.11 | EP.12 | EP.13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Clips per accepted cut | 1.7 | 2.0 | 1.2 | 1.1 | 1.2 (26 clips / 21 lines) | 1.25 (25 clips / 20 lines) | 1.1 (22 clips / 20 lines) | 1.1 (20 clips / 18 lines) | 1.6 (35 clips / 22 cuts) | 1.2 (28 clips / 24 lines) | 1.7 (37 clips / 22 lines) | 1.9 (43 clips / 23 lines) | 1.8 (46 clips / 25 lines) |
| Refusals | 1 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Renders | not logged | 3 | 4 | 3 | **1** | **1** | **1** | **1** | **1** | 2 (first not uploaded) | 2 (first not uploaded) | 3 (first two not uploaded) | 3 (first two not uploaded) |
| Uploads | 2 | 3 | 2 | 2 | **1** | **1** | **1** (scheduled) | **1** (scheduled, uploaded by Claude) | **1** (scheduled, uploaded by Claude) | **1** (scheduled, uploaded by Claude) | **1** (scheduled, uploaded by Claude) | **1** (scheduled, uploaded by Claude) | **1** (scheduled, uploaded by Claude) |

- Yield improved once clips had a single character on screen and masters were detailed.
- **No episode has shipped on the first upload.** Each re-upload came from burned-in text or sync, never from
  the picture. The cheapest protection is in this order: spell-check `burned_text.txt`, `windows`, the owner
  listen check, `drift` on the delivered file, and the word check immediately after the first Save.
- EP.4 had no sync or wording re-upload; both of its extra renders came from **format** (Thai on screen, a new
  design). Porting the previous `build.py` and the English-only assert remove both causes.
- A goal for the next episode: one upload. **EP.5 met it** (one render, one upload): EP.4's `build.py` ported with only
  the timeline changed, `windows` 0, listen check passed, drift 0 ms on the delivered file before the drag.
- EP.5's only retakes were listener faults in two-shots (mouth, wet face); adult-alone (Mabel) and host clips all
  passed first time.
- EP.7: 0 listener faults with three masters per location (teen two-shot, hero-only close, adult-alone); the two
  retakes were a design drift (lashes) and a too-early start. All four new masters and the new sheet were first try.
- EP.8: 0 listener faults again with the three-master pattern (canal two-shot, Pudding close, Walter alone); retakes were a
  design drift (Lily's eyebrows) and a head-turn glitch at a word onset. Sheet → Scheduled in about 1 h of machine time
  once the screen was unlocked (08:06 → 09:06), with a local whisper word check replacing the owner listen.
- EP.8, found after upload: a wrong-way point on "It's on your right" (H4 take 1) and an off-model Walter (brow marks, no
  trousers in W03). Speed came from skipping the host and Walter contact sheets; the fix needs a new video id. See 03 §5a.

- EP.9: 35 clips for 22 cuts, the worst yield since EP.2, all from one cause: a new character whose face Meta kept redrawing.
  Make the **first** clip of a new character before the others and settle the face (masters + bible) on it.
- EP.11: 15 retakes, none from the listener or from words: 5 face details (Rosa, Pudding's eye), 3 background drift, 3 voice pitch, 2 host acting, 2 others.
  A clip took about 40 s from 01:36 at night (10 min before), so retakes were cheap.
- EP.10: that rule worked (Ned: 0 retakes). The four retakes were two host clips, Pudding's eyes/skin, and a sad face.

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
