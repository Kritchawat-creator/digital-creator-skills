#!/bin/sh
# usage: qc.sh NAME -> speech-band timeline (qc_audio.py) + 10-frame contact sheet build/qc_NAME.png
PY=/e/claude-work/pudding-ep1/.venv/Scripts/python.exe
FF=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$PY" qc_audio.py "clips/$1.mp4"
"$PY" voicing.py "clips/$1.mp4"
"$FF" -v error -y -i "clips/$1.mp4" -vf "fps=1,scale=256:-1,drawtext=fontfile='fonts/Nunito[wght].ttf':text='%{pts\:hms}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x2" -frames:v 1 "build/qc_$1.png" && echo "sheet build/qc_$1.png"
