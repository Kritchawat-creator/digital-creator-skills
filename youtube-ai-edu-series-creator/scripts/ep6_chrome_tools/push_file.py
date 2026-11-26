#!/usr/bin/env python3
"""Send a local file into a Chrome tab as window.__fileParts (Uint8Array chunks) and verify SHA-256.
push_file.py <tab-id> <path> [chunk_bytes]"""
import sys, base64, hashlib, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cjs import run
tab, path = sys.argv[1], sys.argv[2]; cs = int(sys.argv[3]) if len(sys.argv) > 3 else 1_500_000
data = open(path, 'rb').read(); sha = hashlib.sha256(data).hexdigest()
run(tab, "window.__fileParts=[];1"); t0 = time.time()
for i in range(0, len(data), cs):
    b = base64.b64encode(data[i:i+cs]).decode()
    n = run(tab, f"window.__fileParts.push(Uint8Array.from(atob('{b}'),c=>c.charCodeAt(0)));window.__fileParts.length")
    if (i // cs) % 10 == 0: print(n, f"{(i+cs)/len(data):.0%}", f"{time.time()-t0:.0f}s", flush=True)
run(tab, "window.__fsha=null;new Blob(window.__fileParts).arrayBuffer().then(a=>crypto.subtle.digest('SHA-256',a)).then(h=>window.__fsha=[...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join(''));1")
for _ in range(30):
    time.sleep(2); got = run(tab, "window.__fsha")
    if got and got != "null": break
print("bytes", len(data), "SHA OK" if got == sha else f"SHA MISMATCH {got} {sha}", f"{time.time()-t0:.0f}s")
