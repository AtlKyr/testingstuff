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
cv.paste(vgrad(S(W), S(H), (10, 44, 34), (2, 8, 6)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (34, 229, 139), 0.20))
INKC = (20, 24, 28, 255)
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
import numpy as np
xs = np.linspace(110, 970, 80); u = (xs - 110) / 860
ys = 1000 - 300 * (np.exp(2.6 * u) - 1) / (np.exp(2.6) - 1)
for yl in (900, 800):
    for xx in range(110, 970, 44):
        g.line([(S(xx), S(yl)), (S(xx + 24), S(yl))], fill=(255, 210, 74, 200), width=S(5))
g.line([(S(x), S(y)) for x, y in zip(xs, ys)], fill=(34, 229, 139, 255), width=S(15), joint="curve")
cv.glow(G, (34, 229, 139), 20, 0.8)
cv.paste(G)
cv.title("?", 860, 820, 150, (255, 255, 255), (255, 214, 64), rot=6, stroke=10, glow_col=(255, 200, 60), glow=26)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #19", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT GOT", 540, 340, 150, (255, 255, 255), (220, 210, 255), rot=-4, stroke=12, glow_col=(120, 60, 220), glow=22)
cv.title("EASIER.", 560, 520, 220, (255, 210, 215), (255, 77, 106), rot=-4, stroke=13, glow_col=(255, 60, 90), glow=24)
cv.redacted("WORTH:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(220, 210, 255))
cv.title("A OR B?", 540, 1790, 190, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_19_kapak.png")
print("ok")
