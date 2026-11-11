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
cv.paste(vgrad(S(W), S(H), (92, 16, 26), (14, 2, 6)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (255, 77, 106), 0.30))
INKC = (20, 24, 28, 255)
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
stone = (233, 226, 208, 255)
cx, base = 540, 1010
d.polygon([(S(cx - 300), S(base - 380)), (S(cx), S(base - 520)), (S(cx + 300), S(base - 380))], fill=stone, outline=INKC, width=S(8))
d.rectangle([S(cx - 310), S(base - 385), S(cx + 310), S(base - 340)], fill=stone, outline=INKC, width=S(6))
for k in range(6):
    x = cx - 260 + k * 104
    d.rectangle([S(x - 26), S(base - 340), S(x + 26), S(base - 40)], fill=stone, outline=INKC, width=S(5))
d.rectangle([S(cx - 340), S(base - 40), S(cx + 340), S(base)], fill=stone, outline=INKC, width=S(6))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
ax = 870
g.polygon([(S(ax), S(470)), (S(ax + 110), S(600)), (S(ax + 45), S(600)), (S(ax + 45), S(820)), (S(ax - 45), S(820)), (S(ax - 45), S(600)), (S(ax - 110), S(600))],
          fill=(255, 77, 106, 255), outline=INKC, width=S(8))
cv.glow(G, (255, 77, 106), 26, 0.9)
cv.paste(L); cv.paste(G)
cv.text("%", 870, 690, 120, (255, 255, 255), stroke=8)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #16", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THE FED", 540, 330, 150, (255, 255, 255), (255, 210, 215), rot=-4, stroke=12, glow_col=(200, 30, 60), glow=22)
cv.title("HIKES...", 560, 480, 170, (255, 230, 170), (255, 120, 60), rot=-4, stroke=12, glow_col=(255, 80, 40), glow=22)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 210, 215))
cv.title("SELL OR HOLD?", 540, 1790, 160, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_16_kapak.png")
print("ok")
