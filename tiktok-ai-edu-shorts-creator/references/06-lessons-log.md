# 06 — Lessons log and report outline

Rows 1-57 are folded into `SKILL.md` and `01`-`05` (2026-11-21, EP04 session); new rows go below, then into the references.

Add a dated block after every episode. Each lesson: what happened, the evidence, the rule it produced.

## EP01 "Open the light?" (Talkoro TikTok, 2026-11-21)
Numbers: 3 masters (3/3 first try), 6 clips for 5 accepted, 0 refusals, rough cut 22.5 s / 10.4 MB, drift 0 ms,
-17.9 LUFS. Files: `talkoro-tiktok/ep01-open-the-light/` (`qc_log.txt` has the full record).

| # | What happened | Evidence | Rule |
| --- | --- | --- | --- |
| 1 | Script v1 put a standing teacher's head in the lower-left foreground of a seated OTS shot | geometry review before generation | Check who sits/stands and screen direction before any prompt (`01`) |
| 2 | Premise needs lamps OFF; payoff with lamps ON in the solo master | masters M1-M3 | Make the set prove the premise; use the solo master for the payoff |
| 3 | Video added an apple-shaped logo to a plain laptop lid (master was plain) | C1_v1 crop at 3 s | Plain-prop sentence in every prompt; crop props at 4-5 times; FAIL if inside the cut |
| 4 | Same logo appeared at 9.5 s in C4 | C4_v1 crop at 9.5 s | Only the cut window matters; note it |
| 5 | Mint mouthed silently 1.0-4.4 s, then spoke 4.6-6.3 s in sync | mouth strip + "[no audio]" in whisper | Cut to the audio; ask the owner to watch that sync |
| 6 | Sighs / long blinks / grins after the line in 4/5 clips | `asr.sh` on tails = "(sighs)" | Out point right after the last word, every clip |
| 7 | "Starting within the first second" ignored (speech at 4.6 s, 1.7 s) | timelines | Trim the lead-in; don't regenerate for it |
| 8 | Intentional mistake "open" kept by Meta in C1 and C2 | whisper | Always whisper-check it anyway |
| 9 | Unaligned cuts drifted 30 ms by segment 5 | `drift.py` first build | Frame-align in/out at 24 fps, pad/trim audio (`build.sh`) |
| 10 | Homebrew ffmpeg has no `drawtext` | qc sheet error | Untimestamped tiles; count them (1 tile = 1 s; strips 0.2 s) |
| 11 | Skill scripts had hard-coded relative paths | port review | Scripts resolve their own folder; run from the episode folder |
| 12 | Owner: TikTok text must be English only (global, like YouTube) | owner message | No Thai in text/caption/subs; Thai only when talking to the owner |
| 13 | Prompt box ignores `form_input`; `cmd+a` never selects in the pane | Meta AI, TikTok description and editor | Type into the visible box; select with JS |
| 14 | TikTok editor fonts don't render ❌ ✓ ✗ | preview | Words + colour |
| 15 | TikTok web has no Save draft; Post/Schedule publish | upload page buttons = Post, Discard | Never press them without a yes; never leave the tab |
| 16 | TikTok preview is a canvas | `<video>` lookup empty | Verify overlays by playing + zooming at each time |
| 17 | Pane viewport resets on resize/turn end | tool note mid-edit | Re-screenshot before coordinate clicks; set 1400x900 again |

## Report outline (owner's language; files sent with the report)
1. What is done, with links: rough cut, masters, cover, SRT, `qc_log.txt`.
2. Script changes and why (one line each).
3. Clips: generated / accepted, every FAIL with its reason.
4. Listen/watch list with rough-cut timestamps.
5. What is on the TikTok post (description, cover, overlays, AI label) and what is not (e.g. full captions).
6. Scheduled time read back from Studio → Content (or "not posted" + who presses Post, when no slot is approved).

## EP02 "I'm boring?" → "I'm bored" (Talkoro TikTok, F2 Don't Say / Say, 2026-11-21)
Numbers: 2 masters (2/2 first try), 5 clips for 5 accepted, 0 refusals, cover 1/1 spelled exactly, rough cut 30.0 s /
17.4 MB, drift 0 ms, -16.3 LUFS. Script → rough cut in ~15 min of generation (16:05-16:13). Files: `talkoro-tiktok/ep02-im-bored/`.

