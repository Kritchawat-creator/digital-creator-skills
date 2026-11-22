# 04 — Cover, subtitles and caption

## Cover
- Generate in the project's Meta AI chat with the cover prompt in `02` (Meta writes the text; nothing is drawn locally).
- Save to `cover/cover_vN.webp` + `.png`; check it is 1152x2048 and read every letter at full size.
- TikTok shows the cover full-screen and as a **3:4 crop in the profile grid** (TikTok made 486x648 from it).
  Keep the text in the upper-middle band (EP01: y 390-690 of 2048) and the bottom quarter free.
- After the owner uploads it, measure the crop in the page with `scripts/tiktok_studio.js` block 4
  (EP01: red rows 44-98, green 112-164, x 28-456 of 486x648 → inside with margin).
- **Judge "did the cover land?" by the picture, not the file input.** EP04: the owner's Upload cover in the built-in
  pane worked although `input[type=file].files` stayed 0 and change/drop/paste hooks logged nothing; the dialog's
  "Preview in profile (4:3)" and the upload page's Cover thumbnail showed it, and block 5 found red + green text
  pixels in the top half of the 486x648 cover (frame 0 with a white overlay has neither). EP02's first try and EP03
  did NOT land — so always check, and decide before Schedule (scheduled posts can't be edited).
- Fallback if it doesn't land: Edit cover → frame 0 (the hook frame with the mistake overlay inside the 4:3 crop);
  the owner can set the real cover after the post is live (Studio → Content → pencil → Edit cover, once a day,
  within 7 days).

## Subtitles
- English SRT only (global audience), timed on the **delivered cut**, not the source clips:
  run `qc_audio.py` and whisper on `out/*.mp4`, set each cue ~0.15 s before its `#` run and ~0.2 s after.
- Write it with `scripts/make_srt.py` (asserts no overlap); check it parses:
  `ffmpeg -v error -i out/x.mp4 -i subtitles/x.srt -map 0 -map 1 -c copy -c:s mov_text -f null -`.
- It is a sidecar file. Don't burn it in (owner rule). TikTok web's editor has no SRT import that we found; the
  on-screen text overlays carry the key lines (see `05`), and full captions need TikTok's auto-captions in the app
  or one text layer per cue.

## Caption (format only; no strategy evidence yet)
- English, ≤ ~240 characters: the mistake as a question, the fix, the quiz, "Comment below", 3-5 topic hashtags,
  then ALWAYS `#fyp #creatorsearchinsight` at the end (owner rule, 2026-11-21: every description/caption).
- EP01: `Do you "open" the light? 💡 Say "turn ON the light" and "turn OFF the light"! Quick quiz: open the TV or
  turn on the TV? Comment below 👇 #learnenglish #englishtips #englishlesson #esl #TalkoroEnglish` (201 chars).
- Emoji are fine in the caption (they render); they do NOT render in TikTok editor text layers.
- Talkoro pattern (series spec §8): `<question hook> <emoji> <one-line rule> Quiz: <quiz>? Comment below 👇
  #learnenglish #englishtips #<topic tag> #esl #TalkoroEnglish #fyp #creatorsearchinsight`. EP04 (273 chars):
  `Do you say "I very like it"? ☕ Use "really" before the verb or "very much" after it: I really like it / I like it
  very much! Quiz: I very like it or I really like it? Comment below 👇 #learnenglish #englishtips #englishgrammar #esl
  #TalkoroEnglish #fyp #creatorsearchinsight`. Read the hashtags back in Studio before Schedule (EP02 went out
  without `#fyp #creatorsearchinsight`).
