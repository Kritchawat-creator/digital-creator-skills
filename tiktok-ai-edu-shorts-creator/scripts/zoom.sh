#!/bin/sh
# 5 fps strip of a larger region (both characters). Run from the episode folder.
# usage: sh zoom.sh NAME START DUR [CROP w:h:x:y, default 720:640:0:300] [ROWS, default 4]  (6 tiles per row)
mkdir -p build
CROP=${4:-720:640:0:300}
ffmpeg -v error -y -ss "$2" -t "$3" -i "clips/$1.mp4" -vf "fps=5,crop=$CROP,scale=300:-1,tile=6x${5:-4}" -frames:v 1 "build/qcz_$1.png" && echo "build/qcz_$1.png"
