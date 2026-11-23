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
cv.paste(vgrad(S(W), S(H), (8, 26, 58), (2, 5, 12)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (120, 190, 255), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AFP = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# a glowing blue "60/40" shield with a crack
cx, cy = 790, 880
pts = [(0, -190), (95, -150), (170, -165), (175, 30), (110, 145), (0, 215), (-110, 145), (-175, 30), (-170, -165), (-95, -150)]
g.polygon([(S(cx + x), S(cy + y)) for x, y in pts], fill=(79, 195, 247, 255), outline=INK, width=S(14))
g.text((S(cx), S(cy + 10)), "60/40", fill=INK, font=ImageFont.truetype(AFP, S(100)), anchor="mm")
g.line([S(cx + 15), S(cy - 190), S(cx - 20), S(cy - 90), S(cx + 30), S(cy - 15), S(cx - 15), S(cy + 90), S(cx + 8), S(cy + 212)], fill=INK, width=S(14))
cv.glow(G, (140, 200, 255), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #41", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN THE SHIELD", 540, 340, 160, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(120, 190, 255), glow=22)
cv.title("CRACKED.", 550, 545, 210, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1150, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "detective", prop_magnifier)
cv.sprite(roc, 330, 1210, spot=(200, 225, 255))
cv.title("ALL STOCKS OR 60/40?", 540, 1790, 100, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_41_kapak.png")
print("ok")
