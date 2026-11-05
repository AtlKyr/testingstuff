import sys, json, math, subprocess, random
import numpy as np
import pandas as pd
import cairo
from rocco import draw_rocco, ROWS as RROWS, COLS as RCOLS


W, H, FPS = 1080, 1920, 30

WORDS = json.load(open("words_r2.json"))["words"]
END = WORDS[-1]["end"]
TOTAL = END + 1.4


HEAD, MONO, INTER = "Anton", "JetBrains Mono", "Inter"
TAGF = "Inter Black"          # labels/tags (heavy, clean)
NOBOLD = ("Anton", "Inter Black")   # single-weight faces: never ask cairo for a synthetic bold
C = dict(
    ink=(0x14, 0x18, 0x1C), cream=(0xF4, 0xEC, 0xD8), paper=(0xEE, 0xE4, 0xCC), green=(0x22, 0xE5, 0x8B),
    red=(0xFF, 0x4D, 0x6A), blue=(0x3D, 0x7D, 0xD8), yellow=(0xF2, 0xB1, 0x34), grey=(0x8A, 0x94, 0x9B),
    white=(0xF7, 0xF4, 0xEC), dark=(0x1B, 0x22, 0x27), purple=(0x8E, 0x5C, 0xD8), orange=(0xE8, 0x87, 0x3A),
)
FLAGCOLS = [C["red"], C["green"], C["blue"], C["yellow"]]



import rocco as _rocco
_rocco.COSTUME["crown"] = [(-4, 4, "y..y..y..y"), (-3, 4, "yy.yyyy.yy"), (-2, 4, "yyyyyyyyyy"),
                           (-1, 4, "yRyyEEyyRy"), (0, 4, "YYYYYYYYYY")]
_rocco.COSTUME["doctor"] = [(2, 3, "KKKKKKKKKKKKK"), (1, 7, "KSSSSK"), (0, 7, "KwwwSK"), (-1, 8, "KKKK"),
                            (12, 3, "wwwwwwwwwwww"), (13, 2, "wwwwDwwwwDwwww"), (14, 2, "ww"), (14, 5, "wwwSSwSwww"),
                            (14, 14, "ww"), (15, 6, "wwSwwS"), (16, 6, "wwwSSw")]

def wt(word, nth=1):
    k = 0
    for w in WORDS:
        if w["text"].strip(".,?:…—") == word:
            k += 1
            if k == nth:
                return w["start"]
    raise KeyError(word)

#@@DATA@@

def scene_at(t):
    cur = SCENES[0]
    for s in SCENES:
        if t >= s[0]:
            cur = s
    nxt = [s for s, _ in SCENES if s > cur[0]]
    return cur[1], cur[0], (nxt[0] if nxt else TOTAL)

# ---------------------------------------------------------------- helpers
def rgba(col, a=1.0):
    return (col[0] / 255, col[1] / 255, col[2] / 255, a)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


def back(x):
    x = clamp(x); c1 = 1.9; return max(0.0, 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2)


def prog(t, s, d):
    return clamp((t - s) / d)


