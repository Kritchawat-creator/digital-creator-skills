"""One frame (middle of the window, crop applied) per unique clip window of build.py -> build/grid.png"""
import sys, subprocess, importlib.util
from PIL import Image, ImageDraw
sys.argv = ["build.py", "plan"]
spec = importlib.util.spec_from_file_location("b", "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
seen = []
for s in b.SEGS:
    if s["kind"] == "clip":
        k = (s["name"], s["t_in"], s["t_out"], s.get("crop"))
        if k not in seen: seen.append(k)
W, H = 384, 216; cols = 6; rows = (len(seen) + cols - 1) // cols
g = Image.new("RGB", (cols * W, rows * (H + 18)), "white"); d = ImageDraw.Draw(g)
for i, (n, a, c, crop) in enumerate(seen):
    vf = (f"crop={crop}," if crop else "") + f"scale={W}:{H}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str((a + c) / 2), "-i", f"clips/{n}.mp4", "-frames:v", "1", "-vf", vf, "build/_g.png"])
    x, y = (i % cols) * W, (i // cols) * (H + 18)
    g.paste(Image.open("build/_g.png"), (x, y + 18)); d.text((x + 4, y + 3), f"{n} {a}-{c}", fill="black")
g.save("build/grid.png"); print(len(seen), "windows")
