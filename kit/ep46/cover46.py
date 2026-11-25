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
cv.paste(vgrad(S(W), S(H), (14, 26, 64), (3, 5, 16)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 200, 90), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# a glowing roadside milestone stone "50K" with a gold "?" (original drawing)
cx, cy = 800, 935
g.rounded_rectangle([S(cx - 170), S(cy - 120), S(cx + 170), S(cy + 200)], radius=S(16), fill=(184, 190, 200, 255), outline=INK, width=S(10))
g.pieslice([S(cx - 170), S(cy - 290), S(cx + 170), S(cy + 50)], 180, 360, fill=(184, 190, 200, 255), outline=INK, width=S(10))
g.rectangle([S(cx - 160), S(cy - 125), S(cx + 160), S(cy - 110)], fill=(184, 190, 200, 255))
g.rectangle([S(cx - 210), S(cy + 190), S(cx + 210), S(cy + 230)], fill=(58, 42, 26, 255))
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(130))
g.text((S(cx), S(cy + 20)), "50K", font=f, fill=INK, anchor="mm")
f2 = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(170))
g.text((S(cx - 245), S(cy - 120)), "?", font=f2, fill=(255, 210, 74, 255), anchor="mm", stroke_width=S(10), stroke_fill=INK)
cv.glow(G, (255, 200, 90), 24, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #46", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("HE CAME BACK", 540, 350, 170, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(120, 170, 255), glow=22)
cv.title("IN AUGUST.", 540, 570, 170, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "party", None)
cv.sprite(roc, 300, 1210, spot=(255, 230, 190))
cv.title("CASH OUT OR HOLD?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_46_kapak.png")
print("ok")
