import cairo, math
import render_05 as R
from render_05 import *
surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
t = 1.3
# split background: winter (left/bottom) vs summer (right/top)
bg_fill(ctx, *SKY)
god_rays(ctx, 900, 420, 0.4, 0.12, C["white"], 14, 1800)
ctx.save(); ctx.new_path(); ctx.move_to(0, 760); ctx.line_to(W, 1260); ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path(); ctx.clip()
bg_fill(ctx, (0x1C, 0x2C, 0x52), (0x0A, 0x12, 0x26))
for k in range(120):
    x = (k * 131) % W; y = 700 + (k * 223) % 1250
    ctx.new_path(); ctx.arc(x, y, 3 + (k % 4), 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.6); ctx.fill()
ctx.restore()
ctx.new_path(); ctx.move_to(0, 760); ctx.line_to(W, 1260); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(14); ctx.stroke()
sun(ctx, 900, 560, 90, 0.3)
# title
ctx.save(); ctx.translate(W / 2, 250); ctx.rotate(-0.04)
text(ctx, "SELL IN MAY", 0, 0, 150, C["white"], 1, HEAD, True, "center", outline=26, ocol=C["ink"])
ctx.restore()
ctx.save(); ctx.translate(W / 2, 400); ctx.rotate(0.03)
card(ctx, -400, -70, 800, 130, C["yellow"], 1, 18)
text(ctx, "...AND GO AWAY?", 0, 26, 76, C["ink"], 1, HEAD, True, "center")
ctx.restore()
# calendar: MAY crossed out
ctx.save(); ctx.translate(220, 640); ctx.rotate(-0.08)
card(ctx, -150, -130, 300, 260, C["cream"], 1, 16); rect(ctx, -146, -126, 292, 66, C["red"])
text(ctx, "MAY", 0, 75, 110, C["ink"], 1, HEAD, True, "center")
xmark(ctx, 0, 40, 90, C["red"], 20)
ctx.restore()
# Rocco big, shocked, straw hat
px = 34
ctx.save(); ctx.translate(W / 2 - 22 * px * 0.42 + 40, 1100)
draw_rocco(ctx, 0, 0, px, "shock", "straw")
ctx.restore()
# question
ctx.save(); ctx.translate(W / 2, 1720); ctx.rotate(-0.03)
card(ctx, -470, -95, 940, 190, C["red"], 1, 22)
text(ctx, "20 YEARS. WORTH IT?", 0, 30, fit(ctx, "20 YEARS. WORTH IT?", 96, 880), C["white"], 1, HEAD, True, "center")
ctx.restore()
text(ctx, "STRATEGY AUTOPSY #5", W / 2, 1880, 34, C["cream"], 0.9, MONO, True, "center")
vignette(ctx); paper_grain(ctx, 0.05)
surf.write_to_png("StrategyAutopsy_05_kapak.png")
