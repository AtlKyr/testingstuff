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
cv.paste(vgrad(S(W), S(H), (70, 12, 26), (6, 3, 10)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (255, 80, 60), 0.25))
INKC = (20, 24, 28, 255)
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
import numpy as np
xs = np.linspace(110, 970, 80)
ys = 1010 - 260 / (1 + np.exp(-(xs - 640) / 70)) + 14 * np.sin(xs / 23.0)
g.line([(S(x), S(y)) for x, y in zip(xs, ys)], fill=(255, 92, 92, 255), width=S(14), joint="curve")
g.polygon([(S(990), S(735)), (S(935), S(740)), (S(975), S(785))], fill=(255, 92, 92, 255))
cv.glow(G, (255, 60, 60), 22, 0.9)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #20", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN RATES", 540, 340, 160, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(220, 60, 60), glow=22)
cv.title("EXPLODED.", 560, 530, 220, (255, 230, 120), (255, 120, 40), rot=-4, stroke=13, glow_col=(255, 90, 30), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 200, 190))
cv.title("SELL OR HOLD?", 540, 1790, 170, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_20_kapak.png")
print("ok")
