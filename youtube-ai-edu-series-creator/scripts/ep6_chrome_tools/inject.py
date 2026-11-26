#!/usr/bin/env python3
"""Put a local image into meta.ai localStorage as base64 WebP (1280 px, q85).  inject.py <tabkey> <png> <lskey>
Prints the SHA-256 check. The page then attaches it with window.__lsFile(lskey, name)."""
import sys, io, base64, hashlib, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cjs import run
from PIL import Image
tab, png, key = sys.argv[1:4]
im = Image.open(png).convert("RGB"); im.thumbnail((1280, 1280))
buf = io.BytesIO(); im.save(buf, "WEBP", quality=85); raw = buf.getvalue()
b64 = base64.b64encode(raw).decode(); sha = hashlib.sha256(raw).hexdigest()
run(tab, "window.__b64=[];1")
for i in range(0, len(b64), 60000):
    run(tab, f"window.__b64.push('{b64[i:i+60000]}');window.__b64.length")
run(tab, f"localStorage.setItem('{key}', window.__b64.join(''));window.__sha=null;"
         f"crypto.subtle.digest('SHA-256', Uint8Array.from(atob(localStorage.getItem('{key}')), c=>c.charCodeAt(0))).then(h=>window.__sha=[...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join(''));1")
time.sleep(1)
got = run(tab, "window.__sha")
print(png, im.size, len(raw), "bytes", "SHA OK" if got == sha else f"SHA MISMATCH {got} vs {sha}")
