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
cv.paste(vgrad(S(W), S(H), (46, 26, 8), (8, 4, 2)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 210, 90), 0.20))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AF = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(150))
# a glowing "2X" lever badge with a hidden value
cx, cy = 790, 860
g.ellipse([S(cx - 190), S(cy - 190), S(cx + 190), S(cy + 190)], fill=(255, 210, 74, 255), outline=INK, width=S(12))
g.text((S(cx), S(cy - 30)), "2X", fill=INK, font=ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(190)), anchor="mm")
g.text((S(cx), S(cy + 115)), "DAILY", fill=INK, font=ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(56)), anchor="mm")
cv.glow(G, (255, 210, 90), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #37", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 340, 190, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(255, 120, 140), glow=22)
cv.title("VANISHED.", 550, 545, 210, (255, 236, 160), (255, 170, 60), rot=-4, stroke=13, glow_col=(255, 150, 60), glow=26)
cv.redacted("WINNER:", 470, 1065, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "race", prop_magnifier)
cv.sprite(roc, 330, 1185, spot=(255, 200, 180))
cv.title("RICH OR WRECKED?", 540, 1790, 112, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_37_kapak.png")
print("ok")
