// EP.6 page helpers (owner's Chrome via AppleScript; the tab is often hidden, so read textContent, not innerText,
// and drive the waiting from outside the page: hidden tabs throttle chained timers).
window.__lsFile = (key, name) => { const s = localStorage.getItem(key); const bin = Uint8Array.from(atob(s), c => c.charCodeAt(0)); return new File([bin], name, { type: 'image/webp' }); };
window.__attach = (files) => { const dt = new DataTransfer(); files.forEach(f => dt.items.add(f));
  const inp = [...document.querySelectorAll('input[type=file]')].pop(); inp.files = dt.files;
  inp.dispatchEvent(new Event('change', { bubbles: true })); return inp.accept + ' ' + inp.files.length; };
window.__ed = () => [...document.querySelectorAll('[contenteditable=true]')].pop();
window.__paste = (text) => { const ed = window.__ed(); ed.focus();
  if (ed.textContent.trim()) return 'NOTEMPTY';
  const dt = new DataTransfer(); dt.setData('text/plain', text);
  ed.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true })); return 'PASTED'; };
window.__edText = () => window.__ed().textContent;
window.__clear = () => { const ed = window.__ed(); ed.focus(); document.execCommand('selectAll'); document.execCommand('delete'); return ed.textContent.length; };
window.__vids = () => [...new Set([...document.querySelectorAll('video')].map(v => v.currentSrc || v.src || (v.querySelector('source')||{}).src).filter(Boolean))];
window.__imgs = () => [...new Set([...document.images].map(i => i.currentSrc || i.src).filter(s => s.includes('t39.105495')))];
window.__mark = () => { window.__kv = new Set(window.__vids().map(s => s.split('?')[0])); window.__ki = new Set(window.__imgs().map(s => s.split('?')[0])); window.__tc0 = document.body.textContent.length; return window.__kv.size + '/' + window.__ki.size; };
window.__sendBtn = () => [...document.querySelectorAll('button')].find(b => b.getAttribute('aria-label') === 'Send');
window.__go = () => { const b = window.__sendBtn(); if (!b || b.disabled) return 'NOSEND'; b.click(); return 'SENT'; };
window.__state = () => JSON.stringify({
  nv: window.__vids().filter(s => !window.__kv.has(s.split('?')[0])),
  ni: window.__imgs().filter(s => !window.__ki.has(s.split('?')[0])),
  tail: document.body.textContent.replace(/\s+/g, ' ').slice(-700) });
'helpers ok';
window.__lastV = () => { const v = [...document.querySelectorAll('video')].map(v => v.currentSrc || v.src || '').filter(Boolean); return v.length ? v[v.length - 1] : ''; };
window.__txt = () => { const m = document.querySelector('main') || document.body; return (m.innerText || m.textContent).replace(/\s+/g, ' '); };
window.__st2 = () => { window.scrollTo(0, 1e9); document.querySelectorAll('[class*=scroll], main').forEach(e => { try { e.scrollTop = e.scrollHeight; } catch (x) {} });
  return JSON.stringify({ last: window.__lastV(), tail: window.__txt().slice(-900) }); };
'helpers2 ok';
window.__txt = () => { const m = (document.querySelector('main') || document.body).cloneNode(true); m.querySelectorAll('script,style,template').forEach(e => e.remove()); return (m.innerText && m.innerText.length > 50 ? m.innerText : m.textContent).replace(/\s+/g, ' '); };
'helpers3 ok';
window.__lastI = () => { const v = [...document.images].map(i => i.currentSrc || i.src).filter(s => s.includes('t39.105495') && !s.includes('.mp4')); return v.length ? v[v.length - 1] : ''; };
window.__st2 = () => { window.scrollTo(0, 1e9); document.querySelectorAll('[class*=scroll], main').forEach(e => { try { e.scrollTop = e.scrollHeight; } catch (x) {} });
  return JSON.stringify({ last: window.__lastV(), img: window.__lastI(), tail: window.__txt().slice(-900) }); };
'helpers4 ok';
window.__lastMp4 = () => { const m = document.documentElement.innerHTML.match(/https:\/\/scontent[^"' <>]*?\.mp4[^"' <>\\]*(?:\\u0026[^"' <>\\]*)*/g) || []; return m.length ? m[m.length - 1].replace(/\\u0026/g, '&').replace(/&amp;/g, '&') : ''; };
window.__st2 = () => { window.scrollTo(0, 1e9); document.querySelectorAll('[class*=scroll], main').forEach(e => { try { e.scrollTop = e.scrollHeight; } catch (x) {} });
  return JSON.stringify({ last: window.__lastV() || window.__lastMp4(), img: window.__lastI(), tail: window.__txt().slice(-900) }); };
'helpers5 ok';
