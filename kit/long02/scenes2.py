# ================================================================ scenes (long #2: the Nasdaq just crashed)
BX = (130, 250, 1150, 520)
YRS = (2005, 2008, 2011, 2014, 2017, 2020, 2024)
RED_D = (0xB0, 0x1E, 0x32)
GREEN_D = (0x12, 0x9E, 0x5E)


def chapter_card(num, title, sub, col):
    def f(ctx, t, s0, s1):
        ops_room(ctx, t)
        p = back(prog(t, s0 + 0.05, 0.4))
        if p > 0:
            ctx.save(); ctx.translate(720, 520); ctx.rotate(-0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
            card(ctx, -560, -230, 1120, 460, C["cream"], 1, 22, border=col)
            rect(ctx, -556, -226, 1112, 100, col)
            text(ctx, num, 0, -158, 52, C["ink"], 1, MONO, True, "center")
            size = 120
            while tw(ctx, title, size) > 1020:
                size -= 6
            text(ctx, title, 0, 60, size, C["ink"], 1, HEAD, True, "center")
            text(ctx, sub, 0, 170, 40, C["ink"], 0.6, HEAD, True, "center")
            ctx.restore()
    return f


def falling_candles(ctx, t, n=26, col=None, a=0.55, seed=3):
    col = col or C["red"]
    rr = random.Random(seed)
    for k in range(n):
        x = rr.random() * W
        sp = 120 + rr.random() * 260
        y = (rr.random() * H + t * sp) % (H + 300) - 150
        h = 60 + rr.random() * 120
        rect(ctx, x + 9, y - 30, 4, h + 60, col, a * 0.7)
        rect(ctx, x, y, 22, h, col, a)


def alarm_bg(ctx, t):
    bg_fill(ctx, (0x3A, 0x0C, 0x14), (0x12, 0x04, 0x08))
    pulse = 0.08 + 0.08 * (0.5 + 0.5 * math.sin(t * 7))
    ctx.set_source_rgba(1, 0.1, 0.15, pulse); ctx.paint()
    falling_candles(ctx, t)


def sticker(ctx, x, y, label, p, col=None, size=40, rot=0.05):
    """comment sticker with a drawn down-arrow"""
    if p <= 0:
        return
    col = col or C["yellow"]
    w = tw(ctx, label, size) + 120
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + math.sin(t_glob[0] * 6) * 0.015); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -w / 2, -size * 0.95, w, size * 1.9, col, 1, 26)
    text(ctx, label, -30, size * 0.36, size, C["ink"], 1, HEAD, True, "center")
    ax = w / 2 - 50
    bob = math.sin(t_glob[0] * 9) * 6
    ctx.new_path(); ctx.move_to(ax, -size * 0.45 + bob); ctx.line_to(ax, size * 0.45 + bob)
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.move_to(ax - 16, size * 0.18 + bob); ctx.line_to(ax, size * 0.5 + bob); ctx.line_to(ax + 16, size * 0.18 + bob); ctx.stroke()
    ctx.restore()


t_glob = [0.0]


def lock_icon(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -22, 22, math.pi, 0); ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(9); ctx.stroke()
    rrect(ctx, -32, -22, 64, 52, 8); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, 7, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()
    ctx.restore()


def redacted(ctx, x, y, w, h, label="??", torn=0.0):
    """black redaction bar; torn in [0,1] slides it off"""
    if torn >= 1:
        return
    ctx.save(); ctx.translate(x + torn * 900, y - torn * 300); ctx.rotate(-0.04 - torn * 0.6)
    rect(ctx, -w / 2, -h / 2, w, h, C["ink"], 1 - torn * 0.5)
    for k in range(int(w / 40)):
        rect(ctx, -w / 2 + k * 40 + 6, -h / 2 + 6, 22, 5, (0x33, 0x38, 0x3C), 0.8)
    text(ctx, label, 0, h * 0.18, h * 0.5, (0x55, 0x5C, 0x62), 1, MONO, True, "center")
    ctx.restore()


def schematic_line(ctx, box, pts, upto_u, col, width=8):
    """illustrative (not data) line from normalized points"""
    n = max(2, int(len(pts) * clamp(upto_u)))
    xs = [box[0] + p[0] * box[2] for p in pts[:n]]
    ys = [box[1] + box[3] - p[1] * box[3] for p in pts[:n]]
    poly(ctx, xs, ys, col, width, 1, True)
    return xs[-1], ys[-1]


_rs = random.Random(11)
NASDAQ_SKETCH = []
_v = 0.35
for _k in range(120):
    if _k < 80:
        _v += 0.006 + (_rs.random() - 0.45) * 0.02
    elif _k < 96:
        _v -= 0.004 + _rs.random() * 0.01
    elif _k < 104:
        _v -= 0.002 + _rs.random() * 0.004
    elif _k == 104:
        _v -= 0.13
    elif _k == 105:
        _v += 0.035
    else:
        break
    NASDAQ_SKETCH.append((_k / 105, clamp(_v, 0.05, 0.98)))


# ---------------------------------------------------------------- CH0 cold open
def s_hook1(ctx, t, s0, s1):
    alarm_bg(ctx, t)
    ticker_band(ctx, 880, t, "NASDAQ -5.5%   ·   NASDAQ-100 -6.4%   ·   CHIP STOCKS -12%   ·   ~$3 TRILLION GONE   ·   ", C["red"], C["white"], 260)
    p = back(prog(t, -0.12, 0.3))
    if p > 0:
        ctx.save(); ctx.translate(700, 470); ctx.rotate(-0.05 + math.sin(t * 30) * 0.004 * (1 - prog(t, 0, 1.2)))
        ctx.scale(max(p, 1e-3), max(p, 1e-3))
        text(ctx, "-5.5%", 0, 120, 340, C["white"], 1, HEAD, True, "center", outline=26, ocol=C["ink"])
        ctx.restore()
    q = back(prog(t, 0.25, 0.35))
    tag(ctx, 700, 180, "NASDAQ · THURSDAY", C["yellow"], q, 52, 0.03)
    tag(ctx, 700, 760, "WHAT NEXT?", C["white"], back(prog(t, 1.4, 0.35)), 56, 0.04)


