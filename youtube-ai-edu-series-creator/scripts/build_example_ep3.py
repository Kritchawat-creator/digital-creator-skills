"""Assemble Pudding EP3 "Changing Money" (16:9, 1920x1080) from QC-passed Meta AI clips, Pillow cards,
original music/SFX, burned-in English subtitles, and EN/TH .srt files.

Run: E:/claude-work/pudding-ep1/.venv/Scripts/python.exe build.py [plan]   (from E:/claude-work/pudding-ep3)
Output: out/pudding_ep3.mp4, out/pudding_ep3.en.srt, out/pudding_ep3.th.srt
"""
import os
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1920, 1080, 30
NAVY, CREAM, YELLOW = (31, 42, 68), (255, 246, 229), (255, 201, 60)
RED, GREEN, MINT, WHITE = (229, 72, 77), (46, 173, 107), (143, 217, 196), (255, 255, 255)
BALOO, NUNITO = "fonts/Baloo2[wght].ttf", "fonts/Nunito[wght].ttf"
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
    """Blurred EP.3 counter master under a cream wash, so cards stay in the same world."""
    global _BG
    if _BG is None:
        bg = Image.open("masters/counter_master.png").convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
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

# Biscuit story lines are Biscuit-alone clips (Meta's alternative after it refused Biscuit speaking to Pudding in the
# two-shot). They are cropped to a medium shot so they read as a reverse shot of the counter, not as Pudding vanishing.
MED = "768:432:100:90"

