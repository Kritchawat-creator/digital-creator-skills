"""build/meta.json from docs/family-ep04-upload-metadata.md, chapters from build.py's timeline (run after the final plan)."""
import json, re, sys, importlib.util
sys.argv = ["build.py", "plan"]
spec = importlib.util.spec_from_file_location("b", "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
t, starts, seen_cliff = 0.0, {}, 0
for s in b.SEGS:
    key = s.get("title") or (s.get("name") if s["kind"] == "clip" else None)
    if key and key not in starts: starts[key] = t
    if s["kind"] == "clip" and s["name"] == "N03" and s["t_in"] == 1.4:
        seen_cliff += 1
        if seen_cliff == 2: starts["CLIFF2"] = t
    t += s["dur"]
TOTAL = t
f = lambda k: "%02d:%02d" % divmod(int(starts[k]), 60)
CH = [("00:00", "Don't say this! · Last time"), (f("That afternoon, in the kitchen..."), "Story: baking in the kitchen"),
      (f("5 Phrases for Baking"), "5 phrases for baking"), (f("Common Mistake"), "Common mistake"),
      (f("bake · cook"), "Grammar: bake or cook · imperatives · first... then..."), (f("Ben's Fast English"), "Ben's Fast English"),
      (f("Say It With Toby!"), "Say it with Toby"), (f("Quiz Time!"), "Quiz"), (f("Watch Again"), "Watch again"),
      (f("CLIFF2"), "What happens next?"), (f(b.END_TITLE), "Next episode")]
doc = open("docs/family-ep04-upload-metadata.md", encoding="utf-8").read()
title = doc.split("## Title\n\n")[1].split("\n")[0].strip()
desc = doc.split("## Description\n\n```\n")[1].split("\n```")[0]
desc = desc.replace("CHAPTERS", "\n".join(f"{a} {c}" for a, c in CH))
tags = doc.split("## Tags")[1].split("```\n")[1].split("\n```")[0].strip()
assert "EP.4" in title and len(title) <= 100, title
assert "CHAPTERS" not in desc and len(desc) < 5000
json.dump({"title": title, "desc": desc, "tags": tags}, open("build/meta.json", "w"), ensure_ascii=False, indent=1)
print(title, len(title)); print("\n".join(f"{a} {c}" for a, c in CH)); print("desc", len(desc), "tags", len(tags), "end card start %.1f" % (TOTAL - 16))
