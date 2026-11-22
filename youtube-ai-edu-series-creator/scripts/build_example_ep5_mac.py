"""Build Pudding EP5 "Hotel Check-in" (16:9, 1920x1080) from QC-passed Meta AI clips, Pillow cards,
original music/SFX, burned-in English subtitles, and EN/TH .srt files.

EP.4's build.py (= EP.3's) with only the EP.5 timeline, masters and paths changed.
Same look and structure as pudding-ep3/build.py (owner 2026-11-21: "KEEP CONSISTENT"): style helpers, cards on a
blurred master under a cream wash, navy subtitle bar, tags/badges, music ducking and loudness are copied from EP.3.
Burned-in text is ENGLISH ONLY (global channel); Thai exists only in the .th.srt track.

Run (Mac, from pudding-ep5): python3 build.py [plan]
Output: out/pudding_ep5.mp4, out/pudding_ep5.en.srt, out/pudding_ep5.th.srt
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
    """Blurred EP.5 front-desk master under a cream wash, so cards stay in the same world (as EP.3/EP.4)."""
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

MED = "896:504:192:40"      # host take 2: medium shot of Biscuit (EP.4 host master is centred)

# Sentence-timed subtitles: (seconds from the clip's in point, EN, TH), from measured speech onsets (edl.tsv).
CUES = {
    # EP.4 recap clips (copied files, EP.4 in/out and cues)
    "ep4_Z01": [(0.1, "Hello!", "สวัสดี!"), (1.6, "I have a booking.", "ฉันจองห้องไว้")],
    "ep4_Z02b": [(0.1, "Hmm...", "อืม..."), (2.0, "Sorry.", "ขอโทษนะคะ"), (4.0, "I can't find your booking.", "หาการจองของคุณไม่เจอค่ะ")],
    "ep4_H6": [(0.1, "Pudding is at his hotel!", "พุดดิ้งมาถึงโรงแรมแล้ว!"), (2.8, "But where is his booking?", "แต่การจองของเขาหายไปไหน?"),
               (5.1, "Find out in episode five!", "ติดตามได้ในตอนที่ห้า!")],
    # EP.5 (from measured speech onsets, about 0.2 s before each)
    "M03": [(0.1, "Ah, here it is!", "อ๊ะ เจอแล้วค่ะ!"), (2.3, "Three nights.", "สามคืน"), (4.3, "Welcome!", "ยินดีต้อนรับค่ะ!")],
    "M06": [(0.1, "Here's your key.", "นี่กุญแจของคุณค่ะ"), (2.5, "Your room is on the second floor.", "ห้องของคุณอยู่ชั้นสองค่ะ")],
    "H6": [(0.1, "Pudding has his room!", "พุดดิ้งได้ห้องแล้ว!"), (2.4, "But what's wrong with it?", "แต่ห้องมีปัญหาอะไรนะ?"),
           (4.5, "Find out in episode six!", "ติดตามได้ในตอนที่หก!")],
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
    ("H1", (0.9, 2.8), (6.9, 9.4), MED, "I'd like to check in, please.", "I'd like to check out, please.",
     "ขอเช็กอินหน่อยครับ", "ขอเช็กเอาต์หน่อยครับ", (6.9, 9.4)),
    ("H2", (0.4, 4.3), (6.5, 9.1), MED, "I have a booking under the name Pudding.", "I have a reservation for three nights.",
     "ฉันจองห้องไว้ในชื่อพุดดิ้ง", "ฉันจองห้องไว้สามคืน", (6.5, 9.1)),
    ("H3", (3.3, 5.1), (6.3, 8.3), MED, "Could you spell that, please?", "Could you check again, please?",
     "ช่วยสะกดชื่อหน่อยได้ไหม?", "ช่วยตรวจดูอีกครั้งได้ไหม?", (6.3, 8.3)),
    ("H4", (0.6, 2.6), (5.2, 7.3), MED, "What time is breakfast?", "What time is check-out?",
     "อาหารเช้ากี่โมง?", "เช็กเอาต์กี่โมง?", (5.2, 7.3)),
    ("H5", (1.5, 3.6), (6.0, 8.2), MED, "Does the room have a kettle?", "Does the room have a shower?",
     "ในห้องมีกาต้มน้ำไหม?", "ในห้องมีฝักบัวไหม?", (6.0, 8.2)),
]

# --- HOOK
clip("D01", 1.3, 3.8, sub="But I has a booking!", banner="Don't say this!", icon="cross", icon_at=1.4, sfx=[("buzz", 1.5)],
     th="แต่ฉันจองห้องไว้! (ผิด: I has)")
card(3.2, title="Pudding Goes to London", lines=[L("Episode 5 · Hotel Check-in", GREY, 70)], sfx=[("sting", 0)],
     th="พุดดิ้งไปลอนดอน ตอนที่ 5 · เช็กอินที่โรงแรม")
# --- LAST TIME (EP.4 cliffhanger at the Red Kettle Hotel; EP.4 clips copied as files)
card(2.6, title="Last time on Pudding...", sfx=[("whoosh", 0)], th="ตอนที่แล้ว...")
clip("ep4_Z01", 2.9, 5.7, sub="Hello! I have a booking.", th="สวัสดี! ฉันจองห้องไว้")
clip("ep4_Z02b", 1.6, 7.0, sub="Hmm... Sorry. I can't find your booking.", sfx=[("buzz", 5.3)], th="อืม... ขอโทษนะคะ หาการจองของคุณไม่เจอค่ะ")
clip("ep4_H6", 0.4, 7.6, sub="Pudding is at his hotel! But where is his booking? Find out in episode five!",
     th="พุดดิ้งมาถึงโรงแรมแล้ว! แต่การจองของเขาหายไปไหน? ติดตามได้ในตอนที่ห้า!")
# --- STORY: front desk (Pudding + Ollie / Mabel alone, shot - reverse shot) -> the room
card(2.4, title="At the front desk...", sfx=[("whoosh", 0)], th="ที่เคาน์เตอร์ต้อนรับ...")
desk = [
    ("D01", 1.3, 3.8, "But I has a booking!", "แต่ฉันจองห้องไว้! (ผิด: I has)", dict(icon="cross", icon_at=1.4, sfx=[("buzz", 1.5)])),
    ("D02", 1.0, 5.0, "Try: I have a booking under the name Pudding.", "ลองพูดว่า: ฉันจองห้องไว้ในชื่อพุดดิ้ง",
     dict(icon="check", icon_at=0.4, sfx=[("ding", 0.5)])),
    ("D03b", 0.0, 4.7, "I have a booking under the name Pudding.", "ฉันจองห้องไว้ในชื่อพุดดิ้ง", {}),
    ("M01", 1.6, 3.4, "Could you spell that, please?", "ช่วยสะกดชื่อหน่อยได้ไหมคะ?", dict(tag=FAST)),
    ("D04b", 3.0, 6.2, "Sorry, could you say that again, slowly?", "ขอโทษนะ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?", {}),
    ("M02", 3.2, 7.1, "Could you... spell that... please?", "ช่วย... สะกด... หน่อยได้ไหมคะ?", dict(tag=SLOW)),
    ("D05", 0.6, 8.1, "P-U-D-D-I-N-G.", "พี-ยู-ดี-ดี-ไอ-เอ็น-จี", {}),
    ("M03", 0.3, 5.7, "Ah, here it is! Three nights. Welcome!", "อ๊ะ เจอแล้วค่ะ! สามคืน ยินดีต้อนรับค่ะ!", {}),
    ("D06b", 0.7, 2.3, "What time is breakfast?", "อาหารเช้ากี่โมง?", {}),
    ("M04", 1.1, 3.9, "Breakfast is from seven to ten.", "อาหารเช้าตั้งแต่เจ็ดโมงถึงสิบโมงค่ะ", {}),
    ("D07b", 1.3, 3.3, "Does the room have a kettle?", "ในห้องมีกาต้มน้ำไหม?", {}),
    ("M05", 0.8, 3.3, "Every room has a kettle!", "ทุกห้องมีกาต้มน้ำค่ะ!", {}),
    ("M06", 1.0, 5.8, "Here's your key. Your room is on the second floor.", "นี่กุญแจของคุณค่ะ ห้องของคุณอยู่ชั้นสองค่ะ", {}),
]
for n, a, b, s, th, extra in desk:
    clip(n, a, b, sub=s, th=th, **extra)
card(2.4, title="In Pudding's room...", sfx=[("whoosh", 0)], th="ในห้องของพุดดิ้ง...")
clip("C01b", 3.9, 5.6, sub="The room is tiny!", th="ห้องเล็กนิดเดียว!")
clip("C02", 5.3, 7.0, sub="And the light doesn't work!", sfx=[("buzz", 1.3)], th="แล้วไฟก็เปิดไม่ติดด้วย!")
card(3.6, title="Oh no, Pudding!", lines=[L("But first... let's learn the English!", GREY, 66)],
     sfx=[("whoosh", 0), ("sting", 0.4)], th="แย่แล้วพุดดิ้ง! แต่ก่อนอื่น... มาเรียนภาษาอังกฤษกัน!")
# --- 5 PHRASES (Biscuit on his own, to camera; two takes, the dead air between them cut)
card(3.0, title="5 Phrases for Hotel Check-in", sfx=[("sting", 0)], th="5 วลีสำหรับเช็กอินที่โรงแรม")
for i, (n, (a1, b1), (a2, b2), crop2, p, ex, pth, exth, _v) in enumerate(PHRASES, 1):
    clip(n, a1, b1, sub=p, tag=(f"PHRASE {i}/5 · listen twice", NAVY), sfx=[("pop", 0.1)], th=pth)
    clip(n, a2, b2, sub=p, tag=(f"PHRASE {i}/5 · again", NAVY), th=pth, crop=crop2)
    card(4.6, badge=(f"PHRASE {i}/5", NAVY),
         lines=[L(p, NAVY, 92), L("You can also say:", (110, 110, 130), 54), L(ex, GREEN, 80)],
         sfx=[("pop", 0.15), ("pop", 1.4)], srt=f"{p} / You can also say: {ex}", th=f"{pth} / พูดแบบนี้ก็ได้: {exth}")
# --- COMMON MISTAKE + GRAMMAR: have / has
card(3.0, title="Common Mistake", sfx=[("whoosh", 0), ("sting", 0.3)], th="ข้อผิดพลาดที่พบบ่อย")
clip("D01", 1.3, 3.8, sub="But I has a booking!", icon="cross", icon_at=1.4, sfx=[("buzz", 1.5)], th="แต่ฉันจองห้องไว้! (ผิด: I has)")
clip("D02", 1.0, 5.0, sub="Try: I have a booking under the name Pudding.", icon="check", icon_at=0.4, sfx=[("ding", 0.5)],
     th="ลองพูดว่า: ฉันจองห้องไว้ในชื่อพุดดิ้ง (ถูก)")
card(6.0, lines=[L("I has a booking!", RED, 84), L("I have a booking under the name Pudding.", GREEN, 80)], icon="check",
     sfx=[("buzz", 0.2), ("ding", 1.8)], srt="Not: I has a booking! Say: I have a booking under the name Pudding.",
     th="อย่าพูดว่า I has a booking! ให้พูดว่า I have a booking under the name Pudding.")
card(7.0, title="have / has", lines=[L("I / you / we / they  have", GREEN, 76),
                                     L("he / she / it  has", GREEN, 76),
                                     L("The room has a kettle.", NAVY, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="have / has: I, you, we, they have. He, she, it has. The room has a kettle.",
     th="I / you / we / they ใช้ have · he / she / it ใช้ has · ห้องนี้มีกาต้มน้ำ")
card(7.0, title="Does ... have ... ?", lines=[L("Does the room  have  a kettle?", GREEN, 78),
                                             L("Yes, it does!", NAVY, 72),
                                             L("Not: Does the room has a kettle?", RED, 60)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="Does the room have a kettle? Yes, it does! Not: Does the room has a kettle?",
     th="หลัง does ใช้ have เสมอ: Does the room have a kettle? · ตอบว่า Yes, it does!")
card(7.0, title="Spelling Your Name", lines=[L("P - U - D - D - I - N - G", NAVY, 80),
                                            L("In the UK: D D = double D", GREEN, 66),
                                            L("Could you spell that, please?", NAVY, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6), ("pop", 3.0)],
     srt="Spelling your name: P - U - D - D - I - N - G. In the UK: D D = double D. Could you spell that, please?",
     th="การสะกดชื่อ: P-U-D-D-I-N-G · ในอังกฤษ DD พูดว่า double D · ช่วยสะกดหน่อยได้ไหม?")
# --- MABEL'S FAST ENGLISH (EP.4: "Frank's Fast English" / "Can you understand him?")
card(3.0, title="Mabel's Fast English", lines=[L("Can you understand her?", GREY, 62)], sfx=[("sting", 0)],
     th="ภาษาอังกฤษแบบเร็วของเมเบิล ฟังออกไหม?")
clip("M01", 1.6, 3.4, sub="Could you spell that, please?", tag=FAST, th="(พูดเร็ว) ช่วยสะกดชื่อหน่อยได้ไหมคะ?")
card(5.0, lines=[L("Could you spell that, please?", NAVY, 80), L("= Please say the letters of your name.", GREEN, 66)],
     sfx=[("pop", 0.2), ("pop", 1.6)], srt="Could you spell that, please? = Please say the letters of your name.",
     th="Could you spell that, please? = ช่วยบอกตัวสะกดชื่อของคุณ")
clip("M02", 3.2, 7.1, sub="Could you... spell that... please?", tag=SLOW, th="(พูดช้า) ช่วย... สะกด... หน่อยได้ไหมคะ?")
clip("M04", 1.1, 3.9, sub="Breakfast is from seven to ten.", tag=NORMAL, th="(ความเร็วปกติ) อาหารเช้าตั้งแต่เจ็ดโมงถึงสิบโมงค่ะ")
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
    ("Question 1", "Put the words in order:  booking / I / a / have / under the name Pudding",
     "I have a booking under the name Pudding.", ("H2", 6.5, 9.1),
     "เรียงคำให้ถูก: booking / I / a / have / under the name Pudding", "I have a booking under the name Pudding. (ฉันจองห้องไว้ในชื่อพุดดิ้ง)"),
    ("Question 2", "Fill the gap:  \"Every room ___ a kettle.\"  (have / has)", "Every room has a kettle!", ("M05", 0.8, 3.3),
     "เติมคำ: Every room ___ a kettle. (have / has)", "Every room has a kettle! (ทุกห้องมีกาต้มน้ำ)"),
    ("Question 3", "Fix the sentence:  \"I has a booking.\"", "I have a booking.", ("ep4_Z01", 4.4, 5.7),
     "แก้ประโยคให้ถูก: I has a booking.", "I have a booking. (ฉันจองห้องไว้)"),
    ("Question 4", "You want to eat in the morning. What do you ask?", "What time is breakfast?", ("H4", 5.2, 7.3),
     "คุณอยากกินข้าวเช้า คุณจะถามว่าอะไร?", "What time is breakfast? (อาหารเช้ากี่โมง?)"),
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
for n, a, b, s, th, extra in [desk[2], desk[3], desk[9], desk[12]]:
    clip(n, a, b, sub=s, th=th, **{k: v for k, v in extra.items() if k not in ("tag", "icon", "icon_at", "sfx")})
# --- CLIFFHANGER + END SCREEN
clip("C01b", 3.9, 5.6, sub="The room is tiny!", th="ห้องเล็กนิดเดียว!")
clip("C02", 5.3, 7.0, sub="And the light doesn't work!", sfx=[("buzz", 1.3)], th="แล้วไฟก็เปิดไม่ติดด้วย!")
clip("H6", 0.2, 7.0, sub="Pudding has his room! But what's wrong with it? Find out in episode six!",
     th="พุดดิ้งได้ห้องแล้ว! แต่ห้องมีปัญหาอะไรนะ? ติดตามได้ในตอนที่หก!")
card(16.0, title="Next: EP.6 · Room Problem!", lines=[L("Subscribe so you don't miss it!", NAVY, 66)], sfx=[("sting", 0)],
     srt="Next: Episode 6 · Room Problem! Subscribe so you don't miss it!", th="ตอนต่อไป: EP.6 ปัญหาในห้องพัก! กดติดตามจะได้ไม่พลาด!")


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
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/pudding_ep5.mp4"])
    for path, rows in [(f"{OUT}/pudding_ep5.en.srt", en), (f"{OUT}/pudding_ep5.th.srt", th)]:
        with open(path, "w", encoding="utf-8") as f:
            for k, (a, b, txt) in enumerate(rows, 1):
                f.write(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(f"DONE total {t:.2f}s")
    r = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/pudding_ep5.mp4", "-af", "loudnorm=print_format=summary",
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
