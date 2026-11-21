"""Scene-consistency montage: one labelled frame per clip (NAME@SECONDS ...) tiled 4 wide -> build/montage_<tag>.png."""
import subprocess, sys, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
ff = imageio_ffmpeg.get_ffmpeg_exe()
tag, items = sys.argv[1], sys.argv[2:]
tiles = []
for it in items:
    name, t = it.split("@")
    out = f"build/mf_{name}.png"
    subprocess.run([ff, "-v", "error", "-y", "-ss", t, "-i", f"clips/{name}.mp4", "-frames:v", "1", "-vf", "scale=480:-1", out], check=True)
    im = Image.open(out).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 150, 30], fill=(0, 0, 0))
    d.text((6, 4), it, fill=(255, 255, 255), font=ImageFont.truetype("fonts/Nunito[wght].ttf", 20))
    tiles.append(im)
cols = 4
rows = (len(tiles) + cols - 1) // cols
w, h = tiles[0].size
sheet = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
for i, im in enumerate(tiles):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(f"build/montage_{tag}.png")
print(f"build/montage_{tag}.png")
