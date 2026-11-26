#!/usr/bin/env python3
"""Run prompts/queue.json (or the names given) through meta.ai; download + QC each new clip. Stops on refusal."""
import sys, json, subprocess, time
sys.path.insert(0, "tools")
import meta
import os
Q = json.load(open(os.environ.get("QUEUE", "prompts/queue.json")))
names = sys.argv[1:]
if names: Q = [q for q in Q if q[0] in names]
for name, master, text in Q:
    print(f"=== {name} {time.strftime('%H:%M:%S')}", flush=True)
    for attempt in range(8):
        try:
            new = meta.go("video", ("" if master.startswith("__") else "__ep11_") + master, text, 330, resume=bool(os.environ.pop("RESUME", "")))
            if new != "OVER": break
            new = None; time.sleep(75)
        except SystemExit as e:
            print("ERR", e, flush=True); new = None; time.sleep(10)
    if not new:
        print(f"STOPPED at {name}", flush=True); sys.exit(1)
    url = new[0]
    open("clips/urls.txt", "a").write(f"{name}\t{url}\n")
    subprocess.run(["python3", "dlqc.py", name, url])
    subprocess.run(f"python3 voicing.py clips/{name}.mp4 | tail -4", shell=True)
    sys.stdout.flush(); time.sleep(6)
print("DONE", flush=True)