def font(ctx, f=HEAD, bold=True, size=40):
    ctx.select_font_face(f, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if (bold and f not in NOBOLD) else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def tw(ctx, s, size, f=HEAD, bold=True):
    font(ctx, f, bold, size); return ctx.text_extents(s).x_advance


def text(ctx, s, x, y, size, col, a=1.0, f=HEAD, bold=True, align="left", outline=0, ocol=None):
    font(ctx, f, bold, size)
    w = ctx.text_extents(s).x_advance
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    if outline:
        # v2 display text: soft drop shadow + 3D extrude + thick stroke + vertical gradient fill + gloss
        oc = ocol or C["ink"]
        ext = max(2, int(size * 0.045))
        ctx.new_path(); ctx.move_to(x + size * 0.03, y + size * 0.09); ctx.text_path(s)
        ctx.set_source_rgba(0, 0, 0, 0.35 * a); ctx.set_line_width(outline * 1.6); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve(); ctx.fill()
        for k in range(ext, 0, -2):
            ctx.new_path(); ctx.move_to(x + k * 0.35, y + k); ctx.text_path(s)
            ctx.set_source_rgba(*rgba(oc, a)); ctx.set_line_width(outline); ctx.stroke_preserve(); ctx.fill()
        ctx.new_path(); ctx.move_to(x, y); ctx.text_path(s)
        ctx.set_source_rgba(*rgba(oc, a)); ctx.set_line_width(outline); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()
        top = tuple(min(255, int(v + (255 - v) * 0.45)) for v in col); bot = tuple(int(v * 0.86) for v in col)
        g = cairo.LinearGradient(0, y - size * 0.78, 0, y + size * 0.05)
        g.add_color_stop_rgba(0, *rgba(top, a)[:3], a); g.add_color_stop_rgba(0.55, *rgba(col, a)[:3], a)
        g.add_color_stop_rgba(1, *rgba(bot, a)[:3], a)
        ctx.new_path(); ctx.move_to(x, y); ctx.text_path(s); ctx.set_source(g); ctx.fill()
        ctx.save(); ctx.new_path(); ctx.rectangle(x - 10, y - size * 0.8, w + 20, size * 0.36); ctx.clip()
        ctx.new_path(); ctx.move_to(x, y); ctx.text_path(s); ctx.set_source_rgba(1, 1, 1, 0.16 * a); ctx.fill()
        ctx.restore(); ctx.new_path()
        return w
    if size >= 40 and f in (HEAD, TAGF):    # big plain headings get a crisp hard shadow so they never sit flat
        ctx.new_path(); ctx.move_to(x + size * 0.025, y + size * 0.05)
        ctx.set_source_rgba(0, 0, 0, 0.28 * a); ctx.show_text(s)
    ctx.new_path(); ctx.move_to(x, y)
    ctx.set_source_rgba(*rgba(col, a)); ctx.show_text(s)
    ctx.new_path()
    return w


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def card(ctx, x, y, w, h, fill, a=1.0, r=14, shadow=True, border=None):
    """v2: soft layered shadow, vertical gradient (lit from above), inner top highlight, bevel line at the bottom"""
    if w <= 0 or h <= 0:
        return
    if shadow:
        for k, al in ((16, 0.10), (11, 0.14), (7, 0.22)):
            rrect(ctx, x + k * 0.5, y + k, w, h, r); ctx.set_source_rgba(0, 0, 0, al * a); ctx.fill()
    top = tuple(min(255, int(v + (255 - v) * 0.16)) for v in fill); bot = tuple(int(v * 0.82) for v in fill)
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgba(0, *rgba(top)[:3], a); g.add_color_stop_rgba(1, *rgba(bot)[:3], a)
    rrect(ctx, x, y, w, h, r); ctx.set_source(g); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(border or C["ink"], a * 0.9)); ctx.set_line_width(4); ctx.stroke()
    if h > 24 and w > 24:
        ctx.save(); rrect(ctx, x + 2, y + 2, w - 4, h - 4, max(1, r - 2)); ctx.clip()
        ctx.new_path(); ctx.move_to(x + r, y + 5); ctx.line_to(x + w - r, y + 5)
        ctx.set_source_rgba(1, 1, 1, 0.30 * a); ctx.set_line_width(3); ctx.stroke()
        ctx.new_path(); ctx.move_to(x + r, y + h - 5); ctx.line_to(x + w - r, y + h - 5)
        ctx.set_source_rgba(0, 0, 0, 0.22 * a); ctx.set_line_width(4); ctx.stroke()
        ctx.restore()


def rect(ctx, x, y, w, h, col, a=1.0):
    ctx.new_path(); ctx.rectangle(x, y, w, h); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def check(ctx, x, y, s, col, a=1.0, width=8):
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + s * 0.35, y + s * 0.35); ctx.line_to(x + s, y - s * 0.45)
    ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(width); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()


def money(v):
    return "${:,.0f}".format(v)


