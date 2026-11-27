import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import math, os
from coverlib import *
from PIL import ImageDraw
cv = Cover()
cv.paste(vgrad(S(W), S(H), (16, 22, 60), (3, 4, 12)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(930), S(760), (255, 90, 110), 0.16))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255); RED = (240, 62, 90, 255)
AN = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# one big calendar page "JANUARY" with a glowing hidden value + a row of grey month pages
px_, py_ = 540, 900
g.rounded_rectangle([S(px_ - 190), S(py_ - 170), S(px_ + 190), S(py_ + 170)], radius=S(22), fill=(250, 250, 250, 255), outline=INK, width=S(10))
g.rectangle([S(px_ - 184), S(py_ - 164), S(px_ + 184), S(py_ - 80)], fill=RED)
g.text((S(px_), S(py_ - 122)), "JANUARY", font=ImageFont.truetype(AN, S(64)), fill=(255, 255, 255, 255), anchor="mm")
g.text((S(px_), S(py_ + 50)), "-?.??%", font=ImageFont.truetype(AN, S(110)), fill=RED, anchor="mm")
cv.glow(G, (255, 120, 120), 22, 0.5)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #54", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("A HAIR", 540, 350, 190, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(255, 140, 70), glow=22)
cv.title("DECIDED 2020.", 540, 570, 170, (255, 236, 160), (255, 150, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "grad", None)
cv.sprite(roc, 300, 1210, spot=(255, 230, 190))
cv.title("SKIP OR STAY?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_54_kapak.png")
print("ok")
