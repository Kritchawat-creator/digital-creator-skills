"""EP.3: whisper every unique accepted clip window of build.py on the whole window AND two overlapping halves (EP.2 'have have' lesson).
Prints sub | whole | half A | half B, and flags a word that appears more often in the transcripts than in the subtitle."""
import sys, re, subprocess, json
sys.argv = ["build.py", "plan"]; import importlib.util
spec = importlib.util.spec_from_file_location("b", "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
seen = {}
for s in b.SEGS:
    if s["kind"] == "clip": seen.setdefault((s["name"], s["t_in"], s["t_out"]), s["sub"])
    elif s.get("voice"): vc, va, vb, _ = s["voice"]; seen.setdefault((vc, va, vb), s.get("srt"))
def asr(n, a, c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(c), "-i", f"clips/{n}.mp4", "-ac", "1", "-ar", "16000", "build/sc.wav"])
    r = subprocess.run(["whisper-cli", "-m", "/Users/kritchawatpattharawiwatkul/.cache/whisper/ggml-small.bin", "-f", "build/sc.wav", "-l", "en", "-nt", "-np"], capture_output=True, text=True)
    return " ".join(r.stdout.split())
W = lambda t: re.findall(r"[a-z']+", (t or "").lower())
bad = 0
for (n, a, c), sub in seen.items():
    m = round((a + c) / 2, 2); ov = 0.3
    whole, h1, h2 = asr(n, a, c), asr(n, a, m + ov), asr(n, m - ov, c)
    flag = ""
    sw = W(sub)
    for w in set(W(whole)):
        if W(whole).count(w) > max(1, sw.count(w)): flag += f" REPEAT?{w}"
    for w in set(sw):
        if w not in W(whole) + W(h1) + W(h2) and len(w) > 2: flag += f" MISSING?{w}"
    if flag: bad += 1
    print(f"{n} {a}-{c} | SUB {sub} | WHOLE {whole} | A {h1} | B {h2}{' <<<' + flag if flag else ''}", flush=True)
print("windows", len(seen), "flagged", bad)