def s_hook2(ctx, t, s0, s1):
    alarm_bg(ctx, t)
    # 19 months flipping
    k = int(clamp((t - s0) / 1.6) * 19)
    for j in range(19):
        x = 150 + (j % 10) * 100; y = 330 + (j // 10) * 150
        on = j < k
        card(ctx, x, y, 84, 120, C["cream"] if on else (0x40, 0x20, 0x26), 1, 10)
        if on:
            ctx.new_path(); ctx.move_to(x + 14, y + 20); ctx.line_to(x + 70, y + 100); ctx.move_to(x + 70, y + 20); ctx.line_to(x + 14, y + 100)
            ctx.set_source_rgba(*rgba(C["red"])); ctx.set_line_width(8); ctx.stroke()
    text(ctx, f"{k}", 1250, 470, 160, C["yellow"], 1, MONO, True, "center", outline=10, ocol=C["ink"])
    text(ctx, "MONTHS", 1250, 540, 40, C["white"], 1, MONO, True, "center")
    stamp(ctx, "WORST DAY", "IN 19 MONTHS", 700, 760, t, A("ch0", "worst"), C["red"], 80)


def s_hook3(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x14, 0x10), (0x0A, 0x06, 0x05))
    # money flying away
    u = t - s0
    rr = random.Random(4)
    for k in range(60):
        x0 = 300 + rr.random() * 800; y0 = 450 + rr.random() * 300
        sp = 200 + rr.random() * 500
        tt = max(0.0, u - rr.random() * 1.5)
        x = x0 + tt * sp * 0.9; y = y0 - tt * sp * 0.5 - 60 * math.sin(tt * 3 + k)
        ctx.save(); ctx.translate(x, y); ctx.rotate(tt * 3 + k)
        rect(ctx, -34, -18, 68, 36, (0x5C, 0xB8, 0x5C), 0.95); rect(ctx, -34, -18, 68, 36, (0x2E, 0x7D, 0x32), 0.3)
        text(ctx, "$", 0, 10, 26, (0x1B, 0x4D, 0x20), 1, HEAD, True, "center")
        ctx.restore()
    big_card(ctx, "~$3 TRILLION", 700, 380, back(prog(t, A("ch0", "trillion") - 0.2, 0.35)), C["red"], C["white"], 110, -0.04)
    tag(ctx, 700, 600, "GONE IN ONE SESSION", C["yellow"], back(prog(t, A("ch0", "gone"), 0.35)), 46, 0.04)


def s_hook4(ctx, t, s0, s1):
    bg_fill(ctx, (0x22, 0x26, 0x2C), (0x0C, 0x0E, 0x12))
    god_rays(ctx, 700, 500, t, 0.05, C["red"], 12)
    text(ctx, "EVERYONE IS ASKING:", 700, 260, 48, C["grey"], 1, MONO, True, "center")
    qs = [("SELL?", 250, 380), ("HOLD?", 1120, 360), ("IS IT 2008?", 330, 700), ("BUY THE DIP?", 1080, 720),
          ("CASH?", 200, 540), ("PANIC?", 1190, 560), ("TOO LATE?", 700, 820)]
    for j, (q, x, y) in enumerate(qs):
        p = back(prog(t, A("ch0", "everyone") + j * 0.22, 0.3))
        if p <= 0:
            continue
        fade = 1 - 0.65 * clamp((t - A("ch0", "Do") + 0.1) / 0.3)
        ctx.save(); ctx.translate(x, y + math.sin(t * 3 + j) * 6); ctx.rotate(-0.06 + 0.04 * (j % 3)); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        w_ = tw(ctx, q, 40) + 50
        card(ctx, -w_ / 2, -40, w_, 76, C["white"], fade, 30)
        ctx.new_path(); ctx.move_to(-20, 34); ctx.line_to(-34, 62); ctx.line_to(6, 34); ctx.close_path(); ctx.set_source_rgba(*rgba(C["white"], fade)); ctx.fill()
        text(ctx, q, 0, 14, 40, C["ink"], fade, HEAD, True, "center")
        ctx.restore()
    p = back(prog(t, A("ch0", "Do") - 0.1, 0.35))
    if p > 0:
        pulse = 1 + 0.05 * math.sin(t * 9)
        ctx.save(); ctx.translate(700, 520); ctx.scale(max(p * pulse, 1e-3), max(p * pulse, 1e-3))
        card(ctx, -330, -110, 660, 220, C["red"], 1, 110)
        text(ctx, "SELL?", 0, 50, 150, C["white"], 1, HEAD, True, "center")
        ctx.restore()


_GRID = {}


def _grid_surface():
    if "s" in _GRID:
        return _GRID["s"]
    cols, cw = 126, 9
    rows = (N + cols - 1) // cols
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * cw + 20, rows * cw + 20)
    g = cairo.Context(sf)
    g.set_source_rgba(*rgba((0x14, 0x22, 0x2E))); g.paint()
    for i in range(N):
        c_, r_ = i % cols, i // cols
        g.rectangle(10 + c_ * cw, 10 + r_ * cw, cw - 2, cw - 2)
    g.set_source_rgba(*rgba((0x2A, 0x3A, 0x48))); g.fill()
    _GRID["s"] = sf; _GRID["dims"] = (cols, cw, rows)
    return sf


def s_hook5(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x1A, 0x24), (0x05, 0x0A, 0x10))
    sf = _grid_surface(); cols, cw, rows = _GRID["dims"]
    x0, y0 = 700 - (cols * cw + 20) / 2, 240
    a = clamp((t - s0) / 0.4)
    ctx.save(); ctx.translate(x0, y0); ctx.set_source_surface(sf, 0, 0); ctx.paint_with_alpha(a); ctx.restore()
    k = clamp((t - A("ch0", "every", 1)) / 2.2)
    shown = int(k * len(CRASH))
    for j, i in enumerate(CRASH[:shown]):
        c_ = i % cols; r_ = i // cols
        pop_ = back(clamp((t - A("ch0", "every", 1) - j / len(CRASH) * 2.2) / 0.25))
        sz = 8 + 10 * pop_
        rect(ctx, x0 + 10 + c_ * cw + 3.5 - sz / 2, y0 + 10 + r_ * cw + 3.5 - sz / 2, sz, sz, C["red"])
    text(ctx, "5,033 TRADING DAYS · SPY 2005-2024", 700, y0 - 24, 30, C["grey"], 1, MONO, True, "center")
    text(ctx, "1 SQUARE = 1 DAY", 700, y0 + rows * cw + 60, 26, C["grey"], 1, MONO, True, "center")
    flip_counter(ctx, 520, 760, 360, 150, "CRASH DAYS (-4% OR WORSE)", str(shown), C["red"], 1, 90)


