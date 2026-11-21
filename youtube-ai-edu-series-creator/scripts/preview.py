"""Story preview: every accepted cut in story order, crops applied, labelled. -> out/ep4_story_preview.mp4"""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
RANK = "1024:576:0:144"; WHEEL = "768:432:470:40"
order = [("R01",1.3,4.1,RANK),("R02",0.9,2.7,None),("R03",2.7,4.4,RANK),("R04b",0.1,3.4,RANK),("R05",1.8,6.2,RANK),
         ("R06c",0.8,5.2,None),("K01b",4.8,6.4,None),("K02",3.6,5.4,WHEEL),("K03",1.5,5.6,None),("K04",2.9,6.5,WHEEL),
         ("K05",4.0,7.4,None),("K06b",1.7,6.0,None),("K07",1.6,2.7,None),("K08",0.5,5.2,WHEEL),("Z01",2.9,5.7,None),
         ("Z02b",1.6,7.0,None),("H1",0.6,2.9,None),("H1",6.7,9.0,None)]
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
os.makedirs("build/prev", exist_ok=True); parts = []
for k, (n, s, e, crop) in enumerate(order):
    lab = f"build/prev/l{k}.png"; im = Image.new("RGBA", (1280, 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    t = f"{n}  {s:.1f}-{e:.1f}" + ("  (crop)" if crop else ""); w = d.textlength(t, font=f)
    d.rectangle((10, 6, 30 + w, 46), fill=(0, 0, 0, 150)); d.text((20, 10), t, font=f, fill="white"); im.save(lab)
    vf = (f"crop={crop}," if crop else "") + "scale=1280:720,setsar=1,fps=30"
    out = f"build/prev/p{k}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s), "-t", f"{e-s:.2f}", "-i", f"clips/{n}.mp4", "-i", lab,
                    "-filter_complex", f"[0:v]{vf}[b];[b][1:v]overlay=0:8,format=yuv420p[v];[0:a]aresample=48000,loudnorm=I=-16:TP=-1.5[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-c:a", "pcm_s16le", out.replace(".mp4", ".mov")], check=True)
    parts.append(out.replace(".mp4", ".mov"))
with open("build/prev/list.txt", "w") as fh:
    fh.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "build/prev/list.txt", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k", "out/ep4_story_preview.mp4"], check=True)
print("ok", len(parts))
