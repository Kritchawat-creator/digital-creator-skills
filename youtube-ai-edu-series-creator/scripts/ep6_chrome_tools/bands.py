#!/usr/bin/env python3
"""bands.py CLIP a b [a b ...] -> mean dB in 4 bands per window (tells birdsong/ambience from music/voice)."""
import sys, subprocess, re
c = sys.argv[1]; w = sys.argv[2:]
for i in range(0, len(w), 2):
    a, b = w[i], w[i + 1]; out = []
    for lo, hi in [(100, 400), (400, 1500), (1500, 4000), (4000, 10000)]:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", a, "-to", b, "-i", f"clips/{c}.mp4", "-af", f"highpass=f={lo},lowpass=f={hi},volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        m = re.search(r"mean_volume: (-?[\d.]+)", r); out.append(f"{lo}-{hi}:{m.group(1) if m else '?'}")
    print(c, a, b, " ".join(out))
