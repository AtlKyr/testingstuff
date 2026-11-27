import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import math, os
from coverlib import *
from PIL import ImageDraw
cv = Cover()
cv.paste(vgrad(S(W), S(H), (40, 18, 8), (4, 3, 6)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(950), S(760), (255, 120, 60), 0.16))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255); BR = (139, 90, 60, 255); MZ = (216, 168, 128, 255)
AN = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# four sealed case tiles, one glowing (the bear that settles it)
for k, lab in enumerate(("20??", "20??", "20??", "20??")):
    x = 120 + k * 220; y = 820
    glow = k == 0
    g.rounded_rectangle([S(x), S(y), S(x + 190), S(y + 200)], radius=S(18), fill=(30, 26, 22, 255) if not glow else (60, 40, 10, 255),
                        outline=(255, 210, 74, 255) if glow else (120, 120, 120, 255), width=S(8))
    cx = x + 95; cy = y + 80
    for ex in (-34, 34):
        g.ellipse([S(cx + ex - 18), S(cy - 52), S(cx + ex + 18), S(cy - 16)], fill=INK)
        g.ellipse([S(cx + ex - 13), S(cy - 47), S(cx + ex + 13), S(cy - 21)], fill=BR)
    g.ellipse([S(cx - 48), S(cy - 44), S(cx + 48), S(cy + 52)], fill=INK)
    g.ellipse([S(cx - 42), S(cy - 38), S(cx + 42), S(cy + 46)], fill=BR)
    g.ellipse([S(cx - 20), S(cy + 4), S(cx + 20), S(cy + 40)], fill=MZ)
    g.ellipse([S(cx - 7), S(cy + 8), S(cx + 7), S(cy + 20)], fill=INK)
    g.text((S(cx), S(y + 170)), lab, font=ImageFont.truetype(AN, S(40)), fill=(255, 210, 74, 255) if glow else (200, 200, 200, 255), anchor="mm")
cv.glow(G, (255, 170, 80), 22, 0.5)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #53", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("ONE BEAR", 540, 350, 180, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(255, 140, 70), glow=22)
cv.title("SETTLED IT.", 540, 570, 180, (255, 236, 160), (255, 150, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "detective", None)
cv.sprite(roc, 300, 1210, spot=(255, 230, 190))
cv.title("BUY OR WAIT?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_53_kapak.png")
print("ok")
