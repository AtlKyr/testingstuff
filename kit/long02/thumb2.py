import cairo, math, random
from long2_render import *
from PIL import Image


def save(surf, name):
    surf.write_to_png("/tmp/th.png")
    Image.open("/tmp/th.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(name)


# ---------------- A: -5.5% / WHAT NEXT?
surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
bg_fill(ctx, (0x4A, 0x0E, 0x18), (0x14, 0x04, 0x08))
god_rays(ctx, 1500, 560, 0.4, 0.08, C["red"], 16, 1700)
rr = random.Random(5)
# big falling candle chart behind
x = 60; y = 300
for k in range(22):
    up = k < 12 and rr.random() < 0.6
    h = 40 + rr.random() * 60 if k != 19 else 330
    col = C["green"] if up else C["red"]
    y0 = y if up else y
    if not up:
        rect(ctx, x + 14, y - 20, 6, h + 40, col, 0.5); rect(ctx, x, y, 34, h, col, 0.55); y += h * 0.8
    else:
        rect(ctx, x + 14, y - h - 20, 6, h + 40, col, 0.5); rect(ctx, x, y - h, 34, h, col, 0.55); y -= h * 0.6
    x += 56
ctx.save(); ctx.translate(560, 470); ctx.rotate(-0.06)
text(ctx, "-5.5%", 0, 120, 360, C["white"], 1, HEAD, True, "center", outline=30, ocol=C["ink"])
ctx.restore()
ctx.save(); ctx.translate(380, 130); ctx.rotate(-0.04)
card(ctx, -300, -62, 600, 124, C["yellow"], 1, 16)
text(ctx, "NASDAQ CRASH", 0, 30, 76, C["ink"], 1, HEAD, True, "center")
ctx.restore()
ctx.save(); ctx.translate(620, 900); ctx.rotate(0.03)
card(ctx, -500, -90, 1000, 180, C["white"], 1, 22)
text(ctx, "WHAT HAPPENS NEXT?", 0, 30, 82, C["ink"], 1, HEAD, True, "center")
ctx.restore()
draw_rocco(ctx, 1270, 300, 30, "shock", "fire")
vignette(ctx); paper_grain(ctx, 0.05)
save(surf, "StrategyAutopsy_Long02_thumb_A.png")

# ---------------- B: 39 mystery tiles
surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(surf)
bg_fill(ctx, (0xF6, 0xD3, 0x6B), (0xE8, 0x9A, 0x3A))
god_rays(ctx, 600, 560, 0.2, 0.14, C["white"], 16, 1500)
ctx.save(); ctx.translate(620, 150); ctx.rotate(-0.03)
card(ctx, -540, -95, 1080, 190, C["red"], 1, 22)
text(ctx, "39 CRASH DAYS", 0, 40, 112, C["white"], 1, HEAD, True, "center")
ctx.restore()
for j in range(39):
    c_, r_ = j % 13, j // 13
    ctx.save(); ctx.translate(130 + c_ * 84, 400 + r_ * 104); ctx.rotate(math.sin(j * 1.7) * 0.06)
    rect(ctx, -36, -44, 72, 88, C["ink"], 0.92)
    text(ctx, "?", 0, 24, 62, C["cream"], 1, HEAD, True, "center")
    ctx.restore()
ctx.save(); ctx.translate(620, 900); ctx.rotate(0.03)
card(ctx, -470, -85, 940, 170, C["white"], 1, 22)
text(ctx, "1 YEAR LATER...?", 0, 34, 104, C["ink"], 1, HEAD, True, "center")
ctx.restore()
draw_rocco(ctx, 1270, 330, 30, "shock", "detective")
prop_magnifier(ctx, 1270 + 30 * 16.5, 330 + 30 * 13.5, 30, 0.3)
vignette(ctx); paper_grain(ctx, 0.05)
save(surf, "StrategyAutopsy_Long02_thumb_B.png")
print("ok")
