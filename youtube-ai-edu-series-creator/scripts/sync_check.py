"""Sync QC for the assembled episode.
  drift [file]  cross-correlate (Pearson, +-1.5 s) each clip segment's speech envelope in the assembled file with its
                source clip; prints the audio offset in ms and the correlation. Offsets must stay near 0 to the end.
  cues          print each cued clip's speech timeline from its in point with the subtitle cue starts marked.
  windows       every clip window and every card voice window from build.SEGS: speech line per window, and a flag
                when a window has no speech (wrong in/out) or speech in its first/last 100 ms (word cut off).
Run from the episode folder: python sync_check.py drift build/body.mov"""
import array, math, subprocess, sys
import imageio_ffmpeg
import build as B
ff = imageio_ffmpeg.get_ffmpeg_exe()
SR, HOP, PAD = 8000, 80, 150  # 10 ms envelope, +-1.5 s search


def env(path, ss, dur):
    pre = min(ss, 0.0)
    raw = subprocess.run([ff, "-v", "error", "-ss", f"{max(ss, 0)}", "-t", f"{dur + pre}", "-i", path, "-ac", "1", "-ar", str(SR),
                          "-af", "highpass=f=250,lowpass=f=3500", "-f", "s16le", "-"], capture_output=True).stdout
    a = array.array("h", raw)
    e = [math.sqrt(sum(x * x for x in a[i:i + HOP]) / HOP) for i in range(0, len(a) - HOP, HOP)]
    return [0.0] * int(round(-pre * 100)) + e


def pearson(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((v - mx) ** 2 for v in x)); sy = math.sqrt(sum((v - my) ** 2 for v in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy + 1e-9)


mode = sys.argv[1] if len(sys.argv) > 1 else "drift"
target = sys.argv[2] if len(sys.argv) > 2 else "build/body.mov"
if mode == "drift":
    t, worst = 0.0, 0
    for i, s in enumerate(B.SEGS):
        if s["kind"] == "clip" and s["dur"] >= 1.0:
            ref = env(f"clips/{s['name']}.mp4", s["t_in"], s["dur"])
            got = env(target, t - PAD / 100, s["dur"] + 2 * PAD / 100)
            best = max(((pearson(ref, got[o:o + len(ref)]), o) for o in range(0, 2 * PAD) if len(got[o:o + len(ref)]) == len(ref)))
            off = (best[1] - PAD) * 10
            worst = max(worst, abs(off)) if best[0] > 0.6 else worst
            print(f"seg {i:03d} {s['name']:8s} at {t:6.1f}s  audio offset {off:+5d} ms  r={best[0]:.2f}")
        t += s["dur"]
    print(f"WORST |offset| (r>0.6): {worst} ms")
elif mode == "windows":
    # EP3: H1/H4 second takes were cut from the wrong row of the RMS timeline (silent / truncated); this catches it.
    wins, bad = [], 0
    for i, s in enumerate(B.SEGS):
        if s["kind"] == "clip":
            wins.append((i, s["name"], s["t_in"], s["dur"]))
        elif s.get("voice"):
            vc, va, vb, _at = s["voice"]
            wins.append((i, vc + " (voice)", va, vb - va))
    for i, name, a, d in wins:
        e = env(f"clips/{name.split()[0]}.mp4", a, d)
        v = [20 * math.log10((sum(e[k:k + 10]) / 10 or 1) / 32768) for k in range(0, len(e) - 9, 10)]
        ref = env(f"clips/{name.split()[0]}.mp4", 0, 10)
        rv = [20 * math.log10((sum(ref[k:k + 10]) / 10 or 1) / 32768) for k in range(0, len(ref) - 9, 10)]
        fl = sorted(rv)[len(rv) // 5]  # floor from the whole clip, not the window
        line = "".join("#" if x > fl + 12 else "+" if x > fl + 6 else "." for x in v)
        flag = "NO SPEECH" if "#" not in line else ("CUT START" if line[:1] == "#" else ("CUT END" if line[-1:] == "#" else ""))
        bad += bool(flag)
        print(f"seg {i:03d} {name:12s} {a:4.1f}+{d:3.1f}  {line:30s} {flag}")
    print(f"windows flagged: {bad}")
else:
    seen = set()
    for s in B.SEGS:
        if s["kind"] != "clip" or not s.get("cues") or (s["name"], s["t_in"]) in seen:
            continue
        seen.add((s["name"], s["t_in"]))
        e = env(f"clips/{s['name']}.mp4", s["t_in"], s["dur"])
        v = [20 * math.log10((sum(e[k:k + 10]) / 10 or 1) / 32768) for k in range(0, len(e) - 9, 10)]
        fl = sorted(v)[len(v) // 5]
        line = "".join("#" if x > fl + 12 else "+" if x > fl + 6 else "." for x in v)
        marks = [" "] * (len(line) + 1)
        for a, b, en, _ in s["cues"]:
            marks[min(len(line), int(round(a * 10)))] = "^"
        print(f"{s['name']:8s} in={s['t_in']} dur={s['dur']:.1f}\n   {line}\n   {''.join(marks)}  " + " | ".join(f"{a:.1f} {en}" for a, b, en, _ in s["cues"]))
