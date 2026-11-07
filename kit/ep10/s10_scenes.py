# ================================================================ Autopsy #10 scenes (buy after 3 red days)
HCOL = (0x4F, 0xC3, 0xF7)    # HOLDER (buy & hold)
PCOL = (0xFF, 0x9F, 0x1C)    # PANIC BUYER (3 red closes -> buy)
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x2A, 0x0C, 0x16), (0x08, 0x03, 0x06)


def candle(ctx, x, y, w, h, col, a=1.0, wick=40):
    rect(ctx, x + w / 2 - 4, y - wick, 8, h + 2 * wick, C["ink"], a)
    card(ctx, x, y, w, h, col, a, 8, shadow=False, border=C["ink"])


def red_stairs(ctx, x0, y0, s, t, a=1.0, n=3, lit=3):
    """three red candles stepping down"""
    for k in range(n):
        wob = math.sin(t * 3 + k) * 4
        candle(ctx, x0 + k * 110 * s, y0 + k * 90 * s + wob, 70 * s, 170 * s, REDC if k < lit else (0x55, 0x2A, 0x33), a, 34 * s)


def arrow_up(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.new_path()
    ctx.move_to(0, -90); ctx.line_to(70, -10); ctx.line_to(28, -10); ctx.line_to(28, 80); ctx.line_to(-28, 80); ctx.line_to(-28, -10)
    ctx.line_to(-70, -10); ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke(); ctx.restore()


def arrow_down(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, -s); ctx.restore()
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.pi); arrow_up(ctx, 0, 0, s, col, a); ctx.restore()


def sticker(ctx, t, t0, t1, kind):
    """comment prompt sticker (visual only). kind: 'guess' or 'right'. Centre y=1085 (captions sit at ~1240)."""
    if not (t0 - 0.01 <= t <= t1):
        return
    p = back(prog(t, t0, 0.35)) * (1 - ease(prog(t, t1 - 0.25, 0.25)))
    if p <= 0:
        return
    wob = 1 + 0.03 * math.sin(t * 9)
    ctx.save(); ctx.translate(W / 2, 1085); ctx.rotate(-0.035); ctx.scale(max(p * wob, 1e-3), max(p * wob, 1e-3))
    if kind == "guess":
        card(ctx, -440, -62, 880, 124, GOLD, 1, 26, border=C["ink"])
        text(ctx, "COMMENT YOUR GUESS", -395, 22, 58, C["ink"], 1, HEAD, True, "left")
        bob = math.sin(t * 10) * 8
        ar = 0.36
        ctx.save(); ctx.translate(205, bob); arrow_down(ctx, 0, 0, ar, C["red"]); ctx.restore()
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


