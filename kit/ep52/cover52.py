import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import math, os
from coverlib import *
from PIL import ImageDraw
cv = Cover()
cv.paste(vgrad(S(W), S(H), (46, 10, 22), (4, 3, 10)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(1000), S(760), (255, 200, 90), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255); DG = (34, 229, 139, 255); DR = (255, 77, 106, 255)
AN = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# rising sun (the next morning) behind decorative candles
g.pieslice([S(700), S(820), S(1000), S(1120)], 180, 360, fill=(255, 196, 70, 255))
for k in range(9):
    a = math.pi + k * math.pi / 8
    g.line([(S(850 + 170 * math.cos(a)), S(970 + 170 * math.sin(a))), (S(850 + 230 * math.cos(a)), S(970 + 230 * math.sin(a)))], fill=(255, 196, 70, 255), width=S(10))
g.rectangle([S(640), S(966), S(1060), S(978)], fill=(255, 236, 200, 255))
for j in range(8):   # candles: falling, then a green comeback (decorative)
    x = 130 + j * 72; base = 900 + 90 * math.sin(j / 7 * math.pi)
    h = 110 if j != 4 else 160
    col = DR if j < 4 else DG
    g.line([(S(x), S(base - h / 2 - 40)), (S(x), S(base + h / 2 + 40))], fill=INK, width=S(10))
    g.rounded_rectangle([S(x - 24), S(base - h / 2), S(x + 24), S(base + h / 2)], radius=S(6), fill=col, outline=INK, width=S(6))
g.text((S(850), S(905)), "?", font=ImageFont.truetype(AN, S(110)), fill=INK, anchor="mm")
cv.glow(G, (255, 170, 80), 22, 0.5)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #52", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN THE", 540, 350, 170, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(255, 140, 70), glow=22)
cv.title("BELL RANG.", 540, 570, 190, (255, 236, 160), (255, 150, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "fire", None)
cv.sprite(roc, 300, 1210, spot=(255, 230, 190))
cv.title("SELL OR HOLD?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_52_kapak.png")
print("ok")
