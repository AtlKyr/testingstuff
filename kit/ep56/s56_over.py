

# ================================================================ #56 overrides (3x S&P fund vs plain S&P)
LCOL = (0xFF, 0x7A, 0x2E)      # 3X FUND (orange)
HCOL = (0x4F, 0xC3, 0xF7)      # PLAIN S&P (blue)
XE1 = di("2017-06-30")


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #56", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 610, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 625, 38, 330, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 790, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 625, 38, 330, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(Q_THREE_V), 790, 78, fit(ctx, money(Q_THREE_V), 36, 300, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["Verd"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2009, 2013, 2017), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = 0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(16000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = 0.0
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for jj in range(22):
        rect(ctx, bx + jj * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "race", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("PLAIN S&P", HCOL), ("3X FUND", LCOL))):
        rect(ctx, bx + 20, by + 22 + k * 30, 26, 10, col)
        text(ctx, lab, bx + 55, by + 32 + k * 30, 22, col, 1, MONO, True, "left")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x34, 0x08, 0x10), (0x08, 0x01, 0x04))
    god_rays(ctx, W / 2, 470, t, 0.09, REDC, 14, 1400)
    for j in range(7):                      # falling red candles (decorative, no axes)
        x_ = 90 + j * 150; y_ = -200 + ((t * 140 + j * 230) % 1900)
        gcandle(ctx, x_, y_, 0.35, REDC, 0.2, 0.0)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    s_ = max(p * sc * (1 + 0.03 * math.sin(t * 6)), 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 300); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "3X S&P FUND", 0, 0, 140, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540 + shake, 560); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "-85.5%", 0, 0, 280, REDC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(-0.02); ctx.scale(s_, s_)
    text(ctx, "IN ONE YEAR", 0, 0, 150, GOLD, 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 900, "2008 · SIMULATED 3X DAILY FUND (UPRO-STYLE)", C["cream"], back(prog(tl, 1.0, 0.3)), 28, -0.03)


def prop_downcandle(ctx, x, y, px, t):
    ctx.save(); ctx.translate(x + 150, y - 150)
    gcandle(ctx, 0, 0, 0.55, REDC, 1, 0.12 + 0.1 * math.sin(t * 5))
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e, prop=prop_downcandle)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "fire", lambda e: "shock", prop=prop_downcandle)


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["rule"], di("2005-12-30"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 70 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["Tri2"] - 0.1, T["plain"] - 0.2, "3X FUND", "PLAIN S&P", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["One"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1, "ONE STRANGE YEAR", "20?? · ??%"); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, curtain=di("2006-01-03"), a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, SC["rule"] + 0.02, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["One"] else None)


