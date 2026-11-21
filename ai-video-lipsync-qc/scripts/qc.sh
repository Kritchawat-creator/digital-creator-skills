#!/bin/sh
# usage: qc.sh NAME -> speech segments (non-silent intervals) + 10-frame contact sheet build/qc_NAME.png
FF=$(./.venv/Scripts/python.exe -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
echo "== $1 audio (silence gaps):"
"$FF" -hide_banner -i "clips/$1.mp4" -af "silencedetect=n=-32dB:d=0.25" -f null - 2>&1 | grep -oE "silence_(start|end): [0-9.]+" | tr '\n' ' '; echo
"$FF" -v error -y -i "clips/$1.mp4" -vf "fps=1,scale=256:-1,drawtext=fontfile='fonts/Nunito[wght].ttf':text='%{pts\:hms}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x2" -frames:v 1 "build/qc_$1.png" && echo "sheet build/qc_$1.png"
