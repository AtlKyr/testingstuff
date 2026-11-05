"""High-quality cover (kapak) toolkit for Strategy Autopsy — PIL, rendered at 2x and downsampled (LANCZOS).

Why: the cairo covers (#1-#8) looked flat/cheap: thin outlines, no depth, paper grain noise, pixel Rocco blown up and
overlapped by boxes, low-contrast pill text. This module gives thumbnail-grade typography (Anton, thick stroke, gradient
fill, hard shadow + soft glow), cinematic backgrounds, rim-lit Rocco and clean case-file props.

    from coverlib import *
    cv = Cover()                                  # 1080x1920 logical, drawn at SS=2
    cv.split_bg(DAY, NIGHT) ...                   # see cover8.py for a full example
    cv.save("StrategyAutopsy_NN_kapak.png")
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

SS = 2
W, H = 1080, 1920
ANTON = "/root/.fonts/anton-latin-400-normal.ttf"
INTER_BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
MONO = "/root/.fonts/jetbrains-mono-latin-700-normal.ttf"
INK = (14, 16, 22)


def S(v):
    return int(round(v * SS))


def font(path, size):
    return ImageFont.truetype(path, S(size))


def vgrad(w, h, top, bot):
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(top, np.float32)[None, None, :]; b = np.array(bot, np.float32)[None, None, :]
    arr = (a + (b - a) * t) * np.ones((1, w, 1), np.float32)
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGB")


def radial(w, h, cx, cy, r, col, alpha=1.0):
    """soft radial glow layer (RGBA)"""
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** 2 * 255 * alpha
    out = np.zeros((h, w, 4), np.uint8); out[..., :3] = col; out[..., 3] = a.astype(np.uint8)
    return Image.fromarray(out, "RGBA")


class Cover:
    def __init__(self):
        self.im = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 255))

    # ------------------------------------------------------------ layers
    def paste(self, layer, xy=(0, 0)):
        self.im.alpha_composite(layer, (int(xy[0]), int(xy[1])))

    def glow(self, mask_layer, col, blur, strength=1.0):
        """colored glow from the alpha of mask_layer"""
        a = mask_layer.split()[3].filter(ImageFilter.GaussianBlur(S(blur)))
        if strength != 1.0:
            a = a.point(lambda v: min(255, int(v * strength)))
        g = Image.new("RGBA", self.im.size, col + (0,)); g.putalpha(a)
        self.paste(g)

    def shadow(self, layer, dx=10, dy=14, blur=10, alpha=0.55):
        a = layer.split()[3].filter(ImageFilter.GaussianBlur(S(blur))).point(lambda v: int(v * alpha))
        sh = Image.new("RGBA", self.im.size, (0, 0, 0, 0)); sh.putalpha(a)
        self.paste(sh, (S(dx), S(dy)))

    # ------------------------------------------------------------ backgrounds
    def split_bg(self, seam_top=640, seam_bot=420, day=((70, 190, 255), (255, 214, 140)), night=((32, 30, 96), (6, 6, 24)), t=0.4):
        w, h = self.im.size
        dayim = vgrad(w, h, *day).convert("RGBA")
        dayim.alpha_composite(radial(w, h, S(190), S(330), S(620), (255, 240, 170), 0.9))
        nightim = vgrad(w, h, *night).convert("RGBA")
        nightim.alpha_composite(radial(w, h, S(880), S(330), S(560), (150, 140, 255), 0.55))
        # stars
        d = ImageDraw.Draw(nightim); rr = random.Random(3)
        for k in range(140):
            x, y = rr.random() * w, rr.random() * h * 0.7; s = S(1 + rr.random() * 2.6); a = int(120 + rr.random() * 135)
            d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, a))
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).polygon([(S(seam_top), 0), (w, 0), (w, h), (S(seam_bot), h)], fill=255)
        self.im = Image.composite(nightim, dayim, mask)
        # glowing seam
        seam = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(seam).line([(S(seam_top), 0), (S(seam_bot), h)], fill=(255, 255, 255, 255), width=S(6))
        self.glow(seam, (255, 236, 190), 18, 1.6); self.paste(seam)
        self.seam = (seam_top, seam_bot)

    def sun(self, cx, cy, r):
        w, h = self.im.size
        self.paste(radial(w, h, S(cx), S(cy), S(r * 3.2), (255, 250, 200), 0.85))
        L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for k in range(12):
            a = k * math.pi / 6
            x0, y0 = S(cx + math.cos(a) * r * 1.25), S(cy + math.sin(a) * r * 1.25)
            x1, y1 = S(cx + math.cos(a) * r * 1.7), S(cy + math.sin(a) * r * 1.7)
            d.line([(x0, y0), (x1, y1)], fill=(255, 196, 40, 255), width=S(16))
        d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=(255, 214, 64, 255))
        d.ellipse([S(cx - r * 0.72), S(cy - r * 0.8), S(cx + r * 0.5), S(cy + r * 0.3)], fill=(255, 236, 140, 255))
        self.paste(L)

    def moon(self, cx, cy, r):
        w, h = self.im.size
        self.paste(radial(w, h, S(cx), S(cy), S(r * 3.4), (190, 180, 255), 0.7))
        L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=(240, 236, 255, 255))
        cut = Image.new("L", (w, h), 0)
        ImageDraw.Draw(cut).ellipse([S(cx - r * 0.4), S(cy - r * 1.1), S(cx + r * 1.3), S(cy + r * 0.6)], fill=255)
        L.putalpha(ImageChops.subtract(L.split()[3], cut))
        self.paste(L)

    def skyline(self, base=1920, seed=5, day_col=(120, 150, 190), night_col=(14, 16, 44), lit=(255, 200, 90)):
        w, h = self.im.size
        rr = random.Random(seed)
        day = Image.new("RGBA", (w, h), (0, 0, 0, 0)); night = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        dd, dn = ImageDraw.Draw(day), ImageDraw.Draw(night)
        x = -20
        while x < W + 20:
            bw = 70 + rr.random() * 110; bh = 180 + rr.random() * 330
            box = [S(x), S(base - bh), S(x + bw), S(base)]
            dd.rectangle(box, fill=day_col + (255,)); dn.rectangle(box, fill=night_col + (255,))
            for wy in range(int(base - bh + 22), int(base - 18), 34):
                for wx in range(int(x + 12), int(x + bw - 16), 24):
                    if rr.random() < 0.5:
                        dn.rectangle([S(wx), S(wy), S(wx + 11), S(wy + 15)], fill=lit + (230,))
                        dd.rectangle([S(wx), S(wy), S(wx + 11), S(wy + 15)], fill=(200, 225, 245, 200))
            x += bw + 8
        mask = Image.new("L", (w, h), 0)
        st, sb = getattr(self, "seam", (640, 420))
        ImageDraw.Draw(mask).polygon([(S(st), 0), (w, 0), (w, h), (S(sb), h)], fill=255)
        both = Image.composite(night, day, mask)
        self.paste(both)

    def bottom_fade(self, y0=1450, col=(5, 6, 14), alpha=0.92):
        w, h = self.im.size
        a = np.zeros((h, w), np.float32)
        ys = np.arange(h)
        prof = np.clip((ys - S(y0)) / (h - S(y0)), 0, 1) ** 1.3 * 255 * alpha
        a[:] = prof[:, None]
        L = Image.new("RGBA", (w, h), col + (0,)); L.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
        self.paste(L)

    # ------------------------------------------------------------ typography
    def title(self, s, cx, cy, size, fill_top, fill_bot, path=ANTON, rot=0.0, stroke=12, glow_col=None, glow=0,
              extrude=10, extrude_col=INK, track=0):
        """thumbnail text: gradient fill + thick ink stroke + 3D extrude + soft glow. (cx, cy) = center."""
        f = font(path, size)
        bbox = f.getbbox(s, stroke_width=S(stroke))
        tw_, th_ = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = S(stroke + extrude + 40)
        cw, ch = tw_ + 2 * pad, th_ + 2 * pad
        ox, oy = pad - bbox[0], pad - bbox[1]
        # fill mask
        m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).text((ox, oy), s, font=f, fill=255)
        ms = Image.new("L", (cw, ch), 0); ImageDraw.Draw(ms).text((ox, oy), s, font=f, fill=255, stroke_width=S(stroke), stroke_fill=255)
        L = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        # extrude (stacked stroke silhouettes down-right)
        for k in range(S(extrude), 0, -2):
            e = Image.new("RGBA", (cw, ch), extrude_col + (255,)); e.putalpha(ms)
            L.alpha_composite(e, (k // 2, k))
        st = Image.new("RGBA", (cw, ch), INK + (255,)); st.putalpha(ms); L.alpha_composite(st)
        gr = vgrad(cw, ch, fill_top, fill_bot).convert("RGBA"); gr.putalpha(m)
        # glossy highlight on the top half
        hl = Image.new("L", (cw, ch), 0); ImageDraw.Draw(hl).rectangle([0, 0, cw, oy + (bbox[3] - bbox[1]) * 0.42 + bbox[1]], fill=60)
        hl = ImageChops.multiply(hl, m)
        white = Image.new("RGBA", (cw, ch), (255, 255, 255, 0)); white.putalpha(hl)
        L.alpha_composite(gr); L.alpha_composite(white)
        if rot:
            L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
        full = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        full.alpha_composite(L, (S(cx) - L.width // 2, S(cy) - L.height // 2))
        if glow_col:
            self.glow(full, glow_col, glow or 30, 1.2)
        self.shadow(full, 8, 16, 14, 0.6)
        self.paste(full)
        return full

    def text(self, s, x, y, size, col, path=INTER_BLACK, anchor="mm", stroke=0, stroke_col=INK):
        d = ImageDraw.Draw(self.im)
        d.text((S(x), S(y)), s, font=font(path, size), fill=col, anchor=anchor, stroke_width=S(stroke), stroke_fill=stroke_col)

    # ------------------------------------------------------------ props
    def badge(self, s, cx, cy, r, col=(255, 64, 96), fg=(255, 255, 255), rot=-8):
        w, h = self.im.size
        L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([S(cx - r - 8), S(cy - r - 8), S(cx + r + 8), S(cy + r + 8)], fill=INK + (255,))
        d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=col + (255,))
        d.text((S(cx), S(cy + 4)), s, font=font(ANTON, r * 1.05), fill=fg, anchor="mm", stroke_width=S(5), stroke_fill=INK)
        L = L.rotate(rot, center=(S(cx), S(cy)), resample=Image.BICUBIC)
        self.shadow(L, 6, 10, 8, 0.5); self.paste(L)

    def stamp(self, s, cx, cy, size, col=(225, 40, 60), rot=-7, sub=None):
        f = font(ANTON, size)
        bb = f.getbbox(s); tw_, th_ = bb[2] - bb[0], bb[3] - bb[1]
        padx, pady = S(34), S(22)
        cw, ch = tw_ + 2 * padx, th_ + 2 * pady + (S(size * 0.42) if sub else 0)
        L = Image.new("RGBA", (cw + S(40), ch + S(40)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        o = S(20)
        d.rounded_rectangle([o, o, o + cw, o + ch], S(14), fill=(250, 244, 228, 235), outline=col + (255,), width=S(9))
        d.rounded_rectangle([o + S(14), o + S(14), o + cw - S(14), o + ch - S(14)], S(8), outline=col + (255,), width=S(3))
        d.text((o + padx - bb[0], o + pady - bb[1]), s, font=f, fill=col + (255,))
        if sub:
            d.text((o + cw // 2, o + ch - S(size * 0.3)), sub, font=font(MONO, size * 0.3), fill=INK + (255,), anchor="mm")
        # distress: knock out random specks
        rr = random.Random(7); a = L.split()[3]; ad = ImageDraw.Draw(a)
        for _ in range(70):
            x, y = rr.random() * L.width, rr.random() * L.height; r_ = rr.random() * S(1.8)
            ad.ellipse([x - r_, y - r_, x + r_, y + r_], fill=0)
        L.putalpha(a)
        L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
        full = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        full.alpha_composite(L, (S(cx) - L.width // 2, S(cy) - L.height // 2))
        self.shadow(full, 5, 8, 6, 0.45); self.paste(full)

    def redacted(self, label, cx, cy, w=760, h=118, rot=-3):
        """'WINNER: $??,???' as a black redaction tape with caution stripes"""
        L = Image.new("RGBA", (S(w + 60), S(h + 60)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        o = S(30)
        d.rectangle([o, o, o + S(w), o + S(h)], fill=(12, 12, 14, 255))
        sw = S(24)
        stripes = Image.new("RGBA", L.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(stripes)
        for x0 in range(-S(h), S(w) + S(h), sw * 2):     # caution stripes, then keep only both ends
            ds.polygon([(o + x0, o), (o + x0 + sw, o), (o + x0 + sw - S(h), o + S(h)), (o + x0 - S(h), o + S(h))], fill=(255, 196, 0, 255))
        keep = Image.new("L", L.size, 0); dk = ImageDraw.Draw(keep)
        dk.rectangle([o, o, o + S(64), o + S(h)], fill=255); dk.rectangle([o + S(w - 64), o, o + S(w), o + S(h)], fill=255)
        stripes.putalpha(ImageChops.multiply(stripes.split()[3], keep)); L.alpha_composite(stripes)
        d.text((o + S(96), o + S(h / 2)), label, font=font(INTER_BLACK, 40), fill=(255, 255, 255, 255), anchor="lm")
        d.text((o + S(w - 92), o + S(h / 2) + S(2)), "$??,???", font=font(MONO, 62), fill=(120, 126, 134, 255), anchor="rm")
        L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
        full = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        full.alpha_composite(L, (S(cx) - L.width // 2, S(cy) - L.height // 2))
        self.shadow(full, 8, 14, 12, 0.6); self.paste(full)

    def sprite(self, rgba, cx, top, rim=(255, 255, 255), rim_w=7, spot=None):
        """paste a pre-rendered sprite (PIL RGBA at final 2x size) with white rim + soft rim glow + ground shadow"""
        w, h = self.im.size
        full = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        x = S(cx) - rgba.width // 2; y = S(top)
        full.alpha_composite(rgba, (x, y))
        if spot:
            self.paste(radial(w, h, S(cx), S(top) + rgba.height // 2, rgba.width * 0.95, spot, 0.75))
        a = full.split()[3]
        dil = a.filter(ImageFilter.MaxFilter(S(rim_w) * 2 + 1))
        rimL = Image.new("RGBA", (w, h), rim + (0,)); rimL.putalpha(dil)
        self.glow(rimL, rim, 16, 0.9)
        # ground shadow
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([S(cx) - rgba.width * 0.38, y + rgba.height - S(18), S(cx) + rgba.width * 0.38, y + rgba.height + S(26)], fill=(0, 0, 0, 150))
        self.paste(sh.filter(ImageFilter.GaussianBlur(S(8))))
        self.paste(rimL); self.paste(full)

    def finish(self, grain=0.012, vignette=0.32):
        w, h = self.im.size
        if vignette:
            yy, xx = np.mgrid[0:h, 0:w]
            d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 1.41
            a = (np.clip((d - 0.45) / 0.55, 0, 1) ** 1.6 * 255 * vignette).astype(np.uint8)
            v = Image.new("RGBA", (w, h), (0, 0, 0, 0)); v.putalpha(Image.fromarray(a, "L")); self.paste(v)
        out = self.im.convert("RGB").resize((W, H), Image.LANCZOS)
        if grain:   # fine, soft film grain (not the blocky paper texture)
            n = np.random.default_rng(1).normal(0, 255 * grain, (H, W, 1)).astype(np.float32)
            out = Image.fromarray(np.clip(np.asarray(out, np.float32) + n, 0, 255).astype(np.uint8))
        return out

    def save(self, path):
        self.finish().save(path, optimize=True)


def rocco_sprite(px, expr="shock", costume="detective", prop=None, t=0.4):
    """render Rocco with cairo onto a transparent surface at 2x and return PIL RGBA"""
    import cairo
    from rocco import draw_rocco, ROWS, COLS
    pxs = px * SS
    pad = pxs * 8
    w, h = int(COLS * pxs + pad * 2), int(ROWS * pxs + pad * 2)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); ctx = cairo.Context(surf)
    ctx.translate(pad, pad)
    draw_rocco(ctx, 0, 0, pxs, expr, costume)
    if prop:
        prop(ctx, pxs * 16.5, pxs * 13.5, pxs, t)
    surf.flush()
    arr = np.ndarray((h, w, 4), np.uint8, surf.get_data(), strides=(surf.get_stride(), 4, 1)).copy()
    rgba = arr[..., [2, 1, 0, 3]].astype(np.float32)
    al = rgba[..., 3:4] / 255.0
    rgba[..., :3] = np.where(al > 0, rgba[..., :3] / np.maximum(al, 1e-6), 0)   # un-premultiply
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA")
    return im.crop(im.getbbox())
