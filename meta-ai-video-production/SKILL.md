---
name: meta-ai-video-production
description: Produce consistent, lip-sync-clean cartoon story clips with Meta AI (meta.ai web) for YouTube episodes. Use when generating character sheets, scene masters, or 10-second talking clips in Meta AI, when characters or backgrounds drift between clips, when two characters' mouths move at once, or when downloading Meta AI clips for editing. Triggers: "Meta AI video", "meta.ai clip", "character consistency", "lip sync overlap", "animate image", "vibes", "16:9 Meta AI", "scene master".
---

# Meta AI Video Production

## When to Use
- Making a series of short AI-animated clips (story scenes, lesson host clips) in Meta AI's web chat.
- Keeping the same characters, scene layout and art style across many clips.
- Getting exact scripted dialogue with native Meta AI audio.

## When NOT to Use
- Realistic people or real public figures. Use a different workflow and consent process.
- Music videos with licensed songs. Meta's "Music" and song lip-sync create Content ID risk on YouTube.
- Anything needing clips longer than 10 s in one take. Plan cuts instead.

## Core Workflow
1. **Character sheets first** (image, "Create an image. Character reference sheet …"), one thread for the whole project, so later prompts can say "exact design from the X sheet".
2. **One scene master per location** (image, HORIZONTAL 16:9, *no title text*, fixed left/right positions and screen direction).
   - Don't call it by a label in quotes. A label like "PHRASE CORNER" leaked into the background as a sign. Use descriptions instead: "the no-title image of Biscuit at the brown desk on the left, Pudding on the right".
3. **Every clip of that location = "Animate the same <scene> still image again … into a NEW 10-second HORIZONTAL 16:9 video. ONE continuous static shot, no cuts, no zoom, no new text."** Referencing the still by description in the same thread reproduced the first frame reliably.
4. **One speaker per clip.** Name the speaker ("ONLY X speaks") and state every other character's mouth state for the entire clip ("Y does NOT speak: closed-mouth smile the entire video").
5. Ask the line to start "within the first second" to cut dead air. Meta often adds 2–4 s of silence or an ad-lib after the line, so trim in the edit.
6. Download each clip (see Code Examples), then run lip-sync QC (skill `ai-video-lipsync-qc`) before accepting it.

## Project Context (Pudding EP1, measured 2026-11-20)
- Output: 10 s, 1280×720 (16:9) or 720×1280 (9:16), 24 fps, H.264, AAC mono 24 kHz with native speech/ambience.
- 16:9 works when the prompt says "HORIZONTAL 16:9 landscape video (wide, not vertical)".
- Generation takes ≈ 40–70 s per clip. The chat keeps all media; later prompts can reference earlier images.
- The in-app (Claude desktop) browser has no file-upload tool, so scene masters were generated inside Meta AI, not uploaded.
- Official docs: clips are max 10 s with an Extend option; **Lip sync → Text** and **Voice** take a typed script and a chosen voice (an alternative route to exact lines). Muse Video (native audio) announced Jul 2026, "coming soon".

## Reference Guide
| Problem seen | Fix that worked |
| --- | --- |
| Two speakers in one 10 s clip → wrong character's mouth moved | Split into single-speaker clips |
| Listener ad-libs after the line | Trim to the scripted segment (find it with the audio timeline) |
| Character drift (eyelashes, hair tufts) | Repeat the design ("dot eyes, NO eyelashes, no hair tufts") and animate from a master still |
| Backgrounds/desks differ per clip | Scene master + "Animate the same … still image again" |
| Real names appeared (agency name on a screen, real airport sign, badge on a cap) | Explicit negatives: "Do NOT show the words X, Y; screens blank; no flags, logos, emblems" |
| Realistic plane shot inside a cartoon clip | "same flat cartoon style for the whole video, no realistic shots"; trim |
| Meta refused: 16-year-old character addressing the camera as teacher | Don't work around it. Make an adult/animal character the on-camera host; teens stay in-story only |
| Plain-background master → each clip swapped in a *different* detailed hall (EP2 belt) | Make the master detailed from the start (windows, belt, trolleys, blank screen); then clips keep it |
| Clip started from an older image in the thread (grey-beak Biscuit from a rejected master) | Name the master by how it looks: "the THIRD desk image, Biscuit with big shiny eyes and the ORANGE beak (not the first or second)" |
| Listener told to look "surprised" opened an "o" mouth during the other's line | Ask for "mouth fully closed, only his eyes blink"; never give the listener a surprised face |
| Teen boy's line came out as breath/sighs (owner heard no words) | "talks in a CLEAR, FULL, NORMAL-VOLUME speaking voice, every word fully voiced (not a whisper, not breathy, not a sigh)" |
| Listener grins with an open mouth (teeth) | "lips pressed together, a calm closed-lip smile, NO grin, NO teeth" |
| Character morphs mid-clip (front view, goggle eyes, emblem on cap) | Regenerate; restate the full design and "stays in side view" |
| Image came back 3:2 (1920×1280) instead of 16:9 | Fine as a master: animation reframes to 1280×720, but check the first clip's framing (feet were cropped) |
| Laugh or chuckle after the line | Owner rule: cut right after the last word; add "Nobody laughs. No laughing" to every prompt |
| Biscuit speaking to Pudding refused (EP3) | Ask Meta what it can make; accepted Biscuit-alone → still solo master → cropped reverse shot in the edit |
| "Another Biscuit-alone video" kept Pudding in frame | Make a still solo master and animate it by name ("the Biscuit-ALONE counter still image") |
| Background swaps mid-clip on a reused master (A2) | "The background stays EXACTLY the same as the still image for the whole video: same quiet hall, no new people, no new screens" |
| Listener teen opens an "o" mouth looking at something (T01b) | "Ollie stays calm and still, a calm neutral face, lips pressed together in a thin straight line, he does not react" |

