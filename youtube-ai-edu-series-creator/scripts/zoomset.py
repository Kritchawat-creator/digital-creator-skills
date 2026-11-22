"""Stacked 5 fps face strips: python3 zoomset.py OUT CROP NAME:START:END ... -> build/OUT.png (scaled 0.6)"""
import subprocess, sys
from PIL import Image
out, crop, items = sys.argv[1], sys.argv[2], sys.argv[3:]
strips = []
for it in items:
    n, s, e = it.split(":")
    subprocess.run(["python3", "zoom2.py", n, s, e, crop], check=True)
    strips.append(Image.open(f"build/zoom_{n}.png").copy())
w = max(i.width for i in strips); o = Image.new("RGB", (w, sum(i.height + 10 for i in strips)), "white"); y = 0
for i in strips: o.paste(i, (0, y)); y += i.height + 10
o.resize((o.width * 6 // 10, o.height * 6 // 10)).save(f"build/{out}.png")
