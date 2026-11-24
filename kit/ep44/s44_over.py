

# ================================================================ #44 overrides (the 4% rule, retired at the 2007 top)
LCOL = (0xFF, 0x6B, 0x3D)   # A: BROKE / the panicking twin (orange-red)
HCOL = (0x4F, 0xC3, 0xF7)   # B: RICHER / the retiree who stayed (blue)
PAYC = (0xE8, 0xF5, 0xE9)


def paycheck(ctx, cx, cy, s, amount="$40,000", sub="YEAR 1", a=1.0, rot=-0.05):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -250, -110, 500, 220, PAYC, a, 14, border=C["ink"])
    rect(ctx, -250, -110, 500, 44, (0x2E, 0x7D, 0x32), a)
    text(ctx, "PAYCHECK", -228, -76, 32, C["white"], a, HEAD, True, "left")
    text(ctx, sub, 228, -76, 26, C["white"], a, MONO, True, "right")
    text(ctx, "PAY TO: THE RETIREE", -228, -14, 26, C["ink"], a, MONO, True, "left")
    card(ctx, -120, 20, 330, 74, C["white"], a, 8, shadow=False, border=C["ink"])
    text(ctx, amount, 45, 74, fit(ctx, amount, 56, 300, HEAD), (0x0B, 0x8A, 0x4C), a, HEAD, True, "center")
    ctx.restore()


def pay_rain(ctx, t, n=12, a=0.5):
    for k in range(n):
        u = ((t * 0.16) + k / n) % 1
        x = (k * 197) % W + math.sin(t * 1.1 + k) * 30
        paycheck(ctx, x, -100 + u * 2100, 0.2, "$", "", a, math.sin(t + k) * 0.5)


def prop_bag(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 60, y - 110 + math.sin(t * 3) * 6)
    if fl:
        ctx.scale(-1, 1)
    ctx.rotate(math.sin(t * 4) * 0.08)
    ctx.new_path(); ctx.arc(0, 20, 52, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0xC8, 0x9B, 0x5A))); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(6); ctx.stroke()
    rect(ctx, -22, -42, 44, 22, (0xA0, 0x78, 0x40)); 
    text(ctx, "$", 0, 44, 60, (0x0B, 0x8A, 0x4C), 1, HEAD, True, "center")
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev1"]
    tag(ctx, 160, 66, "CASE #44", C["cream"], a, 26, -0.03)
    text(ctx, "MONEY LEFT:", 600, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 615, 38, 360, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$?,???,???", 795, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev1"], 0.35))
        card(ctx, 615, 38, 360, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(LEFT_V), 795, 78, fit(ctx, money(LEFT_V), 36, 340, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["richer"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2008, 2009), x0=None, show=(True, True)):
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
    sers = [x for x, sh_ in zip((VV, PP), show) if sh_]
    vmax = max(1.25e6, 1.12 * float(max(np.nanmax(x[s0_:hi]) for x in sers)))
    vmin = 0.0
    yb = by + bh - (1e6 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, GOLD, 0.45)
    text(ctx, "$1M START", bx + 8, yb - 8, 20, GOLD, 0.8, MONO, True, "left")
    if show[1]:
        xs2, ys2 = series_xy(PP, s0_, xe, up, RBOX, vmin, vmax, 1)
        poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    if show[0]:
        xs1, ys1 = series_xy(VV, s0_, xe, up, RBOX, vmin, vmax, 1)
        poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True)
        mini_rocco(ctx, xs1[-1], ys1[-1] - 4, 4, "tophat", t, "neutral", False, True)
    if show[1]:
        off = 60 if (show[0] and abs(ys1[-1] - ys2[-1]) < 60) else 0
        mini_rocco(ctx, xs2[-1], ys2[-1] - 4 - off, 4, "night", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    labs = [("THE RETIREE", HCOL)] if show[0] else []
    labs += [("HIS TWIN", LCOL)] if show[1] else []
    for k, (lab, col) in enumerate(labs):
        rect(ctx, bx + bw - 250, by + 20 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 215, by + 30 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2016-12-31"); XE3 = di("2020-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x2E, 0x22, 0x06), (0x08, 0x05, 0x01))
    god_rays(ctx, W / 2, 470, t, 0.09, GOLD, 14, 1400)
    for k in range(26):
        u = ((t * 0.25) + k / 26) % 1
        rect(ctx, (k * 151) % W, u * 1500, 4, 36, (0xFF, 0xE0, 0x90), 0.12)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 470); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "$1,000,000", 0, 0, 200, GRNC, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 680); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "RETIRED AT", 0, 0, 150, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "THE TOP", 0, 0, 230, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 1040, "OCT 9, 2007 · S&P 500 RECORD CLOSE", C["cream"], back(prog(tl, 1.0, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if e != "talk" else e, prop=prop_bag)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "tophat", lambda e: "shock", prop=prop_bag)


