import cairo, math
from render_07 import *
surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
bg_fill(ctx, (0x12, 0x3A, 0x2A), (0x05, 0x12, 0x0C))
god_rays(ctx, W / 2, 900, 0.3, 0.08, C["green"], 16, 1800)
for k in range(60):
    rect(ctx, (k * 137) % W, 300 + (k * 211) % 1500, 7, 7, C["yellow"], 0.35)
ctx.save(); ctx.translate(W / 2, 240); ctx.rotate(-0.04)
text(ctx, "TURTLE", 0, 40, 220, C["white"], 1, HEAD, True, "center", outline=28, ocol=C["ink"])
ctx.restore()
ctx.save(); ctx.translate(W / 2, 420); ctx.rotate(0.03)
card(ctx, -340, -65, 680, 120, C["yellow"], 1, 18)
text(ctx, "BREAKOUT", 0, 28, 84, C["ink"], 1, HEAD, True, "center")
ctx.restore()
# real SPY 2023 window: price + 20-day high + 10-day low, BUY on the real breakout bar
i0, i1 = di("2023-03-01"), di("2023-07-20")
box = (120, 570, 840, 330)
card(ctx, box[0] - 30, box[1] - 30, box[2] + 60, box[3] + 60, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
seg = np.concatenate([CLOSE[i0:i1 + 1], HH[i0:i1 + 1], LL[i0:i1 + 1]]); vmin, vmax = seg.min() * 0.99, seg.max() * 1.01
xs, ys = series_xy(HH, i0, i1, i1, box, vmin, vmax, 1); poly(ctx, xs, ys, C["green"], 6, 0.9)
xs, ys = series_xy(LL, i0, i1, i1, box, vmin, vmax, 1); poly(ctx, xs, ys, C["red"], 6, 0.9)
xs, ys = series_xy(CLOSE, i0, i1, i1, box, vmin, vmax, 1); poly(ctx, xs, ys, C["white"], 7, 1, glow=True)
bi = di("2023-05-01") - 1
x, y = sx_of(bi, i0, i1, box), sy_of(CLOSE[bi], vmin, vmax, box)
ctx.new_path(); ctx.arc(x, y, 24, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"])); ctx.fill_preserve()
ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
tag(ctx, x, y + 80, "BUY", C["green"], 1, 44, -0.05, C["ink"])
# Rocco big, detective + magnifier, shocked; turtle peeking
turtle(ctx, 880, 1530, 1.1, 0.6, hide=0.0)
px = 32
ctx.save(); ctx.translate(W / 2 - 22 * px * 0.42 - 150, 1040)
draw_rocco(ctx, 0, 0, px, "shock", "detective")
prop_magnifier(ctx, px * 16.5, px * 13.5, px, 0.4)
ctx.restore()
ctx.save(); ctx.translate(W / 2, 1735); ctx.rotate(-0.03)
card(ctx, -470, -100, 940, 200, C["red"], 1, 22)
s = "SLOW & STEADY WINS?"
text(ctx, s, 0, 34, fit(ctx, s, 104, 880), C["white"], 1, HEAD, True, "center")
ctx.restore()
text(ctx, "STRATEGY AUTOPSY #7", W / 2, 1885, 34, C["cream"], 0.9, MONO, True, "center")
vignette(ctx); paper_grain(ctx, 0.05)
surf.write_to_png("StrategyAutopsy_07_kapak.png")
