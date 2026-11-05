import cairo, math
from render_08 import *
surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
t = 0.4
bg_fill(ctx, SKY, SKY2); sun(ctx, 190, 330, 80, t); cloud(ctx, 60, 700, 1.0)
ctx.save(); ctx.new_path(); ctx.move_to(640, 0); ctx.line_to(W, 0); ctx.line_to(W, H); ctx.line_to(420, H); ctx.close_path(); ctx.clip()
bg_fill(ctx, NAVY, NAVY2); stars(ctx, t, 60, 0, 1500, 3); moon(ctx, 880, 330, 85)
ctx.restore()
ctx.new_path(); ctx.move_to(640, 0); ctx.line_to(420, H); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(14); ctx.stroke()
# case file tab
ctx.save(); ctx.translate(W / 2, 110); ctx.rotate(-0.03)
card(ctx, -230, -55, 460, 110, (0xE2, 0xBC, 0x76), 1, 14)
text(ctx, "CASE #8", 0, 30, 76, C["red"], 1, HEAD, True, "center")
ctx.restore()
ctx.save(); ctx.translate(300, 620); ctx.rotate(-0.06)
text(ctx, "DAY", 0, 0, 230, C["yellow"], 1, HEAD, True, "center", outline=28, ocol=C["ink"]); ctx.restore()
ctx.save(); ctx.translate(560, 720); text(ctx, "vs", 0, 0, 90, C["white"], 1, HEAD, True, "center", outline=14, ocol=C["ink"]); ctx.restore()
ctx.save(); ctx.translate(800, 870); ctx.rotate(0.05)
text(ctx, "NIGHT", 0, 0, 170, MOONC, 1, HEAD, True, "center", outline=26, ocol=C["ink"]); ctx.restore()
# redacted result
ctx.save(); ctx.translate(W / 2, 1010); ctx.rotate(-0.02)
card(ctx, -400, -70, 800, 140, C["dark"], 1, 16, border=C["white"])
text(ctx, "WINNER:", -370, 18, 40, C["white"], 1, MONO, True, "left")
rect(ctx, -110, -45, 480, 90, (0x05, 0x05, 0x05))
text(ctx, "$??,???", 130, 26, 70, (0x66, 0x6B, 0x70), 1, MONO, True, "center")
ctx.restore()
px = 30
ctx.save(); ctx.translate(W / 2 - 22 * px * 0.42 - 120, 1110)
draw_rocco(ctx, 0, 0, px, "shock", "detective")
prop_magnifier(ctx, px * 16.5, px * 13.5, px, 0.4)
ctx.restore()
ctx.save(); ctx.translate(W / 2, 1750); ctx.rotate(-0.03)
card(ctx, -420, -100, 840, 200, C["red"], 1, 22)
s = "WHO WINS?"
text(ctx, s, 0, 40, fit(ctx, s, 130, 780), C["white"], 1, HEAD, True, "center")
ctx.restore()
text(ctx, "STRATEGY AUTOPSY #8", W / 2, 1890, 34, C["cream"], 1, MONO, True, "center", outline=6, ocol=C["ink"])
vignette(ctx); paper_grain(ctx, 0.05)
surf.write_to_png("StrategyAutopsy_08_kapak.png")