def s_hook6(ctx, t, s0, s1):
    grid_bg(ctx)
    rect(ctx, 160, 520, 1100, 8, C["cream"], 0.8)
    for k, (lab, word, nth) in enumerate((("1 DAY LATER", "day", 3), ("1 MONTH LATER", "month", 1), ("1 YEAR LATER", "year", 1))):
        p = back(prog(t, A("ch0", word, nth), 0.35))
        x = 260 + k * 450
        if p > 0:
            ctx.new_path(); ctx.arc(x, 524, 26 * p, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["yellow"])); ctx.fill()
        tag(ctx, x, 420 + (k % 2) * 220, lab, C["cream"], p, 38, -0.04 + k * 0.04)
    ctx.new_path(); ctx.arc(140, 524, 30, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["red"])); ctx.fill()
    text(ctx, "CRASH", 140, 600, 30, C["red"], 1, MONO, True, "center")


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0xF6, 0xD3, 0x6B), (0xE8, 0x9A, 0x3A))
    god_rays(ctx, 700, 540, t, 0.12, C["white"], 16)
    p = back(prog(t, s0 + 0.05, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(700, 230); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -560, -95, 1120, 190, C["white"], 1, 20)
        text(ctx, "1 YEAR AFTER A CRASH DAY,", 0, -12, 48, C["ink"], 1, HEAD, True, "center")
        text(ctx, "HOW MANY OF 39 WERE HIGHER?", 0, 54, 48, C["red"], 1, HEAD, True, "center")
        ctx.restore()
    fade = 1 - clamp((t - A("ch0", "A", 4) + 0.3) / 0.35)
    if fade > 0:
        for j in range(39):
            p = back(prog(t, s0 + 0.4 + j * 0.035, 0.25))
            if p <= 0:
                continue
            c_, r_ = j % 13, j // 13
            lit = t >= A("ch0", "thirty-nine") and (int(t * 8) + j * 7) % 5 == 0
            ctx.save(); ctx.translate(250 + c_ * 76, 430 + r_ * 86); ctx.scale(p * fade, p * fade); ctx.rotate(math.sin(t * 2 + j) * 0.05)
            rect(ctx, -32, -36, 64, 72, C["yellow"] if lit else C["ink"], 0.9)
            text(ctx, "?", 0, 18, 46, C["ink"] if lit else C["cream"], 1, HEAD, True, "center")
            ctx.restore()
        text(ctx, "39 CRASH DAYS. +1 YEAR. HIGHER OR LOWER?", 700, 720, 34, C["ink"], fade * clamp((t - A("ch0", "One") + 0.1) / 0.3), MONO, True, "center")
    for k, (lab, sub, col, word) in enumerate((("A", "LESS THAN HALF", C["red"], "A"), ("B", "ALMOST ALL", C["green"], "B"))):
        nth = 4 if word == "A" else 1
        b = back(prog(t, A("ch0", word, nth) - 0.1, 0.35))
        if b > 0:
            x = 420 + k * 560
            ctx.save(); ctx.translate(x, 520); ctx.scale(max(b, 1e-3) * (1 + 0.03 * math.sin(t * 8 + k)), max(b, 1e-3))
            card(ctx, -230, -110, 460, 220, col, 1, 30)
            text(ctx, lab, -150, 40, 120, C["white"] if k == 0 else C["ink"], 1, HEAD, True, "center")
            text(ctx, sub, 50, 22, 40, C["white"] if k == 0 else C["ink"], 1, HEAD, True, "center")
            ctx.restore()
    lp = back(prog(t, A("ch0", "Lock"), 0.35))
    if lp > 0:
        redacted(ctx, 700, 740, 420, 110, "??/39")
        lock_icon(ctx, 970, 740, lp, C["yellow"])
    t_glob[0] = t
    sticker(ctx, 1080, 860 - 60, "COMMENT YOUR GUESS", back(prog(t, A("ch0", "guess") + 0.2, 0.35)), C["white"], 38)


def s_tease(ctx, t, s0, s1):
    bg_fill(ctx, (0x1A, 0x10, 0x2A), (0x08, 0x05, 0x10))
    for kk in range(40):
        rect(ctx, (kk * 263) % W, 160 + (kk * 151) % 500, 5, 5, C["cream"], 0.3 + 0.5 * abs(math.sin(t * 2 + kk)))
    p = back(prog(t, s0 + 0.15, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(700, 420); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -540, -150, 1080, 300, C["cream"], 1, 22, border=C["purple"])
        text(ctx, "ON THE WAY:", 0, -90, 34, C["ink"], 0.6, MONO, True, "center")
        q1 = back(prog(t, A("ch0", "panic") - 0.15, 0.3)); q2 = back(prog(t, A("ch0", "beat") - 0.15, 0.3))
        if q1 > 0:
            text(ctx, "THE PANIC MOVE THAT", 0, -20, 58 * min(1.15, q1), C["ink"], 1, HEAD, True, "center")
        if q2 > 0:
            text(ctx, "BEAT DOING NOTHING", 0, 62, 70 * min(1.15, q2), (0x6B, 0x3F, 0xB8), 1, HEAD, True, "center")
        redacted(ctx, 0, 118, 520, 50, "CLASSIFIED")
        ctx.restore()
    stamp(ctx, "...AND WHY", "I WOULDN'T TOUCH IT", 700, 760, t, A("ch0", "wouldn't"), C["red"], 70, 0.05)


# ---------------------------------------------------------------- CH1 what happened
NBOX = (150, 260, 1100, 500)


def sketch_card(ctx):
    chart_card(ctx, NBOX)
    text(ctx, "NASDAQ · ILLUSTRATION, NOT TO SCALE", NBOX[0], NBOX[1] - 4, 22, C["ink"], 0.45, MONO, True)


def s_record(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x30, 0x2A), (0x06, 0x14, 0x12))
    sketch_card(ctx)
    k = ease_io(prog(t, s0 + 0.1, 2.6))
    pts = [p for p in NASDAQ_SKETCH if p[0] <= 80 / 105 + 0.001]
    x, y = schematic_line(ctx, NBOX, pts, k, GREEN_D)
    if k >= 0.99:
        tag(ctx, x - 40, y - 60, "RECORD HIGH · OCT 6", C["green"], back(prog(t, A("ch1", "record") - 0.1, 0.35)), 34, -0.04)
    for j in range(5):
        p = back(prog(t, A("ch1", "AI") + j * 0.12, 0.3))
        if p > 0:
            cx = NBOX[0] + 120 + j * 200; cy = NBOX[1] + NBOX[3] - 70 - j * 40 + math.sin(t * 4 + j) * 6
            ctx.save(); ctx.translate(cx, cy); ctx.scale(p, p)
            rrect(ctx, -34, -34, 68, 68, 8); ctx.set_source_rgba(*rgba(C["dark"])); ctx.fill()
            for q in range(4):
                rect(ctx, -46, -24 + q * 14, 12, 6, C["yellow"]); rect(ctx, 34, -24 + q * 14, 12, 6, C["yellow"])
            text(ctx, "AI", 0, 12, 30, C["yellow"], 1, MONO, True, "center")
            ctx.restore()


def s_selloff(ctx, t, s0, s1):
    rain_bg(ctx, t, 9)
    sketch_card(ctx)
    k = ease_io(prog(t, s0 + 0.1, A("ch1", "Thursday") - s0 + 0.6))
    pts = NASDAQ_SKETCH[:106]
    schematic_line(ctx, NBOX, pts[:80], 1.0, GREEN_D)
    tail = pts[79:]
    n = max(2, int(len(tail) * k))
    xs = [NBOX[0] + p[0] * NBOX[2] for p in tail[:n]]; ys = [NBOX[1] + NBOX[3] - p[1] * NBOX[3] for p in tail[:n]]
    poly(ctx, xs, ys, C["red"], 9, 1, True)
    tag(ctx, 470, 340, "CHIPS -12%", C["red"], back(prog(t, A("ch1", "twelve"), 0.35)), 46, -0.05, C["white"])
    tag(ctx, 830, 440, "NASDAQ-100 -6.4%", C["red"], back(prog(t, A("ch1", "six"), 0.35)), 46, 0.04, C["white"])
    tag(ctx, 760, 560, "WORST DAY SINCE MARCH 2020", C["yellow"], back(prog(t, A("ch1", "since"), 0.35)), 34, -0.03)


def s_correction(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x2E), (0x10, 0x0A, 0x14))
    # thermometer from record high down
    x0, top, bot = 380, 240, 820
    rect(ctx, x0 - 50, top, 100, bot - top, (0x30, 0x34, 0x3A))
    k = ease_io(prog(t, s0 + 0.2, 1.4))
    lvl = top + (bot - top) * 0.62 * k
    rect(ctx, x0 - 50, top, 100, lvl - top, C["red"])
    for j, lab in enumerate(("RECORD", "-5%", "-10%")):
        y = top + (bot - top) * 0.3 * j
        rect(ctx, x0 + 60, y, 50, 4, C["cream"])
        text(ctx, lab, x0 + 130, y + 12, 36, C["cream"], 1, MONO, True)
    stamp(ctx, "CORRECTION", "MORE THAN 10% BELOW THE HIGH", 920, 470, t, A("ch1", "correction"), C["red"], 96)


