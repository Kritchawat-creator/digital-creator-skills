# 07 — YouTube Studio upload

Done from the owner's Chrome by script. **The video file is uploaded by script too** (owner rule, 2026-11-24: "อัพโหลดไฟล์ได้แล้ว"):
nobody drags anything. Everything is read back. Selectors and coordinates were measured in November 2026 and will change: confirm each
with a screenshot.

## 1. Before opening Studio

- The delivered file passes `sync_check.py drift` (0 ms to the last clip) and the loudness check.
- `build/burned_text.txt` is spell-checked and the owner has watched and listened.
- The metadata doc is written (`06`).
- The owner has decided audience, AI disclosure and visibility. Upload is **Private**.
- **Close or reload every other Studio tab** that might still hold an upload dialog.

## 2. Steps

1. Open your **own** Studio tab at `studio.youtube.com/channel/<channel id>/videos/upload?d=ud` and upload the file
   yourself: `python3 tools/studio_upload_video.py <tab id> out/<episode>.mp4` (from
   `scripts/ep6_chrome_tools/`). It sends the bytes into the page in 1.5 MB base64 chunks over AppleScript, checks
   SHA-256 in the page, builds a `File` and puts it into the dialog's `input[type=file]` with `DataTransfer` +
   `change`, then prints the video link and Filename (EP.7: 76 MB in 62 s, upload complete within a minute).
   Studio's CSP blocks `http://127.0.0.1`, so a local server doesn't work; this does. Check the file exists on disk
   first. Don't ask the owner to drag.
2. **Work in the tab you uploaded in.** If another tab must be used, reload the upload tab at once.
3. Confirm the dialog's **Filename** and the video link before editing anything.
4. **Reuse details** from the previous episode (it copies title, description, tags, language, category and
   playlist), then replace title, description with chapters, and tags. Check the tag counter.
5. Audience: "not made for kids". Show more → altered content "No". Only as the owner decided.
6. Video elements → Subtitles → Upload file → With timing → Continue (injected English SRT) → Done.
7. End screen → template "1 video, 1 subscribe" → video element → Choose specific video → the previous episode
   (one click) → check the radio says "Video: <title>" and look at the preview → set the start times → Save.
8. Visibility **Private** → Save. Read back the video ID.
9. **Word check now** (section 5), before the slow steps. Automatic captions were ready within a minute of
   "Checks complete". If it fails, the re-upload costs only steps 3–8.
10. Thumbnail on the **edit page**, after processing has finished (`05`).
11. Subtitles page: Add language for each translation; upload the second-language `.srt`; set each language's
    title and description; Publish each.
12. Playlist: check it after Reuse details (it may already be there). Otherwise Content → Playlists → New
    playlist (Private, order "Date published (oldest)") — ask the owner first.
13. **Readback** (section 4) on the edit page after a reload.
14. Record "As uploaded" in the metadata doc and the result in `qc_log.txt`.

## 3. Controls that worked

| Step | Selector / control |
| --- | --- |
| Title / description | `ytcp-uploads-dialog #textbox[contenteditable]` [0] / [1]: focus → `execCommand('selectAll')` → `execCommand('insertText', …)` |
| Tags | chip bar `#clear-button`, then `insertText("a, b, c,")` + Enter keydown |
| Audience / altered | `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`, `#toggle-button` (Show more), `[name="VIDEO_HAS_ALTERED_CONTENT_NO"]` |
| Subtitles (upload dialog) | `#subtitles-button` → "Upload file" → Continue |
| End-screen times | Fields take `m:ss:ff` (frames). Type the start (for example `4:51:06`) and press Tab, per element. The template default starts 20 s before the end and overlapped the last spoken clip |
| Visibility | `[name="PRIVATE"]` then `#done-button` |
| Thumbnail (upload dialog) | `ytcp-thumbnail-uploader #select-button` |
| Thumbnail (edit page) | `ytcp-video-thumbnail-editor #select-button` (the first one = Upload file), then `ytcp-button#save` |
| Subtitles page rows | Buttons exist only after hover: focus `ytgn-video-translation-cell-captions #cell-container` (or `…-cell-metadata`) and dispatch `mouseenter` / `mouseover`; then `#captions-more-options` → Download → `.srt`, `#captions-add`, `#metadata-add` |
| Add language | "Add language" → `tp-yt-paper-item` by exact name |
| Translation dialog | Two editable textareas plus read-only ones (the original). Set values with the `HTMLTextAreaElement.prototype` value setter + `input` / `change` events; button "Publish" |
| Readback | `studio.youtube.com/video/<id>/edit`; `ytcp-video-metadata-visibility` text |
| Delete an upload | Edit page → `#overflow-menu-button` → Delete → tick the checkbox → "Delete forever" |

