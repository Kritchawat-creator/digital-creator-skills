---
name: youtube-ip-safe-ai-content
description: Copyright, trademark and platform-policy checklist for monetizable AI-made YouTube videos (animated characters, AI voices, music, fonts, on-screen text, made-for-kids signals). Use before generating assets and again before upload. Triggers: "no copyright", "trademark", "can I monetize", "is this voice/music/font allowed", "made for kids", "AI disclosure", "YPP safe".
---

# YouTube IP-Safe AI Content

## When to Use
- Planning or reviewing any AI-assisted video meant for the YouTube Partner Program.
- Choosing voices, music, fonts or tools for a channel.

## When NOT to Use
- Legal advice for a dispute or takedown. Escalate to the owner and a lawyer.

## Core Workflow
1. **Characters:** original designs; never "in the style of" a studio/show/artist; check look-alikes (famous pig families, flying-ear elephants, etc.).
2. **Names:** search the channel/character name on YouTube and in trademark registers (USPTO, the owner's national IP office, EUIPO; class 41 for education/entertainment). The owner runs the official register search.
3. **Places & props:** generic only. No real airport/agency/airline/transit names, logos, crests, uniforms with emblems, or shop brands. Made-up signs ("Arrivals", "Passport Control").
4. **Voices:** use a source with clear commercial rights. Edge "Read Aloud"/edge-tts has **no clear commercial licence**, so it's excluded. Meta AI native/lip-sync voices: Meta AI Terms (effective 2026-05-13) don't forbid commercial use and make the user responsible. Paid TTS with commercial terms, or human voice, are the safest.
5. **Music & SFX:** synthesise originals in code (owned outright) or use the YouTube Audio Library. Never in-app licensed songs (Content ID).
6. **Fonts:** SIL OFL fonts (e.g. Nunito, Baloo 2 from google/fonts); keep the OFL.txt with the project.
7. **Audience:** teen/adult-facing topics and wording; teen characters drawn as teens, not small children; the owner sets "made for kids" honestly in Studio. Never set it for them.
8. **Disclosure:** clearly animated content usually doesn't need the "altered or synthetic" label; the owner decides, and disclosing doesn't hurt reach.
9. **Before upload:** QC every frame strip for leaked real names/logos (AI models add them on screens and signs).

## Project Context (2026-11-20)
- Meta AI generated "UK BORDER FORCE" on a screen and a real airport sign in one clip despite "no logos". Explicit word-level negatives fixed it.
- Meta AI refused a 16-year-old character addressing the camera as a teacher; switched the host to an adult animal character.
- EP2: money as a plot point (no British money) was shown with **no banknotes or coins at all**: real note designs and royal portraits (Bank of England, Thai baht) are a legal and cultural risk. The cliffhanger is a spoken line and a worried face.
- EP2: Meta treats Pudding as a baby. It refused scenes of him left alone ("wait here"), visibly upset, or silently coached by an adult. Accept Meta's own alternative; never reword around the refusal. These refusals also keep the content clearly non-exploitative, which matters for a cute-character channel set to "not made for kids".
- EP2: a character that morphs mid-clip can gain an emblem (a crown badge on a cap). Treat any badge/crest that appears as an IP QC failure.
- EP3 (money episode): amounts are only spoken ("five thousand baht", "three pounds"); every AI prompt (masters, clips, thumbnail art) names the banned items: banknotes, coins, paper money, cash, wallets, currency symbols, exchange-rate boards, flags. The exchange counter is generic (blank screen, no bureau/bank name). Prices appear only as typed text on our own lesson cards. Zero money visible in 26 clips + 4 images.
- EP3: Meta refused an adult character speaking to Pudding in the same frame, and a goodbye-wave exchange with him. Its alternative (the adult alone) was accepted and the scene was cut as shot / reverse shot. This is accepting Meta's offer, not working around the refusal: no prompt was reworded to get the refused content.
- EP3 taxi rank: generic black cartoon cars with no roof sign text, logos or plates; crowd seen from behind; Pudding is with Ollie, not alone, and cheerful rather than upset.
- AI-use note in the description: EP.1's wording "Animation made with AI tools. Story, script and lessons written and directed by the Pudding team." (EP.2 was uploaded without it).

## Constraints
**MUST DO**
- Record each asset's source and licence in the project doc.
- Ask the owner before downloads/installs, uploads, and any public visibility.

**MUST NOT DO**
- Publish publicly or set the audience setting on the owner's behalf.
- Work around an AI tool's safety refusal.

## Decision Frameworks
- Licence unclear → exclude it. Use an owned or clearly licensed alternative.
- Real brand visible for under 1 s in the background → still regenerate or crop; don't rely on blur.

## Common Pitfalls
- "No logos" alone isn't enough. Name the specific words to avoid.
- Scene-label words in prompts can appear as signage.

## Output Templates
| Element | Rule | Status |
| --- | --- | --- |
| Voices | Meta AI native audio (terms checked YYYY-MM-DD) | OK |
