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
cv.paste(vgrad(S(W), S(H), (8, 40, 44), (2, 6, 8)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 210, 90), 0.20))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AF = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(150))
# a big glowing envelope (the bill) with a hidden amount
cx, cy, ang = 760, 830, math.radians(-10)
def rot(p):
    x, y = p; return (S(cx + x * math.cos(ang) - y * math.sin(ang)), S(cy + x * math.sin(ang) + y * math.cos(ang)))
g.polygon([rot(p) for p in [(-250, -160), (250, -160), (250, 160), (-250, 160)]], fill=(243, 236, 220, 255), outline=INK, width=S(12))
g.line([rot((-250, -160)), rot((0, 20)), rot((250, -160))], fill=INK, width=S(10))
g.polygon([rot(p) for p in [(150, -140), (225, -140), (225, -55), (150, -55)]], fill=(240, 62, 90, 255))
tx, ty = rot((0, 95))
g.text((tx, ty), "$??,???", fill=(240, 62, 90, 255), font=ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(96)), anchor="mm", stroke_width=S(5), stroke_fill=INK)
cv.glow(G, (255, 210, 90), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #35", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("IT WAS NEVER", 540, 340, 170, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(255, 120, 140), glow=22)
cv.title("BILLED.", 550, 545, 220, (255, 236, 160), (255, 170, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("REAL COST:", 470, 1065, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "tophat", prop_magnifier)
cv.sprite(roc, 330, 1185, spot=(255, 200, 180))
cv.title("A LITTLE OR A LOT?", 540, 1790, 112, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_35_kapak.png")
print("ok")