### Refusals seen (EP2, 2026-11-20): accept Meta's own offered alternative, never reword to get around it
| Prompt | Meta's reason | What we used |
| --- | --- | --- |
| Officer says a line "VERY FAST in one quick breath" | declined | Meta's offer: natural speed (still ~5 words/s, tagged FAST) |
| Officer tells Pudding "OK. Please wait here." | leaving a little one alone in public | dropped the line |
| Pudding "sad and droopy" because his bag is missing | baby character in an upset, vulnerable moment | Meta's offer: Pudding asks calmly and bravely |
| Biscuit teaches the phrase while Pudding stands silent and nods | one-sided adult-to-baby instruction | Meta's offer: Biscuit teaches to camera **on his own** → a solo host master (same desk, no Pudding) for all lesson clips. This also removes the listener-mouth problem |

### Refusals seen (EP3, 2026-11-20)
| Prompt | Meta's reason | What we used |
| --- | --- | --- |
| Biscuit: "You again! Hello, Pudding!" in the two-shot, Pudding silent | "a direct, close speaking exchange" with a baby character | Meta's offer: Biscuit-alone at the same counter → all Biscuit lines as reverse shots |
| Pudding: "Thank you! You too!" while Biscuit waves back | "a close waving goodbye exchange" | Meta's offer: Biscuit-alone phrase demo of the same words → used as the answer voice on a lesson card; Pudding's goodbye dropped from the story |

## Project Context (Pudding EP2, measured 2026-11-20)
- 3 masters (desk, belt, solo host) from 6 master images; 43 clips downloaded for 22 accepted cuts (about 2:1).
- Failures: off-model/drift 7 (eyelashes, grey beak, morphs), listener mouth 4, no audible voice 3, scene inconsistency 6 (plain belt master), refusals 4; laughs/ad-libs trimmed in most clips.
- Generation ~25–40 s per clip. The in-app browser JS tool times out at 45 s, so poll in ≤38 s steps:
```js
const prev='<id of the previous clip>'; const last=()=>[...document.querySelectorAll('video')].filter(v=>v.currentSrc&&v.videoWidth).map(v=>v.currentSrc).pop()||'';
let t=0; while(last().includes(prev) && t<38){await new Promise(r=>setTimeout(r,2000)); t+=2;} ({t, url:last(), tail:document.body.innerText.slice(-200)})
```
- `tail` shows refusals ("I can't make this one…"); read it before assuming the clip is still generating.
- The newest image is not always the last `img` in the DOM: list the last few `t39.105495` images with their sizes.
- Owner rules added in EP2: no laughing at the end of a scene; keep scene and characters consistent across every clip of a location (check with a cross-clip montage, skill `ai-video-lipsync-qc`).

## Project Context (Pudding EP3, measured 2026-11-20)
- 3 new masters, each accepted first try (counter two-shot, Biscuit-alone counter, taxi rank) + EP.2's belt master reused. 26 clips generated, 2 refused, 21 accepted cuts (about 1.2:1, better than EP.2's 2:1 because single-character shots have no listener to fail).
- **New refusal pattern: an adult character speaking to Pudding in the same frame.** Refused: Biscuit says "You again! Hello, Pudding!" in the two-shot (*"centers on Pudding as a baby character in a direct, close speaking exchange"*), and Pudding waving goodbye to Biscuit. Allowed in the same session: Pudding speaking while Biscuit stays silent (4 clips), Ollie (teen) speaking to Pudding at the belt, Pudding + Ollie at a taxi queue. EP.2's desk clips with Biscuit speaking to Pudding had passed, so the line moved or is enforced inconsistently: test the first clip of every two-character scene.
- **Ask for the alternative explicitly.** After a refusal with no offer, "Understood, I won't push on that. For <line>, what version would you be able to make instead?" got a concrete offer both times (Biscuit-alone at the same counter). Accepting that and building the scene as **shot / reverse shot** (Pudding's lines in the two-shot, Biscuit's lines in a Biscuit-alone shot cropped to a medium shot in the edit) kept the story and removed every listener-mouth risk for Biscuit's lines.
- "Make another Biscuit-alone version" video prompts started from the newest *still* (the two-shot), so Pudding stayed in frame (2 fails; Meta itself said so). Fix: a **still Biscuit-alone master** ("the same counter … but with ONLY Biscuit, nobody else anywhere"), then "Animate the Biscuit-ALONE counter still image". The same master served the lesson-host clips.
- Two-take phrase demos ("says it TWICE: slowly, one-second pause, natural speed"): the gap between takes measured 2.8–4.5 s, and take 2 started anywhere from 5.9 to 7.0 s. Cut them as two segments; never assume where take 2 is.
- Meta sometimes edits inside "ONE continuous static shot": Pudding walked out of frame before Biscuit spoke (C03, usable after he left), a cut to a close-up between takes (H2, used as the second take), a hall swap mid-clip on a reused master (A2, fail).
- Drift seen again: eyelashes on Biscuit (C10) and on Pudding (T01) when "NO eyelashes" was not restated for that character.
- Generation 15–40 s per clip. Refusals arrive as text in the same poll; the poll helper below stops early on "can't".
- Image downloads: the newest image is the `t39.105495` `.webp` not seen before; keep a list of known ids (the old ones stay in the DOM).

