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
- YouTube Studio: same CSP block for localhost, but the file can still go in from page JS: open `/videos/upload?d=ud`
  and run `studio_upload_video.py` (bytes over AppleScript + SHA-256 + `DataTransfer`). No manual step (owner rule,
  2026-11-24).

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
decision in `qc_log.txt`. Stop only for: Public, deleting an upload, installs of new software,
payments, and creative choices the plan leaves open (new character designs). Send one report at the end, with the
open items.

**Update (owner, 2026-11-23/24): "ไม่ต้องถามละนะ" · "update skill สามารถอัพโหลด คลิปลง youtube เองได้เลย ไม่ต้องรอฉัน".**
- **Uploading the video file to YouTube is never an owner step.** Open `/videos/upload?d=ud` in the owner's Chrome and run
  `scripts/ep6_chrome_tools/studio_upload_video.py` the moment the render passes QC. Don't ask, don't wait, don't
  hand the owner a path to drag.
- When the owner has set a release plan (e.g. "daily 08:00"), scheduling Public at that slot and downloading the
  automatic captions for the word check are already approved. Don't ask again.
- Pick new character designs yourself (sheet first, check against the bible), and log the choice.
- What is left for the owner: unlocking the screen / keeping the meta.ai tab visible, deletes, installs, payments,
  and changes to older episodes.

## 6. Attaching masters and sending prompts from page JS (EP.5, 2026-11-21)

| Need | What works |
| --- | --- |
| Re-attach a master **generated in the thread** | Its `scontent…/t39.105495-…webp` URL is CORS-readable: `fetch(url)` → `File` → `DataTransfer` → the chat's `input[type=file]` + `change` |
| Re-attach a master that was only **uploaded** to the thread | `cdn.fbsbx.com` attachment URLs send no CORS header (fetch and crossOrigin canvas both fail); `localhost` is blocked by meta.ai's CSP `connect-src`; `window.open` replaces the pane's tab; clipboard write is denied; the "+" button opens an OS picker the browser tools can't drive. Working fallback: compress the PNG to WebP (1280 px, q80, ~40 KB), send it as 4 base64 chunks into the page, check SHA-256 against the local file, and store it in `localStorage` (survives reloads). Better: generate the masters inside the thread so they have t39 URLs |
| Type a prompt | `[contenteditable=true]` is a Lexical editor: `execCommand('insertText')` does nothing; dispatch `new ClipboardEvent('paste', {clipboardData: dt})` with `dt.setData('text/plain', prompt)`. Clear leftovers with a real cmd+a + Delete first. Send = `button[aria-label="Send"]` |
| Generate many clips | An async queue in the page (`scripts/meta_queue_ep5.js`): attach → paste → Send → poll for a new `video.currentSrc` (≤180 s) → store the URL → 5 s pause → next; stop on refusal text. 13 clips in ~13 min unattended; download each with `dlqc.py` meanwhile |
| Find which thread image is which | Download candidate t39 images and diff them against the local master (`ImageChops.difference` mean = 0 for the same picture) |

## 7. Driving the owner's own Chrome without the extension (EP.6, 2026-11-23)

| Need | What works |
| --- | --- |
| Run JS in a tab | `osascript -e 'tell application "Google Chrome" to execute (tab id T of window id W) javascript "…"'` (episode `tools/cjs.py`). Needs View > Developer > **Allow JavaScript from Apple Events** in *that* Chrome profile; other profiles' windows answer "turned off". Address tabs by window id + tab id (window index changes with z-order). Results are synchronous: start async work in the page and poll a `window.__x` variable |
| Hidden tab | While the window is occluded `innerText` is empty: read `textContent` of `main` minus `script`/`style`. A **locked screen** stops Meta AI from rendering replies; a reload doesn't hydrate until unlock |
| Masters into meta.ai | Local PNG → WebP 1280 q85 → base64 into `localStorage` (`tools/inject.py`, SHA-256 check) → `DataTransfer` into the chat's `input[type=file]` |
| Prompt queue | Driven from Python (`tools/meta.py`, `tools/runq.py`), not an in-page timer loop (hidden tabs throttle timers). New clip = last `video` in DOM order after scrolling; on a 300 s timeout reload and re-check before giving up |
| Studio video upload without a drag | `tools/push_file.py` sends the file into the page as Uint8Array chunks (1.5 MB base64 per call, ~1 MB/s), SHA-256 check, then `DataTransfer` into `ytcp-uploads-file-picker input[type=file]` + `change`. **Standing owner rule since 2026-11-24: always upload this way, no drag** (`studio_upload_video.py`) |
| Subtitles without real clicks | Upload dialog: `#choose-upload-file` → inject straight into `#captions-file-loader input` (Continue with the click patch did nothing). Subtitles page: a JS `click()` on the row's `ytgn-video-translation-hover-cell` (+ its `#cell-container`) reveals `#captions-add/#captions-edit/#metadata-add`; synthetic mouseover alone doesn't. Cue count in the editor = number of `ytve-captions-marker-container` |
| Visibility on the edit page | `ytcp-video-metadata-visibility #select-button` (mousedown/up/click) → `[name=PUBLIC]` → Done → `ytcp-button#save`; reload and read "Visibility Public"; oEmbed returns 200 for a public video |
| Visible tab (EP.7) | An occluded or hidden meta.ai window stops new clips from rendering into `video` elements, and a reload doesn't re-hydrate. Keep that Chrome window **on screen** for the whole generation (ask the owner to put it there); `tools/resume.sh` polls `document.hidden` + `[contenteditable]` and restarts `runq.py` |
| Season plan (EP.7) | Read Drive `channel-plan.md` with the Google Drive connector (`search_files` → `read_file_content`); no browser needed |
| Drive the queue unbuffered (EP.7) | `python3 -u` (or `flush=True`) when logging a background queue, or the log stays empty until the end |

**Battery (EP.13, 2026-11-25):** the Mac ran down to 1 % during a render (no charger) and later locked itself: 9 h lost. Check `pmset -g batt` before the first clip and before every render;
under 30 % on battery, tell the coordinator/owner at once. `caffeinate` does not stop the lock screen after a power loss. Background waits: never `pgrep -f <own text>` in the same command
(it matches itself); match the interpreter line (`^/.*Python .*tools/run`) or `^sh build/chainN.sh`, and kill the waiting parent shell, not only its child.
