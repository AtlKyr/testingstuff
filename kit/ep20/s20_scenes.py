# ================================================================ Autopsy #20 scenes (yields spike)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD
PCOL = (0xFF, 0x6B, 0x3D)    # PANIC SELLER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x1C, 0x10, 0x3A), (0x05, 0x03, 0x10)
RBOX = (110, 620, 860, 320)
LCOL = (0xFF, 0xA8, 0x1E)    # THE 200-DAY LINE rule
STAMP_OR, STAMP_GR = (0xD0, 0x50, 0x00), (0x0B, 0x8A, 0x4C)


def candle(ctx, x, y, w, h, col, a=1.0, wick=40):
    rect(ctx, x + w / 2 - 4, y - wick, 8, h + 2 * wick, C["ink"], a)
    card(ctx, x, y, w, h, col, a, 8, shadow=False, border=C["ink"])


def arrow_up(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.new_path()
    ctx.move_to(0, -90); ctx.line_to(70, -10); ctx.line_to(28, -10); ctx.line_to(28, 80); ctx.line_to(-28, 80); ctx.line_to(-28, -10)
    ctx.line_to(-70, -10); ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke(); ctx.restore()


def arrow_down(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.pi); arrow_up(ctx, 0, 0, s, col, a); ctx.restore()


def sticker(ctx, t, t0, t1, kind, y=1085):
    """comment prompt sticker (visual only). kind: 'guess' or 'right'. Captions sit at ~1240."""
    if not (t0 - 0.01 <= t <= t1):
        return
    p = back(prog(t, t0, 0.35)) * (1 - ease(prog(t, t1 - 0.25, 0.25)))
    if p <= 0:
        return
    wob = 1 + 0.03 * math.sin(t * 9)
    ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.035); ctx.scale(max(p * wob, 1e-3), max(p * wob, 1e-3))
    if kind == "guess":
        card(ctx, -440, -62, 880, 124, GOLD, 1, 26, border=C["ink"])
        text(ctx, "COMMENT YOUR GUESS", -395, 22, 58, C["ink"], 1, HEAD, True, "left")
        bob = math.sin(t * 10) * 8
        ctx.save(); ctx.translate(205, bob); arrow_down(ctx, 0, 0, 0.36, C["red"]); ctx.restore()
        card(ctx, 255, -42, 160, 84, C["ink"], 1, 18, shadow=False)
        text(ctx, "A or B?", 335, 16, 40, C["white"], 1, HEAD, True, "center")
    else:
        card(ctx, -470, -62, 940, 124, C["white"], 1, 26, border=C["ink"])
        text(ctx, "WERE YOU RIGHT?", -430, 22, 54, C["ink"], 1, HEAD, True, "left")
        card(ctx, 30, -40, 70, 80, GRNC, 1, 14, shadow=False, border=C["ink"]); check(ctx, 46, 2, 38, C["ink"], 1, 10)
        text(ctx, "/", 122, 22, 50, C["ink"], 1, HEAD, True, "center")
        card(ctx, 145, -40, 70, 80, C["red"], 1, 14, shadow=False, border=C["ink"]); xmark(ctx, 180, 0, 18, C["white"], 9)
        text(ctx, "IN THE", 330, -6, 30, C["ink"], 1, TAGF, False, "center")
        text(ctx, "COMMENTS", 330, 30, 34, C["ink"], 1, TAGF, False, "center")
    ctx.restore()


def race_idx(t, pts):
    if t <= pts[0][0]:
        return max(1, pts[0][1])
    for (a, ia), (b, ib) in zip(pts, pts[1:]):
        if t <= b:
            return int(ia + (ib - ia) * ease_io((t - a) / max(1e-3, b - a)))
    return pts[-1][1]


