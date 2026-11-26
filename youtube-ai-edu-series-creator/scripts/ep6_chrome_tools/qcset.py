#!/usr/bin/env python3
"""qcset.py NAME:START:END[:CROP] ... -> ASR of each window + stacked 10-frame sheet + 5 fps strip -> build/rev.png"""
import subprocess, sys
from PIL import Image
P = "640:540:20:130"; R = "700:480:560:20"; L = "640:420:320:80"; H = "560:420:360:60"
DEF = {"P": P, "R": R, "L": L, "N": R, "H": H, "O": "700:600:140:120"}
ims = []
for it in sys.argv[1:]:
    f = it.split(":", 3); n, s, e = f[:3]; crop = f[3] if len(f) > 3 else DEF[n[0]]
    print(subprocess.run(["sh", "tools/asr.sh", n, s, e], capture_output=True, text=True).stdout.strip())
    subprocess.run(["python3", "zoom2.py", n, s, e, crop], check=True)
    ims += [Image.open(f"build/qc_{n}.png").convert("RGB"), Image.open(f"build/zoom_{n}.png").convert("RGB")]
W = 1600; ims = [i.resize((W, int(i.height * W / i.width))) for i in ims]
o = Image.new("RGB", (W, sum(i.height for i in ims))); y = 0
for i in ims: o.paste(i, (0, y)); y += i.height
o.save("build/rev.png")
