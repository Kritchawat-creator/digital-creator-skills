# 06 — Title, description, tags, translations, settings

Write everything into `docs/<series>-epN-upload-metadata.md` before opening Studio, and record the result there
afterwards ("As uploaded").

**Evidence level:** the formulas below come from the channel plan and were applied to three episodes. There is no
performance data behind them yet: on 2026-11-21 only EP.2 was Public. Revisit this file once analytics exist
(impressions, click-through rate, search terms).

## 1. Title

Long-form videos are found by search, so the title starts with what a learner types; the series name goes last.

`[Situation] English: [benefit or question] | <Series short name> EP.[n]`

| Episode | Title | Length |
| --- | --- | --- |
| EP.1 | Airport English: 5 Phrases You Need at Immigration \| Pudding EP.1 | 69 |
| EP.2 | Lost Luggage English: What to Say When Your Bag Is Missing \| Pudding EP.2 | 75 |
| EP.3 | Changing Money English: Ask "Where?" and "How Much?" \| Pudding EP.3 | 69 |

Keep the episode number in both the title and the thumbnail. No "for kids" wording.

## 2. Description

Structure used on EP.3 (copy the order; replace the content):

```
<One line: what you learn + the hero, with one or two emoji>
<Two lines of story: the problem, the question, what the lesson contains>

Level: Beginner (A1–A2) · English with English subtitles (turn on CC for more languages)

📌 Phrases in this lesson
1. …
2. …
5. …

📝 Grammar: <the rule in one line>
❌ Common mistake: "<wrong>" ✅ Say: "<right>"
<one extra teaching line for the topic>

⏱ Chapters
00:00 Last time on <series>
00:20 Story: …
01:10 5 phrases for …
01:54 Common mistake: …
02:45 Fast English vs slow English
03:03 Speaking practice (say it with <hero>)
03:31 Quiz
04:15 Watch again
04:39 Next episode

💬 Quiz: write your answers in the comments!
◀ Previous episode: <title>: <url>
▶ Next episode: <title> (coming soon)
📺 Season playlist: <url>

#LearnEnglish #EnglishForBeginners #TravelEnglish #<Topic> #EnglishConversation

Animation made with AI tools. Story, script and lessons written and directed by the <team name>.
```

Rules:
- **Chapters come from `build.py plan`**, never by hand. The first chapter is `00:00`, there are at least three,
  and each is at least 10 s long. EP.1's first draft had a chapter at 00:04 and had to be merged into 00:00.
- The first two lines carry the search terms in natural sentences.
- The translations reuse everything from "📌" onward in English (section 4), so keep that part
  language-neutral.
- **Read the live description of the previous episode before copying it.** EP.2 went up without the AI-note
  line; a "template" assumed from memory would have been wrong.
- Whether the next-episode link points to a Private video is the owner's call: viewers can't open it.

## 3. Tags

- Limit: **500 characters by Studio's own counter.** Count there, not locally.
- Used: 17 tags (about 350 characters) on EP.1, 19 on EP.2, 21 tags (415/500) on EP.3.
- Mix, in this order:
  1. head terms: `learn english`, `english for beginners`, `basic english`, `esl`
  2. the episode's situation: `changing money english`, `currency exchange english`, `airport english`
  3. the exact phrases as people search them: `how much is it`, `where can i change money`
  4. the grammar or skill: `english questions`, `question word order`, `english speaking practice`,
     `english shadowing`
  5. format: `english cartoon story`
  6. "learn English" in the target languages: `เรียนภาษาอังกฤษ`, `aprender inglés`, `học tiếng anh`,
     `belajar bahasa inggris`, plus one topic term in the main second language
- No other channels' names, no brand names, no misleading terms.

## 4. Translations (Studio → Subtitles → languages)

Five languages on every episode: **Thai, Spanish, Portuguese, Vietnamese, Indonesian.**

| Part | Rule |
| --- | --- |
| Title | Translate the situation and benefit; keep the quoted English phrase and "\| <Series> EP.n" unchanged |
| Description | A translated intro (what you learn, level, the grammar point in that language), then the **English original from "📌" onward**: phrases, chapters and links stay in English |
| Subtitles | English `.srt` always; the main second language (`.th.srt`) as a file. Not auto-dubbing |

Example title set (EP.3):
- TH: ภาษาอังกฤษสำหรับแลกเงิน: ถาม "Where?" และ "How much?" | Pudding EP.3
- ES: Inglés para cambiar dinero: pregunta "Where?" y "How much?" | Pudding EP.3
- PT: Inglês para trocar dinheiro: pergunte "Where?" e "How much?" | Pudding EP.3
- VI: Tiếng Anh khi đổi tiền: hỏi "Where?" và "How much?" | Pudding EP.3
- ID: Bahasa Inggris untuk menukar uang: tanya "Where?" dan "How much?" | Pudding EP.3

## 5. Settings block

| Setting | Value | Who decides |
| --- | --- | --- |
| Visibility | **Private** on upload | Public only when the owner says so in chat |
| Audience | "No, it's not made for kids" | The owner (decided for this series on EP.1) |
| Altered or synthetic content | "No" for clearly animated content, with the AI-note line in the description | The owner (decided on EP.1) |
| Category / language | Education / English; caption language English | — |
| Captions | `<episode>.en.srt`, `<episode>.th.srt` | — |
| Thumbnail | `out/<episode>_thumbnail.jpg` (AI art + local OFL text) | — |
| End screen | Previous episode + subscribe, over the 16 s end card | — |
| Playlist | The season playlist, "watch in order", oldest first | Ask before creating a new one |

Made for kids, in short (asked on EP.1): a made-for-kids video loses comments, notifications, end screens and
personalised ads. The setting must be honest. This series is written for teens and adults, so the owner chose
"not made for kids".

## 6. Linking the series

- Playlist from the first episode. "Reuse details" from the previous episode adds the new upload to the same
  playlist.
- End screen: the previous episode + subscribe (the next one doesn't exist yet).
- **Changing an older episode** (adding a "next episode" link to its description or end screen) needs the
  owner's yes each time.
- Plan items not done yet: pinned comment with previous / next / playlist links, community polls, Shorts with
  related-video links.

## 7. "As uploaded" record

Append to the metadata doc after the upload:
```
## As uploaded (YYYY-MM-DD)
- Video: https://youtu.be/<id> (Private) — file out/<episode>.mp4 (render N): 5:07, −14.5 LUFS / −1.5 dBTP, A/V 0 ms
- Title, description + chapters + AI-note line, N tags (X/500), audience, altered content, category, language,
  thumbnail, EN subtitles (N cues), TH subtitles (N cues), title + description in TH/ES/PT/VI/ID,
  end screen (elements, start–end), playlist. Read back on the edit page: visibility Private.
- Word check (automatic captions): result.
- Superseded uploads: id, why, who deleted it.
- Open: anything waiting for the owner.
```