def hourglass(ctx, cx, cy, s, t):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.sin(t * 1.5) * 0.15)
    ctx.scale(s, s)
    rect(ctx, -90, -150, 180, 20, (0x8B, 0x5A, 0x2B)); rect(ctx, -90, 130, 180, 20, (0x8B, 0x5A, 0x2B))
    for sgn in (-1, 1):
        ctx.new_path(); ctx.move_to(-70, sgn * 130); ctx.line_to(70, sgn * 130); ctx.line_to(8, 0); ctx.line_to(-8, 0); ctx.close_path()
        ctx.set_source_rgba(0.85, 0.95, 1, 0.35); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(6); ctx.stroke()
    f = (t * 0.35) % 1
    ctx.new_path(); ctx.move_to(-70 * (1 - f), -130 * (1 - f)); ctx.line_to(70 * (1 - f), -130 * (1 - f)); ctx.line_to(6, -6); ctx.line_to(-6, -6); ctx.close_path()
    ctx.set_source_rgba(*rgba(GOLD)); ctx.fill()
    hh = 130 * f
    ctx.new_path(); ctx.move_to(-70 * f - 10, 130); ctx.line_to(70 * f + 10, 130); ctx.line_to(0, 130 - hh); ctx.close_path(); ctx.fill()
    rect(ctx, -3, -6, 6, 136, GOLD)
    ctx.restore()



