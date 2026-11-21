#!/bin/sh
# usage: zoom.sh NAME START DUR [crop] -> 5 fps strip of both faces during a speech window, build/qcz_NAME.png
PY=/e/claude-work/pudding-ep1/.venv/Scripts/python.exe
FF=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
CROP=${4:-1000:380:120:110}
"$FF" -v error -y -ss "$2" -t "$3" -i "clips/$1.mp4" -vf "fps=5,crop=$CROP,scale=420:-1,drawtext=fontfile='fonts/Nunito[wght].ttf':text='%{pts\:flt}':x=4:y=4:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=4x${5:-5}" -frames:v 1 "build/qcz_$1.png" && echo "build/qcz_$1.png"
