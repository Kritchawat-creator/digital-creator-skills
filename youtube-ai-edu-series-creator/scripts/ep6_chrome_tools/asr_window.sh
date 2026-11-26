# word-level times: asrw_seg.sh NAME in out
ffmpeg -v error -y -ss $2 -to $3 -i clips/$1.mp4 -ac 1 -ar 16000 build/w.wav; printf "$1 $2-$3: "; whisper-cli -m ~/.cache/whisper/ggml-small.bin -f build/w.wav -l en -nt -np 2>/dev/null | tr '\n' ' '; echo
