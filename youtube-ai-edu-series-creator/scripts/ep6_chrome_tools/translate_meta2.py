"""EP.16: Studio's NEW Languages page (28 Nov 2026): Add language -> pick -> a ytcp-dialog '<Lang>' with two contenteditable #textbox (title, description) + 'Update'."""
import sys, time, json, re
sys.path.insert(0, 'tools'); from cjs import run
T = '645346567'
s = open('docs/family-ep16-upload-metadata.md', encoding='utf-8').read()
M = json.load(open('build/meta.json'))
rest = M['desc'][M['desc'].index('Phrases in this lesson:'):]
rows = {}
for line in s.split('## Translations')[1].split('## Thumbnail')[0].splitlines():
    m = re.match(r'\| (TH|ES|PT|VI|ID) \| (.*?) \| (.*) \|$', line)
    if m: rows[m.group(1)] = (m.group(2).replace('\\|', '|'), m.group(3))
names = {'TH': 'Thai', 'ES': 'Spanish', 'PT': 'Portuguese', 'VI': 'Vietnamese', 'ID': 'Indonesian'}
DLG = "[...document.querySelectorAll('ytcp-dialog')].filter(d=>d.offsetParent&&d.textContent.trim().startsWith(%s))[0]"
for code in sys.argv[1:]:
    lang = names[code]; title, opening = rows[code]; desc = opening + '\n\n' + rest
    assert len(title) <= 100, (code, len(title))
    if run(T, "String(!!(" + DLG % json.dumps(lang) + "))") != 'true':
        run(T, "document.querySelector('#add-translations-button').click();1"); time.sleep(2)
        print(code, run(T, "(()=>{const it=[...document.querySelectorAll('tp-yt-paper-item')].filter(i=>i.offsetParent!==null||true).find(i=>i.textContent.trim()===%s);if(!it)return 'noitem';it.scrollIntoView();it.click();return 'picked'})()" % json.dumps(lang)))
        for _ in range(10):
            time.sleep(1.5)
            if run(T, "String(!!(" + DLG % json.dumps(lang) + "))") == 'true': break
    r = run(T, """(()=>{const d=%s;if(!d)return 'nodlg';const tb=[...d.querySelectorAll('#textbox[contenteditable]')];
function put(t,v){t.focus();document.execCommand('selectAll');document.execCommand('insertText',false,v);}
put(tb[0],%s);put(tb[1],%s);return tb.length+' '+tb[0].innerText.length+' '+tb[1].innerText.length})()""" % (DLG % json.dumps(lang), json.dumps(title, ensure_ascii=False), json.dumps(desc, ensure_ascii=False)))
    print(code, 'filled', r); time.sleep(1.5)
    print(code, run(T, """(()=>{const d=%s;const b=[...d.querySelectorAll('ytcp-button,button')].filter(b=>b.textContent.trim()==='Update').pop();if(!b)return 'noupdate';if(b.hasAttribute('disabled')||b.getAttribute('aria-disabled')==='true')return 'disabled';b.click();return 'updated'})()""" % (DLG % json.dumps(lang))))
    time.sleep(5)
    print(code, 'dialog still open:', run(T, "String(!!(" + DLG % json.dumps(lang) + "))"))
print(run(T, "JSON.stringify([...document.querySelectorAll('ytgn-video-translation-row')].map(r=>r.textContent.replace(/\\s+/g,' ').trim().slice(0,70)))"))
