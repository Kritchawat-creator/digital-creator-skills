#!/bin/sh
# usage: listen_check.sh LIST.txt OUT.mp4
# One labelled MP4 of the clips the owner must hear. LIST.txt has one line per clip:  CLIP|in|out|label
#   C08|2.5|5.2|Pudding: "How much is it?" - once or twice?
# Each part shows "N. CLIP in-out  label" on screen and runs 0.6 s past the out point.
PY=${PY:-python}   # set PY to the project venv python, e.g. export PY=/e/claude-work/<project>/.venv/Scripts/python.exe
FF=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
LIST=${1:?usage: listen_check.sh LIST.txt OUT.mp4}; OUT=${2:?usage: listen_check.sh LIST.txt OUT.mp4}
mkdir -p build/listen; : > build/listen/list.txt; n=0
while IFS='|' read -r clip a b label; do
  [ -z "$clip" ] && continue
  n=$((n+1)); d=$("$PY" -c "print($b-$a+0.6)")
  printf '%s' "$n. $clip $a-$b  $label" > build/listen/t$n.txt
  "$FF" -nostdin -v error -y -ss "$a" -t "$d" -i "clips/$clip.mp4" -vf "scale=1280:720,drawtext=fontfile='fonts/Nunito[wght].ttf':textfile=build/listen/t$n.txt:x=20:y=20:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.7" \
    -af "aresample=48000,aformat=channel_layouts=stereo" -c:v libx264 -preset veryfast -crf 23 -r 24 -c:a pcm_s16le build/listen/p$n.mov
  echo "file 'p$n.mov'" >> build/listen/list.txt
done < "$LIST"
"$FF" -v error -y -f concat -safe 0 -i build/listen/list.txt -c:v copy -c:a aac -b:a 160k "$OUT" && echo "$OUT ($n parts)"
