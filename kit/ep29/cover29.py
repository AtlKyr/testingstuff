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
cv.paste(vgrad(S(W), S(H), (40, 18, 70), (5, 3, 14)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(760), S(820), (160, 110, 255), 0.25))
INKC = (20, 24, 28, 255)
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
# two calendar pages: red MON, green TUE with a big "?"
for (x, y, col, rot) in ((250, 730, (240, 62, 90, 255), 0), (560, 760, (34, 229, 139, 255), 0)):
    g.rounded_rectangle([S(x), S(y), S(x + 250), S(y + 270)], radius=S(22), fill=(250, 250, 250, 255), outline=(20, 24, 28, 255), width=S(8))
    g.rectangle([S(x + 4), S(y + 4), S(x + 246), S(y + 80)], fill=col)
    for k in (60, 190):
        g.rectangle([S(x + k - 9), S(y - 25), S(x + k + 9), S(y + 25)], fill=(20, 24, 28, 255))
cv.glow(G, (200, 120, 255), 22, 0.6)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #29", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN IT", 540, 340, 200, (255, 255, 255), (255, 220, 200), rot=-4, stroke=12, glow_col=(220, 60, 60), glow=22)
cv.title("STOPPED.", 550, 545, 220, (255, 230, 120), (255, 120, 40), rot=-4, stroke=13, glow_col=(255, 90, 30), glow=26)
cv.redacted("WINNER:", 470, 1080, 760, 116, rot=-3)
roc = rocco_sprite(22, "shock", "detective", prop_magnifier)
cv.sprite(roc, 520, 1160, spot=(255, 200, 190))
cv.title("REAL OR MYTH?", 540, 1790, 128, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_29_kapak.png")
from PIL import ImageFont
d = ImageDraw.Draw(cv.im)
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(56))
fq = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(150))
d.text((S(375), S(772)), "MON", font=f, fill=(255, 255, 255), anchor="mm")
d.text((S(685), S(802)), "TUE", font=f, fill=(20, 24, 28), anchor="mm")
d.text((S(375), S(930)), "RED", font=ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(90)), fill=(240, 62, 90), anchor="mm")
d.text((S(685), S(950)), "?", font=fq, fill=(34, 180, 110), anchor="mm")
cv.save("StrategyAutopsy_29_kapak.png")
print("ok")
