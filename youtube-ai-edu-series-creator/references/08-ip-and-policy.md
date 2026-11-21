# 08 — Copyright, trademark and platform policy

A checklist for monetizable AI-made videos. Run it when planning the episode, in every prompt, on every clip and
once more on the delivered file. It is not legal advice: a dispute or takedown goes to the owner and a lawyer.

## 1. Checklist

| Element | Rule | How it was met (Pudding) |
| --- | --- | --- |
| Characters | Original designs. Never "in the style of" a studio, show or artist. Check for look-alikes of famous characters | Original cast; prompts end "Original characters" |
| Names | Search the channel and character names on YouTube and in trademark registers (USPTO, EUIPO, the owner's national office; class 41 for education and entertainment). The owner runs the official register search | Listed for the owner |
| Places and props | Generic only: no real airport, agency, airline, transit, bank or shop names; no logos, crests or uniforms with emblems. From EP.2 on, masters carry no text at all | Generic halls and counters, blank screens, plain cap |
| On-screen words | All words are added in the edit with our own fonts. AI images carry no text | "NO text, NO letters, NO numbers" in every master |
| Money | No banknotes, coins, cash, wallets, currency symbols, exchange-rate boards, flags or portraits in AI images. Real note designs and royal portraits are a legal and cultural risk. Amounts are only spoken, or typed on our own cards | EP.2 cliffhanger = a spoken line and a worried face; EP.3: zero money visible in 26 clips and 4 images |
| Vehicles | Generic cartoon cars: no livery, brand, readable plates or sign text | EP.3 taxi rank |
| Voices | A source with clear commercial rights | Meta AI native audio (below) |
| Music and effects | Synthesised in code (owned outright) or the YouTube Audio Library. Never an AI tool's licensed songs or song lip sync (Content ID) | `audio_gen.py` |
| Fonts | SIL OFL fonts; keep `OFL.txt` with the project | Nunito, Baloo 2 |
| Audience | Topics and wording for teens and adults; teen characters drawn as teens. The owner sets "made for kids" honestly | Owner chose "not made for kids" |
| AI disclosure | Clearly animated content usually doesn't need the "altered or synthetic" label. The owner decides; a note in the description is honest and cheap | Owner chose "No" + the AI-note line |

Voices in detail:
- **edge-tts / Edge "Read Aloud": excluded.** No clear commercial licence.
- **Meta AI native and lip-sync voices:** Meta AI Terms (effective 2026-05-13) don't forbid commercial use and
  make the user responsible for the output. Re-read the terms when they change.
- Paid TTS with commercial terms, or a human voice, are the safest options.

AI-note line used in descriptions:
> Animation made with AI tools. Story, script and lessons written and directed by the Pudding team.

## 2. Prompts: name the words, not the category

"No logos" alone didn't work. Meta AI drew "UK BORDER FORCE" on a screen, a real airport's name on a sign and a
badge on a cap in one clip (EP.1). What worked:

- Word-level negatives: "Do NOT show the words X, Y; screens blank; no flags, logos, emblems".
- The episode's banned objects listed in **every** prompt: masters, clips and thumbnail art.
- No scene labels in quotes: a label became a sign in the background.
- A character that morphs mid-clip can gain an emblem (a crown badge on a cap in EP.2). Any badge or crest that
  appears is a QC failure.

## 3. On every clip and on the delivered file

- Scan each contact sheet and zoom strip for leaked names, logos, emblems, flags, money, text.
- A real brand visible for under a second still fails: regenerate or crop. Don't rely on blur.
- Scan the whole-video contact sheets from `final_qc.sh` once more before upload.

## 4. AI tool refusals are policy signals

Meta AI treats a baby character as a child. It refused scenes where he was left alone, visibly upset, silently
coached by an adult, spoken to closely by an adult, or waved goodbye to (table in `02`). It also refused a
16-year-old character addressing the camera as a teacher.

- **Never reword a prompt to get the refused content.** Ask what the tool can make and accept that.
- Restructuring the scene around the offered alternative (the adult alone → shot / reverse shot in the edit) is
  accepting the offer. No prompt was changed to obtain the refused image.
- These limits also keep a cute-character channel clearly non-exploitative, which matters when its audience
  setting is "not made for kids".
- Log every refusal with the tool's reason and what was used instead.

## 5. Monetization policy: "inauthentic content"

From the channel plan (sources linked there): generic, repetitive or template-only videos can't be monetized,
whether or not AI made them. AI-assisted channels can be, when a person directs the work and each video offers
distinct value. Guardrails: a new story beat and a new phrase list every episode; a person reviews the script,
listens to the voices and decides the settings; varied formats; no bulk uploading.

## 6. Records to keep

- Each asset's source and licence in the series bible (voices, music, fonts, images), with the date the terms
  were read.
- The episode's banned-items table in the script doc.
- Refusals and IP failures in `qc_log.txt`.

| Element | Rule | Status |
| --- | --- | --- |
| Voices | Meta AI native audio (terms read YYYY-MM-DD) | OK |
| Music | Synthesised in `audio_gen.py` | OK |
| Fonts | Nunito, Baloo 2 (OFL, `fonts/OFL.txt`) | OK |

## 7. Decisions

- Licence unclear → leave it out; use an owned or clearly licensed alternative.
- Ask the owner before downloads and installs, uploads, and any Public visibility.
- Never set the audience setting or publish on the owner's behalf without their word in chat.
