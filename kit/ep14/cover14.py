import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math, os
from coverlib import *
from PIL import ImageDraw


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
cv = Cover()
cv.paste(vgrad(S(W), S(H), (8, 84, 58), (2, 14, 10)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(760), S(720), S(820), (34, 229, 139), 0.30))
# candles: a red slide, then one huge green candle
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
INKC = (20, 24, 28, 255)
x = 90
for k, (top, h) in enumerate([(560, 150), (640, 170), (740, 120), (800, 160), (880, 130)]):
    d.rectangle([S(x + 36), S(top - 34), S(x + 46), S(top + h + 34)], fill=INKC)
    d.rounded_rectangle([S(x), S(top), S(x + 82), S(top + h)], radius=S(10), fill=(240, 62, 90, 255), outline=INKC, width=S(6))
    x += 118
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
g.rectangle([S(x + 84), S(545), S(x + 100), S(1040)], fill=INKC)
g.rounded_rectangle([S(x + 10), S(600), S(x + 174), S(980)], radius=S(14), fill=(34, 229, 139, 255), outline=INKC, width=S(8))
cv.glow(G, (34, 229, 139), 26, 0.9)
cv.paste(L); cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #14", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("CHASE THE", 540, 330, 150, (255, 255, 255), (200, 255, 225), rot=-4, stroke=12, glow_col=(20, 160, 100), glow=22)
cv.title("BOUNCE?", 560, 480, 170, (255, 230, 170), (255, 150, 30), rot=-4, stroke=12, glow_col=(255, 120, 30), glow=22)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(200, 255, 225))
cv.title("ALL CLEAR?", 540, 1790, 180, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_14_kapak.png")
print("ok")
