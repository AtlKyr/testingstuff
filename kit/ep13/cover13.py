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
cv.paste(vgrad(S(W), S(H), (64, 20, 80), (12, 4, 20)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(600), S(820), (255, 159, 28), 0.28))
# week strip of calendar pages: MON crossed out
L = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
for k, day in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
    x = 70 + k * 192; y = 560 + (k % 2) * 20
    col = (240, 62, 90, 255) if k == 0 else (244, 236, 216, 255)
    d.rounded_rectangle([S(x), S(y), S(x + 170), S(y + 200)], radius=S(16), fill=col, outline=(20, 24, 28, 255), width=S(6))
    d.rectangle([S(x + 3), S(y + 3), S(x + 167), S(y + 52)], fill=(20, 24, 28, 230))
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(40))
        d.text((S(x + 85), S(y + 28)), day, font=f, fill=(255, 255, 255, 255), anchor="mm")
    except Exception:
        pass
    if k == 0:
        d.line([S(x + 30), S(y + 80), S(x + 140), S(y + 180)], fill=(255, 255, 255, 255), width=S(16))
        d.line([S(x + 140), S(y + 80), S(x + 30), S(y + 180)], fill=(255, 255, 255, 255), width=S(16))
cv.glow(L, (255, 160, 60), 14, 0.5)
cv.paste(L)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #13", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("SKIP MONDAYS?", 540, 420, 150, (255, 230, 170), (255, 150, 30), rot=-4, stroke=12, glow_col=(255, 120, 30), glow=22)
cv.redacted("WINNER:", 540, 960, 820, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1100, spot=(255, 230, 200))
cv.title("WORTH IT?", 540, 1790, 180, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_13_kapak.png")
print("ok")
