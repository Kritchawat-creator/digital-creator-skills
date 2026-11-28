"""EP.3: redo only build.py's last step (two-pass loudnorm + limiter + AAC) from build/mix.mov with a lower limiter ceiling.
Render 1 measured -0.3 dBTP (inter-sample overs after AAC) with limit=0.79; EP.2 was -1.6 with the same chain."""
import json, subprocess, sys
LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 0.70
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", "build/mix.mov", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/mix.mov", "-map", "0:v", "-map", "0:a", "-af", f"{ln},alimiter=limit={LIM}:level=false:attack=3:release=60,aresample=48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/family_ep03.mp4"], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", "out/family_ep03.mp4", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
s = r[r.rindex("Summary"):]
print("limit", LIM, " ".join(l.strip() for l in s.splitlines() if l.strip().startswith(("I:", "Peak:"))))
