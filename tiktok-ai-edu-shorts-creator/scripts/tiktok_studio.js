// TikTok Studio web (tiktok.com/tiktokstudio/upload) helpers for the browser tool's page-JS call.
// The OWNER uploads the video and the cover (the in-app browser has no file upload). Never press Post / Discard, and
// press Schedule only for a slot the owner approved in chat. Keep all work in the upload tab: the page has no Save draft
// button on web, so a reload or navigating away loses description, cover and editor text.

// 1) Description box is a contenteditable; cmd+a does NOT select in the browser pane. Select its contents first,
//    then press Backspace with the computer tool, then type the caption (hashtags become links on a trailing space).
(() => { const e = [...document.querySelectorAll('[contenteditable="true"]')][0]; e.focus();
  const r = document.createRange(); r.selectNodeContents(e); const s = getSelection(); s.removeAllRanges(); s.addRange(r);
  return s.toString().length; })();

// 1b) If one Backspace removed only one character (EP02, EP04): put the caret at the end, then Backspace x(len+5).
(() => { const e = [...document.querySelectorAll('[contenteditable="true"]')][0]; e.focus();
  const r = document.createRange(); r.selectNodeContents(e); r.collapse(false); const s = getSelection();
  s.removeAllRanges(); s.addRange(r); return e.innerText.length; })();

// 2b) AI-generated content switch by element (a coordinate click can hit "Learn more" and navigate away).
(() => { const sw = [...document.querySelectorAll('input[type=checkbox],[role=switch]')].find(e => { let p = e, t = '';
    for (let i = 0; i < 6 && p; i++) { p = p.parentElement; if (p && p.innerText && p.innerText.length < 120) t = p.innerText; }
    return t.startsWith('AI-generated content'); });
  if (!(sw.checked ?? sw.getAttribute('aria-checked') === 'true')) sw.click(); return location.href; })();

// 2) Read back description + switches (expect "AI-generated content: true").
(() => ({ desc: [...document.querySelectorAll('[contenteditable="true"]')][0]?.innerText,
  switches: [...document.querySelectorAll('input[type=checkbox],[role=switch]')].map(e => { let p = e, t = '';
    for (let i = 0; i < 6 && p; i++) { p = p.parentElement; if (p && p.innerText && p.innerText.length < 120) t = p.innerText; }
    return t.split('\n')[0] + ': ' + (e.checked ?? e.getAttribute('aria-checked')); }),
  buttons: [...document.querySelectorAll('button')].filter(b => b.getBoundingClientRect().width > 0).map(b => b.innerText.trim()).filter(Boolean) }))();

// 3) Editor (Edit -> Text): the content box is a <textarea>; cmd+a fails here too. Select, then type to replace:
window.__selTA = () => { const t = [...document.querySelectorAll('textarea')].find(t => t.getBoundingClientRect().width > 0);
  t.focus(); t.setSelectionRange(0, t.value.length); return t.value; };
// Font dropdown ignores the computer-tool click: open it with a pointer/mouse sequence, return the item's CSS rect
// (divide by 1.75 for the 800-px screenshot frame at a 1400x900 viewport), then click it with the computer tool.
window.__openFont = () => { const t = document.querySelector('.PropSettingTextFontFamily__trigger'); if (!t) return 'no trigger';
  for (const ev of ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'])
    t.dispatchEvent(new (ev.startsWith('pointer') ? PointerEvent : MouseEvent)(ev, { bubbles: true, cancelable: true, view: window }));
  return 'ok'; };
window.__pickFont = async (name) => { window.__openFont(); await new Promise(r => setTimeout(r, 800));
  const it = [...document.querySelectorAll('.Select__item')].find(e => e.innerText.includes(name));
  if (!it) return { err: 'no item' }; it.scrollIntoView({ block: 'center' }); const r = it.getBoundingClientRect();
  return { x: r.x + r.width / 2, y: r.y + r.height / 2, text: it.innerText }; };
// Font size: triple_click the size box with the computer tool, type the number, Return (a JS focus() there reverted
// the font once). If the preview stage is blank: zoom menu "100%" -> "Zoom to fit".

// 4) Cover crop check (3:4 profile-grid crop TikTok makes from the uploaded cover): where is the red/green text?
(() => { const i = [...document.querySelectorAll('img')].find(i => i.naturalWidth === 486 && i.naturalHeight === 648);
  const c = document.createElement('canvas'); c.width = 486; c.height = 648; const g = c.getContext('2d'); g.drawImage(i, 0, 0);
  const d = g.getImageData(0, 0, 486, 648).data; const rows = f => { const ys = []; for (let y = 0; y < 648; y++) { let n = 0;
    for (let x = 0; x < 486; x++) { const k = (y * 486 + x) * 4; if (f(d[k], d[k + 1], d[k + 2])) n++; } if (n > 8) ys.push(y); } return [ys[0], ys.at(-1)]; };
  return { red: rows((r, g, b) => r > 190 && g < 80 && b < 80), green: rows((r, g, b) => g > 140 && r < 110 && b < 110) }; })();
// Text rows must be > ~20 px from the top/bottom of the 648-px crop. Block 4 takes the FIRST 486x648 <img>, which can be
// a stale hidden one (EP04: it read the old frame-0 blob, no text rows) - use block 5 on the visible thumbnail first.

// 5) Did the owner's cover land? Count red/green text pixels in the top 45% of the cover thumbnail on the upload page
//    (the real cover has thousands of each; frame 0 with a white overlay has ~0). Don't trust input[type=file].files.
[...document.querySelectorAll('img')].filter(i => { const r = i.getBoundingClientRect(); return r.width > 50 && i.naturalWidth === 486; })
  .map(i => { const c = document.createElement('canvas'); c.width = 486; c.height = 648; const g = c.getContext('2d'); g.drawImage(i, 0, 0);
    const d = g.getImageData(0, 0, 486, 292).data; let red = 0, green = 0;
    for (let k = 0; k < d.length; k += 4) { if (d[k] > 190 && d[k + 1] < 80 && d[k + 2] < 80) red++; if (d[k + 1] > 140 && d[k] < 110 && d[k + 2] < 110) green++; }
    return { red, green }; });

// 6) Before pressing Schedule: read the time/date inputs and the browser time zone, then bring the button into view.
(() => ({ inputs: [...document.querySelectorAll('input')].map(i => i.value).filter(v => /\d\d:\d\d|20\d\d-/.test(v)),
  tz: Intl.DateTimeFormat().resolvedOptions().timeZone }))();
//   const b=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()==='Schedule'&&b.getBoundingClientRect().width>0); b.scrollIntoView({block:'center'});
// After Schedule the tab goes to Studio -> Content; reload and read the row: "Nov 22, 5:00 PM (GMT+7) Bangkok".
