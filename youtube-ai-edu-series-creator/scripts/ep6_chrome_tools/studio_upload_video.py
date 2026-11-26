#!/usr/bin/env python3
"""Upload a video file to YouTube Studio from the owner's Chrome, without a drag (owner rule, 2026-11-24).

Usage (from the episode folder, with cjs.py + push_file.py next to this file in tools/):
    python3 tools/studio_upload_video.py <studio-tab-id> out/<episode>.mp4

Before running: open studio.youtube.com/channel/<channel id>/videos/upload?d=ud in that tab (the "Upload videos"
dialog with its "Select files" button). Steps:
  1. push_file.py sends the file into the page as Uint8Array chunks (1.5 MB base64 per AppleScript call, ~1.2 MB/s)
     and checks SHA-256 in the page (EP.7: 76 MB in 62 s).
  2. A File built from those chunks goes into the dialog's input[type=file] through DataTransfer + "change".
  3. Waits for the details step and prints the video link, the Filename field and the upload progress.
"""
import json
import subprocess
import sys
import time

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cjs import run  # noqa: E402

tab, path = sys.argv[1], sys.argv[2]
name = path.rsplit('/', 1)[-1]
r = subprocess.run([sys.executable, __file__.rsplit('/', 1)[0] + '/push_file.py', tab, path], capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)
if 'SHA OK' not in r.stdout:
    raise SystemExit('bytes did not arrive intact; not injecting')
print(run(tab, """(()=>{const inp=[...document.querySelectorAll('ytcp-uploads-dialog input[type=file], ytcp-uploads-file-picker input[type=file], input[type=file]')][0];
if(!inp)return 'NO FILE INPUT: open /videos/upload?d=ud first';
const f=new File(window.__fileParts,%s,{type:'video/mp4'});const dt=new DataTransfer();dt.items.add(f);inp.files=dt.files;
inp.dispatchEvent(new Event('change',{bubbles:true}));window.__fileParts=null;return 'injected '+f.size})()""" % json.dumps(name)))
for _ in range(20):
    time.sleep(3)
    out = run(tab, """(()=>{const d=document.querySelector('ytcp-uploads-dialog');if(!d)return '';
const a=[...d.querySelectorAll('a')].map(a=>a.href).filter(h=>/youtu\\.be\\//.test(h));
const fn=[...d.querySelectorAll('*')].find(e=>e.children.length==0&&/^Filename$/.test(e.textContent.trim()));
const p=(d.querySelector('ytcp-video-upload-progress')||{textContent:''}).textContent.replace(/\\s+/g,' ').trim();
return a.length?JSON.stringify({link:a[0],filename:fn?fn.parentElement.textContent.replace('Filename','').trim():'',progress:p}):''})()""")
    if out:
        print(out)
        break
else:
    print('no video link yet: check the dialog')
