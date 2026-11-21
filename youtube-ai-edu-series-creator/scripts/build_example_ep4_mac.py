"""Build Pudding EP4 "Taxi" (16:9, 1920x1080) from QC-passed Meta AI clips, Pillow cards,
original music/SFX, burned-in English subtitles, and EN/TH .srt files.

Same look and structure as pudding-ep3/build.py (owner 2026-11-21: "KEEP CONSISTENT"): style helpers, cards on a
blurred master under a cream wash, navy subtitle bar, tags/badges, music ducking and loudness are copied from EP.3.
Burned-in text is ENGLISH ONLY (global channel); Thai exists only in the .th.srt track.

Run (Mac, from pudding-ep4): python3 build.py [plan]
Output: out/pudding_ep4.mp4, out/pudding_ep4.en.srt, out/pudding_ep4.th.srt
"""
import json
import os
import re
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FF = "ffmpeg"
W, H, FPS = 1920, 1080, 30
NAVY, CREAM, YELLOW = (31, 42, 68), (255, 246, 229), (255, 201, 60)
RED, GREEN, MINT, WHITE = (229, 72, 77), (46, 173, 107), (143, 217, 196), (255, 255, 255)
BALOO, NUNITO = "fonts/Baloo2.ttf", "fonts/Nunito.ttf"
SEG_DIR, OUT = "build/segs", "out"
os.makedirs(SEG_DIR, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def draw_icon(d, kind, cx, cy, r):
    """Big round check or cross badge (drawn with shapes, no glyph fonts needed)."""
    col = GREEN if kind == "check" else RED
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=WHITE, width=10)
    lw = int(r * 0.22)
    if kind == "check":
        d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.38)], fill=WHITE, width=lw, joint="curve")
    else:
        o = r * 0.42
        d.line([(cx - o, cy - o), (cx + o, cy + o)], fill=WHITE, width=lw)
        d.line([(cx - o, cy + o), (cx + o, cy - o)], fill=WHITE, width=lw)


def pill(d, x, y, text, bg, fg=WHITE, size=46):
    f = font(BALOO, size, 800)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 60, y + size + 34], radius=(size + 34) // 2, fill=bg)
    d.text((x + 30, y + 10), text, font=f, fill=fg)