| # | What happened | Evidence | Rule |
| --- | --- | --- | --- |
| 18 | First prompt typed into an unhydrated Meta AI composer: prehydration `<textarea>`, Send disabled, Return ignored | `[data-testid=composer-add-attachment-button-skeleton]` present; console 503s | Before typing, wait until the skeleton is gone and the box is a contenteditable; if stuck, reload your own tab |
| 19 | F2 solo-to-lens format: no listener, every clip to lens, no laptop in frame | 5/5 clips PASS, no logo or eyeline checks needed | For F2 write "no laptop and no computer anywhere"; skip the from-behind check; alternate two framings (waist-up / chest-up) so pose jumps read as cuts; quiz clip on the hook's framing for the loop |
| 20 | All three intentional mistakes kept ("I'm boring", "interesting in English", "confusing") with "it is the common mistake on purpose, keep it exactly" | whisper on clips and the whole cut | Keep that sentence for every deliberate error |
| 21 | Meta added a word to the quiz line ("a long, long, LONG meeting") | whisper C5 | Harmless repetitions: accept, make the SRT match the audio, list it for the owner |
| 22 | A 5 fps mouth strip suggested a 0.3 s lip offset; 10 fps showed sync was fine | C5 7.4-9.0 | Before failing a clip for sync, re-check the window at 10 fps |
| 23 | Leo-to-lens clips end in a sigh/head drop 0.2-0.5 s after the last word in 5/5 | `asr.sh` tails "(sighs)" | Same out-point rule as EP01; it holds for solo clips too |
| 24 | Two-line speech with a natural pause gives ~30 s for 5 clips | cut length | F2 with 3 swaps + rule + quiz lands at the 30 s cap; for shorter, merge the rule into C1 or drop one swap |
| 25 | The TikTok upload page showed "A video you were editing wasn't saved. Continue editing?" after EP01 had already been posted (Studio → Content lists EP01 at 15:58) | page text | Check Studio → Content in a separate tab before deciding what the banner means; never press its Discard yourself |
| 26 | Claude in Chrome `file_upload` caps one call at 10 MB; the CRF 16 cut is 17 MB | tool schema | Keep a CRF 22 re-encode (`out/*_upload_small.mp4`, 7.8 MB, drift 0 ms) ready for an extension upload |
| 27 | Clicking the "AI-generated content" switch by coordinates hit its "Learn more" link and navigated the upload tab away | tab URL became /tns-inapp/pages/ai-generated-content | Toggle switches by `find`/ref or JS-located element, never by coordinate near a link; if it happens, reopen /tiktokstudio/upload and press "Continue editing" — video + switches survive, the description does NOT (retype it) |
| 28 | Description: JS range-select + one Backspace deleted only ONE character (first time) | read-back "ep02_im_bored_roughcu…" | After Backspace, read back; if text remains, Backspace ×N (N = remaining length), then type |
| 29 | Editor: the first Stroke "+" click after a font-size Return or a closed fill popup is swallowed | 3 of 5 layers had no stroke until clicked again | Zoom-check Fill/Stroke/Shadow on every layer before Save; click Stroke "+" again if missing |
| 30 | Font dropdown order changes (recent fonts move): a fixed y-coordinate picked Nunito | layer 5 | Screenshot the open dropdown before choosing the font |
| 31 | A text layer dragged past the clip end makes the project longer (30.5 s) | timeline total 00:30:12 | Keep the last layer's right edge inside the video; check the total reads the clip length |
| 32 | Cover upload by the owner inside the built-in pane did not deliver the file (dialog file input 0 files); page fetch from localhost blocked | JS read of `input[type=file]` | Cover needs a real file upload: owner in their own Chrome / desktop, or the Chrome extension. Check `input[type=file].files.length` and the profile preview before scheduling |
| 33 | Scheduling: "Schedule" radio → consent "Allow your video to be saved for scheduled posting?" → time picker (hour/minute columns; one scroll tick = one step, clicking an item recentres) defaults to now+15 min in the browser TZ | page | Check `Intl…timeZone`, set hour by click, click the top minute item until 00 shows, read "Schedule" on the button, then confirm in Studio → Content ("Nov 21, 8:00 PM (GMT+7) Bangkok") |
| 34 | Owner asked "why does EP02 have no cover?" — the Meta AI cover never reached TikTok; and a **scheduled post cannot be edited** (Studio tooltip "Scheduled posts cannot be edited."). After it is posted, Studio → Content → pencil → Edit cover works, but "Captions and covers can only be edited once a day and within the first 7 days of posting." | Studio content page, EP01 edit page | Get the cover file into the upload page BEFORE pressing Schedule (owner's own Chrome or the extension) and confirm the 4:3 profile preview shows it; if it is missed, fix it after the post goes live (within 7 days) |

## EP03 "When finish?" → "When do you need this by?" (Talkoro TikTok, F3 Meeting English, Khun Dao + Mint, 2026-11-21)
Numbers: 3 masters (3/3 first try), 6 clips for 5 accepted, 0 refusals, cover 1/1 spelled exactly, rough cut 22.6 s /
11.3 MB, drift 0 ms, -16.4 LUFS. Script → rough cut 16:20-16:34; scheduled 16:49. Files: `talkoro-tiktok/ep03-deadline/`.

| # | What happened | Evidence | Rule |
| --- | --- | --- | --- |
| 35 | First Dao + Mint pairing (38 + 24 across a small table): no refusals, no mother/child read | 3 masters + 6 clips | For a mentor + learner pair add "Two adult coworkers in a short work meeting", "<learner> is a grown-up 24-year-old woman, adult proportions", "<mentor> looks 38, not older" to every prompt |
| 36 | Seating both characters across a small round meeting table, no laptop/phone/written paper | 0 logo/text failures; listener from behind static in 4/4 OTS clips | F3 set: meeting table + plain folder + mug; "NO laptop, no computer, no phone, no papers with writing anywhere" |
| 37 | "with a short pause between the two questions" + "..." gave a 2.7 s silent gap (C4_v1) | timeline 3.3-6.0 s | Never ask for a pause inside a line; ask for "one smooth flow with only a tiny breath between them (no long pause)" (C4_v2: 0.6 s) |
| 38 | Two-word broken English "when finish" was spoken as written, but whisper always transcribes "finished" | 3 whisper runs; owner listened and approved | Whisper "corrects" short broken phrases; for a deliberate error that whisper can't confirm, put it on the owner listen list instead of regenerating |
| 39 | Asking the owner once, early (masters + C1 + first Dao clip + cover ready, one 8 s check file sent with SendUserFile) kept the pipeline moving | answer in ~3 min | Batch the voice check with the upload-timing question; send the check file proactively |
| 40 | Built-in pane, hidden: page has 0x0 viewport but screenshots (800x600 frame), clicks and typing still work | Meta AI tab | Don't stop for a hidden pane; screenshot first to get the frame size |
| 41 | Cover image did not reach TikTok's Edit cover from the built-in pane: owner's Upload-cover file pick -> input 0 files; page fetch of the fbcdn URL and of a 127.0.0.1 CORS server -> "Failed to fetch"; synthetic cmd+v -> no paste event. Owner drag-drop / Cmd+V onto the dialog: my drop/paste hooks logged NO event, so it is unclear whether they were blocked or not tried (MP4 drag-drop into the upload page DID work) | `input[type=file].files.length`, hook logs | In the pane, have a frame cover ready (hook frame, overlay inside the 4:3 crop). For the real cover use Claude in Chrome `file_upload` or the owner's own Chrome before Schedule, or Studio -> Content -> pencil -> Edit cover once the post is LIVE (scheduled posts can't be edited). Worth one retry: owner drags the PNG straight onto "Upload cover" with a drop hook installed |
| 42 | TikTok font dropdown ignores the computer-tool click; a JS pointer/mouse event sequence on `.PropSettingTextFontFamily__trigger` opens it, then a normal click on the `.Select__item` works | editor | Use `window.__openFont()` (dispatch pointerdown/mousedown/pointerup/mouseup/click) and read the item's rect |
| 43 | Fill/Stroke first click swallowed again after a size Return (as #29), on Fill too | layers 2-4 | Click Fill/Stroke, screenshot, click again if the picker/colour didn't appear |
| 44 | The schedule time picker had no consent popup on the 2nd scheduled post; one scroll tick moved the hour one step; clicking a visible item recentres (17 → 13 → 10 → 08) | page | Set minute 00 first, then click hour items toward the target; read `input` values ("08:00", "2026-11-22") before pressing Schedule |
| 35 | Re-post: the owner's second cover upload in the pane DID land (the first did not; cause unknown, probably the dialog flow) | 486x648 crop pixel check | Always verify the cover by pixels/preview after the owner says "uploaded" — never trust "done" alone |
| 36 | Editor: a JS `focus()` on the size input right after choosing a font reverted the font to the previous one | layer 1 of the re-post | Set size by `triple_click` on the size box + type + Return (no JS focus); screenshot after the font pick |
| 37 | Shadow "+" is swallowed as often as Stroke "+" (3/5 layers on the re-post) | zoom of Style panel | Zoom-check Fill/Stroke/Shadow on every layer; re-click whichever shows "+" |

## EP04 "I very like it?" → "I really like it" (Talkoro TikTok, F1, Mint + Leo, café, 2026-11-21)
Numbers: office masters 3 (dropped after the owner's new location rule), café masters 5 for 3 accepted, 10 clips for 5
accepted, 0 refusals, cover 2 (both spelled exactly), rough cut 22.25 s / 12.3 MB, drift 0 ms, -19.1 LUFS. Script → final
cut 16:55-17:33 incl. one location switch and one face fix. Files: `talkoro-tiktok/ep04-really-like/`.

| # | What happened | Evidence | Rule |
| --- | --- | --- | --- |
| 45 | Owner mid-episode: "ให้สถานที่ แต่ละตอน หลากหลายหน่อย ไม่ซ้ำกัน ให้คลิปดูหน้าสนใจ" — every episode a new location | owner message ~17:20 | Pick the episode's location from spec §3's table; masters for the old set go to `masters/*_unused/`; characters, voices, overlays, cover template stay |
| 46 | A re-prompt for a better M1 came back as an EDIT of the previous image (only the laptop changed, same face) | office M1_v1 vs M1_v2 | When fixing a character, start the prompt with "Create a brand-new image from scratch (do not edit or reuse the previous image)" |
| 47 | In the new café masters Mint's face drifted rounder/chubbier and read younger than EP01/EP03; the bible's "round face" wording pulls that way | face crops at master scale (`build/faces.png`) | Run the §10 face check on the MASTERS before any clip; for Mint add after the age line: "a slim oval adult face with gently defined cheekbones and chin (not chubby baby cheeks), eyes big but not oversized, adult neck and shoulders; looks like a 24-year-old office worker" (+ "cable-knit" cardigan, which the sheet has) |
| 48 | Café clips are framed WIDER than their masters (whole café, characters smaller); consistent across all clips from the same master | C1-C5 sheets | Accept as the episode look if all clips match; judge faces on a 1:1 crop of the clip, not only the master |
| 49 | Big open smile + silent mouthing between "Leo," and the rest (C1_v1); a teeth grin at the out point | mouth strip | Add "says the whole line in ONE smooth flow (no pause after the name), warm closed-mouth look between words" and "As soon as her last word is said, she closes her mouth" — fixed in C1_v2/v3, C4, C5 |
| 50 | Mint looked down at her cup with eyes closed for a whole sentence (C4_v2) — breaks "characters look at each other" | strip 1.4-4.0 s | For a line said to the other character add "KEEPS her eyes open on <X> for the whole line (does not look down at the cup, does not close her eyes)" |
| 51 | Out point 6.4 clipped the last word "it" (C2); only the whisper of the WHOLE delivered cut caught it ("I really like?") | whole-cut whisper | Whisper the whole cut after every build and compare word by word with the script; move the out point, not the line |
| 52 | Meta's café prompt "nobody else" gave blurred customers/passers-by in 2 clips | C1_v1, C5_v2 | "Nobody else appears anywhere: no customers, no staff, no passers-by" removes people indoors; far blurred passers-by outside the window are allowed by spec §3 |
| 53 | Built-in pane: a new image sometimes stays an empty `<img>` (no src) until clicked; clicking opens a viewer with its OWN prompt box (a prompt typed there still posted to the thread) | DOM read, screenshot | To fetch a lazy image: click it, read `__newimgs()`, press Escape before typing the next prompt; check `[contenteditable]` count is 1 |
| 54 | Teaching rule wording: "very goes at the end" is wrong ("I very much like it" is fine) | advisor review | State the rule precisely in lines, overlays and caption: "very alone can't go before a verb: use really before it or very much after it" |
| 55 | TikTok editor: the preview canvas (`.StageCanvas__screen`) was 0x0 after opening Edit at 1400x900 — no picture to place text on | DOM rect, blank stage | Open the zoom menu (top centre "100%") → "Zoom to fit"; the frame appears |
| 56 | Owner's Upload cover in the pane WORKED for EP04 (cover_v2), though my change/drop/paste hooks logged nothing and `input[type=file]` stayed 0 | dialog + profile preview showed it; 486x648 cover had red/green text pixels | Judge the cover by the preview + pixel check (red/green text rows in the top half), not by the file input or hooks |
| 57 | Scheduling in one pass: Schedule radio → date picker (click 22) → time: minute 00, then hour 17 clicked directly (visible in the list) → inputs "17:00"/"2026-11-22" → Schedule → redirected to Content | Content "Nov 22, 5:00 PM (GMT+7) Bangkok" | No consent popup on later posts; reload Content to read back |

## EP05 "Can you loop me in?" (Talkoro TikTok, F4 POV quiz, Khun Dao + Mint, lobby by the lifts, 2026-11-21)
Numbers: masters 7 for 3 accepted, clips 7 for 5 accepted, 0 refusals, cover 2 (both spelled exactly), rough cut 21.96 s /
13.5 MB, drift 0 ms. Script → rough cut 18:00-18:23; owner upload + cover swap + overlays + schedule to 19:53. Files: `talkoro-tiktok/ep05-loop-me-in/`.

| # | What happened | Evidence | Rule |
| --- | --- | --- | --- |
| 58 | STANDING scenes: Meta framed wide/full-body; Mint at full height next to Dao reads child-sized (M1_v1, M2_v1, M3_v1, cover_v1) | masters, cover | For standing shots ask for "CLOSE over-the-shoulder … only the back of <A>'s head and shoulder, big, cropped by the frame edge" and "MEDIUM CLOSE-UP from the chest up, legs and feet NOT visible"; for two-person covers "chest-up, <A> only a little shorter than <B> (two adult women of similar height)" |
| 59 | Mint looking UP at the taller Dao + round cheeks read young (M2_v2); level eyeline fixed it | face montage | "her head is level (not tilted back), eyes at about her own eye level, calm composed professional look" + "round gold glasses are normal adult size, not oversized" |
| 60 | Cardigan grew a hood once (M1_v1) | master | Add "cable-knit pattern and NO hood" to Mint's block for the episode |
| 61 | Lift lobby: naming the text hazards (floor indicator, maker's plate, exit sign, directory, call panel "two plain round buttons, no arrows, no numbers", matte champagne doors not mirror-shiny) gave 0 text in 7 masters + 7 clips | crops | Ban a location's typical text surfaces BY NAME in M1 and copy the block word for word |
| 62 | Letter lists: "A, B, or C?" came back "A, A, B, or C?" (C3_v1), then a long pause with silent open-mouth mouthing + an extra "A or C?" (C3_v2) | whisper windows, mouth strip | "each letter only ONCE" + "one smooth flow, tiny breath only" + "for the rest of the video stays silent with lips gently pressed together … her mouth does not move after the line" (C3_v3: clean line + 1 s closed-lip hold = reading time for the choices) |
| 63 | "Sorry... loop you in?" with an ellipsis produced "Ah… sorry" twice before the real line (C2_v1, usable window 5.6-6.95) | whisper windows | Never write "..." in a line; use a comma |
| 64 | A worried/sad face for "a little unsure" and for a quiz host (C2/C3_v1) | sheet | Quiz host clips: "bright, curious, friendly look (not worried, not sad)" |
| 65 | Owner uploaded cover_v1 (the file I had already rejected) — the folder held both | Edit cover preview | Before asking for the upload, move rejected covers out of `cover/` (or name the exact file in the request) and verify the thumbnail is the right version, not just "a cover" |
| 66 | TikTok text box width is fixed (~75% of the stage); DynaPuff 20 wraps "B) include me / CC me" mid-phrase | editor | Break long overlay lines by hand; keep each line ≤ ~18 characters at size 20 |
| 67 | Size box: triple_click + "20" + Return gave 21 on 2 of 4 layers | input value read | After setting the size, read `input` values by JS and redo if it is not the target |
| 68 | Schedule time picker opened ABOVE the field over the Location row; coordinate clicks on hour items fell through and set Location (Phuket Island, Bangkok). JS clicks on items did nothing | Location input value | Set the time by scrolling the picker columns (one `scroll` action = one step) and read `input` values; after any stray click read the Location input and clear it (×) before Schedule |
| 69 | Clip windows: Meta clips framed wider than the masters again (lobby) — consistent per master | sheets | Same as #48: accept if every clip of a master matches |
