# ================================================================ Autopsy #6 scenes (MACD 12/26/9)
def fit(ctx, s, size, maxw, f=HEAD):
    while tw(ctx, s, size, f) > maxw and size > 10:
        size -= 2
    return size


def xmark(ctx, x, y, s, col, w=9):
    ctx.new_path(); ctx.move_to(x - s, y - s); ctx.line_to(x + s, y + s); ctx.move_to(x + s, y - s); ctx.line_to(x - s, y + s)
    ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def stamp_box(ctx, lines, x, y, t0, t, col, w=820, size=78, rot=-0.1):
    sk = prog(t, t0, 0.3)
    if sk <= 0:
        return
    sc = 2.2 - 1.2 * ease(sk); a = clamp(sk * 2)
    h = 70 + len(lines) * size * 1.1
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    rrect(ctx, -w / 2, -h / 2, w, h, 14); ctx.set_source_rgba(*rgba(C["cream"], 0.95 * a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(10); ctx.stroke()
    for k, ln in enumerate(lines):
        sz = fit(ctx, ln, size, w - 60)
        text(ctx, ln, 0, -h / 2 + 35 + size * 0.9 + k * size * 1.1, sz, col, a, HEAD, True, "center")
    ctx.restore()


def cloud(ctx, x, y, s, col=(0xFF, 0xFF, 0xFF), a=0.92):
    for dx, dy, r in ((0, 0, 40), (40, -14, 48), (86, 0, 38)):
        ctx.new_path(); ctx.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def sun(ctx, cx, cy, r, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 0.6)
    for k in range(12):
        ctx.save(); ctx.rotate(k * math.pi / 6)
        rect(ctx, r + 12, -9, 34 + 10 * math.sin(t * 4 + k), 18, C["yellow"], a)
        ctx.restore()
    ctx.restore()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0xFF, 0xD2, 0x4A), a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()


def pop_card(ctx, x, y, w, h, fill, p, rot=0.0, border=None):
    """returns True if drawn; leaves ctx translated (caller must restore)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -w / 2, -h / 2, w, h, fill, 1, 16, border=border)


GREY = (0x9A, 0xA4, 0xAA)


def inout_chart(ctx, box, upto, vmin, vmax, w_in=7, w_out=5):
    """SPY price line + IN/OUT barcode strip under it (green = MACD in the market, grey = in cash)"""
    xs, ys = series_xy(CLOSE, 0, N - 1, upto, box, vmin, vmax, 2)
    poly(ctx, xs, ys, C["white"], 5, 0.9)
    sy, sh = box[1] + box[3] + 14, 44
    i = 0
    while i < upto:
        j = i
        while j + 1 < upto and POSV[j + 1] == POSV[i]:
            j += 1
        x0_ = box[0] + i / (N - 1) * box[2]; x1_ = box[0] + (j + 1) / (N - 1) * box[2]
        rect(ctx, x0_, sy, max(1.0, x1_ - x0_), sh, C["green"] if POSV[i] > 0 else (0x9A, 0xA4, 0xAA))
        i = j + 1

# ---------------------------------------------------------------- 11 fees
def campfire(ctx, cx, cy, t):
    for k in range(5):   # bills falling into the fire
        u = ((t * 0.55 + k / 5) % 1)
        x = cx - 140 + k * 70 + math.sin(t * 3 + k) * 30
        y = cy - 520 + u * 440
        ctx.save(); ctx.translate(x, y); ctx.rotate(math.sin(t * 4 + k) * 0.6)
        card(ctx, -46, -24, 92, 48, (0x8F, 0xD1, 0x8B), 1 - u * 0.7, 6, shadow=False, border=(0x2E, 0x6B, 0x34))
        text(ctx, "$", 0, 13, 34, (0x2E, 0x6B, 0x34), 1 - u * 0.7, HEAD, True, "center")
        ctx.restore()
    for k in range(4):
        rect(ctx, cx - 170 + k * 20, cy + 10 - k * 6, 300 - k * 40, 26, (0x6B, 0x3E, 0x1E))
    for k, (col, sc) in enumerate(((C["red"], 1.0), (C["orange"], 0.75), (C["yellow"], 0.45))):
        ctx.new_path(); ctx.move_to(cx - 170 * sc, cy + 10)
        for q in range(9):
            xx = cx - 170 * sc + (q + 0.5) * 340 * sc / 9
            hh = (150 + 90 * math.sin(t * 9 + q * 1.7 + k)) * sc * (1.3 if q in (3, 4, 5) else 0.9)
            ctx.line_to(xx, cy - hh); ctx.line_to(cx - 170 * sc + (q + 1) * 340 * sc / 9, cy + 10)
        ctx.close_path(); ctx.set_source_rgba(*rgba(col, 0.95)); ctx.fill()
    text(ctx, "FEES", cx, cy + 90, 40, C["yellow"], 0.9, MONO, True, "center")



# ================================================================ Autopsy #7 scenes (Turtle 20/10 breakout)
SHELL, SHELL_D, SKIN = (0x3F, 0x9E, 0x4E), (0x2A, 0x6E, 0x36), (0x9C, 0xD6, 0x6A)


def turtle(ctx, cx, cy, s, t, hide=0.0, walk=0.0, a=1.0, flip=False):
    """generic cartoon turtle (original drawing). hide 0..1 pulls head+legs into the shell; walk animates legs."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s * (-1 if flip else 1), s)
    out = 1 - hide
    for k, lx in enumerate((-70, -25, 30, 72)):           # legs
        sw = math.sin(t * 10 + k * 1.6) * 10 * walk
        rrect(ctx, lx - 16 + sw, 20 + 30 * hide, 32, 40 * out + 6, 10); ctx.set_source_rgba(*rgba(SKIN, a)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(5); ctx.stroke()
    hx = 120 * out + 40 * hide; hy = -10 + math.sin(t * 3) * 4 * out
    ctx.new_path(); ctx.arc(hx, hy, 36, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(SKIN, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(5); ctx.stroke()
    if out > 0.3:
        ctx.new_path(); ctx.arc(hx + 12, hy - 8, 7, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
        ctx.new_path(); ctx.arc(hx + 14, hy - 10, 2.5, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, a); ctx.fill()
    ctx.new_path(); ctx.move_to(-110, 20); ctx.curve_to(-105, -110, 105, -110, 110, 20); ctx.close_path()   # shell dome
    ctx.set_source_rgba(*rgba(SHELL, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke()
    for px_, py_ in ((-50, -20), (0, -45), (50, -20), (0, 5)):
        ctx.new_path()
        for q in range(6):
            an = q * math.pi / 3
            (ctx.move_to if q == 0 else ctx.line_to)(px_ + math.cos(an) * 24, py_ + math.sin(an) * 18)
        ctx.close_path(); ctx.set_source_rgba(*rgba(SHELL_D, a)); ctx.fill()
    rrect(ctx, -118, 12, 236, 22, 10); ctx.set_source_rgba(*rgba((0xD9, 0xC2, 0x6A), a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def label_card(ctx, x, y, w, h, top, big, col, p, rot=0.0, bigcol=None):
    if p <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -w / 2, -h / 2, w, h, C["cream"], 1, 16)
    rect(ctx, -w / 2 + 4, -h / 2 + 4, 20, h - 8, col)
    text(ctx, top, 10, -h / 2 + 52, fit(ctx, top, 56, w - 70), bigcol or col, 1, HEAD, True, "center", outline=6, ocol=C["ink"])
    text(ctx, big, 10, h / 2 - 30, fit(ctx, big, 34, w - 70, MONO), C["ink"], 1, MONO, True, "center")
    ctx.restore()


# ---------------------------------------------------------------- 1 hook
def s_hook(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x3A, 0x2A), (0x05, 0x12, 0x0C))
    god_rays(ctx, W / 2, 380, t, 0.08, C["green"], 16, 1500)
    for k in range(40):
        x = (k * 137 + t * 70 * (1 + k % 3)) % (W + 40) - 20
        y = 360 + (k * 211 + t * 30) % 1400
        rect(ctx, x, y, 6, 6, C["yellow"], 0.25 + 0.35 * abs(math.sin(t * 3 + k)))
    # giant multiplier slams at frame 0 (pop starts at t=-0.12 so frame 0 is not blank)
    p = back(prog(t, -0.12, 0.3)); sc = 1.0 + 0.6 * (1 - ease(prog(t, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    ctx.save(); ctx.translate(W / 2, 330); ctx.rotate(-0.05); ctx.scale(max(p * sc * wob, 1e-3), max(p * sc * wob, 1e-3))
    text(ctx, f"{WL_RATIO:.1f}x", 0, 90, 270, C["green"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    tag(ctx, W / 2, 500, "WINNERS vs LOSERS", C["yellow"], back(prog(t, T["twice"] - 0.05, 0.35)), 46, 0.03)
    # avg win vs avg loss bars
    box_y, base = 590, 810
    a = ease(prog(t, 0.2, 0.3))
    if a > 0:
        card(ctx, 140, box_y, 800, 380, (0x10, 0x16, 0x14), a, 18, border=C["grey"])
        rect(ctx, 180, base, 720, 4, C["grey"], a)
        for j, (lab, v, col, tt, x) in enumerate((("AVG WIN", AVG_WIN, C["green"], T["winners"], 260),
                                                  ("AVG LOSS", AVG_LOSS, C["red"], T["losers"], 600))):
            g = ease_io(prog(t, tt - 0.05, 0.45))
            if g <= 0:
                continue
            hh = abs(v) / 4.5 * 170 * g
            if v > 0:
                card(ctx, x, base - hh, 220, hh, col, 1, 8, shadow=False)
                text(ctx, f"+{v * g:.1f}%", x + 110, base - hh - 18, 54, C["white"], 1, MONO, True, "center", outline=6, ocol=C["ink"])
            else:
                card(ctx, x, base + 4, 220, hh, col, 1, 8, shadow=False)
                text(ctx, f"{v * g:.1f}%", x + 110, base - 18, 54, C["white"], 1, MONO, True, "center", outline=6, ocol=C["ink"])
            text(ctx, lab, x + 110, box_y + 360, 26, C["grey"], 1, MONO, True, "center")
    # the trading book
    q = back(prog(t, T["book"] - 0.1, 0.35))
    if q > 0 and t < T["crushed"] + 0.25:
        ctx.save(); ctx.translate(W / 2 + 120, 1070); ctx.rotate(0.05 + math.sin(t * 2) * 0.02); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -300, -95, 600, 190, (0x7A, 0x2E, 0x2E), 1, 10)
        card(ctx, -285, -85, 280, 170, C["cream"], 1, 6, shadow=False); card(ctx, 5, -85, 280, 170, C["cream"], 1, 6, shadow=False)
        text(ctx, "LET WINNERS", -145, -25, 34, C["ink"], 1, HEAD, True, "center"); text(ctx, "RUN", -145, 30, 52, C["green"], 1, HEAD, True, "center", outline=5, ocol=C["ink"])
        text(ctx, "CUT LOSERS", 145, -25, 34, C["ink"], 1, HEAD, True, "center"); text(ctx, "SHORT", 145, 30, 52, C["red"], 1, HEAD, True, "center", outline=5, ocol=C["ink"])
        ctx.restore()
    stamp_box(ctx, ["STILL CRUSHED."], W / 2, 980, T["crushed"], t, C["red"], 720, 110, -0.08)
    tag(ctx, 740, 1840, "TURTLE BREAKOUT · SPY", C["cream"], back(prog(t, 2.0, 0.35)), 28, 0.02)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["crushed"]) else ("smug" if e != "talk" and t > T["book"] else e))


# ---------------------------------------------------------------- 2 title
def s_title(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x5E, 0x5E), (0x0C, 0x2A, 0x2C))
    for i in range(0, W, 120):
        rect(ctx, i, 0, 3, H, C["white"], 0.06)
    for j in range(0, H, 120):
        rect(ctx, 0, j, W, 3, C["white"], 0.06)
    god_rays(ctx, W / 2, 330, t * 0.4, 0.07, C["white"], 12, 900)
    card(ctx, 110, 880, 860, 70, (0xC8, 0xD2, 0xD6), 1, 12)
    rect(ctx, 180, 950, 26, 190, (0x7A, 0x86, 0x8C)); rect(ctx, 874, 950, 26, 190, (0x7A, 0x86, 0x8C))
    hide = 1 - ease(prog(t, T["turtle1"] - 0.1, 0.35))
    turtle(ctx, 430, 820, 1.5, t, hide=hide)
    card(ctx, 780, 420, 240, 280, (0x0E, 0x14, 0x18), 1, 12, border=C["green"])
    text(ctx, "VITALS", 900, 465, 30, C["green"], 1, MONO, True, "center")
    for q in range(8):
        v = 30 + abs(math.sin(q * 0.9 + t * 2.5)) * 90
        rect(ctx, 806 + q * 24, 610 - v, 16, v, C["green"] if q % 3 else C["yellow"])
    heart_line(ctx, 795, 660, 210, 22, t, C["green"], 200)
    p = back(prog(t, T["table"], 0.4))
    if p > 0:
        ctx.save(); ctx.translate(300, 1060); ctx.rotate(-0.08 + math.sin(t * 3) * 0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        ctx.new_path(); ctx.move_to(-10, -120); ctx.line_to(0, -45); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        card(ctx, -200, -45, 400, 120, (0xF2, 0xE2, 0xB0), 1, 10)
        text(ctx, "PATIENT #7", 0, -5, 26, (0x5A, 0x64, 0x6B), 1, MONO, True, "center")
        lab = "TURTLE BREAKOUT"
        text(ctx, lab, 0, 52, fit(ctx, lab, 46, 370), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    q = back(prog(t, T["breakout"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(780, 1070); ctx.rotate(0.05); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -195, -55, 390, 110, C["yellow"], 1, 14)
        ctx.new_path(); ctx.move_to(-175, 25); ctx.line_to(-148, -25); ctx.line_to(-121, 25); ctx.close_path(); ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()
        text(ctx, "NEW HIGHS", 35, 16, fit(ctx, "NEW HIGHS", 46, 290), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "STRATEGY AUTOPSY", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor")


# ---------------------------------------------------------------- 3 rules
_RA, _RB = di("2023-03-01"), di("2023-08-25")
_BUYI = di("2023-05-01") - 1   # breakout close (signal), fill next open
_SELLI = di("2023-08-03") - 1


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx)
    i0, i1 = _RA, _RB
    box = (130, 430, 820, 430)
    card(ctx, 90, 370, 900, 560, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
    k = ease_io(prog(t, s0 + 0.15, T["sell"] - s0 - 0.2))
    up = int(i0 + 1 + (i1 - i0 - 1) * k)
    seg = np.concatenate([CLOSE[i0:i1 + 1], HH[i0:i1 + 1], LL[i0:i1 + 1]]); vmin, vmax = seg.min() * 0.99, seg.max() * 1.01
    xs, ys = series_xy(HH, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["green"], 5, 0.85)
    xs, ys = series_xy(LL, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["red"], 5, 0.85)
    xs, ys = series_xy(CLOSE, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["white"], 6, 1, glow=True)
    text(ctx, "SPY 2023", box[0], box[1] - 12, 24, C["grey"], 1, MONO, True)
    text(ctx, "20-DAY HIGH", box[0] + 300, box[1] - 12, 24, C["green"], 1, MONO, True)
    text(ctx, "10-DAY LOW", box[0] + 560, box[1] - 12, 24, C["red"], 1, MONO, True)
    for (ii, lab, col, key) in ((_BUYI, "BUY", C["green"], "buy1"), (_SELLI, "SELL", C["red"], "sell")):
        p = back(prog(t, T[key] - 0.05, 0.35))
        if p <= 0:
            continue
        x = sx_of(ii, i0, i1, box); y = sy_of(CLOSE[ii], vmin, vmax, box)
        rect(ctx, x - 2, box[1], 4, box[3], col, 0.5 * p)
        ctx.new_path(); ctx.arc(x, y, 20 * p, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        tag(ctx, x, box[1] + box[3] - 30 if lab == "BUY" else box[1] + 40, lab, col, p, 38, -0.05, C["ink"] if col == C["green"] else C["white"])
    label_card(ctx, 290, 1060, 440, 170, "BUY", "close > 20d high", C["green"], back(prog(t, T["above"] - 0.05, 0.35)), -0.03)
    label_card(ctx, 790, 1060, 440, 170, "SELL", "close < 10d low", C["red"], back(prog(t, T["below"] - 0.05, 0.35)), 0.03)
    bunting(ctx, "THE RULES", t, s0)
    rocco(ctx, t, "lab")


# ---------------------------------------------------------------- 4 test
def s_test(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    x, y, w, h = 120, 400, 840, 380
    card(ctx, x, y, w, h, (0x0E, 0x14, 0x18), 1, 14, border=C["green"])
    for k, col in enumerate((C["red"], C["yellow"], C["green"])):
        ctx.new_path(); ctx.arc(x + 30 + k * 30, y + 30, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    cmd = "> backtest turtle_20_10 SPY"
    nch = int(len(cmd) * prog(t, s0 + 0.05, 0.8))
    text(ctx, cmd[:nch] + ("_" if int(t * 3) % 2 == 0 and nch < len(cmd) else ""), x + 26, y + 100, 34, C["green"], 1, MONO, True)
    for k, ln in enumerate([f"{N:,} trading days, 2005-2024", "warm-up bars skipped", "next-open fills, 0.05% fees", "running... done."]):
        la = prog(t, s0 + 0.7 + k * 0.3, 0.2)
        if la > 0:
            text(ctx, ln, x + 26, y + 160 + k * 50, 28, (0xB8, 0xC4, 0xCC), la, MONO, False)
    for k, (lab, tt) in enumerate((("20 YEARS", T["twenty"]), ("$10,000 START", T["ten"]), ("FEES INCLUDED", T["fees1"]))):
        p = back(prog(t, tt, 0.35))
        if p > 0:
            ctx.save(); ctx.translate(W / 2 - 60 + k * 60, 880 + k * 105); ctx.rotate(-0.03 + k * 0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
            card(ctx, -300, -44, 600, 88, C["cream"], 1, 12)
            ctx.new_path(); ctx.arc(-245, 0, 28, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"])); ctx.fill()
            check(ctx, -260, 2, 30, C["ink"], 1, 7)
            text(ctx, lab, 20, 15, 44, C["ink"], 1, HEAD, True, "center")
            ctx.restore()
    if t >= T["ten"]:
        coin(ctx, 200, 1560 - abs(math.sin((t - T["ten"]) * 4)) * 120, 60, t)
    bunting(ctx, "THE TEST", t, s0)
    rocco(ctx, t, "race", prop=prop_flag)


# ---------------------------------------------------------------- 5 stats: 85 trades, win rate
def s_stats(ctx, t, s0, s1):
    grid_bg(ctx, (0x12, 0x30, 0x22), (0x06, 0x12, 0x0C))
    cols, sq, gap = 17, 44, 9
    x0 = W / 2 - (cols * (sq + gap) - gap) / 2; y0 = 440
    rows = math.ceil(len(TRADES) / cols)
    card(ctx, x0 - 26, y0 - 26, cols * (sq + gap) - gap + 52, rows * (sq + gap) - gap + 110, (0x14, 0x18, 0x1C), 1, 14, border=C["grey"])
    tstart, tend = s0 + 0.15, T["trades"] + 0.4
    for k, tr in enumerate(TRADES):
        p = back(prog(t, tstart + (tend - tstart) * k / len(TRADES), 0.18))
        if p <= 0:
            continue
        r_, c_ = divmod(k, cols)
        cx, cy = x0 + c_ * (sq + gap) + sq / 2, y0 + r_ * (sq + gap) + sq / 2
        s = sq * p * (1 + 0.15 * math.sin(t * 5 + k) * (1 if t > T["f56"] and tr["r"] > 0 else 0))
        rect(ctx, cx - s / 2, cy - s / 2, s, s, C["green"] if tr["r"] > 0 else C["red"])
    ly = y0 + rows * (sq + gap) + 40
    for j, (lab, col) in enumerate((("WIN", C["green"]), ("LOSS", C["red"]))):
        rect(ctx, x0 + j * 170, ly - 22, 28, 28, col)
        text(ctx, lab, x0 + 42 + j * 170, ly, 26, C["white"], 1, MONO, True)
    text(ctx, "1 SQUARE = 1 TRADE", x0 + cols * (sq + gap) - gap, ly, 24, C["grey"], 1, MONO, True, "right")
    tag(ctx, 300, 400, f"{NTR} TRADES", C["yellow"], back(prog(t, T["e85"] - 0.05, 0.35)), 46, -0.05)
    q = back(prog(t, T["f56"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(W / 2 + 60, 1000); ctx.rotate(-0.05); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -280, -110, 560, 220, C["cream"], 1, 20, border=C["green"])
        text(ctx, "WIN RATE", 0, -50, 36, C["ink"], 0.75, MONO, True, "center")
        text(ctx, f"{WINR:.1f}%", 0, 80, 140, C["green"], 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "THE RESULTS", t, s0, [C["green"], C["yellow"], C["green"], C["white"]])
    rocco(ctx, t, "grad", lambda e: "smug" if (e != "talk" and t > T["f56"]) else e)


# ---------------------------------------------------------------- 6 covid crash
_CA, _CB, _CP = di("2020-02-03"), di("2020-04-30"), di("2020-02-19")


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t, 11)
    i0, i1 = _CA, _CB
    box = (130, 430, 820, 300)
    bh = BHV / BHV[_CP] * 100; sm = SIMV / SIMV[_CP] * 100
    vmin, vmax = 60, 110
    card(ctx, box[0] - 40, box[1] - 60, box[2] + 80, box[3] + 140, C["cream"], 1, 16)
    text(ctx, "COVID CRASH 2020", W / 2, box[1] - 18, 30, C["ink"], 0.75, MONO, True, "center")
    k = ease_io(prog(t, s0 + 0.1, 1.6))
    up = int(i0 + 1 + (i1 - i0 - 1) * k)
    xs, ys = series_xy(bh, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["red"], 7, 1)
    xs, ys = series_xy(sm, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["green"], 8, 1, glow=True)
    yy = sy_of(100, vmin, vmax, box); rect(ctx, box[0], yy, box[2], 2, C["ink"], 0.4)
    for mm, lab in (("2020-02-03", "FEB"), ("2020-03-02", "MAR"), ("2020-04-01", "APR")):
        text(ctx, lab, sx_of(di(mm), i0, i1, box), box[1] + box[3] + 44, 26, C["ink"], 0.6, MONO, True, "center")
    a = ease_io(prog(t, T["four"] - 0.2, 0.5)); b = ease_io(prog(t, T["t34"] - 0.3, 0.6))
    if t >= T["four"] - 0.2:
        flip_counter(ctx, 60, 850, 470, 140, "TURTLE", f"{COV_M * a:.1f}%", C["green"], 1, 80)
    if t >= T["t34"] - 0.3:
        flip_counter(ctx, 550, 850, 470, 140, "BUY & HOLD", f"{COV_B * b:.0f}%", C["red"], 1, 80)
    bunting(ctx, "COVID CRASH", t, s0, [C["red"], C["white"], C["red"], C["yellow"]])
    rocco(ctx, t, "fire", lambda e: "smug" if (e != "talk" and t > T["four"]) else e, prop=prop_umbrella)


# ---------------------------------------------------------------- 7 drawdown
def s_drawdown(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x14, 0x1C), (0x12, 0x08, 0x0C))
    box = (110, 450, 860, 360)
    card(ctx, box[0] - 30, box[1] - 70, box[2] + 60, box[3] + 140, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
    text(ctx, "DROP FROM THE PEAK", W / 2, box[1] - 22, 28, C["grey"], 1, MONO, True, "center")
    k = ease_io(prog(t, s0 + 0.15, 1.4))
    up = int(1 + (N - 2) * k)
    xs, ys = series_xy(BH_DD, 0, N - 1, up, box, -60, 0, 3)
    ctx.new_path(); ctx.move_to(box[0], box[1])
    for x_, y_ in zip(xs, ys):
        ctx.line_to(x_, y_)
    ctx.line_to(xs[-1], box[1]); ctx.close_path(); ctx.set_source_rgba(*rgba(C["red"], 0.45)); ctx.fill()
    poly(ctx, xs, ys, C["red"], 4)
    xs, ys = series_xy(SIM_DD, 0, N - 1, up, box, -60, 0, 3)
    poly(ctx, xs, ys, C["green"], 6, 1, glow=True)
    for yr in (2005, 2010, 2015, 2020, 2024):
        i = max(0, di(f"{yr}-01-01"))
        text(ctx, str(yr), sx_of(i, 0, N - 1, box), box[1] + box[3] + 44, 24, C["grey"], 0.9, MONO, True, "center")
    for v in (-20, -40):
        yy = sy_of(v, -60, 0, box); rect(ctx, box[0], yy, box[2], 2, C["white"], 0.15)
        text(ctx, f"{v}%", box[0] + 6, yy - 8, 20, C["grey"], 0.8, MONO, True)
    a = ease_io(prog(t, T["t27"] - 0.2, 0.6)); b = ease_io(prog(t, T["f55"] - 0.2, 0.6))
    if t >= T["t27"] - 0.2:
        flip_counter(ctx, 60, 925, 470, 150, "TURTLE", f"{SIM_DDV * a:.0f}%", C["green"], 1, 80)
    if t >= T["f55"] - 0.2:
        flip_counter(ctx, 550, 925, 470, 150, "BUY & HOLD", f"{BH_DDV * b:.0f}%", C["red"], 1, 80)
    bunting(ctx, "WORST DROP", t, s0, [C["green"], C["red"], C["green"], C["red"]])
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 8 the catch
def s_catch(ctx, t, s0, s1):
    bg_fill(ctx, (0x34, 0x10, 0x3A), (0x0E, 0x04, 0x12))
    for k in range(14):   # floating question marks
        x = (k * 157 + t * 60 * (1 + k % 2)) % (W + 80) - 40
        y = 380 + (k * 113 + math.sin(t * 2 + k) * 40) % 760
        text(ctx, "?", x, y, 40 + (k % 3) * 20, C["purple"], 0.35, HEAD, True, "center")
    speed_lines(ctx, t)
    big_card(ctx, "THE CATCH?", W / 2, 470, back(prog(t, T["catch"] - 0.05, 0.35)), C["yellow"], C["ink"], 100, -0.05)
    # turtle hides in its shell, waits for a breakout
    hide = 0.3 + 0.7 * ease(prog(t, T["only"], 0.4))
    turtle(ctx, W / 2 + 60 + math.sin(t * 1.5) * 20, 850, 1.7, t, hide=hide)
    if hide > 0.8:
        for q in range(3):
            zz = ((t * 0.8 + q / 3) % 1)
            text(ctx, "z", W / 2 + 200 + zz * 60, 760 - zz * 120, 40 + q * 8, C["white"], 1 - zz, HEAD, True)
    q = back(prog(t, T["breakouts"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(W / 2 + 40, 1080); ctx.rotate(0.03); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -380, -60, 760, 120, C["cream"], 1, 14, border=C["red"])
        s = "ONLY BUYS BREAKOUTS"
        text(ctx, s, 0, 18, fit(ctx, s, 58, 700), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE CATCH", t, s0, [C["purple"], C["yellow"], C["purple"], C["white"]])
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["breakouts"]) else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 9 rebound: bought back 3 weeks late
_RBA, _RBB = di("2020-02-19"), di("2020-05-08")


def s_rebound(ctx, t, s0, s1):
    grid_bg(ctx, (0x1C, 0x16, 0x34), (0x08, 0x06, 0x14))
    i0, i1 = _RBA, _RBB
    box = (140, 440, 800, 440)
    card(ctx, box[0] - 50, box[1] - 60, box[2] + 100, box[3] + 150, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
    text(ctx, "SPY 2020", box[0], box[1] - 18, 26, C["grey"], 1, MONO, True)
    seg = BHV[i0:i1 + 1]; vmin, vmax = seg.min() * 0.95, seg.max() * 1.03
    k = ease_io(prog(t, s0 + 0.1, T["weeks"] - s0 + 0.3))
    up = int(i0 + 1 + (i1 - i0 - 1) * k)
    # shade the cash period low -> buy
    if t > T["three"] - 0.1:
        xa = sx_of(COV_LOW_I, i0, i1, box); xb = sx_of(COV_BUY_I, i0, i1, box)
        g = ease(prog(t, T["three"] - 0.1, 0.4))
        rect(ctx, xa, box[1], (xb - xa) * g, box[3], C["grey"], 0.25)
        text(ctx, "IN CASH", (xa + xb) / 2, box[1] + 40, 26, C["white"], g, MONO, True, "center")
    xs, ys = series_xy(BHV, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["white"], 6, 1, glow=True)
    for mm, lab in (("2020-03-02", "MAR"), ("2020-04-01", "APR"), ("2020-05-01", "MAY")):
        text(ctx, lab, sx_of(di(mm), i0, i1, box), box[1] + box[3] + 44, 26, C["grey"], 0.8, MONO, True, "center")
    p = back(prog(t, T["low2"] - 0.05, 0.35))
    if p > 0:
        x = sx_of(COV_LOW_I, i0, i1, box); y = sy_of(BHV[COV_LOW_I], vmin, vmax, box)
        ctx.new_path(); ctx.arc(x, y, 18 * p, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["red"])); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        tag(ctx, x - 20, y + 50, "THE LOW", C["red"], p, 32, -0.05)
    p = back(prog(t, T["weeks"] - 0.05, 0.35))
    if p > 0:
        x = sx_of(COV_BUY_I, i0, i1, box); y = sy_of(BHV[COV_BUY_I], vmin, vmax, box)
        ctx.new_path(); ctx.arc(x, y, 18 * p, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"])); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        tag(ctx, x + 60, y - 60, "TURTLE BUYS", C["green"], p, 32, 0.04, C["ink"])
    q = back(prog(t, T["three"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(300, 1060); ctx.rotate(-0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -230, -70, 460, 140, C["cream"], 1, 16)
        clock(ctx, -160, 0, 48, t, 3.0)
        text(ctx, "3 WEEKS", 55, 22, 60, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    big_card(ctx, f"+{REBOUND:.0f}%", 790, 1050, back(prog(t, T["t24"] - 0.05, 0.35)), C["red"], C["white"], 96, 0.05)
    if t > T["t24"] + 0.3:
        text(ctx, "ALREADY MISSED", 790, 1155, 28, C["white"], ease(prog(t, T["t24"] + 0.3, 0.3)), MONO, True, "center", outline=6, ocol=C["ink"])
    bunting(ctx, "LATE TO THE PARTY", t, s0, [C["purple"], C["red"], C["purple"], C["yellow"]])
    rocco(ctx, t, "none", lambda e: "sad" if (e != "talk" and t > T["t24"]) else e)


# ---------------------------------------------------------------- 10 sat in cash
def s_cash(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x14, 0x30), (0x05, 0x08, 0x14))
    for k in range(50):
        x = (k * 131) % W; y = 330 + (k * 223) % 500
        ctx.new_path(); ctx.arc(x, y, 2 + (k % 3), 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 0.85, 0.3 + 0.5 * abs(math.sin(t * 2 + k))); ctx.fill()
    ctx.new_path(); ctx.arc(930, 1420, 60, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.97, 0.85, 0.9); ctx.fill()
    ctx.new_path(); ctx.arc(905, 1405, 58, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0x0E, 0x14, 0x30))); ctx.fill()
    skyline(ctx, 1560, t, 5, (0x18, 0x1E, 0x34))
    rect(ctx, 0, 1560, W, H - 1560, (0x10, 0x14, 0x22))
    # 20-year IN/OUT barcode
    box = (110, 470, 860, 230)
    a = ease(prog(t, s0 + 0.1, 0.3))
    card(ctx, box[0] - 30, box[1] - 70, box[2] + 60, box[3] + 150, (0x14, 0x18, 0x1C), a, 16, border=C["grey"])
    k = ease_io(prog(t, s0 + 0.2, T["cash"] - s0 + 0.2))
    inout_chart(ctx, box, int(2 + (N - 3) * k), CLOSE.min() * 0.9, CLOSE.max() * 1.05)
    for j, (lab, col) in enumerate((("IN MARKET", C["green"]), ("IN CASH", GREY))):
        rect(ctx, box[0] + 10 + j * 260, box[1] - 38, 34, 14, col, a)
        text(ctx, lab, box[0] + 54 + j * 260, box[1] - 24, 24, C["white"], a, MONO, True)
    tag(ctx, 540, 900, f"{CASHP:.0f}% OF DAYS IN CASH", (0x9A, 0xA4, 0xAA), back(prog(t, T["half2"] - 0.05, 0.3)), 40, -0.04)
    # market multiplier while the Turtle was in cash
    if t > T["market2"] - 0.15:
        g = ease_io(prog(t, T["market2"] - 0.1, T["doubled"] - T["market2"] + 0.3))
        la = ease(prog(t, T["market2"] - 0.15, 0.25))
        card(ctx, 90, 980, 900, 150, (0x1B, 0x22, 0x27), la, 14, shadow=False, border=(0x3A, 0x42, 0x48))
        wmax = 880; w_ = max(20, wmax * (1 + (MOUT - 1) * g) / 2.4)
        rrect(ctx, 100, 990, w_, 130, 12); ctx.set_source_rgba(*rgba(C["yellow"], la)); ctx.fill()
        text(ctx, "SPY WHILE TURTLE WAITED", 120, 1036, 26, C["ink"], la, MONO, True)
        text(ctx, f"x{1 + (MOUT - 1) * g:.2f}", 120, 1104, 64, C["ink"], la, HEAD, True)
    ex = lambda e: ("shock" if t > T["doubled"] else ("sleep" if t < T["market2"] else e)) if e != "talk" else e
    bunting(ctx, "WAITING IN CASH", t, s0, [C["blue"], C["white"], C["blue"], C["yellow"]])
    rocco(ctx, t, "night", ex)


# ---------------------------------------------------------------- 11 score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    card(ctx, 70, 400, 940, 720, (0x14, 0x18, 0x1C), 1, 20, border=C["yellow"])
    text(ctx, "$10,000 IN · SPY 2005-2024", W / 2, 470, 30, C["yellow"], 1, MONO, True, "center")
    a = ease_io(prog(t, T["thirty"] - 0.3, 0.9)); b = ease_io(prog(t, T["s71"] - 0.5, 1.0))
    flip_counter(ctx, 110, 520, 860, 190, "TURTLE 20/10", money(10000 + (SIM_V - 10000) * a) if t >= T["thirty"] - 0.4 else "?", C["red"], 1, 96)
    flip_counter(ctx, 110, 750, 860, 190, "BUY & HOLD", money(10000 + (BH_V - 10000) * b) if t >= T["s71"] - 0.6 else "?", C["green"], 1, 96)
    box = (130, 975, 820, 120)
    k = ease_io(prog(t, s0 + 0.2, 2.8))
    up = int(1 + (N - 2) * k)
    xs, ys = series_xy(BHV, 0, N - 1, up, box, 0, 78000, 4); poly(ctx, xs, ys, C["green"], 5)
    xs, ys = series_xy(SIMV, 0, N - 1, up, box, 0, 78000, 4); poly(ctx, xs, ys, C["red"], 6, 1, glow=True)
    bunting(ctx, "FINAL SCORE", t, s0)
    rocco(ctx, t, "party", lambda e: "sad" if (e != "talk" and t > T["s71"] + 0.4) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 the original 55/20 version
def s_original(ctx, t, s0, s1):
    bg_fill(ctx, (0x5A, 0x44, 0x26), (0x26, 0x1A, 0x0C))
    for i in range(0, W, 90):
        rect(ctx, i, 0, 2, H, (0xF2, 0xE2, 0xB0), 0.07)
    for k in range(30):   # dust
        x = (k * 173 + t * 30 * (1 + k % 3)) % W
        rect(ctx, x, 380 + (k * 97) % 900, 5, 5, (0xF2, 0xE2, 0xB0), 0.2 + 0.3 * abs(math.sin(t * 2 + k)))
    p = back(prog(t, s0 + 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 480); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -400, -70, 800, 140, C["cream"], 1, 14, border=(0x8A, 0x5A, 0x10))
        text(ctx, "THE ORIGINAL TURTLE RULE", 0, -12, fit(ctx, "THE ORIGINAL TURTLE RULE", 46, 740), C["ink"], 1, HEAD, True, "center")
        text(ctx, "55-day high in · 20-day low out", 0, 42, 28, (0x8A, 0x5A, 0x10), 1, MONO, True, "center")
        ctx.restore()
    tag(ctx, 260, 655, "55-DAY", C["yellow"], back(prog(t, T["f55b"] - 0.05, 0.35)), 56, -0.06, C["ink"])
    q = back(prog(t, T["seventeen"] - 0.1, 0.35))
    g = ease_io(prog(t, T["seventeen"] - 0.1, 0.9))
    q = max(q, 0.0) if t >= T["seventeen"] - 0.1 else ease(prog(t, s0 + 0.3, 0.3))
    if q > 0:
        ctx.save(); ctx.translate(W / 2, 830); ctx.rotate(0.03); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        flip_counter(ctx, -400, -95, 800, 190, "$10,000 BECAME", money(10000 + (V55 - 10000) * g) if t >= T["seventeen"] - 0.1 else "?", C["red"], 1, 100)
        ctx.restore()
    # a slow turtle crawls across
    tx = -200 + (t - s0) * 210
    turtle(ctx, tx, 1080, 0.75, t, walk=1.0)
    bunting(ctx, "THE ORIGINAL", t, s0, [C["yellow"], (0x8A, 0x5A, 0x10), C["yellow"], C["cream"]])
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["seventeen"]) else e)


# ---------------------------------------------------------------- 13 fees
def hbar(ctx, y, lab, v, g, col, vmax=34000):
    x0, wmax = 90, 900
    card(ctx, x0, y, wmax, 120, (0x1B, 0x22, 0x27), 1, 12, shadow=False, border=(0x3A, 0x42, 0x48))
    w_ = max(10, (wmax - 8) * (v / vmax) * g)
    rrect(ctx, x0 + 4, y + 4, w_, 112, 10); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    text(ctx, lab, x0 + 24, y + 46, 30, C["white"], 1, MONO, True, outline=6, ocol=C["ink"])
    text(ctx, money(10000 + (v - 10000) * g) if g > 0 else "?", x0 + 24, y + 100, 46, C["white"], 1, HEAD, True, outline=8, ocol=C["ink"])


def s_fees(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x1A, 0x0C), (0x14, 0x08, 0x04))
    for k in range(36):
        x = (k * 97 + math.sin(t * 2 + k) * 30) % W
        y = H - ((k * 211 + t * (160 + (k % 4) * 60)) % (H - 300))
        rect(ctx, x, y, 7, 7, C["orange"] if k % 2 else C["yellow"], 0.35 + 0.4 * abs(math.sin(t * 4 + k)))
    a = ease(prog(t, s0 + 0.1, 0.4))
    g = ease_io(prog(t, T["t23"] - 0.3, 0.7))
    tag(ctx, W / 2, 420, "FEES PER SIDE", C["cream"], back(prog(t, s0 + 0.1, 0.3)), 40, -0.03)
    hbar(ctx, 500, "0.05% (OUR TEST)", FEES[0][1], a, C["blue"])
    hbar(ctx, 650, "0.20% PER SIDE", FEES[2][1], g, C["orange"])
    sx = 90 + 4 + (900 - 8) * 10000 / 34000
    rect(ctx, sx, 480, 4, 310, C["white"], 0.7 * a)
    text(ctx, "START $10K", sx + 14, 815, 24, C["white"], 0.8 * a, MONO, True)
    p = back(prog(t, T["side"], 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 930); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -380, -60, 760, 120, C["cream"], 1, 14, border=C["orange"])
        s_ = "SAME TRADES. PRICIER FILLS."
        text(ctx, s_, 0, 16, fit(ctx, s_, 50, 700), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    campfire(ctx, 800, 1790, t)
    bunting(ctx, "FEE STRESS TEST", t, s0, [C["orange"], C["red"], C["orange"], C["yellow"]])
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["t23"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 14 verdict
def s_verdict(ctx, t, s0, s1):
    bg_fill(ctx, (0xD9, 0xF2, 0xEA), (0xA8, 0xDD, 0xCB))
    for i in range(0, W, 90):
        rect(ctx, (i + t * 40) % (W + 90) - 90, 0, 45, H, (0xFF, 0xFF, 0xFF), 0.12)
    cards = ((f"{SIM_DDV:.0f}% vs {BH_DDV:.0f}%", "WORST DROP", T["verdict"] + 0.1, True, 285),
             (f"${SIM_V / 1000:.0f}K vs ${BH_V / 1000:.0f}K", "FINAL MONEY", T["verdict"] + 0.45, False, 795))
    for k, (lab, sub, tt, ok, x) in enumerate(cards):
        p = back(prog(t, tt, 0.35))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(x, 560); ctx.rotate(-0.04 + k * 0.08); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -230, -170, 460, 340, C["cream"], 1, 18)
        text(ctx, lab, 0, -40, fit(ctx, lab, 72, 410), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub, 0, 20, 28, C["ink"], 0.7, MONO, True, "center")
        ctx.new_path(); ctx.arc(0, 100, 46, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"] if ok else C["red"])); ctx.fill()
        if ok:
            check(ctx, -22, 102, 46, C["ink"], 1, 9)
        else:
            xmark(ctx, 0, 100, 20, C["ink"], 9)
        ctx.restore()
    stamp_box(ctx, ["GREAT SEATBELT."], W / 2, 880, T["seatbelt"], t, C["green"], 760, 80, -0.06)
    stamp_box(ctx, ["SLOW ENGINE."], W / 2 + 30, 1060, T["slow"], t, C["red"], 680, 84, 0.04)
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor", lambda e: "sad" if (e != "talk" and t >= T["slow"]) else ("smug" if e != "talk" and t > T["seatbelt"] else e))
# ---------------------------------------------------------------- 13 outro
def s_outro(ctx, t, s0, s1):
    bg_fill(ctx, (0x6F, 0xC3, 0xE6), (0xBF, 0xE6, 0xF2))
    for k in range(4):
        x = (k * 310 + t * 50) % (W + 300) - 150
        cloud(ctx, x, 420 + (k % 2) * 160, 1.0)
    sun(ctx, 120, 320, 50, t)
    rect(ctx, 0, 1460, W, H - 1460, (0x5C, 0xA8, 0x4A))
    p = back(prog(t, s0 + 0.15, 0.4))
    if p > 0:
        ctx.save(); ctx.translate(W / 2 + 100, 740); ctx.rotate(0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -360, -230, 720, 460, (0x2A, 0x1A, 0x2E), 1, 18, border=C["yellow"])
        text(ctx, "FULL VIDEO ON THE CHANNEL", 0, -170, 30, C["yellow"], 1, MONO, True, "center")
        for j, (lab, col) in enumerate((("RSI", C["red"]), ("GOLDEN X", C["yellow"]), ("DIP", C["blue"]))):
            xx = -230 + j * 230
            card(ctx, xx - 95, -120, 190, 230, C["cream"], 1, 12, border=col)
            rect(ctx, xx - 91, -116, 182, 50, col)
            text(ctx, lab, xx, -80, 28, C["ink"] if col == C["yellow"] else C["white"], 1, HEAD, True, "center")
            text(ctx, "?", xx, 70, 110, col, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        text(ctx, "WHO WON? · 8 MIN", 0, 180, 40, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    fb = back(prog(t, T["follow"] + 0.1, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2 + 120, 1110); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -230, -55, 460, 110, C["red"], 1, 55)
        text(ctx, "FOLLOW", 0, 22, 62, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    text(ctx, "STRATEGY AUTOPSY", W / 2 + 120, 1220, 30, C["ink"], 0.85, MONO, True, "center")
    text(ctx, "my backtest · not financial advice", W / 2 + 120, 1260, 22, C["ink"], 0.6, MONO, False, "center")
    bunting(ctx, "NEXT AUTOPSY?", t, s0)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "title": s_title, "rules": s_rules, "test": s_test, "stats": s_stats, "crash": s_crash, "drawdown": s_drawdown,
            "catch": s_catch, "rebound": s_rebound, "cash": s_cash, "score": s_score, "original": s_original, "fees": s_fees,
            "verdict": s_verdict, "outro": s_outro}
