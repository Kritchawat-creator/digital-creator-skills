"""EP2 thumbnail: Meta AI cover art (Pudding + suitcase on the left, empty sky right) + sticker text added here.

Text is drawn locally (OFL fonts) because AI image models misspell words.
Measured on the 1280x720 art: Pudding ends at x≈650, so text lives in x 690-1260 (centre 975).
Run from E:/claude-work/pudding-ep2 with the EP1 venv. Output: out/pudding_ep2_thumbnail.jpg + QC sizes in build/.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
NAVY, YELLOW, WHITE, PINK = (31, 42, 68), (255, 201, 60), (255, 255, 255), (255, 143, 171)
CX = 975  # centre of the free sky area
PILL_PAD_X, PILL_CY, PILL_H = 48, 540, 84  # pill text keeps >= 48 px side padding (owner rule)


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes([weight])
    return f


def sticker(d, text, y, fnt, fill, sw=11):
    tw = d.textlength(text, font=fnt)
    x = CX - tw / 2
    d.text((x + 5, y + 7), text, font=fnt, fill=(31, 42, 68, 110), stroke_width=sw, stroke_fill=(31, 42, 68, 110))
    d.text((x, y), text, font=fnt, fill=fill, stroke_width=sw, stroke_fill=NAVY)


img = Image.open("thumb/meta_cover.png").convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)

big = font("fonts/Baloo2[wght].ttf", 138, 800)
mid = font("fonts/Baloo2[wght].ttf", 42, 800)
ep = font("fonts/Baloo2[wght].ttf", 50, 800)

sticker(d, "LOST", 170, big, YELLOW)
sticker(d, "BAG!", 310, big, WHITE)

label = "What to Say in English"
bx0, by0, bx1, by1 = d.textbbox((0, 0), label, font=mid, stroke_width=4)
tw, th = bx1 - bx0, by1 - by0
pill = [CX - tw / 2 - PILL_PAD_X, PILL_CY - PILL_H / 2, CX + tw / 2 + PILL_PAD_X, PILL_CY + PILL_H / 2]
d.rounded_rectangle(pill, radius=PILL_H // 2, fill=PINK, outline=WHITE, width=6)
d.text((CX - tw / 2 - bx0, PILL_CY - th / 2 - by0), label, font=mid, fill=WHITE, stroke_width=4, stroke_fill=NAVY)
assert pill[0] >= 680 and pill[2] <= W - 12, f"pill out of the free area: {pill}"
print(f"pill x {pill[0]:.0f}-{pill[2]:.0f}, side padding {PILL_PAD_X}px, text width {tw}px")

# EP.2 badge, top-right, clear of the YouTube timestamp (bottom-right)
d.ellipse([1118, 26, 1254, 162], fill=NAVY, outline=YELLOW, width=8)
tw = d.textlength("EP.2", font=ep)
d.text((1186 - tw / 2, 64), "EP.2", font=ep, fill=YELLOW)

img = Image.alpha_composite(img, layer).convert("RGB")
img.save("out/pudding_ep2_thumbnail.jpg", quality=92)
for w in (320, 168):  # QC sizes: suggested-video and mobile list
    img.resize((w, w * 9 // 16), Image.LANCZOS).save(f"build/thumb_qc_{w}.png")
print("saved out/pudding_ep2_thumbnail.jpg + build/thumb_qc_320.png, build/thumb_qc_168.png")
