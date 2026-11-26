#!/usr/bin/env python3
"""Run image prompts (prompts/<name>.txt, attach key from prompts/images.json) through meta.ai, save to masters/ (or thumb/).
runimg.py name [name ...]   Stops on refusal."""
import sys, json, subprocess, time
sys.path.insert(0, "tools")
import meta
A = json.load(open("prompts/images.json"))
for name in sys.argv[1:]:
    print(f"=== {name} {time.strftime('%H:%M:%S')}", flush=True)
    new = None
    for attempt in range(8):
        try:
            new = meta.go("image", A[name], open(f"prompts/{name}.txt").read().strip(), 300)
            if new == "OVER" and "couldn't attach the image" in meta.st()["tail"].replace("\u2019","'"):  # EP.11: accept Meta's own offer
                new = meta.go("image", "none", f"Yes, please make it again: the image exactly as described in my last message.", 300)
            if new != "OVER": break
            new = None; time.sleep(75)
        except SystemExit as e:
            print("ERR", e, flush=True); time.sleep(10)
    if not new:
        print(f"STOPPED at {name}", flush=True); sys.exit(1)
    subprocess.run(["sh", "tools/getimg.sh", name, new[0]])
    if name == "thumb_art":
        subprocess.run("cp masters/thumb_art.png thumb/thumb_art_v1.png; cp masters/thumb_art.webp thumb/thumb_art_v1.webp", shell=True)
        open("thumb/meta_cover_url.txt", "w").write(new[0] + "\n")
    time.sleep(6)
print("DONE", flush=True)
