# 10 — Mac setup, a new Meta AI account, and running end to end

Measured on EP.4 (2026-11-21). Applies when the work moves to another machine or Meta AI account.

## 1. Mac setup

| Need | What works |
| --- | --- |
| Python | system `python3` + Pillow (no numpy needed). Run scripts from the episode folder |
| ffmpeg | Homebrew `ffmpeg`/`ffprobe`. It has `zoompan`, `xfade`, `loudnorm`, `alimiter`, but **no `drawtext` and no `subtitles`** → burn text as Pillow PNG overlays (`build_example_ep4_mac.py`) |
| Fonts | OFL only: Nunito, Baloo 2 (Latin), Noto Sans Thai (Thai), from github.com/google/fonts (`ofl/…`). Variable fonts: `font.set_variation_by_name("Bold")` |
| Music/SFX | `audio_gen.py` (the same file in every episode) synthesises music and SFX in pure Python, so the channel owns them outright |
| QC | `dlqc.py NAME URL` = download + speech bursts (speech band, floor + 8 dB) + 10-frame sheet; `zoom2.py NAME START END CROP` = 5 fps face strip; `preview.py` = labelled story preview of all accepted cuts |

## 2. Files the browser pane can't move

- Google Drive folders on another Google account than the Drive connector: read text files through the browser pane
  (`drive.google.com/file/d/<id>/view` renders .md/.txt/.py as text). Binary files (mp4, png) can't be pulled to the
  Mac: the page's CSP blocks fetches to localhost. Get images from the Meta AI thread instead (signed fbcdn URLs
  can be fetched with curl), or ask the owner to download.
- YouTube Studio: same CSP block → the owner drags `out/<episode>.mp4` into the upload dialog. Open the dialog first
  (`/videos/upload?d=ud`) so the drag is the only manual step.

## 3. A new Meta AI account

1. Start a new thread. Message 1: attach the character sheets (in-page `fetch(fbcdn URL)` → `DataTransfer` → the
   chat's `input[type=file]`, `change` event), describe each sheet by name, "do not create anything yet, reply OK".
2. Message 2: attach the location masters the same way, named by look (TAXI RANK, KERB, …).
3. Clips animate from attached images. After several turns Meta answers "I can no longer access the X image":
   attach the master again with the prompt ("Here is the X image again. Animate this attached image…").
4. Old-thread image URLs are signed and expire (≈ 4 days). Save every sheet and master as PNG locally
   (`Characters/`, `masters/`) as soon as it is accepted.
5. Voices are generated per clip, not per account, but check: one listen file comparing an old-account clip and a
   new-account clip of each recurring character (EP.4: owner approved Frank, Pudding, Ollie, Biscuit).

## 4. Page-driving helpers (meta.ai)

- `__upload(items)`: fetch each URL as a Blob → File → DataTransfer → `input[type=file].files` → `change`.
- `__vw(ms)`: poll `video` elements for a new `currentSrc` not in the "before" set (mark the set right before
  sending). Lazy-loaded old videos can appear as "new" right after a reload: check the clip id before downloading.
- Type prompts with the computer tool; never put `\"` in the typed text (backslashes are typed literally).
- After a reload all `window.__*` helpers are gone; define them again.
- JS calls time out at 45 s: wait in two calls (≈25 s + ≈15 s).

## 5. End to end (owner rule, 2026-11-21)

Run masters → clips → QC → assembly → thumbnail → metadata → Studio prep without asking after each step. Log every
decision in `qc_log.txt`. Stop only for: Public, deleting an upload, installs of new software, the Studio drag,
payments, and creative choices the plan leaves open (new character designs). Send one report at the end, with the
open items.

## 6. Attaching masters and sending prompts from page JS (EP.5, 2026-11-21)

| Need | What works |
| --- | --- |
| Re-attach a master **generated in the thread** | Its `scontent…/t39.105495-…webp` URL is CORS-readable: `fetch(url)` → `File` → `DataTransfer` → the chat's `input[type=file]` + `change` |
| Re-attach a master that was only **uploaded** to the thread | `cdn.fbsbx.com` attachment URLs send no CORS header (fetch and crossOrigin canvas both fail); `localhost` is blocked by meta.ai's CSP `connect-src`; `window.open` replaces the pane's tab; clipboard write is denied; the "+" button opens an OS picker the browser tools can't drive. Working fallback: compress the PNG to WebP (1280 px, q80, ~40 KB), send it as 4 base64 chunks into the page, check SHA-256 against the local file, and store it in `localStorage` (survives reloads). Better: generate the masters inside the thread so they have t39 URLs |
| Type a prompt | `[contenteditable=true]` is a Lexical editor: `execCommand('insertText')` does nothing; dispatch `new ClipboardEvent('paste', {clipboardData: dt})` with `dt.setData('text/plain', prompt)`. Clear leftovers with a real cmd+a + Delete first. Send = `button[aria-label="Send"]` |
| Generate many clips | An async queue in the page (`scripts/meta_queue_ep5.js`): attach → paste → Send → poll for a new `video.currentSrc` (≤180 s) → store the URL → 5 s pause → next; stop on refusal text. 13 clips in ~13 min unattended; download each with `dlqc.py` meanwhile |
| Find which thread image is which | Download candidate t39 images and diff them against the local master (`ImageChops.difference` mean = 0 for the same picture) |
