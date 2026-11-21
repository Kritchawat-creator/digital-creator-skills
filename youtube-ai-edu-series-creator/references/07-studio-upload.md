# 07 — YouTube Studio upload

Done from a browser tool that has **no file picker**. The owner drags the video file; everything else is set by
script and read back. Selectors and coordinates were measured in November 2026 and will change: confirm each
with a screenshot.

## 1. Before opening Studio

- The delivered file passes `sync_check.py drift` (0 ms to the last clip) and the loudness check.
- `build/burned_text.txt` is spell-checked and the owner has watched and listened.
- The metadata doc is written (`06`).
- The owner has decided audience, AI disclosure and visibility. Upload is **Private**.
- **Close or reload every other Studio tab** that might still hold an upload dialog.

## 2. Steps

1. Open `studio.youtube.com/channel/<channel id>/videos/upload?d=ud` and ask the owner to drag
   `out/<episode>.mp4` in. (Studio's CSP blocks `http://127.0.0.1` fetches and images, so a local server
   doesn't help.)
2. **Work in the tab the owner dropped the file into.** If another tab must be used, reload the drop tab at once.
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
2. The owner drags the new file. **Reuse details from the superseded upload** (it is the first tile) to carry
   title, description, tags and playlist; replace only what changed (chapters).
3. In the end-screen picker the superseded video is listed first and looks identical. Pick the previous episode
   by its title and check the radio text. Tell uploads apart by video ID (the thumbnail URL contains `vi/<id>/`).
4. Run the word check on the new upload.
5. **The owner deletes the old upload**, or says in chat exactly which ID to delete. Before deleting, verify the
   URL's ID and the duration shown in the dialog.

Only a caption file wrong → edit the SRT in place; no re-upload.

## 7. Traps

- **A leftover upload dialog published a video.** The owner's drag opened the dialog in one tab; the work was
  finished in another. Clicking through the stale dialog reached Visibility with **Public** preselected, and
  EP.2 went Public. The owner kept it, but it should have been their choice.
- If the browser pane restarts between the drag and the next step, the upload survives as a **Draft** row in
  Content: "Edit draft" reopens the same dialog (`udvid=<id>` in the URL). Check there before asking for a
  second drag. The pane can also come back signed out; the owner signs in.
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
