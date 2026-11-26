"""Replace one line in the PUBLISHED title/description translations of a video (owner's yes needed).
Usage: link_translations.py <tab on /video/<id>/translations> <OLD> <NEW> <backup.json> LANG [LANG ...]
Backs up every translation before changing it; changes only OLD -> NEW; stops if OLD is not there exactly once."""
import json, os, sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from cjs import run
T, OLD, NEW, BK = sys.argv[1:5]
ED = "const e=[...document.querySelectorAll('ytgn-metadata-editor')].filter(e=>e.offsetParent).pop();"
ROW = "const r=[...document.querySelectorAll('ytgn-video-translation-row')].find(r=>r.textContent.trim().startsWith(%s));"
bk = json.load(open(BK)) if os.path.exists(BK) else {}
for lang in sys.argv[5:]:
    L = json.dumps(lang)
    run(T, "(()=>{" + ROW % L + "const c=r.querySelectorAll('ytgn-video-translation-hover-cell')[1];['pointerover','pointerenter','mouseover','mouseenter'].forEach(t=>c.dispatchEvent(new MouseEvent(t,{bubbles:true})));c.click();c.querySelector('#cell-container').click();return 1})()"); time.sleep(2.5)
    o = run(T, "(()=>{" + ROW % L + "const b=r.querySelector('#metadata-edit');if(!b)return 'nobtn '+[...r.querySelectorAll('[id]')].map(e=>e.id).join(',');b.click();return 'open'})()")
    ok = False
    for _ in range(8):
        time.sleep(1.5)
        h = run(T, "(()=>{" + ED + "return e?e.textContent.replace(/\\s+/g,' ').trim().slice(0,140):''})()")
        if lang in h: ok = True; break
    if not ok: raise SystemExit(f'{lang}: editor not open ({o}) {h}')
    v = json.loads(run(T, "(()=>{" + ED + "return JSON.stringify([...e.querySelectorAll('textarea')].map(t=>t.value))})()"))
    title, desc = v[1], v[3]
    if desc.count(OLD) != 1: raise SystemExit(f'{lang}: OLD found {desc.count(OLD)} times; editor left open, nothing changed')
    bk[lang] = {'title': title, 'desc': desc}; json.dump(bk, open(BK, 'w'), ensure_ascii=False, indent=1)
    new = desc.replace(OLD, NEW)
    r = run(T, "(()=>{" + ED + "const t=e.querySelectorAll('textarea')[3];t.focus();Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(t,%s);t.dispatchEvent(new Event('input',{bubbles:true}));t.dispatchEvent(new Event('change',{bubbles:true}));return String(t.value===%s)+' '+(e.querySelectorAll('textarea')[1].value===%s)})()" % (json.dumps(new, ensure_ascii=False), json.dumps(new, ensure_ascii=False), json.dumps(title, ensure_ascii=False)))
    if r != 'true true': raise SystemExit(f'{lang}: value not set ({r})')
    time.sleep(1)
    # a background tab never paints the dialog (display:none), so click the editor's own #publish-button
    p = run(T, "(()=>{" + ED + "const b=e.querySelector('#publish-button');if(!b||b.getAttribute('aria-disabled')==='true')return 'nopub';b.click();return 'Publish'})()")
    print(lang, '|', title[:40], '|', len(desc), '->', len(new), '|', p, flush=True)
    if p.startswith('nopub'): raise SystemExit(1)
    time.sleep(6)
