"""f0g.py clip a b ... -> median f0 (pure Python, octave guard as f0np.py: prefer 2x/3x lag when nearly as good), 8 kHz, 70-450 Hz, voiced frames."""
import subprocess, array, math, sys
def f0(path, a, b):
    raw = subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i',path,'-ac','1','-ar','8000','-af','highpass=f=60,lowpass=f=1000','-f','s16le','-'],capture_output=True).stdout
    x = array.array('h', raw); N = 320; out = []
    E = [sum(v*v for v in x[i:i+N]) for i in range(0, len(x)-N-120, 160)]; thr = max(E)*0.08
    lo, hi = int(8000/450), int(8000/70)
    for k, e in enumerate(E):
        if e < thr: continue
        s = x[k*160:k*160+N+hi]
        if len(s) < N+hi: break
        m = sum(s[:N])/N; s = [v-m for v in s]
        def ac(l):
            c = sum(s[i]*s[i+l] for i in range(N)); n = math.sqrt(sum(s[i]**2 for i in range(N))*sum(s[i+l]**2 for i in range(N)) or 1); return c/n
        sc = [(ac(l), l) for l in range(lo, hi)]; best, lag = max(sc)
        for mul in (2, 3):
            if lag*mul < hi and ac(lag*mul) > 0.85*best: lag = lag*mul
        if best > 0.6: out.append(8000/lag)
    out.sort(); n = len(out)
    return f"median {out[n//2]:.0f} Hz (p25 {out[n//4]:.0f} p75 {out[3*n//4]:.0f}) n={n}" if n else "none"
a = sys.argv[1:]
for k in range(0, len(a), 3): print(a[k], a[k+1], a[k+2], f0(a[k], float(a[k+1]), float(a[k+2])))
