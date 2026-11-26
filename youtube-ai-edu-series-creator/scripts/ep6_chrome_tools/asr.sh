# local word check: tools/asr.sh NAME [in out] -> whisper-cli (ggml-small, already on this Mac) transcript of clips/NAME.mp4
n=$1; ss=${2:-0}; to=${3:-10}
ffmpeg -v error -y -ss $ss -to $to -i clips/$n.mp4 -ac 1 -ar 16000 build/asr_$n.wav
printf "%s\t" "$n"; whisper-cli -m ~/.cache/whisper/ggml-small.bin -f build/asr_$n.wav -l en -nt -np 2>/dev/null | tr '\n' ' '; echo
