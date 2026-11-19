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
cv.paste(vgrad(S(W), S(H), (40, 10, 52), (5, 3, 12)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(800), S(760), (255, 200, 80), 0.20))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AF = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(64))
# fear gauge, needle resting in the calm zone, with a sleepy "Z Z"
cx, cy, r = 540, 960, 230
g.pieslice([S(cx - r - 14), S(cy - r - 14), S(cx + r + 14), S(cy + r + 14)], 180, 360, fill=(12, 16, 28, 255), outline=INK, width=S(10))
for k, col in enumerate(((34, 229, 139, 255), (255, 210, 74, 255), (240, 62, 90, 255))):
    g.arc([S(cx - r + 30), S(cy - r + 30), S(cx + r - 30), S(cy + r - 30)], 180 + k * 60, 180 + (k + 1) * 60, fill=col, width=S(44))
ang = math.pi + math.pi * 0.14
g.line([S(cx), S(cy), S(cx + math.cos(ang) * 180), S(cy + math.sin(ang) * 180)], fill=(255, 255, 255, 255), width=S(16))
g.ellipse([S(cx - 24), S(cy - 24), S(cx + 24), S(cy + 24)], fill=INK)
g.text((S(cx + 250), S(cy - 190)), "Z", fill=(200, 210, 255, 255), font=AF)
g.text((S(cx + 310), S(cy - 250)), "Z", fill=(200, 210, 255, 200), font=AF)
cv.glow(G, (255, 200, 80), 20, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #33", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 340, 190, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(200, 120, 255), glow=22)
cv.title("WENT SILENT.", 550, 540, 190, (220, 235, 255), (120, 180, 255), rot=-4, stroke=13, glow_col=(90, 140, 255), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "tophat", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 220, 160))
cv.title("BUY OR JUST HOLD?", 540, 1790, 112, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_33_kapak.png")
print("ok")
