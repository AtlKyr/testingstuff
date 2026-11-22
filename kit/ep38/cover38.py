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
cv.paste(vgrad(S(W), S(H), (60, 26, 8), (10, 4, 2)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 150, 60), 0.22))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AFP = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# falling autumn leaves
import random; random.seed(4)
for k in range(26):
    x, y, r = random.randint(0, 1080), random.randint(700, 1900), random.randint(14, 30)
    col = random.choice([(232, 106, 28, 200), (217, 58, 30, 200), (242, 177, 42, 200)])
    g.ellipse([S(x - r), S(y - r // 2), S(x + r), S(y + r // 2)], fill=col)
# a sealed calendar page with a hidden year
cx, cy = 790, 870
g.rounded_rectangle([S(cx - 170), S(cy - 180), S(cx + 170), S(cy + 180)], radius=S(22), fill=(255, 255, 255, 255), outline=INK, width=S(12))
g.rectangle([S(cx - 164), S(cy - 174), S(cx + 164), S(cy - 80)], fill=(240, 62, 90, 255))
g.text((S(cx), S(cy - 127)), "NOV 20??", fill=(255, 255, 255), font=ImageFont.truetype(AFP, S(62)), anchor="mm")
g.text((S(cx), S(cy + 50)), "?", fill=INK, font=ImageFont.truetype(AFP, S(200)), anchor="mm")
cv.glow(G, (255, 170, 80), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #38", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("HE MISSED", 540, 340, 190, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(255, 120, 140), glow=22)
cv.title("THIS ONE.", 550, 545, 210, (255, 236, 160), (255, 170, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1065, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "tophat", prop_magnifier)
cv.sprite(roc, 330, 1185, spot=(255, 200, 160))
cv.title("SIT OUT OR HOLD?", 540, 1790, 112, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_38_kapak.png")
print("ok")
