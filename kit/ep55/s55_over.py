

# ================================================================ #55 overrides (sell a -5% week, buy back after a +5% week)
LCOL = (0xFF, 0x7A, 0x2E)      # SELL & WAIT (orange)
HCOL = (0x4F, 0xC3, 0xF7)      # BUY & HOLD (blue)
CASHC = (0xFF, 0xB0, 0x40)
XE1 = di("2011-12-30")


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #55", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["Verd"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2007, 2009, 2011), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = 0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    j = s0_                                # orange bands = in cash
    while j <= up:
        if not INN[j]:
            k = j
            while k <= up and not INN[k]:
                k += 1
            x1 = sx_of(j, s0_, xe, RBOX); x2 = sx_of(k, s0_, xe, RBOX)
            rect(ctx, x1, by, max(2, x2 - x1), bh, CASHC, 0.2 * a)
            j = k
        j += 1
    for si in Q_SELL:                       # red tick at every sale
        if s0_ <= si <= up:
            xs_ = sx_of(si, s0_, xe, RBOX)
            rect(ctx, xs_ - 3, by - 14, 6, 26, REDC, a)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for jj in range(22):
        rect(ctx, bx + jj * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "detective", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("SELL & WAIT", LCOL))):
        rect(ctx, bx + bw - 300, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 265, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x06, 0x2A, 0x1C), (0x01, 0x07, 0x05))
    god_rays(ctx, W / 2, 470, t, 0.09, GRNC, 14, 1400)
    for j in range(7):                      # rising green candles (decorative, no axes)
        x_ = 90 + j * 150; y_ = 1700 - ((t * 120 + j * 230) % 1300)
        gcandle(ctx, x_, y_, 0.35, GRNC, 0.22, 0.0)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    s_ = max(p * sc * (1 + 0.03 * math.sin(t * 6)), 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 450); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "+5.6%", 0, 0, 300, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 620); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "IN ONE WEEK", 0, 0, 110, C["white"], 1, HEAD, True, "center", outline=16, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 820); ctx.rotate(-0.02); ctx.scale(s_, s_)
    text(ctx, "BUY BACK?", 0, 0, 190, GOLD, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 0.7:
        tag(ctx, 540, 960, "S&P 500 · BEST WEEK SINCE APRIL 2025", C["cream"], back(prog(tl, 0.7, 0.3)), 32, -0.03)


def prop_upcandle(ctx, x, y, px, t):
    ctx.save(); ctx.translate(x + 150, y - 150)
    gcandle(ctx, 0, 0, 0.55, GRNC, 1, -0.12 + 0.1 * math.sin(t * 5))
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_upcandle)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_upcandle)


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["rule"], di("2005-06-30")), (SC["race"], di("2005-12-30")), (SC["y2008"], di("2007-06-29"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 70 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["Sell"] - 0.1, T["hold"] - 0.3, "SELL THE CRASH", "JUST HOLD", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["One"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1, "ONE LONG WAIT", "?? YEARS ??"); ctx.restore()
        hourglass(ctx, 900, 560, 0.45 * q + 1e-3, t)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, curtain=di("2007-07-02"), a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, SC["rule"] + 0.02, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["One"] else None)


def week_card(ctx, cx, cy, p, label, sub, col, up_, rot=0.0):
    if p <= 0:
        return
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -230, -150, 460, 300, (0x10, 0x14, 0x22), 1, 22, border=col)
    gcandle(ctx, -140, 10, 0.5, col, 1, 0.0)
    (arrow_up if up_ else arrow_down)(ctx, -140, 10, 0.28, C["white"], 0.9)
    text(ctx, label, 60, -40, fit(ctx, label, 70, 280), col, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    text(ctx, sub, 60, 60, fit(ctx, sub, 54, 290), C["white"], 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    ctx.restore()


def s_rule(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x16, 0x36), (0x05, 0x06, 0x14))
    tag(ctx, 540, 470, "THE RULE · CHECKED EVERY FRIDAY CLOSE", GOLD, back(prog(t, s0 + 0.05, 0.3)), 32, -0.03, C["ink"])
    week_card(ctx, 300, 720, back(prog(t, T["Down"] - 0.1, 0.35)), "-5% WEEK", "SELL", REDC, False, -0.03)
    week_card(ctx, 780, 720, back(prog(t, T["Up2"] - 0.1, 0.35)), "+5% WEEK", "BUY BACK", GRNC, True, 0.03)
    if t > T["sell"] - 0.1:
        tag(ctx, 300, 940, "NEXT MONDAY'S OPEN", REDC, back(prog(t, T["sell"] - 0.1, 0.3)), 30, 0.02, C["white"])
    if t > T["buyb"] - 0.1:
        tag(ctx, 780, 940, "NEXT MONDAY'S OPEN", GRNC, back(prog(t, T["buyb"] - 0.1, 0.3)), 30, -0.02, C["ink"])
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_news(ctx, t, s0, s1):
    bg_fill(ctx, (0x22, 0x10, 0x2A), (0x06, 0x03, 0x0A))
    for k in range(26):
        u = ((t * 0.25) + k / 26) % 1
        rect(ctx, (k * 173) % W, 1500 - u * 1500, 3, 30, (0xFF, 0xFF, 0xFF), 0.08)
    tag(ctx, 540, 470, "IT FIRED ON THE REAL S&P 500", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 34, -0.03, C["ink"])
    week_card(ctx, 300, 720, back(prog(t, s0 + 0.1, 0.35)), "-8.6%", "NOV 16-20", REDC, False, -0.03)
    week_card(ctx, 780, 720, back(prog(t, T["It37"] - 0.15, 0.35)), "+5.6%", "NOV 23-27", GRNC, True, 0.03)
    if t > T["sold"] - 0.1:
        stamp_box(ctx, ["SOLD MON"], 300, 950, T["sold"] - 0.1, t, REDC, 360, 52, -0.06)
    if t > T["buys37"] - 0.1:
        stamp_box(ctx, ["BUYS MON"], 780, 950, T["buys37"] - 0.1, t, STAMP_GR, 360, 52, 0.05)
    bunting(ctx, "THIS MONTH", t, s0, [C["red"], C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if e != "talk" else e)


def s_race(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x1E, 0x2E), (0x02, 0x05, 0x0A))
    up = race_idx(t, [(s0, di("2005-12-30")), (s1, di("2007-06-29"))])
    race_chart(ctx, t, up, XE1, curtain=di("2007-07-02"))
    tag(ctx, 540, 470, "$10,000 · SPY 2005-2024 · 0.05% FEES", GOLD, back(prog(t, T["ten"] - 0.1, 0.3)), 36, -0.03, C["ink"])
    bunting(ctx, "THE RACE", t, s0, [LCOL, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: e, prop=prop_flag)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    up = race_idx(t, [(s0 + 0.05, di("2007-06-29")), (T["buys08"], Q_B08), (T["foolish"] + 0.3, di("2008-12-31"))])
    race_chart(ctx, t, up, XE1, curtain=di("2009-01-02"))
    if t > T["sells08"] - 0.15:
        tag(ctx, 540, 470, "SOLD JULY 30, 2007", REDC, back(prog(t, T["sells08"] - 0.15, 0.3)), 44, -0.03, C["white"])
    if t > T["third"] - 0.15:
        tag(ctx, 540, 1090, f"BACK IN OCT 2008: {abs(Q_RAW07) * 100:.0f}% CHEAPER", GRNC, back(prog(t, T["third"] - 0.15, 0.3)), 38, 0.02, C["ink"])
    if t > T["foolish"] - 0.15:
        tag(ctx, 800, 560, "WAY AHEAD!", GOLD, back(prog(t, T["foolish"] - 0.15, 0.35)), 46, 0.08, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown" if t > T["foolish"] - 0.1 else "fire", lambda e: "smug" if e != "talk" else e)


def s_whip(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x14, 0x06), (0x08, 0x04, 0x01))
    up = race_idx(t, [(s0 + 0.05, di("2008-12-31")), (T["three"] + 0.4, di("2011-12-30"))])
    race_chart(ctx, t, up, XE1, curtain=di("2012-01-03"))
    trips = [r for r in Q_RT if "2008-10" <= r["sell"] <= "2011-10"]
    ts = [T["o1"], T["i1"], T["o2"], T["i2"]]
    for k in range(12):
        tt = ts[k] if k < 4 else T["i2"] + 0.12 * (k - 3)
        p = back(prog(t, tt - 0.1, 0.3))
        if p <= 0:
            continue
        x = 95 + k * 81
        out_ = k % 2 == 0
        ctx.save(); ctx.translate(x, 1095); ctx.rotate(0.06 * math.sin(t * 8 + k)); ctx.scale(p, p)
        card(ctx, -36, -32, 72, 64, REDC if out_ else GRNC, 1, 10, border=C["ink"])
        text(ctx, "OUT" if out_ else "IN", 0, 12, 30, C["white"] if out_ else C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["six"] - 0.12:
        tag(ctx, 540, 470, f"{len(trips)} ROUND TRIPS · OCT 2008 - OCT 2011", GOLD, back(prog(t, T["six"] - 0.12, 0.3)), 36, -0.03, C["ink"])
    bunting(ctx, "WHIPLASH", t, s0, [C["red"], C["ink"], GRNC, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "shock" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x16, 0x2A), (0x02, 0x04, 0x08))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    r = back(prog(t, s0 + 0.05, 0.35))
    big_title(ctx, "THAT LONG", W / 2, 560, 150, C["white"], r, 980, -0.03, 14)
    big_title(ctx, "WAIT...", W / 2, 740, 190, GOLD, back(prog(t, T["long2"] - 0.1, 0.35)), 980, 0.02, 14)
    hourglass(ctx, 860, 960, 0.6 * r + 1e-3, t * 2)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


QZ0, QZ1 = di("2015-01-02"), di("2020-06-30")
QBOX = (130, 560, 820, 360)


def wait_zoom(ctx, t, up, show_buy, show_covid):
    bx, by, bw, bh = QBOX
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92, 16, border=C["grey"])
    lo, hi = float(RAWC[QZ0:QZ1 + 1].min()) * 0.93, float(RAWC[QZ0:QZ1 + 1].max()) * 1.05
    up = max(QZ0 + 2, min(up, QZ1))
    if up > Q_S15:
        xa = sx_of(Q_S15, QZ0, QZ1, QBOX); xb = sx_of(min(up, Q_B20), QZ0, QZ1, QBOX)
        rect(ctx, xa, by, xb - xa, bh, CASHC, 0.2)
        if xb - xa > 260:
            text(ctx, "IN CASH", (xa + xb) / 2, by + 40, 30, CASHC, 0.9, MONO, True, "center")
    xs, ys = series_xy(RAWC, QZ0, QZ1, up, QBOX, lo, hi, 1); poly(ctx, xs, ys, C["white"], 6, 1, glow=True)
    for lab, d in (("2015", "2015-01-02"), ("2016", "2016-01-04"), ("2017", "2017-01-03"), ("2018", "2018-01-02"), ("2019", "2019-01-02"), ("2020", "2020-01-02")):
        text(ctx, lab, sx_of(di(d), QZ0, QZ1, QBOX), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    if up >= Q_S15 and t > T["sells15"] - 0.15:
        sx = sx_of(Q_S15, QZ0, QZ1, QBOX); sy = by + bh - (RAWO[Q_S15] - lo) / (hi - lo) * bh
        ctx.new_path(); ctx.arc(sx, sy, 13, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(REDC)); ctx.fill()
        tag(ctx, sx + 20, sy + 70, f"SOLD AUG 24, 2015 · ${RAWO[Q_S15]:.0f}", REDC, back(prog(t, T["sells15"] - 0.15, 0.3)), 26, 0.0, C["white"])
    if show_covid:
        ci = di("2020-03-23"); cx_ = sx_of(ci, QZ0, QZ1, QBOX); cy_ = by + bh - (RAWC[ci] - lo) / (hi - lo) * bh
        tag(ctx, cx_ - 120, cy_ + 60, "COVID CRASH", REDC, back(prog(t, T["Covid"] - 0.15, 0.3)), 26, 0.04, C["white"])
    if show_buy:
        bxx = sx_of(Q_B20, QZ0, QZ1, QBOX); byy = by + bh - (RAWO[Q_B20] - lo) / (hi - lo) * bh
        ctx.new_path(); ctx.arc(bxx, byy, 13, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GRNC)); ctx.fill()
        tag(ctx, bxx - 170, byy - 80, f"BUY MAR 30, 2020 · ${RAWO[Q_B20]:.0f}", GRNC, back(prog(t, T["buys111"] - 0.15, 0.3)), 26, 0.0, C["ink"])


def s_payoff(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x0A, 0x2A), (0x04, 0x02, 0x0A))
    up = race_idx(t, [(s0 + 0.05, di("2015-06-30")), (T["sells15"], Q_S15), (T["half"] + 0.3, di("2020-02-14"))])
    wait_zoom(ctx, t, up, False, False)
    tag(ctx, 540, 470, "AUGUST 2015 · A -5% WEEK", REDC, back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["white"])
    if t > T["next"] - 0.15:                 # waiting counter (calendar years since the sale, from the chart index)
        yrs = (DATES[max(up, Q_S15)] - DATES[Q_S15]).days / 365.25
        pk = back(prog(t, T["next"] - 0.15, 0.35))
        ctx.save(); ctx.translate(560, 1095); ctx.rotate(0.02); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -380, -62, 760, 124, GOLD, 1, 22, border=C["ink"])
        s_ = f"NO +5% WEEK: {yrs:.1f} YEARS"
        text(ctx, s_, 0, 26, fit(ctx, s_, 64, 700), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE WAIT", t, s0, [LCOL, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if (e != "talk" and t > T["four"]) else e)


def s_covid(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x10), (0x08, 0x02, 0x04))
    up = race_idx(t, [(s0 + 0.05, di("2020-02-14")), (T["buys111"], Q_B20), (s1 - 0.3, QZ1)])
    wait_zoom(ctx, t, up, t > T["buys111"] - 0.15, t > T["Covid"] - 0.15)
    tag(ctx, 540, 470, f"STILL IN CASH · {Q_YRS:.1f} YEARS", CASHC, back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    if t > T["third2"] - 0.12:
        pk = back(prog(t, T["third2"] - 0.12, 0.35))
        ctx.save(); ctx.translate(560, 1095); ctx.rotate(0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -400, -62, 800, 124, REDC, 1, 22, border=C["ink"])
        s_ = f"BOUGHT BACK +{Q_RAW15 * 100:.0f}% HIGHER (PRICE)"
        text(ctx, s_, 0, 26, fit(ctx, s_, 60, 740), C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "2020", t, s0, [C["red"], C["ink"], GRNC, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if (e != "talk" and t > T["third2"]) else ("shock" if e != "talk" else e))


def footnote(ctx, t):
    if t >= T["Verd"] - 0.1:
        a = back(prog(t, T["Verd"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 985); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"4% WEEKS: {money(Q_SCAN['-0.04/0.04'])} · 6%: {money(Q_SCAN['-0.06/0.06'])} · 7%: {money(Q_SCAN['-0.07/0.07'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 34, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, f"$10,000 · 2005-2024 · {_R['tim'] * 100:.0f}% OF DAYS INVESTED", W / 2, 400, 32, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "SELL & WAIT", money(CL_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "THE SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x02, 0x03, 0x0A), 0.8)
    stamp_box(ctx, ["THE CRASH NEVER", "BEAT HIM."], W / 2, 470, T["Verd"] - 0.05, t, STAMP_OR, 860, 76, -0.05)
    if t > T["big"] - 0.1:
        stamp_box(ctx, ["THE WAIT DID."], W / 2, 720, T["big"] - 0.1, t, C["red"], 760, 84, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Verd"] + 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 860); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -46, 600, 92, C["red"], 1, 46)
        text(ctx, "FOLLOW for case #56", 0, 16, 44, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "rule": s_rule, "news": s_news, "race": s_race, "y2008": s_y2008, "whip": s_whip,
            "remember": s_remember, "payoff": s_payoff, "covid": s_covid, "score": s_score, "verdict": s_verdict, "loop": s_loop}
