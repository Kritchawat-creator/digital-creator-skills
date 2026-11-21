---
name: youtube-studio-upload
description: Upload and finish a YouTube episode in YouTube Studio from a browser tool without a file picker - owner drags the video, then Reuse details, title/description/tags, custom thumbnail via canvas, audience and altered-content settings, subtitles (SRT injected), end screen to an earlier episode, title/description translations, playlist, visibility, and a word check against YouTube's automatic captions. Use when uploading a lesson episode to Studio, replacing a bad upload, or adding subtitles/translations/end screens. Triggers: upload to YouTube, YouTube Studio, reuse details, end screen, add subtitles srt, translations title description, playlist, automatic captions check, re-upload.
---

# YouTube Studio Upload

## When to Use
- Uploading a finished episode (Private first) and filling every Studio field.
- Replacing an upload whose burned-in text or A/V sync is wrong (YouTube can't replace the video file).
- Adding subtitles, title/description translations, end screens or a playlist to an existing video.

## When NOT to Use
- Deciding audience, AI disclosure or public visibility. The owner decides; ask before setting them.
- Checking the video itself. Run lip-sync and A/V sync QC (skill `ai-video-lipsync-qc`) on the delivered file **before** uploading.

## Core Workflow
1. Before upload: delivered file passes `sync_check.py drift` (0 ms to the end), burned-in text list is spell-checked, the owner has watched it.
2. Open `studio.youtube.com/channel/<id>/videos/upload?d=ud` and ask the owner to drag the file in (the browser tool has no file upload; Studio's CSP blocks localhost fetches).
3. Work in **the tab the owner dropped the file into**. If you have to use another tab, reload the drop tab immediately (see pitfalls).
4. Confirm the dialog's **Filename** and video link before editing anything.
5. **Reuse details** from the previous episode, then replace title, description (with chapters) and tags.
6. Thumbnail: redraw on a canvas in the Studio page (code below) → patched file input → `ytcp-thumbnail-uploader #select-button`.
7. Audience `VIDEO_MADE_FOR_KIDS_NOT_MFK`, Show more → `VIDEO_HAS_ALTERED_CONTENT_NO` (only as the owner decided).
8. Video elements → Subtitles → Upload file → With timing → Continue (injected EN SRT) → Done.
9. End screen → template "1 video, 1 subscribe" → video element → Choose specific video → earlier episode (one click) → check the radio and preview → Save.
10. Visibility **Private** → Save. Read back the video ID.
11. Subtitles page: Add language TH/ES/PT/VI/ID; TH subtitles via Upload file; each language's Title & description via the pencil (textarea setter) → Publish.
12. Playlist: check it after Reuse details (it may already be added); otherwise Content → Playlists → New playlist (Private, order "Date published (oldest)").
13. Re-open the video's edit page and read back title, tags count, thumbnail, audience, altered content, **visibility**, playlist.
14. Word check: automatic captions vs script (below). Any mismatch with burned-in text → fix, re-render, re-upload.

## Project Context (Pudding, 2026-11-20)
- Channel `UCfAQFnZ6_mT9DYep-iDCzvw` (phone-verified, so custom thumbnails work). EP.1 `V8LRzmztGoA`; EP.2 final `nbh33IVMdr8`; playlist "Season 1: Pudding Goes to London (watch in order)" `PLMdtrC3tC660`.
- EP.2 took three uploads: v1 had two burned-in subtitle/audio mismatches (found by the ASR check), v2 had audio drifting late (found by the owner after 3:00). Both deleted by the owner.
- Translations used: TH, ES, PT ("Portuguese", as on EP.1), VI, ID. Translated intro + English phrase list and chapters.
- AI-note line (EP.1 description, last line): "Animation made with AI tools. Story, script and lessons written and directed by the Pudding team." EP.2's description lacks it; read a live description before assuming a template.
- **EP.3 (2026-11-21):** final `EmeIwYR8gww` (Private). Two uploads: the ASR check on the first (`RSR07iZwk2Y`) showed a line spoken twice under a once-only burned subtitle, although the owner had listened and said "once". Lessons measured this session:
  - **A clip whose speech timeline shows two bursts for a short line is probably the line said twice.** Don't settle it with one owner listen; cut to the first burst, or run the ASR check on a throwaway Private upload before the full Studio work.
  - Run the ASR check **right after Save, before** TH subtitles and translations: automatic captions were ready within a minute of "Checks complete", and a re-upload then costs only the Details/elements steps.
  - If the browser pane restarts between the owner's drag and your next call, the upload survives as a **Draft** row in Content: "Edit draft" reopens the same dialog (`udvid=<id>` in the URL). Check there before asking for a second drag. The pane can also come back signed out; the owner signs in.
  - On a re-upload, **Reuse details from the superseded upload** (it is the first tile) to carry title, description, tags and playlist; then replace only what changed (chapters). The end-screen picker then lists the superseded video first: pick the previous episode by its thumbnail/title, and check the radio text.
  - End-screen time fields take `m:ss:ff` (frames); type the start (e.g. `4:51:06`) and press Tab, per element. The template default starts 20 s before the end, which overlapped the last spoken clip.
  - Subtitles page row buttons only exist after hover: focus `ytgn-video-translation-cell-captions #cell-container` (or `…-cell-metadata`) and dispatch `mouseenter/mouseover`; then `#captions-more-options` → Download → `.srt`, `#captions-add`, `#metadata-add`. "Add language" → `tp-yt-paper-item` by exact name.
  - Translation dialog: 2 editable + read-only textareas; build each description as translated intro + the English original from "📌" onward (read from the read-only textarea).
  - Passing SRT text into the page: send a compact `end_ds|text` list (start only when a gap) and rebuild the SRT in page JS; a third of the size of the raw file.
  - Deleting a superseded upload (only with the owner's explicit OK naming the video): edit page → `#overflow-menu-button` → Delete → tick the checkbox → "Delete forever"; verify the URL id and the duration shown in the dialog first.
  - **Thumbnail readback must look at the picture.** On the re-upload the canvas thumbnail was set in the dialog while the video was still "Processing" and did not stick; the readback counted `img` elements and the auto-generated preview passed it. The owner noticed. Verify after a reload: the "Uploaded thumbnail" preview `img` has a `ytimg.com/.../mqdefault` src with `naturalWidth > 0` (an empty slot has the page URL as src and width 0), and take a screenshot. Fix on the edit page: `ytcp-video-thumbnail-editor #select-button` (first one = Upload file) with the patched file input, then `ytcp-button#save`.

## Reference Guide
| Step | Selector / control that worked |
| --- | --- |
| Title / description | `ytcp-uploads-dialog #textbox[contenteditable]` [0] / [1]: focus → `execCommand('selectAll')` → `execCommand('insertText', …)` |
| Tags | chip bar `#clear-button`, then `insertText("a, b, c,")` + Enter keydown |
| Audience / altered | `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`, `#toggle-button` (Show more), `[name="VIDEO_HAS_ALTERED_CONTENT_NO"]` |
| Subtitles (upload dialog) | `#subtitles-button` → "Upload file" (≈117,163) → Continue (≈497,379) |
| Visibility | `[name="PRIVATE"]` then `#done-button` |
| Translation dialog | the two editable `textarea`s; `HTMLTextAreaElement.prototype` value setter + `input`/`change` events; button "Publish" |
| Readback | `studio.youtube.com/video/<id>/edit`, `ytcp-video-metadata-visibility` text |

## Code Examples
File input without a picker (SRT or thumbnail):
```js
const orig=HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click=function(){ if(this.type==='file'&&window.__nextFile){ const dt=new DataTransfer(); dt.items.add(window.__nextFile); this.files=dt.files; window.__nextFile=null; this.dispatchEvent(new Event('change',{bubbles:true})); return;} return orig.call(this); };
window.__nextFile=new File([srtText],'ep.en.srt',{type:'application/x-subrip'});
```
Thumbnail canvas (fbcdn art sends CORS; Google Fonts css2 works in Studio):
```js
const f=new FontFace('Baloo2T','url(https://fonts.gstatic.com/s/baloo2/v23/…woff2)',{weight:'800'}); await f.load(); document.fonts.add(f);
const img=new Image(); img.crossOrigin='anonymous'; img.src=FBCDN_URL; await img.decode();
// draw art + text with the same coordinates as the local thumbnail.py, then:
window.__nextFile=new File([await new Promise(r=>c.toBlob(r,'image/jpeg',0.92))],'thumb.jpg',{type:'image/jpeg'});
document.querySelector('ytcp-thumbnail-uploader #select-button').click();
```
Word check (automatic captions): wrap `fetch`/`XHR` in the Subtitles page, then ⋮ → Download → .srt on "English (automatic captions)"; decode `content` (base64url) from the `download_caption_track` response:
```js
const j=JSON.parse(window.__capResp); const b=j.content.replace(/-/g,'+').replace(/_/g,'/');
const txt=new TextDecoder().decode(Uint8Array.from(atob(b+'='.repeat((4-b.length%4)%4)),c=>c.charCodeAt(0)));
```

## Constraints
**MUST DO**
- Upload Private. Ask the owner before audience, AI-disclosure, public visibility, downloads and deletions.
- Read back every setting on the edit page after saving, including visibility.
- Reload or close any other Studio tab that still shows the upload dialog for the same video.
- Treat the automatic-captions Download as a file download: Studio still saves the .srt even when you capture the response, so get the owner's OK first.

**MUST NOT DO**
- Click the pencil on "English (automatic captions)" when an uploaded English track exists: it offers "Overwrite track" for your captions. Cancel.
- Use the watch-page `timedtext` URL for the ASR check: without the player's PO token it returns an empty body.
- Delete an old upload yourself unless the owner says so in chat.

## Decision Frameworks
- Burned-in text or A/V sync wrong → re-render and upload as a new video; the owner deletes the old one. Captions-only issue → edit the SRT in place.
- Previous episode Private → it can still be an end-screen element, but viewers of a Public video won't see it. Tell the owner.
- Previous episode is in a playlist → "Reuse details" adds the new upload to that playlist too.

## Common Pitfalls
- **Leftover upload dialog published the video.** The owner's drag opens the dialog in the tab they used; the work was finished in another tab. Clicking through the stale dialog reached Visibility with **Public** preselected and made EP.2 Public. The owner kept it, but it should have been their choice.
- The end-screen chooser closes on the first click; a second click lands on "Most recent upload". Click once, then check the radio says "Video: <title>".
- After a page navigation, `window` helpers (patched click, SRT strings) are gone. Re-inject them.
- Two uploads with the same title and thumbnail look identical in pickers. Tell them apart by video ID (thumbnail URL `vi/<id>/`).

## Output Templates
```
Video: https://youtu.be/<id> (Private) · file <name>.mp4 (A/V 0 ms, −14.6 LUFS)
Set: title, description+chapters, N tags, not made for kids, altered: No, thumbnail, EN+TH subs,
     TH/ES/PT/VI/ID title+description, end screen → EP.n−1 + subscribe, playlist <id>
Readback: visibility Private ✓ · ASR word check: all lines match / mismatches: …
```
