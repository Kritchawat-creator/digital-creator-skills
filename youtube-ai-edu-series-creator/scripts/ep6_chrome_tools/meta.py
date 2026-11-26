#!/usr/bin/env python3
"""Drive one meta.ai prompt from outside the page.  meta.py <video|image> <lskey|none> <prompt-file> [timeout]
Attaches localStorage master <lskey> (or nothing), pastes the prompt, sends, waits for a new clip/image or refusal."""
import sys, time, json, re, subprocess
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cjs import run
TAB = "645346540"
REFUSE = re.compile(r"can.t make|can’t make|not able to|couldn.t attach|can no longer access|I can.t help|can.t create|can’t create|unable to", re.I)
OVER = re.compile(r"media service is overloaded|try again in a little while|could not be generated right now|couldn.t be generated right now|returning no video|Something went wrong. Please try again|try again later|couldn.t attach the image. Want me to make it again", re.I)
def reload():
    subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to reload tab id 645346540 of window id 645343510'])
    time.sleep(8)
    for _ in range(40):
        try:
            if run(TAB, "document.querySelectorAll('[contenteditable=true]').length") != "0": break
        except SystemExit: pass
        time.sleep(5)
    time.sleep(6); run(TAB, open(__file__.rsplit('/', 1)[0] + "/meta_helpers.js").read()); run(TAB, "window.__st2()"); time.sleep(3)
def js(c):
    for _ in range(5):
        try: return run(TAB, c)
        except SystemExit as e: time.sleep(6)
    return ""
STOP = "[...document.querySelectorAll('button')].some(b=>b.getAttribute('aria-label')==='Stop')"
def st():
    try: return json.loads(js("window.__st2()"))
    except Exception:
        js(open(__file__.rsplit('/', 1)[0] + "/meta_helpers.js").read()); return json.loads(js("window.__st2()"))
SKIP = set()
def dup(url):
    """EP.11: after a reload an OLD clip can come back under another URL path (t39 -> t58); compare the bytes with every clip on disk."""
    import glob, hashlib, urllib.request
    u = url.split("?")[0]
    if u in SKIP: return True
    try: h = hashlib.md5(urllib.request.urlopen(url, timeout=60).read()).hexdigest()
    except Exception: return True
    if any(hashlib.md5(open(f, "rb").read()).hexdigest() == h for f in glob.glob("clips/*.mp4")+glob.glob("../pudding-ep*/masters/*.webp")+glob.glob("../pudding-ep*/thumb/*.webp")): SKIP.add(u); print("OLD MEDIA again, skipped", flush=True); return True
    return False
def wait(kind, before, text, limit=660):
    """Wait for a new clip/image. Reload every 4 min (a finished clip may not render); never resend while a reply is running (Stop button)."""
    fld = "last" if kind == "video" else "img"; k = text[-60:]; t0 = time.time(); rl = t0; dead = 0
    while time.time() - t0 < limit:
        time.sleep(5)
        if js("String(document.hidden)") != "false": subprocess.run(["sh", "tools/wait_visible.sh"]); reload(); t0 = rl = time.time()
        s = st()
        if s[fld] and s[fld].split("?")[0] != before and not dup(s[fld]):
            time.sleep(0 if kind == "video" else 10); s = st()
            print("NEW", int(time.time() - t0), "s", s[fld], flush=True); return [s[fld]]
        tail = s["tail"].split(k)[-1] if k in s["tail"] else s["tail"][-400:]
        if OVER.search(tail): print("OVERLOADED", int(time.time() - t0), "s", flush=True); return "OVER"
        if REFUSE.search(tail): print("REFUSAL?", int(time.time() - t0), "s", tail, flush=True); return None
        if time.time() - rl > 90 and js(STOP) == "false":  # EP.11: no reply running and nothing came back -> the reply was lost
            dead += 1
            if dead >= 2: print("LOST REPLY", int(time.time() - t0), "s", flush=True); return "OVER"
        if time.time() - rl > 90: print("reload", int(time.time() - t0), js(STOP), flush=True); reload(); rl = time.time()
    print("TIMEOUT", st()["tail"][-250:], flush=True); js("[...document.querySelectorAll('button')].find(b=>b.getAttribute('aria-label')==='Stop')?.click();1"); time.sleep(5); reload()
    return "OVER"
def go(kind, key, text, timeout=240, resume=False):
    subprocess.run(["sh", "tools/wait_visible.sh"])
    js(open(__file__.rsplit('/', 1)[0] + "/meta_helpers.js").read())
    fld = "last" if kind == "video" else "img"
    if js("window.__edText()").strip() or js("String([...document.querySelectorAll('img')].filter(i=>(i.src||'').startsWith('blob:')).length)") not in ("0", ""): reload()  # an unsent prompt + attachment is left in the composer -> reload clears both
    before = st()[fld].split("?")[0]
    if resume:  # the running/finished reply is compared with the last downloaded clip
        before = open("clips/urls.txt").read().strip().splitlines()[-1].split("\t")[1].split("?")[0]
        return wait(kind, before, text)
    for _ in range(60):  # never send while an earlier reply is running
        if js(STOP) != "true": break
        time.sleep(10)
    else: js("[...document.querySelectorAll('button')].find(b=>b.getAttribute('aria-label')==='Stop')?.click();1"); time.sleep(5)
    before = st()[fld].split("?")[0]
    if key != "none":
        fl = ",".join(f"window.__lsFile('{k}','{k.replace('__ep12_','').replace('__ep11_','').replace('__ep10_','').replace('__ep9_','').replace('__ep8_','').replace('__ep7_','').replace('__ep6_','')}_master.webp')" for k in key.split('+'))
        js(f"window.__attach([{fl}])"); time.sleep(6)
        print('previews', js("[...document.querySelectorAll('img')].filter(i=>(i.src||'').startsWith('blob:')||(i.src||'').startsWith('data:image')).length+' blob'"), flush=True)
    r = js("window.__paste(" + json.dumps(text) + ")"); time.sleep(1.5)
    got = js("window.__edText()")
    if got.strip() != text.strip(): print("PASTE MISMATCH", r, len(got), len(text), flush=True); reload(); return "OVER"
    time.sleep(1); print(js("window.__go()"), flush=True)
    return wait(kind, before, text)
if __name__ == "__main__":
    kind, key, pf = sys.argv[1:4]
    go(kind, key, open(pf).read().strip(), int(sys.argv[4]) if len(sys.argv) > 4 else 240)
