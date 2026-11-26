exec(open('build/st.py').read())
SEL="""(()=>{const ed=document.querySelector('ytve-editor');const it=[...ed.querySelectorAll('ytve-endscreen-editor-preview-overlay-item')].filter(i=>i.offsetWidth>20)[%d];['mousedown','mouseup','click'].forEach(t=>it.dispatchEvent(new MouseEvent(t,{bubbles:true})));return 1})()"""
SET="""(()=>{const ed=document.querySelector('ytve-editor');const p=ed.querySelector('ytve-endscreen-editor-options-panel');const inp=p.querySelectorAll('ytve-framestamp-input input')[0];
inp.focus();inp.select();document.execCommand('insertText',false,'5:00:03');
['keydown','keyup'].forEach(t=>inp.dispatchEvent(new KeyboardEvent(t,{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true})));
['keydown','keyup'].forEach(t=>inp.dispatchEvent(new KeyboardEvent(t,{key:'Tab',code:'Tab',keyCode:9,which:9,bubbles:true})));
inp.dispatchEvent(new Event('change',{bubbles:true}));inp.blur();inp.dispatchEvent(new FocusEvent('focusout',{bubbles:true}));return inp.value})()"""
GET="""(()=>{const ed=document.querySelector('ytve-editor');const p=ed.querySelector('ytve-endscreen-editor-options-panel');return p.textContent.replace(/\\s+/g,' ').slice(0,25)+' ... '+p.textContent.replace(/\\s+/g,' ').slice(-60)+' '+[...p.querySelectorAll('ytve-framestamp-input input')].map(i=>i.value).join(' - ')})()"""
for rnd in range(2):
    for k in (1,0):
        J(SEL%k); time.sleep(1.2); print('set',k,J(SET)); time.sleep(1.2)
for k in (0,1):
    J(SEL%k); time.sleep(1.5); print(k,J(GET))
