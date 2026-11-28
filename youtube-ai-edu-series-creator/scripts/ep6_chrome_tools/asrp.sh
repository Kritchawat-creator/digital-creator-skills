# tools/asrp.sh NAME in out -> whisper on the exact window + token probabilities (proves an intentional mistake word)
n=$1; a=$2; b=$3
ffmpeg -v error -y -ss $a -to $b -i clips/$n.mp4 -ac 1 -ar 16000 build/asrw_$n.wav
whisper-cli -m ~/.cache/whisper/ggml-small.bin -f build/asrw_$n.wav -l en -ojf -of build/asrw_$n -np >/dev/null 2>&1
python3 -c "
import json; j=json.load(open('build/asrw_$n.json'))
for s in j['transcription']:
  print('$n $a-$b', s['text'].strip(), '|', ' '.join(t['text'].strip()+':%.2f'%t['p'] for t in s['tokens'] if not t['text'].startswith('[')))"
