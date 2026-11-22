#!/bin/sh
# 5 fps strip of one face (mouth / jaw) to see WHO moves during a speech run. Run from the episode folder.
# usage: sh mouth.sh NAME START DUR CROP   (CROP = w:h:x:y in 720x1280 source px; 10 tiles per row = 2.0 s)
# Find the CROP first with:  ffmpeg -ss 0 -i clips/NAME.mp4 -frames:v 1 -vf crop=200:200:X:Y build/probe.png
mkdir -p build
ROWS=$(python3 -c "import math;print(math.ceil($3*5/10))")
ffmpeg -v error -y -ss "$2" -t "$3" -i "clips/$1.mp4" -vf "fps=5,crop=$4,scale=160:-1,tile=10x$ROWS" -frames:v 1 "build/qcm_$1.png" && echo "build/qcm_$1.png"
