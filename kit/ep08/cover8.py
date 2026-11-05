import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math
from coverlib import *

# prop_magnifier copied from the engine (cairo), drawn into Rocco's sprite
def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
    ctx.new_path(); ctx.arc(cx - px * 0.95, cy - px * 0.95, px * 0.75, math.pi, 1.5 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(px * 0.3); ctx.stroke()

cv = Cover()
cv.split_bg(seam_top=650, seam_bot=430)
cv.sun(175, 300, 82)
cv.moon(900, 300, 92)
cv.skyline(base=1920, seed=5)
cv.bottom_fade(1380, alpha=0.9)
cv.stamp("CASE #8", 540, 118, 74, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("DAY", 300, 520, 300, (255, 236, 90), (255, 150, 20), rot=6, stroke=13, glow_col=(255, 200, 60), glow=34)
cv.title("NIGHT", 760, 840, 250, (255, 255, 255), (180, 160, 255), rot=-5, stroke=13, glow_col=(130, 110, 255), glow=40)
cv.badge("VS", 520, 690, 74)
cv.redacted("WINNER:", 540, 1060, 760, 116, rot=-3)
roc = rocco_sprite(23, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1150, spot=(255, 240, 200))
cv.title("WHO WINS?", 540, 1800, 168, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_08_kapak.png")
print("ok")
