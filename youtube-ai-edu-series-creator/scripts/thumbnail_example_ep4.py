"""EP.4 thumbnail: Meta AI art (thumb/thumb_art_v1.png, no text) + local text in the EP.3 layout:
EP badge top-right (navy circle, yellow text), two-line yellow headline with dark outline, pink pill line.
Asserts: text stays in the empty right side, the pill text fits its pill, nothing in the bottom-right timestamp area."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
art = Image.open("thumb/thumb_art_v1.png").convert("RGB").resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(art)


def font(path, size, weight="ExtraBold"):
    f = ImageFont.truetype(path, size)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f


NAVY = (38, 56, 110); YEL = (255, 204, 51); OUT = (59, 42, 30); PINK = (244, 143, 177); WHITE = (255, 255, 255)
SAFE_X = int(W * 0.585)              # characters + cab live left of this
boxes = []

# EP badge (top-right, same corner as EP.3)
cx, cy, r = W - 95, 95, 68
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=NAVY, outline=WHITE, width=6)
fb = font("fonts/Baloo2.ttf", 50); t = "EP.4"; tw = d.textlength(t, font=fb)
d.text((cx - tw / 2, cy - 34), t, font=fb, fill=YEL)
boxes.append((cx - r, cy - r, cx + r, cy + r))

# headline
size = 150
while max(d.textlength(l, font=font("fonts/Baloo2.ttf", size)) for l in ("TAXI,", "PLEASE!")) > (W - SAFE_X - 60):
    size -= 4
fh = font("fonts/Baloo2.ttf", size)
y = 200
for line in ("TAXI,", "PLEASE!"):
    tw = d.textlength(line, font=fh)
    x = SAFE_X + (W - SAFE_X - tw) / 2
    d.text((x, y), line, font=fh, fill=YEL, stroke_width=10, stroke_fill=OUT)
    bb = d.textbbox((x, y), line, font=fh, stroke_width=10); boxes.append(bb); y += 140

# pill
fp = font("fonts/Nunito.ttf", 40, "Black"); t = "Could you take me...?"
tw = d.textlength(t, font=fp); pw = tw + 60; px = SAFE_X + (W - SAFE_X - pw) / 2; py = y + 40
d.rounded_rectangle((px, py, px + pw, py + 80), radius=40, fill=PINK, outline=WHITE, width=5)
ink = d.textbbox((0, 0), t, font=fp)
tx = px + (pw - (ink[2] - ink[0])) / 2 - ink[0]; ty = py + (80 - (ink[3] - ink[1])) / 2 - ink[1]
d.text((tx, ty), t, font=fp, fill=WHITE, stroke_width=3, stroke_fill=(150, 50, 90))
tb = d.textbbox((tx, ty), t, font=fp, stroke_width=3)
assert px + 10 <= tb[0] and tb[2] <= px + pw - 10 and py + 6 <= tb[1] and tb[3] <= py + 74, ("pill overflow", tb, (px, py, pw))
boxes.append((px, py, px + pw, py + 80))

for b in boxes:
    assert b[0] >= SAFE_X - 10 and b[2] <= W - 10 and b[1] >= 10, ("text outside the right side", b)
    assert not (b[2] > W - 260 and b[3] > H - 90), ("text in the timestamp area", b)
art.save("out/pudding_ep4_thumbnail.jpg", quality=92)
for w in (320, 168):
    art.resize((w, int(w * 9 / 16)), Image.LANCZOS).save(f"build/thumb_{w}.png")
print("thumbnail ok", boxes)
