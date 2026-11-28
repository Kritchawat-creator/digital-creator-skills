#!/usr/bin/env python3
"""Back up a meta.ai localStorage key to masters/_ls_backup/<key>.webp (chunked read), print sha + size. lsbackup.py <tab> <key>"""
import sys, base64, hashlib
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cjs import run
tab, key = sys.argv[1:3]
n = int(run(tab, f"(localStorage.getItem('{key}')||'').length"))
parts = [run(tab, f"localStorage.getItem('{key}').slice({i},{i+60000})") for i in range(0, n, 60000)]
b64 = "".join(parts); assert len(b64) == n, (len(b64), n)
raw = base64.b64decode(b64); open(f"masters/_ls_backup/{key}.webp", "wb").write(raw)
js_sha = None
print(key, n, "chars", len(raw), "bytes sha", hashlib.sha256(raw).hexdigest()[:16])
