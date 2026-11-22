// Meta AI page helpers used for Pudding EP.5 (2026-11-21). Paste into the meta.ai thread page with the browser tool's
// JavaScript call (each call times out at 45 s, so start long work without awaiting it and poll window.__qlog).
// See references/10-mac-new-account-and-end-to-end.md section 6.

// --- files to attach -------------------------------------------------------------------------------------------------
// A master generated in this thread has a CORS-readable t39 URL:
window.__urlFile = async (url, name) => { const r = await fetch(url); const b = await r.blob(); return new File([b], name, { type: b.type || 'image/webp' }); };
// A master that only exists as an upload (cdn.fbsbx.com, no CORS) was sent once as base64 and kept in localStorage:
//   window.__b64 = [chunk0, chunk1, ...];  // check SHA-256 of the decoded bytes against the local file
//   localStorage.setItem('__ep5_reception_b64', window.__b64.join(''));
window.__lsFile = (key, name) => { const s = localStorage.getItem(key); const bin = Uint8Array.from(atob(s), c => c.charCodeAt(0)); return new File([bin], name, { type: 'image/webp' }); };
window.__attach = async (files) => {
  const dt = new DataTransfer(); files.forEach(f => dt.items.add(f));
  const inp = [...document.querySelectorAll('input[type=file]')].pop(); inp.files = dt.files;
  inp.dispatchEvent(new Event('change', { bubbles: true }));
};

// --- prompt box (Lexical): execCommand does not work, a paste event does -----------------------------------------
window.__send = async (text, go) => {
  const ed = [...document.querySelectorAll('[contenteditable=true]')].pop(); ed.focus();
  if (ed.innerText.trim()) return { err: 'not empty: clear it with a real cmd+a + Delete first' };
  const dt = new DataTransfer(); dt.setData('text/plain', text);
  ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  await new Promise(r => setTimeout(r, 700));
  const ok = ed.innerText.trim() === text.trim();
  if (go && ok) { window.__vk(); [...document.querySelectorAll('button')].find(b => b.getAttribute('aria-label') === 'Send').click(); }
  return { ok };
};

// --- new clip detection --------------------------------------------------------------------------------------------
window.__vk = () => { window.__vknown = new Set([...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(Boolean).map(s => s.split('?')[0])); };
window.__newVids = () => [...new Set([...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(s => s && !window.__vknown.has(s.split('?')[0])))];

// --- queue: [[name, masterKeyOrFn, promptText], ...] -> window.__R[name] = clip URL ---------------------------------
// window.__U2 = { desk: '<t39 url>', room: '<t39 url>', host: '<t39 url>' };
window.__R = window.__R || {}; window.__qlog = [];
window.__runQ = async (Q) => {
  while (Q.length) {
    const [name, master, text] = Q.shift(); await new Promise(r => setTimeout(r, 5000));
    const f = master === 'reception' ? window.__lsFile('__ep5_reception_b64', 'm6_reception.webp') : await window.__urlFile(window.__U2[master], master + '_master.webp');
    await window.__attach([f]); await new Promise(r => setTimeout(r, 1800));
    const s = await window.__send(text, true);
    if (!s.ok) { window.__qlog.push(name + ' SENDFAIL'); Q.unshift([name, master, text]); return; }
    let t = 0, stop = false;
    while (t < 180) {
      await new Promise(r => setTimeout(r, 2000)); t += 2;
      if (window.__newVids().length) break;
      if (/can.t make|can’t make|not able to|couldn.t attach|can no longer access|I can.t help/i.test(document.body.innerText.slice(-500))) { stop = true; break; }
    }
    if (stop) { window.__qlog.push(name + ' STOP ' + document.body.innerText.slice(-500)); return; } // log the refusal; never reword
    window.__R[name] = window.__newVids()[0] || null; window.__qlog.push(name + ' ' + t);
  }
  window.__qlog.push('DONE');
};
// window.__runQ(myQueue);  // then poll: JSON.stringify({log: window.__qlog, R: window.__R})