def overlay_png(path, sub=None, tag=None, banner=None, icon=None):
    """Transparent 1920x1080 overlay: subtitle bar, top-left tag, top banner, right icon."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if sub:
        f = font(NUNITO, 58, 800)
        lines = wrap(d, sub, f, 1560)
        lh = 74
        box_h = lh * len(lines) + 40
        y0 = H - 70 - box_h
        widest = max(d.textlength(l, font=f) for l in lines)
        x0 = (W - widest) / 2 - 40
        d.rounded_rectangle([x0, y0, x0 + widest + 80, y0 + box_h], radius=28, fill=(31, 42, 68, 215))
        for i, l in enumerate(lines):
            tw = d.textlength(l, font=f)
            d.text(((W - tw) / 2, y0 + 20 + i * lh), l, font=f, fill=WHITE)
    if tag:
        pill(d, 50, 44, tag[0], tag[1])
    if banner:
        f = font(BALOO, 64, 800)
        tw = d.textlength(banner, font=f)
        d.rounded_rectangle([(W - tw) / 2 - 40, 36, (W + tw) / 2 + 40, 140], radius=30, fill=(255, 201, 60, 240))
        d.text(((W - tw) / 2, 44), banner, font=f, fill=NAVY)
    if icon:
        draw_icon(d, icon, W - 230, 300, 130)
    im.save(path)


_BG = None


def card_bg():
    """Blurred EP.4 taxi-rank master under a cream wash, so cards stay in the same world (as EP.3)."""
    global _BG
    if _BG is None:
        bg = Image.open("masters/taxi_master.png").convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
        _BG = Image.blend(bg, Image.new("RGB", (W, H), CREAM), 0.72)
    return _BG.copy()


def card_png(path, title=None, lines=(), badge=None, icon=None):
    """Full-frame card. lines = [(text, color, size)]."""
    im = card_bg()
    d = ImageDraw.Draw(im)
    if badge:
        pill(d, 80, 60, badge[0], badge[1])
    rows = []  # (text, font, color, advance) measured first so the block can be centred vertically
    if title:
        f = font(BALOO, 112, 800)
        rows += [(l, f, NAVY, 128) for l in wrap(d, title, f, 1700)]
        rows.append((None, None, None, 30))
    for text, color, size in lines:
        f = font(NUNITO, size, 850)
        rows += [(l, f, color, int(size * 1.3)) for l in wrap(d, text, f, 1640)]
        rows.append((None, None, None, 26))
    total = sum(r[3] for r in rows[:-1]) if rows else 0
    y = max(150, (H - total) // 2 - 20)
    for text, f, color, adv in rows:
        if text:
            tw = d.textlength(text, font=f)
            d.text(((W - tw) / 2, y), text, font=f, fill=color)
        y += adv
    if icon:
        draw_icon(d, icon, W - 200, H - 200, 110)
    im.save(path)


# ---------------------------------------------------------------- segments
SEGS, SRT = [], []

RANK = "1024:576:0:144"     # taxi-rank clips: hides the canopy wayfinding sign Meta adds
WHEEL = "768:432:470:40"    # Frank at the wheel: hides the meter numbers
MED = "896:504:192:40"      # host take 2: medium shot of Biscuit (new host master is centred)

# Sentence-timed subtitles: (seconds from the clip's in point, EN, TH), from measured speech onsets (edl.tsv).
CUES = {
    "R01": [(0.1, "Look!", "ดูสิ!"), (1.7, "It's our turn now.", "ถึงตาเราแล้ว")],
    "R06c": [(0.1, "Of course!", "ได้เลยครับ!"), (3.2, "Hop in!", "ขึ้นมาเลย!")],
    "K06b": [(0.1, "Really?", "จริงเหรอ?"), (2.5, "Could you show me tomorrow?", "พรุ่งนี้พาฉันไปดูได้ไหม?")],
    "K08": [(0.1, "Here we are!", "ถึงแล้วครับ!"), (2.3, "The Red Kettle Hotel.", "โรงแรมเรดเคตเทิล")],
    "Z01": [(0.1, "Hello!", "สวัสดี!"), (1.6, "I have a booking.", "ฉันจองห้องไว้")],
    "Z02b": [(0.1, "Hmm...", "อืม..."), (2.0, "Sorry.", "ขอโทษนะคะ"), (4.0, "I can't find your booking.", "หาการจองของคุณไม่เจอค่ะ")],
    "T01": [(0.1, "Oh no!", "แย่แล้ว!"), (2.0, "Look at that queue!", "ดูคิวนั่นสิ!")],
    "H6": [(0.1, "Pudding is at his hotel!", "พุดดิ้งมาถึงโรงแรมแล้ว!"), (2.8, "But where is his booking?", "แต่การจองของเขาหายไปไหน?"),
           (5.1, "Find out in episode five!", "ติดตามได้ในตอนที่ห้า!")],
}


def clip(name, t_in, t_out, sub=None, tag=None, banner=None, icon=None, icon_at=0.0, sfx=(), th=None, crop=None):
    dur = t_out - t_in
    cues = None
    if sub and name in CUES:  # (start, end, en, th) within the segment
        c = CUES[name]
        cues = [(a, c[k + 1][0] if k + 1 < len(c) else dur, en, t) for k, (a, en, t) in enumerate(c)]
    SEGS.append(dict(kind="clip", name=name, t_in=t_in, t_out=t_out, sub=sub, tag=tag, banner=banner, icon=icon,
                     icon_at=icon_at, sfx=list(sfx), dur=dur, th=th, cues=cues, crop=crop))


def card(dur, title=None, lines=(), badge=None, icon=None, voice=None, sfx=(), countdown=None, srt=None, th=None):
    """voice = (clip, t_in, t_out, at); countdown = (start, length) seconds within card."""
    SEGS.append(dict(kind="card", dur=dur, title=title, lines=list(lines), badge=badge, icon=icon,
                     voice=voice, sfx=list(sfx), countdown=countdown, srt=srt, th=th))


FAST, SLOW, NORMAL = ("FAST!", RED), ("SLOW", GREEN), ("NORMAL", (90, 110, 200))
GREY = (90, 90, 120)
L = lambda t, c=NAVY, s=78: (t, c, s)  # noqa: E731

# Host clips (Biscuit alone at the lesson counter, to camera). Two takes each; the dead air between them is cut:
# (clip, take1 in/out, take2 in/out, take2 crop, phrase, example, th, example_th, shadow voice (in, out))
PHRASES = [
    ("H1", (0.6, 2.9), (6.7, 9.0), MED, "Could you take me to the hotel, please?", "Could you take me to the station, please?",
     "ช่วยพาฉันไปที่โรงแรมหน่อยได้ไหม?", "ช่วยพาฉันไปสถานีหน่อยได้ไหม?", (6.7, 9.0)),
    ("H2", (0.6, 2.5), (5.8, 7.8), MED, "How long does it take?", "How long does it take to the airport?",
     "ใช้เวลานานแค่ไหน?", "ไปสนามบินใช้เวลานานแค่ไหน?", (5.8, 7.8)),
    ("H3", (1.7, 4.0), (5.4, 7.3), MED, "It takes about forty minutes.", "It takes about ten minutes.",
     "ใช้เวลาประมาณสี่สิบนาที", "ใช้เวลาประมาณสิบนาที", (5.4, 7.3)),
    ("H4", (2.0, 3.8), (6.8, 9.0), MED, "Could you say that again, please?", "Could you speak more slowly, please?",
     "ช่วยพูดอีกครั้งได้ไหม?", "ช่วยพูดช้าลงหน่อยได้ไหม?", (6.8, 9.0)),
    ("H5", (0.7, 2.5), (6.0, 8.0), MED, "Could you stop here, please?", "Could you open the window, please?",
     "ช่วยจอดตรงนี้หน่อยได้ไหม?", "ช่วยเปิดหน้าต่างหน่อยได้ไหม?", (6.0, 8.0)),
]

# --- HOOK
clip("R03", 2.7, 4.4, sub="Go to hotel!", banner="Don't say this!", icon="cross", icon_at=0.9, sfx=[("buzz", 1.0)],
     th="ไปโรงแรม! (พูดไม่สุภาพ/ไม่ครบ)", crop=RANK)
card(3.2, title="Pudding Goes to London", lines=[L("Episode 4 · Taxi", GREY, 70)], sfx=[("sting", 0)],
     th="พุดดิ้งไปลอนดอน ตอนที่ 4 · แท็กซี่")
# --- LAST TIME (EP.3 cliffhanger, re-made in the new Meta AI account at the same taxi rank)
card(2.6, title="Last time on Pudding...", sfx=[("whoosh", 0)], th="ตอนที่แล้ว...")
clip("T01", 2.0, 6.2, sub="Oh no! Look at that queue!", sfx=[("buzz", 3.8)], th="แย่แล้ว! ดูคิวนั่นสิ!", crop=RANK)
# --- STORY: taxi rank (Ollie, Frank) -> in the taxi -> (hotel kept for the cliffhanger)
card(2.4, title="At the taxi rank...", sfx=[("whoosh", 0)], th="ที่จุดขึ้นแท็กซี่...")
rank = [
    ("R01", 1.3, 4.1, "Look! It's our turn now.", "ดูสิ! ถึงตาเราแล้ว", dict(crop=RANK)),
    ("R02", 0.9, 2.7, "Where would you like to go?", "อยากไปที่ไหนครับ?", dict(tag=FAST)),
    ("R03", 2.7, 4.4, "Go to hotel!", "ไปโรงแรม! (พูดไม่สุภาพ/ไม่ครบ)", dict(crop=RANK, icon="cross", icon_at=0.9, sfx=[("buzz", 1.0)])),
    ("R04b", 0.1, 3.4, "Try: Could you take me to the hotel, please?", "ลองพูดว่า: ช่วยพาฉันไปโรงแรมหน่อยได้ไหม?",
     dict(crop=RANK, icon="check", icon_at=0.4, sfx=[("ding", 0.5)])),
    ("R05", 1.8, 6.2, "Could you take me to the Red Kettle Hotel, please?", "ช่วยพาฉันไปโรงแรมเรดเคตเทิลหน่อยได้ไหม?", dict(crop=RANK)),
    ("R06c", 0.8, 5.2, "Of course! Hop in!", "ได้เลยครับ! ขึ้นมาเลย!", {}),
]
for n, a, b, s, th, extra in rank:
    clip(n, a, b, sub=s, th=th, **extra)
card(2.4, title="In the taxi...", sfx=[("whoosh", 0)], th="ในแท็กซี่...")
cab = [
    ("K01b", 4.8, 6.4, "How long does it take?", "ใช้เวลานานแค่ไหน?", {}),
    ("K02", 3.6, 5.4, "It takes about forty minutes.", "ใช้เวลาประมาณสี่สิบนาทีครับ", dict(crop=WHEEL, tag=FAST)),
    ("K03", 1.5, 5.6, "Sorry, could you say that again, slowly?", "ขอโทษนะ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?", {}),
    ("K04", 2.9, 6.5, "It takes... about... forty minutes.", "ใช้เวลา... ประมาณ... สี่สิบนาทีครับ", dict(crop=WHEEL, tag=SLOW)),
    ("K05", 4.0, 7.4, "The café where I work is near your hotel!", "คาเฟ่ที่ผมทำงานอยู่ใกล้โรงแรมของนายเลย!", {}),
    ("K06b", 1.7, 6.0, "Really? Could you show me tomorrow?", "จริงเหรอ? พรุ่งนี้พาฉันไปดูได้ไหม?", {}),
    ("K07", 1.6, 2.7, "Sure!", "ได้สิ!", {}),
    ("K08", 0.5, 5.2, "Here we are! The Red Kettle Hotel.", "ถึงแล้วครับ! โรงแรมเรดเคตเทิล", dict(crop=WHEEL)),
]
for n, a, b, s, th, extra in cab:
    clip(n, a, b, sub=s, th=th, **extra)
card(2.4, title="At the Red Kettle Hotel...", sfx=[("whoosh", 0)], th="ที่โรงแรมเรดเคตเทิล...")
clip("Z01", 2.9, 5.7, sub="Hello! I have a booking.", th="สวัสดี! ฉันจองห้องไว้")
clip("Z02b", 1.6, 7.0, sub="Hmm... Sorry. I can't find your booking.", sfx=[("buzz", 5.3)], th="อืม... ขอโทษนะคะ หาการจองของคุณไม่เจอค่ะ")
card(3.6, title="Oh no, Pudding!", lines=[L("But first... let's learn the English!", GREY, 66)],
     sfx=[("whoosh", 0), ("sting", 0.4)], th="แย่แล้วพุดดิ้ง! แต่ก่อนอื่น... มาเรียนภาษาอังกฤษกัน!")
# --- 5 PHRASES (Biscuit on his own, to camera; two takes, the dead air between them cut)
card(3.0, title="5 Phrases for a Taxi Ride", sfx=[("sting", 0)], th="5 วลีสำหรับนั่งแท็กซี่")
for i, (n, (a1, b1), (a2, b2), crop2, p, ex, pth, exth, _v) in enumerate(PHRASES, 1):
    clip(n, a1, b1, sub=p, tag=(f"PHRASE {i}/5 · listen twice", NAVY), sfx=[("pop", 0.1)], th=pth)
    clip(n, a2, b2, sub=p, tag=(f"PHRASE {i}/5 · again", NAVY), th=pth, crop=crop2)
    card(4.6, badge=(f"PHRASE {i}/5", NAVY),
         lines=[L(p, NAVY, 92), L("You can also say:", (110, 110, 130), 54), L(ex, GREEN, 80)],
         sfx=[("pop", 0.15), ("pop", 1.4)], srt=f"{p} / You can also say: {ex}", th=f"{pth} / พูดแบบนี้ก็ได้: {exth}")
# --- COMMON MISTAKE + GRAMMAR: Could you ...? / How long does it take?
card(3.0, title="Common Mistake", sfx=[("whoosh", 0), ("sting", 0.3)], th="ข้อผิดพลาดที่พบบ่อย")
clip("R03", 2.7, 4.4, sub="Go to hotel!", icon="cross", icon_at=0.9, sfx=[("buzz", 1.0)], th="ไปโรงแรม! (พูดไม่สุภาพ/ไม่ครบ)", crop=RANK)
clip("R04b", 0.1, 3.4, sub="Try: Could you take me to the hotel, please?", icon="check", icon_at=0.4, sfx=[("ding", 0.5)],
     th="ลองพูดว่า: ช่วยพาฉันไปโรงแรมหน่อยได้ไหม? (ถูก)", crop=RANK)
card(6.0, lines=[L("Go to hotel!", RED, 84), L("Could you take me to the hotel, please?", GREEN, 84)], icon="check",
     sfx=[("buzz", 0.2), ("ding", 1.8)], srt="Not: Go to hotel! Say: Could you take me to the hotel, please?",
     th="อย่าพูดว่า Go to hotel! ให้พูดว่า Could you take me to the hotel, please?")
card(7.0, title="Could you + verb ... ?", lines=[L("Could you  take  me to the station?", GREEN, 76),
                                                 L("Could you  stop  here?", GREEN, 76),
                                                 L("Answer: Sure! / Of course!", NAVY, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="Could you + verb: Could you take me to the station? Could you stop here? Answer: Sure! / Of course!",
     th="Could you + กริยา: ใช้ขอร้องอย่างสุภาพ · ตอบว่า Sure! / Of course!")
card(7.0, title="How long does it take?", lines=[L("How long  does  it take?", GREEN, 80),
                                                 L("It takes about forty minutes.", NAVY, 72),
                                                 L("Not: How long it takes?", RED, 60)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="How long does it take? It takes about forty minutes. Not: How long it takes?",
     th="คำถามต้องมี does: How long does it take? · ตอบว่า It takes about ... minutes.")
card(7.0, title="More Taxi Phrases", lines=[L("Could you open the boot, please?", NAVY, 72),
                                            L("Could you turn on the heating, please?", NAVY, 72),
                                            L("Boot = the back of the car (UK)", GREEN, 60)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="More taxi phrases: Could you open the boot, please? Could you turn on the heating, please? Boot = the back of the car (UK).",
     th="ประโยคในแท็กซี่เพิ่มเติม: ช่วยเปิดท้ายรถหน่อย · ช่วยเปิดฮีตเตอร์หน่อย · boot = ท้ายรถ (อังกฤษ)")
card(7.0, title="How Long?", lines=[L("It takes about ten minutes.", NAVY, 74), L("It takes about an hour.", NAVY, 74),
                                    L("It takes about forty minutes.", GREEN, 74)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="How long? It takes about ten minutes. It takes about an hour. It takes about forty minutes.",
     th="ใช้เวลานานแค่ไหน: ประมาณสิบนาที · ประมาณหนึ่งชั่วโมง · ประมาณสี่สิบนาที")
# --- FRANK'S FAST ENGLISH (EP.3: "Biscuit's Fast English")
card(3.0, title="Frank's Fast English", lines=[L("Can you understand him?", GREY, 62)], sfx=[("sting", 0)],
     th="ภาษาอังกฤษแบบเร็วของแฟรงก์ ฟังออกไหม?")
clip("R02", 0.9, 2.7, sub="Where would you like to go?", tag=FAST, th="(พูดเร็ว) อยากไปที่ไหนครับ?")
card(5.0, lines=[L("Where would you like to go?", NAVY, 80), L("= Where do you want to go?", GREEN, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6)], srt="Where would you like to go? = Where do you want to go?",
     th="Where would you like to go? = อยากไปที่ไหน?")
clip("K02", 3.6, 5.4, sub="It takes about forty minutes.", tag=FAST, crop=WHEEL, th="(พูดเร็ว) ใช้เวลาประมาณสี่สิบนาทีครับ")
clip("K04", 2.9, 6.5, sub="It takes... about... forty minutes.", tag=SLOW, crop=WHEEL, th="(พูดช้า) ใช้เวลา... ประมาณ... สี่สิบนาทีครับ")
clip("K08", 0.5, 5.2, sub="Here we are! The Red Kettle Hotel.", tag=NORMAL, crop=WHEEL, th="(ความเร็วปกติ) ถึงแล้วครับ! โรงแรมเรดเคตเทิล")
# --- SHADOWING
card(3.2, title="Say It With Pudding!", lines=[L("Listen... then say it out loud!", GREY, 62)], sfx=[("sting", 0)],
     th="พูดตามพุดดิ้ง! ฟังแล้วพูดออกเสียงตาม")
for i, (n, _t1, _t2, _c, p, ex, pth, exth, (va, vb)) in enumerate(PHRASES, 1):
    vd = vb - va
    card(vd + 3.2, badge=(f"YOUR TURN {i}/5", GREEN), lines=[L(p, NAVY, 92), L("Now you!", GREEN, 70)],
         voice=(n, va, vb, 0.2), countdown=(vd + 0.4, 2.8),
         sfx=[("tick", vd + 0.4 + k * 0.7) for k in range(4)], srt=p, th=f"{pth} (พูดตาม)")
# --- QUIZ
card(3.0, title="Quiz Time!", lines=[L("4 questions. Answer before the timer ends!", GREY, 58)], sfx=[("sting", 0)],
     th="ควิซ! 4 คำถาม ตอบก่อนหมดเวลา!")
QUIZ = [
    ("Question 1", "Put the words in order:  please / Could / take / me / you / to the hotel",
     "Could you take me to the hotel, please?", ("H1", 6.7, 9.0),
     "เรียงคำให้ถูก: please / Could / take / me / you / to the hotel", "Could you take me to the hotel, please? (ช่วยพาฉันไปโรงแรมหน่อยได้ไหม?)"),
    ("Question 2", "You want to know the time of the trip. What do you ask?", "How long does it take?", ("H2", 5.8, 7.8),
     "คุณอยากรู้ว่าใช้เวลานานแค่ไหน คุณจะถามว่าอะไร?", "How long does it take? (ใช้เวลานานแค่ไหน?)"),
    ("Question 3", "Fix the sentence:  \"Go to hotel!\"", "Could you take me to the hotel, please?", ("H1", 0.6, 2.9),
     "แก้ประโยคให้ถูก: Go to hotel!", "Could you take me to the hotel, please? (ช่วยพาฉันไปโรงแรมหน่อยได้ไหม?)"),
    ("Question 4", "Fix the sentence:  \"How long it takes?\"", "How long does it take?", ("K01b", 4.8, 6.4),
     "แก้ประโยคให้ถูก: How long it takes?", "How long does it take? (ใช้เวลานานแค่ไหน?)"),
]
for qn, q, ans, (vc, va, vb), qth, ath in QUIZ:
    card(6.0, badge=(qn, NAVY), lines=[L(q, NAVY, 76)], countdown=(0.8, 5.0),
         sfx=[("pop", 0.1)] + [("tick", 0.8 + k) for k in range(5)], srt=q, th=qth)
    card((vb - va) + 2.0, badge=("Answer", GREEN), lines=[L(ans, GREEN, 92)], icon="check",
         voice=(vc, va, vb, 0.6), sfx=[("ding", 0.1)], srt=ans, th=ath)
card(4.0, title="Write your answers in the comments!", sfx=[("pop", 0.2)], th="เขียนคำตอบไว้ในคอมเมนต์นะ!")
# --- WATCH AGAIN (comprehension replay)
card(3.4, title="Watch Again", lines=[L("Now you understand every word!", GREY, 62)], sfx=[("whoosh", 0), ("sting", 0.3)],
     th="ดูอีกครั้ง ตอนนี้คุณเข้าใจทุกคำแล้ว!")
for n, a, b, s, th, extra in [rank[3], rank[4], rank[5], cab[0], cab[1], cab[7]]:
    clip(n, a, b, sub=s, th=th, **{k: v for k, v in extra.items() if k not in ("tag", "icon", "icon_at", "sfx")})
# --- CLIFFHANGER + END SCREEN
clip("Z02b", 1.6, 7.0, sub="Hmm... Sorry. I can't find your booking.", sfx=[("buzz", 5.3)], th="อืม... ขอโทษนะคะ หาการจองของคุณไม่เจอค่ะ")
clip("H6", 0.4, 7.6, sub="Pudding is at his hotel! But where is his booking? Find out in episode five!",
     th="พุดดิ้งมาถึงโรงแรมแล้ว! แต่การจองของเขาหายไปไหน? ติดตามได้ในตอนที่ห้า!")
card(16.0, title="Next: EP.5 · Hotel Check-in!", lines=[L("Subscribe so you don't miss it!", NAVY, 66)], sfx=[("sting", 0)],
     srt="Next: Episode 5 · Hotel Check-in! Subscribe so you don't miss it!", th="ตอนต่อไป: EP.5 เช็กอินที่โรงแรม! กดติดตามจะได้ไม่พลาด!")


# ---------------------------------------------------------------- render
def run(args):
    r = subprocess.run([FF, "-v", "error", "-y"] + args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])


_GAIN = {}


def clip_gain(name, a, b):
    """EP.4 addition: level-match clips from two Meta AI accounts (host clips came out ~10 dB quieter)."""
    if (name, a, b) not in _GAIN:
        r = subprocess.run([FF, "-hide_banner", "-ss", str(a), "-t", f"{b - a:.3f}", "-i", f"clips/{name}.mp4", "-af",
                            "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
        m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', r)
        _GAIN[(name, a, b)] = max(-10.0, min(12.0, -18.0 - float(m.group(1)))) if m else 0.0
    return _GAIN[(name, a, b)]


def sfx_inputs(sfx, base_idx):
    """Return (extra ffmpeg inputs, filter labels) for sfx list placed with adelay."""
    ins, labels, filt = [], [], []
    for k, (name, at) in enumerate(sfx):
        ins += ["-i", f"audio/sfx_{name}.wav"]
        lab = f"s{k}"
        ms = int(at * 1000)
        filt.append(f"[{base_idx + k}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.55,adelay={ms}|{ms}[{lab}]")
        labels.append(f"[{lab}]")
    return ins, labels, filt


def render(i, s):
    out = f"{SEG_DIR}/seg_{i:03d}.mov"
    dur = s["dur"]
    if s["kind"] == "clip":
        ov = f"build/ov_{i:03d}.png"
        overlay_png(ov, sub=None if s["cues"] else s["sub"], tag=s["tag"], banner=s["banner"])
        args = ["-ss", f"{s['t_in']}", "-t", f"{dur}", "-i", f"clips/{s['name']}.mp4", "-loop", "1", "-t", f"{dur}", "-i", ov]
        crop = f"crop={s['crop']}," if s.get("crop") else ""
        vf = f"[0:v]{crop}scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[b];[b][1:v]overlay=0:0[v1]"
        idx, vlast = 2, "[v1]"
        if s["icon"]:
            ic = f"build/ic_{i:03d}.png"
            overlay_png(ic, icon=s["icon"])
            args += ["-loop", "1", "-t", f"{dur}", "-i", ic]
            vf += f";{vlast}[{idx}:v]overlay=0:0:enable='gte(t,{s['icon_at']})'[vi]"
            vlast, idx = "[vi]", idx + 1
        for k, (a, b, en, _th) in enumerate(s["cues"] or []):  # one subtitle PNG per spoken sentence
            cp = f"build/cue_{i:03d}_{k}.png"
            overlay_png(cp, sub=en)
            args += ["-loop", "1", "-t", f"{dur}", "-i", cp]
            vf += f";{vlast}[{idx}:v]overlay=0:0:enable='between(t,{a},{b})'[vc{k}]"
            vlast, idx = f"[vc{k}]", idx + 1
        sin, slab, sf = sfx_inputs(s["sfx"], idx)
        args += sin
        g = clip_gain(s["name"], s["t_in"], s["t_out"])
        af = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.1f}dB,afade=t=in:d=0.06,"
              f"afade=t=out:st={dur - 0.1:.2f}:d=0.1[a0]"] + sf
        mix = f"[a0]{''.join(slab)}amix=inputs={1 + len(slab)}:normalize=0:duration=first[aout]"
        fc = vf + ";" + ";".join(af) + ";" + mix
        args += ["-filter_complex", fc, "-map", vlast, "-map", "[aout]"]
    else:
        png = f"build/card_{i:03d}.png"
        card_png(png, title=s["title"], lines=s["lines"], badge=s["badge"], icon=s["icon"])
        args = ["-loop", "1", "-t", f"{dur}", "-i", png, "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=48000:cl=stereo"]
        zoom = f"scale=w='trunc({W}*(1+0.045*t/{dur})/2)*2':h=-2:eval=frame,crop={W}:{H},fps={FPS},setsar=1"
        if s["countdown"]:
            st, ln = s["countdown"]
            zoom += (f",drawbox=x=0:y={H - 34}:w='{W}*max(0\\,1-(t-{st})/{ln})':h=34:color=0xFFC93C:t=fill"
                     f":enable='between(t,{st},{st + ln})'")
        vf = f"[0:v]{zoom}[vout]"
        idx = 2
        af = ["[1:a]anull[base]"]
        labels = []
        if s["voice"]:
            vc, va, vb, at = s["voice"]
            args += ["-ss", f"{va}", "-t", f"{vb - va}", "-i", f"clips/{vc}.mp4"]
            ms = int(at * 1000)
            g = clip_gain(vc, va, vb)
            af.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.1f}dB,afade=t=in:d=0.05,"
                      f"afade=t=out:st={vb - va - 0.08:.2f}:d=0.08,adelay={ms}|{ms}[vo]")
            labels.append("[vo]")
            idx += 1
        sin, slab, sf = sfx_inputs(s["sfx"], idx)
        args += sin
        af += sf
        labels += slab
        mix = f"[base]{''.join(labels)}amix=inputs={1 + len(labels)}:normalize=0:duration=first[aout]"
        args += ["-filter_complex", vf + ";" + ";".join(af) + ";" + mix, "-map", "[vout]", "-map", "[aout]"]
    args += ["-t", f"{dur}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", f"{FPS}",
             "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", out]
    run(args)
    return out


def ts(t):
    """SRT timestamp from seconds, via integer milliseconds (avoids float drift like 80.9999 -> 01:20,000)."""
    ms = int(round(t * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    files, t, en, th = [], 0.0, [], []
    for i, s in enumerate(SEGS):
        files.append(render(i, s))
        text = s.get("sub") if s["kind"] == "clip" else (s.get("srt") or " ".join(x for x in [s.get("title")] + [l[0] for l in s["lines"]] if x))
        if s.get("cues"):
            for a, b, en_t, th_t in s["cues"]:
                en.append((t + a, t + b, en_t))
                if th and th[-1][2] == th_t and abs(th[-1][1] - (t + a)) < 1e-6:
                    th[-1] = (th[-1][0], t + b, th_t)  # same Thai line continues (e.g. slow word-by-word EN)
                else:
                    th.append((t + a, t + b, th_t))
        elif text:
            en.append((t, t + s["dur"], text))
            if s.get("th"):
                th.append((t, t + s["dur"], s["th"]))
        t += s["dur"]
        print(f"seg {i:03d} {s['kind']:4s} {s['dur']:5.2f}s  total {t:6.2f}s", flush=True)
    with open("build/concat.txt", "w", encoding="utf-8") as f:
        for p in files:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["-f", "concat", "-safe", "0", "-i", "build/concat.txt", "-c", "copy", "build/body.mov"])
    # music bed, ducked under speech with a sidechain compressor, faded at both ends
    run(["-i", "build/body.mov", "-stream_loop", "-1", "-i", "audio/music_loop.wav", "-filter_complex",
         f"[0:a]asplit=2[voice][sc];[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{t:.2f},volume=0.30,"
         f"afade=t=in:d=1.5,afade=t=out:st={t - 3:.2f}:d=3[mus];[mus][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];"
         f"[voice][duck]amix=inputs=2:normalize=0:duration=first[aout]",
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "pcm_s16le", "build/mix.mov"])
    r = subprocess.run([FF, "-hide_banner", "-i", "build/mix.mov", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["-i", "build/mix.mov", "-map", "0:v", "-map", "0:a", "-af", f"{ln},alimiter=limit=0.79:level=false:attack=3:release=60,aresample=48000", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/pudding_ep4.mp4"])
    for path, rows in [(f"{OUT}/pudding_ep4.en.srt", en), (f"{OUT}/pudding_ep4.th.srt", th)]:
        with open(path, "w", encoding="utf-8") as f:
            for k, (a, b, txt) in enumerate(rows, 1):
                f.write(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(f"DONE total {t:.2f}s")
    r = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/pudding_ep4.mp4", "-af", "loudnorm=print_format=summary",
                        "-f", "null", "-"], capture_output=True, text=True)
    print("\n".join(l for l in r.stderr.splitlines() if "Input Integrated" in l or "Input True Peak" in l))


def plan():
    """Dry run: total length, section start times (for chapters) and every burned-in string, for a spell-check
    before rendering. Burned-in text cannot be fixed after upload."""
    t, rows, body, heads = 0.0, [], [], []
    with open("build/burned_text.txt", "w", encoding="utf-8") as f:
        for s in SEGS:
            if s["kind"] == "card" and s.get("title"):
                rows.append(f"{int(t // 60):02d}:{int(t % 60):02d}  {s['title']}")
            texts = [s.get("sub"), s.get("banner"), (s.get("tag") or [None])[0], s.get("title"),
                     (s.get("badge") or [None])[0]] + [l[0] for l in s.get("lines", [])] + [c[2] for c in s.get("cues") or []]
            for x in texts:
                if x:
                    f.write(x + "\n")
            body += [x for x in [s.get("sub")] + [l[0] for l in s.get("lines", [])] + [c[2] for c in s.get("cues") or []] if x]
            heads += [x for x in [s.get("banner"), (s.get("tag") or [None])[0], s.get("title"), (s.get("badge") or [None])[0]] if x]
            t += s["dur"]
    print("\n".join(rows))
    print(f"TOTAL {t:.2f}s ({int(t // 60)}:{t % 60:04.1f})")
    for path, texts in [(NUNITO, body), (BALOO, heads)]:
        fnt = ImageFont.truetype(path, 60)
        notdef = bytes(fnt.getmask(""))
        bad = sorted({c for x in texts for c in x if not c.isspace() and bytes(fnt.getmask(c)) == notdef})
        print(f"glyph check {path}: " + ("OK" if not bad else f"MISSING {bad}"))
        assert not bad, f"{path} has no glyph for {bad}"
    thai = sum(1 for x in body + heads for c in x if "฀" <= c <= "๿")
    print(f"Thai characters burned in: {thai}")
    assert thai == 0, "global channel: no Thai text on screen"


if __name__ == "__main__":
    import sys
    plan() if sys.argv[1:] == ["plan"] else main()
