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
cv.paste(vgrad(S(W), S(H), (34, 16, 58), (6, 3, 14)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (200, 140, 255), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# a violet cloud with a calendar page "OCT ??" (original drawing)
cx, cy = 780, 920
for ox, oy, r in ((-110, 20, 85), (-30, -40, 110), (70, -10, 95), (135, 30, 70), (0, 40, 95)):
    g.ellipse([S(cx + ox - r - 10), S(cy + oy - r - 10), S(cx + ox + r + 10), S(cy + oy + r + 10)], fill=INK)
for ox, oy, r in ((-110, 20, 85), (-30, -40, 110), (70, -10, 95), (135, 30, 70), (0, 40, 95)):
    g.ellipse([S(cx + ox - r), S(cy + oy - r), S(cx + ox + r), S(cy + oy + r)], fill=(192, 124, 255, 255))
px_, py_ = cx - 10, cy + 10
g.rounded_rectangle([S(px_ - 95), S(py_ - 100), S(px_ + 95), S(py_ + 100)], radius=S(14), fill=(250, 250, 250, 255), outline=INK, width=S(8))
g.rectangle([S(px_ - 91), S(py_ - 96), S(px_ + 91), S(py_ - 45)], fill=(240, 62, 90, 255))
f0 = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(40))
g.text((S(px_), S(py_ - 70)), "OCT", font=f0, fill=(255, 255, 255, 255), anchor="mm")
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(100))
g.text((S(px_), S(py_ + 30)), "??", font=f, fill=INK, anchor="mm")
cv.glow(G, (192, 124, 255), 24, 0.55)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #48", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("OCTOBER CHANGED", 540, 350, 140, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(120, 170, 255), glow=22)
cv.title("EVERYTHING.", 540, 560, 170, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "lab", None)
cv.sprite(roc, 300, 1210, spot=(255, 230, 190))
cv.title("CLOUD OR HOLD?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_48_kapak.png")
print("ok")