def s_bounce(ctx, t, s0, s1):
    bg_fill(ctx, (0xD9, 0xF2, 0xEA), (0xA8, 0xDD, 0xCB))
    p = back(prog(t, A("ch1", "bounced") - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(560, 560); ctx.scale(1, max(p, 1e-3))
        rect(ctx, -70, -110, 140, 110, C["green"]); rect(ctx, -6, -170, 12, 230, GREEN_D)
        ctx.restore()
        text(ctx, "+1.1%", 560, 380, 90, GREEN_D, 1, HEAD, True, "center")
    tag(ctx, 560, 700, "FRIDAY", C["cream"], back(prog(t, A("ch1", "Friday"), 0.35)), 40)
    tag(ctx, 960, 450, "A TINY BREATH", C["white"], back(prog(t, A("ch1", "breath") - 0.2, 0.35)), 46, 0.05)


def s_world(ctx, t, s0, s1):
    rain_bg(ctx, t, 7)
    cx, cy, r = 600, 560, 230
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["blue"])); ctx.fill()
    for k in range(5):
        ctx.new_path(); ctx.arc(cx + math.cos(k * 1.3 + t * 0.4) * 120, cy + math.sin(k * 2.1) * 120, 50 + k * 8, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba(C["green"], 0.85)); ctx.fill()
    big_card(ctx, "THE END OF THE WORLD?", 640, 230, back(prog(t, A("ch1", "end") - 0.2, 0.35)), C["red"], C["white"], 64, -0.04)
    stamp(ctx, "NOT THE FIRST", "NOT EVEN CLOSE", 1000, 640, t, A("ch1", "first") - 0.1, C["yellow"], 84, 0.06)


# ---------------------------------------------------------------- CH2 39 crash days
def s_method(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x18), (0x05, 0x07, 0x0A))
    card(ctx, 160, 230, 1120, 560, (0x0B, 0x10, 0x14), 1, 18, border=C["green"])
    lines = [("> data: SPY (S&P 500 fund)", "used"), ("> period: 2005-2024 (5,033 days)", "Two"),
             ("> rule: daily close <= -4%", "Every"), ("> matches: 39 days", "Thirty-nine")]
    for k, (ln, w) in enumerate(lines):
        tt = A("ch2", w)
        n = int(clamp((t - tt) / 0.7) * len(ln))
        if n > 0:
            text(ctx, ln[:n], 210, 350 + k * 120, 52, C["green"] if k < 3 else C["yellow"], 1, MONO, True)
    if int(t * 2) % 2 == 0:
        rect(ctx, 210, 350 + 3 * 120 + 34, 34, 8, C["green"])


def s_timeline39(ctx, t, s0, s1):
    grid_bg(ctx)
    box = (130, 250, 1150, 380)
    chart_card(ctx, box)
    series(ctx, box, ADJ, 0, N - 1, N - 1, ADJ.min() * 0.9, ADJ.max() * 1.05, C["ink"], 4, False, 4)
    k = clamp((t - s0 - 0.2) / 1.6)
    for j, i in enumerate(CRASH[:int(k * len(CRASH))]):
        x, y = pt(box, i, ADJ[i], 0, N - 1, ADJ.min() * 0.9, ADJ.max() * 1.05)
        ctx.new_path(); ctx.arc(x, y, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["red"])); ctx.fill()
    years_axis(ctx, box, 0, N - 1, YRS)
    yrs = L2["years"]
    by = 760
    for k2, (yr, cnt) in enumerate(sorted(yrs.items())):
        x = 240 + k2 * 150
        hl = (yr == "2008" and t >= A("ch2", "Sixteen")) or (yr == "2020" and t >= A("ch2", "Nine"))
        hgt = cnt * 9 * clamp((t - s0 - 0.6) / 0.8)
        rect(ctx, x - 40, by + 140 - hgt, 80, hgt, C["red"] if hl else (0x8A, 0x4A, 0x55))
        text(ctx, str(yr), x, by + 175, 26, C["cream"], 1, MONO, True, "center")
        if hl:
            text(ctx, str(cnt), x, by + 130 - hgt, 40, C["yellow"], 1, MONO, True, "center")
    tag(ctx, 1000, 540, "THEY COME IN PACKS", C["yellow"], back(prog(t, A("ch2", "packs") - 0.2, 0.35)), 40, 0.04)


def s_worst(ctx, t, s0, s1):
    alarm_bg(ctx, t)
    a, b = di("2020-02-14"), di("2020-04-14")
    box = (160, 300, 1100, 420)
    chart_card(ctx, box)
    n = int(clamp((t - s0 - 0.1) / 1.6) * (b - a))
    bw = box[2] / (b - a)
    for j in range(n):
        i = a + j
        r = RET[i]
        h = abs(r) * box[3] / 0.12 * 0.5
        col = C["red"] if r < 0 else C["green"]
        if i == di("2020-03-16"):
            col = (0xFF, 0x20, 0x40)
        y = box[1] + box[3] / 2
        rect(ctx, box[0] + j * bw + 2, y if r < 0 else y - h, bw - 4, h, col)
    text(ctx, "FEB 2020", box[0], box[1] + box[3] + 40, 26, C["ink"], 0.6, MONO, True)
    text(ctx, "APR 2020", box[0] + box[2], box[1] + box[3] + 40, 26, C["ink"], 0.6, MONO, True, "right")
    big_card(ctx, "MAR 16, 2020: -10.9%", 700, 240, back(prog(t, A("ch2", "March") - 0.1, 0.35)), C["red"], C["white"], 60, -0.03)


def s_morning(ctx, t, s0, s1):
    bg_fill(ctx, (0xF7, 0xC8, 0x8A), (0xF2, 0x8A, 0x5C))
    u = prog(t, s0, 1.4)
    cy = 820 - 260 * ease(u)
    god_rays(ctx, 700, cy, t, 0.10, C["white"], 14)
    ctx.new_path(); ctx.arc(700, cy, 120, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.92, 0.55, 1); ctx.fill()
    rect(ctx, 0, 820, W, H - 820, (0x3A, 0x2A, 0x40))
    big_card(ctx, "THE NEXT MORNING?", 700, 300, back(prog(t, A("ch2", "next") - 0.3, 0.35)), C["ink"], C["white"], 80, 0.03)


# ---------------------------------------------------------------- CH3 next day / month
def compare_bars(ctx, t, title, a_val, b_val, ta, tb, lab_a="AFTER A CRASH", lab_b="ANY NORMAL DAY", worse=False):
    bg_fill(ctx, (0x1E, 0x2A, 0x3A), (0x0C, 0x12, 0x1A))
    text(ctx, title, 700, 240, 54, C["cream"], 1, HEAD, True, "center")
    base = 820
    for k, (lab, v, tt, col) in enumerate(((lab_a, a_val, ta, C["red"] if worse else C["yellow"]), (lab_b, b_val, tb, C["grey"]))):
        u = ease_io(prog(t, tt - 0.3, 0.8))
        h = (v / 100) * 460 * u
        x = 460 + k * 480
        rect(ctx, x - 120, base - h, 240, h, col)
        if u > 0.05:
            text(ctx, f"{v * u:.0f}%", x, base - h - 24, 80, C["white"], 1, MONO, True, "center")
        text(ctx, lab, x, base + 50, 30, C["cream"], 1, MONO, True, "center")
    rect(ctx, 260, base, 880, 6, C["cream"])


