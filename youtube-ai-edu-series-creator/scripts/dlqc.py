"""Download a Meta AI clip and QC it in one step (Mac).
Usage: python3 dlqc.py NAME URL
 -> clips/NAME.mp4, prints speech bursts (speech band 250-3000 Hz, 0.1 s windows, > floor+8 dB),
    writes build/qc_NAME.png (10 frames) for the contact-sheet check.
"""
import array, math, os, subprocess, sys, urllib.request
from io import BytesIO
from PIL import Image, ImageDraw

name, url = sys.argv[1], sys.argv[2]
os.makedirs("clips", exist_ok=True); os.makedirs("build", exist_ok=True)
clip = f"clips/{name}.mp4"
urllib.request.urlretrieve(url, clip)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip],
                           capture_output=True, text=True).stdout.strip() or 0)
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", clip, "-af", "highpass=f=250,lowpass=f=3000", "-ac", "1",
                      "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
a = array.array("h"); a.frombytes(pcm)
db = []
for i in range(0, len(a), 1600):
    s = a[i:i + 1600]
    r = math.sqrt(sum(x * x for x in s) / max(1, len(s))) / 32768
    db.append(20 * math.log10(r) if r > 0 else -99)
floor = sorted(db)[len(db) // 5]
bursts, start = [], None
for k, d in enumerate(db + [-99]):
    on = d > floor + 8
    if on and start is None: start = k
    if not on and start is not None:
        if k - start >= 2: bursts.append((start / 10, k / 10, max(db[start:k])))
        start = None
# merge bursts separated by < 0.3 s
merged = []
for b in bursts:
    if merged and b[0] - merged[-1][1] < 0.3: merged[-1] = (merged[-1][0], b[1], max(merged[-1][2], b[2]))
    else: merged.append(b)
print(f"{name}: {dur:.1f}s floor {floor:.0f} dB  bursts: " + ", ".join(f"{s:.1f}-{e:.1f}({p:.0f})" for s, e, p in merged))

tw, th = 384, 216
sheet = Image.new("RGB", (tw * 5, (th + 18) * 2), "white"); d = ImageDraw.Draw(sheet)
for k in range(10):
    t = 0.5 + k
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", clip, "-frames:v", "1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True).stdout
    if not png: continue
    im = Image.open(BytesIO(png)).convert("RGB").resize((tw, th))
    x, y = (k % 5) * tw, (k // 5) * (th + 18)
    sheet.paste(im, (x, y + 18)); d.text((x + 4, y + 3), f"{t:.1f}s", fill="black")
sheet.save(f"build/qc_{name}.png")
