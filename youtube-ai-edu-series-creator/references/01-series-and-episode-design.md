# 01 — Series and episode design

What to decide before any image is generated. Values marked *(Pudding)* are project-specific.

## 1. What the series is for

From the channel plan (`channel-plan.md`, November 2026; its sources are linked there, re-check them before
relying on a number):

- **Long-form earns watch hours; Shorts don't.** Watch time from the Shorts feed doesn't count toward the
  watch-hour threshold. Shorts bring subscribers, long-form lessons bring hours, playlists add more hours.
- **16:9 is always long-form.** A vertical video over 3 minutes is also long-form, but the owner chose horizontal.
- **Target the bar that applies to the channel's age.** The plan aims at 1,000 subscribers and 8,000 watch hours
  for ad revenue, with 500 subscribers and 3,000 hours as the first milestone.
- **Positioning:** a serialized story with cliffhangers. Viewers come back for the plot as well as the lesson.
  Each episode is a new place, a new problem and a different phrase list.
- **Audience:** teens and adults, beginner level. Keep every signal adult-facing (travel, work, daily life;
  titles for adult learners; no nursery songs; no "for kids" keywords) so the honest audience setting is
  "not made for kids".
- **Auto-dubbing stays off** for a language lesson: it would replace the audio being taught. Subtitles and
  translated titles carry other languages.

**Staying clear of "inauthentic content"** (the main monetization risk for an AI-made channel, per the plan):
- Every episode moves the story forward. Never re-skin one video with different words.
- Every episode teaches different language.
- A person directs the work: the owner reviews scripts, listens to the voices, decides the settings.
- Vary the formats and don't bulk-upload.

## 2. The series bible

Keep one document that every episode obeys (*Pudding: `pudding-ep1-cast-and-script.md`*):

| Part | Content |
| --- | --- |
| Cast | Per character: shape, colours, the two or three details that must never change (Pudding: yellow backpack, dot eyes, **no eyelashes**; Biscuit: **orange** beak, big shiny eyes, plain navy cap with **no badge**), voice description, teaching job |
| Roles | Hero = beginner who makes the viewer's mistakes. Guide = speaks fast, so the hero asks "Sorry, could you say that again, slowly?" every episode. Friends model natural speech. One adult or animal character is the on-camera lesson host |
| Style | Flat 2D cartoon, thick outlines, flat colours, no realistic textures. Say it in every prompt |
| Canon positions | Per location: who is LEFT, who is RIGHT, which way they face. Never swap within an episode |
| Episode table | Per episode: situation, key phrases, grammar point, cliffhanger |
| Rules table | Copyright and trademark rules, voices, music, fonts (see `08`) |

Teens stay in-story only. Meta AI refused a 16-year-old character addressing the camera as a teacher, so the
host is the adult animal.

## 3. Episode structure that fills 5 minutes without dead air

All three episodes used this order. Times are the chapter starts of EP.1 and EP.3 as delivered.

| Section | EP.1 | EP.3 | What it is |
| --- | --- | --- | --- |
| Hook | 0:00 | 0:00 | The wrong sentence, a ❌ and "Don't say this!" (4–7 s), then a 3 s title card |
| Last time on… | (none) | 0:09 | One card plus the previous cliffhanger, reusing the previous episode's accepted cuts as files |
| Story | 0:07 | 0:20 | About 60–70 s of single-speaker clips with short location cards between places |
| Phrases | 1:20 | 1:10 | 5 phrases. Each: the host says it twice (two takes), then an example card with a new sentence |
| Common mistake + grammar | 2:18 | 1:54 | Wrong clip with ❌, right clip with ✅, then one or two rule cards |
| Extra teaching | — | 2:24 | Cards that add value for the topic (EP.3: saying prices) |
| Fast vs slow | 2:40 | 2:45 | The guide's fast line, a card that explains it, the slow version, a normal-speed line |
| Speaking practice | 3:00 | 3:03 | Shadowing: the voice, then a 2.8 s countdown with ticks, 5 lines |
| Quiz | 3:30 | 3:31 | 3–4 questions: 6 s timer card, then the answer card with a voice. Ends "Write your answers in the comments!" |
| Watch again | 4:10 | 4:15 | The story clips replayed, now understood |
| Cliffhanger + end card | 4:49 | 4:39 | New problem, the host's teaser line, then a 16 s end card for the end-screen elements |

