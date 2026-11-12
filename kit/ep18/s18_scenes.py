# ================================================================ Autopsy #18 scenes (the 200-day line)
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
    a = ease(prog(t, SC["line"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #18", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["line"]) / (T["money2"] - SC["line"]))
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







# ---------------------------------------------------------------- race chart (Oct 2007 -> 2024, two top buyers)
XE = di("2013-12-31")



# ---------------------------------------------------------------- race chart (2005-10 -> 2016, line rule vs buy & hold)
XE = di("2016-12-30")


def race_chart(ctx, t, up, zones=(), curtain=None, a=1.0):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    for d0, d1, col, za in zones:
        x0 = sx_of(di(d0), S0, XE, RBOX); x1 = sx_of(di(d1), S0, XE, RBOX)
        rect(ctx, x0, by, max(6, x1 - x0), bh, col, za)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in (2006, 2008, 2010, 2012, 2014, 2016):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), S0, XE, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    up = max(S0 + 2, up)
    lim = curtain if curtain is not None else up
    hi = min(up, lim) + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(RV[S0:hi]), np.nanmax(BV[S0:hi]))))
    vmin = 5000.0
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    if curtain is not None:
        up = min(up, curtain)
    tips = []
    for arr, col in ((BV, HCOL), (RV, LCOL)):
        xs, ys = series_xy(arr, S0, XE, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (lx, ly) = tips
    lead_l = RV[up] > BV[up]
    off = 0 if abs(hy - ly) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_l else 0), 4, "tophat", t, "sad" if lead_l else "smug", False, True)
    mini_rocco(ctx, lx, ly - 4 - (0 if lead_l else off), 4, "race", t, "smug" if lead_l else "sad", False, True)
    if curtain is not None:
        xc = sx_of(curtain, S0, XE, RBOX) + 14
        curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    # legend inside the box, bottom-right
    for k, (lab, col) in enumerate((("THE LINE", LCOL), ("JUST HOLD", HCOL))):
        rect(ctx, bx + bw - 300, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 260, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")


def mini_chart(ctx, box, i0, i1, t, k=1.0, cash=True, a=1.0):
    """real SPY price (white) + its 200-day average (gold) for a zoomed window; IN/OUT strip under it"""
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    lo = float(np.nanmin(np.minimum(PX[i0:i1 + 1], SMA[i0:i1 + 1]))) * 0.97
    hi = float(np.nanmax(np.maximum(PX[i0:i1 + 1], SMA[i0:i1 + 1]))) * 1.03
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    if cash:
        for i in range(i0, up):
            rect(ctx, sx_of(i, i0, i1, box), by + bh + 14, bw / (i1 - i0) + 1, 22, GRNC if INN[i - 1] == 1 else (0x55, 0x5B, 0x66), 0.9)
    xs, ys = series_xy(SMA, i0, i1, up, box, lo, hi, 1)
    poly(ctx, xs, ys, LCOL, 7, a, glow=True)
    xs, ys = series_xy(PX, i0, i1, up, box, lo, hi, 1)
    poly(ctx, xs, ys, C["white"], 5, a, glow=False)
    return lo, hi


def week_candles(ctx, cx, cy, s, t, k=(1, 1, 1), labels=True):
    """the S&P's last 7 days, drawn as 3 candles: Nov 5 (-4.4%), Nov 9 (+2.35%), Nov 11 (+1.3%) — sizes ~ real moves"""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    specs = ((-160, -60, 4.4, REDC, "NOV 5"), (0, 60, 2.35, GRNC, "NOV 9"), (160, 20, 1.31, GRNC, "NOV 11"))
    for (x, y0, mv, col, lab), kk in zip(specs, k):
        if kk <= 0:
            continue
        h = mv * 42 * ease(kk)
        top = y0 - h / 2
        candle(ctx, x - 40, top, 80, h, col, 1, 26)
        if labels:
            text(ctx, lab, x, 190, 30, C["white"], 0.9, MONO, True, "center", outline=5, ocol=C["ink"])
    ctx.restore()


def evidence(ctx, cx, cy, t, a=1.0, label="THE TRAP"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "??????????", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: -4% / +2% / NOW WHAT?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x10, 0x14, 0x30), (0x03, 0x04, 0x0C))
    god_rays(ctx, W / 2, 600, t, 0.08, GOLD, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, u * 1500, 4, 40, (0x55, 0x66, 0xAA), 0.14)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(285 + shake, 500); ctx.rotate(-0.06); ctx.scale(s_, s_)
    text(ctx, "-4%", 0, 0, 196, REDC, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    s2 = s_ * (1 + 0.12 * math.sin(math.pi * prog(tl, T["jumped"] - 0.05, 0.4)))
    ctx.save(); ctx.translate(800, 520); ctx.rotate(0.06); ctx.scale(s2, s2)
    text(ctx, "+2%", 0, 0, 196, GRNC, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 790); ctx.rotate(-0.02); ctx.scale(s_, s_)
    text(ctx, "NOW WHAT?", 0, 0, fit(ctx, "NOW WHAT?", 210, 980), C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    arrow_down(ctx, 290, 650 + math.sin(t * 6) * 6, 0.32 * s_, REDC); arrow_up(ctx, 790, 640 - math.sin(t * 6) * 6, 0.32 * s_, GRNC)
    week_candles(ctx, 300, 1020, 0.62 * max(p, 1e-3), t, labels=False)
    if show_tag:
        tag(ctx, 540, 200, "THE S&P 500 · LAST 7 DAYS", C["cream"], p, 42, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 one simple line
def s_line(ctx, t, s0, s1):
    grid_bg(ctx, (0x22, 0x18, 0x40), (0x08, 0x06, 0x16))
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "ONE SIMPLE LINE", W / 2, 430, 130, GOLD, p, 960, -0.02, 16)
    k = ease_io(prog(t, s0 + 0.15, s1 - s0 - 0.3))
    mini_chart(ctx, (130, 560, 820, 360), di("2007-06-01"), di("2009-12-31"), t, k)
    if t > T["dodge"] - 0.15:
        tag(ctx, 540, 1010 - 520, "DODGES EVERY CRASH?", C["red"], back(prog(t, T["dodge"] - 0.15, 0.3)), 40, 0.03, C["white"])
    tag(ctx, 830, 600, "200-DAY AVERAGE", LCOL, back(prog(t, T["line1"], 0.3)), 28, 0.04, C["ink"])
    bunting(ctx, "THE LINE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess (race starts under the cards)
def ab_cards(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, sub, col, x, tt) in enumerate((("A", "THE LINE WINS", LCOL, -230, ta), ("B", "JUST HOLD WINS", HCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -130, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, sub.split()[0] + (" " + sub.split()[1] if len(sub.split()) > 2 else ""), 60, -12, fit(ctx, "THE LINE", 50, 230), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub.split()[-1] + "?", 60, 52, 54, C["ink"], 1, HEAD, True, "center")
        ctx.restore()


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards(ctx, t, T["A"], T["B"], 420, T["wins"])
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        up = race_idx(t, [(T["B"], S0 + 2), (SC["rules"] + 4.0, di("2007-12-31"))])
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, up, a=rc); ctx.restore()
    sticker(ctx, t, T["wins"] - 0.1, T["wins"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 the trap (evidence) — race keeps running
def s_trap(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "ONE TRAP IS HIDING...", W / 2, 425, 96, C["white"], p, 980, -0.02, 12)
    q = back(prog(t, T["chart1"] - 0.5, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    up = race_idx(t, [(SC["guess"] + 0.1, S0 + 2), (SC["rules"] + 4.0, di("2007-12-31"))])
    race_chart(ctx, t, up)
    sticker(ctx, t, T["wins"] - 0.1, T["wins"] + 2.3, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 5 rules
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("ABOVE THE LINE", "YOU'RE IN", GRNC, 290, T["above"]),
                                                 ("BELOW THE LINE", "CASH", (0xA0, 0xA6, 0xB0), 790, T["Below"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        if k == 0:
            arrow_up(ctx, -175, 0, 0.42, C["white"])
        else:
            coin(ctx, -175, 0, 48, t)
        text(ctx, title, 45, -12, fit(ctx, title, 56, 330), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 45, 62, fit(ctx, l1, 64, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    up = race_idx(t, [(SC["guess"] + 0.1, S0 + 2), (SC["rules"] + 4.0, di("2007-12-31"))])
    race_chart(ctx, t, up)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 6 2008
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["flat"] + 0.3, di("2009-06-30")), (s1, di("2009-09-30"))]
    race_chart(ctx, t, race_idx(t, pts), [("2008-01-01", "2009-03-09", C["red"], 0.18)])
    tag(ctx, 540, 440, "2008: MARKET -36%", C["red"], back(prog(t, T["thirtysix"] - 0.15, 0.3)), 50, -0.03, C["white"])
    tag(ctx, 540, 530, "THE LINE: ALMOST FLAT", LCOL, back(prog(t, T["Almost"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 7 the line leads ... then slips
def s_leads(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x2A, 0x06), (0x10, 0x0A, 0x02))
    god_rays(ctx, W / 2, 700, t, 0.10, GOLD, 16, 1500)
    pts = [(s0 + 0.1, di("2009-09-30")), (T["leads"] + 0.3, di("2014-10-20")), (T["slipping"] + 0.4, di("2015-12-31"))]
    up = race_idx(t, pts)
    cur = di("2015-12-31") if t > T["slipping"] + 0.35 else None
    race_chart(ctx, t, up, curtain=cur)
    tag(ctx, 540, 440, "6 YEARS IN THE LEAD", LCOL, back(prog(t, T["six"] - 0.15, 0.3)), 50, -0.03, C["ink"])
    if t > T["slipping"] - 0.15:
        tag(ctx, 540, 530, "...THEN IT SLIPS", C["red"], back(prog(t, T["slipping"] - 0.15, 0.3)), 44, 0.02, C["white"])
    bunting(ctx, "THE LEAD", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("sad" if t > T["slipping"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 8 remember the trap -> the whipsaw
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    for k in range(40):
        u = ((t - s0) * 0.35 + k / 40) % 1
        rect(ctx, (k * 137) % W, u * 1300, 4, 46, REDC, 0.16)
    if t < T["whipsaw"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 420, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THE TRAP?", W / 2, 570, 120, C["white"], r, 980, 0, 14)
    else:
        p = back(prog(t, T["whipsaw"] - 0.12, 0.35)); pulse = 1 + 0.04 * math.sin(t * 8)
        big_title(ctx, "THE WHIPSAW", W / 2, 470, 170, REDC, p * pulse, 980, -0.03, 18)
    k0 = ease(prog(t, s0 + 0.1, 0.4))
    week_candles(ctx, 540, 860, 1.0, t, (k0, k0, 0), labels=False)
    k3 = prog(t, T["down2"] - 0.1, 0.35)
    if k3 > 0:   # ghost candle: the move nobody knows yet
        ctx.save(); ctx.set_dash([14, 10]); rrect(ctx, 660, 860 + 20 - 100 * ease(k3), 80, 200 * ease(k3), 8)
        ctx.set_source_rgba(*rgba(REDC, 0.9)); ctx.set_line_width(6); ctx.stroke(); ctx.restore()
        text(ctx, "?", 700, 900, 90, GOLD, ease(k3), HEAD, True, "center", outline=8, ocol=C["ink"])
    for tt, lab, col, x in ((T["Down"], "DOWN", REDC, 380), (T["up"], "UP", GRNC, 540), (T["down2"], "DOWN AGAIN?", REDC, 730)):
        if t > tt - 0.1:
            q = back(prog(t, tt - 0.1, 0.3))
            text(ctx, lab, x, 1090, 44 * max(q, 0.01), col, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    text(ctx, "NOV 5         NOV 9", 460, 1150, 26, C["white"], 0.8 * k0, MONO, True, "center")
    bunting(ctx, "THE TRAP", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["whipsaw"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 9 41 fakeouts (real 2015 whipsaw zoom + trade dots)
W0, W1 = di("2015-06-25"), di("2015-12-30")


def s_fakeouts(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x0A, 0x14), (0x06, 0x02, 0x05))
    k = ease_io(prog(t, s0 + 0.1, 2.2))
    mini_chart(ctx, (130, 365, 820, 210), W0, W1, t, k)
    lab = "2015: IN, OUT, IN, OUT..." if t < T["within"] - 0.1 else "IN & OUT WITHIN 2 WEEKS"
    text(ctx, lab, 540, 690, 34, C["white"], ease(prog(t, s0 + 0.3, 0.3)), MONO, True, "center", outline=6, ocol=C["ink"])
    # 64 trade dots, 8 x 8
    nt = len(FAKE) + 23
    fk = [i for i in range(nt) if i % 3 != 2][:len(FAKE)]
    lost_set = set(fk[:len(FAKE_LOST)])
    on1 = prog(t, T["Fortyone"] - 0.1, 1.2); on2 = prog(t, T["lost"] - 0.1, 0.9)
    for i in range(nt):
        cx = 205 + (i % 8) * 96; cy = 745 + (i // 8) * 42
        col = (0x55, 0x5B, 0x66)
        if i in fk and on1 * len(fk) > fk.index(i):
            col = LCOL
            if i in lost_set and on2 * len(lost_set) > sorted(lost_set).index(i):
                col = REDC
        ctx.new_path(); ctx.arc(cx, cy, 16, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
    if t < T["lost"] - 0.1:
        tag(ctx, 540, 1120, "41 FAKEOUTS", LCOL, back(prog(t, T["Fortyone"] - 0.1, 0.3)), 52, -0.03, C["ink"])
    else:
        tag(ctx, 540, 1120, "MOST LOST MONEY", REDC, back(prog(t, T["lost"] - 0.1, 0.3)), 52, 0.03, C["white"])
    bunting(ctx, "FAKEOUTS", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("sad" if t > T["lost"] else "shock") if e != "talk" else e)


# ---------------------------------------------------------------- 10 2020
C0, C1 = di("2020-01-02"), di("2020-08-31")


def s_covid(ctx, t, s0, s1):
    bg_fill(ctx, (0x0B, 0x10, 0x2A), (0x02, 0x03, 0x0A))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    big_title(ctx, "THE 2020 CRASH", W / 2, 440, 110, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
    box = (130, 520, 820, 380)
    k = ease_io(prog(t, s0 + 0.1, max(1.0, T["bounce"] - s0)))
    lo, hi = mini_chart(ctx, box, C0, C1, t, k)
    ish = di("2020-02-28"); ibk = di("2020-05-28"); ilo = di("2020-03-23")
    for i, lab, col, tt, dy in ((ish, "SOLD", REDC, T["sold"], -70), (ilo, "BOTTOM", C["white"], T["crash2"], 70), (ibk, "BACK IN", GRNC, T["bought"], -90)):
        if t > tt - 0.1:
            x = sx_of(i, C0, C1, box); y = box[1] + box[3] - (PX[i] - lo) / (hi - lo) * box[3]
            q = back(prog(t, tt - 0.1, 0.3))
            ctx.new_path(); ctx.arc(x, y, 14 * max(q, 1e-3), 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
            tag(ctx, min(max(x, 200), 880), y + dy, lab, col, q, 32, 0.0, C["ink"] if col != REDC else C["white"])
    bunting(ctx, "OUT & BACK IN", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("shock" if t > T["bounce"] else "sleep") if e != "talk" else e)


# ---------------------------------------------------------------- 11 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -42, 900, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"WORST DROP: LINE {MDD_L:.0f}%  ·  HOLD {MDD_B:.0f}%"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 860, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · OCT 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · THE 200-DAY LINE (0.05% FEES)", money(LINE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · JUST HOLDING", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["Way"] - 0.15, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["LESS THAN HALF", "THE PAIN."], W / 2, 470, T["Less"] - 0.05, t, STAMP_GR, 860, 76, -0.05)
    stamp_box(ctx, ["WAY LESS MONEY."], W / 2 + 10, 740, T["Way"] - 0.05, t, C["red"], 860, 84, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["Way"] - 0.15, "right", y=1085)
    fb = back(prog(t, T["Way"] + 0.15, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1085); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #19", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "line": s_line, "guess": s_guess, "trap": s_trap, "rules": s_rules, "crash": s_crash, "leads": s_leads,
            "remember": s_remember, "fakeouts": s_fakeouts, "covid": s_covid, "score": s_score, "verdict": s_verdict, "loop": s_loop}
