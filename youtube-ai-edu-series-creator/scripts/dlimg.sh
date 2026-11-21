#!/bin/sh
# usage: dlimg.sh OUT_PATH_WITHOUT_EXT URL -> saves .webp + .png (Meta AI image from fbcdn)
PY=${PY:-python}   # set PY to the project venv python, e.g. export PY=/e/claude-work/<project>/.venv/Scripts/python.exe
curl -sSfL -o "$1.webp" "$2" && "$PY" -c "import sys;from PIL import Image;im=Image.open(sys.argv[1]+'.webp').convert('RGB');im.save(sys.argv[1]+'.png');print(sys.argv[1]+'.png',im.size)" "$1"
