

# ================================================================ #45 overrides (Bollinger Bands)
LCOL = (0xC0, 0x7C, 0xFF)   # A: THE BANDS (violet)
HCOL = (0x4F, 0xC3, 0xF7)   # B: BUY & HOLD (blue)


def bb_chart(ctx, box, i0, i1, k, t, marks=True, a=1.0, labels=(), tmark=None):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    seg = np.r_[CL[i0:i1 + 1], BLO[i0:i1 + 1], BUP[i0:i1 + 1]]
    lo, hi = float(np.nanmin(seg)) * 0.98, float(np.nanmax(seg)) * 1.02
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    # band fill
    xs_u, ys_u = series_xy(BUP, i0, i1, up, box, lo, hi, 1); xs_l, ys_l = series_xy(BLO, i0, i1, up, box, lo, hi, 1)
    ctx.new_path(); ctx.move_to(xs_u[0], ys_u[0])
    for x_, y_ in zip(xs_u, ys_u):
        ctx.line_to(x_, y_)
    for x_, y_ in zip(xs_l[::-1], ys_l[::-1]):
        ctx.line_to(x_, y_)
    ctx.close_path(); ctx.set_source_rgba(*rgba(LCOL, 0.16 * a)); ctx.fill()
    poly(ctx, xs_u, ys_u, LCOL, 4, 0.9 * a, glow=False); poly(ctx, xs_l, ys_l, LCOL, 4, 0.9 * a, glow=False)
    xs, ys = series_xy(BMID, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, GOLD, 3, 0.8 * a, glow=False)
    xs, ys = series_xy(CL, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, C["white"], 6, a, glow=True)
    if marks:
        for bi, si in zip(TB_I, TS_I):
            for mi, lab, col, dy in ((bi, "BUY", GRNC, 60), (si, "SELL", REDC, -60)):
                if i0 <= mi <= up and (tmark is None or t >= tmark):
                    sx = sx_of(mi, i0, i1, box); sy = by + bh - (OP[mi] - lo) / (hi - lo) * bh
                    ctx.new_path(); ctx.arc(sx, sy, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
                    card(ctx, sx - 44, sy + dy - 20, 88, 40, col, 1, 8, border=C["ink"])
                    text(ctx, lab, sx, sy + dy + 10, 24, C["ink"], 1, HEAD, True, "center")
    for lab, d in labels:
        text(ctx, lab, sx_of(di(d), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    return lo, hi


def prop_band(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 60, y - 120)
    if fl:
        ctx.scale(-1, 1)
    ctx.rotate(math.sin(t * 4) * 0.1)
    card(ctx, -70, -50, 140, 100, (0x0C, 0x10, 0x1C), 1, 12, border=C["white"])
    for k, col in enumerate((LCOL, GOLD, LCOL)):
        ctx.new_path(); ctx.move_to(-55, -25 + k * 25)
        for j in range(12):
            ctx.line_to(-55 + j * 10, -25 + k * 25 + math.sin(j * 0.8 + t * 3) * 8)
        ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #45", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["big"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
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
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    # IN-MARKET barcode
    xs_ = None
    for bi, si in zip(TB_I, TS_I):
        if s0_ <= bi <= up:
            x1 = sx_of(bi, s0_, xe, RBOX); x2 = sx_of(min(si, up), s0_, xe, RBOX)
            rect(ctx, x1, by + bh - 16, max(2, x2 - x1), 16, LCOL, 0.55 * a)
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "lab", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("BOLLINGER BANDS", LCOL))):
        rect(ctx, bx + bw - 300, by + 20 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 265, by + 30 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-06-30"); XE2 = di("2014-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x20, 0x0C, 0x3A), (0x05, 0x02, 0x0C))
    god_rays(ctx, W / 2, 480, t, 0.08, LCOL, 14, 1400)
    for k in range(3):
        ctx.new_path()
        for j in range(60):
            x_ = j * 19; y_ = 1180 + (k - 1) * 90 + math.sin(j * 0.25 + t * 2) * 50
            (ctx.move_to if j == 0 else ctx.line_to)(x_, y_)
        ctx.set_source_rgba(*rgba(LCOL if k != 1 else GOLD, 0.35)); ctx.set_line_width(6); ctx.stroke()
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 500); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "65 WINS", 0, 0, 250, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "20 LOSSES", 0, 0, 200, REDC, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 920, "BOLLINGER BANDS · SPY · 20 YEARS", C["cream"], back(prog(tl, 1.0, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "lab", lambda e: "shock" if e != "talk" else e, prop=prop_band)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "lab", lambda e: "shock", prop=prop_band)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE SEPTEMBER TRADE", hidden="SEP ??, 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["bands"], di("2005-06-30"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.5, T["B"] - 0.6, "BANDS", "HOLD", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Watch"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    elif t > s0:
        bb_chart(ctx, (180, 620, 720, 260), di("2018-01-02"), di("2018-04-30"), 1.0, t, marks=False)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


QB0, QB1 = di("2018-01-02"), di("2018-04-30")


def s_bands(ctx, t, s0, s1):
    grid_bg(ctx, (0x1E, 0x12, 0x36), (0x0B, 0x07, 0x16))
    tag(ctx, 540, 440, "BOLLINGER BANDS (20 DAYS, 2 STDEV)", LCOL, back(prog(t, s0 + 0.05, 0.3)), 36, -0.03, C["ink"])
    k = ease(prog(t, s0 + 0.1, 1.6))
    bb_chart(ctx, (130, 540, 820, 330), QB0, QB1, k, t, marks=t > T["Buy"] - 0.2, labels=(("JAN 2018", "2018-01-10"), ("APR 2018", "2018-04-20")))
    for kk, (title, col, x, tt) in enumerate((("BELOW LOWER BAND: BUY", GRNC, 290, T["Buy"]), ("BACK TO MIDDLE: SELL", REDC, 790, T["Sell"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1060); ctx.rotate(-0.03 if kk == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 50, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


def s_wins(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    pts = [(s0 + 0.1, di("2005-06-30")), (T["Then"], di("2007-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "$10,000 · SPY · FROM 2005", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    if t > T["Small"] - 0.15:
        tag(ctx, 540, 530, "SMALL BOUNCES, SMALL WINS", GRNC, back(prog(t, T["Small"] - 0.15, 0.3)), 42, 0.02, C["ink"])
        nw = 0
        for kk, (bi, w) in enumerate(zip(TB_I, TWIN)):
            if TRD[kk][0] > "2007-12-31":
                break
            tt = T["Small"] + kk * 0.12
            if t >= tt:
                card(ctx, 120 + (kk % 12) * 72, 1060 + (kk // 12) * 66, 58, 54, GRNC if w else REDC, 1, 10, shadow=False, border=C["ink"])
    bunting(ctx, "2005-2007", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2008-01-02")), (T["ahead"], di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: THE CRASH", REDC, back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["white"])
    if t > T["half"] - 0.15:
        tag(ctx, 540, 530, "HALF THE TIME IN CASH", GOLD, back(prog(t, T["half"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    if t > T["ahead"] - 0.15:
        stamp_box(ctx, ["WAY AHEAD!"], 540, 1090, T["ahead"] - 0.1, t, STAMP_GR, 520, 70, -0.05)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown" if t > T["ahead"] else "fire", lambda e: "smug" if e != "talk" else e)


QS0, QS1 = di("2008-08-01"), di("2008-11-14")


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["That"] - 0.1:
        pk = back(prog(t, s0 + 0.05, 0.35))
        ctx.save(); ctx.translate(540, 560); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -360, -60, 720, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "SO THE BANDS WORK?", 0, 26, 70, GOLD, 1, HEAD, True, "center")
        ctx.restore()
    elif t < T["bought"] - 0.15:
        r = back(prog(t, T["That"] - 0.1, 0.35))
        big_title(ctx, "THAT SEPTEMBER TRADE?", W / 2, 500, 110, GOLD, r, 980, 0, 14)
    else:
        box = (130, 560, 820, 330)
        k = ease(prog(t, T["bought"] - 0.15, T["Sold"] - T["bought"] + 0.5))
        lo, hi = bb_chart(ctx, box, QS0, QS1, k, t, marks=True, labels=(("AUG 2008", "2008-08-11"), ("NOV 2008", "2008-11-07")))
        tag(ctx, 540, 450, "BOUGHT: SEP 5, 2008", GRNC, back(prog(t, T["bought"] - 0.1, 0.3)), 40, -0.03, C["ink"])
        if t > T["Lehman"] - 0.1:
            sx = sx_of(I_LEH, QS0, QS1, box)
            for j in range(10):
                rect(ctx, sx - 2, box[1] + j * 34, 4, 20, REDC, 0.9)
            tag(ctx, sx + 120, box[1] + 30, "LEHMAN: SEP 15", REDC, back(prog(t, T["Lehman"] - 0.1, 0.3)), 26, 0.03, C["white"])
        if t > T["twentytwo"] - 0.15:
            pk = back(prog(t, T["twentytwo"] - 0.15, 0.35))
            ctx.save(); ctx.translate(560, 1040); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            text(ctx, f"{SEP_R * 100:.1f}%", 0, 0, 130, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
            ctx.restore()
            tag(ctx, 560, 1120, "SOLD OCT 31", C["white"], pk, 30, 0.03, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective" if t < T["bought"] else "fire", lambda e: "shock" if (e != "talk" and t > T["twentytwo"]) else e,
          prop=prop_magnifier if t < T["bought"] else None)


def s_erased(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x10), (0x06, 0x02, 0x04))
    big_title(ctx, "ONE LOSS =", W / 2, 470, 120, C["white"], back(prog(t, s0 + 0.05, 0.35)), 900, -0.03, 14)
    for kk in range(9):
        tt = T["eight"] - 0.3 + kk * 0.08
        pk = back(prog(t, tt, 0.3))
        if pk <= 0:
            continue
        cx = 180 + (kk % 5) * 180; cy = 660 + (kk // 5) * 200
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -70, -70, 140, 140, GRNC if kk < 8 else (0x30, 0x36, 0x40), 1, 20, border=C["ink"])
        text(ctx, "WIN" if kk < 8 else "+", 0, 18, 50, C["ink"], 1, HEAD, True, "center")
        if kk < 8 and t > T["eight"] + 0.6:
            xmark(ctx, 0, 0, 50, C["red"], 12)
        ctx.restore()
    if t > T["eight"] + 0.3:
        tag(ctx, 540, 1110, "MORE THAN 8 AVERAGE WINS", REDC, back(prog(t, T["eight"] + 0.3, 0.3)), 44, 0.02, C["white"])
    bunting(ctx, "THE DAMAGE", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def s_cash(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    stars(ctx, t, 30, 180, 1200, 9, 0.4)
    pts = [(s0 + 0.1, di("2009-06-30")), (T["five"] + 0.3, di("2013-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2013-12-31"), years=(2005, 2008, 2011, 2014))
    tag(ctx, 540, 440, "CASH 4 DAYS OUT OF 5", HCOL, back(prog(t, T["Cash"] - 0.15, 0.3)), 50, -0.03, C["ink"])
    bunting(ctx, "AFTER 2009", t, s0, [C["blue"], C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Winning"] - 0.1:
        a = back(prog(t, T["Winning"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = "85 TRADES · 76% WINNERS · EXIT AT THE UPPER BAND INSTEAD: $35,467"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · MAR 2005 TO 2024 · 85 TRADES", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "BOLLINGER BANDS", money(BB_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "FINAL COUNT", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["WINNING OFTEN", "ISN'T WINNING BIG."], W / 2, 540, T["Winning"] - 0.05, t, STAMP_OR, 880, 70, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["big"] - 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #46", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "bands": s_bands, "wins": s_wins, "crash": s_crash, "remember": s_remember,
            "erased": s_erased, "cash": s_cash, "score": s_score, "verdict": s_verdict, "loop": s_loop}
