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
cv.paste(vgrad(S(W), S(H), (8, 52, 30), (2, 8, 5)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (120, 255, 170), 0.16))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# a mini price card: big green candle, dashed START line, a "?" where the dip should be
cx, cy = 790, 900
g.rounded_rectangle([S(cx - 190), S(cy - 190), S(cx + 190), S(cy + 190)], radius=S(30), fill=(12, 16, 28, 255), outline=(200, 205, 210, 255), width=S(8))
for j in range(9):
    g.line([S(cx - 170 + j * 40), S(cy + 70), S(cx - 150 + j * 40), S(cy + 70)], fill=(255, 210, 74, 255), width=S(8))
g.line([S(cx - 60), S(cy - 170), S(cx - 60), S(cy + 90)], fill=INK, width=S(12))
g.rounded_rectangle([S(cx - 100), S(cy - 130), S(cx - 20), S(cy + 70)], radius=S(10), fill=(34, 229, 139, 255), outline=INK, width=S(8))
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(190))
g.text((S(cx + 75), S(cy - 20)), "?", font=f, fill=(255, 210, 74, 255), anchor="mm", stroke_width=S(10), stroke_fill=INK)
cv.glow(G, (120, 255, 170), 22, 0.55)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #43", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THE DIP", 540, 340, 220, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(120, 255, 170), glow=22)
cv.title("NEVER CAME.", 550, 560, 190, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1150, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "detective", prop_magnifier)
cv.sprite(roc, 300, 1210, spot=(215, 255, 225))
cv.title("JUMP IN OR WAIT?", 540, 1790, 110, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_43_kapak.png")
print("ok")
