# build/w.sh NAME... : wait for each clip in build/q2.log (or Q=log), then whisper + speech runs
L=${Q:-build/q2.log}
for n in "$@"; do
  until grep -qE "^$n: [0-9.]+s|STOPPED|Traceback" $L; do sleep 5; done
  grep -E "STOPPED|Traceback|REFUS" $L && exit 1
  sh tools/asr.sh $n; python3 build/env.py $n 0 10
done
