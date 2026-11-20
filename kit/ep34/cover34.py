import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math, os
from coverlib import *
from PIL import ImageDraw, ImageFont


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
cv = Cover()
cv.paste(vgrad(S(W), S(H), (58, 8, 22), (6, 2, 8)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 90, 110), 0.22))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AF = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(150))
# a big shop price tag, tilted, with a "?" price
cx, cy, ang = 770, 900, math.radians(-14)
pts = [(-230, -110), (150, -110), (240, 0), (150, 110), (-230, 110)]
def rot(p):
    x, y = p; return (S(cx + x * math.cos(ang) - y * math.sin(ang)), S(cy + x * math.sin(ang) + y * math.cos(ang)))
g.polygon([rot(p) for p in pts], fill=(240, 62, 90, 255), outline=INK, width=S(12))
hx, hy = rot((165, 0)); g.ellipse([hx - S(22), hy - S(22), hx + S(22), hy + S(22)], outline=INK, width=S(10))
g.line([hx, hy, S(cx + 330), S(cy - 260)], fill=(240, 230, 210, 255), width=S(6))
tx, ty = rot((-50, -10))
g.text((tx, ty), "$???", fill=(255, 255, 255, 255), font=AF, anchor="mm", stroke_width=S(6), stroke_fill=INK)
cv.glow(G, (255, 90, 120), 22, 0.65)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #34", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN THE", 540, 340, 190, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(255, 120, 140), glow=22)
cv.title("SALE CAME.", 550, 540, 200, (255, 236, 160), (255, 170, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1100, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 330, 1170, spot=(255, 200, 180))
cv.title("BUY OR WAIT?", 540, 1790, 130, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_34_kapak.png")
print("ok")