File input without a picker (SRT or thumbnail) — `scripts/studio_inject.js`:
```js
const orig=HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click=function(){ if(this.type==='file'&&window.__nextFile){ const dt=new DataTransfer(); dt.items.add(window.__nextFile); this.files=dt.files; window.__nextFile=null; this.dispatchEvent(new Event('change',{bubbles:true})); return;} return orig.call(this); };
window.__nextFile=new File([srtText],'ep.en.srt',{type:'application/x-subrip'});
```
- After any page navigation the `window` helpers are gone. Inject them again.
- Passing SRT text into the page: send a compact `end_ds|text` list (start only when there is a gap) and rebuild
  the SRT in page JS. It is a third of the size of the raw file.
- Building a translated description: translated intro + the English original from "📌" onward, read from the
  read-only textarea.

Thumbnail canvas (the art's fbcdn URL sends CORS headers; the font comes from fonts.gstatic.com):
```js
const f=new FontFace('Baloo2T','url(<fonts.gstatic.com url from the css2 response>)',{weight:'800'}); await f.load(); document.fonts.add(f);
const img=new Image(); img.crossOrigin='anonymous'; img.src=ART_URL; await img.decode();
// draw the art and the text with the same coordinates as the local thumbnail.py, then:
window.__nextFile=new File([await new Promise(r=>c.toBlob(r,'image/jpeg',0.92))],'thumb.jpg',{type:'image/jpeg'});
document.querySelector('ytcp-video-thumbnail-editor #select-button').click();
```

## 4. Readback

Reload `studio.youtube.com/video/<id>/edit` and check each item against the metadata doc:

- title, description (first and last lines), tag count
- audience and altered content
- **visibility** (`ytcp-video-metadata-visibility`)
- playlist
- **thumbnail, by looking at the picture:** the "Uploaded thumbnail" preview `img` has a `ytimg.com/…/mqdefault`
  src with `naturalWidth > 0` (an empty slot has the page URL as src and width 0). Take a screenshot too.
- subtitles list (languages and "Published"), end screen elements and times

On EP.3 the readback counted `img` elements; the auto-generated preview passed, and the owner noticed the
missing custom thumbnail.

## 4a. Gate before Public or Schedule: subtitles and translations

Owner rule (2026-11-23, EP.6: "อย่าลืมใส่ซับไตเติ้ลนะ", then "จำไว้อย่าลืมใส่ subtitle translation"). Before the
visibility step sets Public or Schedule, all of these must be true on the edit page's Subtitles tab:

| Item | Must show |
|---|---|
| English | uploaded `out/<series>_epN.en.srt` (With timing), first cue matches, cue count = file, **Published** |
| Thai | uploaded `out/<series>_epN.th.srt`, first cue matches, cue count = file, **Published** |
| English (automatic captions) | untouched (never click its pencil) |
| Title & description | translations **TH, ES, PT, VI, ID**, each **Published** |

If any line is missing, stop and finish it first, even when the owner said "publish now". Write the table into the
episode's upload-metadata doc with ✓ per line.

## 5. Word check with automatic captions

The QC tools can't hear words. YouTube's "English (automatic captions)" can, minutes after a Private upload.

1. Ask the owner first: the Download action also saves a `.srt` file to their machine.
2. On the Subtitles page wrap `fetch` / `XMLHttpRequest` to capture the response of
   `youtubei/v1/globalization/download_caption_track`.
3. Hover the "English (automatic captions)" row → ⋮ → Download → `.srt`.
4. Decode `content` (base64url) and compare it with the script and the burned subtitles, line by line:
```js
const j=JSON.parse(window.__capResp); const b=j.content.replace(/-/g,'+').replace(/_/g,'/');
const txt=new TextDecoder().decode(Uint8Array.from(atob(b+'='.repeat((4-b.length%4)%4)),c=>c.charCodeAt(0)));
```
- Expect harmless ASR noise ("2 weeks" for "two weeks", "5,000 bot" for "baht", stray fragments).
- A real mismatch with burned-in text (a missing "Thank you!", an extra "Yes.", a line said twice) → fix,
  re-render, upload as a new video.
- **Don't click the pencil on "English (automatic captions)"** when an uploaded English track exists: it offers
  "Overwrite track" for your captions. Cancel.
- The watch-page `timedtext` URL returns an empty body without the player's token. Use the Studio download.

Found this way: two subtitle/audio mismatches (EP.2) and a line spoken twice under a once-only subtitle (EP.3).

## 6. Re-uploads

YouTube can't replace a video file. When burned-in text or sync is wrong:

1. Fix and re-render; run every delivered-file check again.
2. Upload the new file the same way (`studio_upload_video.py`). **Reuse details from the superseded upload** (it is the first tile) to carry
   title, description, tags and playlist; replace only what changed (chapters).
3. In the end-screen picker the superseded video is listed first and looks identical. Pick the previous episode
   by its title and check the radio text. Tell uploads apart by video ID (the thumbnail URL contains `vi/<id>/`).
4. Run the word check on the new upload.
5. **The owner deletes the old upload**, or says in chat exactly which ID to delete. Before deleting, verify the
   URL's ID and the duration shown in the dialog.

Only a caption file wrong → edit the SRT in place; no re-upload.

## 6a. Notes from EP.4 (macOS, browser pane, 2026-11-21)

| Step | What worked |
| --- | --- |
| Languages | Same on every episode: English captions (uploaded, Published) + Thai captions; title/description translations TH, ES, PT, VI, ID; automatic English untouched |
| English SRT in the upload dialog | A **real click** on "Upload file" (a JS click does not create the input). Leave "With timing", do **not** press Continue (it opens the OS picker); inject into the new `input[type=file]`, check the first cues, Done |
| Pasting text into JS | Print the file with `json.dumps(..., ensure_ascii=False)` and paste it as a string; never type `\"` (swap `"` to `'` and back with `.replace`) |
| End screen times | Template "1 video, 1 subscribe" → Choose specific video. Select each element's bar, triple-click the start field, type `m:ss:ff`, Enter, then **Tab** — the bar moves only after blur. Both bars start at the end card |
| Thumbnail | Redraw in-page on a canvas (Meta AI fbcdn art + OFL fonts from `raw.githubusercontent.com/google/fonts`), inject into `#file-loader` on the edit page, Save. **The first injection right after the upload dialog saved without changing the thumbnail**; a second one after a fresh load stuck. Reload and look at the Thumbnail block every time; a grey "…" `mqdefault` right after saving is processing, not a failure |
| Add language menu | Long list: find the `tp-yt-paper-item` by exact text, `scrollIntoView`, then click (off-screen items fail an `offsetParent` filter) |
| Thai captions | Click the Subtitles cell, then its pencil → real click "Upload file" → inject into the **last** `input[type=file]` → Publish |
| Translations | Click the Title & description cell, then its pencil; fill the visible `ytgn-metadata-editor` (`textarea[1]` title, `textarea[3]` translated opening + English rest from `textarea[2]`), dispatch `input`+`change`, Publish. Move the mouse away before reading the table (hover replaces cell text with icons) |
| Deleting the superseded upload | Only on the owner's yes. Content row → hover → ⋮ → Delete forever; check the duration in the dialog (the two uploads have the same title), tick the box, Delete; reload and list rows by video ID |

## 6b. Notes from EP.5 (2026-11-21, one upload)

| Step | What worked |
| --- | --- |
| Reuse details | Upload dialog → "Reuse details" → previous episode tile → keep all ticks → Reuse: carries playlist, tags, language, category, Shorts remixing; then overwrite title/description (`#textbox` + `execCommand('insertText')`) and tags (chip bar `#clear-button`, insert the comma list + Enter) |
| Schedule (owner asked) | Visibility step → `#second-container-expand-button` (Schedule) → date picker (click the day) → time field opens a list (`find` "8:00 AM" option, scroll_to, click) → time-zone list (first item = GMT+0700 local) → "Schedule". Read back the "Video scheduled … set to public on <date> at <time>" dialog and the Content list ("Scheduled", date) |
| End-screen readback | Opening the saved end screen on the edit page to read it back leaves a modal that Escape and "Discard changes" (with nothing changed) don't close; reload the edit page to leave it (the saved end screen is unaffected) |
| End screen | Fields often keep the old start until the bar is reselected: type the start, Tab, Tab, click the empty timeline, then click each bar and zoom on its start field; both must read 4:50:03-style values |
| Thumbnail canvas | `FontFace('…','url(https://raw.githubusercontent.com/google/fonts/main/ofl/baloo2/Baloo2%5Bwght%5D.ttf)',{weight:'400 800'})` and Nunito `{weight:'200 1000'}`; Pillow's `d.text((x,y))` top = canvas baseline `y + ascent` (`font.getmetrics()[0]`); Pillow `stroke_width=10` = canvas `lineWidth=20` + `lineJoin='round'`. Check `measureText` width against Pillow's `textlength` (EP.5: 348.9 vs 348). Inject into `ytcp-video-thumbnail-editor #file-loader` on a freshly loaded edit page, Save — stuck first try |
| Translations | `Add language` → `tp-yt-paper-item` by exact name for all five first; then per row: real hover on the Title & description cell, click its pencil, check the editor header reads "English\n<Language>", fill `textarea[1]` / `textarea[3]` with the value setter + `input`/`change`, Publish (button inside `ytgn-metadata-editor`). The dialog can take ~3 s to open; retry the header check instead of filling a stale editor |

## 6c. Notes from EP.7 (2026-11-24, scheduled)

| Step | What worked |
| --- | --- |
| English SRT (upload dialog) | `#subtitles-button` → "Upload file" (JS click) → inject into `#captions-file-loader`; the cues load behind a leftover "Select subtitles file type" picker → click its **Cancel**, then **Done** in the English editor |
| Thai SRT (Subtitles page) | Dispatch `pointerover`/`mouseover`/`mousemove` on every cell of the Thai row (`td`, `ytgn-video-translation-hover-cell`) → `#captions-add` appears → "Upload file" → inject into the last `input[type=file]` → Cancel the leftover picker → Publish |
| Cue counts | Uploaded English: "Edit as text" gives one textarea → 85 = file. A translation track ignores "Edit as text" and renders rows lazily: scroll the editor and key each `div.segment` by its start/end timestamps (`m:ss:ff`), then match every file cue start (±0.1 s) → 85 = 85 |
| Automatic captions download | Hover events on the row → `#captions-more-options` (never `#captions-edit`) → "Download" (in `tp-yt-paper-listbox`) → ".srt"; the file lands in `~/Downloads` (fetch/XHR wrapping didn't capture it) |
| End screen | `es_time2.js` sets both, but the first element reverted to the template start; set it again alone (`[0]` item), click the timeline, reselect both and read `ytve-framestamp-input` values |
| Schedule (edit page) | visibility `#select-button` → `#second-container-expand-button` → `#datepicker-trigger` → `.calendar-day` "24" in the "Nov 2026" block → time input → leaf "8:00 AM" item in `ytcp-time-of-day-picker` → Done → `ytcp-button#save` → reload: "Visibility Scheduled", picker "Nov 24, 2026 / 8:00 AM / GMT+0700"; Content list shows "Scheduled · <date>" but no time. **No Escape** inside the picker |
| Previous episode's "coming soon" link (Pudding season 1: standing yes, see §8; another series needs its own yes) | Edit page, background tab: reload, find the one text node with the old line in `#description-container #textbox`, select only that range, `execCommand('insertText')`, check the new text equals the old text with that one replacement, Save, reload, compare again. **The TH/ES/PT/VI/ID translations keep the old line**: ask for them in the same question, then run `link_translations.py <tab on /video/<id>/translations> "<old>" "<new>" <backup.json> <Language>` one language at a time, reloading the tab between them (it backs up, changes only that line and clicks the editor's own `#publish-button`, because a background tab never paints the dialog), and compare the public `&hl=` pages with the backup |

## 6d. Notes from EP.8 (2026-11-24, uploaded by Claude, scheduled)

| Step | What worked |
| --- | --- |
| Upload | `studio_upload_video.py` in a freshly navigated `/videos/upload?d=ud` tab: 88 MB, SHA OK, 71 s. Make the Studio tab the window's active tab first (`set active tab index`): while it was a background tab every dialog button read `offsetParent=null` |
| Reuse details | `#reuse-details-button` → click the `ytcp-entity-card` whose text has the previous "EP.n" → `#select-button` (Reuse) |
| End-screen template | `.click()` on "1 video, 1 subscribe" did nothing; pointer events with clientX/Y on the template's `.card` (pointerdown, mousedown, pointerup, mouseup, click) applied it. Choose specific video → click the `ytcp-entity-card` of the previous episode → radio text reads "Video: <title>". Subscribe kept 4:56:03 after the shared set; `es_one.js` on element [0] fixed it |
| Caption editor buttons | On the Subtitles page `#captions-edit` / `#captions-add` appear only after hover events on every cell + a JS click on the row's first `ytgn-video-translation-hover-cell` and its `#cell-container`, then **wait ~1.5 s** before querying |
| Cue counts after publish | Open each track with `#captions-edit`, count `ytve-captions-marker-container` (EN 94 = file, TH 90 = file), close with the editor's `#close-button`; no edits, nothing to save |
| Schedule time | The time list's "8:00 AM" contains a narrow no-break space: match with `textContent.replace(/[\s\u202f\u00a0]+/g,' ').trim()`. Time zone line reads "Default set to local time zone (GMT+0700)". Content list columns: `Scheduled / Nov 25, 2026` |

## 6e. Notes from EP.9 (2026-11-24, scheduled)

| Step | What worked |
| --- | --- |
| English SRT | `#subtitles-button` → patch `HTMLInputElement.prototype.click` (no OS picker) → leaf "Upload file" click → set `input#captions-file-loader` files + `change` → count `ytve-captions-marker-container` → the type picker's `#cancel-button` → `#publish-button` ("Done") → the button reads "Edit" |
| Radios after Reuse details | Reuse does **not** carry audience or altered content: both read `aria-checked=false`; set and read back |
| End screen | Pointer events on the "1 video, 1 subscribe" `.card`; select item [1] (video) → "Choose specific video" → the card whose HTML has the wanted id; start `4:52:03` typed per element, twice, then both read back |
| Date | `#datepicker-trigger` → `.calendar-month` with "Nov 2026" → `.calendar-day` "26"; time input click → `tp-yt-paper-item` "8:00 AM" (normalised spaces) → Done → `ytcp-button#save` → reload and reopen the picker to read it |
| Whole Studio pass | 20:0x → 20:2x, about 25 min by script, with `build/st.py` (`J(js)` helper) instead of one-off files |

## 6f. Notes from EP.10 (2026-11-25, scheduled)

The whole Studio pass is in `scripts/ep6_chrome_tools/studio_steps_ep10.txt` (every command in order, all worked first try, about 15 min
from the upload to the read-back schedule; `st.py` = the `J(js)` helper, `es.py` = end-screen times). Pick the Reuse-details card and the
end-screen card **by id** (`outerHTML.includes('<previous id>')`). End-card start in frames = whole seconds + tenths × 30 (300.1 s → `5:00:03`).
Automatic captions can add a stray word over the end-card music ("Hey,"): not a mismatch.

## 6g. Notes from EP.11 (2026-11-25, scheduled)

`studio_steps_ep10.txt` again, every step first try (03:16 → 03:29). Change five things: episode number in the file names, the previous episode's id
(two places: Reuse card, end-screen card), the new id, the calendar day, the end-card start in `es.py` (296.7 s → `4:56:21`). Generate everything in Meta AI
before switching the window to the Studio tab (a hidden meta.ai tab stops rendering), and switch back to it afterwards.

## 6h. Notes from EP.12 (2026-11-25, scheduled)

`studio_steps_ep10.txt` a third time, every step first try (09:31 → 09:45). Before opening Studio check the delivered file with `ffprobe`: `r_frame_rate` 30/1 and
duration equal to the plan (EP.12 render 1 was 60/1 and 0.5 s too long).

## 6i. Notes from EP.13 (2026-11-25, scheduled, season finale)

`studio_steps_ep10.txt` a fourth time (21:16 → 21:36). One trap: the end screen showed 5:37:18 in the editor but the first save kept the template's 5:33:18 (last 20 s).
**Always re-open the end screen after the reload and read both elements' times.** Fix: edit page → "End screen" → `es.py` again → the editor's Save → re-open and read (EP.12 and
earlier were read back right). On a season finale the description and the translations carry no "Next episode" line.

## 7. Traps


- **A leftover upload dialog published a video.** The upload opened the dialog in one tab; the work was
  finished in another. Clicking through the stale dialog reached Visibility with **Public** preselected, and
  EP.2 went Public. The owner kept it, but it should have been their choice.
- If the browser restarts between the upload and the next step, the upload survives as a **Draft** row in
  Content: "Edit draft" reopens the same dialog (`udvid=<id>` in the URL). Check there before uploading a
  second time. The pane can also come back signed out; the owner signs in.
- The end-screen chooser closes on the first click; a second click lands on "Most recent upload". Click once,
  then check the radio.
- A Private previous episode can be an end-screen element, but viewers of a Public video won't see it. Tell the
  owner.
- End screens need at least one video or playlist element, so the first episode of a series can't have one until
  a playlist or a second episode exists.
- Custom thumbnails need a phone-verified channel.

## 8. What needs the owner's yes in chat

Audience and AI disclosure; anything Public; creating a playlist; the automatic-captions download; deleting an
upload (naming the video); changing an older episode. A yes for one of these doesn't cover the next.

**Never on this list: uploading the video file.** Claude uploads it itself with `studio_upload_video.py` and does not
wait for the owner (owner, 2026-11-24: "สามารถอัพโหลด คลิปลง youtube เองได้เลย ไม่ต้องรอฉัน"). When the owner has
given a release plan (e.g. EP.7–EP.10 "daily 08:00"), scheduling at that slot and the automatic-captions download are
covered by it (refs/10 §5).

**Next-episode links, Pudding season 1** (owner, 2026-11-24, asked about every older episode in all languages: "Yes, all
episodes"): after episode N is Scheduled, replace the "(coming soon)" line of episode N-1 with N's link in English and
TH/ES/PT/VI/ID. That one line only; reload and compare. Nothing else on an older episode is covered by this yes.
