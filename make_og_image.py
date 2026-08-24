#!/usr/bin/env python3
"""Generate a 1200x630 branded Open Graph / social share card for faviconpal.com."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BG = (246, 247, 249)        # #f6f7f9
WHITE = (255, 255, 255)
INK = (16, 24, 40)          # #101828
BLUE = (37, 99, 235)        # #2563eb
PURPLE = (124, 58, 237)     # #7c3aed
GREEN = (6, 118, 71)        # #067647
MUTED = (71, 84, 103)       # #475467
CHIP_BG = (239, 246, 255)   # #eff6ff
CHIP_TX = (29, 78, 216)     # #1d4ed8
GREEN_BG = (236, 253, 243)  # #ecfdf3

FONT_DIR = "C:/Windows/Fonts"
REG = os.path.join(FONT_DIR, "arial.ttf")
BOLD = os.path.join(FONT_DIR, "arialbd.ttf")

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)

def gradient_square(size, c1, c2):
    """Diagonal gradient rounded square (blue -> purple) as a mask-friendly image."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # base blue, then paint a diagonal purple overlay by scanning
    d.rectangle([0, 0, size, size], fill=c1 + (255,))
    for i in range(size):
        # diagonal: weight grows from top-left to bottom-right
        t = i / size
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        d.line([(i, 0), (i, size)], fill=(r, g, b, 255))
    # round the corners by masking
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, size, size], radius=size // 6, fill=255)
    img.putalpha(mask)
    return img

def rounded_chip(d, xy, fill, radius=14):
    d.rounded_rectangle(xy, radius=radius, fill=fill)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# soft shadow card
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=(16, 24, 40, 18))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
d = ImageDraw.Draw(img)

# white card
d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=WHITE)

# ---- brand mark (top-left) ----
glyph = gradient_square(64, BLUE, PURPLE)
img.paste(glyph, (88, 86), glyph)
d.text((172, 96), "FaviconPal", font=font(34, bold=True), fill=INK)

# ---- headline ----
d.text((88, 196), "Turn any image into a", font=font(58, bold=True), fill=INK)
d.text((88, 268), "complete favicon set", font=font(58, bold=True), fill=INK)

# ---- format chips ----
labels = ["WebP", "JPG", "SVG", "AVIF"]
chip_h = 56
y = 372
x = 88
gap = 14
arrow_x = None
for lab in labels:
    w = d.textlength(lab, font=font(26, bold=True))
    bw = int(w) + 40
    rounded_chip(d, [x, y, x + bw, y + chip_h], fill=CHIP_BG)
    d.text((x + 20, y + 14), lab, font=font(26, bold=True), fill=CHIP_TX)
    x += bw + gap
# arrow
d.text((x + 6, y + 8), "\u2192", font=font(40, bold=True), fill=MUTED)
x += 52
# ICO target chip (accent gradient)
ico_w = 110
rounded_chip(d, [x, y, x + ico_w, y + chip_h], fill=BLUE)
d.text((x + 24, y + 14), "ICO", font=font(26, bold=True), fill=WHITE)

# ---- trust line ----
ty = 478
# green check badge
rounded_chip(d, [88, ty, 88 + 44, ty + 44], fill=GREEN_BG)
d.text((104, ty + 6), "\u2713", font=font(30, bold=True), fill=GREEN)
trust = "100% in your browser \u00b7 no files uploaded \u00b7 no signup"
d.text((150, ty + 6), trust, font=font(28, bold=False), fill=MUTED)

# ---- footer hint ----
d.text((88, 552), "Free online favicon generator \u00b7 faviconpal.com",
       font=font(22, bold=False), fill=(152, 162, 179))

out = "assets/og-image.png"
os.makedirs("assets", exist_ok=True)
img.save(out, "PNG")
print("Saved", out, img.size)
