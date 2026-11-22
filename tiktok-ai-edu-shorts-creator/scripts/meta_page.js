// Meta AI web chat helpers (paste the needed block into the browser tool's page-JS call; each call must stay < 38 s).
// Typing: the visible prompt box is a contenteditable; the hidden <textarea> ignores value setters and form_input.
// Click the box, then type with the computer tool, then press Return. Check what landed with:
//   [...document.querySelectorAll('[contenteditable="true"]')].map(e=>e.innerText.length)

// 1) Before a new IMAGE: remember the image ids already in the thread (old ones stay in the DOM, some lazy 0x0).
window.__seen = new Set([...document.querySelectorAll('img')].filter(i => i.src.includes('t39.105495'))
  .map(i => (i.src.match(/\/(\d+_\d+_\d+_n)\./) || [])[1]));
window.__newimgs = () => { const m = new Map();
  [...document.querySelectorAll('img')].filter(i => i.src.includes('t39.105495')).forEach(i => {
    const id = (i.src.match(/\/(\d+_\d+_\d+_n)\./) || [])[1];
    if (id && !window.__seen.has(id)) m.set(id, { id, w: i.naturalWidth, h: i.naturalHeight, src: i.src }); });
  return [...m.values()]; };
// Poll for a VERTICAL image (h > w). An unseen 2048x1152 one is usually an OLD lazy-loaded image: add it to __seen.
//   let t=0; while(window.__newimgs().filter(x=>x.w&&x.h>x.w).length<1&&t<36){ if(/can't make|can’t make|not able to/.test(document.body.innerText.slice(-400))) break; await new Promise(r=>setTimeout(r,2000)); t+=2;} ({t, imgs:window.__newimgs(), tail:document.body.innerText.slice(-250)})

// 2) Before a new VIDEO: remember the video files already in the thread. Vertical clips are 720x1280, so never
//    filter on videoWidth===1280 (the 16:9 helper in the YouTube skill does).
window.__vid = v => v.split('/').pop().split('?')[0];
window.__vseen = new Set([...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(Boolean).map(window.__vid));
window.__vpoll = async () => { let t = 0;
  const nv = () => [...document.querySelectorAll('video')].filter(v => (v.currentSrc || v.src) && !window.__vseen.has(window.__vid(v.currentSrc || v.src)));
  while (nv().filter(v => v.videoWidth).length < 1 && t < 36) {
    if (/can't make|can’t make|not able to|can't create|can’t create/.test(document.body.innerText.slice(-500))) break;
    await new Promise(r => setTimeout(r, 2000)); t += 2; }
  return { t, n: nv().map(v => ({ id: window.__vid(v.currentSrc || v.src), w: v.videoWidth, h: v.videoHeight, d: v.duration, url: v.currentSrc || v.src })),
           tail: document.body.innerText.slice(-350) }; };
// Call `await window.__vpoll()` repeatedly (first call usually returns n:[] while Meta "composes"; clips take 40-80 s).
// After downloading, mark it seen:
//   [...document.querySelectorAll('video')].map(v=>v.currentSrc||v.src).filter(Boolean).forEach(s=>window.__vseen.add(window.__vid(s)))
// Download right away with curl (signed fbcdn URLs expire):  curl -sSfL -o clips/C1_v1.mp4 "<url>"

// 3) A new image can stay an empty <img> (no src) until clicked. Click it with the computer tool, then:
//      window.__newimgs().filter(x=>x.w)      -> the 1152x2048 image with its src
//    then press Escape: the image viewer has its OWN prompt box. Before typing the next prompt check:
//      [...document.querySelectorAll('[contenteditable="true"]')].length === 1
// Fix prompts for a drifting character start with "Create a brand-new image from scratch (do not edit or reuse the
// previous image)." - otherwise Meta may return an edit of the last image.

