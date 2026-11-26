# 02 — Meta AI generation (masters, clips, downloads)

Measured on meta.ai web chat in November 2026. Tools change: confirm the first image and the first clip of an
episode before relying on any number here.

## 1. What the tool gives you

| Item | Measured |
| --- | --- |
| Clip | 10 s, 1280×720 (16:9) or 720×1280 (9:16), 24 fps, H.264, AAC mono 24 kHz with native speech and ambience |
| 16:9 | Works when the prompt says "HORIZONTAL 16:9 landscape video (wide, not vertical)" |
| Generation time | 15–70 s per clip across the three episodes |
| Images | Sometimes 3:2 (1920×1280) instead of 16:9. Fine as a master: the animation reframes to 1280×720. Check the first clip's framing (feet were cropped once) |
| Thread | The chat keeps all media; later prompts can refer to earlier images. Keep **one thread per project** |
| Upload | The desktop app's browser pane has no file-upload tool, so masters are generated inside Meta AI, not uploaded |
| Docs | Clips are max 10 s with an Extend option. **Lip sync → Text** and **Voice** take a typed script and a chosen voice: the fallback when native audio gets the words wrong |

Yield per episode: 34 clips for 20 accepted cuts (EP.1), 43 for 22 (EP.2, about 2:1), 26 for 21 (EP.3, about
1.2:1). EP.3 was better because most clips had a single character, so there was no listener to fail.

## 2. Order of work

1. **Character sheets** once per series: "Create an image. Character reference sheet …". Later prompts say
   "exact design from the X sheet".
2. **One scene master per location** (image):
   - HORIZONTAL 16:9, flat cartoon style, fixed left/right positions and screen direction.
   - **Detailed background from the start** (windows, belt, trolleys, a blank screen, a clock). A plain
     background made every clip invent a different hall (EP.2 belt: 6 different backgrounds).
   - "NO text, NO letters, NO numbers", blank screens, plus the episode's banned items by name.
   - **No title text and no label in quotes.** A label like "PHRASE CORNER" appeared in the scene as a sign.
   - Restate every character's fixed details.
3. **A solo master** for any character who hosts the lesson or speaks to the hero: "the same counter … but with
   ONLY Biscuit, nobody else anywhere". Asking a video prompt for "another Biscuit-alone version" kept starting
   from the two-shot still (2 fails; Meta said so itself).
4. **Clips**, one line each, animated from the master (skeleton below).
5. **Download** each clip when it appears, then QC it (`03`) before generating variations.
6. **Cover art** for the thumbnail in the same thread (`05`).

Accept or reject each master in `qc_log.txt` and save both the candidates and the accepted file in `masters/`.
EP.2 needed three desk candidates (grey beak, small eyes, wrong cap) before one was on-model; EP.3's three new
masters were each accepted first try with the fuller prompts.

## 3. Prompts

**Master (image)** — as used for the EP.3 counter, shortened:
```
Create an image. HORIZONTAL 16:9 landscape image (wide, not vertical). Same flat 2D cartoon style as the earlier
<series> images in this chat. <Location with five or six concrete background objects>, one big BLANK <colour>
screen. LEFT side: <character A, exact design: every fixed detail>. RIGHT side: <character B, every fixed
detail, props>. <Episode's banned items by name: "NO money anywhere: no banknotes, no coins, no paper money,
no cash, no wallets, no currency symbols, no exchange-rate board, no flags">. NO text, NO letters, NO numbers.
Original characters.
```

**Clip (video)** — single speaker:
```
Animate the same <location> still image again (<the master described by how it looks: character A with <detail>
on the LEFT; character B with <detail> on the RIGHT; <two background objects>>) into a NEW 10-second HORIZONTAL
16:9 video. ONE continuous static shot, no cuts, no zoom, no new text or signs, same flat cartoon style for the
whole video. <Speaker> <small action> and, starting within the first second, says <manner> in a CLEAR, FULL,
NORMAL-VOLUME speaking voice: "<exact line>". ONLY <Speaker> speaks. <Listener> does NOT speak: <mouth> closed
the entire video, <silent action>. <Banned items again>. No narration, no music, <quiet ambience>. Nobody
laughs. No laughing.
```

**Listener and continuity clauses added in EP.5** (each fixed a measured failure):
- "<Listener>'s mouth stays shut the whole time; he only listens." — fixed a teen talking along with a short question.
- "<Teen>'s hair and face are DRY: NO water drops on his face or hair (only his closed umbrella is wet)." — a wet
  umbrella in the master made Meta add drips running down his face.
