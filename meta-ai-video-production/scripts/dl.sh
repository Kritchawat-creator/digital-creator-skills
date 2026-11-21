#!/bin/sh
# usage: dl.sh NAME URL  -> downloads clip and prints its specs
FF=$(./.venv/Scripts/python.exe -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
curl -sSfL -o "clips/$1.mp4" "$2" && "$FF" -hide_banner -i "clips/$1.mp4" 2>&1 | grep -E "Duration|Video:|Audio:" | sed 's/^ *//'
