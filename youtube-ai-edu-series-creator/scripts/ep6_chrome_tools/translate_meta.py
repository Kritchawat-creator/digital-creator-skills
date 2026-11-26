import sys, time, json, re
sys.path.insert(0, 'tools'); from cjs import run
T = '645346567'
s = open('docs/pudding-ep10-upload-metadata.md', encoding='utf-8').read()
M = json.load(open('build/meta.json'))
rest = M['desc'][M['desc'].index('Phrases in this lesson:'):]
rows = {}
for line in s.split('## Translations')[1].split('## Thumbnail')[0].splitlines():
    m = re.match(r'\| (TH|ES|PT|VI|ID) \| (.*?) \| (.*) \|$', line)
    if m: rows[m.group(1)] = (m.group(2).replace('\\|', '|'), m.group(3))
names = {'TH': 'Thai', 'ES': 'Spanish', 'PT': 'Portuguese', 'VI': 'Vietnamese', 'ID': 'Indonesian'}
for code in sys.argv[1:]:
    lang = names[code]; title, opening = rows[code]; desc = opening + '\n\n' + rest
    has = run(T, "String([...document.querySelectorAll('ytgn-video-translation-row')].some(r=>r.textContent.trim().startsWith(%s)))" % json.dumps(lang))
    if has != 'true':
        run(T, "[...document.querySelectorAll('ytcp-button')].find(b=>b.offsetParent&&b.textContent.trim()==='Add language').click();1"); time.sleep(1.5)
        run(T, "(()=>{const it=[...document.querySelectorAll('tp-yt-paper-item')].find(i=>i.textContent.trim()===%s);it.scrollIntoView();it.click();return 1})()" % json.dumps(lang)); time.sleep(2.5)
    run(T, "(()=>{const r=[...document.querySelectorAll('ytgn-video-translation-row')].find(r=>r.textContent.trim().startsWith(%s));const c=r.querySelectorAll('ytgn-video-translation-hover-cell')[1];['pointerover','pointerenter','mouseover','mouseenter'].forEach(t=>c.dispatchEvent(new MouseEvent(t,{bubbles:true})));c.click();c.querySelector('#cell-container').click();return 1})()" % json.dumps(lang)); time.sleep(2.5)
    print(code, run(T, "(()=>{const r=[...document.querySelectorAll('ytgn-video-translation-row')].find(r=>r.textContent.trim().startsWith(%s));const b=r.querySelector('#metadata-add, #metadata-edit');if(!b)return 'nobtn '+[...r.querySelectorAll('[id]')].map(e=>e.id).join(',');b.click();return 'open'})()" % json.dumps(lang)))
    ok = False
    for _ in range(8):
        time.sleep(1.5)
        h = run(T, "(()=>{const e=[...document.querySelectorAll('ytgn-metadata-editor')].filter(e=>e.offsetParent).pop();return e?e.textContent.replace(/\\s+/g,' ').trim().slice(0,140):''})()")
        if lang in h: ok = True; break
    if not ok: print(code, 'EDITOR NOT OPEN', h); continue
    r = run(T, """(()=>{const e=[...document.querySelectorAll('ytgn-metadata-editor')].filter(e=>e.offsetParent).pop();const ta=[...e.querySelectorAll('textarea')];
const set=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set;
function put(t,v){t.focus();set.call(t,v);t.dispatchEvent(new Event('input',{bubbles:true}));t.dispatchEvent(new Event('change',{bubbles:true}));}
put(ta[1],%s);put(ta[3],%s);return ta.length+' '+ta[1].value.slice(0,30)+' | '+ta[3].value.length})()""" % (json.dumps(title, ensure_ascii=False), json.dumps(desc, ensure_ascii=False)))
    print(code, r); time.sleep(1)
    print(code, run(T, "(()=>{const e=[...document.querySelectorAll('ytgn-metadata-editor')].filter(e=>e.offsetParent).pop();const d=e.closest('tp-yt-paper-dialog, ytcp-dialog')||document;const b=[...d.querySelectorAll('ytcp-button')].filter(b=>b.offsetParent&&b.textContent.trim()==='Publish').pop();if(!b)return 'nopub';b.click();return 'published'})()"))
    time.sleep(4)
print(run(T, "JSON.stringify([...document.querySelectorAll('ytgn-video-translation-row')].map(r=>r.textContent.replace(/\\s+/g,' ').trim().slice(0,70)))"))
