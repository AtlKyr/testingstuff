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
# a glowing dividend check with a hidden amount
cx, cy = 720, 860
g.rounded_rectangle([S(cx - 300), S(cy - 150), S(cx + 300), S(cy + 150)], radius=S(18), fill=(244, 235, 208, 255), outline=INK, width=S(12))
g.rectangle([S(cx - 294), S(cy - 144), S(cx + 294), S(cy - 88)], fill=(34, 229, 139, 255))
g.text((S(cx - 270), S(cy - 116)), "DIVIDEND", fill=INK, font=ImageFont.truetype(AFP, S(44)), anchor="lm")
g.text((S(cx - 270), S(cy - 30)), "PAY TO: YOU", fill=INK, font=ImageFont.truetype(AFP, S(40)), anchor="lm")
g.rounded_rectangle([S(cx + 40), S(cy - 60), S(cx + 270), S(cy + 30)], radius=S(10), fill=(255, 255, 255, 255), outline=INK, width=S(6))
g.text((S(cx + 155), S(cy - 15)), "$??", fill=(11, 138, 76), font=ImageFont.truetype(AFP, S(70)), anchor="mm")
for k in range(3):
    g.rectangle([S(cx - 270), S(cy + 50 + k * 28), S(cx - 270 + 330 - k * 80), S(cy + 58 + k * 28)], fill=(20, 24, 28, 120))
cv.glow(G, (140, 255, 180), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #39", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 340, 190, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(120, 255, 170), glow=22)
cv.title("QUIETLY GREW.", 550, 545, 170, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1100, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "party", prop_magnifier)
cv.sprite(roc, 330, 1210, spot=(200, 255, 220))
cv.title("POCKET OR REINVEST?", 540, 1790, 100, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_39_kapak.png")
print("ok")
