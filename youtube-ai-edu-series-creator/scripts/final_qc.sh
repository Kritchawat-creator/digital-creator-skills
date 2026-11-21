#!/bin/sh
# usage: final_qc.sh out/EPISODE.mp4 -> stream specs, whole-video contact sheets (1 frame / 4 s) in build/, loudness
PY=${PY:-python}   # set PY to the project venv python, e.g. export PY=/e/claude-work/<project>/.venv/Scripts/python.exe
FF=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
V=${1:?usage: final_qc.sh out/EPISODE.mp4}
"$FF" -hide_banner -i "$V" 2>&1 | grep -E "Duration|Video:|Audio:" | sed 's/^ *//'
"$FF" -v error -y -i "$V" -vf "fps=1/4,scale=384:-1,drawtext=fontfile='fonts/Nunito[wght].ttf':text='%{pts\:hms}':x=4:y=4:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.6,tile=6x7" build/final_sheet_%d.png
ls build/final_sheet_*.png
"$FF" -hide_banner -nostdin -i "$V" -vn -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
