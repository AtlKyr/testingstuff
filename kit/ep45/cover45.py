import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math, os
from coverlib import *
from PIL import ImageDraw


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
cv = Cover()
cv.paste(vgrad(S(W), S(H), (36, 12, 60), (6, 2, 12)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (200, 140, 255), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# a Bollinger-band card: violet bands, white price dipping under the lower band, "?" on the dip
import math as _m
cx, cy = 780, 900
g.rounded_rectangle([S(cx - 220), S(cy - 170), S(cx + 220), S(cy + 170)], radius=S(30), fill=(12, 16, 28, 255), outline=(200, 205, 210, 255), width=S(8))
def wave(off, amp, col, w):
    pts = [(S(cx - 190 + j * 19), S(cy + off + _m.sin(j * 0.55) * amp)) for j in range(21)]
    g.line(pts, fill=col, width=S(w))
wave(-80, 25, (192, 124, 255, 255), 8); wave(0, 25, (255, 210, 74, 255), 5); wave(80, 25, (192, 124, 255, 255), 8)
pts = [(S(cx - 190 + j * 19), S(cy + _m.sin(j * 0.55) * 25 + (110 if 12 <= j <= 15 else 0) * _m.sin((j - 12) / 3 * _m.pi))) for j in range(21)]
g.line(pts, fill=(255, 255, 255, 255), width=S(9))
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(150))
g.text((S(cx + 120), S(cy - 60)), "?", font=f, fill=(255, 210, 74, 255), anchor="mm", stroke_width=S(9), stroke_fill=INK)
cv.glow(G, (200, 140, 255), 22, 0.55)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #45", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN", 540, 340, 230, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(200, 140, 255), glow=22)
cv.title("SEPTEMBER CAME.", 540, 560, 132, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1150, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "lab", None)
cv.sprite(roc, 300, 1210, spot=(235, 215, 255))
cv.title("BANDS OR HOLD?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_45_kapak.png")
print("ok")