Rules that keep it tight:
- Every clip is trimmed to speech ± about 0.3 s. No laugh, chuckle or ad-lib after the last word (owner rule).
- No silent card. Every card has music plus a pop, tick, sting or a voice.
- Two-take host clips are cut as two segments, removing the 3–5 s gap between takes.
- **Short of the target? Add teaching, not padding.** EP.3 went from 4:42 to 5:07 with "Saying Prices", "More
  Prices", "More Questions" and a fourth quiz question.

## 4. Writing the lines

- **One speaker per clip.** A two-speaker clip made the wrong mouth move (EP.1 S01).
- Lines used ran from one word to three short sentences. The longest single clip line was 7.5 s (EP.3 H6, three
  sentences). A 10 s clip won't hold more.
- Put the intentional mistake in the script on purpose, and mark it. Meta AI may "correct" it, so that clip always
  goes into the listen check.
- A fast line is still written with correct spelling. Speed is shown with a FAST / SLOW tag.
- A two-take host line is prompted as "says it TWICE: slowly, one-second pause, natural speed". The takes were
  not reliably slower or faster, so the burned tag says "listen twice", not "slow → natural".
- Quiz answer cards must match the voice under them word for word.
- Repeat one line across episodes as a series habit *(Pudding: "Sorry, could you say that again, slowly?")*.

## 5. Design the scenes around what the AI tool allows

Meta AI treated the baby hero as a child and refused several scenes. Plan for these from the script stage instead
of discovering them clip by clip (full table in `02`):

| Don't write | Write instead |
| --- | --- |
| An adult character speaking to the hero in the same frame | Shot / reverse shot: the hero's lines in the two-shot, the adult's lines in an adult-alone shot of the same place |
| An adult coaching the silent hero | The host teaches straight to camera, alone |
| The hero left alone ("wait here"), crying, sad or frightened | The hero stays with a friend and asks calmly and bravely |
| A goodbye wave or close exchange between adult and hero | End the scene on the adult's line; use the reply as a lesson-card voice |
| A teen addressing the camera as teacher | The adult or animal host |
| A listener who looks "surprised", grins or watches something | A listener with lips pressed together and a calm face |

The line moved between episodes (a two-shot with the adult speaking passed in EP.2 and was refused in EP.3), so
test the first clip of every two-character scene before generating the rest.

## 6. The script document

Save as `docs/<series>-epN-script.md`. Sections, in order:

1. **Header:** situation, key phrases, grammar point, the mistake the hero makes (and why learners make it),
   callback to earlier episodes, cliffhanger.
2. **Continuity and IP rules for this episode:** a table of props, positions, character details and banned items.
   Example rows *(EP.3)*: backpack always on; the suitcase he got back in EP.2 is beside him in every shot;
   counter positions; "No banknotes, coins, cash, wallets, currency symbols or exchange-rate boards on screen";
   generic counter; generic taxi rank.
3. **Structure:** the section table with target times and source clips.
4. **Story clips:** `Clip | Location | Speaker | Line (exact) | Action / others`. The last column states every
   other character's mouth ("Biscuit beak closed").
5. **Lesson host clips:** `Clip | Host says | Example card`.
6. **Mistake and grammar cards**, with a note in the learners' language where it helps.
7. **Fast / slow sequence.**
8. **Quiz:** question, answer, and which clip window is the answer voice.
9. **End card** text and the end-screen elements.
10. **Prompts:** the master prompt and the clip skeleton actually used.
11. **As-built changes:** added after delivery. What was refused, replaced, cut or added, and why.

## 7. Subtitle language conventions *(Pudding, Thai)*

- Keep each character's pronoun the same across episodes (Pudding = ฉัน since EP.1).
- The hero's lines have no polite particles; example sentences for the viewer may use ค่ะ/ครับ.
- Mark intentional mistakes in the translation too ("(เรียงคำผิด)", "(ผิด)").
- A slow, word-by-word English line keeps one Thai line across its cues; identical consecutive Thai cues are
  merged in the `.srt`.

## 8. Episode folder

```
E:\claude-work\<series>-epN\
  clips\        downloaded clips (and reused cuts from earlier episodes, copied as files)
  masters\      scene masters (.png, plus the candidates that were rejected)
  thumb\        cover art from the AI tool
  audio\        music_loop.wav, sfx_*.wav (from audio_gen.py)
  fonts\        Nunito, Baloo 2 and their OFL.txt
  build\        intermediate files, QC sheets, burned_text.txt
  out\          <episode>.mp4, .en.srt, .th.srt, thumbnail, listen-check MP4
  docs\         script and upload metadata
  edl.tsv  qc_log.txt  sync_measurements.txt  build.py  thumbnail.py  + the QC scripts
```
Reuse the first episode's venv and fonts; copy the scripts from this skill's `scripts/` folder.
