

# ================================================================ #46 overrides (Dow 50,000: sell the milestone?)
LCOL = (0xFF, 0x9E, 0x2C)   # A: MILESTONE SELLER (orange)
HCOL = (0x4F, 0xC3, 0xF7)   # B: BUY & HOLD (blue)
STONE = (0xB8, 0xBE, 0xC8)
NAVY0, NAVY1 = (0x0C, 0x18, 0x3A), (0x02, 0x05, 0x10)


def milestone(ctx, cx, cy, s, label, a=1.0, col=STONE, rot=0.0, glow=False, t=0.0):
    """a roadside milestone stone (rounded top) with a carved number (original drawing)"""
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    if glow:
        for r_, al in ((150, 0.10), (120, 0.14)):
            ctx.new_path(); ctx.arc(0, -40, r_, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD, al * a * (0.8 + 0.2 * math.sin(t * 5)))); ctx.fill()
    ctx.save(); ctx.translate(10, 12)
    ctx.new_path(); ctx.move_to(-90, 90); ctx.line_to(-90, -40); ctx.arc(0, -40, 90, math.pi, 0); ctx.line_to(90, 90); ctx.close_path()
    ctx.set_source_rgba(0, 0, 0, 0.35 * a); ctx.fill(); ctx.restore()
    ctx.new_path(); ctx.move_to(-90, 90); ctx.line_to(-90, -40); ctx.arc(0, -40, 90, math.pi, 0); ctx.line_to(90, 90); ctx.close_path()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(9); ctx.stroke()
    ctx.new_path(); ctx.arc(-30, -70, 22, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.25 * a); ctx.fill()
    rect(ctx, -110, 84, 220, 22, (0x3A, 0x2A, 0x1A), a)
    text(ctx, label, 0, 10, fit(ctx, label, 64, 150, HEAD), C["ink"], a, HEAD, True, "center")
    ctx.restore()


