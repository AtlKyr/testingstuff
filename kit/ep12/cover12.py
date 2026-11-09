import sys; sys.path.insert(0, ".."); sys.path.insert(0, ".")
import cairo, math
from coverlib import *
from PIL import ImageDraw


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + px * 4.7, y - px * 6.3
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - px * 2.1, cy + px * 2.1)
    ctx.set_source_rgba(0.42, 0.29, 0.18, 1); ctx.set_line_width(px * 0.85); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, px * 3.0, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(0.08, 0.09, 0.11, 1); ctx.set_line_width(px * 0.65); ctx.stroke()
cv = Cover()
cv.paste(vgrad(S(W), S(H), (8, 52, 36), (2, 10, 8)).convert("RGBA"))
# right half: navy "wait" world (diagonal)
R = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(R)
d.polygon([(S(610), 0), (S(W), 0), (S(W), S(H)), (S(470), S(H))], fill=(22, 28, 80, 255))
cv.paste(R)
cv.paste(radial(S(W), S(H), S(260), S(700), S(700), (40, 230, 140), 0.25))
cv.paste(radial(S(W), S(H), S(820), S(700), S(600), (255, 210, 74), 0.18))
# record peak line with a drop (glowing), top area
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
pts = [(80, 980), (200, 900), (280, 930), (380, 820), (460, 850), (560, 720), (640, 750), (740, 610), (800, 640), (860, 560)]
d.line([(S(x), S(y)) for x, y in pts], fill=(34, 229, 139, 255), width=S(16), joint="curve")
d.line([(S(860), S(560)), (S(930), S(700)), (S(990), S(680)), (S(1040), S(790))], fill=(240, 62, 90, 255), width=S(16), joint="curve")
for k in range(16):
    d.rectangle([S(60 + k * 62), S(552), S(92 + k * 62), S(560)], fill=(255, 210, 74, 220))
cv.glow(L, (255, 255, 255), 16, 0.5)
cv.paste(L)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #12", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("RECORD", 760, 330, 120, (255, 236, 160), (255, 196, 40), rot=4, stroke=10, glow_col=(0, 0, 0), glow=14)
cv.title("S&P -5.6%", 520, 470, 150, (255, 130, 150), (230, 40, 70), rot=-4, stroke=12, glow_col=(255, 40, 80), glow=24)
cv.redacted("WINNER:", 540, 1000, 820, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1110, spot=(220, 255, 230))
cv.title("BUY OR WAIT?", 540, 1790, 170, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_12_kapak.png")
print("ok")
