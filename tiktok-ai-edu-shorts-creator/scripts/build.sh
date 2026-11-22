#!/bin/sh
# Rough cut from edl.tsv (clip, in, out, ...): cut each window, scale 720x1280 -> 1080x1920 (format change only),
# concat. No overlays, no text, no colour or pixel edits. Run from the episode folder.
# usage: sh build.sh [OUT]   (default out/roughcut.mp4)
# In/out are frame-aligned at 24 fps and audio is padded/trimmed to the same length, so every segment's audio and
# video are identical in length. Without this, EP01 drifted up to 30 ms by the 5th segment.
set -e
OUT=${1:-out/roughcut.mp4}
mkdir -p build/seg "$(dirname "$OUT")"; rm -f build/seg/*.mov; : > build/seg/list.txt; i=0
tail -n +2 edl.tsv | while IFS="$(printf '\t')" read -r clip tin tout rest; do
  i=$((i+1)); o=$(printf 'build/seg/s%02d_%s.mov' $i "$clip")
  a=$(python3 -c "print(f'{round($tin*24)/24:.6f}')"); n=$(python3 -c "print(round(($tout-$tin)*24))"); d=$(python3 -c "print(f'{$n/24:.6f}')")
  ffmpeg -nostdin -v error -y -ss "$a" -i "clips/$clip.mp4" -frames:v "$n" -t "$d" \
    -vf "scale=1080:1920:flags=lanczos,fps=24,setsar=1,format=yuv420p" \
    -af "aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=$d,atrim=0:$d" \
    -c:v libx264 -preset slow -crf 16 -c:a pcm_s16le "$o"
  echo "file '$(basename "$o")'" >> build/seg/list.txt
done
ffmpeg -v error -y -f concat -safe 0 -i build/seg/list.txt -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "$OUT"
