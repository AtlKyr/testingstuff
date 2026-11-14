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
cv.paste(vgrad(S(W), S(H), (8, 52, 30), (3, 8, 6)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (60, 255, 140), 0.22))
INKC = (20, 24, 28, 255)
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
import numpy as np
xs = np.linspace(110, 970, 80)
ys = 1010 - 300 * (xs - 110) / 860 + 22 * np.sin(xs / 23.0)
g.line([(S(x), S(y)) for x, y in zip(xs, ys)], fill=(60, 240, 140, 255), width=S(14), joint="curve")
g.polygon([(S(990), S(735)), (S(935), S(740)), (S(975), S(785))], fill=(60, 240, 140, 255))
cv.glow(G, (40, 230, 120), 22, 0.9)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #22", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN", 540, 340, 160, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(40, 200, 110), glow=22)
cv.title("SPRING CAME.", 540, 530, 170, (255, 230, 120), (255, 150, 40), rot=-4, stroke=13, glow_col=(255, 150, 30), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(200, 255, 220))
cv.title("LOCK IN OR HOLD?", 540, 1790, 128, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_22_kapak.png")
print("ok")
