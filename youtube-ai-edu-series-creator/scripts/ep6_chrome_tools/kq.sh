# tools/kq.sh NAME [a b] : kids two-shot clip QC: whisper + speech runs + mouth strips (Toby row, Ivy row, full frame) over a..b -> build/kq_NAME.png
# EP.3: crops per master (1280x720 clip): supkids Toby 200:160:330:150 / Ivy 200:160:640:150 (measured on supkids_master); override with TC=/IC=
n=$1; a=${2:-0.2}; b=${3:-5.0}
TC=${TC:-200:160:330:150}; IC=${IC:-200:160:640:150}
sh tools/asr.sh $n; python3 build/env.py $n 0 10
python3 tools/eyez.py $n:$a:$b:$TC $n:$a:$b:$IC $n:$a:$b:1280:720:0:0 && cp build/look.png build/kq_$n.png
