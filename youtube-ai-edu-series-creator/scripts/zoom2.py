"""Face strip: python3 zoom2.py NAME START END CROP -> build/zoom_NAME.png (5 fps)"""
import subprocess, sys
from io import BytesIO
from PIL import Image, ImageDraw
name, s, e, crop = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
ims = []; t = s
while t <= e + 1e-6:
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", f"clips/{name}.mp4", "-frames:v", "1",
                          "-vf", f"crop={crop},scale=200:-1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    if png: ims.append((t, Image.open(BytesIO(png)).convert("RGB")))
    t += 0.2
w, h = ims[0][1].size; cols = 10
o = Image.new("RGB", (w * cols, (h + 14) * ((len(ims) + cols - 1) // cols)), "white"); d = ImageDraw.Draw(o)
for k, (t, im) in enumerate(ims):
    x, y = (k % cols) * w, (k // cols) * (h + 14); o.paste(im, (x, y + 14)); d.text((x + 2, y + 1), f"{t:.1f}", fill="black")
o.save(f"build/zoom_{name}.png")
