import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import math, os
from coverlib import *
from PIL import ImageDraw
cv = Cover()
cv.paste(vgrad(S(W), S(H), (44, 10, 40), (6, 2, 8)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(560), S(900), S(760), (255, 80, 100), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255); RED = (240, 62, 90, 255); GOLD = (255, 210, 74, 255)
AN = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# alarm bell (left) + an upside-down curve card (right)
bx, by = 360, 900
g.pieslice([S(bx - 130), S(by - 160), S(bx + 130), S(by + 100)], 180, 360, fill=RED, outline=INK, width=S(10))
g.rectangle([S(bx - 130), S(by - 32), S(bx + 130), S(by + 60)], fill=RED)
g.line([S(bx - 130), S(by - 32), S(bx - 130), S(by + 60)], fill=INK, width=S(10)); g.line([S(bx + 130), S(by - 32), S(bx + 130), S(by + 60)], fill=INK, width=S(10))
g.rounded_rectangle([S(bx - 165), S(by + 50), S(bx + 165), S(by + 90)], radius=S(12), fill=RED, outline=INK, width=S(10))
g.ellipse([S(bx - 28), S(by + 85), S(bx + 28), S(by + 140)], fill=GOLD, outline=INK, width=S(8))
for r in (190, 240):
    g.arc([S(bx - r), S(by - 40 - r), S(bx + r), S(by - 40 + r)], 200, 235, fill=GOLD, width=S(12))
    g.arc([S(bx - r), S(by - 40 - r), S(bx + r), S(by - 40 + r)], 305, 340, fill=GOLD, width=S(12))
cx, cy = 790, 880
g.rounded_rectangle([S(cx - 160), S(cy - 120), S(cx + 160), S(cy + 120)], radius=S(22), fill=(250, 246, 236, 255), outline=INK, width=S(10))
pts = [(S(cx - 125 + 250 * u / 30), S(cy - 70 + 140 * (1 - math.exp(-4 * u / 30)))) for u in range(31)]
g.line(pts, fill=INK, width=S(26)); g.line(pts, fill=RED, width=S(14))
g.text((S(cx), S(cy + 150)), "?", font=ImageFont.truetype(AN, S(120)), fill=GOLD, anchor="mm", stroke_width=S(8), stroke_fill=INK)
cv.glow(G, (255, 110, 120), 26, 0.5)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #57", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 340, 180, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(255, 90, 110), glow=22)
cv.title("SAID BUY.", 540, 560, 190, (255, 236, 160), (255, 150, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1195, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "night", None)
cv.sprite(roc, 270, 1240, spot=(255, 230, 190))
cv.title("SELL OR IGNORE?", 540, 1790, 115, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_57_kapak.png")
print("ok")
