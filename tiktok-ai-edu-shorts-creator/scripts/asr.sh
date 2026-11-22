#!/bin/sh
# Whisper transcript of one window of a clip: checks the exact words of a cut and what a tail noise is ("(sighs)").
# Run from the episode folder.  usage: sh asr.sh NAME START END
M=${WHISPER_MODEL:-$HOME/.cache/whisper/ggml-small.bin}
mkdir -p build
ffmpeg -v error -y -ss "$2" -to "$3" -i "clips/$1.mp4" -ac 1 -ar 16000 build/_asr.wav
printf "%s %s-%s: " "$1" "$2" "$3"; whisper-cli -m "$M" -l en -nt -np build/_asr.wav 2>/dev/null | tr -d '\n'; echo
