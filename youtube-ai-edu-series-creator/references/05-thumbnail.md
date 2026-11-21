# 05 — Thumbnail

One template look for the series: the hero's face with a big emotion, two or three words, and an episode badge
in the same corner every time. The art comes from the AI tool; the words are drawn locally.

## 1. Art

Generate a dedicated image in the project's Meta AI thread. Don't use a video frame: frames gave half-cut signs,
an ear cut by the text panel and far more layout tuning (EP.1's first attempt).

Prompt points:
- "HORIZONTAL 16:9", same flat cartoon style, exact character designs with their fixed details.
- "**NO text, NO letters**" — AI images misspell words.
- "characters fully visible inside the **left 55%**; the **right 45%** is clean empty background for text later".
- The episode's banned items by name (EP.3: no money of any kind).
- One clear emotion and one prop that tells the topic (EP.3: waving, sparkly eyes, the suitcase).

Save the art to `thumb/meta_cover.webp` / `.png` and keep its URL in `thumb/meta_cover_url.txt`: the Studio
step redraws the thumbnail from that URL (section 4). The URL is signed and expires, so read it again from the
page if the upload happens on a later day.

## 2. Text layout (local, 1280×720)

`scripts/thumbnail_example_ep3.py` is the working layout. Steps:

1. Resize the art to 1280×720 and **measure where the characters end** (EP.1: x≈680; EP.3: x≈740). Text lives to
   the right of that, with a margin: `FREE = (760, 1268)`, centre `CX = 1012`.
2. Two title words as outlined "sticker" text: Baloo 2 weight 800 at 112–116 px, navy outline 11 px, soft drop
   shadow. Line 1 yellow, line 2 white (EP.1 "AIRPORT / ENGLISH", EP.3 "CHANGE / MONEY!").
3. A pink pill with the benefit ("5 Phrases You Need!", "Where? How much?"): Baloo 2 at 42 px, white with a navy
   4 px outline. **Size the pill from the text's real ink box** (`textbbox` with the stroke width) plus 48 px of
   side padding; height 84 px.
4. Episode badge: a navy circle with a yellow ring, top-right (`[1118, 26, 1254, 162]`), "EP.N" at 50 px. The
   bottom-right corner stays empty because YouTube draws the duration there.
5. Save `out/<episode>_thumbnail.jpg` (quality 92) and QC copies at 320 and 168 px wide.

Asserts in the script (they fail the run, so an overflow can't ship):
```python
assert b[0] >= FREE[0] and b[2] <= FREE[1]                       # each title word inside the free area
assert pill[0] + PILL_PAD_X - 1 <= ink[0] and ink[2] <= pill[2] - PILL_PAD_X + 1   # text inside the pill with padding
assert pill[1] < ink[1] and ink[3] < pill[3]
assert pill[0] >= FREE[0] and pill[2] <= FREE[1]                 # pill inside the free area
```
The owner caught pill text overflowing its pink background on EP.1. That is why the pill is sized from the ink
box and asserted.

## 3. QC

Look at the image at three sizes: 1280×720 (full), 320×180 (suggested video) and 168×94 (mobile list).

- Title words readable at 168 px.
- No text touches or covers a character (ears, trunk, props).
- Pill text has visible padding on both sides.
- Nothing in the bottom-right timestamp area.
- No sign, word or object in the art is cut by the frame edge.
- No real brand, emblem, flag or banned item in the art.
- Same badge position and palette as the earlier episodes.

## 4. Setting it in Studio without a file picker

The browser tool can't pick a local file, and Studio's CSP blocks `http://127.0.0.1` fetches and images. What
works: redraw the same layout on a canvas **inside the Studio page**.

- The art loads from its fbcdn URL with `crossOrigin='anonymous'` (fbcdn sends CORS headers, so the canvas isn't
  tainted).
- The font loads with `FontFace` from the `fonts.gstatic.com` URL found in the Google Fonts css2 response. Ask
  css2 for the exact characters (include the space) so the right subset comes back.
- Draw with the same coordinates as the local script, `toBlob('image/jpeg', 0.92)`, put the `File` in
  `window.__nextFile`, and click the uploader's select button (`scripts/studio_inject.js` patches the file
  input). Code in `07`.

Requirements and traps:
- Custom thumbnails need a **phone-verified channel**. Studio shows "Unlock more on YouTube" until the owner
  verifies at youtube.com/verify.
- **Set the thumbnail after processing has finished, on the edit page.** On EP.3 it was set in the upload dialog
  while the video was still processing and didn't stick.
- **Read it back by looking at the picture** after a reload (`07`, readback). Counting `img` elements passed an
  auto-generated preview.
