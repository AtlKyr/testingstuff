import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math, os
from coverlib import *
from PIL import ImageDraw, ImageFont


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
cv = Cover()
cv.paste(vgrad(S(W), S(H), (24, 52, 130), (4, 8, 28)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(700), S(820), (255, 210, 74), 0.24))
INKC = (20, 24, 28, 255); GOLDC = (255, 210, 74, 255)
F = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(100))
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)


def coin(cx, cy, r, f=None):
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=GOLDC, outline=INKC, width=S(max(4, r // 9)))
    d.ellipse([S(cx - r * 0.7), S(cy - r * 0.7), S(cx + r * 0.7), S(cy + r * 0.7)], outline=(224, 154, 16, 255), width=S(max(3, r // 12)))
    ff = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(int(r * 1.1)))
    d.text((S(cx), S(cy)), "$", font=ff, fill=INKC, anchor="mm")
coin(250, 800, 150)                                   # one big coin (all in)
for k in range(12):                                   # twelve small ones (the drip)
    coin(600 + (k % 4) * 115, 690 + (k // 4) * 115, 46)
cv.glow(L, (255, 200, 60), 18, 0.55)
cv.paste(L)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #15", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("ALL IN", 400, 350, 190, (255, 220, 150), (255, 150, 30), rot=-4, stroke=12, glow_col=(255, 120, 30), glow=22)
cv.title("OR DRIP?", 610, 520, 170, (200, 240, 255), (79, 195, 247), rot=-3, stroke=12, glow_col=(40, 120, 220), glow=22)
cv.badge("VS", 455, 800, 62)
cv.redacted("WINNER:", 540, 1060, 820, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1150, spot=(255, 235, 200))
cv.title("WHO WINS?", 540, 1790, 180, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_15_kapak.png")
print("ok")