def prop_stone(ctx, x, y, px, t):
    sw = math.sin(t * 4) * 0.08
    milestone(ctx, x + 75, y - 150, 0.62, "50K", 1, GOLD, -0.15 + sw)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #46", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["seventeen"] + 0.4 - SC["guess"]))
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
    # OUT-OF-MARKET bands (sold at a milestone, waiting 3 months)
    for si, bi in zip(MS_SI, MS_BI):
        if s0_ <= si <= up:
            x1 = sx_of(si, s0_, xe, RBOX); x2 = sx_of(min(bi, up), s0_, xe, RBOX)
            rect(ctx, x1, by, max(3, x2 - x1), bh, LCOL, 0.20 * a)
            rect(ctx, x1, by + bh - 16, max(3, x2 - x1), 16, LCOL, 0.85 * a)
            ctx.save(); ctx.translate(x1, by - 2); ctx.rotate(math.pi / 4)
            rect(ctx, -9, -9, 18, 18, GOLD, a); ctx.restore()
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
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("MILESTONE SELLER", LCOL))):
        rect(ctx, bx + bw - 330, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-06-30"); XE2 = di("2021-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, NAVY0, NAVY1)
    god_rays(ctx, W / 2, 470, t, 0.09, GOLD, 14, 1400)
    for k in range(26):
        u = ((t * 0.25) + k / 26) % 1
        rect(ctx, (k * 151) % W, 1500 - u * 1500, 5, 30, GOLD, 0.12)
    skyline(ctx, 1240, t, 5, (0x10, 0x1C, 0x3C), True)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 330); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "THE DOW", 0, 0, 170, C["white"], 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 610); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "50,000", 0, 0, 270, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    milestone(ctx, 190, 1060, 1.05 * max(p, 1e-3), "50K", 1, STONE, -0.06, True, t)
    if show_tag and tl >= T["SPY"] - 0.15:
        tag(ctx, 540, 800, "SPY HIT 10 ROUND-NUMBER MILESTONES", C["cream"], back(prog(tl, T["SPY"] - 0.15, 0.3)), 34, -0.03)
    if show_tag and tl >= 0.7:
        tag(ctx, 540, 150, "DOW CLOSE NOV 24: 50,018.70", HCOL, back(prog(tl, 0.7, 0.3)), 30, 0.02, C["ink"])


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_stone)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_stone)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE MILESTONE BEFORE 2008", hidden="SPY $1?? · ??? 2007"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -340, -70, 680, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -310, -22, fit(ctx, "EVIDENCE: " + label, 30, 620, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -310, 0, 620, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -310 + ((t * 0.9) % 1) * 620
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["headline"], di("2005-09-30")), (SC["rule"], di("2006-06-30")),
                               (SC["s200"], di("2007-03-30"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.5, T["Hold"] - 0.1, "SELL IT", "HOLD", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["One"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    else:
        milestone(ctx, 540, 820, 1.3, "50K", 1, GOLD, 0.04 * math.sin(t * 3), True, t)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["One"] else None)


def newspaper(ctx, cx, cy, s, head1, head2, a=1.0, rot=-0.05):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -400, -230, 800, 460, (0xF4, 0xEE, 0xDF), a, 10, border=C["ink"])
    text(ctx, "THE DAILY TICKER", 0, -170, 50, C["ink"], a, HEAD, True, "center")
    rect(ctx, -370, -150, 740, 6, C["ink"], a); rect(ctx, -370, -138, 740, 2, C["ink"], a)
    text(ctx, head1, 0, -50, fit(ctx, head1, 110, 720), C["ink"], a, HEAD, True, "center")
    text(ctx, head2, 0, 60, fit(ctx, head2, 80, 720), (0x6A, 0x5A, 0x4A), a, HEAD, True, "center")
    for j in range(5):
        rect(ctx, -370, 110 + j * 22, 340 if j % 2 else 300, 8, (0x9A, 0x90, 0x80), a)
        rect(ctx, 30, 110 + j * 22, 340, 8, (0x9A, 0x90, 0x80), a)
    ctx.restore()


def s_headline(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x1C, 0x36), (0x06, 0x08, 0x12))
    for k, lv in enumerate(MS_LV):
        tt = s0 + 0.1 + k * 0.12
        pk = back(prog(t, tt, 0.3))
        if pk > 0:
            milestone(ctx, 130 + (k % 5) * 205, 520 + (k // 5) * 270, 0.78 * pk, f"${lv}", 1, STONE, (-1) ** k * 0.04)
    q = back(prog(t, T["headline"] - 0.15, 0.35))
    if q > 0:
        newspaper(ctx, 540, 720, q * 1.0, "A NEW ROUND NUMBER!", "RECORD HIGHS EVERYWHERE", 1, -0.04)
    if t > T["top"] - 0.15:
        stamp_box(ctx, ["THE TOP IS IN!"], 540, 1050, T["top"] - 0.1, t, C["red"], 760, 86, -0.07)
    bunting(ctx, "THE HEADLINE", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if (e != "talk" and t > T["top"]) else e)


def s_rule(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x12, 0x30), (0x06, 0x03, 0x0C))
    race_chart(ctx, t, race_idx(t, [(s0, di("2007-03-30")), (s1, di("2007-07-31"))]), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 450, "$10,000 · SPY · FROM 2005", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    for kk, (title, col, x, tt) in enumerate((("MILESTONE: SELL", REDC, 290, T["sells"]), ("3 MONTHS: BUY BACK", GRNC, 790, T["buys"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1080); ctx.rotate(-0.03 if kk == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 50, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["sells"] + 0.25:
        text(ctx, "NEXT OPEN", 290, 1165, 24, C["white"], 0.8, MONO, True, "center", outline=5, ocol=C["ink"])
    if t > T["three"]:
        text(ctx, "63 TRADING DAYS", 790, 1165, 24, C["white"], 0.8, MONO, True, "center", outline=5, ocol=C["ink"])
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


Q14A, Q14B = di("2014-06-02"), di("2015-01-30")


def s_s200(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x22, 0x2A), (0x02, 0x06, 0x08))
    sun(ctx, 920, 250, 55, t, 0.5)
    if t > T["two"] - 0.15:
        tag(ctx, 540, 450, "SPY HITS $200 · AUG 2014", GOLD, back(prog(t, T["two"] - 0.15, 0.3)), 44, -0.03, C["ink"])
    box = (130, 560, 820, 330)
    k = ease(prog(t, s0 + 0.1, T["more"] - s0))
    zoom_chart(ctx, box, Q14A, Q14B, k, t, [(I_14S, "SELL", REDC, T["sells2"] - 0.1), (I_14B, "BUY", GRNC, T["Three"] + 0.3)],
               labels=(("JUN 2014", "2014-06-16"), ("JAN 2015", "2015-01-16")))
    if t > T["sells2"]:
        seg = CL[Q14A:Q14B + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
        yl = box[1] + box[3] - (OP[I_14S] - lo) / (hi - lo) * box[3]
        for j in range(20):
            rect(ctx, box[0] + j * 42, yl - 2, 24, 4, REDC, 0.7)
    if t > T["more"] - 0.12:
        stamp_box(ctx, ["PAID MORE"], 540, 1060, T["more"] - 0.1, t, STAMP_OR, 560, 80, -0.06)
    bunting(ctx, "MILESTONE #2", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "sad" if (e != "talk" and t > T["more"]) else e, prop=prop_flag)


LAD = [(250, T["Two"]), (350, T["threefifty"]), (400, T["four"])]


def s_ladder(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0E, 0x16), (0x08, 0x02, 0x05))
    pts = [(s0 + 0.1, di("2015-01-30")), (T["Seven"], di("2021-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2021-12-31"), years=(2005, 2010, 2015, 2020))
    if t < T["Seven"] - 0.15:
        for k, (lv, tt) in enumerate(LAD):
            pk = back(prog(t, tt - 0.12, 0.35))
            if pk > 0:
                milestone(ctx, 250 + k * 290, 470, 0.62 * pk, f"${lv}", 1, STONE, (-1) ** k * 0.05)
                if t > tt + 0.35:
                    tag(ctx, 250 + k * 290, 540, "HIGHER", REDC, back(prog(t, tt + 0.35, 0.3)), 30, 0.04, C["white"])
    else:
        tag(ctx, 540, 450, "BOUGHT BACK HIGHER", REDC, back(prog(t, T["Seven"] - 0.15, 0.3)), 46, -0.03, C["white"])
    if t > T["Seven"] - 0.1:
        done = [k for k in range(len(MTR)) if "buy" in MTR[k]]
        for j, k in enumerate(done):
            tt = T["Seven"] - 0.1 + j * 0.1
            pk = back(prog(t, tt, 0.3))
            if pk <= 0:
                continue
            cx = 120 + j * 105; cy = 1085
            ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            card(ctx, -46, -46, 92, 92, REDC if MS_HIGHER[k] else (0x30, 0x36, 0x40), 1, 14, border=C["ink"])
            text(ctx, f"{MS_LV[k]}", 0, 12, 34, C["white"], 1, HEAD, True, "center")
            ctx.restore()
    bunting(ctx, "2015-2021", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


QM0, QM1 = di("2007-03-01"), di("2009-04-30")


def m07_chart(ctx, t, k, marks):
    box = (130, 560, 820, 330)
    zoom_chart(ctx, box, QM0, QM1, k, t, marks, labels=(("2007", "2007-06-15"), ("2008", "2008-06-16"), ("2009", "2009-03-02")))
    return box


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["May"] - 0.15:
        r = back(prog(t, s0 + 0.05, 0.35))
        big_title(ctx, "THAT MILESTONE", W / 2, 520, 120, GOLD, r, 980, -0.03, 14)
        big_title(ctx, "BEFORE 2008?", W / 2, 680, 120, C["white"], back(prog(t, s0 + 0.3, 0.35)), 980, 0.02, 14)
        milestone(ctx, 540, 960, 0.9, "$1??", 1, STONE, 0.04 * math.sin(t * 3), True, t)
    else:
        k = ease(prog(t, T["May"] - 0.15, T["cheaper"] + 0.4 - T["May"])) * (di("2007-09-14") - QM0) / (QM1 - QM0)
        m07_chart(ctx, t, k, [(I_M07S, "SELL", REDC, T["sells3"] - 0.1), (I_M07B, "BUY", GRNC, T["cheaper"] - 0.1)])
        tag(ctx, 540, 450, "SPY HITS $150 · MAY 2007", GOLD, back(prog(t, T["May"] - 0.1, 0.3)), 44, -0.03, C["ink"])
        if t > T["cheaper"] - 0.1:
            tag(ctx, 560, 1070, "BOUGHT BACK CHEAPER · AUG 3", GRNC, back(prog(t, T["cheaper"] - 0.1, 0.3)), 40, 0.03, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if (e != "talk" and t > T["cheaper"]) else e, prop=prop_magnifier)


def s_genius(ctx, t, s0, s1):
    if t > T["never"] - 0.2:
        rain_bg(ctx, t)
    else:
        bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    f1 = (di("2007-09-14") - QM0) / (QM1 - QM0); f2 = (I_TOP07 + 8 - QM0) / (QM1 - QM0)
    if t < T["top2"]:
        k = lerp(f1, f2, ease(prog(t, T["August"] - 0.2, T["top2"] - T["August"] + 0.2)))
    else:
        k = lerp(f2, 1.0, ease(prog(t, T["never"] - 0.3, 1.0)))
    box = m07_chart(ctx, t, k, [(I_M07S, "SELL", REDC, 0), (I_M07B, "BUY", GRNC, 0)])
    tag(ctx, 540, 450, "SPY HITS $150 · MAY 2007", GOLD, 1, 44, -0.03, C["ink"])
    if t < T["August"]:
        stamp_box(ctx, ["GENIUS?"], 540, 1060, T["Genius"] - 0.05, t, STAMP_GR, 520, 90, -0.06)
    if t > T["top2"] - 0.15:
        seg = CL[QM0:QM1 + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
        sx = sx_of(I_TOP07, QM0, QM1, box); sy = box[1] + box[3] - (CL[I_TOP07] - lo) / (hi - lo) * box[3]
        pk = back(prog(t, T["top2"] - 0.15, 0.3))
        ctx.new_path(); ctx.arc(sx, sy, 22 * pk + 1e-3, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD)); ctx.set_line_width(6); ctx.stroke()
        tag(ctx, sx + 90, sy - 50, "THE TOP · OCT 2007", GOLD, pk, 26, 0.03, C["ink"])
    if t > T["never"] - 0.15:
        tag(ctx, 540, 1070, "HE RODE THE WHOLE CRASH", REDC, back(prog(t, T["never"] - 0.15, 0.3)), 46, 0.03, C["white"])
    bunting(ctx, "2007-2009", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown" if t < T["August"] else "none", lambda e: ("smug" if t < T["August"] else "sad") if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Round"] - 0.1:
        a = back(prog(t, T["Round"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"BUY BACK AFTER 1 MONTH INSTEAD: {money(VAR['21'])} (WINS) · 6 MONTHS: {money(VAR['126'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024 · 10 MILESTONES", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "MILESTONE SELLER", money(MS_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "THE TOTALS", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["MILESTONES", "AREN'T TOPS."], W / 2, 540, T["Round"] - 0.05, t, STAMP_OR, 820, 80, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Selling"] - 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #47", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "headline": s_headline, "rule": s_rule, "s200": s_s200, "ladder": s_ladder,
            "remember": s_remember, "genius": s_genius, "score": s_score, "verdict": s_verdict, "loop": s_loop}
