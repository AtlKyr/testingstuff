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
cv.paste(vgrad(S(W), S(H), (58, 8, 16), (8, 2, 4)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 120, 140), 0.18))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
AFP = os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf")
# a glowing red "X" crossing badge (two crossing lines = the cross)
cx, cy = 790, 880
g.rounded_rectangle([S(cx - 170), S(cy - 150), S(cx + 170), S(cy + 150)], radius=S(30), fill=(250, 245, 235, 255), outline=INK, width=S(14))
g.line([S(cx - 140), S(cy - 70), S(cx + 140), S(cy + 90)], fill=(255, 210, 74, 255), width=S(18))
g.line([S(cx - 140), S(cy + 40), S(cx + 140), S(cy - 30)], fill=(30, 34, 40, 255), width=S(14))
for sg in (1, -1):
    g.line([S(cx - 70), S(cy - 70 * sg), S(cx + 70), S(cy + 70 * sg)], fill=INK, width=S(46))
    g.line([S(cx - 70), S(cy - 70 * sg), S(cx + 70), S(cy + 70 * sg)], fill=(240, 62, 90, 255), width=S(30))
cv.glow(G, (255, 140, 150), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #42", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("HE SOLD ON", 540, 340, 190, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(255, 120, 140), glow=22)
cv.title("APRIL 1ST.", 550, 545, 210, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1150, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "detective", prop_magnifier)
cv.sprite(roc, 330, 1210, spot=(255, 215, 220))
cv.title("SELL OR IGNORE IT?", 540, 1790, 100, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_42_kapak.png")
print("ok")
