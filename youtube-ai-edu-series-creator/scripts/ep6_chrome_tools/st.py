import sys,json,time
sys.path.insert(0,'tools'); from cjs import run
T='645346567'
def J(c): return run(T,c)
M=json.load(open('build/meta.json'))
PATCH="""(()=>{if(!window.__origClick){window.__origClick=HTMLInputElement.prototype.click;HTMLInputElement.prototype.click=function(){if(this.type==='file'){window.__blockedInput=this;return;}return window.__origClick.call(this);};}return 1})()"""
