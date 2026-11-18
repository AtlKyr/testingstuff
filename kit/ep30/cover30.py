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
cv.paste(radial(S(W), S(H), S(780), S(760), S(700), (60, 255, 140), 0.22))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# four falling red candles + one sealed green "?" candle
for k in range(4):
    x = 130 + k * 120; y = 720 + k * 70
    g.rectangle([S(x + 30), S(y - 40), S(x + 40), S(y + 200)], fill=INK)
    g.rounded_rectangle([S(x), S(y), S(x + 70), S(y + 150)], radius=S(8), fill=(240, 62, 90, 255), outline=INK, width=S(6))
x, y = 640, 560
g.rectangle([S(x + 40), S(y - 60), S(x + 52), S(y + 470)], fill=INK)
g.rounded_rectangle([S(x), S(y), S(x + 92), S(y + 400)], radius=S(10), fill=(34, 229, 139, 255), outline=INK, width=S(7))
g.text((S(x + 18), S(y + 120)), "?", fill=INK, font=ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(130)))
cv.glow(G, (60, 255, 140), 24, 0.7)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #30", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 330, 190, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(220, 60, 60), glow=22)
cv.title("EXPLODED.", 550, 530, 220, (150, 255, 190), (30, 200, 110), rot=-4, stroke=13, glow_col=(40, 220, 120), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 200, 190))
cv.title("BUY OR WAIT?", 540, 1790, 130, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_30_kapak.png")
print("ok")