# paper grain (precomputed)
rng = np.random.default_rng(7)
_g = (rng.random((H // 2, W // 2)) * 255).astype(np.uint8)
grain = np.zeros((H // 2, W // 2, 4), dtype=np.uint8)
grain[..., 0] = _g; grain[..., 1] = _g; grain[..., 2] = _g; grain[..., 3] = 255
GRAIN = cairo.ImageSurface.create_for_data(memoryview(grain), cairo.FORMAT_RGB24, W // 2, H // 2)


def paper_grain(ctx, a=0.07):
    ctx.save(); ctx.scale(2, 2); ctx.set_source_surface(GRAIN, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_NEAREST)
    ctx.paint_with_alpha(a); ctx.restore()


def bg_fill(ctx, top, bot):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *[v / 255 for v in top]); g.add_color_stop_rgb(1, *[v / 255 for v in bot])
    ctx.set_source(g); ctx.paint()


# ---------------------------------------------------------------- UI: bunting, captions, counters
def bunting(ctx, title, t, t_in, colors=None):
    a = ease(prog(t, t_in, 0.35))
    colors = colors or FLAGCOLS
    y0, sag = 150, 50
    ctx.set_source_rgba(*rgba(C["ink"], 0.9)); ctx.set_line_width(4); ctx.new_path()
    ctx.move_to(-10, y0); ctx.curve_to(300, y0 + sag * 1.4, 780, y0 + sag * 1.4, W + 10, y0); ctx.stroke()
    n = 9
    for i in range(n):
        u = (i + 0.5) / n
        x = u * W
        y = y0 + sag * 4 * u * (1 - u) * 1.05
        sway = math.sin(t * 2.2 + i * 0.9) * 0.06
        drop = (1 - back(prog(t, t_in + i * 0.03, 0.45))) * -160
        ctx.save(); ctx.translate(x, y + drop); ctx.rotate(sway)
        ctx.new_path(); ctx.move_to(-58, 0); ctx.line_to(58, 0); ctx.line_to(0, 125); ctx.close_path()
        ctx.set_source_rgba(0, 0, 0, 0.3); ctx.save(); ctx.translate(5, 6); ctx.fill_preserve(); ctx.restore()
        ctx.new_path(); ctx.move_to(-58, 0); ctx.line_to(58, 0); ctx.line_to(0, 125); ctx.close_path()
        ctx.set_source_rgba(*rgba(colors[i % len(colors)])); ctx.fill()
        ctx.restore()
    # title
    words = title.split(" ")
    size = 86
    while tw(ctx, title, size) > W - 120:
        size -= 4
    total = tw(ctx, title, size)
    x = W / 2 - total / 2
    sp = tw(ctx, " ", size)
    for k, wd in enumerate(words):
        p = back(prog(t, t_in + 0.08 + k * 0.07, 0.4))
        wwd = tw(ctx, wd, size)
        if p <= 0.01:
            x += wwd + sp
            continue
        ctx.save(); ctx.translate(x + wwd / 2, 255); ctx.scale(max(p, 1e-3), max(p, 1e-3)); ctx.rotate(math.sin(t * 3 + k) * 0.02)
        text(ctx, wd, 0, 0, size, C["white"], a, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
        x += wwd + sp


def build_chunks():
    toks = [w for w in WORDS if w["text"] not in ("—",)]
    sents, cur = [], []
    for w in toks:
        cur.append(w)
        if w["text"][-1] in ".?:…,":
            sents.append(cur); cur = []
    if cur:
        sents.append(cur)
    chunks = []
    for sn in sents:
        n = math.ceil(len(sn) / 3)
        size = math.ceil(len(sn) / n)
        for i in range(0, len(sn), size):
            chunks.append(sn[i:i + size])
    out = []
    for k, ch in enumerate(chunks):
        t0 = ch[0]["start"] - 0.04
        t1 = chunks[k + 1][0]["start"] - 0.04 if k + 1 < len(chunks) else ch[-1]["end"] + 0.5
        out.append((t0, t1, ch))
    return out


CHUNKS = build_chunks()


def captions(ctx, t, y=1240):
    """v2 captions: Anton caps, thick ink stroke + extrude + shadow; the word being spoken turns yellow and pops bigger"""
    for a0, a1, ch in CHUNKS:
        if not (a0 <= t < a1):
            continue
        size = 74
        words = [w["text"].strip("—").upper() for w in ch]
        gap = size * 0.34
        ws = [tw(ctx, w, size, HEAD) * 1.14 for w in words]     # reserve room for the active-word pop (x1.14)
        total = sum(ws) + gap * (len(ws) - 1)
        if total > W - 90:
            k_ = (W - 90) / total; size *= k_; gap *= k_
            ws = [tw(ctx, w, size, HEAD) * 1.14 for w in words]
            total = sum(ws) + gap * (len(ws) - 1)
        x = W / 2 - total / 2
        for k, (wd, w_, wo) in enumerate(zip(words, ws, ch)):
            p = back(prog(t, wo["start"] - 0.05, 0.2))
            if p <= 0:
                x += w_ + gap
                continue
            active = wo["start"] - 0.05 <= t < wo["end"] + 0.08
            sc = p * (1.14 if active else 1.0)
            col = C["yellow"] if active else C["white"]
            ctx.save(); ctx.translate(x + w_ / 2, y + size * 0.36); ctx.rotate(-0.02 if k % 2 == 0 else 0.015); ctx.scale(max(sc, 1e-3), max(sc, 1e-3))
            text(ctx, wd, 0, 0, size, col, 1, HEAD, False, "center", outline=max(8, int(size * 0.17)), ocol=C["ink"])
            ctx.restore()
            x += w_ + gap
        return


def flip_counter(ctx, x, y, w, h, label, value, col=None, a=1.0, size=None):
    card(ctx, x, y, w, h, C["dark"], a, 16)
    rect(ctx, x + 6, y + h / 2 + 18, w - 12, 3, (0, 0, 0), 0.6 * a)
    text(ctx, label, x + w / 2, y + 40, 26, C["grey"], a, MONO, True, "center")
    size = size or h * 0.48
    while tw(ctx, value, size, MONO) > w - 30:
        size -= 2
    text(ctx, value, x + w / 2, y + h / 2 + 18 + size * 0.36, size, col or C["white"], a, MONO, True, "center", outline=max(5, int(size * 0.09)), ocol=(0x05, 0x07, 0x0A))


# ---------------------------------------------------------------- Rocco state
def mouth_open(t):
    for w in WORDS:
        if w["start"] <= t <= w["end"] and w["text"] != "—":
            return abs(math.sin((t - w["start"]) * 13)) > 0.35
    return False


def lerp(a, b, u):
    return a + (b - a) * u





#@@MOTION@@

def rocco(ctx, t, costume, expr_override=None, prop=None, **_):
    x, y, px, flip, moving, lift = motion(t)
    expr = "talk" if mouth_open(t) else "neutral"
    bt = (t + 0.4) % 3.1
    if bt < 0.1 and expr == "neutral":
        expr = "blink"
    if expr_override:
        expr = expr_override(expr) if callable(expr_override) else expr_override
    if moving:
        lift += abs(math.sin(t * 13)) * px * 1.2
    w_, h_ = RCOLS * px, RROWS * px
    # squash & stretch near the ground
    sq = 1.0
    if moving or lift > 0:
        g = clamp(lift / 40)
        sq = 0.9 + 0.1 * g if g < 1 else 1.04
    breathe = math.sin(t * 3) * 3
    tilt = math.sin(t * 13) * 0.05 if moving else 0
    # shadow on the ground
    sh = clamp(1 - lift / 400)
    ctx.new_path(); ctx.save(); ctx.translate(x + w_ * 0.42, y + h_ + 6); ctx.scale(1, 0.18)
    ctx.arc(0, 0, px * 8 * sh, 0, 2 * math.pi); ctx.restore(); ctx.set_source_rgba(0, 0, 0, 0.3 * sh); ctx.fill()
    ctx.save()
    ctx.translate(x + w_ * 0.42, y + h_ - lift + breathe)   # feet anchor
    ctx.rotate(tilt)
    ctx.scale((2 - sq) * (-1 if flip else 1), sq)
    ctx.translate(-w_ * 0.42, -h_)
    draw_rocco(ctx, 0, 0, px, expr, costume)
    if prop:
        prop(ctx, px * 16.5, px * 13.5, px, t)
    ctx.restore()


# props (drawn at Rocco's right paw, local coords)
def prop_pointer(target):
    def f(ctx, x, y, px, t):
        ctx.new_path(); ctx.move_to(x, y); ctx.line_to(*target)
        ctx.set_source_rgba(*rgba((0x8B, 0x5A, 0x2B))); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        rect(ctx, x - px * 0.6, y - px * 0.6, px * 1.2, px * 1.2, C["ink"])
    return f


def prop_flag(ctx, x, y, px, t):
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + 30, y - 260)
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(10); ctx.stroke()
    wave = math.sin(t * 10)
    for i in range(6):
        for j in range(4):
            col = C["ink"] if (i + j) % 2 == 0 else C["white"]
            xx = x + 34 + i * 28
            yy = y - 260 + j * 28 + math.sin(t * 10 + i * 0.8) * 8
            rect(ctx, xx, yy, 29, 29, col)


def prop_magnifier(ctx, x, y, px, t):
    cx, cy = x + 90, y - 120 + math.sin(t * 2) * 10
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx - 40, cy + 40)
    ctx.set_source_rgba(*rgba((0x6B, 0x4A, 0x2E))); ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, 58, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.35); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(12); ctx.stroke()
    ctx.new_path(); ctx.arc(cx - 18, cy - 18, 14, math.pi, 1.5 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(6); ctx.stroke()


def prop_coin(ctx, x, y, px, t):
    ph = t * 9
    yy = y - 160 - abs(math.sin(t * 3.2)) * 160
    sx = abs(math.cos(ph))
    ctx.save(); ctx.translate(x + 40, yy); ctx.scale(max(0.08, sx), 1)
    ctx.new_path(); ctx.arc(0, 0, 54, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["yellow"])); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba((0xC9, 0x8A, 0x1C))); ctx.set_line_width(8); ctx.stroke()
    if sx > 0.4:
        text(ctx, "E" if math.cos(ph) > 0 else "L", 0, 18, 52, (0x8A, 0x5A, 0x10), 1, HEAD, True, "center")
    ctx.restore()


# ---------------------------------------------------------------- charts
def poly(ctx, xs, ys, col, width, a=1.0, glow=False):
    if len(xs) < 2:
        return
    for wd, aa in (((width * 3.5, 0.18 * a),) if glow else ()) + ((width, a),):
        ctx.new_path(); ctx.move_to(xs[0], ys[0])
        for x, y in zip(xs[1:], ys[1:]):
            ctx.line_to(x, y)
        ctx.set_source_rgba(*rgba(col, aa)); ctx.set_line_width(wd); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def series_xy(arr, i0, i1, upto, box, vmin, vmax, step=4):
    idx = list(range(i0, max(i0 + 1, upto), step)) + [max(i0 + 1, upto)]
    xs = [box[0] + (i - i0) / (i1 - i0) * box[2] for i in idx]
    ys = [box[1] + box[3] - (arr[i] - vmin) / (vmax - vmin) * box[3] for i in idx]
    return xs, ys




def prop_umbrella(ctx, x, y, px, t):
    cx, cy = x - px * 8, y - px * 18 + math.sin(t * 3) * 4
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(cx, cy)
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    R = px * 9
    for k in range(6):
        a0 = math.pi + k * math.pi / 6; a1 = a0 + math.pi / 6
        ctx.new_path(); ctx.move_to(cx, cy); ctx.arc(cx, cy, R, a0, a1); ctx.close_path()
        ctx.set_source_rgba(*rgba(C["red"] if k % 2 == 0 else C["white"])); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy - 4, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()


SNAIL = [
    "..........K.K.",
    "...KKKK....K.K",
    "..KyyyyK...KK.",
    ".KyKKKyyK.KggK",
    ".KyKyKKyK.KggK",
    ".KyKyyKyKKggK.",
    "..KyyyyyKgggK.",
    "KKKKKKKKgggggK",
    "KggggggggggggK",
    "KKKKKKKKKKKKKK",
]
SNAIL_COL = {"K": C["ink"], "y": C["orange"], "g": (0x9F, 0xD8, 0xA0)}


def snail(ctx, x, y, px, t):
    bob = int(t * 4) % 2
    for j, row in enumerate(SNAIL):
        for i, ch in enumerate(row):
            if ch in SNAIL_COL:
                rect(ctx, x + i * px, y + j * px - (bob * px * 0.3 if j < 7 else 0), px + 0.6, px + 0.6, SNAIL_COL[ch])


def heart_line(ctx, x0, y0, w, h, t, col, speed=260):
    """scrolling ECG trace"""
    pts = []
    period = 360
    off = (t * speed) % period
    for k in range(0, int(w) + 1, 4):
        u = ((k + off) % period) / period
        if 0.30 < u < 0.34:
            v = -0.25 * math.sin((u - 0.30) / 0.04 * math.pi)
        elif 0.40 < u < 0.43:
            v = 0.25
        elif 0.43 < u < 0.47:
            v = -1.0 + (u - 0.43) / 0.04 * 0.2
        elif 0.47 < u < 0.51:
            v = 0.45
        elif 0.60 < u < 0.70:
            v = -0.3 * math.sin((u - 0.60) / 0.10 * math.pi)
        else:
            v = 0
        pts.append((x0 + k, y0 + v * h))
    poly(ctx, [p[0] for p in pts], [p[1] for p in pts], col, 7, 1, glow=True)


def god_rays(ctx, cx, cy, t, a, col, n=14, r=1300):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 0.25)
    for k in range(n):
        ctx.new_path(); ctx.move_to(0, 0); ctx.arc(0, 0, r, k * 2 * math.pi / n, k * 2 * math.pi / n + math.pi / n); ctx.close_path()
        ctx.set_source_rgba(*rgba(col, a)); ctx.fill()
    ctx.restore()


def skyline(ctx, base, t, seed=3, col=(0x1E, 0x24, 0x3A), lit=True):
    rr = random.Random(seed)
    x = -20
    while x < W + 20:
        bw = 70 + rr.random() * 90; bh = 160 + rr.random() * 380
        rect(ctx, x, base - bh, bw, bh, col)
        if lit:
            for wy in range(int(base - bh + 20), int(base - 20), 34):
                for wx in range(int(x + 12), int(x + bw - 16), 26):
                    on = rr.random() < 0.45 or (int(t * 1.5 + wx * 0.01 + wy * 0.02) % 9 == 0)
                    if on:
                        rect(ctx, wx, wy, 12, 16, C["yellow"], 0.75)
        x += bw + 8


def ticker_band(ctx, y, t, text_s, col_bg, col_fg, speed=220):
    rect(ctx, 0, y, W, 64, col_bg)
    rect(ctx, 0, y, W, 4, C["ink"]); rect(ctx, 0, y + 60, W, 4, C["ink"])
    unit = tw(ctx, text_s, 32, MONO)
    off = (t * speed) % unit
    x = -off
    while x < W:
        text(ctx, text_s, x, y + 44, 32, col_fg, 1, MONO, True)
        x += unit


def tag(ctx, x, y, label, col, p, size=34, rot=-0.05, fg=None):
    if p <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    w_ = tw(ctx, label, size, TAGF) + 44
    card(ctx, -w_ / 2, -size * 0.95, w_, size * 1.75, col, 1, 12)
    text(ctx, label, 0, size * 0.34, size, fg or C["ink"], 1, TAGF, False, "center")
    ctx.restore()


def price_chart(ctx, box, i0, i1, upto, vmin, vmax, a=1.0, sma=True, price_col=None, sma_upto=None):
    xs, ys = series_xy(CLOSE, i0, i1, upto, box, vmin, vmax, 1)
    poly(ctx, xs, ys, price_col or (0x5A, 0x64, 0x6B), 4, a)
    if sma:
        su = upto if sma_upto is None else sma_upto
        for arr, col, wd in ((S200, (0x3D, 0x7D, 0xD8), 6), (S50, (0xE0, 0x9A, 0x10), 6)):
            xs, ys = series_xy(arr, i0, i1, su, box, vmin, vmax, 1)
            poly(ctx, xs, ys, col, wd, a, glow=True)


def xy_of(arr, i, i0, i1, box, vmin, vmax):
    return box[0] + (i - i0) / (i1 - i0) * box[2], box[1] + box[3] - (arr[i] - vmin) / (vmax - vmin) * box[3]




#@@SCENES@@

def wipe(ctx, t):
    for k, b in enumerate(BOUNDS):
        dt = t - b
        if -0.18 <= dt <= 0.18:
            u = (dt + 0.18) / 0.36
            x = -W * 1.3 + u * W * 2.6
            col = FLAGCOLS[k % 4]
            ctx.save(); ctx.translate(x, 0)
            ctx.new_path(); ctx.move_to(0, 0); ctx.line_to(W * 1.1, 0); ctx.line_to(W * 1.1 - 300, H); ctx.line_to(-300, H); ctx.close_path()
            ctx.set_source_rgba(*rgba(col)); ctx.fill()
            ctx.restore()





def bursts(ctx, t):
    for k, (t0, x, y, pal, sz) in enumerate(EVENTS):
        u = (t - t0) / 0.7
        if not (0 <= u < 1):
            continue
        rr = random.Random(k * 31 + 7)
        for i in range(18):
            ang = rr.random() * 2 * math.pi
            sp = (180 + rr.random() * 260) * sz
            d = sp * ease(u)
            px_ = x + math.cos(ang) * d
            py_ = y + math.sin(ang) * d + 200 * u * u
            r = (6 + rr.random() * 8) * sz * (1 - u)
            col = pal[i % len(pal)]
            ctx.save(); ctx.translate(px_, py_); ctx.rotate(ang + u * 6)
            rect(ctx, -r, -r / 2, r * 2, r, col, 1 - u * 0.6)
            ctx.restore()
        # ring
        ctx.new_path(); ctx.arc(x, y, 30 + 220 * ease(u) * sz, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba(pal[0], 0.5 * (1 - u))); ctx.set_line_width(8 * (1 - u) + 1); ctx.stroke()


def punch(t):
    z = 1.0
    for t0 in PUNCH:
        u = t - t0
        if 0 <= u < 0.45:
            z += 0.05 * math.exp(-u * 9) * (1 if u > 0.02 else u / 0.02)
    return z


def flash(ctx, t):
    for t0 in FLASH:
        u = t - t0
        if 0 <= u < 0.18:
            ctx.set_source_rgba(1, 1, 1, 0.45 * (1 - u / 0.18)); ctx.paint()


_vg = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
_vc = cairo.Context(_vg)
_g = cairo.RadialGradient(W / 2, H / 2, H * 0.32, W / 2, H / 2, H * 0.78)
_g.add_color_stop_rgba(0, 0, 0, 0, 0); _g.add_color_stop_rgba(1, 0, 0, 0, 0.42)
_vc.set_source(_g); _vc.paint()
VIGNETTE = _vg


def vignette(ctx):
    ctx.set_source_surface(VIGNETTE, 0, 0); ctx.paint()


def speed_lines(ctx, t):
    rr = random.Random(5)
    for k in range(16):
        y = 360 + rr.random() * 820
        ln = 120 + rr.random() * 260
        sp = 900 + rr.random() * 900
        x = W - ((t * sp + rr.random() * 3000) % (W + ln * 2))
        rect(ctx, x, y, ln, 4, C["white"], 0.55)



#@@EVENTS@@

def render(out, preview=0):
    nframes = int(TOTAL * FPS)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    proc = None
    if not preview:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
               "-i", "-", "-i", AUDIO, "-af", "apad", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-profile:v", "high", "-level", "4.2",
               "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
               "-movflags", "+faststart", out]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(nframes):
        if preview and f % preview:
            continue
        t = f / FPS
        name, s0, s1 = scene_at(t)
        ctx.save()
        # gentle push-in per scene
        z = (1 + 0.035 * prog(t, s0, max(0.5, s1 - s0))) * punch(t)
        ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2)
        SCENE_FN[name](ctx, t, s0, s1)
        bursts(ctx, t)
        ctx.restore()
        vignette(ctx)
        if t < T["follow"] - 0.2:
            captions(ctx, t)
        paper_grain(ctx, 0.06)
        flash(ctx, t)
        wipe(ctx, t)
        surf.flush()
        if preview:
            surf.write_to_png(f"preview/f{f:05d}.png")
        else:
            proc.stdin.write(bytes(surf.get_data()))
    if proc:
        proc.stdin.close(); proc.wait()


if __name__ == "__main__":
    pv = int(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else 0
    render(sys.argv[1], pv)
