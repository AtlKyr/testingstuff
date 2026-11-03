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


# ---------------------------------------------------------------- 1 hook
def s_hook(ctx, t, s0, s1):
    bg_fill(ctx, (0x2B, 0x12, 0x4A), (0x0C, 0x06, 0x1C))
    god_rays(ctx, W / 2, 330, t, 0.07, C["yellow"], 16, 1500)
    for k in range(40):   # drifting sparks
        x = (k * 137 + t * 70 * (1 + k % 3)) % (W + 40) - 20
        y = 360 + (k * 211 + t * 30) % 1400
        rect(ctx, x, y, 6, 6, C["yellow"], 0.25 + 0.35 * abs(math.sin(t * 3 + k)))
    # giant number slams at frame 0, rolls up 0 -> 207
    p = back(prog(t, -0.12, 0.3))
    sc = 1.0 + 0.6 * (1 - ease(prog(t, -0.05, 0.3)))
    val = NTR if t > 0.35 or t < 0.02 else NTR - int(8 * (1 - prog(t, 0.0, 0.35)))
    ctx.save(); ctx.translate(W / 2, 360); ctx.rotate(-0.04); ctx.scale(max(p * sc, 1e-3), max(p * sc, 1e-3))
    text(ctx, f"{val}", 0, 80, 260, C["white"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    tag(ctx, W / 2, 530, "TRADES", C["yellow"], back(prog(t, T["trades"] - 0.05, 0.35)), 52, 0.03)
    # SPY chart, green = in the market, grey = in cash
    box = (110, 650, 860, 340)
    a = ease(prog(t, 0.45, 0.3))
    if a > 0:
        card(ctx, box[0] - 30, box[1] - 30, box[2] + 60, box[3] + 104, (0x14, 0x18, 0x1C), a, 16, border=C["grey"])
        k = ease_io(prog(t, 0.6, 3.6))
        up = int(2 + (N - 3) * k)
        inout_chart(ctx, box, up, CLOSE.min() * 0.9, CLOSE.max() * 1.05)
        text(ctx, "SPY 2005-2024", box[0] + 10, box[1] + 26, 26, C["grey"], a, MONO, True)
        for j, (lab, col) in enumerate((("IN", C["green"]), ("OUT", GREY))):
            rect(ctx, box[0] + 470 + j * 190, box[1] + 14, 34, 12, col, a)
            text(ctx, lab + (" MARKET" if j == 0 else " (CASH)"), box[0] + 514 + j * 190, box[1] + 28, 22, C["white"], a, MONO, True)
    tag(ctx, 300, 880, "SAT OUT", GREY, back(prog(t, T["out1"] - 0.05, 0.3)), 44, -0.06)
    stamp_box(ctx, ["OUT  >  IN"], W / 2, 900, T["in1"], t, C["red"], 620, 120, -0.08)
    tag(ctx, 760, 1840, "MACD 12/26/9 · SPY", C["cream"], back(prog(t, 2.6, 0.35)), 28, 0.02)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["out1"]) else e)


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
    # patient on the table: two wavy lines crossing (MACD vs signal)
    k = ease_io(prog(t, s0 + 0.15, 1.2))
    n = 140
    m = int(n * k) + 1
    xs = [140 + i / n * 600 for i in range(m)]
    ya = [800 - 70 * math.sin(i / n * 3 * math.pi + t * 1.5) for i in range(m)]
    yb = [800 - 60 * math.sin(i / n * 3 * math.pi - 0.6 + t * 1.5) for i in range(m)]
    poly(ctx, xs, yb, C["orange"], 8, 1)
    poly(ctx, xs, ya, C["blue"], 10, 1, glow=True)
    # monitor with a moving MACD histogram
    card(ctx, 780, 420, 240, 280, (0x0E, 0x14, 0x18), 1, 12, border=C["green"])
    text(ctx, "MACD", 900, 465, 30, C["green"], 1, MONO, True, "center")
    rect(ctx, 800, 590, 200, 2, C["grey"], 0.6)
    for q in range(10):
        v = math.sin(q * 0.7 - t * 3) * 70
        col = C["green"] if v > 0 else C["red"]
        if v > 0:
            rect(ctx, 806 + q * 19, 590 - v, 14, v, col)
        else:
            rect(ctx, 806 + q * 19, 590, 14, -v, col)
    heart_line(ctx, 795, 660, 210, 22, t, C["green"], 200)
    p = back(prog(t, T["table"], 0.4))
    if p > 0:
        ctx.save(); ctx.translate(290, 1030); ctx.rotate(-0.10 + math.sin(t * 3) * 0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        ctx.new_path(); ctx.move_to(-10, -150); ctx.line_to(0, -45); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        card(ctx, -200, -45, 400, 120, (0xF2, 0xE2, 0xB0), 1, 10)
        text(ctx, "PATIENT #6", 0, -5, 26, (0x5A, 0x64, 0x6B), 1, MONO, True, "center")
        lab = "MACD CROSSOVER"
        text(ctx, lab, 0, 52, fit(ctx, lab, 46, 370), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    for j, (lab, key) in enumerate((("12", "twelve"), ("26", "t26"), ("9", "nine"))):
        tag(ctx, 600 + j * 150, 1060 + (j % 2) * 20, lab, [C["yellow"], C["green"], C["blue"]][j],
            back(prog(t, T[key] - 0.05, 0.3)), 60, -0.06 + j * 0.06)
    bunting(ctx, "STRATEGY AUTOPSY", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor")


# ---------------------------------------------------------------- 3 rules
_RA, _RB = di("2019-05-01"), di("2019-08-20")
_BUYI = di("2019-06-07") - 1   # signal bar (cross at close), fill next open
_SELLI = di("2019-07-18") - 1


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx)
    i0, i1 = _RA, _RB
    pbox = (130, 420, 820, 230); mbox = (130, 700, 820, 220)
    card(ctx, 90, 370, 900, 600, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
    k = ease_io(prog(t, s0 + 0.15, T["sell"] - s0 - 0.2))
    up = int(i0 + 1 + (i1 - i0 - 1) * k)
    seg = CLOSE[i0:i1 + 1]; vmin, vmax = seg.min() * 0.985, seg.max() * 1.01
    xs, ys = series_xy(CLOSE, i0, i1, up, pbox, vmin, vmax, 1); poly(ctx, xs, ys, C["white"], 5, 0.9)
    text(ctx, "SPY 2019", pbox[0], pbox[1] - 8, 24, C["grey"], 1, MONO, True)
    mseg = np.concatenate([MACDV[i0:i1 + 1], SIGV[i0:i1 + 1]]); mmin, mmax = mseg.min() * 1.15, mseg.max() * 1.15
    yz = sy_of(0, mmin, mmax, mbox); rect(ctx, mbox[0], yz, mbox[2], 2, C["grey"], 0.4)
    xs, ys = series_xy(SIGV, i0, i1, up, mbox, mmin, mmax, 1); poly(ctx, xs, ys, C["orange"], 6, 1)
    xs, ys = series_xy(MACDV, i0, i1, up, mbox, mmin, mmax, 1); poly(ctx, xs, ys, C["blue"], 7, 1, glow=True)
    text(ctx, "MACD", mbox[0], mbox[1] + mbox[3] + 34, 26, C["blue"], 1, MONO, True)
    text(ctx, "SIGNAL", mbox[0] + 120, mbox[1] + mbox[3] + 34, 26, C["orange"], 1, MONO, True)
    for (ii, lab, col, key) in ((_BUYI, "BUY", C["green"], "buy1"), (_SELLI, "SELL", C["red"], "sell")):
        p = back(prog(t, T[key] - 0.05, 0.35))
        if p <= 0:
            continue
        x = sx_of(ii, i0, i1, mbox); y = sy_of(MACDV[ii], mmin, mmax, mbox)
        ctx.new_path(); ctx.arc(x, y, 18 * p, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        rect(ctx, x - 2, pbox[1], 4, mbox[1] + mbox[3] - pbox[1], col, 0.5 * p)
        tag(ctx, x, pbox[1] + 40, lab, col, p, 36, -0.05, C["ink"] if col == C["green"] else C["white"])
    for j, (lab, key, col) in enumerate((("CROSS UP = BUY", "above", C["green"]), ("CROSS DOWN = SELL", "below", C["red"]))):
        p = back(prog(t, T[key] - 0.05, 0.35))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(290 + j * 500, 1080); ctx.rotate(-0.03 + j * 0.06); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -230, -55, 460, 110, C["cream"], 1, 14)
        rect(ctx, -226, -51, 22, 102, col)
        text(ctx, lab, 12, 14, fit(ctx, lab, 44, 400), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE RULES", t, s0)
    rocco(ctx, t, "lab")


# ---------------------------------------------------------------- 4 test
def s_test(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    x, y, w, h = 120, 400, 840, 380
    card(ctx, x, y, w, h, (0x0E, 0x14, 0x18), 1, 14, border=C["green"])
    for k, col in enumerate((C["red"], C["yellow"], C["green"])):
        ctx.new_path(); ctx.arc(x + 30 + k * 30, y + 30, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    cmd = "> backtest macd_12_26_9 SPY"
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
        coin(ctx, 260, 1560 - abs(math.sin((t - T["ten"]) * 4)) * 120, 60, t)
    bunting(ctx, "THE TEST", t, s0)
    rocco(ctx, t, "detective", prop=prop_magnifier)


# ---------------------------------------------------------------- 5 good news: covid crash
_CA, _CB, _CP = di("2020-02-03"), di("2020-04-30"), di("2020-02-19")


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t, 11)
    i0, i1 = _CA, _CB
    box = (130, 430, 820, 300)
    bh = BHV / BHV[_CP] * 100; sm = SIMV / SIMV[_CP] * 100
    vmin, vmax = 60, 110
    card(ctx, box[0] - 40, box[1] - 60, box[2] + 80, box[3] + 140, C["cream"], 1, 16)
    text(ctx, "COVID CRASH 2020", W / 2, box[1] - 18, 30, C["ink"], 0.75, MONO, True, "center")
    k = ease_io(prog(t, T["covid"] - 0.1, 1.6))
    up = int(i0 + 1 + (i1 - i0 - 1) * k)
    if t > T["covid"] - 0.1:
        xs, ys = series_xy(bh, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["red"], 7, 1)
        xs, ys = series_xy(sm, i0, i1, up, box, vmin, vmax, 1); poly(ctx, xs, ys, C["green"], 8, 1, glow=True)
        yy = sy_of(100, vmin, vmax, box); ctx.save(); ctx.set_dash([10, 8]); rect(ctx, box[0], yy, box[2], 2, C["ink"], 0.4); ctx.restore()
    for mm, lab in (("2020-02-03", "FEB"), ("2020-03-02", "MAR"), ("2020-04-01", "APR")):
        text(ctx, lab, sx_of(di(mm), i0, i1, box), box[1] + box[3] + 44, 26, C["ink"], 0.6, MONO, True, "center")
    a = ease_io(prog(t, T["four"] - 0.2, 0.5)); b = ease_io(prog(t, T["t34"] - 0.3, 0.6))
    if t >= T["four"] - 0.2:
        flip_counter(ctx, 60, 850, 470, 140, "MACD", f"{COV_M * a:.1f}%", C["green"], 1, 80)
    if t >= T["t34"] - 0.3:
        flip_counter(ctx, 550, 850, 470, 140, "BUY & HOLD", f"{COV_B * b:.0f}%", C["red"], 1, 80)
    tag(ctx, 300, 520, "GOOD NEWS", C["green"], back(prog(t, T["good"], 0.3)), 44, -0.06) if t < T["covid"] + 0.3 else None
    tag(ctx, 760, 690, "DODGED IT", C["yellow"], back(prog(t, T["dodged"], 0.3)), 40, 0.06) if t < T["four"] - 0.2 else None
    bunting(ctx, "GOOD NEWS", t, s0, [C["green"], C["white"], C["green"], C["yellow"]])
    rocco(ctx, t, "fire", lambda e: "smug" if (e != "talk" and t > T["four"]) else e, prop=prop_umbrella)


# ---------------------------------------------------------------- 6 drawdown
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
    a = ease_io(prog(t, T["t26b"] - 0.2, 0.6)); b = ease_io(prog(t, T["f55"] - 0.2, 0.6))
    if t >= T["t26b"] - 0.2:
        flip_counter(ctx, 60, 925, 470, 150, "MACD", f"{SIM_DDV * a:.0f}%", C["green"], 1, 80)
    if t >= T["f55"] - 0.2:
        flip_counter(ctx, 550, 925, 470, 150, "BUY & HOLD", f"{BH_DDV * b:.0f}%", C["red"], 1, 80)
    bunting(ctx, "WORST DROP", t, s0, [C["green"], C["red"], C["green"], C["red"]])
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 7 bad news: win rate
def s_bad(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x14, 0x24), (0x14, 0x06, 0x0E))
    for kk in range(30):
        x = (kk * 173 + t * 40 * (1 + kk % 3)) % (W + 40) - 20
        rect(ctx, x, 380 + (kk * 97) % 900, 6, 6, C["red"], 0.3 + 0.4 * abs(math.sin(t * 3 + kk)))
    cols, sq, gap = 18, 42, 7
    x0 = W / 2 - (cols * (sq + gap) - gap) / 2; y0 = 440
    tstart, tend = s0 + 0.25, T["f47"] - 0.1
    card(ctx, x0 - 26, y0 - 26, cols * (sq + gap) - gap + 52, 12 * (sq + gap) - gap + 52, (0x14, 0x18, 0x1C), 1, 14, border=C["grey"])
    for k, tr in enumerate(TRADES):
        tt = tstart + (tend - tstart) * k / len(TRADES)
        p = back(prog(t, tt, 0.18))
        if p <= 0:
            continue
        r_, c_ = divmod(k, cols)
        cx, cy = x0 + c_ * (sq + gap) + sq / 2, y0 + r_ * (sq + gap) + sq / 2
        s = sq * p
        rect(ctx, cx - s / 2, cy - s / 2, s, s, C["green"] if tr["r"] > 0 else C["red"])
    for j, (lab, col) in enumerate((("WIN", C["green"]), ("LOSS", C["red"]))):
        rect(ctx, x0 + j * 170, y0 + 12 * (sq + gap) + 22, 30, 30, col)
        text(ctx, lab, x0 + 44 + j * 170, y0 + 12 * (sq + gap) + 47, 28, C["white"], 1, MONO, True)
    tag(ctx, 760, 1075, "EACH SQUARE = 1 TRADE", C["cream"], back(prog(t, s0 + 0.4, 0.3)), 26, 0.03)
    q = back(prog(t, T["f47"], 0.35))
    if q > 0:
        ctx.save(); ctx.translate(W / 2, 700); ctx.rotate(-0.06); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -300, -130, 600, 260, C["cream"], 1, 20, border=C["red"])
        text(ctx, "WIN RATE", 0, -60, 40, C["ink"], 0.75, MONO, True, "center")
        text(ctx, f"{WINR:.0f}%", 0, 95, 170, C["red"], 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "THE BAD NEWS", t, s0, [C["red"], C["grey"], C["red"], C["white"]])
    rocco(ctx, t, "none", lambda e: "sad" if (e != "talk" and t > T["f47"]) else ("shock" if e != "talk" and t > T["bad"] else e))


# ---------------------------------------------------------------- 8 the twist: in cash vs invested
BASE_Y, TOP_Y = 1085, 620


def s_cash(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x14, 0x30), (0x05, 0x08, 0x14))
    for k in range(50):
        x = (k * 131) % W; y = 330 + (k * 223) % 500
        ctx.new_path(); ctx.arc(x, y, 2 + (k % 3), 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 0.85, 0.3 + 0.5 * abs(math.sin(t * 2 + k))); ctx.fill()
    ctx.new_path(); ctx.arc(900, 380, 60, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.97, 0.85, 0.9); ctx.fill()
    ctx.new_path(); ctx.arc(875, 365, 58, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0x0E, 0x14, 0x30))); ctx.fill()
    skyline(ctx, 1500, t, 5, (0x18, 0x1E, 0x34))
    rect(ctx, 0, 1500, W, H - 1500, (0x10, 0x14, 0x22))
    p = back(prog(t, s0 + 0.15, 0.35))
    if p > 0 and t < T["seven2"] + 0.05:
        ctx.save(); ctx.translate(W / 2, 450); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -420, -55, 840, 110, C["cream"], 1, 14)
        s = "SAME 20 YEARS, SPLIT IN TWO"
        text(ctx, s, 0, 16, fit(ctx, s, 46, 780), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    stamp_box(ctx, ["OUT  >  IN"], W / 2 - 40, 430, T["seven2"] + 0.05, t, C["red"], 560, 96, -0.06)
    hmax = BASE_Y - TOP_Y
    rect(ctx, 90, BASE_Y, 900, 8, C["cream"])
    bars = (("IN CASH", MOUT, T["grew"] - 0.1, T["eight"] + 0.1, (0x9A, 0xA4, 0xAA), 170, "half1"),
            ("INVESTED", MIN_, T["held"] - 0.2, T["seven2"] + 0.1, C["green"], 590, "the3"))
    for lab, mult, ta, tb, col, x, lk in bars:
        if t < T[lk] - 0.1:
            continue
        g = ease_io(prog(t, ta, max(0.3, tb - ta)))
        la = ease(prog(t, T[lk] - 0.1, 0.3))
        hh = max(6, hmax * mult / 2.9 * g)
        card(ctx, x, BASE_Y - hh, 320, hh, col, la, 10)
        if g > 0.02:
            text(ctx, f"×{1 + (mult - 1) * g:.2f}", x + 160, BASE_Y - hh - 24, 72, C["white"], la, HEAD, True, "center", outline=10, ocol=C["ink"])
        if hh > 70:
            text(ctx, lab, x + 160, BASE_Y - 26, 38, C["ink"], la, MONO, True, "center")
        if lab == "IN CASH" and g > 0.3:
            for q in range(3):   # zzz
                zz = ((t * 0.8 + q / 3) % 1)
                text(ctx, "z", x + 220 + zz * 60, BASE_Y - hh / 2 - zz * 120, 40 + q * 8, C["white"], 1 - zz, HEAD, True)
    tag(ctx, 330, 610, f"{CASHP:.0f}% OF DAYS", (0x9A, 0xA4, 0xAA), back(prog(t, T["half1"] - 0.05, 0.3)), 40, -0.05) if t < T["grew"] + 0.2 else None
    bunting(ctx, "THE TWIST", t, s0, [C["blue"], C["white"], C["blue"], C["yellow"]])
    ex = lambda e: ("shock" if t > T["seven2"] else ("sleep" if t < T["held"] else e)) if e != "talk" else e
    rocco(ctx, t, "night", ex)


# ---------------------------------------------------------------- 9 score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    card(ctx, 70, 400, 940, 720, (0x14, 0x18, 0x1C), 1, 20, border=C["yellow"])
    text(ctx, "$10,000 IN · SPY 2005-2024", W / 2, 470, 30, C["yellow"], 1, MONO, True, "center")
    a = ease_io(prog(t, T["t22"] - 0.3, 0.9)); b = ease_io(prog(t, T["s73"] - 0.5, 1.0))
    flip_counter(ctx, 110, 520, 860, 190, "MACD 12/26/9", money(10000 + (SIM_V - 10000) * a) if t >= T["t22"] - 0.4 else "—", C["red"], 1, 96)
    flip_counter(ctx, 110, 750, 860, 190, "BUY & HOLD", money(10000 + (BH_V - 10000) * b) if t >= T["buy2"] - 0.2 else "—", C["green"], 1, 96)
    box = (130, 975, 820, 120)
    k = ease_io(prog(t, s0 + 0.2, 2.8))
    up = int(1 + (N - 2) * k)
    xs, ys = series_xy(BHV, 0, N - 1, up, box, 0, 78000, 4); poly(ctx, xs, ys, C["green"], 5)
    xs, ys = series_xy(SIMV, 0, N - 1, up, box, 0, 78000, 4); poly(ctx, xs, ys, C["red"], 6, 1, glow=True)
    bunting(ctx, "FINAL SCORE", t, s0)
    rocco(ctx, t, "race", prop=prop_flag)


# ---------------------------------------------------------------- 10 years
def s_years(ctx, t, s0, s1):
    grid_bg(ctx, (0x1A, 0x2E, 0x22), (0x08, 0x12, 0x0C))
    tw_, th_, gap = 172, 112, 14
    x0 = W / 2 - (5 * tw_ + 4 * gap) / 2
    hl = ease(prog(t, T["three"], 0.3))
    for k, yr in enumerate(YEARS):
        rr_, cc = divmod(k, 5)
        p = back(prog(t, s0 + 0.15 + k * 0.05, 0.25))
        if p <= 0:
            continue
        ok = yr["m"] > yr["b"]
        cx, cy = x0 + cc * (tw_ + gap) + tw_ / 2, 420 + rr_ * (th_ + gap) + th_ / 2
        sc = p * (1 + (0.12 * hl if ok else 0))
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(sc, 1e-3), max(sc, 1e-3))
        card(ctx, -tw_ / 2, -th_ / 2, tw_, th_, C["green"] if ok else (0x5A, 0x22, 0x2C), 1, 12)
        text(ctx, str(yr["y"]), 0, -th_ / 2 + 40, 32, C["ink"] if ok else C["white"], 1, MONO, True, "center")
        if ok:
            check(ctx, -20, 26, 36, C["ink"], 1, 7)
        else:
            xmark(ctx, 0, 22, 14, C["red"], 7)
        if not ok and hl > 0:
            rrect(ctx, -tw_ / 2, -th_ / 2, tw_, th_, 12); ctx.set_source_rgba(0, 0, 0, 0.45 * hl); ctx.fill()
        ctx.restore()
    tag(ctx, 540, 965, "MACD BEAT BUY & HOLD?", C["cream"], back(prog(t, T["beat"] - 0.05, 0.3)), 34, -0.04)
    q = back(prog(t, T["three"], 0.35))
    if q > 0:
        ctx.save(); ctx.translate(300, 1085); ctx.rotate(-0.05); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -190, -70, 380, 140, C["yellow"], 1, 18)
        text(ctx, f"{BEATY} OF 20", 0, 30, 84, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "YEAR BY YEAR", t, s0, [C["green"], C["red"], C["green"], C["yellow"]])
    rocco(ctx, t, "grad", lambda e: "sad" if (e != "talk" and t > T["three"]) else e)


