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
cv.paste(vgrad(S(W), S(H), (6, 44, 28), (2, 8, 5)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (120, 255, 170), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AFP = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# a glowing green "+2%" balloon on a string
cx, cy = 800, 850
g.line([S(cx), S(cy + 170), S(cx - 20), S(cy + 200), S(cx + 6), S(cy + 225)], fill=(240, 240, 240, 255), width=S(6))
g.ellipse([S(cx - 140), S(cy - 165), S(cx + 140), S(cy + 165)], fill=(34, 229, 139, 255), outline=INK, width=S(12))
g.polygon([S(cx - 18), S(cy + 182), S(cx + 18), S(cy + 182), S(cx), S(cy + 158)], fill=(34, 229, 139, 255))
g.ellipse([S(cx - 90), S(cy - 120), S(cx - 40), S(cy - 50)], fill=(255, 255, 255, 110))
g.text((S(cx), S(cy + 8)), "+2%", fill=INK, font=ImageFont.truetype(AFP, S(110)), anchor="mm")
cv.glow(G, (140, 255, 180), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #40", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN CAME", 540, 340, 190, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(120, 255, 170), glow=22)
cv.title("ONE TUESDAY.", 550, 545, 180, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1150, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "party", prop_magnifier)
cv.sprite(roc, 330, 1210, spot=(200, 255, 220))
cv.title("SELL THE POP OR HOLD?", 540, 1790, 100, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_40_kapak.png")
print("ok")
