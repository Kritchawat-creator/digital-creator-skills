# build/wq.sh NAME... : like w.sh, plus pitch of every speech run and the contact sheet stays in build/qc_NAME.png
L=${Q:-build/q2.log}
for n in "$@"; do
  until grep -qE "^$n: [0-9.]+s|STOPPED|Traceback" $L; do sleep 5; done
  grep -E "STOPPED|Traceback|REFUS" $L && exit 1
  echo "##### $n"; sh tools/q.sh $n
done