def s_nextday(ctx, t, s0, s1):
    compare_bars(ctx, t, "UP THE NEXT DAY", 59, 55, A("ch3", "fifty-nine"), A("ch3", "fifty-five"))
    tag(ctx, 700, 330, "A SMALL BOUNCE", C["green"], back(prog(t, A("ch3", "bounce") - 0.1, 0.35)), 40, -0.04)


def s_month(ctx, t, s0, s1):
    compare_bars(ctx, t, "UP ONE MONTH LATER", 62, 67, A("ch3", "sixty-two"), A("ch3", "sixty-seven"), worse=True)
    stamp(ctx, "WORSE THAN RANDOM", None, 700, 345, t, A("ch3", "worse"), C["red"], 72, -0.05)


def s_sep08(ctx, t, s0, s1):
    rain_bg(ctx, t, 11)
    a, b = di("2008-09-02"), di("2008-11-28")
    box = (160, 260, 1100, 470)
    chart_card(ctx, box)
    lo, hi = ADJ[a:b].min() * 0.95, ADJ[a:b].max() * 1.03
    k = ease_io(prog(t, s0 + 0.1, A("ch3", "sixteen") - s0))
    upto = int(a + 1 + (b - a - 1) * k)
    series(ctx, box, ADJ, a, b, upto, lo, hi, C["red"], 7, True, 1)
    i0 = di("2008-09-29")
    if upto >= i0:
        x, y = pt(box, i0, ADJ[i0], a, b, lo, hi)
        ctx.new_path(); ctx.arc(x, y, 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["yellow"])); ctx.fill()
        tag(ctx, x + 40, y - 70, "SEP 29: -7.8%", C["yellow"], back(prog(t, A("ch3", "eight", 2), 0.35)), 36, -0.04)
    i1 = min(i0 + 21, b - 1)
    if upto >= i1:
        x, y = pt(box, i1, ADJ[i1], a, b, lo, hi)
        tag(ctx, x + 60, y + 60, "A MONTH LATER: -16%", C["red"], back(prog(t, A("ch3", "sixteen") - 0.2, 0.35)), 36, 0.04, C["white"])
    text(ctx, "SEP 2008", box[0], box[1] + box[3] + 40, 26, C["ink"], 0.6, MONO, True)
    text(ctx, "NOV 2008", box[0] + box[2], box[1] + box[3] + 40, 26, C["ink"], 0.6, MONO, True, "right")


def s_coin(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x24, 0x40), (0x10, 0x0C, 0x1C))
    sc = abs(math.cos(t * 9))
    ctx.save(); ctx.translate(640, 520); ctx.scale(max(sc, 0.05), 1)
    ctx.new_path(); ctx.arc(0, 0, 200, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["yellow"])); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(10); ctx.stroke()
    text(ctx, "?", 0, 70, 220, C["ink"], 1, HEAD, True, "center")
    ctx.restore()
    stamp(ctx, "COIN FLIP", "THE NEXT MONTH", 1000, 300, t, A("ch3", "coin") - 0.1, C["red"], 80, 0.05)


def s_getout(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x30, 0x22), (0x06, 0x12, 0x0C))
    # exit door
    card(ctx, 420, 260, 360, 560, (0x2E, 0x7D, 0x32), 1, 8)
    rect(ctx, 450, 290, 300, 500, (0x1B, 0x4D, 0x20))
    ctx.new_path(); ctx.arc(720, 560, 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["yellow"])); ctx.fill()
    card(ctx, 470, 180, 260, 80, C["green"], 1, 10)
    text(ctx, "EXIT", 600, 238, 54, C["white"], 1, HEAD, True, "center")
    big_card(ctx, "SHOULD YOU GET OUT?", 1000, 400, back(prog(t, A("ch3", "should") - 0.1, 0.35)), C["cream"], C["ink"], 54, 0.04)
    tag(ctx, 1000, 560, "LET'S TEST IT", C["yellow"], back(prog(t, A("ch3", "test") - 0.1, 0.35)), 44, -0.04)


# ---------------------------------------------------------------- CH4 panic seller
def s_two(ctx, t, s0, s1):
    bg_fill(ctx, (0xF4, 0xEC, 0xD8), (0xE2, 0xD4, 0xB0))
    for k, (lab, sub, col, word, nth) in enumerate((("THE HOLDER", "NEVER SELLS", C["green"], "holder", 1),
                                                   ("PANIC SELLER", "AFTER A -4% DAY:\nSELL NEXT MORNING\nBUY BACK 1 MONTH LATER", C["red"], "panic", 1))):
        p = back(prog(t, A("ch4", word, nth) - 0.2, 0.35))
        if p <= 0:
            continue
        x = 400 + k * 560
        ctx.save(); ctx.translate(x, 500); ctx.rotate(-0.03 + k * 0.06); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -250, -230, 500, 460, C["white"], 1, 20, border=col)
        rect(ctx, -246, -226, 492, 90, col)
        text(ctx, lab, 0, -165, 46, C["white"], 1, HEAD, True, "center")
        piggy(ctx, 0, -40, 0.6, t)
        for j, ln in enumerate(sub.split("\n")):
            text(ctx, ln, 0, (110 if k else 140) + j * 44, 28 if k else 38, C["ink"], 1, MONO, True, "center")
        ctx.restore()
    flip_counter(ctx, 520, 790, 360, 130, "EACH", "$10,000", C["yellow"], back(prog(t, A("ch4", "Ten") - 0.1, 0.3)), 60) if t >= A("ch4", "Ten") - 0.1 else None
    tag(ctx, 1100, 830, "FEES INCLUDED", C["yellow"], back(prog(t, A("ch4", "Fees"), 0.35)), 36, 0.04)


def s_race(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x16, 0x2A), (0x06, 0x0A, 0x14))
    box = (130, 260, 1150, 500)
    chart_card(ctx, box)
    t_end = A("ch4", "front") + 0.4
    k = ease_io(prog(t, s0 + 0.1, t_end - s0 - 0.1))
    i_end = N - 1
    upto = int(1 + (i_end - 1) * k)
    vmax = 110000
    # out-of-market shading
    for i in range(0, upto, 3):
        if OUT[i]:
            x, _ = pt(box, i, 0, 0, N - 1, 0, vmax)
            rect(ctx, x, box[1], 4, box[3], C["red"], 0.16)
    series(ctx, box, EQB, 0, N - 1, upto, 0, vmax, (0x5A, 0x64, 0x6B), 6, False, 3)
    series(ctx, box, EQP, 0, N - 1, upto, 0, vmax, C["red"], 7, True, 3)
    years_axis(ctx, box, 0, N - 1, YRS)
    legend(ctx, box[0] + 10, box[1] + 30, [("PANIC SELLER", C["red"]), ("HOLDER", (0x5A, 0x64, 0x6B))])
    yr = DATES[upto].year
    flip_counter(ctx, 560, 280, 250, 110, "YEAR", str(yr), C["yellow"], 1, 56)
    # redacted totals during the race
    redacted(ctx, 1060, 330, 300, 70, "$??,???")
    hx, hy = pt(box, upto, EQP[upto], 0, N - 1, 0, vmax)
    ctx.new_path(); ctx.arc(hx, hy, 12 + 3 * math.sin(t * 10), 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["red"])); ctx.fill()
    for lab, word, col in (("OUT!", "out", C["red"]), ("AHEAD", "ahead", C["green"]), ("2011: OUT AGAIN", "eleven", C["red"]),
                           ("MISSES THE REBOUND", "rebound", C["yellow"]), ("BEHIND", "behind", C["grey"]), ("BACK IN FRONT", "front", C["green"])):
        tt = A("ch4", word)
        if tt - 0.1 <= t < tt + 1.6:
            tx = clamp(hx, 330, 1080); ty = max(330, hy - 90)
            tag(ctx, tx, ty, lab, col, back(prog(t, tt - 0.1, 0.3)), 34, -0.04, C["white"] if col in (C["red"], C["grey"]) else None)


