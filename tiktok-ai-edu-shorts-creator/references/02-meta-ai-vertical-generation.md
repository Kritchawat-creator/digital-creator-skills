# 02 — Meta AI: 9:16 masters, clips and cover

Basics (one chat per project, name a still by its look, one speaker per clip, ask for Meta's alternative after a
refusal) are in `youtube-ai-edu-series-creator/references/02-meta-ai-generation.md`. This file adds what is
different for vertical shorts, measured on EP01 (2026-11-21).

## Driving the page (desktop app's built-in browser pane)
- Prompt box = contenteditable. `form_input` and the hidden textarea's value setter look filled but are ignored.
  Click the visible box, type with the computer tool (2,400-2,600 characters typed fine), press Return.
- Use the poll helpers in `scripts/meta_page.js` (≤38 s per call). First video poll usually returns nothing while
  Meta "composes"; clips arrived after 40-80 s, images after 14-22 s.
- Download with `curl -sSfL -o clips/C1_v1.mp4 "<url>"` immediately; convert stills with
  `sips -s format png X.webp --out X.png` (format change only).
- Work in a new tab when another tab (e.g. TikTok's upload page) holds unsaved work. Always pass your own `tabId`.
- Wait for composer hydration before typing: the attachment-button skeleton must be gone and the box a
  contenteditable (EP02 typed into the prehydration `<textarea>`; Send stayed disabled). If stuck, reload your own tab.
- A hidden pane still works (screenshot frame 800x600/712); take a screenshot first to get the frame size.
- A new image can stay an empty `<img>` (no src) until clicked. Click it → `__newimgs()` returns it → press
  **Escape**: the viewer has its OWN prompt box (EP04 typed a prompt there). Before typing, check
  `[contenteditable]` count is 1. Helper: `scripts/meta_page.js` block 3.

## Output measured
- Stills: "VERTICAL 9:16 portrait image (tall, not wide)" → 1152x2048 every time (4/4).
- Clips: "NEW 10-second VERTICAL 9:16 video (tall, not wide)" → 720x1280, 24 fps, 10.0 s, H.264 + AAC mono 24 kHz (6/6).
- No refusals in EP01 (adult cast, OTS framing, polite content). Still test the two-character clip first.

## Master prompt skeleton
```
Create an image. VERTICAL 9:16 portrait image (tall, not wide). Same cute 3D style and the exact same <A> and <B>
designs as the character sheets earlier in this chat: use the SECOND <A> turnaround sheet (adult proportions), not
the first <A> sheet and not the lineup; and the <B> turnaround sheet. <GLOBAL STYLE BLOCK>
Scene: <location, time of day, the premise detail (e.g. ceiling lamps clearly switched OFF)>; <props, all plain:
plain mug, plain laptop with no logo, shelves with plain boxes (no titles)>. No posters, no signs.
Over-the-shoulder shot from behind <B>: <B> SITS …; the back of his head and <colour> shoulder fill the lower-LEFT
foreground, softly out of focus, his face not visible. <A> sits … facing the camera, eyes looking screen-LEFT at <B>
just past the camera, NOT into the lens, a calm neutral closed-mouth expression.
<A BLOCK> <A> is a grown-up 24-year-old woman, adult proportions. <B BLOCK>
Only <A> and <B>, nobody else. <UNIVERSAL NEGATIVES>
```
Reverse master: "The REVERSE ANGLE of the vertical office image you just made (the one with …)": same set list, the
other character's back in the lower-RIGHT foreground, eyes screen-RIGHT. Solo master: "the same office and desk …
a moment later: NOW the lamps are ON … <A> ALONE … looking straight INTO the lens … Nobody else anywhere".
EP01 result: Meta kept the window on the right in both OTS masters (not a true reverse). It still reads as one room;
accepted.

## Clip prompt skeleton (order matters; the closing sentence must be last)
```
Animate the vertical OVER-<B>'S-SHOULDER office still image with the ceiling lamps OFF (<one-line look of the
master>) into a NEW 10-second VERTICAL 9:16 video (tall, not wide). ONE continuous static shot, no cuts, no zoom,
no camera move, no new text. The background stays EXACTLY the same as the still image for the whole video and the
ceiling lamps stay OFF. <GLOBAL STYLE BLOCK> <A BLOCK> <A> is a grown-up 24-year-old woman, adult proportions.
<B BLOCK> Starting within the first second, <A> looks screen-LEFT at <B> (not into the lens) and <manner> in a
CLEAR, FULL, NORMAL-VOLUME speaking voice, <voice description>, every word fully voiced (not a whisper, not
breathy): "<exact line>". She says exactly these words<, including the word "open" (it is her mistake on purpose,
keep it)>. ONLY <A> speaks. <B> does NOT speak: he stays seen from behind, his head does not turn toward the camera,
his jaw does not move. As soon as her last word is said, <A> closes her mouth and <end state: lips pressed
together, closed-lip expression, no grin, no teeth>. <UNIVERSAL NEGATIVES> The laptop lid is plain matte silver and stays completely blank for the whole
video: NO logo, no mark of any kind on it. Quiet office ambience only. Nobody laughs. No narration, no music, no laughing
```
- Don't name the brand shape you want to avoid ("no apple shape"): describe the plain object instead.
- "Starting within the first second" was ignored in 2 of 6 clips (speech began at 4.6 s and 1.7 s); trimming fixes it.
- Deliberate mistakes: add "(it is the common mistake on purpose, keep it exactly)". Kept in 7/7 lines EP02-EP04.

### Sentences that fixed measured clip faults (add them by default)
| Fault seen | Sentence that fixed it |
| --- | --- |
| Silent mouthing / big open smile in a pause after the name (EP04 C1_v1) | "says the whole line in ONE smooth flow (no pause after \"Leo\"), with a warm closed-mouth look between words (no big open smile, no teeth)" |
| Grin / open mouth at the out point | "As soon as her last word is said, <A> closes her mouth and …" (replaces "After her line …") |
| Long silent gap between two sentences (EP03 C4_v1 2.7 s) | Never ask for a pause; "in one smooth flow with only a tiny breath between them (no long pause)" |
| Speaker looks down at a prop with eyes closed for a whole sentence (EP04 C4_v2) | "KEEPS her eyes open on <B> for the whole line (she does not look down at the cup, does not close her eyes)" |
| Customers / staff walk into a public location (EP04 café) | "Nobody else appears anywhere: no customers, no staff, no passers-by." (far blurred people outside a window remain; allowed) |
| Prop handling in a static shot | "<A> does not drink and does not lift the cup." |
| Standing characters come back full-body, the shorter one child-sized (EP05 lobby) | "CLOSE over-the-shoulder … only the back of <B>'s head and shoulder, big, cropped by the frame edge" / "MEDIUM CLOSE-UP from the chest up, legs and feet NOT visible"; "head level, eyes at about her own eye level" |
| Letter list in one line repeated or padded ("A, A, B, or C", EP05) | "says each letter only ONCE" + "for the rest of the video stays silent with lips gently pressed together" |

### Character drift guard (EP04)
- In a **new location**, Meta re-renders faces from the blocks and may drift: EP04's café Mint came out rounder and
  younger than EP01/EP03 (the bible's "round face" pulls that way). Compare a face crop of each master with the
  canon episodes at the same scale (`03`, montage) **before** making clips.
- Fix: keep the bible block word for word and add after the age line: "Her face reads clearly as a grown-up
  woman's: a slim oval adult face with gently defined cheekbones and chin (not chubby baby cheeks), eyes big but not
  oversized, adult neck and shoulders; she looks like a 24-year-old office worker, never like a child or a
  teenager." Carry the same sentence into every clip and the cover of that episode.
- A re-prompt to fix a character often returns an **edit** of the previous image (EP04 office M1_v2 changed only
  the laptop). Start fix prompts with "Create a brand-new image from scratch (do not edit or reuse the previous image)."
- When several similar stills exist in the chat, name the one to animate: "Animate the LATEST vertical
  OVER-LEO'S-SHOULDER coffee-shop still image, the brand-new one with Mint in a cable-knit mint cardigan (…)".
- Meta's clips may frame **wider** than the master (EP04: whole café visible, characters smaller), consistently for
  every clip of that master. Accept it if all clips match; judge faces on a 1:1 crop of the clip too.
- Two-character pairs with a big age gap (EP03 Dao 38 + Mint 24): "Two adult coworkers in a short work meeting",
  "<learner> is a grown-up 24-year-old woman, adult proportions", "<mentor> looks 38, not older" — 0 refusals.

### Locations (one per episode)
Write the location block once in `M1.txt` (bright daytime, the series' look: soft light, plants, black dome lamps,
window behind on the right) and paste it into M2/M3, every clip and the cover. Public places need the no-text line:
"No menu boards, no chalkboards, no posters, no signs, no price tags, no writing anywhere, no shop signage visible
through the window" + plain cups/props. Crop the window, counter and props on each master to check for text.

## Cover prompt (Meta AI writes the text; owner rule: no local text)
```
Create an image. VERTICAL 9:16 portrait image (tall, not wide): a cute, eye-catching TikTok cover for this lesson.
<same cast/set references, lamps ON> <STYLE> In the lower half: <A> and <B> … <one visual metaphor, e.g. a big
glowing light bulb>, closed-mouth smiles. <BLOCKS> TEXT: in the upper-middle part of the image (between about 15%
and 45% of the height, centred, well inside the left and right edges), exactly two lines of big, bold, rounded,
playful 3D-style lettering with a white outline, spelled exactly: line 1 "<WRONG>" in red with a big red X mark;
line 2 "<RIGHT>" in green with a big green check mark. Spell every word exactly as written. No other text anywhere …
Keep the bottom quarter free of text. Nobody laughs. No laughing.
```
EP01: spelled exactly on the first try ("OPEN the light? ✗ / TURN ON the light ✓"), text at y 390-690 of 2048.
Always read every letter at full size before accepting. EP02-EP04: 4/4 covers spelled exactly on the first try.
For a series, copy the previous episode's `COVER.txt` and change only the words, the characters and the location;
if a character was fixed this episode, add the same face sentence and "Create a brand-new image from scratch".
