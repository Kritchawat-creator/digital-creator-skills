"""EP3 thumbnail: Meta AI cover art (Pudding waving + suitcase, Biscuit peeking, empty mint sky right) + local text.

Text is drawn locally (OFL fonts) because AI image models misspell words.
Measured on the 1280x720 art: Pudding/suitcase/Biscuit end at x~740, so text lives in x 760-1268 (centre 1012).
Run from E:/claude-work/pudding-ep3 with the EP1 venv. Output: out/pudding_ep3_thumbnail.jpg + QC sizes in build/.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
NAVY, YELLOW, WHITE, PINK = (31, 42, 68), (255, 201, 60), (255, 255, 255), (255, 143, 171)
ART_RIGHT = 740          # rightmost character pixel in the art (measured)
FREE = (760, W - 12)     # text must stay inside this x range
CX = 1012                # centre of the free sky area
PILL_PAD_X, PILL_CY, PILL_H = 48, 548, 84  # pill text keeps >= 48 px side padding (owner rule)


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes([weight])
    return f


def sticker(d, text, y, fnt, fill, sw=11):
    """Outlined sticker text centred on CX; returns its ink box so the caller can check it."""
    tw = d.textlength(text, font=fnt)
    x = CX - tw / 2
    d.text((x + 5, y + 7), text, font=fnt, fill=(31, 42, 68, 110), stroke_width=sw, stroke_fill=(31, 42, 68, 110))
    d.text((x, y), text, font=fnt, fill=fill, stroke_width=sw, stroke_fill=NAVY)
    return d.textbbox((x, y), text, font=fnt, stroke_width=sw)


img = Image.open("thumb/meta_cover.png").convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)

big = font("fonts/Baloo2[wght].ttf", 116, 800)
mid = font("fonts/Baloo2[wght].ttf", 42, 800)
ep = font("fonts/Baloo2[wght].ttf", 50, 800)

boxes = [sticker(d, "CHANGE", 190, big, YELLOW), sticker(d, "MONEY!", 320, big, WHITE)]
for b in boxes:
    assert b[0] >= FREE[0] and b[2] <= FREE[1], f"title text out of the free area: {b}"

label = "Where? How much?"
bx0, by0, bx1, by1 = d.textbbox((0, 0), label, font=mid, stroke_width=4)
tw, th = bx1 - bx0, by1 - by0
pill = [CX - tw / 2 - PILL_PAD_X, PILL_CY - PILL_H / 2, CX + tw / 2 + PILL_PAD_X, PILL_CY + PILL_H / 2]
d.rounded_rectangle(pill, radius=PILL_H // 2, fill=PINK, outline=WHITE, width=6)
tx, ty = CX - tw / 2 - bx0, PILL_CY - th / 2 - by0
d.text((tx, ty), label, font=mid, fill=WHITE, stroke_width=4, stroke_fill=NAVY)
ink = d.textbbox((tx, ty), label, font=mid, stroke_width=4)
# the pill must contain the text ink plus padding, and stay in the free area
assert pill[0] + PILL_PAD_X - 1 <= ink[0] and ink[2] <= pill[2] - PILL_PAD_X + 1, (pill, ink)
assert pill[1] < ink[1] and ink[3] < pill[3], (pill, ink)
assert pill[0] >= FREE[0] and pill[2] <= FREE[1], f"pill out of the free area: {pill}"
print(f"pill x {pill[0]:.0f}-{pill[2]:.0f}, ink x {ink[0]:.0f}-{ink[2]:.0f}, side padding {PILL_PAD_X}px; titles {boxes}")

# EP.3 badge, top-right, clear of the YouTube timestamp (bottom-right)
d.ellipse([1118, 26, 1254, 162], fill=NAVY, outline=YELLOW, width=8)
tw = d.textlength("EP.3", font=ep)
d.text((1186 - tw / 2, 64), "EP.3", font=ep, fill=YELLOW)

img = Image.alpha_composite(img, layer).convert("RGB")
img.save("out/pudding_ep3_thumbnail.jpg", quality=92)
for w in (320, 168):  # QC sizes: suggested-video and mobile list
    img.resize((w, w * 9 // 16), Image.LANCZOS).save(f"build/thumb_qc_{w}.png")
print("saved out/pudding_ep3_thumbnail.jpg + build/thumb_qc_320.png, build/thumb_qc_168.png")