## Code Examples
Get the newest clip URL in the Meta AI thread (page JS), then download:
```js
const v=[...document.querySelectorAll('video')].filter(v=>v.currentSrc&&v.videoWidth===1280).map(v=>v.currentSrc); ({n:v.length,last:v.pop()})
```
```sh
curl -sSfL -o "clips/$NAME.mp4" "$URL"   # signed fbcdn URL, works without cookies for a while
```
Poll helper used in EP3 (stops on a refusal; set `window.__prevClip` to the newest clip id first):
```js
window.__last=()=>[...document.querySelectorAll('video')].filter(v=>v.currentSrc&&v.videoWidth).map(v=>v.currentSrc).pop()||'';
window.__poll=async()=>{let t=0; while(window.__last().includes(window.__prevClip)&&t<36){
  if(/can't make|can’t make|not able to/.test(document.body.innerText.slice(-400))) break;
  await new Promise(r=>setTimeout(r,2000)); t+=2;}
  const u=window.__last(), changed=!u.includes(window.__prevClip);
  if(changed) window.__prevClip=u.split('/').pop().split('_n.mp4')[0];
  return {t, changed, url:changed?u:'', tail:document.body.innerText.slice(-300)}};
```
Prompt skeleton (single speaker, scene master):
```
Animate the same DESK still image again (<describe layout>) into a NEW 10-second HORIZONTAL 16:9 video.
ONE continuous static shot, no cuts, no zoom, no new text or signs. <Speaker> <action> and, starting
within the first second, says <manner>: "<exact line>". ONLY <Speaker> speaks. <Other> does NOT speak:
mouth closed the whole time, <silent action>. No narration, no music, <ambience>.
```

## Thumbnail art
- Generate the cover in the same thread as a dedicated image, not a video frame: "HORIZONTAL 16:9 … NO text, NO letters … characters fully visible inside the left 55% … RIGHT 45% clean empty background for text later".
- Add the title text locally with OFL fonts (AI images misspell words), then QC at 1280×720, 320×180 and 168×94, and check the text keeps clear of characters and of the bottom-right timestamp area.
- Video frames made worse thumbnails: half-cut signs, ears cut by the text panel, and much more layout tuning.

## Constraints
**MUST DO**
- Keep one Meta AI thread per project (references depend on it).
- Lip-sync and IP QC every clip before it enters the edit list; log PASS/FAIL with a reason.
- Keep the same left/right positions per location across the episode.
- Restate each character's distinguishing details in every clip prompt (e.g. Biscuit's ORANGE beak and plain cap, Pudding with NO eyelashes); left out, they drift.
- Use a detailed scene master (and a solo-host master for lesson clips); name it by how it looks when animating.
- End every prompt with "Nobody laughs. No narration, no music, no laughing" and give the listener a closed mouth, never a "surprised" face.

**MUST NOT DO**
- Use Meta's built-in music or song lip sync for YouTube uploads.
- Prompt "in the style of" a real studio, show or artist.
- Retry or rephrase a refused prompt to get around Meta's policy.
- Accept a clip whose new character voice the owner hasn't heard. Get one listen per new voice before generating the rest.

## Decision Frameworks
- Need exact words → native audio + QC first. If the words come out wrong, use **Lip sync → Text** with a fixed voice.
- Clip passes visually but has an ad-lib → trim, don't regenerate.
- Wrong mouth moves during speech, or off-model/IP text → regenerate.

## Common Pitfalls
- Reading `n` (video count) as progress: the chat virtualises old media, so `n` can stay the same. Compare the returned URL with the previous one.
- The user interacting with the same tab can shift scroll/focus; click the prompt box before typing.

## Output Templates
Edit-decision row: `clip  in  out  SPEAKER  "line"  PASS/FAIL reason`