# Sentence-timed subtitles: (seconds from the clip's in point, EN, TH). Times = measured speech onsets - ~0.2 s
# (edl.tsv). EP.2 lesson: a whole-line subtitle shown before the words reads as "subtitles don't match lip sync".
CUES = {
    "ep2_P05": [(0.0, "The train is over there.", "รถไฟอยู่ทางนั้น"), (3.3, "Do you have pounds?", "เธอมีเงินปอนด์ไหม?")],
    "ep2_P06": [(0.0, "Pounds?", "ปอนด์?"), (1.7, "Oh no...", "แย่แล้ว..."), (4.0, "I don't have any British money!", "ฉันไม่มีเงินอังกฤษเลย!")],
    "A2b": [(0.0, "You mean:", "หมายถึง:"), (1.1, "Where can I change money?", "ฉันแลกเงินได้ที่ไหน?"),
            (3.6, "It's over there!", "อยู่ทางนั้นไง!")],
    "C01": [(0.0, "You again!", "เธออีกแล้ว!"), (1.4, "Hello, Pudding!", "สวัสดี พุดดิ้ง!")],
    "C02": [(0.0, "Hello!", "สวัสดี!"), (1.7, "I'd like to change some money, please.", "ฉันอยากแลกเงินหน่อย")],
    "C03": [(0.0, "Sure!", "ได้เลย!"), (0.9, "How much would you like to change?", "จะแลกเท่าไหร่ดี?")],
    "C04": [(0.0, "Sorry,", "ขอโทษนะ"), (1.0, "could you say that again, slowly?", "ช่วยพูดอีกครั้งช้าๆ ได้ไหม?")],
    "C05": [(0.0, "How much...", "จะแลก... เท่าไหร่... ดี?"), (2.3, "How much... would you like...", "จะแลก... เท่าไหร่... ดี?"),
            (3.8, "How much... would you like... to change?", "จะแลก... เท่าไหร่... ดี?")],
    "C07c": [(0.0, "OK.", "โอเค"), (1.5, "There is a small fee.", "มีค่าธรรมเนียมนิดหน่อยนะ")],
    "C10b": [(0.0, "All done!", "เรียบร้อย!"), (1.5, "Have a nice day!", "ขอให้มีวันที่ดีนะ!")],
    "T01c": [(0.0, "Oh no!", "แย่แล้ว!"), (2.1, "Look at that queue!", "ดูคิวนั่นสิ!")],
    "H6": [(0.0, "Pudding has British money now!", "ตอนนี้พุดดิ้งมีเงินอังกฤษแล้ว!"),
           (3.0, "But can he get a taxi?", "แต่เขาจะได้แท็กซี่ไหมนะ?"), (4.9, "Find out in episode four!", "ติดตามในตอนที่ 4!")],
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

# Host clips (Biscuit alone at the counter, to camera). Each has two takes; the dead air between them is cut:
# (clip, take1 in/out, take2 in/out, take2 crop, phrase, example, th, example_th, shadow voice (in, out))
PHRASES = [
    ("H1", (0.2, 2.6), (6.8, 8.9), MED, "Where can I change money?", "Where can I buy a ticket?",
     "ฉันแลกเงินได้ที่ไหน?", "ฉันซื้อตั๋วได้ที่ไหน?", (6.9, 9.0)),
    ("H2", (0.3, 2.6), (6.1, 8.2), None, "I'd like to change some money, please.", "I'd like a coffee, please.",
     "ฉันอยากแลกเงินหน่อย", "ขอกาแฟหนึ่งแก้วค่ะ/ครับ", (6.2, 8.1)),
    ("H3", (1.1, 2.4), (5.7, 6.9), MED, "How much is it?", "How much is the ticket?",
     "ราคาเท่าไหร่?", "ตั๋วราคาเท่าไหร่?", (5.8, 6.8)),
    ("H4", (0.9, 2.5), (6.6, 8.4), MED, "It's three pounds.", "It's ten pounds fifty.",
     "สามปอนด์", "สิบปอนด์ห้าสิบเพนนี", (6.7, 8.3)),
    ("H5", (1.2, 2.6), (6.3, 7.8), MED, "Have a nice day!", "Thank you! You too!",
     "ขอให้มีวันที่ดีนะ!", "ขอบคุณ! เช่นกันนะ!", (6.4, 7.9)),
]

# --- HOOK
clip("A1", 0.5, 3.0, sub="Where I can change money?", banner="Don't say this!", icon="cross", icon_at=1.2,
     sfx=[("buzz", 1.3)], th="ฉันแลกเงินได้ที่ไหน? (เรียงคำผิด)")
card(3.2, title="Pudding Goes to London", lines=[L("Episode 3 · Changing Money", GREY, 70)], sfx=[("sting", 0)],
     th="พุดดิ้งไปลอนดอน ตอนที่ 3 · แลกเงิน")
# --- LAST TIME (EP.2 cliffhanger, accepted EP.2 cuts reused as files)
card(2.6, title="Last time on Pudding...", sfx=[("whoosh", 0)], th="ตอนที่แล้ว...")
clip("ep2_P05", 0.6, 5.9, sub="The train is over there. Do you have pounds?", th="รถไฟอยู่ทางนั้น เธอมีเงินปอนด์ไหม?")
clip("ep2_P06", 2.2, 9.0, sub="Pounds? Oh no... I don't have any British money!", sfx=[("buzz", 6.0)],
     th="ปอนด์? แย่แล้ว... ฉันไม่มีเงินอังกฤษเลย!")
# --- STORY: belt (Ollie) -> exchange counter (Biscuit)
belt = [
    ("A1", 0.5, 3.0, "Where I can change money?", "ฉันแลกเงินได้ที่ไหน? (เรียงคำผิด)",
     dict(icon="cross", icon_at=1.2, sfx=[("buzz", 1.3)])),
    ("A2b", 1.6, 6.5, "You mean: Where can I change money? It's over there!", "หมายถึง: ฉันแลกเงินได้ที่ไหน? อยู่ทางนั้นไง!",
     dict(icon="check", icon_at=1.3, sfx=[("ding", 1.4)])),
]
for n, a, b, s, th, extra in belt:
    clip(n, a, b, sub=s, th=th, **extra)
card(2.4, title="At the exchange counter...", sfx=[("whoosh", 0)], th="ที่เคาน์เตอร์แลกเงิน...")
desk = [
    ("C01", 0.7, 4.2, "You again! Hello, Pudding!", "เธออีกแล้ว! สวัสดี พุดดิ้ง!", dict(crop=MED)),
    ("C02", 1.0, 5.2, "Hello! I'd like to change some money, please.", "สวัสดี! ฉันอยากแลกเงินหน่อย", {}),
    ("C03", 4.0, 6.7, "Sure! How much would you like to change?", "ได้เลย! จะแลกเท่าไหร่ดี?", dict(crop=MED, tag=FAST)),
    ("C04", 1.9, 5.7, "Sorry, could you say that again, slowly?", "ขอโทษนะ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?", {}),
    ("C05", 1.5, 6.3, "How much would you like to change?", "จะแลก... เท่าไหร่... ดี?", dict(crop=MED, tag=SLOW)),
    ("C06", 0.8, 3.2, "Five thousand baht, please.", "ขอห้าพันบาท", {}),
    ("C07c", 5.1, 8.1, "OK. There is a small fee.", "โอเค มีค่าธรรมเนียมนิดหน่อยนะ", dict(crop=MED)),
    ("C08", 2.5, 3.8, "How much is it?", "ราคาเท่าไหร่?", {}),
    ("C09", 2.6, 4.4, "It's three pounds.", "สามปอนด์", dict(crop=MED)),
    ("C10b", 2.0, 5.1, "All done! Have a nice day!", "เรียบร้อย! ขอให้มีวันที่ดีนะ!", dict(crop=MED)),
]
for n, a, b, s, th, extra in desk:
    clip(n, a, b, sub=s, th=th, **extra)
card(2.4, title="Outside, at the taxi rank...", sfx=[("whoosh", 0)], th="ข้างนอก ที่จุดรอแท็กซี่...")
clip("T01c", 1.0, 5.0, sub="Oh no! Look at that queue!", sfx=[("buzz", 3.6)], th="แย่แล้ว! ดูคิวนั่นสิ!")
card(3.6, title="Oh no, Pudding!", lines=[L("But first... let's learn the English!", GREY, 66)],
     sfx=[("whoosh", 0), ("sting", 0.4)], th="แย่แล้วพุดดิ้ง! แต่ก่อนอื่น... มาเรียนภาษาอังกฤษกัน!")
# --- 5 PHRASES (Biscuit on his own, to camera; two takes, the dead air between them cut)
card(3.0, title="5 Phrases for Changing Money", sfx=[("sting", 0)], th="5 วลีสำหรับการแลกเงิน")
for i, (n, (a1, b1), (a2, b2), crop2, p, ex, pth, exth, _v) in enumerate(PHRASES, 1):
    clip(n, a1, b1, sub=p, tag=(f"PHRASE {i}/5 · listen twice", NAVY), sfx=[("pop", 0.1)], th=pth)
    clip(n, a2, b2, sub=p, tag=(f"PHRASE {i}/5 · again", NAVY), th=pth, crop=crop2)
    voice = ("H5b", 1.7, 4.8, 1.3) if n == "H5" else None  # Meta's "Thank you! You too!" demo (after the C11 refusal)
    card(4.6 if voice is None else 5.0, badge=(f"PHRASE {i}/5", NAVY),
         lines=[L(p, NAVY, 92), L("You can also say:" if n != "H5" else "Answer:", (110, 110, 130), 54), L(ex, GREEN, 80)],
         sfx=[("pop", 0.15)] + ([] if voice else [("pop", 1.4)]), voice=voice,
         srt=f"{p} / {'You can also say' if n != 'H5' else 'Answer'}: {ex}",
         th=f"{pth} / {'พูดแบบนี้ก็ได้' if n != 'H5' else 'ตอบว่า'}: {exth}")
# --- COMMON MISTAKE + GRAMMAR: question word order
card(3.0, title="Common Mistake", sfx=[("whoosh", 0), ("sting", 0.3)], th="ข้อผิดพลาดที่พบบ่อย")
clip("A1", 0.5, 3.0, sub="Where I can change money?", icon="cross", icon_at=1.2, sfx=[("buzz", 1.3)],
     th="ฉันแลกเงินได้ที่ไหน? (เรียงคำผิด)")
clip("A2b", 1.6, 6.5, sub="You mean: Where can I change money? It's over there!", icon="check", icon_at=1.3,
     sfx=[("ding", 1.4)], th="หมายถึง: ฉันแลกเงินได้ที่ไหน? อยู่ทางนั้นไง! (ถูก)")
card(6.0, lines=[L("Where I can change money?", RED, 84), L("Where can I change money?", GREEN, 84)], icon="check",
     sfx=[("buzz", 0.2), ("ding", 1.8)], srt="Not: Where I can change money? Say: Where can I change money?",
     th="อย่าพูดว่า Where I can change money? ให้พูดว่า Where can I change money?")
card(7.0, title="Question word + verb + subject", lines=[L("Where  can I  change money?", GREEN, 80),
                                                       L("How much  is it?", GREEN, 80),
                                                       L("Not: How much it is?", RED, 60)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="Question word + verb + subject: Where can I change money? How much is it? Not: How much it is?",
     th="คำถาม + กริยาช่วย + ประธาน: ภาษาไทยใช้ลำดับเหมือนประโยคบอกเล่า แต่ภาษาอังกฤษสลับกริยาช่วยมาไว้หน้าประธาน")
card(6.0, title="Where? or How much?", lines=[L("Where = a place:  \"Over there.\"", NAVY, 72),
                                              L("How much = a price:  \"It's three pounds.\"", NAVY, 72)],
     sfx=[("pop", 0.2), ("pop", 1.8)], srt="Where asks for a place: Over there. How much asks for a price: It's three pounds.",
     th="Where ถามสถานที่: Over there. (อยู่ทางนั้น) · How much ถามราคา: It's three pounds. (สามปอนด์)")
card(7.0, title="Saying Prices", lines=[L("£3  =  three pounds", NAVY, 76), L("£10.50  =  ten pounds fifty", NAVY, 76),
                                        L("£1  =  one pound  (not \"one pounds\")", GREEN, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="Saying prices: £3 = three pounds. £10.50 = ten pounds fifty. £1 = one pound, not one pounds.",
     th="การพูดราคา: £3 = three pounds · £10.50 = ten pounds fifty · £1 = one pound (ไม่ใช่ one pounds)")
card(7.0, title="More Prices", lines=[L("50p  =  fifty pence", NAVY, 76), L("£2.99  =  two ninety-nine", NAVY, 76),
                                      L("£20  =  twenty pounds", GREEN, 76)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="More prices: 50p = fifty pence. £2.99 = two ninety-nine. £20 = twenty pounds.",
     th="ราคาอื่นๆ: 50p = fifty pence (เพนนี) · £2.99 = two ninety-nine · £20 = twenty pounds")
card(7.0, title="More Questions", lines=[L("Where can I buy a ticket?", NAVY, 74), L("Where can I find a taxi?", NAVY, 74),
                                         L("How much is this?", GREEN, 74)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="More questions: Where can I buy a ticket? Where can I find a taxi? How much is this?",
     th="คำถามอื่นๆ: ฉันซื้อตั๋วได้ที่ไหน? · ฉันเรียกแท็กซี่ได้ที่ไหน? · อันนี้ราคาเท่าไหร่?")
# --- BISCUIT'S FAST ENGLISH
card(3.0, title="Biscuit's Fast English", lines=[L("Can you understand him?", GREY, 62)], sfx=[("sting", 0)],
     th="ภาษาอังกฤษแบบเร็วของบิสกิต ฟังออกไหม?")
clip("C03", 4.0, 6.7, sub="Sure! How much would you like to change?", tag=FAST, crop=MED, th="(พูดเร็ว) ได้เลย! จะแลกเท่าไหร่ดี?")
card(5.0, lines=[L("How much would you like to change?", NAVY, 80), L("= How much money do you want to change?", GREEN, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6)], srt="How much would you like to change? = How much money do you want to change?",
     th="How much would you like to change? = คุณอยากแลกเงินเท่าไหร่?")
clip("C05", 1.5, 6.3, sub="How much would you like to change?", tag=SLOW, crop=MED, th="(พูดช้า) จะแลก... เท่าไหร่... ดี?")
clip("C07c", 5.1, 8.1, sub="OK. There is a small fee.", tag=NORMAL, crop=MED, th="(ความเร็วปกติ) โอเค มีค่าธรรมเนียมนิดหน่อยนะ")
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
    ("Question 1", "Put the words in order:  is / How / it / much", "How much is it?", ("H3", 5.8, 6.8),
     "เรียงคำให้ถูก: is / How / it / much", "How much is it? (ราคาเท่าไหร่?)"),
    ("Question 2", "You need British money. What do you ask?", "Where can I change money?", ("H1", 6.9, 9.0),
     "คุณต้องการเงินอังกฤษ คุณจะถามว่าอะไร?", "Where can I change money? (ฉันแลกเงินได้ที่ไหน?)"),
    ("Question 3", "The fee is £3. What does Biscuit say?", "It's three pounds.", ("C09", 2.8, 4.1),
     "ค่าธรรมเนียมคือ £3 บิสกิตพูดว่าอะไร?", "It's three pounds. (สามปอนด์)"),
    ("Question 4", "Fix the sentence:  \"How much it is?\"", "How much is it?", ("H3", 1.2, 2.3),
     "แก้ประโยคให้ถูก: How much it is?", "How much is it? (ราคาเท่าไหร่?)"),
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
for n, a, b, s, th, extra in [belt[1], desk[1], desk[5], desk[6], desk[7], desk[8], desk[9]]:
    clip(n, a, b, sub=s, th=th, **{k: v for k, v in extra.items() if k not in ("tag", "icon", "icon_at", "sfx")})
# --- CLIFFHANGER + END SCREEN
clip("T01c", 1.0, 5.0, sub="Oh no! Look at that queue!", sfx=[("buzz", 3.6)], th="แย่แล้ว! ดูคิวนั่นสิ!")
clip("H6", 0.2, 7.7, sub="Pudding has British money now! But can he get a taxi? Find out in episode four!",
     th="ตอนนี้พุดดิ้งมีเงินอังกฤษแล้ว! แต่เขาจะได้แท็กซี่ไหมนะ? ติดตามในตอนที่ 4!")
card(16.0, title="Next: EP.4 · Taxi!", lines=[L("Subscribe so you don't miss it!", NAVY, 66)], sfx=[("sting", 0)],
     srt="Next: Episode 4 · Taxi! Subscribe so you don't miss it!", th="ตอนต่อไป: EP.4 แท็กซี่! กดติดตามจะได้ไม่พลาด!")


# ---------------------------------------------------------------- render
def run(args):
    r = subprocess.run([FF, "-v", "error", "-y"] + args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])


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
        af = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.06,afade=t=out:st={dur - 0.1:.2f}:d=0.1[a0]"] + sf
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
            af.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.05,"
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
    # two-pass loudnorm: one pass landed at -15.1 LUFS / -0.5 dBTP on the first EP2 render
    import json
    r = subprocess.run([FF, "-hide_banner", "-i", "build/mix.mov", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["-i", "build/mix.mov", "-map", "0:v", "-map", "0:a", "-af", f"{ln},alimiter=limit=0.79:level=false:attack=3:release=60,aresample=48000", "-c:v", "copy",  # limiter: linear loudnorm left peaks at 0 dBTP
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/pudding_ep3.mp4"])
    for path, rows in [(f"{OUT}/pudding_ep3.en.srt", en), (f"{OUT}/pudding_ep3.th.srt", th)]:
        with open(path, "w", encoding="utf-8") as f:
            for k, (a, b, txt) in enumerate(rows, 1):
                f.write(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(f"DONE total {t:.2f}s")
    # second pass: measure the real integrated loudness of the delivered file
    r = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/pudding_ep3.mp4", "-af", "loudnorm=print_format=summary",
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
    # Glyph check: a character the font lacks renders as an empty box (EP3: "→" in Nunito card lines).
    # Subtitles and card lines use Nunito; titles, tags, badges and banners use Baloo 2.
    for path, texts in [(NUNITO, body), (BALOO, heads)]:
        fnt = ImageFont.truetype(path, 60)
        notdef = bytes(fnt.getmask(""))
        bad = sorted({c for x in texts for c in x if not c.isspace() and bytes(fnt.getmask(c)) == notdef})
        print(f"glyph check {path}: " + ("OK" if not bad else f"MISSING {bad}"))
        assert not bad, f"{path} has no glyph for {bad}"


if __name__ == "__main__":
    import sys
    plan() if sys.argv[1:] == ["plan"] else main()
