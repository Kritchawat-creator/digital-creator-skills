"""Render every text card of build.py before the render (EP.9: the cliff title wrapped). Flags any title/line that wraps onto 2+ lines,
writes build/cardcheck/cNNN.png and a contact sheet build/cardcheck.png."""
import sys, os, importlib.util
sys.argv = ["build.py", "plan"]
spec = importlib.util.spec_from_file_location("b", "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
from PIL import Image, ImageDraw
os.makedirs("build/cardcheck", exist_ok=True)
d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
outs, flags = [], []
for i, s in enumerate(b.SEGS):
    if s["kind"] != "card" or s.get("still") or not (s.get("title") or s.get("lines")): continue
    if s.get("title"):
        n = len(b.wrap(d, s["title"], b.font(b.BALOO, 112, 800), 1700))
        if n > 1: flags.append((i, "TITLE", s["title"], n))
    for t, c, sz in s.get("lines", []):
        n = len(b.wrap(d, t, b.font(b.NUNITO, sz, 850), 1640))
        if n > 1: flags.append((i, "LINE", t, n))
    p = f"build/cardcheck/c{i:03d}.png"; b.card_png(p, s.get("title"), s.get("lines", []), s.get("badge"), s.get("icon")); outs.append(p)
cols = 6; rows = (len(outs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 320, rows * 180), "white")
for k, p in enumerate(outs): sheet.paste(Image.open(p).resize((320, 180)), ((k % cols) * 320, (k // cols) * 180))
sheet.save("build/cardcheck.png")
print(len(outs), "cards;", "WRAPS:" if flags else "no wraps")
for f in flags: print(" ", f)
