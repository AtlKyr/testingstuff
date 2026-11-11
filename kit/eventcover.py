"""EVENT COVER / FRAME-0 style for Strategy Autopsy (user request 2026-11-11, LESSONS.md 21).

Look: white background, giant black Anton headline ending in "." or "?" ("IT FLIPPED.", "2007 AGAIN?"),
a real SPY chart with a red shaded area, a hand-drawn arrow + dotted circle on ONE real moment,
and the answer hidden ("?" or a black redaction block). Small Rocco at the bottom for the brand.

All drawing functions take a cairo context, so the SAME helpers work
  - inside the video engine for frame 0 (draw on the frame ctx), and
  - for the cover PNG via event_cover(...), rendered at 2x and downsampled (crisp text).

Honesty rules (LESSONS 21): the arrow must point at a real date in the backtest data, the headline must be literally true
about that moment, nothing after the hidden point may leak the result, no political symbols, no fake urgency.
"""
import math
import cairo
import numpy as np

INK = (0.05, 0.05, 0.06)
RED = (0.85, 0.12, 0.20)
RED_FILL = (0.94, 0.33, 0.36, 0.85)
W, H = 1080, 1920


def headline(ctx, s, x, y, size=300, maxw=980, col=INK, align="left"):
    """giant Anton headline; shrinks to fit maxw; returns the size used"""
    ctx.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    while ctx.text_extents(s).x_advance > maxw and size > 40:
        size -= 4
        ctx.set_font_size(size)
    w = ctx.text_extents(s).x_advance
    xx = x - w / 2 if align == "center" else x
    ctx.move_to(xx, y); ctx.set_source_rgb(*col); ctx.show_text(s)
    return size


def arrow_to(ctx, x0, y0, x1, y1, col=INK, width=7, bend=60):
    """hand-drawn curved arrow from (x0,y0) to (x1,y1); head follows the curve's real tangent (works from any side)"""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = max(1.0, math.hypot(dx, dy))
    cx, cy = mx - dy / L * bend, my + dx / L * bend          # control point pushed sideways = curve
    ctx.new_path(); ctx.move_to(x0, y0); ctx.curve_to(cx, cy, cx, cy, x1, y1)
    ctx.set_source_rgb(*col); ctx.set_line_width(width); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    ang = math.atan2(y1 - cy, x1 - cx)
    for s_ in (+1, -1):
        a_ = ang + math.pi - s_ * 0.5
        ctx.new_path(); ctx.move_to(x1, y1); ctx.line_to(x1 + 38 * math.cos(a_), y1 + 38 * math.sin(a_)); ctx.stroke()


def dotted_circle(ctx, x, y, r=48, col=INK, width=4):
    ctx.save(); ctx.set_dash([10, 9]); ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.set_source_rgb(*col); ctx.set_line_width(width); ctx.stroke(); ctx.restore()


class Plot:
    """maps index/value to pixels inside box=(x0, y0, x1, y1) for one or more series of equal length"""

    def __init__(self, box, n, lo, hi):
        self.x0, self.y0, self.x1, self.y1 = box
        self.n, self.lo, self.hi = n, lo, hi

    def X(self, i):
        return self.x0 + i / max(1, self.n - 1) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y1 - (v - self.lo) / (self.hi - self.lo) * (self.y1 - self.y0)

    def line(self, ctx, arr, i0=0, i1=None, col=INK, width=6):
        i1 = len(arr) - 1 if i1 is None else i1
        ctx.new_path()
        for i in range(i0, i1 + 1):
            (ctx.move_to if i == i0 else ctx.line_to)(self.X(i), self.Y(arr[i]))
        ctx.set_source_rgb(*col); ctx.set_line_width(width); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()

    def shade_between(self, ctx, a, b, i0, i1, rgba=RED_FILL):
        ctx.new_path(); ctx.move_to(self.X(i0), self.Y(a[i0]))
        for i in range(i0, i1 + 1):
            ctx.line_to(self.X(i), self.Y(a[i]))
        for i in range(i1, i0 - 1, -1):
            ctx.line_to(self.X(i), self.Y(b[i]))
        ctx.close_path(); ctx.set_source_rgba(*rgba); ctx.fill()

    def shade_under_level(self, ctx, arr, level, i0, i1, rgba=RED_FILL):
        """'underwater' area between a horizontal level (e.g. the old peak) and the price"""
        ctx.new_path(); ctx.move_to(self.X(i0), self.Y(level))
        for i in range(i0, i1 + 1):
            ctx.line_to(self.X(i), self.Y(min(arr[i], level)))
        ctx.line_to(self.X(i1), self.Y(level)); ctx.close_path(); ctx.set_source_rgba(*rgba); ctx.fill()

    def level(self, ctx, v, i0, col=RED, width=4):
        ctx.save(); ctx.set_dash([14, 10]); ctx.new_path(); ctx.move_to(self.X(i0), self.Y(v)); ctx.line_to(self.x1, self.Y(v))
        ctx.set_source_rgb(*col); ctx.set_line_width(width); ctx.stroke(); ctx.restore()


def redact_block(ctx, x, y, w, h, label="?"):
    ctx.set_source_rgb(*INK); ctx.rectangle(x, y, w, h); ctx.fill()
    headline(ctx, label, x + w / 2, y + h / 2 + min(w, h) * 0.32, size=min(w, h) * 0.9, maxw=w * 0.9, col=(1, 1, 1), align="center")


