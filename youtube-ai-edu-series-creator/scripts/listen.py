"""Owner listen check (Mac): python3 listen.py LIST OUT.mp4 ; LIST lines = CLIP|in|out|label. Each part shows a number,
clip, window and the expected line, then plays the window at -16 LUFS."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
lst, out = sys.argv[1], sys.argv[2]
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
os.makedirs("build/listen", exist_ok=True); parts = []
for k, line in enumerate(l for l in open(lst, encoding="utf-8").read().splitlines() if l.strip()):
    n, s, e, label = line.split("|", 3); s, e = float(s), float(e)
    lab = f"build/listen/l{k}.png"; im = Image.new("RGBA", (1280, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for j, t in enumerate([f"{k + 1}. {n}  {s:.1f}-{e:.1f}s", label]):
        w = d.textlength(t, font=f); d.rectangle((10, 6 + j * 50, 30 + w, 50 + j * 50), fill=(0, 0, 0, 170)); d.text((20, 10 + j * 50), t, font=f, fill="white")
    im.save(lab); p = f"build/listen/p{k}.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(max(0, s - 0.3)), "-t", f"{e - s + 1.0:.2f}", "-i", f"clips/{n}.mp4", "-i", lab,
                    "-filter_complex", "[0:v]scale=1280:720,setsar=1,fps=30[b];[b][1:v]overlay=0:6,format=yuv420p[v];[0:a]aresample=48000,loudnorm=I=-16:TP=-1.5,apad=pad_dur=0.6[a]",
                    "-map", "[v]", "-map", "[a]", "-shortest", "-c:v", "libx264", "-crf", "20", "-c:a", "pcm_s16le", p], check=True)
    parts.append(p)
with open("build/listen/list.txt", "w") as fh:
    fh.writelines(f"file '{os.path.abspath(p)}'\n" for p in parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "build/listen/list.txt", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", out], check=True)
print("ok", len(parts), out)
