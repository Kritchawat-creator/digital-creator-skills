#!/usr/bin/env python3
"""Owner rule 2026-11-26: Meta AI in Thinking mode for EVERY prompt. thinking.py [tab] -> makes sure the composer mode is Thinking and prints the readback.
Control: button[data-testid=composer-mode-dropdown-button] (text = current mode); menu items role=menuitemradio "Instant" / "Thinking" (aria-checked).
Never touches paid/upgrade items. Exit 1 if Thinking can't be set (log it and tell the coordinator; no workaround)."""
import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cjs import run
TAB = sys.argv[1] if len(sys.argv) > 1 else "645346540"
B = "document.querySelector('[data-testid=composer-mode-dropdown-button]')"
def mode(): return run(TAB, f"(()=>{{const b={B};return b?b.textContent.trim():'NOBUTTON'}})()")
def main():
    m = mode()
    if m == "Thinking": print("MODE Thinking (already)"); return 0
    if m == "NOBUTTON": print("MODE ? no mode button"); return 1
    run(TAB, f"(()=>{{const b={B};const r=b.getBoundingClientRect();const o={{bubbles:true,cancelable:true,pointerId:1,pointerType:'mouse',button:0,clientX:r.x+5,clientY:r.y+5}};b.dispatchEvent(new PointerEvent('pointerdown',o));return 1}})()")
    time.sleep(1.2)
    r = run(TAB, f"(()=>{{const b={B};const m=document.getElementById(b.getAttribute('aria-controls')||'');if(!m)return 'nomenu';const it=[...m.querySelectorAll('[role^=menuitem]')].find(e=>/^Thinking/.test(e.innerText.trim()));if(!it)return 'noitem';it.click();return 'clicked'}})()")
    time.sleep(1.5); m = mode(); print("MODE", m, r)
    return 0 if m == "Thinking" else 1
if __name__ == "__main__": sys.exit(main())
