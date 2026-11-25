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
cv.paste(vgrad(S(W), S(H), (10, 48, 30), (2, 10, 6)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (120, 255, 180), 0.16))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# a glowing calendar page "20??" with a green up-arrow (original drawing)
cx, cy = 790, 930
g.rounded_rectangle([S(cx - 170), S(cy - 190), S(cx + 170), S(cy + 190)], radius=S(20), fill=(250, 250, 250, 255), outline=INK, width=S(10))
g.rectangle([S(cx - 165), S(cy - 185), S(cx + 165), S(cy - 95)], fill=(240, 62, 90, 255))
f0 = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(50))
g.text((S(cx), S(cy - 140)), "NEXT YEAR", font=f0, fill=(255, 255, 255, 255), anchor="mm")
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(150))
g.text((S(cx), S(cy + 50)), "20??", font=f, fill=INK, anchor="mm")
ax, ay = cx - 250, cy + 40
g.polygon([(S(ax), S(ay - 150)), (S(ax + 80), S(ay - 40)), (S(ax + 32), S(ay - 40)), (S(ax + 32), S(ay + 110)), (S(ax - 32), S(ay + 110)), (S(ax - 32), S(ay - 40)), (S(ax - 80), S(ay - 40))], fill=(34, 229, 139, 255), outline=INK, width=S(8))
cv.glow(G, (34, 229, 139), 24, 0.55)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #47", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THE LAST ONE", 540, 350, 170, (255, 255, 255), (220, 235, 255), rot=-4, stroke=12, glow_col=(120, 170, 255), glow=22)
cv.title("SHOCKED HIM.", 540, 570, 170, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1165, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "party", None)
cv.sprite(roc, 300, 1210, spot=(255, 230, 190))
cv.title("CASH OR STAY IN?", 540, 1790, 120, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_47_kapak.png")
print("ok")