def hud(ctx, t):
    a = ease(prog(t, T["And1"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev1"]
    tag(ctx, 160, 66, "CASE #10", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev1"], 0.35))
        card(ctx, 655, 38, 300, 54, C["green"], a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - T["And1"]) / (T["money"] - T["And1"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: 3 RED DAYS. BUY?)
def hook_draw(ctx, t, tl):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 760, t, 0.06, C["red"], 14, 1400)
    # falling red candles in the background
    for k in range(7):
        u = (t * 0.25 + k / 7) % 1
        candle(ctx, (k * 157 + 60) % (W - 60), -220 + u * 1700, 46, 110, REDC, 0.18, 26)
    red_stairs(ctx, 600, 980, 1.0, t, 0.9)
    rect(ctx, 0, 0, W, H, BG1, 0.25)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    hl = 1 + 0.1 * math.sin(math.pi * prog(tl, T["three1"] - 0.1, 0.5))
    s_ = max(p * sc * wob * hl, 1e-3)
    ctx.save(); ctx.translate(540, 470); ctx.rotate(-0.04); ctx.scale(s_, s_)
    sz = fit(ctx, "3 RED DAYS", 210, 980)
    text(ctx, "3 RED DAYS", 0, 0, sz, REDC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    hb = 1 + 0.12 * math.sin(math.pi * prog(tl, T["buy1"] - 0.1, 0.5))
    s2 = max(p * sc * wob * hb, 1e-3)
    ctx.save(); ctx.translate(420, 830); ctx.rotate(0.04); ctx.scale(s2, s2)
    text(ctx, "BUY?", 0, 0, 300, GRNC, 1, HEAD, True, "center", outline=28, ocol=C["ink"])
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    tag(ctx, 800, 1110, "IN A ROW", C["cream"], back(prog(t, T["row"] - 0.05, 0.3)), 40, 0.04)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 guess: buy the panic or just hold?
def chair(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    col = (0x8B, 0x5A, 0x2B)
    rect(ctx, -50, -90, 16, 150, col); rect(ctx, 34, -10, 16, 70, col); rect(ctx, -50, -10, 100, 18, col)
    rect(ctx, -50, -90, 90, 14, col); rect(ctx, -50, -60, 90, 10, col)
    ctx.restore()


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(20):
        u = ((t - s0) * 0.45 + k / 20) % 1
        candle(ctx, (k * 211) % W, 1300 - u * 1150, 30, 70, REDC if k % 3 else GRNC, 0.25 * (1 - u), 16)
    if t < T["years"] - 0.05:
        text(ctx, "WHO WINS?", W / 2, 430, 96, C["white"], back(prog(t, s0 + 0.05, 0.3)), HEAD, True, "center", outline=14, ocol=C["ink"])
    else:
        tag(ctx, W / 2, 400, "20 YEARS", C["cream"], back(prog(t, T["years"] - 0.05, 0.3)), 44, -0.03)
        if t >= T["flipping"] - 0.1:
            tag(ctx, W / 2, 490, "THE LEAD KEPT FLIPPING", GOLD, back(prog(t, T["flipping"] - 0.1, 0.3)), 36, 0.02)
    g = back(prog(t, s0 + 0.08, 0.35))
    if g > 0:
        ctx.save(); ctx.translate(W / 2, 790); ctx.scale(max(g, 1e-3), max(g, 1e-3))
        card(ctx, -470, -230, 940, 460, C["dark"], 1, 22, border=C["white"])
        text(ctx, "YOUR GUESS?", 0, -160, 50, GOLD, 1, HEAD, True, "center")
        blink = int(t * 4) % 2
        for k, (lab, col, fg, x, tt) in enumerate((("A  BUY THE PANIC", PCOL, C["ink"], -225, T["panic1"]),
                                                   ("B  JUST HOLD", HCOL, C["ink"], 225, T["hold"]))):
            on = (blink == k)
            hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
            fl = prog(t, T["flipping"] + k * 0.15, 0.5)       # cards flip over on "flipping"
            fx = abs(math.cos(fl * 2 * math.pi)) if 0 < fl < 1 else 1.0
            ctx.save(); ctx.translate(x, 60); ctx.scale(hl * max(fx, 0.04), hl)
            card(ctx, -205, -170, 410, 300, col, 1, 18, border=C["white"] if on else C["ink"])
            if k == 0:
                red_stairs(ctx, -150, -150, 0.55, t, 1.0)
                arrow_up(ctx, 120, -60, 0.6, GRNC)
            else:
                chair(ctx, 0, -40, 1.2, t)
                mini_rocco(ctx, -10, -30, 5, "tophat", t, "smug", False, False)
            text(ctx, lab, 0, 100, fit(ctx, lab, 56, 380), fg, 1, HEAD, True, "center")
            ctx.restore()
        ctx.restore()
    sticker(ctx, t, T["guess"] - 0.15, T["guess"] + 2.2, "guess")
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["hold"]) else e)


# ---------------------------------------------------------------- 3 rules: two big icons
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    for k, (title, l1, col, fg, y, tt, t2) in enumerate((("BUY", "3 RED CLOSES", GRNC, C["ink"], 520, T["three2"], T["buy2"]),
                                                         ("SELL", "FIRST GREEN CLOSE", REDC, C["white"], 900, T["First"], T["sell"]))):
        p = back(prog(t, tt - 0.12, 0.4))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.025 if k == 0 else 0.025); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -460, -160, 920, 320, col, 1, 22, border=C["ink"])
        card(ctx, -430, -130, 260, 260, C["dark"], 1, 16, shadow=False)
        if k == 0:
            nl = sum(1 for j in range(3) if t >= tt + j * 0.12)
            red_stairs(ctx, -410, -95, 0.62, t, 1.0, 3, nl)
        else:
            candle(ctx, -330, -60, 70, 150, GRNC, 1, 30)
        q = back(prog(t, t2 - 0.08, 0.3))
        big = 1 + 0.1 * math.sin(math.pi * prog(t, t2 - 0.05, 0.4))
        ctx.save(); ctx.translate(140, -30); ctx.scale(big, big)
        text(ctx, l1, 0, 0, fit(ctx, l1, 70, 560), fg, 1, HEAD, True, "center", outline=6 if k else 0, ocol=C["ink"])
        ctx.restore()
        if q > 0:
            ctx.save(); ctx.translate(140, 80); ctx.scale(max(q, 1e-3), max(q, 1e-3))
            card(ctx, -280, -50, 560, 100, C["dark"], 1, 14, shadow=False)
            lab = ("BUY" if k == 0 else "SELL") + " NEXT OPEN"
            text(ctx, lab, 0, 18, fit(ctx, lab, 54, 520), GRNC if k == 0 else C["red"], 1, HEAD, True, "center")
            ctx.restore()
        ctx.restore()
    tag(ctx, 780, 1120, "SPY · 2005-2024", C["cream"], back(prog(t, T["sell"] + 0.15, 0.3)), 34, 0.04)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab")


# ---------------------------------------------------------------- 4 race start: panic buyer vs holder
def s_start(ctx, t, s0, s1):
    stadium(ctx, t)
    for k in range(2):
        y = 820 + k * 200
        rect(ctx, 0, y, W, 150, (0xB8, 0x4A, 0x32))
        rect(ctx, 0, y, W, 6, C["white"]); rect(ctx, 0, y + 144, W, 6, C["white"])
    rect(ctx, 250, 820, 16, 350, C["white"])
    go = t >= T["holder"] + 0.2
    for k, (cos, col, lab, tt) in enumerate((("race", PCOL, "PANIC BUYER", T["Panic"]), ("tophat", HCOL, "HOLDER", T["holder"]))):
        run = prog(t, T["holder"] + 0.2, 2.0)
        x = 180 + ease_io(run) * 420
        mini_rocco(ctx, x, 950 + k * 200, 7, cos, t + k * 0.3, "smug" if go else "neutral", False, go)
        tag(ctx, x + 10, 810 + k * 200, lab, col, back(prog(t, tt - 0.05, 0.3)), 30, 0.02, C["ink"])
    q = back(prog(t, T["Ten"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(500, 560); ctx.rotate(0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        coin(ctx, -190, 0, 70, t)
        text(ctx, "$10,000", 60, 22, 76, GOLD, 1, MONO, True, "center", outline=8, ocol=C["ink"])
        text(ctx, "EACH", 60, 84, 34, C["white"], 1, MONO, True, "center", outline=5, ocol=C["ink"])
        ctx.restore()
    tag(ctx, 540, 700, "VS", C["red"], back(prog(t, T["versus"] - 0.05, 0.3)), 44, -0.05, C["white"])
    stamp_box(ctx, ["GO!"], 860, 420, T["holder"] + 0.15, t, C["green"], 280, 100, -0.08)
    bunting(ctx, "THE RACE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "race", prop=prop_flag)


# ---------------------------------------------------------------- 5-6 race chart (2005 -> 2011, then a curtain hides 2012+)
RBOX = (110, 620, 860, 420)
CUT = "2011-12-30"


def race_idx(t):
    pts = [(SC["crash08"] + 0.15, 0), (T["collapses"], di("2008-09-01")), (T["lead"] + 0.4, di("2008-12-31")),
           (SC["lead"] + 0.1, di("2008-12-31")), (T["ten1"] + 0.3, di("2010-12-31")), (T["eleven"] + 0.4, di(CUT))]
    if t <= pts[0][0]:
        return 1
    for (a, ia), (b, ib) in zip(pts, pts[1:]):
        if t <= b:
            return int(ia + (ib - ia) * ease_io((t - a) / max(1e-3, b - a)))
    return pts[-1][1]


def race_chart(ctx, t, zones=(), curtain=None):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), 0, N - 1, RBOX); x1 = sx_of(di(d1), 0, N - 1, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    up = race_idx(t)
    vmax = max(15000.0, 1.32 * float(max(np.nanmax(SV[:up + 1]), np.nanmax(JV[:up + 1]))))
    vmin = 6000.0
    tips = []
    for arr, col, w_ in ((SV, HCOL, 8), (JV, PCOL, 8)):
        xs, ys = series_xy(arr, 0, N - 1, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, w_, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (px_, py_) = tips
    lead_p = JV[up] > SV[up]
    off = 0 if abs(hy - py_) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_p else 0), 4, "tophat", t, "sad" if lead_p else "smug", False, True)
    mini_rocco(ctx, px_, py_ - 4 - (0 if lead_p else off), 4, "race", t, "smug" if lead_p else "neutral", False, True)
    if curtain is not None and curtain > 0:
        xc = sx_of(di("2012-01-01"), 0, N - 1, RBOX)
        hh = (RBOX[3] + 60) * ease(curtain)
        ctx.save(); ctx.rectangle(xc, RBOX[1] - 30, RBOX[0] + RBOX[2] + 30 - xc, hh); ctx.clip()
        rect(ctx, xc, RBOX[1] - 30, RBOX[0] + RBOX[2] + 30 - xc, RBOX[3] + 60, (0x05, 0x05, 0x05))
        for j in range(14):          # caution stripes
            ctx.save(); ctx.translate(xc + j * 60 - 40, RBOX[1] - 30); ctx.rotate(0.6)
            rect(ctx, 0, 0, 22, 70, GOLD, 0.9); ctx.restore()
        cx = (xc + RBOX[0] + RBOX[2] + 30) / 2
        text(ctx, "CLASSIFIED", cx, RBOX[1] + 170, 66, C["red"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        qs = 1 + 0.1 * math.sin(t * 7)
        ctx.save(); ctx.translate(cx, RBOX[1] + 330); ctx.scale(qs, qs)
        text(ctx, "?", 0, 0, 170, GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"]); ctx.restore()
        ctx.restore()
    # legend (bottom-right inside the box)
    for k, (lab, col) in enumerate((("PANIC BUYER", PCOL), ("HOLDER", HCOL))):
        rect(ctx, RBOX[0] + 150 + k * 330, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 196 + k * 330, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")


def s_crash08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.22)])
    tag(ctx, 540, 440, "2008 CRASH", C["red"], back(prog(t, T["Two"], 0.3)), 38, -0.03, C["white"])
    tag(ctx, 540, 524, "PANIC BUYER TAKES THE LEAD", PCOL, back(prog(t, T["lead"] - 0.2, 0.3)), 34, 0.02)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], C["red"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["collapses"]) else e)


def s_lead(ctx, t, s0, s1):
    why = T["So"] - 0.05 <= t < T["Tw12"] - 0.05
    if why:
        bg_fill(ctx, (0x3A, 0x0E, 0x2A), (0x0A, 0x02, 0x08))
        god_rays(ctx, W / 2, 470, t, 0.09, GOLD, 14, 1400)
    else:
        stadium(ctx, t)
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.10)], curtain=prog(t, T["twelve"] - 0.1, 0.5))
    if t < T["So"] - 0.05:
        yl = "2010" if t < T["Tw11"] - 0.05 else "2010 · 2011"
        tag(ctx, 540, 440, yl, C["cream"], back(prog(t, T["Tw10"], 0.3)), 38, -0.03)
        tag(ctx, 540, 524, "STILL LEADING", PCOL, back(prog(t, T["Still"] - 0.05, 0.3)), 38, 0.02)
    elif why:
        p = back(prog(t, T["So"] - 0.05, 0.3))
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, T["nobody"] - 0.05, 0.45))
        ctx.save(); ctx.translate(W / 2, 455); ctx.rotate(-0.03); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
        text(ctx, "SO WHY DOES", 0, -40, 84, C["white"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
        text(ctx, "NOBODY DO THIS?", 0, 60, 84, GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
        ctx.restore()
    else:
        tag(ctx, 540, 440, "2012", C["cream"], back(prog(t, T["Tw12"] - 0.05, 0.3)), 38, -0.03)
        tag(ctx, 540, 524, "SOMETHING CHANGES...", C["red"], back(prog(t, T["something"] - 0.05, 0.3)), 38, 0.02, C["white"])
    bunting(ctx, "THE LEAD", t, s0, [PCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: ("shock" if t > T["twelve"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 7 covid 2020 (zoomed: % from 2019 close)
CBOX = (110, 620, 860, 420)
_c20 = slice(di("2019-12-31"), di("2020-12-31") + 1)
C_H = SV[_c20] / SV[_c20][0]; C_P = JV[_c20] / JV[_c20][0]; C_N = len(C_H)
C_MIN = float(min(C_H.min(), C_P.min())) - 0.04; C_MAX = float(max(C_H.max(), C_P.max())) + 0.06


def s_covid(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x3A), (0x0A, 0x04, 0x12))
    stars(ctx, t, 40, 0, 1300, 7)
    card(ctx, CBOX[0] - 30, CBOX[1] - 30, CBOX[2] + 60, CBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    i0 = di("2019-12-31")
    x0 = sx_of(di("2020-02-19") - i0, 0, C_N - 1, CBOX); x1 = sx_of(di("2020-03-23") - i0, 0, C_N - 1, CBOX)
    rect(ctx, x0, CBOX[1], x1 - x0, CBOX[3], C["purple"], 0.45)
    yb = sy_of(1.0, C_MIN, C_MAX, CBOX)
    for k in range(18):
        rect(ctx, CBOX[0] + k * 48, yb, 28, 3, C["white"], 0.5)
    text(ctx, "START OF 2020", CBOX[0] + 10, yb + 34, 22, C["white"], 0.7, MONO, True, "left")
    for m, lab in ((1, "JAN"), (3, "MAR"), (6, "JUN"), (9, "SEP"), (12, "DEC")):
        text(ctx, lab, sx_of(di(f"2020-{m:02d}-01") - i0, 0, C_N - 1, CBOX), CBOX[1] + CBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    up = int((C_N - 1) * ease_io(prog(t, s0 + 0.2, T["rebound"] + 0.3 - s0 - 0.2)))
    up = max(up, 1)
    tips = []
    for arr, col in ((C_H, HCOL), (C_P, PCOL)):
        xs, ys = series_xy(arr, 0, C_N - 1, up, CBOX, C_MIN, C_MAX, 1)
        poly(ctx, xs, ys, col, 8, 1, glow=True); tips.append((xs[-1], ys[-1]))
    mini_rocco(ctx, tips[0][0], tips[0][1] - 4, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, tips[1][0], tips[1][1] - 4 - (50 if abs(tips[0][1] - tips[1][1]) < 50 else 0), 4, "race", t, "neutral", False, True)
    for k, (lab, col) in enumerate((("PANIC BUYER", PCOL), ("HOLDER", HCOL))):
        rect(ctx, CBOX[0] + 150 + k * 330, CBOX[1] + CBOX[3] + 87, 36, 10, col)
        text(ctx, lab, CBOX[0] + 196 + k * 330, CBOX[1] + CBOX[3] + 101, 26, col, 1, MONO, True, "left")
    tag(ctx, 540, 440, "2020: COVID", C["purple"], back(prog(t, T["Covid"] - 0.05, 0.3)), 38, -0.03, C["white"])
    lab = "...AND MISSES THE REBOUND" if t >= T["misses"] - 0.05 else "DODGES THE CRASH"
    tag(ctx, 540, 524, lab, PCOL, back(prog(t, T["dodges"] - 0.05, 0.3)), 36, 0.02)
    bunting(ctx, "2020", t, s0, [C["purple"], C["ink"], C["purple"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: ("sad" if t > T["misses"] else "neutral") if e != "talk" else e)


# ---------------------------------------------------------------- 8 the catch: the bounce is real (bars, no numbers)
def s_catch(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x05, 0x08), (0x02, 0x01, 0x02))
    for i in range(0, W, 80):
        rect(ctx, (i + t * 60) % (W + 80) - 80, 0, 2, H, C["red"], 0.10)
    if t < T["edge"] - 0.05:
        text(ctx, "HERE'S THE CATCH", W / 2, 440, 92, C["red"], back(prog(t, T["catch"] - 0.15, 0.3)), HEAD, True, "center", outline=14, ocol=C["ink"])
    stamp_box(ctx, ["THE EDGE IS REAL."], W / 2, 430, T["edge"] - 0.05, t, C["green"], 820, 84, -0.05)
    card(ctx, 90, 540, 900, 590, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    text(ctx, "CHANCE THE NEXT DAY IS GREEN", W / 2, 600, 32, C["white"], ease(prog(t, T["After"] - 0.1, 0.3)), MONO, True, "center")
    base, hmax = 1040, 320
    for k, (lab, v, col, x, tt) in enumerate((("ANY DAY", UPB, C["grey"], 320, T["After"]), ("AFTER 3 RED DAYS", UP3, GRNC, 760, T["bounce1"]))):
        g = ease_io(prog(t, tt, 0.7))
        h = hmax * v / 60.0 * g
        card(ctx, x - 130, base - h, 260, max(h, 4), col, 1, 12, shadow=False, border=C["ink"])
        text(ctx, lab, x, base + 52, fit(ctx, lab, 36, 400), col, 1, HEAD, True, "center", outline=5, ocol=C["ink"])
    rect(ctx, 130, base, 820, 4, C["white"], 0.6)
    if t >= T["bounce1"] + 0.5:
        ytop = base - hmax * UP3 / 60.0
        a = ease(prog(t, T["bounce1"] + 0.5, 0.3))
        for k in range(16):
            rect(ctx, 190 + k * 48, ytop, 28, 4, GOLD, a)
        tag(ctx, 540, ytop - 50, "BOUNCES MORE OFTEN", GOLD, back(prog(t, T["often"] - 0.1, 0.3)), 32, -0.03)
    bunting(ctx, "THE CATCH", t, s0, [C["red"], C["ink"], C["red"], GOLD])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if (e != "talk" and t > T["edge"]) else e)


# ---------------------------------------------------------------- 9 but it's tiny: 8% invested + fees eat half
def pacman(ctx, x, y, r, t, col):
    m = 0.15 + 0.6 * abs(math.sin(t * 10))
    ctx.new_path(); ctx.move_to(x, y); ctx.arc(x, y, r, math.pi + m / 2, math.pi - m / 2 + 2 * math.pi); ctx.close_path()
    ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(6); ctx.stroke()
    ctx.new_path(); ctx.arc(x - r * 0.1, y - r * 0.5, r * 0.13, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()


def s_tiny(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x3A), (0x04, 0x06, 0x14))
    stars(ctx, t, 36, 0, 1200, 3)
    skyline(ctx, 1300, t, 5, (0x0E, 0x14, 0x2A))
    stamp_box(ctx, ["BUT IT'S TINY."], W / 2, 385, T["tiny"] - 0.05, t, C["red"], 640, 84, 0.04)
    # 20-year barcode of days in the market
    bx, by, bw, bh = 110, 565, 860, 90
    card(ctx, bx - 20, by - 60, bw + 40, bh + 90, (0x0C, 0x10, 0x1C), 0.95, 14, border=C["grey"])
    text(ctx, "20 YEARS · DAYS IN THE MARKET", bx, by - 18, 26, C["white"], 0.9, MONO, True, "left")
    rect(ctx, bx, by, bw, bh, (0x2A, 0x30, 0x38))
    lit = prog(t, T["invested"] - 0.1, 0.9)
    if lit > 0:
        upto = int(N * lit)
        ctx.set_source_rgba(*rgba(GRNC))
        for i in range(0, upto):
            if INM[i]:
                ctx.rectangle(bx + i / N * bw, by, max(1.2, bw / N), bh)
        ctx.fill()
    if t >= T["eight2"] - 0.05:
        p = back(prog(t, T["eight2"] - 0.05, 0.35))
        ctx.save(); ctx.translate(W / 2, 765); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        flip_counter(ctx, -230, -70, 460, 140, "INVESTED", f"{TIM:.0f}%", GRNC, 1, 70)
        ctx.restore()
    # profit bar eaten by fees
    if t >= T["fees1"] - 0.3:
        a = ease(prog(t, T["fees1"] - 0.3, 0.3))
        card(ctx, 90, 860, 900, 200, C["dark"], a, 16)
        text(ctx, "ITS PROFIT", 120, 905, 30, GOLD, a, MONO, True, "left")
        x0, x1 = 120, 960
        eat = FEE_EAT * ease_io(prog(t, T["eat"], T["half"] + 0.3 - T["eat"]))
        xe = x1 - (x1 - x0) * eat
        card(ctx, x0, 935, xe - x0, 85, GOLD, a, 10, shadow=False, border=C["ink"])
        for j in range(int((xe - x0) // 50)):
            rect(ctx, x0 + 20 + j * 50, 950, 4, 55, C["ink"], 0.25 * a)
        pacman(ctx, xe + 20, 978, 60, t, C["red"])
        text(ctx, "FEES", xe + 20, 1085, 30, C["red"], a, HEAD, True, "center", outline=5, ocol=C["ink"])
        tag(ctx, 300, 1135, "FEES EAT HALF", C["red"], back(prog(t, T["half"] - 0.05, 0.3)), 40, -0.04, C["white"])
    bunting(ctx, "THE PROBLEM", t, s0, [C["blue"], C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if e != "talk" else e)


# ---------------------------------------------------------------- 10 final score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 430, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 480, 900, 230, "HOLDER · JUST HELD", money(BH_V), C["green"], T["rev1"], t)
    redacted_counter(ctx, 90, 760, 900, 230, "PANIC BUYER · 3 RED DAYS", money(S_V), C["red"], T["rev2"], t)
    if t >= T["rev1"]:
        stamp_box(ctx, ["WINNER"], 885, 530, T["rev1"] + 0.25, t, C["green"], 210, 42, 0.1)
    sticker(ctx, t, T["rev2"] + 0.5, T["Barely"] - 0.1, "right")
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev1"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 11 double the fees
def hbar(ctx, y, lab, v, g, col, vmax):
    card(ctx, 90, y, 900, 150, C["dark"], 1, 16)
    text(ctx, lab, 120, y + 46, 30, col, 1, MONO, True, "left")
    w_ = (840 * v / vmax) * g
    if w_ > 2:
        card(ctx, 120, y + 70, w_, 52, col, 1, 10, shadow=False)
    if g > 0.3:
        text(ctx, money(v), 960, y + 46, 38, C["white"], 1, MONO, True, "right")


def s_double(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x22, 0x0E), (0x10, 0x08, 0x04))
    god_rays(ctx, W / 2, 700, t, 0.06, C["orange"], 14, 1400)
    text(ctx, "DOUBLE THE FEES?", W / 2, 420, 92, C["white"], back(prog(t, s0 + 0.05, 0.3)), HEAD, True, "center", outline=14, ocol=C["ink"])
    vmax = F05 * 1.08
    hbar(ctx, 480, "0.05% FEES (TESTED)", F05, 1.0, PCOL, vmax)
    hbar(ctx, 650, "0.10% FEES", F10, ease_io(prog(t, T["fees2"] - 0.1, 0.8)), C["red"], vmax)
    hbar(ctx, 820, "0.20% FEES", F20, ease_io(prog(t, T["fees2"] + 0.3, 0.8)), (0xB0, 0x30, 0x40), vmax)
    xs = 120 + 840 * 10000 / vmax
    for k in range(13):
        rect(ctx, xs - 3, 470 + k * 40, 6, 22, C["white"], 0.85)
    text(ctx, "START $10,000", xs, 1010, 26, C["white"], 1, MONO, True, "center", outline=5, ocol=C["ink"])
    tag(ctx, 540, 1110, "BARELY ABOVE $10,000", GOLD, back(prog(t, T["Barely"] - 0.05, 0.3)), 40, -0.03)
    sticker(ctx, t, T["rev2"] + 0.5, T["Barely"] - 0.1, "right")
    bunting(ctx, "STRESS TEST", t, s0, [C["orange"], C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "shock" if (e != "talk" and t > T["fees2"]) else e)


# ---------------------------------------------------------------- 12 verdict + FOLLOW (no spoken outro)
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3)
    rect(ctx, 0, 0, W, H, (0x08, 0x02, 0x04), 0.62)
    stamp_box(ctx, ["THE BOUNCE IS REAL."], W / 2, 540, T["bounce2"] - 0.05, t, GOLD, 860, 88, -0.05)
    stamp_box(ctx, ["THE MONEY ISN'T."], W / 2 + 10, 860, T["money"] - 0.05, t, C["red"], 800, 104, 0.04)
    fb = back(prog(t, T["real2"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2 + 160, 1100); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #11", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "rules": s_rules, "start": s_start, "crash08": s_crash08, "lead": s_lead,
            "covid": s_covid, "catch": s_catch, "tiny": s_tiny, "score": s_score, "double": s_double, "verdict": s_verdict,
            "loop": s_loop}
