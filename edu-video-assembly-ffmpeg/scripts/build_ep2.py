"""Assemble Pudding EP2 "The Lost Bag" (16:9, 1920x1080) from QC-passed Meta AI clips, Pillow cards,
original music/SFX, burned-in English subtitles, and EN/TH .srt files.

Run: E:/claude-work/pudding-ep1/.venv/Scripts/python.exe build.py   (from E:/claude-work/pudding-ep2)
Output: out/pudding_ep2.mp4, out/pudding_ep2.en.srt, out/pudding_ep2.th.srt
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
    """Blurred EP.2 desk master under a cream wash, so cards stay in the same world."""
    global _BG
    if _BG is None:
        bg = Image.open("masters/desk_master.png").convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
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


# Sentence-timed subtitles for clips that speak in separate bursts: (seconds from the clip's in point, EN, TH).
# Without them the whole line sat on screen before the mouth said it (owner: "subtitles don't match lip sync").
# Times come from the speech-band timelines in qc_log/edl (burst start minus ~0.2 s).
CUES = {
    "ep1_S13": [(0.0, "Wait...", "เดี๋ยวนะ..."), (2.0, "Wait... where is my bag?!", "เดี๋ยวนะ... กระเป๋าฉันอยู่ไหน?!")],
    "L01": [(0.0, "Oh, it's you again!", "อ้าว เธออีกแล้ว!"), (2.4, "Can I help you?", "มีอะไรให้ช่วยไหม?")],
    "L02f": [(0.0, "Hello.", "สวัสดี"), (1.1, "My bag is missing.", "กระเป๋าของฉันหาย")],
    "L05b": [(0.0, "What...", "มันหน้าตาเป็นยังไง?"), (2.2, "What... does...", "มันหน้าตาเป็นยังไง?"),
             (3.5, "What... does... it...", "มันหน้าตาเป็นยังไง?"), (4.5, "What... does... it... look like?", "มันหน้าตาเป็นยังไง?")],
    "L07": [(0.0, "Ah!", "อ๋อ!"), (2.5, "A small yellow bag?", "กระเป๋าใบเล็กสีเหลืองเหรอ?")],
    "L08c": [(0.0, "Yes!", "ใช่!"), (2.4, "It's a small yellow bag.", "เป็นกระเป๋าใบเล็กสีเหลือง")],
    "L10b": [(0.0, "Yes.", "ใช่"), (1.1, "Yes. Yes,", "ใช่ ใช่"), (3.2, "Yes. Yes, it has a pink name tag.", "ใช่ ใช่ มีป้ายชื่อสีชมพู")],
    "P01b": [(0.0, "Excuse me!", "ขอโทษนะ"), (1.5, "Is this your bag?", "นี่กระเป๋าของเธอหรือเปล่า?")],
    "P03": [(0.0, "No problem.", "ไม่เป็นไร"), (0.9, "It was on the wrong belt.", "มันอยู่ผิดสายพานน่ะ"),
            (3.1, "I'm Ollie.", "ฉันชื่อโอลลี่")],
    "P04b": [(0.0, "Hi, Ollie!", "สวัสดี โอลลี่!"), (2.3, "I'm Pudding.", "ฉันชื่อพุดดิ้ง")],
    "P05": [(0.0, "The train is over there.", "รถไฟอยู่ทางนั้น"), (3.3, "Do you have pounds?", "เธอมีเงินปอนด์ไหม?")],
    "P06": [(0.0, "Pounds?", "ปอนด์?"), (1.7, "Oh no...", "แย่แล้ว..."), (4.0, "I don't have any British money!", "ฉันไม่มีเงินอังกฤษเลย!")],
    "B6": [(0.0, "Pudding has no British money!", "พุดดิ้งไม่มีเงินอังกฤษ!"),
           (3.0, "Find out what happens in episode three!", "ติดตามในตอนที่ 3!")],
}


def clip(name, t_in, t_out, sub=None, tag=None, banner=None, icon=None, icon_at=0.0, sfx=(), th=None):
    dur = t_out - t_in
    cues = None
    if sub and name in CUES:  # (start, end, en, th) within the segment
        c = CUES[name]
        cues = [(a, c[k + 1][0] if k + 1 < len(c) else dur, en, t) for k, (a, en, t) in enumerate(c)]
    SEGS.append(dict(kind="clip", name=name, t_in=t_in, t_out=t_out, sub=sub, tag=tag, banner=banner,
                     icon=icon, icon_at=icon_at, sfx=list(sfx), dur=dur, th=th, cues=cues))


def card(dur, title=None, lines=(), badge=None, icon=None, voice=None, sfx=(), countdown=None, srt=None, th=None):
    """voice = (clip, t_in, t_out, at); countdown = (start, length) seconds within card."""
    SEGS.append(dict(kind="card", dur=dur, title=title, lines=list(lines), badge=badge, icon=icon,
                     voice=voice, sfx=list(sfx), countdown=countdown, srt=srt, th=th))


FAST, SLOW, NORMAL = ("FAST!", RED), ("SLOW", GREEN), ("NORMAL", (90, 110, 200))
L = lambda t, c=NAVY, s=78: (t, c, s)  # noqa: E731

# Host clips (Biscuit on his own at the desk, to camera): (clip, in, out, phrase, example, th, example_th, (voice_in, voice_out))
# Timings filled from QC (edl.tsv).
PHRASES = [
    ("B1", 0.2, 6.0, "My bag is missing.", "My phone is missing.", "กระเป๋าของฉันหาย", "โทรศัพท์ของฉันหาย", (3.8, 5.8)),
    ("B2", 0.1, 6.5, "It's a small yellow bag.", "It's a big black suitcase.", "เป็นกระเป๋าใบเล็กสีเหลือง", "เป็นกระเป๋าเดินทางใบใหญ่สีดำ", (4.1, 6.4)),
    ("B3", 0.1, 6.3, "It has a pink name tag.", "It has a red ribbon.", "มีป้ายชื่อสีชมพู", "มีริบบิ้นสีแดง", (4.2, 6.2)),
    ("B4", 0.2, 5.8, "Is this your bag?", "Is this your phone?", "นี่กระเป๋าของคุณหรือเปล่า?", "นี่โทรศัพท์ของคุณหรือเปล่า?", (4.2, 5.6)),
    ("B5", 0.1, 6.5, "Yes, that's my bag!", "No, that's not my bag.", "ใช่ นั่นกระเป๋าของฉัน!", "ไม่ใช่ นั่นไม่ใช่กระเป๋าของฉัน", (4.4, 6.5)),
]
B6 = ("B6", 0.0, 6.4, "Pudding has no British money! Find out what happens in episode three!")

# --- HOOK
clip("L06b", 1.4, 3.9, sub="It's a bag yellow small!", banner="Don't say this!", icon="cross", icon_at=1.6,
     sfx=[("buzz", 1.7)], th="มันเป็นกระเป๋าเหลืองเล็ก! (เรียงคำผิด)")
card(3.2, title="Pudding Goes to London", lines=[L("Episode 2 · The Lost Bag", (90, 90, 120), 70)], sfx=[("sting", 0)],
     th="พุดดิ้งไปลอนดอน ตอนที่ 2 · กระเป๋าหาย")
# --- LAST TIME (EP.1 cliffhanger, accepted EP.1 cut reused as a file)
card(2.6, title="Last time on Pudding...", sfx=[("whoosh", 0)], th="ตอนที่แล้ว...")
clip("ep1_S13", 4.0, 9.2, sub="Wait... where is my bag?!", sfx=[("buzz", 3.2)], th="เดี๋ยวนะ... กระเป๋าฉันอยู่ไหน?!")
# --- STORY: lost-luggage desk
desk = [
    ("L01", 3.8, 7.6, "Oh, it's you again! Can I help you?", "อ้าว เธออีกแล้ว! มีอะไรให้ช่วยไหม?", {}),
    ("L02f", 3.4, 5.9, "Hello. My bag is missing.", "สวัสดี กระเป๋าของฉันหาย", {}),
    ("L03", 3.3, 5.0, "What does it look like?", "มันหน้าตาเป็นยังไง?", dict(tag=FAST)),
    ("L04b", 4.3, 7.4, "Sorry, could you say that again, slowly?", "ขอโทษ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?", {}),
    ("L05b", 0.6, 6.4, "What does it look like?", "มันหน้าตาเป็นยังไง?", dict(tag=SLOW)),
    ("L06b", 1.4, 3.9, "It's a bag yellow small!", "มันเป็นกระเป๋าเหลืองเล็ก! (เรียงคำผิด)",
     dict(icon="cross", icon_at=1.6, sfx=[("buzz", 1.7)])),
    ("L07", 0.6, 4.7, "Ah! A small yellow bag?", "อ๋อ! กระเป๋าใบเล็กสีเหลืองเหรอ?", {}),
    ("L08c", 1.6, 5.9, "Yes! It's a small yellow bag.", "ใช่! เป็นกระเป๋าใบเล็กสีเหลือง",
     dict(icon="check", icon_at=2.6, sfx=[("ding", 2.7)])),
    ("L09", 0.8, 2.7, "Does it have a name tag?", "มีป้ายชื่อไหม?", {}),
    ("L10b", 1.0, 6.5, "Yes. Yes, it has a pink name tag.", "มี มี มีป้ายชื่อสีชมพู", {}),
]
for n, a, b, s, th, extra in desk:
    clip(n, a, b, sub=s, th=th, **extra)
card(2.4, title="A few minutes later...", sfx=[("whoosh", 0)], th="ไม่กี่นาทีต่อมา...")
# --- STORY: baggage belt (Ollie debuts)
belt = [
    ("P01b", 1.8, 5.1, "Excuse me! Is this your bag?", "ขอโทษนะ นี่กระเป๋าของเธอหรือเปล่า?", {}),
    ("P02", 0.9, 3.0, "Yes, that's my bag!", "ใช่ นั่นกระเป๋าของฉัน!",
     dict(icon="check", icon_at=0.6, sfx=[("ding", 0.7)])),
    ("P03", 0.1, 4.3, "No problem. It was on the wrong belt. I'm Ollie.", "ไม่เป็นไร มันอยู่ผิดสายพานน่ะ ฉันชื่อโอลลี่", {}),
    ("P04b", 0.8, 4.8, "Hi, Ollie! I'm Pudding.", "สวัสดี โอลลี่! ฉันชื่อพุดดิ้ง", {}),
    ("P05", 0.6, 5.9, "The train is over there. Do you have pounds?", "รถไฟอยู่ทางนั้น เธอมีเงินปอนด์ไหม?", {}),
    ("P06", 2.2, 9.0, "Pounds? Oh no... I don't have any British money!", "ปอนด์? แย่แล้ว... ฉันไม่มีเงินอังกฤษเลย!",
     dict(sfx=[("buzz", 6.0)])),
]
for n, a, b, s, th, extra in belt:
    clip(n, a, b, sub=s, th=th, **extra)
card(3.6, title="Oh no, Pudding!", lines=[L("But first... let's learn the English!", (90, 90, 120), 66)],
     sfx=[("whoosh", 0), ("sting", 0.4)], th="แย่แล้วพุดดิ้ง! แต่ก่อนอื่น... มาเรียนภาษาอังกฤษกัน!")
# --- 5 PHRASES (Biscuit on his own, to camera; slow then natural)
card(3.0, title="5 Phrases for a Lost Bag", sfx=[("sting", 0)], th="5 วลีเมื่อกระเป๋าหาย")
for i, (n, a, b, p, ex, pth, exth, _v) in enumerate(PHRASES, 1):
    clip(n, a, b, sub=p, tag=(f"PHRASE {i}/5 · listen twice", NAVY), sfx=[("pop", 0.1)], th=pth)
    card(4.6, badge=(f"PHRASE {i}/5", NAVY), lines=[L(p, NAVY, 92), L("You can also say:", (110, 110, 130), 54), L(ex, GREEN, 80)],
         sfx=[("pop", 0.15), ("pop", 1.4)], srt=f"{p} / You can also say: {ex}", th=f"{pth} / พูดแบบนี้ก็ได้: {exth}")
# --- COMMON MISTAKE + GRAMMAR: adjective + noun
card(3.0, title="Common Mistake", sfx=[("whoosh", 0), ("sting", 0.3)], th="ข้อผิดพลาดที่พบบ่อย")
clip("L06b", 1.4, 3.9, sub="It's a bag yellow small!", icon="cross", icon_at=1.6, sfx=[("buzz", 1.7)],
     th="มันเป็นกระเป๋าเหลืองเล็ก! (เรียงคำผิด)")
clip("L08c", 1.6, 5.9, sub="Yes! It's a small yellow bag.", icon="check", icon_at=2.6, sfx=[("ding", 2.7)],
     th="ใช่! เป็นกระเป๋าใบเล็กสีเหลือง (ถูก)")
card(6.0, lines=[L("It's a bag yellow small.", RED, 84), L("It's a small yellow bag.", GREEN, 84)], icon="check",
     sfx=[("buzz", 0.2), ("ding", 1.8)], srt="Not: It's a bag yellow small. Say: It's a small yellow bag.",
     th="อย่าพูดว่า It's a bag yellow small. ให้พูดว่า It's a small yellow bag.")
card(7.0, title="Adjective + Noun", lines=[L("a small bag  ·  a yellow bag", NAVY, 74), L("a small yellow bag", GREEN, 88),
                                           L("The adjective comes BEFORE the noun.", (90, 90, 120), 58)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="Adjective + noun: a small bag, a yellow bag, a small yellow bag. The adjective comes before the noun.",
     th="คำคุณศัพท์ + คำนาม: ภาษาไทยวางคำคุณศัพท์ไว้หลังคำนาม (กระเป๋าสีเหลืองใบเล็ก) แต่ภาษาอังกฤษวางไว้หน้าคำนาม")
card(6.0, title="Size → Colour", lines=[L("a big black suitcase", NAVY, 84), L("a small red bag", NAVY, 84)],
     sfx=[("pop", 0.2), ("pop", 1.8)], srt="Size, then colour: a big black suitcase, a small red bag.",
     th="ขนาดมาก่อนสี: a big black suitcase (กระเป๋าเดินทางใบใหญ่สีดำ), a small red bag (กระเป๋าใบเล็กสีแดง)")
# --- BISCUIT'S FAST ENGLISH
card(3.0, title="Biscuit's Fast English", lines=[L("Can you understand him?", (90, 90, 120), 62)], sfx=[("sting", 0)],
     th="ภาษาอังกฤษแบบเร็วของบิสกิต ฟังออกไหม?")
clip("L03", 3.3, 5.0, sub="What does it look like?", tag=FAST, th="(พูดเร็ว) มันหน้าตาเป็นยังไง?")
card(5.0, lines=[L("What does it look like?", NAVY, 92), L("= Tell me about your bag.", GREEN, 74)],
     sfx=[("pop", 0.2), ("pop", 1.6)], srt="What does it look like? = Tell me about your bag.",
     th="What does it look like? = บอกหน่อยว่ากระเป๋าของคุณเป็นแบบไหน")
clip("L05b", 0.6, 6.4, sub="What does it look like?", tag=SLOW, th="(พูดช้า) มันหน้าตาเป็นยังไง?")
clip("L09", 0.8, 2.7, sub="Does it have a name tag?", tag=NORMAL, th="(ความเร็วปกติ) มีป้ายชื่อไหม?")
# --- SHADOWING
card(3.2, title="Say It With Pudding!", lines=[L("Listen... then say it out loud!", (90, 90, 120), 62)], sfx=[("sting", 0)],
     th="พูดตามพุดดิ้ง! ฟังแล้วพูดออกเสียงตาม")
for i, (n, a, b, p, ex, pth, exth, (va, vb)) in enumerate(PHRASES, 1):
    vd = vb - va
    card(vd + 3.2, badge=(f"YOUR TURN {i}/5", GREEN), lines=[L(p, NAVY, 96), L("Now you!", GREEN, 70)],
         voice=(n, va, vb, 0.2), countdown=(vd + 0.4, 2.8),
         sfx=[("tick", vd + 0.4 + k * 0.7) for k in range(4)], srt=p, th=f"{pth} (พูดตาม)")
# --- QUIZ
card(3.0, title="Quiz Time!", lines=[L("3 questions. Answer before the timer ends!", (90, 90, 120), 58)], sfx=[("sting", 0)],
     th="ควิซ! 3 คำถาม ตอบก่อนหมดเวลา!")
QUIZ = [
    ("Question 1", "Put the words in order:  It's / bag / yellow / small / a", "It's a small yellow bag.", ("B2", 4.1, 6.4),
     "เรียงคำให้ถูก: It's / bag / yellow / small / a", "It's a small yellow bag. (เป็นกระเป๋าใบเล็กสีเหลือง)"),
    ("Question 2", "Your bag is not on the belt. What do you say?", "My bag is missing.", ("L02f", 4.3, 5.8),
     "กระเป๋าของคุณไม่อยู่บนสายพาน คุณจะพูดว่าอะไร?", "กระเป๋าของฉันหาย"),
    ("Question 3", "Someone asks: \"Is this your bag?\" It is! What do you say?", "Yes, that's my bag!", ("B5", 4.4, 6.5),
     "มีคนถามว่า Is this your bag? และใช่ของคุณ! คุณจะตอบว่าอะไร?", "ใช่ นั่นกระเป๋าของฉัน!"),
]
for qn, q, ans, (vc, va, vb), qth, ath in QUIZ:
    card(6.0, badge=(qn, NAVY), lines=[L(q, NAVY, 76)], countdown=(0.8, 5.0),
         sfx=[("pop", 0.1)] + [("tick", 0.8 + k) for k in range(5)], srt=q, th=qth)
    card((vb - va) + 2.0, badge=("Answer", GREEN), lines=[L(ans, GREEN, 92)], icon="check",
         voice=(vc, va, vb, 0.6), sfx=[("ding", 0.1)], srt=ans, th=ath)
card(4.0, title="Write your answers in the comments!", sfx=[("pop", 0.2)], th="เขียนคำตอบไว้ในคอมเมนต์นะ!")
# --- WATCH AGAIN (comprehension replay)
card(3.4, title="Watch Again", lines=[L("Now you understand every word!", (90, 90, 120), 62)], sfx=[("whoosh", 0), ("sting", 0.3)],
     th="ดูอีกครั้ง ตอนนี้คุณเข้าใจทุกคำแล้ว!")
for n, a, b, s, th, extra in [desk[1], desk[4], desk[7], desk[9]] + belt[:2]:
    clip(n, a, b, sub=s, th=th, **{k: v for k, v in extra.items() if k != "tag"})
# --- CLIFFHANGER + END SCREEN
clip("P06", 2.2, 9.0, sub="Pounds? Oh no... I don't have any British money!", sfx=[("buzz", 6.0)],
     th="ปอนด์? แย่แล้ว... ฉันไม่มีเงินอังกฤษเลย!")
clip(B6[0], B6[1], B6[2], sub=B6[3], th="พุดดิ้งไม่มีเงินอังกฤษ! ติดตามในตอนที่ 3!")
card(16.0, title="Next: EP.3 · Changing Money", lines=[L("Subscribe so you don't miss it!", NAVY, 66)], sfx=[("sting", 0)],
     srt="Next: Episode 3 · Changing Money. Subscribe so you don't miss it!", th="ตอนต่อไป: EP.3 แลกเงิน กดติดตามจะได้ไม่พลาด!")


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
        vf = f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[b];[b][1:v]overlay=0:0[v1]"
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
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/pudding_ep2.mp4"])
    for path, rows in [(f"{OUT}/pudding_ep2.en.srt", en), (f"{OUT}/pudding_ep2.th.srt", th)]:
        with open(path, "w", encoding="utf-8") as f:
            for k, (a, b, txt) in enumerate(rows, 1):
                f.write(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(f"DONE total {t:.2f}s")
    # second pass: measure the real integrated loudness of the delivered file
    r = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/pudding_ep2.mp4", "-af", "loudnorm=print_format=summary",
                        "-f", "null", "-"], capture_output=True, text=True)
    print("\n".join(l for l in r.stderr.splitlines() if "Input Integrated" in l or "Input True Peak" in l))


def plan():
    """Dry run: total length, section start times (for chapters) and every burned-in string, for a spell-check
    before rendering. Burned-in text cannot be fixed after upload."""
    t, rows = 0.0, []
    with open("build/burned_text.txt", "w", encoding="utf-8") as f:
        for s in SEGS:
            if s["kind"] == "card" and s.get("title"):
                rows.append(f"{int(t // 60):02d}:{int(t % 60):02d}  {s['title']}")
            texts = [s.get("sub"), s.get("banner"), (s.get("tag") or [None])[0], s.get("title"),
                     (s.get("badge") or [None])[0]] + [l[0] for l in s.get("lines", [])] + [c[2] for c in s.get("cues") or []]
            for x in texts:
                if x:
                    f.write(x + "\n")
            t += s["dur"]
    print("\n".join(rows))
    print(f"TOTAL {t:.2f}s ({int(t // 60)}:{t % 60:04.1f})")


if __name__ == "__main__":
    import sys
    plan() if sys.argv[1:] == ["plan"] else main()
