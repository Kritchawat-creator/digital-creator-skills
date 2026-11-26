import subprocess,array,math,sys
# env.py clip in out : speech-band dB per 50 ms with marks; gaps >=0.15 s under floor+10
c,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
raw=subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i',f'clips/{c}.mp4','-ac','1','-ar','16000','-af','highpass=f=200,lowpass=f=3500','-f','s16le','-'],capture_output=True).stdout
x=array.array('h',raw); v=[]
for i in range(0,len(x)-800,800):
    s=x[i:i+800]; v.append(20*math.log10((math.sqrt(sum(t*t for t in s)/800) or 1)/32768))
pk=max(v); thr=max(pk-28, sorted(v)[len(v)//6]+7); runs=[]; st=None
for i,d in enumerate(v+[-99]):
    if d>thr and st is None: st=i
    if d<=thr and st is not None: runs.append((a+st*.05,a+i*.05)); st=None
m=[]
for r in runs:
    if m and r[0]-m[-1][1]<0.2: m[-1]=(m[-1][0],r[1])
    else: m.append(r)
print(c,'thr %.0f pk %.0f'%(thr,pk),' '.join('%.2f-%.2f'%r for r in m if r[1]-r[0]>0.05))
