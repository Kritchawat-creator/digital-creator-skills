import subprocess,array,math,sys
def f0(path,a,b):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i',path,'-ac','1','-ar','8000','-af','highpass=f=80,lowpass=f=900','-f','s16le','-'],capture_output=True).stdout
    x=array.array('h',raw); out=[]
    E=[sum(v*v for v in x[i:i+320]) for i in range(0,len(x)-320,160)]; thr=max(E)*0.06
    for k,e in enumerate(E):
        if e<thr: continue
        s=x[k*160:k*160+400]
        if len(s)<400: break
        best=(0,0); n0=sum(v*v for v in s[:260]) or 1
        for lag in range(16,100):
            c=sum(s[i]*s[i+lag] for i in range(260)); n=math.sqrt(n0*(sum(s[i+lag]**2 for i in range(260)) or 1))
            if c/n>best[0]: best=(c/n,lag)
        if best[0]>0.75: out.append(8000/best[1])
    out.sort(); n=len(out)
    return f"n={n} p10={out[n//10]:.0f} med={out[n//2]:.0f} p90={out[9*n//10]:.0f}" if n else 'none'
for p,a,b in [l.split() for l in sys.stdin]: print(p[-22:],f0(p,float(a),float(b)))
