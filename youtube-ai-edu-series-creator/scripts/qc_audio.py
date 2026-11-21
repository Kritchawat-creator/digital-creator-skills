"""Print a speech-band loudness timeline (dB per 100 ms) for a clip, to find who-speaks-when."""
import subprocess, sys, array, math, imageio_ffmpeg
ff = imageio_ffmpeg.get_ffmpeg_exe()
raw = subprocess.run([ff, "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "16000",
                      "-af", "highpass=f=250,lowpass=f=3500", "-f", "s16le", "-"],
                     capture_output=True).stdout
a = array.array("h", raw); step = 1600
vals = []
for i in range(0, len(a) - step, step):
    seg = a[i:i + step]; rms = math.sqrt(sum(x * x for x in seg) / step) or 1
    vals.append(20 * math.log10(rms / 32768))
floor = sorted(vals)[len(vals) // 5]
line = "".join("#" if v > floor + 12 else ("+" if v > floor + 6 else ".") for v in vals)
print(f"{sys.argv[1]} floor={floor:.1f}dB  (#=speech-loud, +=medium, .=quiet; 1 char=0.1s)")
for k in range(0, len(line), 50): print(f"{k/10:5.1f}s {line[k:k+50]}")
