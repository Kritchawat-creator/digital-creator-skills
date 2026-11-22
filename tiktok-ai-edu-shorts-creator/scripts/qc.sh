#!/bin/sh
# Clip QC for 9:16 (720x1280) Meta AI clips, macOS (Homebrew ffmpeg + whisper-cli).
# Run from the EPISODE folder (it needs clips/ and build/):  sh <skill>/scripts/qc.sh C1_v2
# Prints: speech-band timeline (1 char = 0.1 s, rows of 5 s), voicing line (1 char = 40 ms),
#         whisper transcript with segment times; writes build/qc_NAME.png (10 tiles, 1 tile = 1 s).
# Homebrew ffmpeg has no drawtext, so tiles carry no burned timestamps: count them.
H=$(cd "$(dirname "$0")" && pwd)
M=${WHISPER_MODEL:-$HOME/.cache/whisper/ggml-small.bin}
mkdir -p build
python3 -I "$H/qc_audio.py" "clips/$1.mp4"
python3 -I "$H/voicing.py" "clips/$1.mp4"
ffmpeg -v error -y -i "clips/$1.mp4" -vf "fps=1,scale=180:-1,tile=10x1" -frames:v 1 "build/qc_$1.png" && echo "sheet build/qc_$1.png"
ffmpeg -v error -y -i "clips/$1.mp4" -ac 1 -ar 16000 "build/$1.wav" && whisper-cli -m "$M" -l en -np "build/$1.wav" 2>/dev/null | grep -- '-->' | sed 's/^/ASR: /'