def question_mark(ctx, x, y, size=300, col=RED):
    headline(ctx, "?", x, y, size=size, maxw=size, col=col)


def draw_event(ctx, head, series, focus, cut=None, compare=None, shade="between", level=None,
               box=(40, 560, 1040, 1360), head_y=300, head_size=300, rocco=("shock", "detective", 22),
               arrow_from=None, redact=True, sub=None, shade_from=None, rocco_at=None):
    """Full event layout on a 1080x1920 ctx.
    series  : main array (e.g. SPY adj close or the strategy equity), already sliced to the window you want to show
    compare : optional second array of the same length (e.g. buy & hold) -> shade="between" fills the gap
    focus   : index of the ONE real moment the arrow points at
    cut     : last index drawn; everything after is hidden ("?" or a redaction block). Default = len-1.
    shade   : "between" (needs compare) or "underwater" (needs level, e.g. the old peak value)
    """
    n = len(series); cut = n - 1 if cut is None else cut
    vals = [np.asarray(series[: cut + 1])] + ([np.asarray(compare[: cut + 1])] if compare is not None else [])
    lo = min(v.min() for v in vals); hi = max(v.max() for v in vals)
    if level is not None:
        hi = max(hi, level)
    pad = (hi - lo) * 0.06
    x1 = box[2] - 200  # right strip is always reserved for the hidden answer ("?" or redaction)
    P = Plot((box[0], box[1], x1, box[3]), cut + 1, lo - pad, hi + pad)
    ctx.set_source_rgb(1, 1, 1); ctx.paint()
    headline(ctx, head, 50, head_y, head_size, maxw=980)
    if sub:
        ctx.select_font_face("Anton"); ctx.set_font_size(54); ctx.set_source_rgb(*RED)
        ctx.move_to(54, head_y + 80); ctx.show_text(sub)
    if shade == "between" and compare is not None:
        P.shade_between(ctx, series, compare, 0 if shade_from is None else shade_from, cut)
    elif shade == "underwater" and level is not None:
        P.shade_under_level(ctx, series, level, focus if shade_from is None else shade_from, cut)
        P.level(ctx, level, focus)
    if compare is not None:
        P.line(ctx, compare, 0, cut, INK, 7)
        P.line(ctx, series, 0, cut, RED, 7)
    else:
        P.line(ctx, series, 0, cut, INK, 6)
    fx, fy = P.X(focus), P.Y(series[focus])
    dotted_circle(ctx, fx, fy, 50)
    # arrow comes from OUTSIDE the chart on the side the focus is nearer to (top or bottom) so it never crosses the lines
    from_below = fy > (box[1] + box[3]) / 2
    if arrow_from is None:
        ax = fx - 260 if fx > 330 else fx + 220
        arrow_from = (ax, box[3] + 60) if from_below else (ax, box[1] - 40)
    tip = (fx - 6, fy + 58) if from_below else (fx - 6, fy - 58)
    left = arrow_from[0] < fx
    arrow_to(ctx, arrow_from[0], arrow_from[1], tip[0], tip[1], bend=(-70 if left else 70) * (-1 if from_below else 1))
    if redact:
        redact_block(ctx, box[2] - 180, box[1] + 120, 160, box[3] - box[1] - 120)
    else:
        question_mark(ctx, x1 + 40, (box[1] + box[3]) / 2 + 110, size=280)
    if rocco:
        try:
            from rocco import draw_rocco
            rx = 60 if (from_below and fx > 540) else 600   # keep Rocco out of the arrow's way
            rx, ry = rocco_at if rocco_at else (rx, box[3] + 80)
            draw_rocco(ctx, rx, ry, rocco[2], rocco[0], rocco[1])
        except Exception:
            pass
    return P


def frame0_event(ctx, *args, **kw):
    """same layout for VIDEO FRAME 0, inside the Shorts safe zone: the right action column (x > ~960) and the bottom
    caption/title area (y > ~1500) are covered by the YouTube UI in the feed, so the chart, the redaction and Rocco stay clear."""
    kw.setdefault("box", (40, 540, 960, 1240))
    kw.setdefault("rocco", ("shock", "detective", 15))
    kw.setdefault("rocco_at", (70, 1250))   # left + above the caption zone
    P = draw_event(ctx, *args, **kw)
    return P


def event_cover(path, *args, **kw):
    """render draw_event at 2x and downsample -> crisp 1080x1920 PNG"""
    from PIL import Image
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); ctx = cairo.Context(surf)
    ctx.scale(2, 2)
    draw_event(ctx, *args, **kw)
    surf.flush()
    arr = np.ndarray((H * 2, W * 2, 4), np.uint8, surf.get_data(), strides=(surf.get_stride(), 4, 1))[..., [2, 1, 0]].copy()
    Image.fromarray(arr).resize((W, H), Image.LANCZOS).save(path, optimize=True)


if __name__ == "__main__":
    # demo: "2007 AGAIN?" — arrow on the real Oct 2007 SPY peak, underwater area until mid-2009, recovery hidden
    import pandas as pd
    spy = pd.read_csv("spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
    seg = spy["Adj Close"]["2006-01-01":"2009-06-01"]
    pk = seg["2007-01-01":"2007-12-31"].idxmax()
    event_cover("demo_event_cover.png", "2007 AGAIN?", seg.values, seg.index.get_loc(pk), shade="underwater",
                level=float(seg[pk]), redact=False)
    print("demo_event_cover.png")
