# ================================================================ Autopsy #11 scenes (the Nasdaq just crashed - what next?)
HCOL = (0x4F, 0xC3, 0xF7)    # HOLDER (buy & hold)
PCOL = (0xFF, 0x9F, 0x1C)    # PANIC SELLER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x2E, 0x06, 0x10), (0x07, 0x02, 0x04)


def candle(ctx, x, y, w, h, col, a=1.0, wick=40):
    rect(ctx, x + w / 2 - 4, y - wick, 8, h + 2 * wick, C["ink"], a)
    card(ctx, x, y, w, h, col, a, 8, shadow=False, border=C["ink"])


def arrow_up(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.new_path()
    ctx.move_to(0, -90); ctx.line_to(70, -10); ctx.line_to(28, -10); ctx.line_to(28, 80); ctx.line_to(-28, 80); ctx.line_to(-28, -10)
    ctx.line_to(-70, -10); ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke(); ctx.restore()


def arrow_down(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.pi); arrow_up(ctx, 0, 0, s, col, a); ctx.restore()


def sticker(ctx, t, t0, t1, kind, y=1085):
    """comment prompt sticker (visual only). kind: 'guess' or 'right'. Captions sit at ~1240."""
    if not (t0 - 0.01 <= t <= t1):
        return
    p = back(prog(t, t0, 0.35)) * (1 - ease(prog(t, t1 - 0.25, 0.25)))
    if p <= 0:
        return
    wob = 1 + 0.03 * math.sin(t * 9)
    ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.035); ctx.scale(max(p * wob, 1e-3), max(p * wob, 1e-3))
    if kind == "guess":
        card(ctx, -440, -62, 880, 124, GOLD, 1, 26, border=C["ink"])
        text(ctx, "COMMENT YOUR GUESS", -395, 22, 58, C["ink"], 1, HEAD, True, "left")
        bob = math.sin(t * 10) * 8
        ctx.save(); ctx.translate(205, bob); arrow_down(ctx, 0, 0, 0.36, C["red"]); ctx.restore()
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
    a = ease(prog(t, SC["count"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #11", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, PCOL, a, 8, shadow=False)
        text(ctx, money(P1M), 805, 78, fit(ctx, money(P1M), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["count"]) / (T["mostly"] - SC["count"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: NASDAQ -5.5% / WHAT NEXT?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 620, t, 0.07, C["red"], 14, 1400)
    for k in range(8):                      # falling red candles in the background
        u = (t * 0.28 + k / 8) % 1
        candle(ctx, (k * 139 + 50) % (W - 60), -220 + u * 1700, 46, 120, REDC, 0.2, 26)
    # big crash arrow behind the number
    ctx.save(); ctx.translate(880, 900 + math.sin(t * 5) * 14); ctx.rotate(0.35)
    arrow_down(ctx, 0, 0, 1.6, REDC, 0.55); ctx.restore()
    rect(ctx, 0, 0, W, H, BG1, 0.2)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    hl = 1 + 0.1 * math.sin(math.pi * prog(tl, T["five"] - 0.1, 0.5))
    s_ = max(p * sc * wob * hl, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 640); ctx.rotate(-0.04); ctx.scale(s_, s_)
    sz = fit(ctx, "-5.5%", 330, 960)
    text(ctx, "-5.5%", 0, 0, sz, REDC, 1, HEAD, True, "center", outline=26, ocol=C["ink"])
    ctx.restore()
    hb = 1 + 0.12 * math.sin(math.pi * prog(tl, T["run"] - 0.1, 0.5))
    s2 = max(p * sc * wob * hb, 1e-3)
    ctx.save(); ctx.translate(540, 930); ctx.rotate(0.035); ctx.scale(s2, s2)
    sz2 = fit(ctx, "WHAT NEXT?", 190, 980)
    text(ctx, "WHAT NEXT?", 0, 0, sz2, GOLD, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    if show_tag:
        tag(ctx, 540, 225, "NASDAQ", C["white"], p, 64, -0.04)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 count: S&P -4.4%, 39 crash days in 20 years
def s_count(ctx, t, s0, s1):
    rain_bg(ctx, t)
    p = back(prog(t, T["SP"] - 0.1, 0.3))
    if t < T["In"] - 0.1:
        ctx.save(); ctx.translate(W / 2, 520); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        text(ctx, "S&P 500", 0, -60, 120, C["white"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        q = back(prog(t, T["four"] - 0.1, 0.3))
        if q > 0:
            ctx.save(); ctx.scale(max(q, 1e-3), max(q, 1e-3))
            text(ctx, "-4.4%", 0, 170, 210, REDC, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
            ctx.restore()
        ctx.restore()
        tag(ctx, 540, 920, "THURSDAY, NOV 5", C["cream"], back(prog(t, T["too"] - 0.2, 0.3)), 40, 0.03)
    else:
        # 20 columns of red candles: one per crash day (2005-2024), no axis
        g = prog(t, T["In"], T["t39"] - T["In"])
        text(ctx, "SPY · 2005-2024 · DAYS DOWN 4%+", W / 2, 400, 34, C["white"], ease(prog(t, T["In"] - 0.1, 0.3)), MONO, True, "center", outline=6, ocol=C["ink"])
        x0, cw, base = 70, 47, 1060
        shown = 0
        for j, yr in enumerate(range(2005, 2025)):
            cx = x0 + j * cw
            rect(ctx, cx + 4, base + 6, cw - 8, 4, C["white"], 0.5)
            if yr % 5 == 0 or yr in (2008, 2020):
                text(ctx, f"'{yr % 100:02d}", cx + cw / 2, base + 46, 24, GOLD if yr in (2008, 2020) else C["white"], 0.85, MONO, True, "center")
            n = BYYEAR.get(yr, 0)
            for k in range(n):
                idx = shown + k
                if g * NCR < idx + 1:
                    break
                pk = back(clamp((g * NCR - idx) / 1.5))
                yy = base - 18 - k * 34
                ctx.save(); ctx.translate(cx + cw / 2, yy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
                card(ctx, -15, -14, 30, 28, REDC, 1, 5, shadow=False, border=C["ink"])
                ctx.restore()
            shown += n
        c = back(prog(t, T["t39"] - 0.08, 0.35))
        if c > 0:
            ctx.save(); ctx.translate(800, 620); ctx.rotate(0.05); ctx.scale(max(c, 1e-3), max(c, 1e-3))
            card(ctx, -190, -120, 380, 240, C["dark"], 1, 22, border=REDC)
            text(ctx, str(NCR), 0, 50, 170, REDC, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            text(ctx, "TIMES", 0, 100, 34, C["white"], 1, MONO, True, "center")
            ctx.restore()
    bunting(ctx, "THE CRASH", t, s0, [C["red"], C["ink"], C["red"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["t39"]) else e)


# ---------------------------------------------------------------- 3 guess: a year later, how many were higher?
def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(20):
        u = ((t - s0) * 0.45 + k / 20) % 1
        candle(ctx, (k * 211) % W, 1300 - u * 1150, 30, 70, REDC if k % 3 else GRNC, 0.25 * (1 - u), 16)
    hp = back(prog(t, s0 + 0.05, 0.3))
    ctx.save(); ctx.translate(W / 2, 420); ctx.scale(max(hp, 1e-3), max(hp, 1e-3))
    text(ctx, "1 YEAR LATER...", 0, -40, 70, C["white"], 1, HEAD, True, "center", outline=10, ocol=C["ink"])
    q = back(prog(t, T["how"] - 0.1, 0.3))
    if q > 0:
        text(ctx, "HOW MANY WERE HIGHER?", 0, 50, fit(ctx, "HOW MANY WERE HIGHER?", 76, 960) * q, GOLD, 1, HEAD, True, "center", outline=10, ocol=C["ink"])
    ctx.restore()
    g = back(prog(t, T["A2"] - 0.15, 0.35))
    if g > 0:
        blink = int(t * 4) % 2
        for k, (lab, sub, col, x, tt) in enumerate((("A", "UNDER HALF", PCOL, -225, T["A2"]), ("B", "ALMOST ALL", HCOL, 225, T["B"]))):
            if t < tt - 0.15:
                continue
            pk = back(prog(t, tt - 0.15, 0.35))
            on = (blink == k) and t > T["Guess"]
            hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
            ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
            card(ctx, -205, -190, 410, 330, col, 1, 22, border=C["white"] if on else C["ink"])
            text(ctx, lab, 0, -10, 200, C["ink"], 1, HEAD, True, "center")
            for j in range(10):          # 10 mini dots: neutral (no hint)
                rect(ctx, -170 + j * 34, 40, 22, 22, C["ink"], 0.35)
            text(ctx, sub, 0, 120, fit(ctx, sub, 54, 380), C["ink"], 1, HEAD, True, "center")
            ctx.restore()
    sticker(ctx, t, T["Guess"] - 0.15, T["Guess"] + 2.3, "guess")
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 rules: sell next open, wait a month, buy back
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    if t < T["Rule"] - 0.1:
        p = back(prog(t, T["trader"] - 0.1, 0.3))
        ctx.save(); ctx.translate(W / 2, 470); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        text(ctx, "THE PANIC SELLER", 0, 0, 104, PCOL, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
        # mini rocco running in panic across the screen with crash candles
        run = prog(t, s0, T["Rule"] - s0)
        for k in range(4):
            candle(ctx, 150 + k * 230, 700 + 30 * math.sin(t * 4 + k), 60, 140, REDC, 0.9, 30)
        mini_rocco(ctx, 140 + run * 800, 990, 9, "race", t, "shock", False, True)
        tag(ctx, 540, 580, "SELLS AT EVERY CRASH DAY", C["red"], back(prog(t, T["every"] - 0.1, 0.3)), 38, 0.03, C["white"])
    else:
        for k, (title, l1, col, fg, y, tt, t2) in enumerate((("SELL", "AFTER A CRASH DAY", REDC, C["white"], 520, T["crash1"], T["sell"]),
                                                             ("WAIT", "WAIT 1 MONTH", GRNC, C["ink"], 880, T["wait1"], T["buy"]))):
            p = back(prog(t, tt - 0.12, 0.4))
            if p <= 0:
                continue
            ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.025 if k == 0 else 0.025); ctx.scale(max(p, 1e-3), max(p, 1e-3))
            card(ctx, -460, -150, 920, 300, col, 1, 22, border=C["ink"])
            card(ctx, -430, -120, 240, 240, C["dark"], 1, 16, shadow=False)
            if k == 0:
                candle(ctx, -345, -70, 70, 150, REDC, 1, 30)
                arrow_down(ctx, -250, -20, 0.4, C["red"])
            else:
                clock(ctx, -310, 0, 90, t, 2.0)
            q = back(prog(t, t2 - 0.08, 0.3))
            big = 1 + 0.1 * math.sin(math.pi * prog(t, t2 - 0.05, 0.4))
            ctx.save(); ctx.translate(130, -30); ctx.scale(big, big)
            text(ctx, l1, 0, 0, fit(ctx, l1, 66, 560), fg, 1, HEAD, True, "center", outline=6 if k == 0 else 0, ocol=C["ink"])
            ctx.restore()
            if q > 0:
                ctx.save(); ctx.translate(130, 75); ctx.scale(max(q, 1e-3), max(q, 1e-3))
                card(ctx, -280, -48, 560, 96, C["dark"], 1, 14, shadow=False)
                lab = "SELL NEXT OPEN" if k == 0 else "BUY BACK AT OPEN"
                text(ctx, lab, 0, 18, fit(ctx, lab, 52, 520), C["red"] if k == 0 else GRNC, 1, HEAD, True, "center")
                ctx.restore()
            ctx.restore()
        tag(ctx, 540, 1110, "VS HOLDER · $10,000 EACH", GOLD, back(prog(t, T["back"] - 0.05, 0.3)), 36, 0.03)
    sticker(ctx, t, T["Guess"] - 0.15, T["Guess"] + 2.3, "guess")
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "shock" if (e != "talk" and t < T["Rule"]) else e)


# ---------------------------------------------------------------- 5 race chart 2005 -> 2011 (crash ticks)
RBOX = (110, 620, 860, 420)


def race_idx(t, pts):
    if t <= pts[0][0]:
        return max(1, pts[0][1])
    for (a, ia), (b, ib) in zip(pts, pts[1:]):
        if t <= b:
            return int(ia + (ib - ia) * ease_io((t - a) / max(1e-3, b - a)))
    return pts[-1][1]


def curtain_box(ctx, t, xc, top, right, hh, label="CLASSIFIED"):
    ctx.save(); ctx.rectangle(xc, top, right - xc, hh); ctx.clip()
    rect(ctx, xc, top, right - xc, RBOX[3] + 60, (0x05, 0x05, 0x05))
    for j in range(16):
        ctx.save(); ctx.translate(xc + j * 60 - 40, top); ctx.rotate(0.6)
        rect(ctx, 0, 0, 22, 70, GOLD, 0.9); ctx.restore()
    cx = (xc + right) / 2
    text(ctx, label, cx, top + 200, fit(ctx, label, 60, right - xc - 20), C["red"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])
    qs = 1 + 0.1 * math.sin(t * 7)
    ctx.save(); ctx.translate(cx, top + 360); ctx.scale(qs, qs)
    text(ctx, "?", 0, 0, 160, GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"]); ctx.restore()
    ctx.restore()


def race_chart(ctx, t, up, zones=(), curtain=None, cut="2021-01-01"):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), 0, N - 1, RBOX); x1 = sx_of(di(d1), 0, N - 1, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    # crash-day ticks along the bottom (red down triangles), revealed as the race passes them
    for ci in CRASH_I:
        if ci > up:
            break
        xx = sx_of(ci, 0, N - 1, RBOX)
        ctx.new_path(); ctx.move_to(xx - 7, RBOX[1] + RBOX[3] - 18); ctx.line_to(xx + 7, RBOX[1] + RBOX[3] - 18); ctx.line_to(xx, RBOX[1] + RBOX[3] - 4)
        ctx.close_path(); ctx.set_source_rgba(*rgba(REDC, 0.9)); ctx.fill()
    vmax = max(15000.0, 1.25 * float(max(np.nanmax(SV[:up + 1]), np.nanmax(JV[:up + 1]))))
    vmin = 6000.0
    tips = []
    for arr, col in ((SV, HCOL), (JV, PCOL)):
        xs, ys = series_xy(arr, 0, N - 1, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (px_, py_) = tips
    lead_p = JV[up] > SV[up]
    off = 0 if abs(hy - py_) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_p else 0), 4, "tophat", t, "sad" if lead_p else "smug", False, True)
    mini_rocco(ctx, px_, py_ - 4 - (0 if lead_p else off), 4, "race", t, "smug" if lead_p else "sad", False, True)
    if curtain is not None and curtain > 0:
        xc = sx_of(di(cut), 0, N - 1, RBOX)
        curtain_box(ctx, t, xc, RBOX[1] - 30, RBOX[0] + RBOX[2] + 30, (RBOX[3] + 60) * ease(curtain))
    for k, (lab, col) in enumerate((("PANIC SELLER", PCOL), ("HOLDER", HCOL))):
        rect(ctx, RBOX[0] + 150 + k * 330, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 196 + k * 330, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")


def s_crash08(ctx, t, s0, s1):
    late = t >= T["Tw11"] - 0.1
    if late:
        stadium(ctx, t)
    else:
        rain_bg(ctx, t)
    pts = [(s0 + 0.15, 1), (T["Crash"], di("2008-09-12")), (T["lead1"] + 0.3, di("2008-12-31")),
           (T["Tw11"], di("2008-12-31")), (T["ahead"] + 0.2, di("2011-12-30"))]
    race_chart(ctx, t, race_idx(t, pts), [("2007-10-10", "2009-03-09", C["red"], 0.22 if not late else 0.1)])
    if not late:
        tag(ctx, 540, 440, "2008: CRASH AFTER CRASH", C["red"], back(prog(t, T["Two"], 0.3)), 38, -0.03, C["white"])
        tag(ctx, 540, 524, "PANIC SELLER TAKES THE LEAD", PCOL, back(prog(t, T["takes"] - 0.15, 0.3)), 34, 0.02)
    else:
        tag(ctx, 540, 440, "2011", C["cream"], back(prog(t, T["Tw11"] - 0.05, 0.3)), 38, -0.03)
        tag(ctx, 540, 524, "STILL AHEAD", PCOL, back(prog(t, T["still"] - 0.05, 0.3)), 38, 0.02)
    bunting(ctx, "THE RACE" if late else "2008", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("shock" if t < T["takes"] else "smug") if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 6 covid 2020 (zoomed, normalised to the 2019 close)
CBOX = (110, 620, 860, 420)
_c20 = slice(di("2019-12-31"), di("2020-12-31") + 1)
C_H = SV[_c20] / SV[_c20][0]; C_P = JV[_c20] / JV[_c20][0]; C_N = len(C_H)
C_MIN = float(min(C_H.min(), C_P.min())) - 0.04; C_MAX = float(max(C_H.max(), C_P.max())) + 0.06
_i0 = di("2019-12-31")


def s_covid(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x3A), (0x0A, 0x04, 0x12))
    stars(ctx, t, 40, 0, 1300, 7)
    card(ctx, CBOX[0] - 30, CBOX[1] - 30, CBOX[2] + 60, CBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    x0 = sx_of(di("2020-02-19") - _i0, 0, C_N - 1, CBOX); x1 = sx_of(di("2020-03-23") - _i0, 0, C_N - 1, CBOX)
    rect(ctx, x0, CBOX[1], x1 - x0, CBOX[3], C["purple"], 0.45)
    yb = sy_of(1.0, C_MIN, C_MAX, CBOX)
    for k in range(18):
        rect(ctx, CBOX[0] + k * 48, yb, 28, 3, C["white"], 0.5)
    text(ctx, "START OF 2020", CBOX[0] + 10, yb + 34, 22, C["white"], 0.7, MONO, True, "left")
    for m, lab in ((1, "JAN"), (3, "MAR"), (6, "JUN"), (9, "SEP"), (12, "DEC")):
        text(ctx, lab, sx_of(di(f"2020-{m:02d}-01") - _i0, 0, C_N - 1, CBOX), CBOX[1] + CBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    pts = [(s0 + 0.2, 1), (T["crash3"] + 0.2, di("2020-03-27") - _i0), (T["bottom"] + 0.3, di("2020-04-30") - _i0),
           (T["vanishes"] + 0.4, C_N - 1)]
    up = max(1, race_idx(t, pts))
    tips = []
    for arr, col in ((C_H, HCOL), (C_P, PCOL)):
        xs, ys = series_xy(arr, 0, C_N - 1, up, CBOX, C_MIN, C_MAX, 1)
        poly(ctx, xs, ys, col, 8, 1, glow=True); tips.append((xs[-1], ys[-1]))
    # the second panic sale (Apr 2, 2020) near the bottom
    isell = di("2020-04-02") - _i0
    if up >= isell:
        xs_ = sx_of(isell, 0, C_N - 1, CBOX); ys_ = sy_of(C_P[isell], C_MIN, C_MAX, CBOX)
        pp = back(prog(t, T["panics"] - 0.1, 0.3))
        ctx.save(); ctx.translate(xs_, ys_ - 60); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        arrow_down(ctx, 0, 0, 0.32, C["red"]); ctx.restore()
        text(ctx, "SOLD AGAIN", xs_ + 30, ys_ - 100, 26, C["red"], pp, MONO, True, "left", outline=5, ocol=C["ink"])
    lead = C_P[up] * JV[_i0] > C_H[up] * SV[_i0]
    mini_rocco(ctx, tips[0][0], tips[0][1] - 4, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, tips[1][0], tips[1][1] - 4 - (50 if abs(tips[0][1] - tips[1][1]) < 50 else 0), 4, "race", t,
               "smug" if lead else "sad", False, True)
    for k, (lab, col) in enumerate((("PANIC SELLER", PCOL), ("HOLDER", HCOL))):
        rect(ctx, CBOX[0] + 150 + k * 330, CBOX[1] + CBOX[3] + 87, 36, 10, col)
        text(ctx, lab, CBOX[0] + 196 + k * 330, CBOX[1] + CBOX[3] + 101, 26, col, 1, MONO, True, "left")
    tag(ctx, 540, 440, "2020: COVID", C["purple"], back(prog(t, T["Covid"] - 0.05, 0.3)), 38, -0.03, C["white"])
    if t < T["panics"] - 0.05:
        tag(ctx, 540, 524, "DODGES THE CRASH", PCOL, back(prog(t, T["dodges2"] - 0.05, 0.3)), 36, 0.02)
    elif t < T["lead2"] - 0.05:
        tag(ctx, 540, 524, "...PANICS NEAR THE BOTTOM", C["red"], back(prog(t, T["panics"] - 0.05, 0.3)), 36, 0.02, C["white"])
    else:
        tag(ctx, 540, 524, "THE LEAD VANISHES", HCOL, back(prog(t, T["lead2"] - 0.05, 0.3)), 38, 0.02)
    bunting(ctx, "2020", t, s0, [C["purple"], C["ink"], C["purple"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: ("sad" if t > T["vanishes"] else "neutral") if e != "talk" else e)


# ---------------------------------------------------------------- 7 2022 decides it (race to 2020, curtain over 2021+)
def s_decide(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x0E, 0x2A), (0x0A, 0x02, 0x08))
    god_rays(ctx, W / 2, 470, t, 0.08, GOLD, 14, 1400)
    race_chart(ctx, t, di("2020-12-31"), [("2007-10-10", "2009-03-09", C["red"], 0.10), ("2020-02-19", "2020-03-23", C["purple"], 0.25)],
               curtain=prog(t, s0 + 0.05, 0.45))
    p = back(prog(t, T["Tw22"] - 0.05, 0.3))
    hl = 1 + 0.08 * math.sin(math.pi * prog(t, T["decides"] - 0.05, 0.45))
    ctx.save(); ctx.translate(W / 2, 470); ctx.rotate(-0.03); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
    text(ctx, "2022 DECIDES IT", 0, 0, 110, GOLD, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    bunting(ctx, "2022", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 8 the twist: change the wait, the winner changes
def hourglass(ctx, cx, cy, s, t):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.sin(t * 1.5) * 0.15)
    ctx.scale(s, s)
    rect(ctx, -90, -150, 180, 20, (0x8B, 0x5A, 0x2B)); rect(ctx, -90, 130, 180, 20, (0x8B, 0x5A, 0x2B))
    for sgn in (-1, 1):
        ctx.new_path(); ctx.move_to(-70, sgn * 130); ctx.line_to(70, sgn * 130); ctx.line_to(8, 0); ctx.line_to(-8, 0); ctx.close_path()
        ctx.set_source_rgba(0.85, 0.95, 1, 0.35); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(6); ctx.stroke()
    f = (t * 0.35) % 1
    ctx.new_path(); ctx.move_to(-70 * (1 - f), -130 * (1 - f)); ctx.line_to(70 * (1 - f), -130 * (1 - f)); ctx.line_to(6, -6); ctx.line_to(-6, -6); ctx.close_path()
    ctx.set_source_rgba(*rgba(GOLD)); ctx.fill()
    hh = 130 * f
    ctx.new_path(); ctx.move_to(-70 * f - 10, 130); ctx.line_to(70 * f + 10, 130); ctx.line_to(0, 130 - hh); ctx.close_path(); ctx.fill()
    rect(ctx, -3, -6, 6, 136, GOLD)
    ctx.restore()


def s_twist(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x05, 0x08), (0x02, 0x01, 0x02))
    for i in range(0, W, 80):
        rect(ctx, (i + t * 60) % (W + 80) - 80, 0, 2, H, C["red"], 0.10)
    p = back(prog(t, T["Heres"] - 0.15, 0.3))
    ctx.save(); ctx.translate(W / 2, 450); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    text(ctx, "HERE'S THE TWIST", 0, 0, 104, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    hourglass(ctx, W / 2, 830, 1.2 * back(prog(t, T["Change"] - 0.1, 0.4)) + 1e-3, t)
    tag(ctx, 540, 590, "CHANGE THE WAIT", GOLD, back(prog(t, T["wait2"] - 0.1, 0.3)), 40, -0.05)
    tag(ctx, 540, 1080, "...AND THE WINNER CHANGES", C["white"], back(prog(t, T["winner"] - 0.1, 0.3)), 40, 0.04)
    bunting(ctx, "THE TWIST", t, s0, [C["red"], C["ink"], C["red"], GOLD])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if (e != "talk" and t > T["twist"]) else e)


# ---------------------------------------------------------------- 9 the waits: 1 week / 3 months / 6 months (all redacted)
def s_waits(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x3A), (0x04, 0x06, 0x14))
    stars(ctx, t, 36, 0, 1200, 3)
    skyline(ctx, 1300, t, 5, (0x0E, 0x14, 0x2A))
    text(ctx, "SAME PANIC. DIFFERENT WAIT.", W / 2, 420, 66, C["white"], back(prog(t, s0 + 0.05, 0.3)), HEAD, True, "center", outline=10, ocol=C["ink"])
    for k, (lab, tt) in enumerate((("1 WEEK", T["week"]), ("3 MONTHS", T["Three"]), ("6 MONTHS", T["Six"]))):
        p = back(prog(t, tt - 0.15, 0.35))
        if p <= 0:
            continue
        y = 500 + k * 165
        ctx.save(); ctx.translate(W / 2, y); ctx.rotate(0.02 * (1 if k % 2 else -1)); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -440, 0, 880, 140, C["dark"], 1, 18, border=PCOL)
        clock(ctx, -360, 70, 46, t, 1.5 + k)
        text(ctx, lab, -290, 92, 64, PCOL, 1, HEAD, True, "left")
        rect(ctx, 80, 30, 330, 80, (0x05, 0x05, 0x05))
        text(ctx, "$??,???", 245, 88, 50, (0x60, 0x66, 0x6B), 1, MONO, True, "center")
        ctx.restore()
    stamp_box(ctx, ["DIFFERENT ENDINGS."], W / 2, 1100, T["Different"] - 0.05, t, C["red"], 760, 80, -0.04)
    bunting(ctx, "THE WAIT", t, s0, [C["blue"], C["ink"], PCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if (e != "talk" and t < T["Different"]) else ("shock" if e != "talk" else e))


# ---------------------------------------------------------------- 10 final score (3 redacted counters)
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 420, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 200, "HOLDER · JUST HELD", money(BH_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 670, 900, 200, "PANIC SELLER · 1-MONTH WAIT", money(P1M), PCOL, T["rev2"], t)
    redacted_counter(ctx, 90, 890, 900, 200, "PANIC SELLER · 3-MONTH WAIT", money(P3M), C["red"], T["rev3"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, C["green"], 210, 42, 0.1)
    if t >= T["rev3"] + 0.4:
        a = ease(prog(t, T["rev3"] + 0.4, 0.3))
        card(ctx, 90, 1110, 900, 64, (0x05, 0x05, 0x05), 0.85 * a, 12, shadow=False)
        s_ = f"1 WEEK: {money(P1W)}  ·  6 MONTHS: {money(P6M)}"
        text(ctx, s_, W / 2, 1153, fit(ctx, s_, 30, 860, MONO), C["white"], a, MONO, True, "center")
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 11 the answer: 36 of 39 higher a year later
def s_answer(ctx, t, s0, s1):
    bg_fill(ctx, (0x0C, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    god_rays(ctx, W / 2, 620, t, 0.07, GRNC, 14, 1400)
    if t < T["t36"] - 0.1:
        text(ctx, "YOUR GUESS?", W / 2, 640, 150, GOLD, back(prog(t, s0 + 0.05, 0.3)), HEAD, True, "center", outline=16, ocol=C["ink"])
    else:
        p = back(prog(t, T["t36"] - 0.1, 0.35))
        ctx.save(); ctx.translate(W / 2, 470); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        text(ctx, f"{Y1UP} OF {Y1N}", 0, 40, 170, GRNC, 1, HEAD, True, "center", outline=16, ocol=C["ink"])
        ctx.restore()
        tag(ctx, 540, 560, "HIGHER 1 YEAR LATER", C["white"], back(prog(t, T["higher2"] - 0.1, 0.3)), 38, -0.02)
        # 39 dots: green = higher a year later, red = lower (all Sept 2008)
        g = prog(t, T["t36"], 0.9)
        for k, ci in enumerate(CRASH_I):
            if k >= g * len(CRASH_I):
                break
            r_, c_ = divmod(k, 13)
            down = str(DATES[ci].date()) in Y1DOWN
            card(ctx, 135 + c_ * 64, 640 + r_ * 64, 48, 48, REDC if down else GRNC, 1, 10, shadow=False, border=C["ink"])
        if t > T["higher2"]:
            text(ctx, "RED = SEPT 2008", 135, 880, 26, REDC, ease(prog(t, T["higher2"], 0.3)), MONO, True, "left", outline=5, ocol=C["ink"])
        stamp_box(ctx, ["B: ALMOST ALL"], 760, 930, T["higher2"], t, C["green"], 480, 64, -0.06)
    sticker(ctx, t, T["t36"] + 0.4, T["Verdict"] + 1.4, "right")
    bunting(ctx, "THE ANSWER", t, s0, [C["green"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if (e != "talk" and t > T["t36"]) else e)


# ---------------------------------------------------------------- 12 verdict + FOLLOW (no spoken outro)
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x08, 0x02, 0x04), 0.8)
    stamp_box(ctx, ["PANIC ONLY PAID", "WITH LUCKY TIMING."], W / 2, 520, T["panic4"] - 0.05, t, (0xD0, 0x50, 0x00), 860, 80, -0.05)
    stamp_box(ctx, ["THE CRASH WAS", "MOSTLY NOISE."], W / 2 + 10, 860, T["crash4"] - 0.05, t, (0x0B, 0x8A, 0x4C), 780, 84, 0.04)
    sticker(ctx, t, T["t36"] + 0.4, T["Verdict"] + 1.4, "right")
    fb = back(prog(t, T["mostly"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2 + 160, 1110); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #12", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "count": s_count, "guess": s_guess, "rules": s_rules, "crash08": s_crash08, "covid": s_covid,
            "decide": s_decide, "twist": s_twist, "waits": s_waits, "score": s_score, "answer": s_answer, "verdict": s_verdict,
            "loop": s_loop}
