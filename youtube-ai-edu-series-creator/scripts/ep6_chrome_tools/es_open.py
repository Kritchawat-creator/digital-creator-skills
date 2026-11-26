exec(open('build/st.py').read())
J("location.href='https://studio.youtube.com/video/yVKBL1bOGzA/edit';1"); time.sleep(16)
J("(()=>{const b=document.querySelector('#toggle-button');b&&b.click();return 1})()"); time.sleep(3)
print(J("""(()=>{const e=[...document.querySelectorAll('ytcp-text-dropdown-trigger')].find(x=>/End screen/.test(x.textContent));if(!e)return 'none';e.scrollIntoView({block:'center'});const b=e.querySelector('ytcp-dropdown-trigger, [role=button], .container')||e;['mousedown','mouseup','click'].forEach(t=>b.dispatchEvent(new MouseEvent(t,{bubbles:true,composed:true})));return e.textContent.replace(/\\s+/g,' ').trim()})()""")); time.sleep(10)
