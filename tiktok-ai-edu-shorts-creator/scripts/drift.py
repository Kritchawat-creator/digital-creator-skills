"""A/V drift check on the DELIVERED file, after build.sh. Run from the episode folder:
  python3 -I drift.py out/roughcut.mp4
Per edl.tsv segment, cross-correlates the speech-band envelope of the cut (at the segment offset, using the
build/seg video durations) with the source clip window (same 24 fps frame alignment as build.sh), +-0.5 s search.
Expect 0 ms on every segment with r > 0.6."""
import shutil
import array, math, subprocess, sys
FF = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"; SR, HOP, PAD = 8000, 80, 50
def env(path, ss, dur):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{max(ss,0):.3f}", "-t", f"{dur:.3f}", "-i", path, "-ac", "1", "-ar", str(SR),
        "-af", "highpass=f=250,lowpass=f=3500", "-f", "s16le", "-"], capture_output=True).stdout
    a = array.array("h", raw)
    return [math.sqrt(sum(x*x for x in a[i:i+HOP])/HOP) for i in range(0, len(a)-HOP, HOP)]
def pearson(x, y):
    n=len(x); mx, my = sum(x)/n, sum(y)/n
    sx=math.sqrt(sum((v-mx)**2 for v in x)); sy=math.sqrt(sum((v-my)**2 for v in y))
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(sx*sy+1e-9)
target = sys.argv[1]; rows=[l.rstrip("\n").split("\t") for l in open("edl.tsv")][1:]
segdur = lambda clip,i: float(subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=duration","-of","csv=p=0",f"build/seg/s{i:02d}_{clip}.mov"],capture_output=True,text=True).stdout)
t = 0.0; worst = 0
for i, r in enumerate(rows, 1):
    clip = r[0]; tin = round(float(r[1])*24)/24; d = round((float(r[2])-float(r[1]))*24)/24  # same frame alignment as build.sh
    ref = env(f"clips/{clip}.mp4", tin, d)
    got = [0.0]*max(0, PAD - int(t*100)) + env(target, t - PAD/100, d + 2*PAD/100)
    best = max((pearson(ref, got[o:o+len(ref)]), o) for o in range(0, 2*PAD) if len(got[o:o+len(ref)]) == len(ref))
    off = (best[1]-PAD)*10; worst = max(worst, abs(off)) if best[0] > 0.6 else worst
    print(f"seg {i} {clip:6s} at {t:6.2f}s  offset {off:+4d} ms  r={best[0]:.2f}")
    t += segdur(clip, i)
print(f"WORST |offset| (r>0.6): {worst} ms")