- Don't open a two-shot line with an exclamation ("Oh no! …"): the listener's mouth moved on it in 2/2 takes.
- An adult-alone master for a place that already exists (EP.8): attach **both** the place master and the character sheet in
  one prompt ("Here are two images: the canal image (for the place, the evening light and the style) and the Walter sheet
  (for EXACTLY how Walter looks)"). Place only → the design drifted (no trousers, wrong side); sheet only → a different,
  daytime place.
- Lily drew eyebrows in a new place (EP.8 park) although her master had none: keep "NO eyelashes and NO eyebrows … nothing
  drawn above her eyes" in every prompt for a character whose sheet has plain dot eyes.
- An edit of the image Meta just made ("Change ONLY Pudding's skin colour …, keep everything else exactly the same")
  fixed an off-model colour without changing the layout.

- New adult character (EP.9 Rosa): animate from a **waist-up** master (a small face in a wide master is redrawn), say "eyes are SOLID
  BLACK round dots with one tiny white highlight … NO white eyeball, NO iris, NO eyelid lines. <She> keeps her head in the same
  position and only her mouth moves", no nod or tilt. If Meta adds the same small detail (brow, whiskers) in every speaking clip, put it
  into the masters with an edit prompt ("change ONLY … keep everything else") and into the bible instead of fighting it.
- EP.11: a female adult kept getting lash flicks or a pointed eye corner with "NO eyelashes" in the prompt. What worked (5 of 5): no name, no she/her,
  no eyelash word ("The capybara in the attached image … The eye is a plain black button: one perfectly round solid black ball … nothing attached
  to it"), "a calm, friendly face" instead of "smiles", and the voice described on its own ("a warm adult woman's voice").
- EP.11: say what must NOT change in a decorated background ("ONLY the pale-yellow planet has a ring", "the colours stay the same soft pale pastel
  colours as in the attached image"); Meta copies a striking detail (the ring) to the object next to it.
- "I couldn't attach the image. Want me to make it again?" is a delivery fault, not a refusal: answer "Yes, please make it again: the image exactly as
  described in my last message." (no attachment). Sending the full prompt again failed 6 times, the answer worked first try.
- Editing prompts that worked: "remove the swan inside the bandstand", "remove Lily completely, keep Rosa exactly as she is now".
- Attach check: `input.files` resets after `change` ("attach … 0"); count the composer's `blob:` previews instead (1 or 2).

- EP.12 (warm evening light): name every object whose colour must stay ("the apples on the tree stay GREEN", "the insides of his ears stay the same pale PINK", eye
  "PURE BLACK, NOT brown"). Adult voices: "bright, friendly, lively, not deep". Group shot: all mouths closed in the master + a listener block for the whole group.
- EP.13 (return to an old place): do NOT attach the old episode's master together with the new character reference: Meta keeps the old drawing style (lavender skin, two
  brows, 2 images lost). Attach only the newest character master and describe the old place in words; it came out on-model first try.
- EP.13: never leave something in the scene description that is not in the attached master (trolleys grew into the picture); say "behind the windows ONLY plain pale sky",
  "the hall is completely EMPTY: NO travellers", "pale GREY pots". Remove plants behind heads in the master (read as leaves on the head; a leaf badge grew on the backpack).
- EP.13: a friend in every hero shot: over-the-shoulder works for a human friend (back of head at the edge); for an animal friend the back view reads as looking away or is drawn
  realistic. Use the friend in side view, mouth closed, listening (only the hero speaks) or the friends frame.
- EP.13: an edited-away far eye grows back in the animation; keep the still as the model draws it and describe both eyes. "His open mouth is always a small plain soft-RED shape …
  never a white line" removes tooth flashes; "both front legs hang straight down, never points" stops gestures; pigeon host in a scene: "both eyes blink together, NO wink, wings behind the desk".
- EP.13: a SLOW line must be asked word by word ("How... was... your... holiday..."), otherwise it is as fast as the FAST line. Check words per second of both.

**Two-take host line:** "says it TWICE: slowly, then a one-second pause, then at natural speed". Measured gaps
between takes were 2.8–4.5 s and take 2 started anywhere from 5.9 to 7.0 s. Never assume where take 2 is; read
it from the timeline (`03`).

Phrases that fixed specific failures:

| Problem seen | Wording that fixed it |
| --- | --- |
| Two speakers in one clip → the wrong mouth moved | Split into single-speaker clips |
| Listener ad-libs after the line | Trim in the edit (find the end with the speech timeline) |
| Eyelashes, hair tufts, grey beak, badge on a cap | Restate the design in every prompt: "dot eyes, NO eyelashes", "ORANGE beak", "plain navy cap with no badge". A detail left out drifts |
| Backgrounds or desks differ per clip | Scene master + "Animate the same … still image again" |
| Real names on a screen or sign ("UK BORDER FORCE", a real airport name), a badge on a cap | Word-level negatives: "Do NOT show the words X, Y; screens blank; no flags, logos, emblems" |
| A realistic shot inside a cartoon clip | "same flat cartoon style for the whole video, no realistic shots"; trim |
| Clip started from an older, rejected image | Name the master by its look: "the THIRD desk image, Biscuit with big shiny eyes and the ORANGE beak (not the first or second)" |
| Listener told to look "surprised" held an open "o" mouth | "mouth fully closed, only his eyes blink"; never give the listener a surprised face |
| Listener grins with teeth | "lips pressed together, a calm closed-lip smile, NO grin, NO teeth" |
| Listener opens a small "o" while looking at something | "stays calm and still, a calm neutral face, lips pressed together in a thin straight line, he does not react" |
| A teen's line came out as breath or sighs | "talks in a CLEAR, FULL, NORMAL-VOLUME speaking voice, every word fully voiced (not a whisper, not breathy, not a sigh)" |
| Character morphs mid-clip (front view, goggle eyes, emblem) | Regenerate; restate the full design and "stays in side view" |
| Laugh or chuckle after the line | "Nobody laughs. No laughing" in every prompt, and cut after the last word |
| Background swaps mid-clip on a reused master | "The background stays EXACTLY the same as the still image for the whole video: same quiet hall, no new people, no new screens" |
| "Another X-alone video" kept the second character in frame | Make a still solo master and animate it by name |

Meta sometimes edits inside "ONE continuous static shot": a character walked out of frame before the other spoke
(usable after he left), a cut to a close-up between two takes (used as the second take), a hall swap mid-clip
(fail). Check the contact sheet for cuts.

## 4. Refusals

**Rule: never reword or retry to get the refused content.** Log the refusal with Meta's reason, ask what it can
make, accept that, and restructure the scene. After a refusal with no offer, this got a concrete alternative
both times:

> Understood, I won't push on that. For <line>, what version would you be able to make instead?

| Episode | Prompt | Meta's reason | What was used |
| --- | --- | --- | --- |
| EP.1 | A 16-year-old character addressing the camera as teacher | policy: a 16-year-old character can't address the camera as teacher | The adult animal character became the lesson host; teens stay in-story |
| EP.2 | Officer says a line "VERY FAST in one quick breath" | declined | Meta's offer: natural speed (still about 5 words/s, tagged FAST) |
| EP.2 | Officer tells the hero "OK. Please wait here." | leaving a little one alone in public | The line was dropped |
| EP.2 | The hero "sad and droopy" because his bag is missing | baby character in an upset, vulnerable moment | Meta's offer: he asks calmly and bravely |
| EP.2 | The host teaches while the hero stands silent and nods | one-sided adult-to-baby instruction | Meta's offer: the host teaches to camera on his own → solo host master |
| EP.3 | The adult greets the hero in the two-shot, hero silent | "a direct, close speaking exchange" with a baby character | Meta's offer: the adult alone at the same counter → all his lines as reverse shots |
| EP.3 | The hero says goodbye while the adult waves back | "a close waving goodbye exchange" | Meta's offer: the adult alone says the same words → answer voice on a lesson card; the hero's goodbye was dropped |

Allowed in the same EP.3 session: the hero speaking while the adult stays silent (4 clips), a teen speaking to
the hero, the hero and a teen at a taxi queue. The line is enforced inconsistently, so test the first clip of
each two-character scene.

Accepting the alternative also helped quality: adult-alone shots have no listener's mouth to fail.

## 5. Driving the page

The browser tool's JavaScript call times out at 45 s, so poll in steps of at most 38 s. The helper is in
`scripts/meta_poll.js`:
```js
window.__last=()=>[...document.querySelectorAll('video')].filter(v=>v.currentSrc&&v.videoWidth).map(v=>v.currentSrc).pop()||'';
window.__poll=async()=>{let t=0; while(window.__last().includes(window.__prevClip)&&t<36){
  if(/can't make|can’t make|not able to/.test(document.body.innerText.slice(-400))) break;
  await new Promise(r=>setTimeout(r,2000)); t+=2;}
  const u=window.__last(), changed=!u.includes(window.__prevClip);
  if(changed) window.__prevClip=u.split('/').pop().split('_n.mp4')[0];
  return {t, changed, url:changed?u:'', tail:document.body.innerText.slice(-300)}};
```
- Set `window.__prevClip` to the id of the newest clip before sending a prompt.
- `tail` shows refusals ("I can't make this one…"). Read it before assuming the clip is still generating.
- Don't use the count of `video` elements as progress: the chat virtualises old media, so the count can stay the
  same. Compare the returned URL with the previous one.
- The newest image is not always the last `img` in the DOM. List the last few `t39.105495` `.webp` images with
  their sizes and keep a list of ids already seen.
- If the owner used the same tab, scroll and focus may have moved. Click the prompt box before typing.

Download (signed fbcdn URL, works without cookies for a while):
```sh
sh dl.sh C02 "<url>"                    # -> clips/C02.mp4, prints duration and streams
sh dlimg.sh masters/counter_v1 "<url>"  # -> .webp and .png, prints the size
```

## 6. Voices

- Native audio usually says the exact line. Check new voices with the owner before generating the rest: one
  listen per new character.
- A character's voice can come out as breath only (a teen boy in EP.2, three clips). The voicing line catches
  it (`03`).
- If words keep coming out wrong, use **Lip sync → Text** with a fixed voice.
- Don't use Meta's built-in music or song lip sync for YouTube uploads (Content ID risk).