def score_scene(rows, title_line, ch, final_tag=None):
    def f(ctx, t, s0, s1):
        stadium(ctx, t)
        card(ctx, 140, 230, 1140, 600, (0x14, 0x18, 0x1C), 1, 20, border=C["yellow"])
        text(ctx, title_line, 710, 300, 30, C["yellow"], 1, MONO, True, "center")
        for k, (lab, v0, v1, tt, col) in enumerate(rows):
            a = ease_io(prog(t, tt - 0.5, 1.1))
            val = v0 + (v1 - v0) * a
            flip_counter(ctx, 200, 350 + k * 220, 1020, 190, lab, money(val) if t >= tt - 0.6 else "$??,???", col, 1, 100)
        if final_tag:
            lab, tt, col = final_tag
            tag(ctx, 1050, 830, lab, col, back(prog(t, tt, 0.35)), 52, -0.05, C["ink"])
    return f


WINDOWS = [(5, "1 WK", "One", 1), (10, "2 WK", "Two", 2), (15, "3 WK", None, 0), (21, "1 MO", None, 0), (30, "6 WK", None, 0),
           (42, "8 WK", None, 0), (63, "3 MO", "Three", 1), (126, "6 MO", "Six", 1)]


def s_windows(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x2A, 0x3A), (0x0C, 0x12, 0x1A))
    text(ctx, "SAME RULE · DIFFERENT WAITING TIME", 700, 230, 44, C["cream"], 1, HEAD, True, "center")
    base, top = 800, 300
    vmax = 90000
    yb = base - (70214 / vmax) * (base - top)
    for k, (h, lab, word, nth) in enumerate(WINDOWS):
        v = PANIC[h]
        tt = A("ch4", word, nth) if word else (s0 + 0.5 if h == 21 else A("ch4", "narrow"))
        u = ease_io(prog(t, tt - 0.2, 0.6))
        x = 220 + k * 140
        hh = (v / vmax) * (base - top) * u
        win = v > 70214
        col = (C["green"] if win else C["red"]) if t >= A("ch4", "narrow") else (C["yellow"] if h == 21 else C["red"])
        rect(ctx, x - 50, base - hh, 100, hh, col)
        text(ctx, lab, x, base + 44, 28, C["cream"], 1, MONO, True, "center")
        if u > 0.6:
            text(ctx, f"${v / 1000:.0f}K", x, base - hh - 16, 30, C["white"], 1, MONO, True, "center")
    rect(ctx, 150, yb, 1130, 5, C["yellow"])
    text(ctx, "HOLDER", 1290, yb - 6, 26, C["yellow"], 1, MONO, True)
    text(ctx, "$70K", 1290, yb + 30, 26, C["yellow"], 1, MONO, True)
    if t < A("ch4", "narrow"):
        tag(ctx, 220 + 3 * 140, 900, "THE RACE: 1 MONTH OUT", C["yellow"], back(prog(t, s0 + 0.6, 0.3)), 26, -0.03)
    if t >= A("ch4", "narrow"):
        a = clamp((t - A("ch4", "narrow")) / 0.4)
        ctx.new_path(); rrect(ctx, 220 + 2 * 140 - 66, 310, 4 * 140 - 8, 580, 20)
        ctx.set_source_rgba(*rgba(C["green"], 0.9 * a)); ctx.set_line_width(8); ctx.stroke()
        tag(ctx, 220 + 3.5 * 140, 306, "ONLY 3-8 WEEKS WON", C["green"], back(prog(t, A("ch4", "narrow"), 0.35)), 32, -0.03)


def s_hindsight(ctx, t, s0, s1):
    bg_fill(ctx, (0x22, 0x26, 0x2C), (0x0C, 0x0E, 0x12))
    # rear-view mirror
    ctx.save(); ctx.translate(560, 470); ctx.rotate(-0.06)
    rrect(ctx, -330, -150, 660, 300, 140); ctx.set_source_rgba(*rgba(C["dark"])); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["grey"])); ctx.set_line_width(14); ctx.stroke()
    rrect(ctx, -300, -122, 600, 244, 120); ctx.set_source_rgba(0.45, 0.6, 0.75, 1); ctx.fill()
    xs = [-280 + j * 28 for j in range(21)]
    ys = [40 - j * 4 + 30 * math.sin(j * 0.9) for j in range(21)]
    poly(ctx, xs, ys, C["green"], 6)
    ctx.restore()
    stamp(ctx, "HINDSIGHT", "I ONLY KNOW IT LOOKING BACK", 560, 760, t, A("ch4", "looking"), C["red"], 80)
    tag(ctx, 1080, 300, "1 WEEK?", C["cream"], back(prog(t, A("ch4", "week", 2) - 0.1, 0.3)), 44, -0.05)
    tag(ctx, 1080, 420, "1 YEAR?", C["cream"], back(prog(t, A("ch4", "year") - 0.1, 0.3)), 44, 0.05)


# ---------------------------------------------------------------- CH5 second trap
def s_best10(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x24, 0x10), (0x12, 0x0E, 0x05))
    box = (130, 260, 1150, 480)
    chart_card(ctx, box)
    vlo, vhi = -0.12, 0.15
    k = clamp((t - s0 - 0.1) / 1.4)
    upto = int(N * k)
    zero = box[1] + box[3] * (vhi / (vhi - vlo))
    rect(ctx, box[0], zero, box[2], 2, C["ink"], 0.4)
    for i in range(1, upto, 2):
        r = RET[i]
        if abs(r) < 0.02:
            continue
        x = box[0] + i / (N - 1) * box[2]
        h = abs(r) / (vhi - vlo) * box[3]
        rect(ctx, x, zero - h if r > 0 else zero, 2, h, C["green"] if r > 0 else C["red"], 0.55)
    if t >= A("ch5", "ten") - 0.2:
        for j, i in enumerate(BEST10):
            p = back(prog(t, A("ch5", "ten") + j * 0.08, 0.3))
            x = box[0] + i / (N - 1) * box[2]
            y = zero - RET[i] / (vhi - vlo) * box[3]
            if p > 0:
                star(ctx, x, y - 20, 22 * p, C["yellow"], 1, t)
    years_axis(ctx, box, 0, N - 1, YRS)
    tag(ctx, 900, 700, "9 OF 10: WITHIN 2 WEEKS OF A CRASH DAY", C["yellow"], back(prog(t, A("ch5", "Nine") - 0.1, 0.35)), 30, -0.03)


