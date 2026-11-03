import cairo, math
from render_06 import *
surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
bg_fill(ctx, (0x2B, 0x12, 0x4A), (0x0C, 0x06, 0x1C))
god_rays(ctx, W / 2, 900, 0.3, 0.08, C["yellow"], 16, 1800)
for k in range(60):
    rect(ctx, (k * 137) % W, 300 + (k * 211) % 1500, 7, 7, C["yellow"], 0.35)
# title
ctx.save(); ctx.translate(W / 2, 250); ctx.rotate(-0.04)
text(ctx, "MACD", 0, 40, 230, C["white"], 1, HEAD, True, "center", outline=28, ocol=C["ink"])
ctx.restore()
ctx.save(); ctx.translate(W / 2, 430); ctx.rotate(0.03)
card(ctx, -360, -65, 720, 120, C["yellow"], 1, 18)
text(ctx, "CROSSOVER", 0, 28, 84, C["ink"], 1, HEAD, True, "center")
ctx.restore()
# MACD vs signal lines crossing with BUY / SELL markers (illustrative, no result)
box = (110, 560, 860, 300)
card(ctx, box[0] - 30, box[1] - 30, box[2] + 60, box[3] + 60, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
n = 200
xs = [box[0] + i / n * box[2] for i in range(n + 1)]
ya = [box[1] + box[3] / 2 - 110 * math.sin(i / n * 3.2 * math.pi) for i in range(n + 1)]
yb = [box[1] + box[3] / 2 - 95 * math.sin(i / n * 3.2 * math.pi - 0.55) for i in range(n + 1)]
poly(ctx, xs, yb, C["orange"], 9, 1); poly(ctx, xs, ya, C["blue"], 11, 1, glow=True)
crs = []
for i in range(1, n + 1):
    d0, d1 = yb[i - 1] - ya[i - 1], yb[i] - ya[i]
    if d0 <= 0 < d1: crs.append((i, "BUY", C["green"]))
    elif d0 >= 0 > d1: crs.append((i, "SELL", C["red"]))
for i, lab, col in crs:
    x, y = xs[i], (ya[i] + yb[i]) / 2
    ctx.new_path(); ctx.arc(x, y, 22, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    tag(ctx, x, y - 70 if lab == "BUY" else y + 85, lab, col, 1, 40, -0.05, C["ink"] if lab == "BUY" else C["white"])
# Rocco big, detective + magnifier, shocked
px = 32
ctx.save(); ctx.translate(W / 2 - 22 * px * 0.42 - 60, 1060)
draw_rocco(ctx, 0, 0, px, "shock", "detective")
prop_magnifier(ctx, px * 16.5, px * 13.5, px, 0.4)
ctx.restore()
ctx.save(); ctx.translate(W / 2, 1735); ctx.rotate(-0.03)
card(ctx, -470, -100, 940, 200, C["red"], 1, 22)
s = "207 TRADES. WORTH IT?"
text(ctx, s, 0, 34, fit(ctx, s, 100, 880), C["white"], 1, HEAD, True, "center")
ctx.restore()
text(ctx, "STRATEGY AUTOPSY #6", W / 2, 1885, 34, C["cream"], 0.9, MONO, True, "center")
vignette(ctx); paper_grain(ctx, 0.05)
surf.write_to_png("StrategyAutopsy_06_kapak.png")
