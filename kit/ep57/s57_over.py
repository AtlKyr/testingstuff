

# ================================================================ #57 overrides (yield-curve inversion: the recession alarm)
LCOL = (0xFF, 0x7A, 0x2E)      # ALARM RULE (orange)
HCOL = (0x4F, 0xC3, 0xF7)      # BUY & HOLD (blue)
CASHC = (0xFF, 0xB0, 0x40)
XE1 = di("2009-12-31")


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #57", C["cream"], a, 26, -0.03)
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


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007, 2008, 2009), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = 0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    j = s0_
    while j <= up:
        if not INN[j]:
            k = j
            while k <= up and not INN[k]:
                k += 1
            x1 = sx_of(j, s0_, xe, RBOX); x2 = sx_of(k, s0_, xe, RBOX)
            rect(ctx, x1, by, max(3, x2 - x1), bh, CASHC, 0.25 * a)
            j = k
        j += 1
    for si in Q_SELL:
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
    poly(ctx, xs1, ys1, HCOL, 9, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 6, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "detective", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("ALARM RULE", LCOL))):
        rect(ctx, bx + 20, by + 22 + k * 30, 26, 10, col)
        text(ctx, lab, bx + 55, by + 32 + k * 30, 22, col, 1, MONO, True, "left")


def curve_icon(ctx, cx, cy, s, inverted, col, t, a=1.0):
    """schematic yield curve: rates (y) vs maturity (x). Normal = rising, inverted = falling. No numbers."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path()
    for k in range(41):
        u = k / 40
        yv = (1 - math.exp(-4 * u)) * 160
        yy = (-yv + 80) if not inverted else (yv - 80)
        yy += math.sin(t * 3 + u * 6) * 4
        x_ = -200 + 400 * u
        ctx.line_to(x_, yy) if k else ctx.move_to(x_, yy)
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(26); ctx.stroke_preserve()
    ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def bell(ctx, cx, cy, s, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.sin(t * 18) * 0.18); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-70, 50); ctx.curve_to(-70, -60, -40, -90, 0, -90); ctx.curve_to(40, -90, 70, -60, 70, 50)
    ctx.line_to(90, 70); ctx.line_to(-90, 70); ctx.close_path()
    ctx.set_source_rgba(*rgba(REDC, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(9); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 86, 18, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD, a)); ctx.fill()
    for sg in (-1, 1):
        for r in (110, 140):
            ctx.new_path(); ctx.arc(0, -10, r, -math.pi / 2 + sg * 0.5 - 0.25, -math.pi / 2 + sg * 0.5 + 0.25)
            ctx.set_source_rgba(*rgba(GOLD, a * (0.5 + 0.5 * math.sin(t * 12)))); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x2A, 0x0A, 0x22), (0x06, 0x02, 0x08))
    god_rays(ctx, W / 2, 470, t, 0.08, REDC, 14, 1400)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    s_ = max(p * sc * (1 + 0.03 * math.sin(t * 6)), 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 290); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "YIELD CURVE:", 0, 0, 130, C["white"], 1, HEAD, True, "center", outline=16, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 450); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "UPSIDE DOWN", 0, 0, 130, REDC, 1, HEAD, True, "center", outline=16, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540 + shake, 720); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "2+ YEARS", 0, 0, 230, GOLD, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 0.9:
        tag(ctx, 540, 870, "2-YEAR YIELD ABOVE 10-YEAR · JUL 2022 - AUG 2024", C["cream"], back(prog(tl, 0.9, 0.3)), 26, -0.03)


def prop_curve(ctx, x, y, px, t):
    ctx.save(); ctx.translate(x + 150, y - 140); ctx.rotate(-0.1 + 0.08 * math.sin(t * 4))
    card(ctx, -80, -60, 160, 120, C["cream"], 1, 14, border=C["ink"])
    curve_icon(ctx, 0, 0, 0.32, True, REDC, t)
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e, prop=prop_curve)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "night", lambda e: "shock", prop=prop_curve)


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["rule"], di("2005-06-30")), (SC["race"], di("2005-12-01")), (SC["y2006"], di("2005-12-28"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 70 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["Sell"] - 0.1, T["ignore"] - 0.25, "SELL ON THE ALARM", "IGNORE IT", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["One"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1, "ONE ALL-CLEAR SIGNAL", "??? 20??"); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, curtain=di("2006-01-03"), a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, SC["rule"] + 0.02, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["One"] else None)


def s_rule(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x16, 0x36), (0x05, 0x06, 0x14))
    tag(ctx, 540, 470, "THE RULE · 10-YEAR MINUS 2-YEAR TREASURY YIELD", GOLD, back(prog(t, s0 + 0.05, 0.3)), 28, -0.03, C["ink"])
    for kk, (lab, sub, col, x, tt, inv) in enumerate((("INVERTED", "SELL", REDC, 300, T["Short"], True), ("NORMAL AGAIN", "BUY", GRNC, 780, T["Flip"], False))):
        pk = back(prog(t, tt - 0.15, 0.35))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 760); ctx.rotate(-0.03 if kk == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -220, -190, 440, 380, (0x10, 0x14, 0x22), 1, 22, border=col)
        text(ctx, lab, 0, -130, fit(ctx, lab, 56, 400), col, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        curve_icon(ctx, 0, -10, 0.8, inv, col, t)
        text(ctx, "SHORT", -150, 90, 24, C["grey"], 1, MONO, True, "center"); text(ctx, "LONG", 150, 90, 24, C["grey"], 1, MONO, True, "center")
        ctx.restore()
        if (kk == 0 and t > T["sell"] - 0.1) or (kk == 1 and t > T["buyr"] - 0.1):
            stamp_box(ctx, [sub], x, 1010, (T["sell"] if kk == 0 else T["buyr"]) - 0.1, t, REDC if kk == 0 else STAMP_GR, 260, 60, -0.05 if kk == 0 else 0.05)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_alarm(ctx, t, s0, s1):
    bg_fill(ctx, (0x30, 0x08, 0x10), (0x08, 0x02, 0x04))
    god_rays(ctx, W / 2, 700, t, 0.07, REDC, 12, 1300)
    bell(ctx, 540, 760, 1.4 * back(prog(t, s0 + 0.05, 0.35)) + 1e-3, t)
    big_title(ctx, "THE RECESSION", W / 2, 470, 120, C["white"], back(prog(t, T["recess0"] - 0.2, 0.35)), 980, -0.03, 14)
    big_title(ctx, "ALARM", W / 2, 1030, 170, REDC, back(prog(t, T["recess0"] + 0.1, 0.35)), 980, 0.03, 16)
    bunting(ctx, "WALL STREET SAYS", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


def s_race(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x1E, 0x2E), (0x02, 0x05, 0x0A))
    up = race_idx(t, [(s0, di("2005-06-30")), (s1, di("2005-12-28"))])
    race_chart(ctx, t, up, XE1, curtain=di("2006-01-03"))
    tag(ctx, 540, 470, "$10,000 · SPY 2005-2024 · 0.05% FEES", GOLD, back(prog(t, T["ten"] - 0.1, 0.3)), 36, -0.03, C["ink"])
    bunting(ctx, "THE RACE", t, s0, [LCOL, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: e, prop=prop_flag)


def s_y2006(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x14, 0x06), (0x08, 0x04, 0x01))
    up = race_idx(t, [(s0 + 0.05, di("2005-12-28")), (T["Ten"] + 0.3, di("2007-05-31"))])
    race_chart(ctx, t, up, XE1, curtain=di("2007-06-01"))
    if t > T["six"] - 0.15:
        bell(ctx, 900, 520, 0.45, t)
    ts = [T["s1"], T["b1"], T["s2"], T["b2"]]
    for k in range(10):
        tt = ts[k] if k < 4 else T["b2"] + 0.12 * (k - 3)
        p = back(prog(t, tt - 0.1, 0.3))
        if p <= 0:
            continue
        x = 115 + k * 94; out_ = k % 2 == 0
        ctx.save(); ctx.translate(x, 1095); ctx.rotate(0.06 * math.sin(t * 8 + k)); ctx.scale(p, p)
        card(ctx, -40, -32, 80, 64, REDC if out_ else GRNC, 1, 10, border=C["ink"])
        text(ctx, "SELL" if out_ else "BUY", 0, 12, 28, C["white"] if out_ else C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["Ten"] - 0.12 and t < T["And"] - 0.1:
        tag(ctx, 540, 470, f"{_R['sells_0607']} SELLS · DEC 2005 - JUN 2007", GOLD, back(prog(t, T["Ten"] - 0.12, 0.3)), 38, -0.03, C["ink"])
    if t > T["And"] - 0.1:
        tag(ctx, 540, 470, "RECESSION: DEC 2007 - JUN 2009 (NBER)", REDC, back(prog(t, T["And"] - 0.1, 0.3)), 34, -0.03, C["white"])
    bunting(ctx, "2006", t, s0, [C["red"], C["ink"], GRNC, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "shock" if e != "talk" else e)


def raw_zoom(ctx, t, i0, i1, up, box, band=None, marks=(), labels=()):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92, 16, border=C["grey"])
    lo, hi = float(RAWC[i0:i1 + 1].min()) * 0.93, float(RAWC[i0:i1 + 1].max()) * 1.05
    up = max(i0 + 2, min(up, i1))
    if band is not None and up > band[0]:
        xa = sx_of(band[0], i0, i1, box); xb = sx_of(min(up, band[1]), i0, i1, box)
        rect(ctx, xa, by, xb - xa, bh, CASHC, 0.22)
        if xb - xa > 220:
            text(ctx, "IN CASH", (xa + xb) / 2, by + 40, 30, CASHC, 0.9, MONO, True, "center")
    xs, ys = series_xy(RAWC, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, C["white"], 6, 1, glow=True)
    for lab, d in labels:
        text(ctx, lab, sx_of(di(d), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    for mi, px_, lab, col, tt, dx, dy, ink in marks:
        if up >= mi and t > tt - 0.15:
            sx = sx_of(mi, i0, i1, box); sy = by + bh - (px_ - lo) / (hi - lo) * bh
            ctx.new_path(); ctx.arc(sx, sy, 13, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
            tag(ctx, sx + dx, sy + dy, lab, col, back(prog(t, tt - 0.15, 0.3)), 26, 0.0, ink)


def s_y2022(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x0A, 0x2A), (0x04, 0x02, 0x0A))
    i0, i1 = di("2022-01-03"), di("2024-12-31")
    up = race_idx(t, [(s0 + 0.05, di("2022-03-31")), (T["sells22"], Q_S22), (T["forty"] + 0.3, Q_B24 + 30)])
    raw_zoom(ctx, t, i0, i1, up, (130, 560, 820, 360), band=(Q_S22, Q_B24),
             marks=((Q_S22, RAWO[Q_S22], f"SOLD JUL 2022 · ${RAWO[Q_S22]:.0f}", REDC, T["sells22"], 40, 80, C["white"]),
                    (Q_B24, RAWO[Q_B24], f"BACK AUG 2024 · ${RAWO[Q_B24]:.0f}", GRNC, T["forty"], -190, -70, C["ink"])),
             labels=(("2022", "2022-01-14"), ("2023", "2023-01-13"), ("2024", "2024-01-12")))
    tag(ctx, 540, 470, "2022 · THE CURVE INVERTS AGAIN", REDC, back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["white"])
    if t > T["forty"] - 0.12:
        pk = back(prog(t, T["forty"] - 0.12, 0.35))
        ctx.save(); ctx.translate(560, 1095); ctx.rotate(0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -390, -62, 780, 124, GRNC, 1, 22, border=C["ink"])
        s_ = f"SPY WITHOUT HIM: +{Q_RAW22 * 100:.0f}% (PRICE)"
        text(ctx, s_, 0, 26, fit(ctx, s_, 62, 720), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "2022-2024", t, s0, [LCOL, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if (e != "talk" and t > T["sits"]) else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x16, 0x2A), (0x02, 0x04, 0x08))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    big_title(ctx, "THAT", W / 2, 560, 150, C["white"], back(prog(t, s0 + 0.05, 0.35)), 980, -0.03, 14)
    big_title(ctx, "ALL-CLEAR...", W / 2, 750, 170, GRNC, back(prog(t, T["allclear2"] - 0.1, 0.35)), 980, 0.02, 14)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_payoff(ctx, t, s0, s1):
    bg_fill(ctx, (0x06, 0x22, 0x18), (0x01, 0x06, 0x04))
    i0, i1 = di("2006-06-01"), di("2009-06-30")
    up = race_idx(t, [(s0 + 0.05, di("2007-03-30")), (T["buys"], Q_B07), (T["top"] + 0.2, Q_TOP + 5)])
    raw_zoom(ctx, t, i0, i1, up, (130, 560, 820, 360),
             marks=((Q_B07, RAWO[Q_B07], f"BUY JUN 11, 2007 · ${RAWO[Q_B07]:.0f}", GRNC, T["buys"], -60, 90, C["ink"]),
                    (Q_TOP, RAWC[Q_TOP], "THE TOP · OCT 9, 2007", GOLD, T["top"], 60, -60, C["ink"])),
             labels=(("2007", "2007-01-12"), ("2008", "2008-01-14"), ("2009", "2009-01-14")))
    tag(ctx, 540, 470, "JUNE 2007 · THE CURVE FLIPS BACK", GRNC, back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    if t > T["Four"] - 0.12:
        tag(ctx, 540, 1095, f"{_R['months_before_top']:.0f} MONTHS BEFORE THE TOP", GOLD, back(prog(t, T["Four"] - 0.12, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2007", t, s0, [GRNC, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "party" if t < T["top"] else "grad", lambda e: "smug" if (e != "talk" and t < T["top"]) else ("shock" if e != "talk" else e))


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    up = race_idx(t, [(s0 + 0.05, di("2007-06-29")), (T["f55"] + 0.3, Q_LOW09)])
    race_chart(ctx, t, up, XE1, curtain=Q_LOW09 + 1)
    if t > T["f55"] - 0.12:
        tag(ctx, 540, 1095, f"WORST DROP: ALARM {_R['mdd'] * 100:.0f}% · HOLD {_R['mdd_bh'] * 100:.0f}%", REDC, back(prog(t, T["f55"] - 0.12, 0.3)), 38, 0.02, C["white"])
    if t > T["Same"] - 0.12:
        tag(ctx, 540, 470, "SAME AS DOING NOTHING", GOLD, back(prog(t, T["Same"] - 0.12, 0.3)), 46, -0.03, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Verd"] - 0.1:
        a = back(prog(t, T["Verd"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 985); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        sc = _R["scan"]
        s_ = f"CONFIRM 5 DAYS: {money(sc['5'])} · 1 MONTH: {money(sc['21'])} · 3 MONTHS: {money(sc['63'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 34, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, f"$10,000 · 2005-2024 · {_R['sells']} SELLS · {_R['tim'] * 100:.0f}% INVESTED", W / 2, 400, 32, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "ALARM RULE", money(CL_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "THE SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x02, 0x03, 0x0A), 0.9)
    stamp_box(ctx, ["RIGHT ABOUT", "THE RECESSION."], W / 2, 470, T["Verd"] - 0.05, t, STAMP_GR, 820, 72, -0.05)
    if t > T["big"] - 0.1:
        stamp_box(ctx, ["WRONG ABOUT", "THE MONEY."], W / 2, 720, T["big"] - 0.1, t, C["red"], 820, 72, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Verd"] + 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 885); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -42, 600, 84, C["red"], 1, 42)
        text(ctx, "FOLLOW for case #58", 0, 15, 42, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "rule": s_rule, "alarm": s_alarm, "race": s_race, "y2006": s_y2006, "y2022": s_y2022,
            "remember": s_remember, "payoff": s_payoff, "crash": s_crash, "score": s_score, "verdict": s_verdict, "loop": s_loop}