def s_bestcards(ctx, t, s0, s1):
    rain_bg(ctx, t, 15)
    for k, (date, lab, word, a_, b_) in enumerate((("2008-10-13", "OCT 13, 2008: +14.5%", "October", "2008-09-25", "2008-10-31"),
                                                   ("2020-03-24", "MAR 24, 2020: +9.1%", "March", "2020-03-02", "2020-04-08"))):
        p = back(prog(t, A("ch5", word) - 0.15, 0.35))
        if p <= 0:
            continue
        cx = 400 + k * 600
        ctx.save(); ctx.translate(cx, 520); ctx.rotate(-0.03 + k * 0.06); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -280, -250, 560, 500, C["cream"], 1, 18)
        text(ctx, lab, 0, -190, 34, C["ink"], 1, HEAD, True, "center")
        a, b = di(a_), di(b_)
        bw = 480 / (b - a)
        for j in range(b - a):
            i = a + j; r = RET[i]
            h = abs(r) * 1400
            col = C["green"] if r > 0 else C["red"]
            if DATES[i] == pd.Timestamp(date):
                col = C["yellow"]
            rect(ctx, -240 + j * bw + 1, 40 - h if r > 0 else 40, bw - 2, h, col)
        rect(ctx, -240, 40, 480, 2, C["ink"])
        text(ctx, "RED = CRASH DAYS AROUND IT", 0, 220, 22, C["ink"], 0.6, MONO, True, "center")
        ctx.restore()