def big_title(ctx, s, x, y, size, col, p, maxw=980, rot=0.0, outline=14):
    if p <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    text(ctx, s, 0, 0, fit(ctx, s, size, maxw), col, 1, HEAD, True, "center", outline=outline, ocol=C["ink"])
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["point"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #20", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["point"]) / (T["flip"] - SC["point"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])



def curtain_box(ctx, t, xc, top, right, hh, label="CLASSIFIED"):
    ctx.save(); ctx.rectangle(xc, top, right - xc, hh); ctx.clip()
    rect(ctx, xc, top, right - xc, RBOX[3] + 60, (0x05, 0x05, 0x05))
    for j in range(16):
        ctx.save(); ctx.translate(xc + j * 60 - 40, top); ctx.rotate(0.6)
        rect(ctx, 0, 0, 22, 70, GOLD, 0.9); ctx.restore()
    cx = (xc + right) / 2
    text(ctx, label, cx, top + 200, fit(ctx, label, 60, right - xc - 20), C["red"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])
    qs = 1 + 0.1 * math.sin(t * 7)
    ctx.save(); ctx.translate(cx, top + 360); ctx.scale(qs, qs)
    text(ctx, "?", 0, 0, 160, GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"]); ctx.restore()
    ctx.restore()

LCOL = (0xFF, 0x8A, 0x3D)   # YIELD RULE (orange)
YCOL = (0xFF, 0x5C, 0x5C)   # yield line


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2006, 2008, 2010, 2012, 2014)):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 2, up)
    if curtain is not None:
        up = min(up, curtain)
    for i0, i1 in ZONES:   # cash zones of the yield rule (only up to the visible point)
        if i0 > up:
            break
        x0 = sx_of(i0, S0, xe, RBOX); x1 = sx_of(min(i1, up), S0, xe, RBOX)
        rect(ctx, x0, by, max(3, x1 - x0), bh, LCOL, 0.22 * a)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), S0, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(RV[S0:hi]), np.nanmax(BV[S0:hi]))))
    vmin = 5000.0
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    tips = []
    for arr, col in ((BV, HCOL), (RV, LCOL)):
        xs, ys = series_xy(arr, S0, xe, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (lx, ly) = tips
    lead_l = RV[up] > BV[up] + 1
    off = 0 if abs(hy - ly) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_l else 0), 4, "tophat", t, "sad" if lead_l else "smug", False, True)
    mini_rocco(ctx, lx, ly - 4 - (0 if lead_l else off), 4, "race", t, "smug" if lead_l else "sad", False, True)
    if curtain is not None:
        xc = sx_of(curtain, S0, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("YIELD RULE", LCOL), ("JUST HOLD", HCOL))):
        rect(ctx, bx + bw - 300, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 260, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + bh - 60, 30, 18, LCOL, 0.35)
    text(ctx, "= IN CASH", bx + 60, by + bh - 45, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2014-12-31"); XE2 = N - 1
YR2 = (2006, 2010, 2014, 2018, 2022)


def yield_gauge(ctx, cx, cy, s, t, val=5.0, a=1.0):
    """a pressure gauge with the needle in the red at ~5%"""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 150, math.pi, 2 * math.pi); ctx.close_path()
    ctx.set_source_rgba(*rgba((0x0C, 0x10, 0x1C), a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(10); ctx.stroke()
    for k, col in enumerate((GRNC, GOLD, REDC)):
        ctx.new_path(); ctx.arc(0, 0, 118, math.pi + k * math.pi / 3, math.pi + (k + 1) * math.pi / 3)
        ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(30); ctx.stroke()
    ang = math.pi + math.pi * (0.86 + 0.04 * math.sin(t * 9))
    ctx.new_path(); ctx.move_to(0, 0); ctx.line_to(math.cos(ang) * 120, math.sin(ang) * 120)
    ctx.set_source_rgba(*rgba(C["white"], a)); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 18, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: 5% / SELL?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x14), (0x08, 0x02, 0x06))
    god_rays(ctx, W / 2, 560, t, 0.09, REDC, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, 1500 - u * 1500, 4, 40, (0xFF, 0x80, 0x80), 0.14)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(470 + shake, 560); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "5%", 0, 0, 380, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    arrow_up(ctx, 860, 430 - math.sin(t * 6) * 10, 0.55 * s_, REDC)
    ctx.save(); ctx.translate(540, 800); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "SELL?", 0, 0, 230, C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    yield_gauge(ctx, 300, 1060, 0.75 * max(p, 1e-3), t)
    if show_tag:
        tag(ctx, 540, 200, "10-YEAR TREASURY YIELD", C["cream"], p, 44, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 up a full point in a year
def s_point(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x10, 0x18), (0x0A, 0x04, 0x08))
    big_title(ctx, "+1 POINT IN 1 YEAR", W / 2, 420, 120, GOLD, back(prog(t, T["full1"] - 0.2, 0.3)), 960, -0.02, 16)
    base = 1080
    for k, (lab, v, col, x, tt) in enumerate((("NOV 2025", NEWS_YAGO, C["grey"], 330, s0 + 0.05), ("NOV 2026", NEWS_NOW, REDC, 750, T["point1"] - 0.2))):
        g = ease(prog(t, tt, 0.6))
        if g <= 0:
            continue
        h = (v - 3.0) * 230 * g
        card(ctx, x - 120, base - h, 240, h, col, 1, 14, border=C["ink"])
        text(ctx, f"{v:.2f}%", x, base - h - 30, 66, C["white"], 1, MONO, True, "center", outline=8, ocol=C["ink"])
        text(ctx, lab, x, base + 50, 34, C["white"], 0.9, MONO, True, "center", outline=5, ocol=C["ink"])
    if t > T["point1"]:
        arrow_up(ctx, 540, 820 - math.sin(t * 8) * 8, 0.4, GOLD)
    bunting(ctx, "10-YEAR YIELD", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 the question
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "SELL STOCKS", W / 2, 470, 170, C["white"], back(prog(t, T["sell1"] - 0.2, 0.3)), 980, -0.03, 18)
    big_title(ctx, "WHEN YIELDS SPIKE?", W / 2, 640, 120, REDC, back(prog(t, T["yields"] - 0.2 if "yields" in T else T["spike"] - 0.3, 0.3)), 980, 0.02, 14)
    yield_gauge(ctx, 760, 960, 0.9, t, a=ease(prog(t, s0, 0.4)))
    bunting(ctx, "THE QUESTION", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 4 guess (race starts under the cards)
def ab_cards(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "SELL &", "HIDE?", LCOL, -230, ta), ("B", "JUST", "HOLD?", HCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -130, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, -12, 56, C["ink"], 1, HEAD, True, "center")
        text(ctx, l2, 60, 52, 56, C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["rules"] + 3.5, di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards(ctx, t, T["A"], T["B"], 420, T["hold"])
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["hold"] - 0.1, T["hold"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 5 the clue: one year
def evidence(ctx, cx, cy, t, a=1.0, label="THE YEAR"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "20??", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE YEAR IS HIDING...", W / 2, 425, 96, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["year2"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["hold"] - 0.1, T["hold"] + 2.3, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 6 rules
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("YIELD +1 PT IN A YEAR", "GO TO CASH", LCOL, 290, T["jumps"]),
                                                 ("OTHERWISE", "OWN THE S&P", GRNC, 790, T["cash1"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        if k == 0:
            coin(ctx, -175, 0, 48, t)
        else:
            arrow_up(ctx, -175, 0, 0.42, C["white"])
        text(ctx, title, 45, -12, fit(ctx, title, 56, 330), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 45, 62, fit(ctx, l1, 64, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 7 2008
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["everyone"] + 0.2, di("2009-03-09")), (s1, di("2009-09-30"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "2008: YIELDS FELL", C["blue"], back(prog(t, T["fell"] - 0.15, 0.3)), 50, -0.03, C["white"])
    tag(ctx, 540, 530, f"RULE STAYED IN: {_R['y2008'][0]:.0f}%", C["red"], back(prog(t, T["crashed"] - 0.15, 0.3)), 44, 0.02, C["white"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 8 2013: sold, missed the rally
def s_y2013(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x2A, 0x06), (0x10, 0x0A, 0x02))
    god_rays(ctx, W / 2, 700, t, 0.08, GOLD, 16, 1500)
    pts = [(s0 + 0.1, di("2009-09-30")), (T["sells"], di("2013-07-05")), (T["rally1"] + 0.3, di("2014-03-31"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE1, curtain=di("2014-03-31") if t > T["rally1"] else None)
    tag(ctx, 540, 440, "2013: YIELDS JUMP - SOLD", LCOL, back(prog(t, T["sells"] - 0.15, 0.3)), 46, -0.03, C["ink"])
    if t > T["less"] - 0.15:
        tag(ctx, 540, 530, "LESS THAN HALF THE RALLY", C["red"], back(prog(t, T["less"] - 0.15, 0.3)), 42, 0.02, C["white"])
    bunting(ctx, "2013", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("sad" if t > T["less"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 9 remember that one year -> 2022, yields exploded
Y0, Y1 = di("2021-10-01"), di("2022-12-30")


def yield_chart(ctx, box, i0, i1, k, a=1.0):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    lo, hi = 0.0, 5.0
    for lv in (1, 2, 3, 4):
        yy = by + bh - lv / hi * bh
        rect(ctx, bx, yy, bw, 2, C["white"], 0.1)
        text(ctx, f"{lv}%", bx - 8, yy + 8, 22, C["white"], 0.6, MONO, True, "right")
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    xs, ys = series_xy(YLD, i0, i1, up, box, lo, hi, 1)
    poly(ctx, xs, ys, YCOL, 9, a, glow=True)
    for yr in (2022,):
        text(ctx, "JAN 2022", sx_of(di("2022-01-03"), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    text(ctx, "DEC 2022", sx_of(i1, i0, i1, box) - 40, by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    return xs[-1], ys[-1]


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    for k in range(40):
        u = ((t - s0) * 0.35 + k / 40) % 1
        rect(ctx, (k * 137) % W, u * 1300, 4, 46, REDC, 0.16)
    if t < T["twentytwo"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 420, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT ONE YEAR?", W / 2, 570, 110, C["white"], r, 980, 0, 14)
    else:
        p = back(prog(t, T["twentytwo"] - 0.12, 0.35)); pulse = 1 + 0.04 * math.sin(t * 8)
        big_title(ctx, "2022", W / 2, 600, 220, REDC, p * pulse, 980, -0.03, 20)
        k = ease_io(prog(t, T["Yields"] if "Yields" in T else T["exploded"] - 0.4, 1.4))
        if k > 0:
            ex, ey = yield_chart(ctx, (150, 680, 780, 300), Y0, Y1, k)
            if t > T["exploded"]:
                tag(ctx, 420, 700, "YIELDS EXPLODED", REDC, back(prog(t, T["exploded"], 0.3)), 44, 0.03, C["white"])
    bunting(ctx, "THE ONE YEAR", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["twentytwo"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 2022: -7% vs -19%
def s_y2022(ctx, t, s0, s1):
    bg_fill(ctx, (0x0B, 0x10, 0x2A), (0x02, 0x03, 0x0A))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    big_title(ctx, "2022", W / 2, 430, 130, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
    base = 640
    for k, (lab, v, col, x, tt) in enumerate((("YIELD RULE", _R["y2022"][0], LCOL, 330, T["seven"]), ("JUST HOLD", _R["y2022"][1], HCOL, 750, T["nineteen"]))):
        g = ease(prog(t, tt - 0.15, 0.6))
        text(ctx, lab, x, base - 30, 40, col, 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        if g <= 0:
            card(ctx, x - 120, base, 240, 200, (0x05, 0x05, 0x05), 1, 14, border=C["grey"])
            text(ctx, "?", x, base + 150, 140, GOLD, 0.6 + 0.4 * abs(math.sin(t * 5)), HEAD, True, "center", outline=8, ocol=C["ink"])
            continue
        h = -v * 19 * g
        card(ctx, x - 120, base, 240, h, col, 1, 14, border=C["ink"])
        text(ctx, f"{v:.0f}%", x, base + h + 80, 80, C["red"], 1, MONO, True, "center", outline=8, ocol=C["ink"])
    if t > T["hid"] - 0.1:
        tag(ctx, 330, 1160 - 40, "IN CASH", LCOL, back(prog(t, T["hid"] - 0.1, 0.3)), 36, -0.04, C["ink"])
    bunting(ctx, "WHO LOST LESS?", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("smug" if t > T["nineteen"] else "sleep") if e != "talk" else e)


# ---------------------------------------------------------------- 11 almost caught up -> 2023 out again
def s_caught(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    pts = [(s0 + 0.05, di("2021-12-31")), (T["up2"] + 0.2, di("2022-12-30")), (T["Then"] + 0.1, di("2022-12-30")), (T["rally2"] + 0.3, di("2023-12-29"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE2, curtain=up + 1, years=YR2)
    tag(ctx, 540, 440, "ALMOST CAUGHT UP", GOLD, back(prog(t, T["almost"] - 0.15, 0.3)), 50, -0.03, C["ink"])
    if t > T["out"] - 0.15:
        tag(ctx, 540, 530, "2023: OUT AGAIN - HALF THE RALLY", C["red"], back(prog(t, T["out"] - 0.15, 0.3)), 38, 0.02, C["white"])
    bunting(ctx, "THE COMEBACK?", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("sad" if t > T["out"] else "smug") if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 12 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"TRIGGER +0.5 PT: {money(VAR['0.5'])}  ·  +1.25 PT: {money(VAR['1.25'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2006 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · YIELD RULE (+1 PT, 0.05% FEES)", money(RULE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · JUST HOLDING", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 13 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["NUDGE THE TRIGGER..."], W / 2, 470, T["Nudge"] - 0.05, t, STAMP_OR, 860, 76, -0.05)
    stamp_box(ctx, ["THE WINNER CAN FLIP."], W / 2 + 10, 700, T["winner"] - 0.1, t, C["red"], 860, 80, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["trigger"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1180 - 330); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #21", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "point": s_point, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules,
            "crash": s_crash, "y2013": s_y2013, "remember": s_remember, "y2022": s_y2022, "caught": s_caught,
            "score": s_score, "verdict": s_verdict, "loop": s_loop}
