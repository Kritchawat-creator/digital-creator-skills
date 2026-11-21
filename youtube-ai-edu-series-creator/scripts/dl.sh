#!/bin/sh
# usage: dl.sh NAME URL  -> downloads a generated clip to clips/NAME.mp4 and prints its specs
PY=${PY:-python}   # set PY to the project venv python, e.g. export PY=/e/claude-work/<project>/.venv/Scripts/python.exe
FF=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
curl -sSfL -o "clips/$1.mp4" "$2" && "$FF" -hide_banner -i "clips/$1.mp4" 2>&1 | grep -E "Duration|Video:|Audio:" | sed 's/^ *//'
