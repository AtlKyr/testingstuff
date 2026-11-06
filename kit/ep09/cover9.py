import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math
from coverlib import *
from PIL import ImageDraw


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
    ctx.new_path(); ctx.arc(cx - px * 0.95, cy - px * 0.95, px * 0.75, math.pi, 1.5 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(px * 0.3); ctx.stroke()


cv = Cover()
cv.paste(vgrad(S(W), S(H), (40, 26, 84), (6, 4, 18)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (255, 200, 80), 0.35))
# calendar grid of trading days, 10 glowing gold cells
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
import random
rr = random.Random(9); gold = set(rr.sample(range(14 * 9), 10))
for r_ in range(9):
    for c_ in range(14):
        x = 50 + c_ * 70; y = 330 + r_ * 70
        k = r_ * 14 + c_
        col = (255, 210, 74, 255) if k in gold else (255, 255, 255, 34)
        d.rounded_rectangle([S(x), S(y), S(x + 56), S(y + 56)], radius=S(8), fill=col)
cv.glow(L, (255, 200, 60), 18, 0.9)
cv.paste(L)
cv.bottom_fade(1300, alpha=0.95)
cv.stamp("CASE #9", 540, 150, 74, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("MISS", 330, 470, 190, (255, 255, 255), (210, 210, 230), rot=-5, stroke=13, glow_col=(0, 0, 0), glow=20)
cv.title("10 DAYS", 560, 720, 250, (255, 236, 90), (255, 150, 20), rot=4, stroke=13, glow_col=(255, 200, 60), glow=36)
cv.badge("?", 880, 450, 90, rot=10)
cv.redacted("THE COST:", 540, 1000, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1110, spot=(255, 240, 200))
cv.title("WHAT DID IT COST?", 540, 1790, 128, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_09_kapak.png")
print("ok")
