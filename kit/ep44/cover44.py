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
cv.paste(vgrad(S(W), S(H), (52, 38, 8), (8, 5, 1)).convert("RGBA"))
cv.paste(radial(S(W), S(H), S(540), S(860), S(760), (255, 220, 120), 0.16))
G = Image.new("RGBA", cv.im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(G)
INK = (20, 24, 28, 255)
# a paycheck with a red "?" stamp (the twin's file)
cx, cy = 770, 900
g.rounded_rectangle([S(cx - 230), S(cy - 130), S(cx + 230), S(cy + 130)], radius=S(18), fill=(232, 245, 233, 255), outline=INK, width=S(10))
g.rectangle([S(cx - 225), S(cy - 125), S(cx + 225), S(cy - 75)], fill=(46, 125, 50, 255))
fs = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(40))
g.text((S(cx - 205), S(cy - 100)), "PAYCHECK", font=fs, fill=(255, 255, 255, 255), anchor="lm")
fb = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(90))
g.text((S(cx - 60), S(cy + 30)), "$40,000", font=fb, fill=(11, 138, 76, 255), anchor="mm")
f = ImageFont.truetype(os.path.expanduser("~/.fonts/anton-latin-400-normal.ttf"), S(190))
g.text((S(cx + 170), S(cy + 70)), "?", font=f, fill=(240, 62, 90, 255), anchor="mm", stroke_width=S(10), stroke_fill=INK)
cv.glow(G, (255, 220, 140), 22, 0.5)
cv.paste(G)
cv.bottom_fade(1250, alpha=0.95)
cv.stamp("CASE #44", 300, 150, 70, sub="STRATEGY AUTOPSY", rot=-4)
cv.title("THEN HIS", 540, 340, 220, (255, 255, 255), (220, 255, 230), rot=-4, stroke=12, glow_col=(255, 200, 90), glow=22)
cv.title("TWIN SOLD.", 550, 560, 210, (255, 236, 160), (255, 190, 60), rot=-4, stroke=13, glow_col=(255, 190, 60), glow=26)
cv.redacted("WINNER:", 470, 1150, 760, 116, rot=-3)
roc = rocco_sprite(19, "shock", "tophat", None)
cv.sprite(roc, 300, 1210, spot=(255, 235, 200))
cv.title("BROKE OR RICHER?", 540, 1790, 110, (255, 255, 255), (255, 214, 64), stroke=12, extrude=12, glow_col=(0, 0, 0), glow=22)
cv.save("StrategyAutopsy_44_kapak.png")
print("ok")