def s_hide(ctx, t, s0, s1):
    bg_fill(ctx, (0x1A, 0x10, 0x2A), (0x08, 0x05, 0x10))
    big_card(ctx, "THE BEST DAYS HIDE", 640, 250, back(prog(t, s0 + 0.05, 0.35)), C["yellow"], C["ink"], 64, -0.03)
    big_card(ctx, "NEXT TO THE WORST", 640, 380, back(prog(t, A("ch5", "worst") - 0.1, 0.35)), C["red"], C["white"], 64, 0.03)
    p = back(prog(t, A("ch5", "earlier") - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(640, 640); ctx.rotate(-0.02); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -420, -110, 840, 220, C["cream"], 1, 18)
        text(ctx, "CASE #9: MISS THE 10 BEST DAYS", 0, -30, 38, C["ink"], 1, HEAD, True, "center")
        text(ctx, "$70,214  VS  $31,456  (-55%)", 0, 50, 46, C["red"], 1, MONO, True, "center")
        ctx.restore()


def s_doors(ctx, t, s0, s1):
    bg_fill(ctx, (0x6F, 0xC3, 0xE6), (0xBF, 0xE6, 0xF2))
    rect(ctx, 0, 820, W, H - 820, (0x5C, 0xA8, 0x4A))
    u = ease(prog(t, A("ch5", "doors") - 0.4, 0.8))
    # building with doors opening
    card(ctx, 260, 250, 760, 580, (0xD9, 0xCF, 0xB5), 1, 6)
    god_rays(ctx, 640, 560, t, 0.10 * u, C["yellow"], 12, 600)
    rect(ctx, 460, 420, 360, 400, (0xFF, 0xF2, 0xA8), u)
    rect(ctx, 460, 420, 180 * (1 - u), 400, (0x7A, 0x52, 0x34))
    rect(ctx, 640 + 180 * u, 420, 180 * (1 - u), 400, (0x7A, 0x52, 0x34))
    text(ctx, "+14.5%", 640, 360, 60, GREEN_D, u, HEAD, True, "center")
    tag(ctx, 1080, 320, "YOU: OUTSIDE", C["red"], back(prog(t, A("ch5", "outside") - 0.1, 0.35)), 42, 0.05, C["white"])


# ---------------------------------------------------------------- CH6 the answer
def s_answer(ctx, t, s0, s1):
    bg_fill(ctx, (0xF6, 0xD3, 0x6B), (0xE8, 0x9A, 0x3A))
    god_rays(ctx, 700, 520, t, 0.14, C["white"], 16)
    text(ctx, "1 YEAR AFTER A CRASH DAY: HOW MANY WERE HIGHER?", 700, 220, 40, C["ink"], 1, HEAD, True, "center")
    ta = A("ch6", "Thirty-six", 1)
    # drum roll shake before reveal
    sh = math.sin(t * 40) * 6 if ta - 1.2 < t < ta else 0
    torn = ease(prog(t, ta - 0.05, 0.5))
    ctx.save(); ctx.translate(700 + sh, 450)
    if torn > 0:
        text(ctx, "36 / 39", 0, 80, 230, GREEN_D, 1, HEAD, True, "center", outline=16, ocol=C["ink"])
    ctx.restore()
    redacted(ctx, 700 + sh, 420, 820, 230, "??/39", torn)
    for k, (lab, sub, col) in enumerate((("A", "LESS THAN HALF", C["red"]), ("B", "ALMOST ALL", C["green"]))):
        x = 420 + k * 560
        right = k == 1 and t >= ta
        dim = 0.35 if (t >= ta and k == 0) else 1.0
        ctx.save(); ctx.translate(x, 725)
        card(ctx, -200, -65, 400, 130, col, dim, 24)
        text(ctx, f"{lab}: {sub}", 0, 14, 36, C["ink"], dim, HEAD, True, "center")
        if right:
            check(ctx, 150, 0, 60, C["ink"], 1, 12)
        ctx.restore()
    tag(ctx, 1150, 600, "92%", C["green"], back(prog(t, A("ch6", "Ninety-two"), 0.35)), 70, 0.06)
    t_glob[0] = t
    sticker(ctx, 700, 880, "WERE YOU RIGHT? COMMENT A OR B", back(prog(t, ta + 1.4, 0.35)), C["white"], 32, -0.02)


def s_tiles(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x30, 0x2A), (0x06, 0x14, 0x12))
    x0, y0, sz = 170, 270, 100
    for j, v in enumerate(Y1):
        p = back(prog(t, s0 + 0.1 + j * 0.03, 0.25))
        if p <= 0:
            continue
        c_ = j % 10; r_ = j // 10
        col = C["green"] if v > 0 else C["red"]
        ctx.save(); ctx.translate(x0 + c_ * (sz + 8) + sz / 2, y0 + r_ * (sz + 8) + sz / 2); ctx.scale(p, p)
        rect(ctx, -sz / 2, -sz / 2, sz, sz, col)
        text(ctx, f"{v * 100:+.0f}%", 0, 10, 26, C["ink"], 1, MONO, True, "center")
        ctx.restore()
    tag(ctx, 700, 760, "TYPICAL: +30% A YEAR LATER", C["yellow"], back(prog(t, A("ch6", "thirty") - 0.1, 0.35)), 40, -0.03)
    p = back(prog(t, A("ch6", "random") - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(700, 860); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -460, -45, 920, 90, C["cream"], 1, 14)
        text(ctx, "RANDOM DAY: 82%   ·   CRASH DAY: 92%", 0, 14, 36, C["ink"], 1, MONO, True, "center")
        ctx.restore()
    stamp(ctx, "BETTER ODDS", "THAN A NORMAL DAY", 900, 470, t, A("ch6", "better"), GREEN_D, 60, 0.06)


def s_lehman(ctx, t, s0, s1):
    rain_bg(ctx, t, 9)
    reds = [r for r in L2["rows"] if r["y1"] <= 0]
    for k, r in enumerate(reds):
        p = back(prog(t, A("ch6", "three") + k * 0.15, 0.3))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(330 + k * 320, 420); ctx.rotate(-0.05 + k * 0.05); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        rect(ctx, -130, -100, 260, 200, C["red"])
        text(ctx, r["date"], 0, -20, 34, C["white"], 1, MONO, True, "center")
        text(ctx, f"1Y: {r['y1'] * 100:+.0f}%", 0, 50, 44, C["white"], 1, MONO, True, "center")
        ctx.restore()
    big_card(ctx, "ALL SEPT 2008 · LEHMAN BROTHERS", 640, 720, back(prog(t, A("ch6", "Lehman") - 0.2, 0.35)), C["cream"], C["ink"], 52, -0.02)


def s_honest(ctx, t, s0, s1):
    bg_fill(ctx, (0x22, 0x26, 0x2C), (0x0C, 0x0E, 0x12))
    big_card(ctx, "THE HONEST PART", 640, 230, back(prog(t, A("ch6", "honest") - 0.2, 0.35)), C["yellow"], C["ink"], 70, -0.03)
    # timeline 2000-2024 with our data window
    x0, x1, y = 180, 1180, 600
    rect(ctx, x0, y, x1 - x0, 8, C["cream"], 0.6)
    def xy(yr):
        return x0 + (yr - 2000) / 25 * (x1 - x0)
    k = ease_io(prog(t, A("ch6", "data") - 0.2, 0.6))
    rect(ctx, xy(2005), y - 30, (xy(2025) - xy(2005)) * k, 68, C["green"], 0.85)
    text(ctx, "MY DATA: 2005-2024", (xy(2005) + xy(2025)) / 2, y + 90, 32, C["green"], k, MONO, True, "center")
    p = back(prog(t, A("ch6", "dot-com") - 0.2, 0.35))
    if p > 0:
        rect(ctx, xy(2000), y - 30, (xy(2002.8) - xy(2000)) * p, 68, C["red"], 0.85)
        text(ctx, "DOT-COM", xy(2001.4), y - 50, 32, C["red"], p, MONO, True, "center")
        text(ctx, "NOT INCLUDED", xy(2001.4), y + 90, 26, C["red"], p, MONO, True, "center")
        q = ease_io(prog(t, A("ch6", "tech") - 0.1, 1.4))
        if q > 0:
            card(ctx, 170, 300, 420, 200, C["cream"], 1, 14)
            text(ctx, "TECH STOCKS 2000-2002", 190, 334, 22, C["ink"], 0.6, MONO, True)
            pts = [(200 + j * 13.3, 360 + 110 * (j / 28) ** 0.8 + 14 * math.sin(j * 1.7)) for j in range(29)]
            n = max(2, int(len(pts) * q))
            poly(ctx, [a_ for a_, b_ in pts[:n]], [b_ for a_, b_ in pts[:n]], C["red"], 7, 1, True)
            tag(ctx, 760, 400, "ALMOST 3 YEARS DOWN", C["red"], back(prog(t, A("ch6", "years") - 0.1, 0.3)), 26, 0.04, C["white"])
    for yr in (2000, 2005, 2010, 2015, 2020, 2025):
        text(ctx, str(yr), xy(yr), y + 140, 24, C["grey"], 1, MONO, True, "center")
    tag(ctx, 680, 860, "PAST CRASHES PROMISE NOTHING", C["cream"], back(prog(t, A("ch6", "Past") - 0.1, 0.35)), 36, 0.03)


def s_verdict(ctx, t, s0, s1):
    bg_fill(ctx, (0xD9, 0xF2, 0xEA), (0xA8, 0xDD, 0xCB))
    for i in range(0, W, 90):
        rect(ctx, i, 0, 45, H, (0xFF, 0xFF, 0xFF), 0.12)
    card(ctx, 140, 220, 1140, 200, (0x0E, 0x14, 0x18), 1, 18, border=(0x5A, 0x64, 0x6B))
    heart_line(ctx, 170, 330, 1080, 80, t, C["green"])
    stamp(ctx, "A CRASH DAY IS LOUD.", "VERDICT", 700, 560, t, A("ch6", "loud") - 0.2, C["red"], 70, -0.05)
    stamp(ctx, "A YEAR LATER, IT'S USUALLY QUIET.", None, 700, 760, t, A("ch6", "quiet") - 0.3, GREEN_D, 54, 0.03)


def s_outro(ctx, t, s0, s1):
    bg_fill(ctx, (0x6F, 0xC3, 0xE6), (0xBF, 0xE6, 0xF2))
    for k in range(5):
        x = (k * 420 + t * 50) % (W + 300) - 150
        y = 300 + (k % 2) * 120
        for dx, dy, r in ((0, 0, 40), (40, -14, 48), (86, 0, 38)):
            ctx.new_path(); ctx.arc(x + dx, y + dy, r, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.92); ctx.fill()
    rect(ctx, 0, 880, W, H - 880, (0x5C, 0xA8, 0x4A))
    cases = ["RSI", "GOLDEN CROSS", "BUY THE DIP", "RSI-2", "SELL IN MAY", "MACD", "TURTLE", "OVERNIGHT", "10 BEST DAYS", "3 RED DAYS", "CRASH DAYS"]
    cf = 1 - clamp((t - A("ch7", "Next") + 0.2) / 0.3)
    if cf > 0:
        u = t - s0
        for j, nm in enumerate(cases):
            x = 1500 - u * 260 + j * 300
            if -200 < x < 1500:
                ctx.save(); ctx.translate(x, 430 + math.sin(t * 3 + j) * 8); ctx.rotate(-0.04 + 0.03 * (j % 3))
                card(ctx, -125, -75, 250, 150, C["cream"], cf, 12)
                rect(ctx, -125, -75, 110, 24, C["yellow"], cf)
                text(ctx, f"CASE #{j + 1}", -120, -56, 18, C["ink"], cf, MONO, True)
                size = 30
                while tw(ctx, nm, size) > 220:
                    size -= 2
                text(ctx, nm, 0, 22, size, C["ink"], cf, HEAD, True, "center")
                ctx.restore()
        for j, (lab, w) in enumerate((("FEES INCLUDED", "Fees"), ("LOSERS TOO", "Losers"))):
            tag(ctx, 470 + j * 360, 610, lab, C["green"] if j == 0 else C["red"], back(prog(t, A("ch7", w) - 0.1, 0.3)) * cf, 34, -0.04 + j * 0.07, None if j == 0 else C["white"])
    big_card(ctx, "STRATEGY AUTOPSY", 640, 220, back(prog(t, s0 + 0.05, 0.35)), C["ink"], C["white"], 70, -0.02)
    p = back(prog(t, A("ch7", "Next") - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(640, 420); ctx.rotate(0.02); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -440, -70, 880, 140, C["white"], 1, 18)
        text(ctx, "NEXT: TOO LATE TO BUY AT THE TOP?", 0, 16, 42, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    t_glob[0] = t
    sticker(ctx, 640, 590, "YOUR GUESS: A OR B?", back(prog(t, A("ch7", "comments") - 0.1, 0.35)), C["yellow"], 44)
    sp = back(prog(t, A("ch7", "subscribe") - 0.1, 0.35))
    if sp > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(640, 760); ctx.scale(max(sp * pulse, 1e-3), max(sp * pulse, 1e-3))
        card(ctx, -260, -60, 520, 120, C["red"], 1, 60)
        text(ctx, "SUBSCRIBE", 0, 24, 66, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    text(ctx, "STRATEGY AUTOPSY · backtests, not predictions", 640, 950, 24, C["ink"], 0.7, MONO, True, "center")
