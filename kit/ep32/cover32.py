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
cv.paste(vgrad(S(W), S(H), (74, 10, 22), (6, 3, 8)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(760), (255, 90, 110), 0.22))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AF = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(80))
# five red candles stepping down + a sealed sixth "?" candle
for k in range(6):
    x = 130 + k * 140; y = 700 + k * 30
    if k < 5:
        g.line([S(x + 40), S(y - 40), S(x + 40), S(y + 170)], fill=INK, width=S(8))
        g.rounded_rectangle([S(x), S(y), S(x + 80), S(y + 130)], radius=S(10), fill=(240, 62, 90, 255), outline=INK, width=S(6))
    else:
        g.rounded_rectangle([S(x), S(y), S(x + 90), S(y + 140)], radius=S(12), fill=(255, 210, 74, 255), outline=INK, width=S(7))
        g.text((S(x + 24), S(y + 16)), "?", fill=INK, font=AF)
cv.glow(G, (255, 90, 110), 22, 0.7)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #32", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("WATCH WHAT", 540, 340, 170, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(220, 60, 60), glow=22)
cv.title("CAME NEXT.", 550, 540, 200, (255, 236, 160), (255, 170, 40), rot=-4, stroke=13, glow_col=(255, 140, 40), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "fire", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 200, 190))
cv.title("SELL OR SIT TIGHT?", 540, 1790, 112, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_32_kapak.png")
print("ok")