# ---------------------------------------------------------------- 11 fees
def hbar(ctx, y, lab, v, g, col, vmax=24000):
    x0, wmax = 90, 900
    card(ctx, x0, y, wmax, 120, (0x1B, 0x22, 0x27), 1, 12, shadow=False, border=(0x3A, 0x42, 0x48))
    w_ = max(10, (wmax - 8) * (v / vmax) * g)
    rrect(ctx, x0 + 4, y + 4, w_, 112, 10); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    text(ctx, lab, x0 + 24, y + 46, 30, C["white"], 1, MONO, True, outline=6, ocol=C["ink"])
    text(ctx, money(10000 + (v - 10000) * g) if g > 0 else "?", x0 + 24, y + 100, 46, C["white"], 1, HEAD, True, outline=8, ocol=C["ink"])


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


def s_fees(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x1A, 0x0C), (0x14, 0x08, 0x04))
    for k in range(36):   # embers rising
        x = (k * 97 + math.sin(t * 2 + k) * 30) % W
        y = H - ((k * 211 + t * (160 + (k % 4) * 60)) % (H - 300))
        rect(ctx, x, y, 7, 7, C["orange"] if k % 2 else C["yellow"], 0.35 + 0.4 * abs(math.sin(t * 4 + k)))
    a = ease(prog(t, s0 + 0.1, 0.4))
    g = ease_io(prog(t, T["twelve2"] - 0.3, 0.55))
    tag(ctx, W / 2, 420, "FEES PER SIDE", C["cream"], back(prog(t, s0 + 0.1, 0.3)), 40, -0.03)
    hbar(ctx, 500, "0.05% (OUR TEST)", FEES[0][1], a, C["blue"])
    hbar(ctx, 650, "0.20%", FEES[2][1], g, C["orange"])
    rect(ctx, 90 + 4 + (900 - 8) * 10000 / 24000, 480, 4, 310, C["white"], 0.7 * a)
    text(ctx, "START $10K", 90 + (900 - 8) * 10000 / 24000 + 14, 815, 24, C["white"], 0.8 * a, MONO, True)
    p = back(prog(t, T["seventeen"] - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 1000); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -420, -90, 840, 180, C["cream"], 1, 16, border=C["red"])
        text(ctx, "PROFIT AFTER 20 YEARS", 0, -30, 32, C["ink"], 0.75, MONO, True, "center")
        text(ctx, f"+{money(FEE_PROFIT)}", 0, 60, 92, C["red"], 1, HEAD, True, "center")
        ctx.restore()
    campfire(ctx, 800, 1790, t)
    bunting(ctx, "FEE STRESS TEST", t, s0, [C["orange"], C["red"], C["orange"], C["yellow"]])
    rocco(ctx, t, "lab", lambda e: "shock" if (e != "talk" and t > T["seventeen"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 verdict
def s_verdict(ctx, t, s0, s1):
    bg_fill(ctx, (0xD9, 0xF2, 0xEA), (0xA8, 0xDD, 0xCB))
    for i in range(0, W, 90):
        rect(ctx, (i + t * 40) % (W + 90) - 90, 0, 45, H, (0xFF, 0xFF, 0xFF), 0.12)
    cards = ((f"{SIM_DDV:.0f}% vs {BH_DDV:.0f}%", "WORST DROP", T["shield"] - 0.1, True, 285),
             (f"${SIM_V / 1000:.0f}K vs ${BH_V / 1000:.0f}K", "FINAL MONEY", T["not_"], False, 795))
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
    stamp_box(ctx, ["CRASH SHIELD.", "NOT A MONEY MACHINE."], W / 2, 960, T["machine"] + 0.1, t, C["red"], 860, 72, -0.08)
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor", lambda e: "sad" if (e != "talk" and t >= T["machine"]) else ("smug" if e != "talk" and t > T["shield"] else e))


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


SCENE_FN = {"hook": s_hook, "title": s_title, "rules": s_rules, "test": s_test, "crash": s_crash, "drawdown": s_drawdown,
            "bad": s_bad, "cash": s_cash, "score": s_score, "years": s_years, "fees": s_fees, "verdict": s_verdict, "outro": s_outro}
