// Meta AI (meta.ai) page helpers. Run once in the thread's page, then call window.__poll() after each prompt.
// The browser tool's JS call times out at 45 s, so one poll waits at most 36 s; call it again while changed=false.
// Before the first prompt: window.__prevClip = '<id of the newest clip in the thread>' ('' when there is none).
window.__last = () => [...document.querySelectorAll('video')].filter(v => v.currentSrc && v.videoWidth).map(v => v.currentSrc).pop() || '';
window.__poll = async () => {
  let t = 0;
  while (window.__last().includes(window.__prevClip) && t < 36) {
    if (/can't make|can’t make|not able to/.test(document.body.innerText.slice(-400))) break;  // refusal text
    await new Promise(r => setTimeout(r, 2000)); t += 2;
  }
  const u = window.__last(), changed = !u.includes(window.__prevClip);
  if (changed) window.__prevClip = u.split('/').pop().split('_n.mp4')[0];
  // tail = the last text on the page: read it for refusals before assuming the clip is still generating
  return { t, changed, url: changed ? u : '', tail: document.body.innerText.slice(-300) };
};
// Newest image: not always the last <img>. List the last few t39.105495 .webp images with their sizes and
// compare with the ids already saved.
'ready';
