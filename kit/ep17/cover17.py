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
cv.paste(vgrad(S(W), S(H), (40, 22, 84), (6, 4, 18)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (255, 77, 106), 0.25))
INKC = (20, 24, 28, 255)
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
pts = [(0, 0.10), (0.15, 0.30), (0.30, 0.50), (0.45, 0.72), (0.55, 1.0), (0.62, 0.80), (0.70, 0.55), (0.80, 0.18), (0.88, 0.05), (1.0, 0.25)]
xy = [(S(110 + u * 860), S(1000 - v * 270)) for u, v in pts]
g.line(xy, fill=(255, 77, 106, 255), width=S(16), joint="curve")
px, py = 110 + 0.55 * 860, 1000 - 270
g.rectangle([S(px - 5), S(py - 120), S(px + 5), S(py)], fill=INKC)
g.polygon([(S(px + 5), S(py - 120)), (S(px + 120), S(py - 92)), (S(px + 5), S(py - 64))], fill=(255, 214, 64, 255), outline=INKC, width=S(5))
cv.glow(G, (255, 77, 106), 22, 0.9)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #17", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("BOUGHT THE", 540, 330, 140, (255, 255, 255), (220, 210, 255), rot=-4, stroke=12, glow_col=(120, 60, 220), glow=22)
cv.title("2007 TOP", 560, 480, 180, (255, 210, 215), (255, 77, 106), rot=-4, stroke=12, glow_col=(255, 60, 90), glow=22)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(220, 210, 255))
cv.title("HOW LONG?", 540, 1790, 190, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_17_kapak.png")
print("ok")
