"""Assemble Pudding EP1 (16:9, 1920x1080) from QC-passed Meta AI clips, Pillow cards,
original music/SFX, burned-in English subtitles, and EN/TH .srt files.

Run: .venv/Scripts/python.exe build.py
Output: out/pudding_ep1.mp4, out/pudding_ep1.en.srt, out/pudding_ep1.th.srt
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
    """Blurred desk-scene frame under a cream wash, so cards stay in the same world."""
    global _BG
    if _BG is None:
        frame = "build/desk_frame.png"
        subprocess.run([FF, "-v", "error", "-y", "-ss", "0.2", "-i", "clips/B1.mp4", "-frames:v", "1", frame], check=True)
        bg = Image.open(frame).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
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


def clip(name, t_in, t_out, sub=None, tag=None, banner=None, icon=None, icon_at=0.0, sfx=(), th=None):
    SEGS.append(dict(kind="clip", name=name, t_in=t_in, t_out=t_out, sub=sub, tag=tag, banner=banner,
                     icon=icon, icon_at=icon_at, sfx=list(sfx), dur=t_out - t_in, th=th))


def card(dur, title=None, lines=(), badge=None, icon=None, voice=None, sfx=(), countdown=None, srt=None, th=None):
    """voice = (clip, t_in, t_out, at); countdown = (start, length) seconds within card."""
    SEGS.append(dict(kind="card", dur=dur, title=title, lines=list(lines), badge=badge, icon=icon,
                     voice=voice, sfx=list(sfx), countdown=countdown, srt=srt, th=th))


FAST, SLOW, NORMAL = ("FAST!", RED), ("SLOW", GREEN), ("NORMAL", (90, 110, 200))
L = lambda t, c=NAVY, s=78: (t, c, s)  # noqa: E731

# --- HOOK
clip("S07m", 1.5, 5.5, sub="I come for travel!", banner="Don't say this at the airport!", icon="cross", icon_at=1.6,
     sfx=[("buzz", 1.7)], th="ฉันมาเพื่อเดินทาง! (ประโยคนี้ผิด)")
card(3.2, title="Pudding Goes to London", lines=[L("Episode 1 · At the Airport", (90, 90, 120), 70)], sfx=[("sting", 0)],
     th="พุดดิ้งไปลอนดอน ตอนที่ 1 · ที่สนามบิน")
# --- STORY
story = [
    ("C01a", 0.5, 5.2, "Hi! I'm Ploy. Is this your first time in London?", "สวัสดี! ฉันชื่อพลอย มาลอนดอนครั้งแรกเหรอ?"),
    ("C01b", 2.0, 6.0, "Yes! I'm a little nervous.", "ใช่! ฉันตื่นเต้นนิดหน่อย"),
    ("C02", 0.5, 8.0, "Wow... London!", "ว้าว... ลอนดอน!"),
    ("C03", 1.0, 6.5, "Good luck, Pudding! Speak slowly. It's OK.", "โชคดีนะพุดดิ้ง! พูดช้าๆ ไม่เป็นไร"),
]
for n, a, b, s, th in story:
    clip(n, a, b, sub=s, th=th)
clip("S04m", 0.0, 4.0, sub="Passport, please. Purpose of your visit?", tag=FAST, th="ขอดูพาสปอร์ตด้วย มาด้วยจุดประสงค์อะไร?")
clip("S05m", 1.5, 5.6, sub="Sorry, could you say that again, slowly?", th="ขอโทษ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?")
clip("S06m", 0.5, 5.0, sub="What is the purpose of your visit?", tag=SLOW, th="คุณมาด้วยจุดประสงค์อะไร?")
clip("S07m", 1.5, 5.5, sub="I come for travel!", icon="cross", icon_at=1.6, sfx=[("buzz", 1.7)], th="ฉันมาเพื่อเดินทาง! (ผิด)")
clip("S08m", 0.5, 7.0, sub="Psst! Pudding! Say: I'm here on holiday.", th="ชู่ว์! พุดดิ้ง! พูดว่า I'm here on holiday.")
clip("S09m", 0.5, 4.0, sub="I'm here on holiday.", icon="check", icon_at=1.8, sfx=[("ding", 1.9)], th="ฉันมาเที่ยวพักผ่อน")
clip("S10m", 3.5, 6.5, sub="How long are you staying?", th="คุณจะอยู่นานแค่ไหน?")
clip("S11m", 0.5, 4.5, sub="I'm staying for two weeks.", th="ฉันจะอยู่สองสัปดาห์")
clip("S12n", 0.0, 2.0)
clip("S12n", 7.4, 10.0, sub="Welcome to London!", th="ยินดีต้อนรับสู่ลอนดอน!")
clip("S13", 0.0, 9.2, sub="Wait... where is my bag?!", sfx=[("buzz", 7.2)], th="เดี๋ยวนะ... กระเป๋าฉันอยู่ไหน?!")
card(3.6, title="Oh no, Pudding!", lines=[L("But first... let's learn the English!", (90, 90, 120), 66)], sfx=[("whoosh", 0), ("sting", 0.4)],
     th="แย่แล้วพุดดิ้ง! แต่ก่อนอื่น... มาเรียนภาษาอังกฤษกัน!")
# --- 5 PHRASES
card(3.0, title="5 Phrases You Need at the Airport", sfx=[("sting", 0)], th="5 วลีที่ต้องใช้ที่สนามบิน")
phrases = [
    ("B1", 0.3, 8.2, "I'm here on holiday.", "I'm here on business.", "ฉันมาเที่ยวพักผ่อน", "ฉันมาทำธุระ/ทำงาน", (6.4, 8.0)),
    ("B2", 1.0, 7.8, "I'm staying for two weeks.", "I'm staying for five days.", "ฉันจะอยู่สองสัปดาห์", "ฉันจะอยู่ห้าวัน", (5.4, 7.6)),
    ("B3", 0.5, 8.2, "I'm staying at a hotel in London.", "I'm staying with a friend.", "ฉันพักที่โรงแรมในลอนดอน", "ฉันพักกับเพื่อน", (5.6, 8.0)),
    ("B4", 3.5, 7.2, "Sorry, could you say that again, slowly?", "Sorry, could you repeat that?", "ขอโทษ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?", "ขอโทษ ช่วยพูดซ้ำได้ไหม?", (3.6, 7.0)),
    ("B5", 0.5, 6.2, "Here's my passport.", "Here's my boarding pass.", "นี่พาสปอร์ตของฉัน", "นี่บัตรขึ้นเครื่องของฉัน", (4.6, 6.0)),
]
for i, (n, a, b, p, ex, pth, exth, _) in enumerate(phrases, 1):
    tag_txt = f"PHRASE {i}/5" if n == "B4" else f"PHRASE {i}/5 · slow → natural"  # B4 keeps only the slow take
    clip(n, a, b, sub=p, tag=(tag_txt, NAVY), sfx=[("pop", 0.1)], th=pth)
    card(4.6, badge=(f"PHRASE {i}/5", NAVY), lines=[L(p, NAVY, 92), L("You can also say:", (110, 110, 130), 54), L(ex, GREEN, 80)],
         sfx=[("pop", 0.15), ("pop", 1.4)], srt=f"{p} / You can also say: {ex}", th=f"{pth} / พูดแบบนี้ก็ได้: {exth}")
# --- COMMON MISTAKE
card(3.0, title="Common Mistake", sfx=[("whoosh", 0), ("sting", 0.3)], th="ข้อผิดพลาดที่พบบ่อย")
clip("S07m", 1.5, 5.5, sub="I come for travel!", icon="cross", icon_at=1.6, sfx=[("buzz", 1.7)], th="ฉันมาเพื่อเดินทาง! (ผิด)")
clip("S09m", 0.5, 4.0, sub="I'm here on holiday.", icon="check", icon_at=1.8, sfx=[("ding", 1.9)], th="ฉันมาเที่ยวพักผ่อน (ถูก)")
card(6.0, lines=[L("I come for travel.", RED, 84), L("I'm here on holiday.  (UK)", GREEN, 84), L("I'm here on vacation.  (US)", GREEN, 84)],
     icon="check", sfx=[("buzz", 0.2), ("ding", 1.6), ("ding", 3.0)],
     srt="Not: I come for travel. Say: I'm here on holiday. (UK) / I'm here on vacation. (US)",
     th="อย่าพูดว่า I come for travel. ให้พูดว่า I'm here on holiday. (อังกฤษ) / I'm here on vacation. (อเมริกา)")
card(6.0, title="I am  →  I'm", lines=[L("\"I'm here\" = I am in this place now.", NAVY, 66), L("I'm here on holiday.", GREEN, 84)],
     sfx=[("pop", 0.2), ("pop", 2.0)], srt="I am → I'm. \"I'm here\" = I am in this place now.",
     th="I am → I'm  \"I'm here\" = ตอนนี้ฉันอยู่ที่นี่")
# --- BISCUIT'S FAST ENGLISH
card(3.0, title="Biscuit's Fast English", lines=[L("Can you understand him?", (90, 90, 120), 62)], sfx=[("sting", 0)],
     th="ภาษาอังกฤษแบบเร็วของบิสกิต ฟังออกไหม?")
clip("S04m", 0.0, 4.0, sub="Passportpleasepurposeofyourvisit?", tag=FAST, th="(พูดเร็ว) ขอดูพาสปอร์ต มาด้วยจุดประสงค์อะไร?")
card(5.0, lines=[L("Passport, please.", NAVY, 92), L("Purpose of your visit?", NAVY, 92), L("= Why are you here?", GREEN, 70)],
     sfx=[("pop", 0.2), ("pop", 1.3), ("pop", 2.6)], srt="Passport, please. Purpose of your visit? = Why are you here?",
     th="ขอดูพาสปอร์ต มาด้วยจุดประสงค์อะไร? = คุณมาที่นี่ทำไม?")
clip("S06m", 0.5, 5.0, sub="What is the purpose of your visit?", tag=SLOW, th="(พูดช้า) คุณมาด้วยจุดประสงค์อะไร?")
clip("S10m", 3.5, 6.5, sub="How long are you staying?", tag=NORMAL, th="(ความเร็วปกติ) คุณจะอยู่นานแค่ไหน?")
# --- SHADOWING
card(3.2, title="Say It With Pudding!", lines=[L("Listen... then say it out loud!", (90, 90, 120), 62)], sfx=[("sting", 0)],
     th="พูดตามพุดดิ้ง! ฟังแล้วพูดออกเสียงตาม")
for i, (n, a, b, p, ex, pth, exth, (va, vb)) in enumerate(phrases, 1):
    vd = vb - va
    card(vd + 3.2, badge=(f"YOUR TURN {i}/5", GREEN), lines=[L(p, NAVY, 96), L("Now you!", GREEN, 70)],
         voice=(n, va, vb, 0.2), countdown=(vd + 0.4, 2.8),
         sfx=[("tick", vd + 0.4 + k * 0.7) for k in range(4)], srt=p, th=f"{pth} (พูดตาม)")
# --- QUIZ
card(3.0, title="Quiz Time!", lines=[L("3 questions. Answer before the timer ends!", (90, 90, 120), 58)], sfx=[("sting", 0)],
     th="ควิซ! 3 คำถาม ตอบก่อนหมดเวลา!")
quiz = [
    ("Question 1", "The officer asks: \"How long are you staying?\" What do you say?", "I'm staying for two weeks.", ("S11m", 0.8, 3.9),
     "เจ้าหน้าที่ถามว่า How long are you staying? คุณจะตอบว่าอะไร?", "ฉันจะอยู่สองสัปดาห์"),
    ("Question 2", "Fix this sentence: \"I come for travel.\"", "I'm here on holiday.", ("S09m", 0.8, 3.0),
     "แก้ประโยคนี้ให้ถูก: I come for travel.", "ฉันมาเที่ยวพักผ่อน"),
    ("Question 3", "Someone speaks too fast. What do you say?", "Sorry, could you say that again, slowly?", ("S05m", 2.2, 5.6),
     "มีคนพูดเร็วเกินไป คุณจะพูดว่าอะไร?", "ขอโทษ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?"),
]
for qn, q, ans, (vc, va, vb), qth, ath in quiz:
    card(6.0, badge=(qn, NAVY), lines=[L(q, NAVY, 76)], countdown=(0.8, 5.0),
         sfx=[("pop", 0.1)] + [("tick", 0.8 + k) for k in range(5)], srt=q, th=qth)
    card((vb - va) + 2.0, badge=("Answer", GREEN), lines=[L(ans, GREEN, 92)], icon="check",
         voice=(vc, va, vb, 0.6), sfx=[("ding", 0.1)], srt=ans, th=ath)
card(4.0, title="Write your answers in the comments!", sfx=[("pop", 0.2)], th="เขียนคำตอบไว้ในคอมเมนต์นะ!")
# --- WATCH AGAIN (comprehension replay of the desk scene)
card(3.4, title="Watch Again", lines=[L("Now you understand every word!", (90, 90, 120), 62)], sfx=[("whoosh", 0), ("sting", 0.3)],
     th="ดูอีกครั้ง ตอนนี้คุณเข้าใจทุกคำแล้ว!")
for n, a, b, s, th, extra in [
    ("S04m", 0.0, 4.0, "Passport, please. Purpose of your visit?", "ขอดูพาสปอร์ต มาด้วยจุดประสงค์อะไร?", {}),
    ("S05m", 1.5, 5.6, "Sorry, could you say that again, slowly?", "ขอโทษ ช่วยพูดอีกครั้งช้าๆ ได้ไหม?", {}),
    ("S06m", 0.5, 5.0, "What is the purpose of your visit?", "คุณมาด้วยจุดประสงค์อะไร?", {}),
    ("S09m", 0.5, 4.0, "I'm here on holiday.", "ฉันมาเที่ยวพักผ่อน", dict(icon="check", icon_at=1.8, sfx=[("ding", 1.9)])),
    ("S10m", 3.5, 6.5, "How long are you staying?", "คุณจะอยู่นานแค่ไหน?", {}),
    ("S11m", 0.5, 4.5, "I'm staying for two weeks.", "ฉันจะอยู่สองสัปดาห์", {}),
    ("S12n", 7.4, 10.0, "Welcome to London!", "ยินดีต้อนรับสู่ลอนดอน!", {}),
]:
    clip(n, a, b, sub=s, th=th, **extra)
# --- CLIFFHANGER + END SCREEN
clip("S13", 4.0, 9.2, sub="Wait... where is my bag?!", sfx=[("buzz", 3.2)], th="เดี๋ยวนะ... กระเป๋าฉันอยู่ไหน?!")
clip("B6", 1.5, 6.8, sub="Where is Pudding's bag? Find out in episode two!", th="กระเป๋าของพุดดิ้งอยู่ไหน? ติดตามในตอนที่ 2!")
card(16.0, title="Next: EP.2 · The Lost Bag", lines=[L("Subscribe so you don't miss it!", NAVY, 66)], sfx=[("sting", 0)],
     srt="Next: Episode 2 · The Lost Bag. Subscribe so you don't miss it!", th="ตอนต่อไป: EP.2 กระเป๋าหาย กดติดตามจะได้ไม่พลาด!")


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
    out = f"{SEG_DIR}/seg_{i:03d}.mp4"
    dur = s["dur"]
    if s["kind"] == "clip":
        ov = f"build/ov_{i:03d}.png"
        overlay_png(ov, sub=s["sub"], tag=s["tag"], banner=s["banner"])
        args = ["-ss", f"{s['t_in']}", "-t", f"{dur}", "-i", f"clips/{s['name']}.mp4", "-loop", "1", "-t", f"{dur}", "-i", ov]
        vf = f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[b];[b][1:v]overlay=0:0[v1]"
        idx = 2
        if s["icon"]:
            ic = f"build/ic_{i:03d}.png"
            overlay_png(ic, icon=s["icon"])
            args += ["-loop", "1", "-t", f"{dur}", "-i", ic]
            vf += f";[v1][2:v]overlay=0:0:enable='gte(t,{s['icon_at']})'[v2]"
            vlast, idx = "[v2]", 3
        else:
            vlast = "[v1]"
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
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out]
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
        if text:
            en.append((t, t + s["dur"], text))
            if s.get("th"):
                th.append((t, t + s["dur"], s["th"]))
        t += s["dur"]
        print(f"seg {i:03d} {s['kind']:4s} {s['dur']:5.2f}s  total {t:6.2f}s", flush=True)
    with open("build/concat.txt", "w", encoding="utf-8") as f:
        for p in files:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["-f", "concat", "-safe", "0", "-i", "build/concat.txt", "-c", "copy", "build/body.mp4"])
    # music bed, ducked under speech with a sidechain compressor, faded at both ends
    run(["-i", "build/body.mp4", "-stream_loop", "-1", "-i", "audio/music_loop.wav", "-filter_complex",
         f"[0:a]asplit=2[voice][sc];[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{t:.2f},volume=0.30,"
         f"afade=t=in:d=1.5,afade=t=out:st={t - 3:.2f}:d=3[mus];[mus][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];"
         f"[voice][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]",
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         f"{OUT}/pudding_ep1.mp4"])
    for path, rows in [(f"{OUT}/pudding_ep1.en.srt", en), (f"{OUT}/pudding_ep1.th.srt", th)]:
        with open(path, "w", encoding="utf-8") as f:
            for k, (a, b, txt) in enumerate(rows, 1):
                f.write(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(f"DONE total {t:.2f}s")


if __name__ == "__main__":
    main()
