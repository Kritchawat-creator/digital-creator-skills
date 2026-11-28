"""EP.8 (EP.7 lesson: Ivy's false start "deca- deca- decorations" passed whisper whole + halves and splitcheck; the automatic captions caught it
after upload). For every unique clip window of build.py (or the windows given as NAME:in:out):
  1. whisper-cli -ml 1 (word timestamps): flag any word longer than LONG s, any fragment ending in '-', any word not in the subtitle, any word said
     more often than in the subtitle;
  2. 0.8 s probe windows centred on every word of >= 6 letters: flag a probe that hears a fragment / a repeated prefix / a word twice.
Run from the episode folder:  python3 tools/wordcheck.py            (all windows of build.py)
                              python3 tools/wordcheck.py T01:1.0:2.9 (one window)
Prints one line per window + the probes; 'windows N flagged M' at the end. Read every flagged line (a flag is a lead, not a verdict)."""
import sys, re, subprocess, importlib.util
MODEL = "/Users/kritchawatpattharawiwatkul/.cache/whisper/ggml-small.bin"
LONG = 0.9  # and > 0.1 s per letter + 0.2 (EP.7: stuttered 'decorations' 1.51 s flagged, clean 0.92 s passes)
W = lambda t: re.findall(r"[a-z0-9']+-?", (t or "").lower().replace("’", "'"))


def wav(n, a, c, out="build/wc.wav"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(max(0, a)), "-to", str(c), "-i", f"clips/{n}.mp4", "-ac", "1", "-ar", "16000", out], check=True)
    return out


def words(path):
    r = subprocess.run(["whisper-cli", "-m", MODEL, "-f", path, "-l", "en", "-ml", "1", "-np"], capture_output=True, text=True).stdout
    out = []
    for m in re.finditer(r"\[(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)\]\s*(.*)", r):
        t0 = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]); t1 = int(m[4]) * 3600 + int(m[5]) * 60 + float(m[6])
        w = m[7].strip()
        if w and not w.startswith("[") and not w.startswith("("):
            out.append((t0, t1, w))
    return out


def plain(path):
    r = subprocess.run(["whisper-cli", "-m", MODEL, "-f", path, "-l", "en", "-nt", "-np"], capture_output=True, text=True).stdout
    return " ".join(r.split())


def check(n, a, c, sub):
    ws = words(wav(n, a, c))
    sw = W(sub)
    flags = []
    heard = [x for _, _, w in ws for x in W(w)]
    for t0, t1, w in ws:
        lw = W(w)
        nl = len(re.sub(r"[^a-z]", "", w.lower()))
        if t1 - t0 > max(LONG, 0.1 * nl + 0.2) and nl > 1: flags.append(f"LONG {w}:{t1 - t0:.2f}s@{t0:.2f}")
        if w.rstrip(".,!?").endswith("-"): flags.append(f"FRAGMENT {w}@{t0:.2f}")
    for x in set(heard):
        if sw and x not in sw and not x.isdigit(): flags.append(f"EXTRA {x}")
        if heard.count(x) > max(1, sw.count(x)): flags.append(f"REPEAT {x}x{heard.count(x)}")
    probes = []
    for t0, t1, w in ws:
        core = re.sub(r"[^a-z]", "", w.lower())
        mid = a + (t0 + t1) / 2
        if len(core) >= 6 and mid - 0.4 < c - 0.2:  # EP.10: whisper can time a last word past the window end -> no probe there (ffmpeg -to < -ss crashed)
            p = plain(wav(n, mid - 0.4, min(c, mid + 0.4), "build/wcp.wav"))
            pw = W(p)
            bad = any(x.endswith("-") for x in pw) or any(pw.count(x) > 1 for x in pw) or (len(pw) >= 2 and any(pw[i + 1].startswith(pw[i]) and pw[i] != pw[i + 1] for i in range(len(pw) - 1)))
            probes.append(f"{core}@{mid:.2f}:'{p}'" + (" <<<" if bad else ""))
            if bad: flags.append(f"PROBE {core}")
    line = " ".join(f"{w}[{t1 - t0:.2f}]" for t0, t1, w in ws)
    print(f"{n} {a}-{c} | SUB {sub} | WORDS {line} | PROBES {' ; '.join(probes)}" + (f" <<< {' '.join(flags)}" if flags else ""), flush=True)
    return bool(flags)


if __name__ == "__main__":
    seen = {}
    if len(sys.argv) > 1:
        for x in sys.argv[1:]:
            n, a, c = x.split(":"); seen[(n, float(a), float(c))] = ""
    else:
        sys.argv = ["build.py", "plan"]
        spec = importlib.util.spec_from_file_location("b", "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
        for s in b.SEGS:
            if s["kind"] == "clip": seen.setdefault((s["name"], s["t_in"], s["t_out"]), s["sub"] or "")
            elif s.get("voice"): vc, va, vb, _ = s["voice"]; seen.setdefault((vc, va, vb), s.get("srt") or "")
    bad = sum(check(n, a, c, sub) for (n, a, c), sub in seen.items())
    print("windows", len(seen), "flagged", bad)
