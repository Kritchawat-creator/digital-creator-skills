"""Write an English SRT from a cue list measured on the DELIVERED cut (qc_audio.py timeline + whisper on out/*.mp4).
Edit CUES, then run from the episode folder:  python3 -I make_srt.py subtitles/epNN_en.srt
Start each cue ~0.15 s before its speech run and end it ~0.2 s after; never let two cues overlap.
The SRT is a sidecar file: it is NOT burned into the video (owner rule: no local text on pixels)."""
import sys
CUES = [  # (start_s, end_s, text) -- EP01 values as an example
    (0.10, 2.20, "Leo, can you open the light, please?"),
    (2.45, 3.90, "Open the light?"),
]
def ts(s): return f"{int(s//3600):02d}:{int(s%3600//60):02d}:{int(s%60):02d},{round((s-int(s))*1000):03d}"
assert all(a < b for a, b, _ in CUES) and all(CUES[i][1] <= CUES[i+1][0] for i in range(len(CUES)-1)), "bad/overlapping cue"
with open(sys.argv[1], "w", encoding="utf-8") as o:
    for i, (a, b, t) in enumerate(CUES, 1): o.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")
print(sys.argv[1], len(CUES), "cues")
