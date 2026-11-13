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
cv.paste(vgrad(S(W), S(H), (40, 18, 70), (4, 3, 12)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(860), S(820), S(520), (200, 190, 255), 0.22))
INKC = (20, 24, 28, 255)
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
# calendar page FRIDAY 13 (right side, tilted later via glow layer)
x0, y0, w, h = 640, 700, 320, 330
g.rounded_rectangle([S(x0), S(y0), S(x0 + w), S(y0 + h)], radius=S(26), fill=(247, 244, 236, 255), outline=INKC, width=S(8))
g.rounded_rectangle([S(x0), S(y0), S(x0 + w), S(y0 + 95)], radius=S(26), fill=(240, 62, 90, 255), outline=INKC, width=S(8))
g.rectangle([S(x0 + 4), S(y0 + 60), S(x0 + w - 4), S(y0 + 95)], fill=(240, 62, 90, 255))
g.text((S(x0 + w / 2), S(y0 + 50)), "FRIDAY", font=font(ANTON, 62), fill=(255, 255, 255, 255), anchor="mm")
g.text((S(x0 + w / 2), S(y0 + 215)), "13", font=font(ANTON, 200), fill=(20, 24, 28, 255), anchor="mm")
G = G.rotate(-6, resample=Image.BICUBIC, center=(S(x0 + w / 2), S(y0 + h / 2)))
cv.glow(G, (200, 190, 255), 26, 0.8)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #21", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THAT DAY SHOCKED", 540, 340, 130, (255, 255, 255), (220, 210, 255), rot=-4, stroke=12, glow_col=(120, 60, 220), glow=22)
cv.title("EVERYONE!", 560, 520, 210, (190, 255, 220), (34, 229, 139), rot=-4, stroke=13, glow_col=(30, 200, 120), glow=24)
cv.redacted("WINNER:", 470, 1110, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 400, 1190, spot=(220, 210, 255))
cv.title("SKIP OR HOLD?", 540, 1790, 170, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_21_kapak.png")
print("ok")
