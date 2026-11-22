"""Voiced-frame detector: one char per 40 ms frame. V = clear pitch (80-450 Hz), u = unvoiced sound, . = quiet.
Solid VVVV runs = a real voice; scattered V = breath / whisper. usage: python3 -I voicing.py clips/NAME.mp4"""
import shutil
import array
import subprocess
import sys



ff = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
SR, N = 16000, 640
raw = subprocess.run([ff, "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                     capture_output=True).stdout
a = array.array("h", raw)
out = []
for i in range(0, len(a) - N, N):
    x = a[i:i + N]
    e = sum(v * v for v in x)
    if e < 4e4 * N:
        out.append(".")
        continue
    best = 0.0
    for lag in range(SR // 450, SR // 80):
        c = sum(x[k] * x[k + lag] for k in range(0, N - lag, 2))
        best = max(best, c / (e / 2))
    out.append("V" if best > 0.55 else "u")
s = "".join(out)
print(sys.argv[1])
for k in range(0, len(s), 50):
    print(f"{k * 0.04:5.1f}s {s[k:k + 50]}")
