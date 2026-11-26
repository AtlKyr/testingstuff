import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import math, os
from coverlib import *
from PIL import ImageDraw
cv = Cover()
cv.paste(vgrad(S(W), S(H), (74, 18, 10), (12, 3, 2)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 120, 60), 0.20))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255); HOT = (255, 74, 58, 255)
# thermometer (original drawing)
tx, ty = 820, 880
g.rounded_rectangle([S(tx - 52), S(ty - 200), S(tx + 52), S(ty + 80)], radius=S(52), fill=INK)
g.ellipse([S(tx - 92), S(ty + 20), S(tx + 92), S(ty + 204)], fill=INK)
g.rounded_rectangle([S(tx - 38), S(ty - 186), S(tx + 38), S(ty + 70)], radius=S(38), fill=(244, 241, 234, 255))
g.ellipse([S(tx - 78), S(ty + 34), S(tx + 78), S(ty + 190)], fill=HOT)
g.rectangle([S(tx - 22), S(ty - 140), S(tx + 22), S(ty + 60)], fill=HOT)
for j in range(6):
    g.rectangle([S(tx + 38), S(ty + 40 - j * 38), S(tx + 38 + (24 if j % 2 == 0 else 12)), S(ty + 46 - j * 38)], fill=INK)
# calendar page DEC ??
px_, py_ = 470, 900
g.rounded_rectangle([S(px_ - 105), S(py_ - 110), S(px_ + 105), S(py_ + 110)], radius=S(14), fill=(250, 250, 250, 255), outline=INK, width=S(8))
g.rectangle([S(px_ - 101), S(py_ - 106), S(px_ + 101), S(py_ - 50)], fill=(240, 62, 90, 255))
f0 = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(44))
g.text((S(px_), S(py_ - 78)), "DEC", font=f0, fill=(255, 255, 255, 255), anchor="mm")
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(110))
g.text((S(px_), S(py_ + 32)), "??", font=f, fill=INK, anchor="mm")
cv.glow(G, (255, 110, 60), 24, 0.55)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #49", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("IT SOLD IN", 540, 350, 160, (255, 255, 255), (255, 225, 210), rot=-4, stroke=12, glow_col=(255, 110, 60), glow=22)
cv.title("DECEMBER.", 540, 570, 180, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "fire", None)
cv.sprite(roc, 300, 1210, spot=(255, 220, 190))
cv.title("SELL OR HOLD?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_49_kapak.png")
print("ok")