def evidence(ctx, cx, cy, t, a=1.0, label="HIS TWIN BROTHER", hidden="CASE FILE: SEALED"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["top"], di("2007-11-30"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["And"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.45, T["B"] - 0.6, "BROKE", "RICHER", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["And"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    if t < T["B"] - 0.2:
        paycheck(ctx, 540, 860, 1.0 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "$40,000", "YEAR 1", 1, -0.05 + 0.03 * math.sin(t * 4))
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["And"] else None)


def s_top(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x1A, 0x06), (0x05, 0x04, 0x01))
    a0, a1 = 0, 0
    i0 = int(np.searchsorted(DALL, pd.Timestamp("2006-01-03"))); i1 = int(np.searchsorted(DALL, pd.Timestamp("2007-10-09")))
    box = (130, 560, 820, 330)
    card(ctx, box[0] - 20, box[1] - 20, box[2] + 40, box[3] + 70, (0x0C, 0x10, 0x1C), 0.92, 16, border=C["grey"])
    seg = CLALL[i0:i1 + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
    k = ease(prog(t, s0 + 0.05, 1.6)); up = int(i0 + 2 + (i1 - i0 - 2) * k)
    xs, ys = series_xy(CLALL, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, C["white"], 7, 1, glow=True)
    text(ctx, "2006", box[0] + 30, box[1] + box[3] + 40, 24, C["white"], 0.7, MONO, True, "center")
    text(ctx, "OCT 2007", box[0] + box[2] - 40, box[1] + box[3] + 40, 24, C["white"], 0.7, MONO, True, "center")
    tag(ctx, 540, 450, "OCT 9, 2007", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["record"] - 0.15:
        pk = back(prog(t, T["record"] - 0.15, 0.35))
        ctx.new_path(); ctx.arc(xs[-1], ys[-1], 18 + 4 * math.sin(t * 8), 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD)); ctx.fill()
        ctx.save(); ctx.translate(540, 1060); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, "RECORD CLOSE", 0, 0, 110, GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "DAY ONE", t, s0, [GOLD, C["ink"], C["cream"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


def s_rule(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    big_title(ctx, "THE 4% RULE", W / 2, 480, 140, GRNC, back(prog(t, T["four"] - 0.15, 0.35)), 900, -0.03, 14)
    if t > T["forty"] - 0.15:
        paycheck(ctx, 540, 720, 0.95 * back(prog(t, T["forty"] - 0.15, 0.35)) + 1e-3, "$40,000", "YEAR 1", 1, -0.04)
    if t > T["inflation"] - 0.3:
        tag(ctx, 540, 880, "+ INFLATION, EVERY YEAR", GOLD, back(prog(t, T["inflation"] - 0.3, 0.3)), 40, 0.02, C["ink"])
    for k, (title, col, x, tt) in enumerate((("100% SPY", HCOL, 290, T["All"]), ("HIS TWIN: SAME", LCOL, 790, T["His"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1060); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -230, -55, 460, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 58, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE PLAN", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    if t > T["paychecks"] - 0.2:
        pay_rain(ctx, t, 10, 0.4)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["eleven"], I_LOW), (T["Here"], di("2009-06-01"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "2008: THE CRASH", REDC, back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["white"])
    if t > T["eleven"] - 0.15:
        pk = back(prog(t, T["eleven"] - 0.15, 0.35))
        ctx.save(); ctx.translate(560, 1030); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, "$411K", 0, 0, 130, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
        tag(ctx, 540, 530, "MARCH 9, 2009", C["white"], pk, 40, 0.02, C["ink"])
    if t > T["split"] - 0.15:
        stamp_box(ctx, ["THE TWINS SPLIT"], 540, 1120, T["split"] - 0.1, t, STAMP_OR, 620, 60, -0.05)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], HCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire" if t < T["eleven"] else "none", lambda e: "sad" if e != "talk" else e)


def s_twin(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x08), (0x06, 0x02, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["sold"] - 0.15:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "AND THAT TWIN?", W / 2, 520, 150, LCOL, r, 980, 0, 14)
    else:
        pts = [(T["sold"], I_SOLD), (T["Safe"], di("2012-12-31")), (T["out"], I_BROKE), (T["out"] + 1.2, di("2020-06-30"))]
        race_chart(ctx, t, race_idx(t, pts), XE3, years=(2008, 2012, 2016, 2020), show=(False, True))
        tag(ctx, 540, 440, "SOLD EVERYTHING: NOV 20, 2008", LCOL, back(prog(t, T["sold"] - 0.1, 0.3)), 38, -0.03, C["ink"])
        if t > T["Safe"] - 0.15:
            tag(ctx, 540, 530, "SAFE IN CASH... STILL PAYING HIMSELF", C["white"], back(prog(t, T["Safe"] - 0.15, 0.3)), 30, 0.02, C["ink"])
        if t > T["out"] - 0.1:
            stamp_box(ctx, ["BROKE: APRIL 2019"], 540, 1060, T["out"] - 0.05, t, STAMP_OR, 640, 66, -0.06)
    bunting(ctx, "THE TWIN", t, s0, [LCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if (e != "talk" and t > T["out"]) else e)


def s_comeback(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    sun(ctx, 900, 260, 60, t, 0.5)
    pts = [(s0 + 0.1, di("2009-06-01")), (T["fourteen"], I_BACK)]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=I_BACK + 25, years=(2008, 2010, 2012, 2014, 2016), show=(True, False))
    tag(ctx, 540, 440, "HE NEVER SOLD", HCOL, back(prog(t, s0 + 0.05, 0.3)), 52, -0.03, C["ink"])
    if t > T["fourteen"] - 0.1:
        pk = back(prog(t, T["fourteen"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1100); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -360, -60, 720, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "BACK ABOVE $1M: NOV 2014", 0, 22, fit(ctx, "BACK ABOVE $1M: NOV 2014", 60, 680), GOLD, 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE LONG WAY BACK", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def footnote(ctx, t):
    if t >= T["Worst"] - 0.1:
        a = back(prog(t, T["Worst"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"AT 6% A YEAR: {money(_R['r6'])} LEFT · NEVER TOOK A DIME: {money(_R['bh'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$1M · RETIRED OCT 9, 2007 · 4% RULE", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "MONEY LEFT (END OF 2024)", money(LEFT_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "TAKEN OUT AS PAYCHECKS", money(OUT_V), GRNC, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "END OF 2024", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev1"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["WORST POSSIBLE START.", "STILL RICHER."], W / 2, 540, T["Worst"] - 0.05, t, STAMP_GR, 900, 66, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Still"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #45", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "top": s_top, "rule": s_rule, "crash": s_crash, "twin": s_twin,
            "comeback": s_comeback, "score": s_score, "verdict": s_verdict, "loop": s_loop}
