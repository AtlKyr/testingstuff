

# ================================================================ #43 overrides (+4.7% day: jump in or wait for the dip?)
LCOL = (0x22, 0xE5, 0x8B)   # A: JUMPS IN (green)
HCOL = (0x4F, 0xC3, 0xF7)   # B: WAITS FOR THE DIP (blue)


def gcandle(ctx, cx, cy, s, col=GRNC, a=1.0, wob=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(wob); ctx.scale(s, s)
    rect(ctx, -6, -150, 12, 300, C["ink"], a)
    card(ctx, -45, -110, 90, 220, col, a, 10, shadow=False, border=C["ink"])
    rect(ctx, -30, -95, 14, 150, C["white"], 0.35 * a)
    ctx.restore()


def prop_candle(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 40, y - 100)
    if fl:
        ctx.scale(-1, 1)
    gcandle(ctx, 0, 0, 0.42, GRNC, 1, math.sin(t * 4) * 0.12)
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #43", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 600, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 615, 38, 340, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 785, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 615, 38, 340, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(A_V), 785, 78, fit(ctx, money(A_V), 36, 320, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["inn"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2008, 2009), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = X0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(12000.0, 1.15 * float(max(np.nanmax(CUMA[s0_:hi]), np.nanmax(CUMB[s0_:hi]))))
    vmin = min(-6000.0, 1.15 * float(min(np.nanmin(CUMA[s0_:hi]), np.nanmin(CUMB[s0_:hi]))))
    yb = by + bh - (0 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$0 PROFIT", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    for i in RI:
        if s0_ <= i <= up:
            xx = sx_of(i, s0_, xe, RBOX)
            card(ctx, xx - 5, by + bh - 34, 10, 26, GRNC, 0.9 * a, 2, shadow=False)
    xs1, ys1 = series_xy(CUMB, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(CUMA, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "detective", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "party", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("B: WAITS FOR THE DIP", HCOL), ("A: JUMPS IN", LCOL))):
        rect(ctx, bx + bw - 330, by + bh - 80 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + bh - 70 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-06-30"); XE2 = di("2021-01-01")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x06, 0x30, 0x1C), (0x01, 0x08, 0x04))
    god_rays(ctx, W / 2, 480, t, 0.09, GRNC, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, 1500 - u * 1500, 4, 40, (0x80, 0xFF, 0xB0), 0.12)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(510 + shake, 500); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "+4.7%", 0, 0, 270, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    arrow_up(ctx, 960, 235 + math.sin(t * 6) * 10, 0.42 * s_, GRNC)
    ctx.save(); ctx.translate(540, 650); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "IN ONE DAY", 0, 0, 110, C["white"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "BUY NOW?", 0, 0, 240, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 1040, "S&P 500 · MONDAY, NOV 23, 2026", C["cream"], back(prog(tl, 1.0, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_candle)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_candle)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE MARCH MORNING", hidden="MAR ??, 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], X0 + 2), (SC["news"], di("2008-02-15"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.45, T["B"] - 0.5, "JUMP IN", "WAIT", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Watch"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    if t < T["B"] - 0.2:
        gcandle(ctx, 540, 860, 1.1 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, GRNC, 1, math.sin(t * 5) * 0.08)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2008, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


def s_news(ctx, t, s0, s1):
    bg_fill(ctx, (0x08, 0x26, 0x18), (0x02, 0x06, 0x04))
    for k in range(3):
        rect(ctx, 0, 300 + k * 6, W, 3, GRNC, 0.25)
    ticker = "S&P 500 +4.73% TO 7,237.17  ·  DOW +1,448 (+3.0%)  ·  NASDAQ +6.5%  ·  7-DAY LOSING STREAK OVER  ·  "
    xo = -((t - s0) * 260) % 2100
    rect(ctx, 0, 1760, W, 64, (0x05, 0x05, 0x05), 0.9)
    for j in range(3):
        text(ctx, ticker, xo + j * 2100, 1805, 34, GOLD, 1, MONO, True, "left")
    tag(ctx, 540, 450, "MONDAY · NOV 23, 2026", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    p = back(prog(t, s0 + 0.1, 0.35))
    big_title(ctx, "S&P 500: +4.7%", W / 2, 620, 150, GRNC, p, 980, -0.03, 16)
    text(ctx, "CLOSE 7,237.17", W / 2, 720, 44, C["white"], p, MONO, True, "center", outline=6, ocol=C["ink"])
    for j in range(5):
        hh = 80 + j * 35
        gcandle(ctx, 300 + j * 120, 930 - hh * 0.3, 0.4 + 0.12 * j * back(prog(t, s0 + 0.2 + j * 0.12, 0.3)) + 1e-3, GRNC if j == 4 else REDC, 1, 0)
    if t > T["best"] - 0.15:
        tag(ctx, 540, 1110, "BEST DAY SINCE APRIL 2025", GOLD, back(prog(t, T["best"] - 0.15, 0.3)), 50, 0.02, C["ink"])
    bunting(ctx, "THE NEWS", t, s0, [GRNC, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


def s_count(ctx, t, s0, s1):
    grid_bg(ctx, (0x0E, 0x2A, 0x1E), (0x05, 0x10, 0x0A))
    tag(ctx, 540, 440, "SPY: UP 4% OR MORE IN ONE DAY", GRNC, back(prog(t, s0 + 0.05, 0.3)), 42, -0.03, C["ink"])
    # 27 candles, one per monster day, grouped by year
    yrs = [x["day"][:4] for x in ROWS]
    for k in range(27):
        tt = s0 + 0.15 + k * (T["twentyseven"] - s0 - 0.1) / 27
        pk = back(prog(t, tt, 0.25))
        if pk <= 0:
            continue
        cx = 150 + (k % 9) * 97; cy = 610 + (k // 9) * 175
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        gcandle(ctx, 0, 0, 0.36, GRNC)
        text(ctx, yrs[k], 0, 82, 22, C["white"], 0.85, MONO, True, "center")
        ctx.restore()
    if t > T["twentyseven"] - 0.1 and t < T["twins"] - 0.15:
        pk = back(prog(t, T["twentyseven"] - 0.1, 0.35))
        big_title(ctx, "27 TIMES", W / 2, 1110, 120, GOLD, pk, 700, -0.04, 14)
    if t > T["twins"] - 0.15:
        pk = back(prog(t, T["twins"] - 0.15, 0.35))
        for k, (lab, col, x) in enumerate((("A", LCOL, 330), ("B", HCOL, 750))):
            ctx.save(); ctx.translate(x, 1080); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            card(ctx, -170, -60, 340, 120, col, 1, 22, border=C["ink"])
            text(ctx, lab, -105, 40, 110, C["ink"], 1, HEAD, True, "center")
            text(ctx, "$10,000", 45, 20, fit(ctx, "$10,000", 52, 190, MONO), C["ink"], 1, MONO, True, "center")
            ctx.restore()
    bunting(ctx, "THE CASE FILE", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "shock" if (e != "talk" and t > T["twentyseven"]) else e)


def rule_diagram(ctx, t, t0, cx=540, cy=760):
    """schematic: a jump, the dashed START line, the price falls back below it -> B's buy dot"""
    k = ease(prog(t, t0, 1.6))
    pts = [(-380, 60), (-300, 70), (-220, 50), (-200, -150), (-100, -130), (0, -60), (80, 40), (160, 110), (260, 80), (380, -40)]
    card(ctx, cx - 440, cy - 230, 880, 400, (0x0C, 0x10, 0x1C), 0.9, 16, border=C["grey"])
    for j in range(24):
        rect(ctx, cx - 400 + j * 34, cy + 55, 20, 4, GOLD, 0.8)
    text(ctx, "THE START", cx - 400, cy + 95, 26, GOLD, 1, MONO, True, "left")
    n = max(2, int(len(pts) * k) + 1)
    ctx.new_path(); ctx.move_to(cx + pts[0][0], cy + pts[0][1])
    for x_, y_ in pts[1:n]:
        ctx.line_to(cx + x_, cy + y_)
    ctx.set_source_rgba(*rgba(C["white"])); ctx.set_line_width(8); ctx.stroke()
    if n >= 4:
        text(ctx, "+4%", cx - 260, cy - 170, 44, GRNC, 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        ctx.new_path(); ctx.arc(cx - 100, cy - 130, 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(LCOL)); ctx.fill()
        text(ctx, "A BUYS", cx - 100, cy - 160, 28, LCOL, 1, MONO, True, "center", outline=5, ocol=C["ink"])
    if n >= 8:
        ctx.new_path(); ctx.arc(cx + 120, cy + 75, 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(HCOL)); ctx.fill()
        text(ctx, "B BUYS", cx + 190, cy + 140, 28, HCOL, 1, MONO, True, "center", outline=5, ocol=C["ink"])


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 440, "THE RULES", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 46, -0.03, C["ink"])
    rule_diagram(ctx, t, s0 + 0.1)
    for k, (title, col, x, tt) in enumerate((("A: NEXT MORNING", LCOL, 290, T["A2"]), ("B: BELOW THE START", HCOL, 790, T["drop"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1060); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 56, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["year"] - 0.15:
        tag(ctx, 540, 1140, "SCORED 1 YEAR LATER", GOLD, back(prog(t, T["year"] - 0.15, 0.3)), 34, 0.02, C["ink"])
    bunting(ctx, "THE RULES", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2008-02-15")), (T["every"] + 0.4, di("2008-12-31")), (T["ahead"], di("2009-02-27"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2008, 2009))
    tag(ctx, 540, 440, "2008: THE DIP CAME BACK EVERY TIME", HCOL, back(prog(t, s0 + 0.05, 0.3)), 38, -0.03, C["ink"])
    if t > T["pulls"] - 0.15:
        tag(ctx, 540, 530, "B PULLS WAY AHEAD", HCOL, back(prog(t, T["pulls"] - 0.15, 0.3)), 50, 0.02, C["ink"])
    bunting(ctx, "ROUND 1-11", t, s0, [C["red"], C["ink"], HCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


def s_rounds(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x05, 0x0C))
    stars(ctx, t, 30, 180, 1200, 9, 0.4)
    nb = 0
    for k in range(27):
        tt = s0 + 0.2 + k * (T["rounds"] - s0 - 0.1) / 27
        on = t >= tt
        cx = 150 + (k % 9) * 97; cy = 520 + (k // 9) * 120
        col = (HCOL if WINB[k] else LCOL) if on else (0x30, 0x36, 0x40)
        if on and WINB[k]:
            nb += 1
        pk = 1 + 0.25 * (1 - ease(prog(t, tt, 0.25))) if on else 1
        ctx.save(); ctx.translate(cx, cy); ctx.scale(pk, pk)
        card(ctx, -42, -42, 84, 84, col, 1, 12, shadow=False, border=C["ink"])
        text(ctx, "B" if (on and WINB[k]) else ("A" if on else "?"), 0, 18, 50, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
        if k % 9 == 0:
            text(ctx, ROWS[k]["day"][:4], 60, cy + 10, 22, C["white"], 0.7, MONO, True, "center")
    pk = back(prog(t, s0 + 0.1, 0.3))
    ctx.save(); ctx.translate(540, 440); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
    card(ctx, -330, -50, 660, 100, (0x05, 0x05, 0x05), 0.92, 18, shadow=False, border=HCOL)
    text(ctx, f"B WINS {nb} OF 27 ROUNDS", 0, 20, fit(ctx, "B WINS 19 OF 27 ROUNDS", 60, 620), HCOL, 1, HEAD, True, "center")
    ctx.restore()
    if t > T["So"] - 0.15:
        q = back(prog(t, T["So"] - 0.15, 0.35))
        ctx.save(); ctx.translate(540, 950); ctx.rotate(-0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -340, -60, 680, 120, GOLD, 1, 22, border=C["ink"])
        text(ctx, "SO PATIENCE PAYS?", 0, 26, 70, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "ALL 27 ROUNDS", t, s0, [HCOL, C["ink"], C["grey"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


QM0, QM1 = di("2009-02-02"), di("2010-03-12")


def start_line(ctx, box, i0, i1, lvl, col=GOLD, label="THE START"):
    bx, by, bw, bh = box
    seg = CL[i0:i1 + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
    yy = by + bh - (lvl - lo) / (hi - lo) * bh
    for j in range(int(bw / 34)):
        rect(ctx, bx + j * 34, yy - 2, 20, 4, col, 0.9)
    text(ctx, label, bx + bw - 10, yy + 34, 24, col, 1, MONO, True, "right", outline=4, ocol=C["ink"])
    return lo, hi


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["bottom"] - 0.15:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "THAT MARCH MORNING?", W / 2, 470, 120, GOLD, r, 980, 0, 14)
        if t > T["Two2"] - 0.15:
            pk = back(prog(t, T["Two2"] - 0.15, 0.35))
            cal_page(ctx, 540, 820, 0.9 * pk + 1e-3, "MAR 2009" if t > T["nine"] - 0.1 else "MAR 20??", "10", 1, -0.06 + 0.03 * math.sin(t * 4))
    else:
        box = (130, 560, 820, 330)
        k = ease(prog(t, T["bottom"] - 0.15, 1.4))
        zoom_chart(ctx, box, QM0, QM1, k, t, [(I_M09 + 1, "A BUYS", LCOL, T["bottom"])],
                   labels=(("MAR 2009", "2009-03-10"), ("MAR 2010", "2010-03-01")))
        start_line(ctx, box, QM0, QM1, CL[I_M09P], GOLD, "THE START: MAR 9 CLOSE")
        tag(ctx, 540, 450, "MAR 10, 2009 · +6% · A DAY AFTER THE BOTTOM", C["cream"], back(prog(t, T["bottom"] - 0.1, 0.3)), 32, -0.03, C["ink"])
        if t > T["never"] - 0.1:
            stamp_box(ctx, ["THE DIP NEVER CAME"], 540, 1010, T["never"] - 0.05, t, STAMP_OR, 760, 60, -0.06)
        if t > T["cash"] - 0.15:
            hourglass(ctx, 900, 1110, 0.4, t)
            tag(ctx, 540, 1120, "B: IN CASH ALL YEAR", HCOL, back(prog(t, T["cash"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective" if t < T["bottom"] else "night", lambda e: "shock" if (e != "talk" and t > T["never"]) else e,
          prop=prop_magnifier if t < T["bottom"] else None)


QT0, QT1 = di("2020-03-02"), di("2021-04-09")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    tag(ctx, 540, 450, "MARCH 24 + APRIL 6, 2020", C["white"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    box = (130, 560, 820, 330)
    k = ease(prog(t, s0 + 0.1, 1.3))
    zoom_chart(ctx, box, QT0, QT1, k, t, [(I_M24 + 1, "A BUYS", LCOL, s0 + 0.5), (I_A06 + 1, "A BUYS", LCOL, s0 + 0.9)],
               labels=(("MAR 2020", "2020-03-10"), ("APR 2021", "2021-04-01")))
    start_line(ctx, box, QT0, QT1, CL[I_M24 - 1], GOLD, "START: MAR 23")
    if t > T["same"] - 0.15:
        stamp_box(ctx, ["NO DIP. AGAIN."], 540, 1060, T["same"] - 0.1, t, STAMP_OR, 620, 64, -0.05)
    bunting(ctx, "2020", t, s0, [C["blue"], C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Twenty2"] - 0.1:
        a = back(prog(t, T["Twenty2"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"WAIT MAX 1 MONTH, THEN BUY ANYWAY: {money(_R['var']['21'])} · WAITING WINS"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "27 ROUNDS · $10,000 EACH · 1 YEAR", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "A: JUMPED IN", money(A_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "B: WAITED FOR THE DIP", money(B_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "ALL ROUNDS ADDED UP", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["20 DIPS CAME BACK.", "7 DIDN'T: THE BOTTOM WAS IN."], W / 2, 540, T["Twenty2"] - 0.05, t, STAMP_GR, 940, 60, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["bottom2"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #44", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "news": s_news, "count": s_count, "rules": s_rules, "y2008": s_y2008,
            "rounds": s_rounds, "remember": s_remember, "y2020": s_y2020, "score": s_score, "verdict": s_verdict, "loop": s_loop}
