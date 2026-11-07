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
cv = Cover()
cv.paste(vgrad(S(W), S(H), (70, 14, 30), (10, 3, 8)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(700), S(820), (255, 70, 100), 0.30))
# three big red candles stepping down (glowing)
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
for k in range(3):
    x = 600 + k * 140; y = 300 + k * 120
    d.rectangle([S(x + 40), S(y - 50), S(x + 52), S(y + 330)], fill=(20, 24, 28, 255))
    d.rounded_rectangle([S(x), S(y), S(x + 92), S(y + 280)], radius=S(10), fill=(240, 62, 90, 255), outline=(20, 24, 28, 255), width=S(6))
cv.glow(L, (255, 60, 90), 22, 0.9)
cv.paste(L)
cv.bottom_fade(1300, alpha=0.95)
cv.stamp("CASE #10", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("3 RED DAYS", 470, 430, 200, (255, 120, 140), (230, 40, 70), rot=-5, stroke=13, glow_col=(0, 0, 0), glow=20)
cv.title("BUY?", 360, 720, 290, (120, 255, 180), (20, 200, 110), rot=4, stroke=14, glow_col=(30, 230, 140), glow=36)
cv.redacted("RESULT:", 540, 1000, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1110, spot=(255, 220, 220))
cv.title("PANIC OR HOLD?", 540, 1790, 140, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_10_kapak.png")
print("ok")
