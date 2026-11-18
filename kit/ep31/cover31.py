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
cv.paste(vgrad(S(W), S(H), (70, 12, 26), (6, 3, 10)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(760), (170, 120, 255), 0.25))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AF = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(70))
# a row of 12 month pages; the last one is a sealed red "?" page
for m in range(12):
    x = 150 + (m % 6) * 135; y = 700 + (m // 6) * 150
    g.rounded_rectangle([S(x), S(y), S(x + 110), S(y + 125)], radius=S(12), fill=(245, 236, 214, 255), outline=INK, width=S(6))
    g.rectangle([S(x + 3), S(y + 3), S(x + 107), S(y + 32)], fill=(179, 140, 255, 255) if m != 11 else (240, 62, 90, 255))
    if m == 11:
        g.text((S(x + 34), S(y + 36)), "?", fill=INK, font=AF)
cv.glow(G, (170, 120, 255), 22, 0.7)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #31", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 330, 190, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(220, 60, 60), glow=22)
cv.title("FLIPPED.", 550, 530, 220, (230, 210, 255), (150, 100, 255), rot=-4, stroke=13, glow_col=(140, 90, 255), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 200, 190))
cv.title("MONTHLY OR NEVER?", 540, 1790, 112, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_31_kapak.png")
print("ok")