def day_pair(ctx, cx, cy, p, spy_pct, three_pct, rot=0.0):
    if p <= 0:
        return
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -440, -110, 880, 220, (0x10, 0x14, 0x22), 1, 22, border=C["grey"])
    up_ = spy_pct > 0; col = GRNC if up_ else REDC
    text(ctx, "S&P", -300, -40, 48, HCOL, 1, HEAD, True, "center")
    text(ctx, f"{spy_pct:+d}%", -300, 50, 96, col, 1, HEAD, True, "center", outline=10, ocol=C["ink"])
    text(ctx, "=", -60, 30, 90, C["white"], 1, HEAD, True, "center")
    text(ctx, "3X FUND", 220, -40, 48, LCOL, 1, HEAD, True, "center")
    text(ctx, f"{three_pct:+d}%", 220, 60, 130, col, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
    ctx.restore()


def s_rule(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x16, 0x36), (0x05, 0x06, 0x14))
    tag(ctx, 540, 470, "$10,000 EACH · JAN 3, 2005 · HELD TO 2024", GOLD, back(prog(t, T["Ten"] - 0.1, 0.3)), 34, -0.03, C["ink"])
    day_pair(ctx, 540, 700, back(prog(t, T["three"] - 0.15, 0.35)), 1, 3, -0.02)
    day_pair(ctx, 540, 960, back(prog(t, T["every"] - 0.15, 0.35)), -1, -3, 0.02)
    if t > T["every"] + 0.4:
        tag(ctx, 540, 1110, "FEE 0.91%/YR + BORROWING AT T-BILL RATE", C["cream"], back(prog(t, T["every"] + 0.4, 0.3)), 28, 0.02, C["ink"])
    bunting(ctx, "THE RULES", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_y2007(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x1E, 0x2E), (0x02, 0x05, 0x0A))
    up = race_idx(t, [(s0, di("2005-12-30")), (T["ahead"] + 0.2, Q_I07)])
    race_chart(ctx, t, up, XE1, curtain=di("2008-01-02"))
    if t > T["ahead"] - 0.15:
        tag(ctx, 800, 560, "3X AHEAD!", GOLD, back(prog(t, T["ahead"] - 0.15, 0.35)), 46, 0.08, C["ink"])
    bunting(ctx, "THE RACE", t, s0, [LCOL, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    up = race_idx(t, [(s0 + 0.05, Q_I07), (T["March"] + 0.4, Q_ILOW)])
    race_chart(ctx, t, up, XE1, curtain=Q_ILOW + 1)
    tag(ctx, 540, 470, "2008 CRASH", REDC, back(prog(t, T["crash"] - 0.15, 0.3)), 48, -0.03, C["white"])
    if t > T["eight"] - 0.15:
        pk = back(prog(t, T["eight"] - 0.15, 0.35))
        ctx.save(); ctx.translate(560, 1095); ctx.rotate(0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -380, -62, 760, 124, REDC, 1, 22, border=C["ink"])
        s_ = f"MAR 9, 2009: $10,000 -> {money(Q_LOW)}"
        text(ctx, s_, 0, 26, fit(ctx, s_, 62, 700, HEAD), C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "shock" if e != "talk" else e)


def s_comeback(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x22, 0x14), (0x02, 0x08, 0x04))
    if t < T["crawls"] - 0.1:
        big_title(ctx, "GAME OVER?", W / 2, 640, 200, C["white"], back(prog(t, s0 + 0.05, 0.35)), 980, -0.03, 16)
    else:
        up = race_idx(t, [(T["crawls"] - 0.1, Q_ILOW), (T["catch"] + 0.4, Q_ICATCH)])
        race_chart(ctx, t, up, XE1, curtain=Q_ICATCH + 1)
        if t > T["catch"] - 0.15:
            tag(ctx, 540, 1090, f"CAUGHT THE PLAIN S&P: JAN 2017 · {_R['catch_years']:.0f} YEARS", GRNC, back(prog(t, T["catch"] - 0.15, 0.3)), 34, 0.02, C["ink"])
    bunting(ctx, "2009-2016", t, s0, [GRNC, C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


def val_zoom(ctx, t, i0, i1, k, box, series_list, labels=()):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92, 16, border=C["grey"])
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    lo = min(float(s[i0:i1 + 1].min()) for s, _ in series_list) * 0.9
    hi = max(float(s[i0:i1 + 1].max()) for s, _ in series_list) * 1.06
    pts = []
    for s, col in series_list:
        xs, ys = series_xy(s, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, col, 7, 1, glow=True); pts.append((xs[-1], ys[-1]))
    for lab, d in labels:
        text(ctx, lab, sx_of(di(d), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    return up, pts


def s_covid(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x10), (0x08, 0x02, 0x04))
    i0, i1 = di("2020-01-02"), di("2020-06-30")
    k = clamp((t - s0 - 0.1) / max(0.5, T["s76"] + 0.3 - s0))
    val_zoom(ctx, t, i0, i1, k, (130, 560, 820, 360), [(SV, LCOL)],
             (("JAN", "2020-01-15"), ("FEB", "2020-02-14"), ("MAR", "2020-03-16"), ("APR", "2020-04-15"), ("MAY", "2020-05-15"), ("JUN", "2020-06-15")))
    tag(ctx, 540, 470, "2020 · THE 3X FUND", LCOL, back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["s76"] - 0.12:
        pk = back(prog(t, T["s76"] - 0.12, 0.35))
        ctx.save(); ctx.translate(560, 1095); ctx.rotate(0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -380, -62, 760, 124, REDC, 1, 22, border=C["ink"])
        s_ = f"FEB 19 - MAR 23: {_R['c20_3'] * 100:.0f}%"
        text(ctx, s_, 0, 26, fit(ctx, s_, 64, 700), C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "2020", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "shock" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x16, 0x2A), (0x02, 0x04, 0x08))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    big_title(ctx, "THAT STRANGE", W / 2, 580, 150, C["white"], back(prog(t, s0 + 0.05, 0.35)), 980, -0.03, 14)
    big_title(ctx, "YEAR...", W / 2, 770, 200, GOLD, back(prog(t, T["strange2"] - 0.1, 0.35)), 980, 0.02, 14)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_payoff(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x0A, 0x2A), (0x04, 0x02, 0x0A))
    i0, i1 = Q_I10, Q_I11
    n1 = HV / HV[i0] * 100; n3 = SV / SV[i0] * 100
    k = clamp((t - s0 - 0.1) / max(0.5, T["Lost"] - s0))
    val_zoom(ctx, t, i0, i1, k, (130, 560, 820, 360), [(n1, HCOL), (n3, LCOL)],
             (("JAN", "2011-01-14"), ("APR", "2011-04-15"), ("JUL", "2011-07-15"), ("OCT", "2011-10-14"), ("DEC", "2011-12-15")))
    bx, by, bw, bh = (130, 560, 820, 360)
    tag(ctx, 540, 470, "2011 · BOTH START AT 100", GOLD, back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["nowhere"] - 0.15:
        tag(ctx, 300, 1090, f"S&P: {_R['r2011_1'] * 100:+.1f}%", HCOL, back(prog(t, T["nowhere"] - 0.15, 0.3)), 46, -0.03, C["ink"])
    if t > T["eleven2"] - 0.15:
        tag(ctx, 780, 1090, f"3X: {_R['r2011_3'] * 100:+.1f}%", REDC, back(prog(t, T["eleven2"] - 0.15, 0.3)), 50, 0.03, C["white"])
    bunting(ctx, "2011", t, s0, [LCOL, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["eleven2"]) else e)


def s_decay(ctx, t, s0, s1):
    grid_bg(ctx, (0x22, 0x10, 0x10), (0x06, 0x02, 0x02))
    tag(ctx, 540, 470, "EXAMPLE: UP 10%, THEN DOWN 10%", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 38, -0.03, C["ink"])
    rows = (("S&P", HCOL, ["$100", "$110", "$99"]), ("3X", LCOL, ["$100", "$130", "$91"]))
    for r_, (lab, col, vals) in enumerate(rows):
        y_ = 660 + r_ * 220
        p0 = back(prog(t, s0 + 0.15 + r_ * 0.25, 0.3))
        if p0 <= 0:
            continue
        text(ctx, lab, 140, y_ + 20, 60, col, p0, HEAD, True, "center", outline=8, ocol=C["ink"])
        for j, v in enumerate(vals):
            pj = back(prog(t, s0 + 0.3 + r_ * 0.25 + j * 0.35, 0.3))
            if pj <= 0:
                continue
            x_ = 340 + j * 260
            colv = C["white"] if j < 2 else (REDC if v != "$100" else C["white"])
            ctx.save(); ctx.translate(x_, y_); ctx.scale(pj, pj)
            card(ctx, -110, -60, 220, 120, (0x10, 0x14, 0x22), 1, 16, border=col)
            text(ctx, v, 0, 26, 64, colv, 1, HEAD, True, "center")
            ctx.restore()
    if t > T["eats"] - 0.15:
        tag(ctx, 540, 1100, "3X LOST 9%. THE S&P LOST 1%.", REDC, back(prog(t, T["eats"] - 0.15, 0.3)), 40, 0.02, C["white"])
    bunting(ctx, "THE LEAK", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "lab" if False else "tophat", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Verd"] - 0.1:
        a = back(prog(t, T["Verd"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 985); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"2X FUND: {money(Q_TWO_V)} · 3X LOW: {money(Q_LOW)} (MAR 2009) · SIMULATED"
        text(ctx, s_, 0, 14, fit(ctx, s_, 34, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024 · DIVIDENDS + FEES IN", W / 2, 400, 32, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "PLAIN S&P", money(Q_ONE_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "3X FUND", money(Q_THREE_V), LCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "THE SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x02, 0x03, 0x0A), 0.9)
    stamp_box(ctx, ["3X WON."], W / 2, 450, T["Verd"] - 0.05, t, STAMP_GR, 640, 96, -0.05)
    if t > T["big"] - 0.1:
        stamp_box(ctx, ["IF YOU SURVIVED", "A 92% LOSS."], W / 2, 700, T["big"] - 0.1, t, C["red"], 820, 72, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Verd"] + 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 880); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -46, 600, 92, C["red"], 1, 46)
        text(ctx, "FOLLOW for case #57", 0, 16, 44, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "rule": s_rule, "y2007": s_y2007, "crash": s_crash, "comeback": s_comeback, "covid": s_covid,
            "remember": s_remember, "payoff": s_payoff, "decay": s_decay, "score": s_score, "verdict": s_verdict, "loop": s_loop}
