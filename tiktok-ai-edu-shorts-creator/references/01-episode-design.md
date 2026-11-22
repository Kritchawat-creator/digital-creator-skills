# 01 — Lesson design for a vertical short

## TikTok teaching rules (from the cast bible; owner-approved 2026-11-21)

| Viewer behaviour | Rule in the script |
| --- | --- |
| Decides in 1-2 s | First clip IS the mistake or question. No intro, greeting or logo. EP01 C1 starts speaking at 0.2 s |
| Sound often off | Every key English line also listed as on-screen text, top third, clear of the right-side buttons and the bottom caption area |
| One swipe away | One point per clip, ≤3 phrases, 15-40 s (EP01: 22.5 s, 5 clips) |
| Rewatches loops | Last clip leads back to the first (EP01: lamps-on quiz → lamps-off hook) |
| Comments drive reach | End with a two-option quiz to camera ("open the TV, or turn on the TV? Tell me in the comments.") |
| Fear of being wrong | The mistake is kind-funny; the teacher character never mocks; the fix is always shown |
| Global audience (this series) | English only in text, caption, hashtags, subtitles. The learner can still have an accent |

## Script structure that worked (F1 "direct translation vs natural English")

| Clip | Shot | Speaker | Purpose | EP01 length in cut |
| --- | --- | --- | --- | --- |
| C1 | OTS over the teacher → learner | Learner | Wrong sentence = hook | 2.3 s |
| C2 | Reverse OTS → teacher | Teacher | Echo the mistake + natural version | 4.0 s |
| C3 | Reverse OTS → teacher | Teacher | Pattern (on / off), slow | 4.9 s |
| C4 | OTS → learner | Learner | Repeats it, thanks (soft nod, no laugh) | 5.2 s |
| C5 | Learner alone to lens | Learner | Transfer quiz + comment CTA | 6.1 s |

## Script review checklist (do this before any generation)
1. **Shot geometry is physically consistent.** EP01 v1 had the teacher *standing* in the reverse shot but his head in
   the lower-left foreground of the OTS shot (only true if seated). Fix: seat both at neighbouring desks.
2. **Screen direction (180° rule).** Write it into the script and every prompt: learner looks screen-LEFT, teacher
   screen-RIGHT, both "just past the camera, NOT into the lens".
3. **The set makes the premise true.** Asking to turn on a light needs the lamps visibly OFF (dusk) in C1-C4; the
   solo quiz master can show them ON as a visual payoff.
4. **Listener problem removed by framing.** OTS means the listener is the back of a head; the solo master has no
   listener. Two-character same-frame dialogue is where mouth overlap and refusals happen.
5. **Exact lines in quotes**, one speaker each, intentional mistakes marked "keep it".
6. **On-screen text list with rough-cut timings** and the **caption** (English, 3-5 topic hashtags + always `#fyp #creatorsearchinsight`) in `script.md`.
7. Keep `script_v1.md`; put a short "v2 changes" note at the top of `script.md` and in `qc_log.txt`.
8. **The rule you teach is exactly true.** Say it the way a teacher would defend it in the comments. EP04 draft
   "very goes at the end" was wrong ("I very much like it" is fine) → "*very* alone can't go before a verb: use
   *really* before it or *very much* after it". Same wording in lines, overlays and caption.
9. **A new location every episode** (owner rule 2026-11-21, overrides "one office set"). Take it from the series
   spec's location table (Talkoro: `series-consistency-spec.md` §3) and give the line a story reason (EP04: lattes in
   a café → "I very like this coffee!"). Everything else stays identical across episodes: cast blocks, outfits,
   voices, style block, shot grammar, structure, quiz wording, cover template, overlays, caption pattern.
10. **Props make the line true, but stay on the table.** A cup the speaker talks about sits in front of them; write
    "does not drink and does not lift the cup" — lifting/sipping in a static clip breaks lip-sync and adds logo surfaces.

## Series consistency (multi-episode batches)
- One spec file per series (Talkoro: `talkoro-tiktok/docs/series-consistency-spec.md`) is the source of truth; put
  it in every episode session's brief. Copy prompts word for word from the canon episodes; add anything new to it.
- Run the cross-episode montage (one frame per character vs earlier episodes + all covers side by side) on the
  **masters**, before any clip, and again on the final cut. EP03 ran it after scheduling and was stuck with its
  deviations; EP04 caught a younger-looking Mint at master stage and fixed it.

## Format notes
| Format | Masters | Notes |
| --- | --- | --- |
| F1 two-person (learner + teacher) | OTS over teacher, reverse OTS over learner, learner solo to lens | EP01, EP04; 5 clips ≈ 22 s |
| F2 one speaker, Don't say / Say | waist-up + chest-up of the same pose, both to lens | EP02; no laptop, no listener; 3 swaps + quiz ≈ 30 s (cap) |
| F3 mentor + learner meeting | across a small round table, OTS both ways + learner solo | EP03; "Two adult coworkers in a short work meeting", mentor "looks 38, not older" |

## Episode folder
```
epNN-<slug>/  script.md  script_v1.md  prompts/  masters/  clips/  build/  out/  cover/  subtitles/  edl.tsv  qc_log.txt
```
`prompts/*.txt` hold the exact text sent to Meta AI (M1-M3, C1-C5, COVER) so a clip can be regenerated identically.
