# 05 — TikTok Studio (web): fill in, cover, schedule

Page: `tiktok.com/tiktokstudio/upload`, in the desktop app's built-in browser pane, signed in by the owner.
Helpers: `scripts/tiktok_studio.js`. Measured on EP01-EP04, 2026-11-21.

## Hard rules
- The **owner** uploads the video (drags the MP4 onto the upload area in your pane tab): the pane has no file
  upload tool. MP4 drag-drop works in the pane; cover upload works only sometimes (see Cover).
- **Post** and **Schedule** both publish: only for a slot the owner approved in chat (Talkoro batch: "Schedule
  20:00 / 08:00 / 17:00" approved 2026-11-21). Never Post now without a yes. Never press Discard.
- There is **no "Save draft" button on web** (only Post / Schedule / Discard). The upload page holds everything in
  memory: don't reload, navigate away or close the tab; do other browser work in a new tab.
- **Scheduled posts cannot be edited** (no caption or cover change). Get caption, overlays, AI label and cover right
  BEFORE Schedule. A live post's caption/cover can be edited (Studio → Content → pencil), once a day, within 7 days.
- Leave the editor only with **Save** (Cancel drops the text layers).
- The upload page may show "A video you were editing wasn't saved. Continue editing?" left over from another post.
  Check Studio → Content in a separate tab; if the earlier posts are listed, ignore the banner (don't press Discard).

## Order of work
1. Read back what the owner uploaded: file name, "Uploaded (12.3MB)", 1080P.
2. **Description:** block 1 selects the box → Backspace → read back. EP02/EP04: one Backspace removed only ONE
   character; then put the caret at the end (block 1b) and press Backspace ×(length+5), read back `"\n"`, type the
   caption with the computer tool (emoji type fine), read back again (block 2). `cmd+a` never selects in the pane.
3. **Switches:** turn **AI-generated content** on by a JS-located element (block 2b), never by coordinate — its
   "Learn more" link navigates the tab away and the description is lost (EP02). Expect checks "No issues found".
4. **Edit → Text** (on-screen text from the script). Set the viewport first: `resize_window 1400x900` (it resets when
   the pane is resized or the turn ends → screenshot again before coordinate clicks). Screenshots come back at
   800x514; the timeline is ≈ 25.7 screenshot-px per second, 0 s at x≈80.
   - **Blank preview** (EP04: `.StageCanvas__screen` 0x0): top-centre zoom menu "100%" → **Zoom to fit**.
   - "Add text" adds a 5 s layer at the playhead (click the ruler first). Preset tiles add layers too — don't click.
   - Content box = textarea: `window.__selTA()` then type. Newlines in the typed text make multi-line layers.
   - Font: `await window.__pickFont('DynaPuff')` opens the dropdown with a pointer/mouse event sequence (the computer
     click is ignored) and returns the item's CSS rect; click it at (x/1.75, y/1.75) in the 800-px screenshot frame,
     or screenshot the open list first (order changes as fonts are used).
   - Size: `triple_click` the size box, type, Return. No JS `focus()` there (it reverted the font, EP02 re-post).
   - Style: Fill swatch grid (green = middle row, 4th), Stroke "+" (black by default), Shadow "+". **The first
     Stroke/Shadow "+" click is swallowed on about half the layers**: zoom the Style panel after each, re-click any
     row that still shows "+". Escape closes a picker.
   - Move: drag the text box in the preview to the top third. Trim/extend: drag a layer's right edge; keep the last
     layer inside the video (a layer past the end lengthens the project, EP02).
   - **Save** (top right) → back on the upload page; read back the description (it survives).
   - Verify: the upload page's phone preview (a `<canvas>`, no `<video>`) shows the layer at the playhead; play it
     and zoom at each overlay time, or check each layer in the editor before Save (text, font, size, Style rows).
5. **Cover:** Edit cover → ask the owner once to click **Upload cover** and pick `cover/cover_vN.png`, then verify by
   the profile preview + block 5 pixels (`04`). Not landed → frame 0 (hook frame) → Save.
6. **Schedule:** "Schedule" radio → date field → click the day → time field: click minute **00** first, then the hour
   (click visible items; a scroll tick moves one step. EP05: the picker opened over the Location row and item clicks fell
   through and set a location — scrolling the columns is the reliable way; read the Location input and clear it before Schedule) → read the inputs (block 6: "17:00", "2026-11-22", browser TZ
   `Asia/Bangkok`) → scroll the **Schedule** button into view and click it. The first scheduled post showed a consent
   popup ("Allow your video to be saved for scheduled posting?"); later ones didn't. The page redirects to
   Studio → Content; reload it and read the row back ("Nov 22, 5:00 PM (GMT+7) Bangkok").

## Talkoro overlays (series spec §7; EP04 worked example)
| Time | Text | Style |
| --- | --- | --- |
| 0-2.4 s | "I very like it" NO! | DynaPuff 24, white fill, black stroke |
| 5.0-15.0 s | "I really like it" YES! | DynaPuff 20, green fill, black stroke + shadow |
| 9.3-15.0 s | "I like it very much" YES! (under it) | DynaPuff 20, green fill, black stroke + shadow |
| 15.1-22.2 s | "I very like it" or / "I really like it"? / Comment below! | DynaPuff 20, white fill, black stroke |
No ❌ ✓ ✗ in layers (TikTok fonts don't render them): words + colour.
