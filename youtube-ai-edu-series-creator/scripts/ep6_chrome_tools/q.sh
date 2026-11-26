# build/q.sh NAME... : whisper (whole clip), speech runs, pitch of the loud span, contact sheet -> build/qc_NAME.png
for n in "$@"; do
  sh tools/asr.sh $n; python3 build/env.py $n 0 10
  python3 build/env.py $n 0 10 | python3 -c "
import sys,subprocess
l=sys.stdin.read().split(); r=[x for x in l if x.count('-')==1 and x[0].isdigit()]
print(subprocess.run(['python3','build/f0c.py'],input='\n'.join('clips/$n.mp4 %s %s'%tuple(x.split('-')) for x in r if float(x.split('-')[1])-float(x.split('-')[0])>.35),capture_output=True,text=True).stdout,end='')"
done
