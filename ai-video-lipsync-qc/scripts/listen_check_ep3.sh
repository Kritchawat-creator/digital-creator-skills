#!/bin/sh
# usage: listen_check.sh -> out/ep3_listen_check.mp4: the clips the owner must hear, each labelled "N. CLIP  in-out  expected line"
PY=/e/claude-work/pudding-ep1/.venv/Scripts/python.exe
FF=$("$PY" -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
mkdir -p build/listen; : > build/listen/list.txt; n=0
while IFS='|' read -r clip a b label; do
  n=$((n+1)); d=$("$PY" -c "print($b-$a+0.6)")
  printf '%s' "$n. $clip $a-$b  $label" > build/listen/t$n.txt
  "$FF" -nostdin -v error -y -ss "$a" -t "$d" -i "clips/$clip.mp4" -vf "scale=1280:720,drawtext=fontfile='fonts/Nunito[wght].ttf':textfile=build/listen/t$n.txt:x=20:y=20:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.7" \
    -af "aresample=48000,aformat=channel_layouts=stereo" -c:v libx264 -preset veryfast -crf 23 -r 24 -c:a pcm_s16le build/listen/p$n.mov
  echo "file 'p$n.mov'" >> build/listen/list.txt
done <<'LIST'
A1|0.5|3.0|Pudding: "Where I can change money?" (wrong order on purpose)
A2b|1.6|6.5|Ollie: "You mean: Where can I change money? It's over there!"
C01|0.7|3.8|Biscuit: "You again! Hello, Pudding!"
C05|1.5|6.3|Biscuit SLOW: "How much... would you like... to change?"
C06|0.8|3.2|Pudding: "Five thousand baht, please."
C08|2.5|5.2|Pudding: "How much is it?" - once or twice?
T01c|1.0|5.0|Pudding: "Oh no! Look at that queue!"
H5b|1.7|4.8|Biscuit: "Thank you! You too!"
H6|0.2|7.7|Biscuit: "Pudding has British money now! But can he get a taxi? Find out in episode four!"
LIST
"$FF" -v error -y -f concat -safe 0 -i build/listen/list.txt -c:v copy -c:a aac -b:a 160k out/ep3_listen_check.mp4 && echo out/ep3_listen_check.mp4
