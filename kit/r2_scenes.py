# ================================================================ Autopsy #4 scenes (2-day RSI)
def tiles(ctx, x0, y0, n_shown, cols=10, size=62, gap=8, t=0.0):
    for k in range(min(n_shown, len(WINS))):
        r, c = divmod(k, cols)
        p = back(clamp((n_shown - k) / 3))
        col = C["green"] if WINS[k] else C["red"]
        cx, cy = x0 + c * (size + gap) + size / 2, y0 + r * (size + gap) + size / 2
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        rect(ctx, -size / 2, -size / 2, size, size, col)
        if WINS[k]:
            check(ctx, -size * 0.25, 2, size * 0.5, C["ink"], 1, 5)
        else:
            ctx.new_path(); ctx.move_to(-12, -12); ctx.line_to(12, 12); ctx.move_to(12, -12); ctx.line_to(-12, 12)
            ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
        ctx.restore()


def s_hook(ctx, t, s0, s1):
    rain_bg(ctx, t, 15)
    k = ease_io(prog(t, 0.0, T["four"] + 0.3))
    n = int(150 * k)
    wr = 100 * sum(WINS[:n]) / max(1, n)
    flip_counter(ctx, 60, 380, 960, 190, "WIN RATE", f"{wr:.0f}%" if n else "—", C["green"], 1, 120)
    tiles(ctx, 120, 620, n, 15, 48, 8, t)
    p = back(prog(t, T["still"], 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 1020); ctx.rotate(-0.05); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -440, -110, 880, 220, (0x14, 0x18, 0x1C), 1, 18, border=C["red"])
        text(ctx, "$10,000", -220, 30, 84, C["cream"], 1, MONO, True, "center")
        text(ctx, "→", 0, 26, 70, C["cream"], 1, INTER, True, "center")
        v = 10000 + 6525 * ease_io(prog(t, T["sixteen"], 0.8))
        text(ctx, money(v), 230, 30, 84, C["red"], 1, MONO, True, "center")
        ctx.restore()
    tag(ctx, W / 2 + 250, 880, "20 YEARS", C["yellow"], back(prog(t, T["half"], 0.35)), 36, 0.05)
    bunting(ctx, "73% WINNERS?", t, -0.45, [C["green"], C["red"], C["yellow"], C["blue"]])
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["sixteen"]) else e)


def s_title(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x5E, 0x5E), (0x0C, 0x2A, 0x2C))
    for i in range(0, W, 120):
        rect(ctx, i, 0, 3, H, C["white"], 0.06)
    for j in range(0, H, 120):
        rect(ctx, 0, j, W, 3, C["white"], 0.06)
    god_rays(ctx, W / 2, 330, t * 0.4, 0.07, C["white"], 12, 900)
    ctx.new_path(); ctx.save(); ctx.translate(W / 2, 360); ctx.scale(1, 0.45); ctx.arc(0, 0, 210, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*rgba((0xD8, 0xE4, 0xE6))); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(6); ctx.stroke()
    card(ctx, 110, 880, 860, 70, (0xC8, 0xD2, 0xD6), 1, 12)
    rect(ctx, 180, 950, 26, 190, (0x7A, 0x86, 0x8C)); rect(ctx, 874, 950, 26, 190, (0x7A, 0x86, 0x8C))
    # patient: a sawtooth of tiny wins
    k = ease_io(prog(t, s0 + 0.15, 0.9))
    n = 60
    xs = [180 + i / n * 720 for i in range(int(n * k) + 1)]
    ys = [760 - (i % 6) * 14 + (60 if i % 6 == 0 else 0) - i * 0.6 for i in range(int(n * k) + 1)]
    poly(ctx, xs, ys, C["green"], 10, 1, glow=True)
    card(ctx, 760, 470, 250, 150, (0x0E, 0x14, 0x18), 1, 12, border=(0x5A, 0x64, 0x6B))
    heart_line(ctx, 775, 560, 220, 50, t, C["green"], 300)
    p = back(prog(t, T["table"], 0.4))
    if p > 0:
        ctx.save(); ctx.translate(250, 1020); ctx.rotate(-0.12 + math.sin(t * 3) * 0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        ctx.new_path(); ctx.move_to(-10, -150); ctx.line_to(0, -40); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        card(ctx, -150, -45, 330, 120, (0xF2, 0xE2, 0xB0), 1, 10)
        text(ctx, "PATIENT #4", 15, -5, 26, (0x5A, 0x64, 0x6B), 1, MONO, True, "center")
        text(ctx, "2-DAY RSI", 15, 52, 46, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    tag(ctx, 700, 760, "FAMOUS SHORT-TERM SETUP", C["yellow"], back(prog(t, wt("famous"), 0.35)), 28, -0.04)
    bunting(ctx, "STRATEGY AUTOPSY", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor")


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx)
    items = [("FILTER", "SPY ABOVE 200-DAY AVG", T["only"], C["blue"]),
             ("BUY", "2-DAY RSI BELOW 10", T["buy1"], C["green"]),
             ("SELL", "CLOSE ABOVE 5-DAY AVG", T["sell"], C["red"])]
    for k, (lab, sub, tt, col) in enumerate(items):
        p = back(prog(t, tt, 0.35))
        if p <= 0:
            continue
        y = 450 + k * 230
        ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.025 + k * 0.025); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -440, -95, 880, 190, C["cream"], 1, 16)
        rect(ctx, -436, -91, 220, 182, col)
        text(ctx, lab, -326, 20, 54, C["white"] if col != C["blue"] else C["white"], 1, HEAD, True, "center")
        text(ctx, sub, 110, 16, 40, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE RULES", t, s0)
    rocco(ctx, t, "lab")


def s_test(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    x, y, w, h = 120, 400, 840, 380
    card(ctx, x, y, w, h, (0x0E, 0x14, 0x18), 1, 14, border=C["green"])
    for k, col in enumerate((C["red"], C["yellow"], C["green"])):
        ctx.new_path(); ctx.arc(x + 30 + k * 30, y + 30, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    cmd = "> backtest rsi2 SPY 2005-2024"
    nch = int(len(cmd) * prog(t, s0 + 0.05, 0.9))
    text(ctx, cmd[:nch] + ("_" if int(t * 3) % 2 == 0 and nch < len(cmd) else ""), x + 26, y + 100, 30, C["green"], 1, MONO, True)
    for k, ln in enumerate(["5,033 trading days", "next-open fills, 0.05% fees", "running... done."]):
        la = prog(t, s0 + 0.8 + k * 0.3, 0.2)
        if la > 0:
            text(ctx, ln, x + 26, y + 170 + k * 50, 28, (0xB8, 0xC4, 0xCC), la, MONO, False)
    for k, (lab, tt) in enumerate((("20 YEARS", T["twenty1"]), ("FEES INCLUDED", T["fees"]))):
        p = back(prog(t, tt, 0.35))
        if p > 0:
            ctx.save(); ctx.translate(W / 2, 900 + k * 120); ctx.rotate(-0.03 + k * 0.05); ctx.scale(max(p, 1e-3), max(p, 1e-3))
            card(ctx, -300, -46, 600, 92, C["cream"], 1, 12)
            ctx.new_path(); ctx.arc(-245, 0, 28, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"])); ctx.fill()
            check(ctx, -260, 2, 30, C["ink"], 1, 7)
            text(ctx, lab, 20, 15, 44, C["ink"], 1, HEAD, True, "center")
            ctx.restore()
    bunting(ctx, "THE TEST", t, s0)
    rocco(ctx, t, "lab")


def money_printer(ctx, cx, cy, t, on):
    card(ctx, cx - 170, cy - 110, 340, 200, (0x5A, 0x64, 0x6B), 1, 18)
    rect(ctx, cx - 130, cy - 70, 260, 26, C["ink"])
    for j in range(3):
        ctx.new_path(); ctx.arc(cx - 110 + j * 40, cy + 40, 12, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba(C["green"] if (on and int(t * 6 + j) % 2) else C["ink"])); ctx.fill()
    if on:
        for k in range(6):
            ph = (t * 1.6 + k / 6) % 1
            bx = cx - 60 + math.sin(k * 2.1) * 120 * ph
            by = cy - 80 - ph * 420
            ctx.save(); ctx.translate(bx, by); ctx.rotate(math.sin(t * 4 + k) * 0.5)
            rect(ctx, -60, -28, 120, 56, (0x6D, 0xB8, 0x6A), 1 - ph * 0.6)
            rect(ctx, -12, -28, 24, 56, C["cream"], 0.9 * (1 - ph * 0.6))
            ctx.restore()


def s_trades(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x30, 0x22), (0x06, 0x16, 0x10))
    god_rays(ctx, W / 2, 700, t, 0.05, C["green"], 16)
    k = ease_io(prog(t, s0 + 0.1, T["s73"] - s0 + 0.4))
    n = int(150 * k)
    wr = 100 * sum(WINS[:n]) / max(1, n)
    flip_counter(ctx, 60, 330, 470, 160, "TRADES", f"{n}", C["white"], 1, 90)
    flip_counter(ctx, 550, 330, 470, 160, "WIN RATE", f"{wr:.0f}%" if n else "—", C["green"], 1, 90)
    tiles(ctx, 140, 540, n, 15, 44, 6, t)
    a = back(prog(t, T["average"], 0.35))
    tag(ctx, W / 2, 1110, "AVG HOLD: 3.5 DAYS", C["yellow"], a, 40, -0.04)
    if t >= T["money"] - 0.2:
        q = back(prog(t, T["money"] - 0.2, 0.4))
        ctx.save(); ctx.translate(W / 2 + 220, 1580); ctx.scale(max(q, 1e-3), max(q, 1e-3)); ctx.translate(-(W / 2 + 220), -1580)
        money_printer(ctx, W / 2 + 220, 1580, t, True)
        ctx.restore()
    bunting(ctx, "THE RESULTS", t, s0, [C["green"], C["yellow"], C["green"], C["white"]])
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


def s_problem(ctx, t, s0, s1):
    bg_fill(ctx, (0x1B, 0x1F, 0x3E), (0x0B, 0x0D, 0x1C))
    for kk in range(40):
        rect(ctx, (kk * 263) % W, 330 + (kk * 151) % 500, 5, 5, C["cream"], 0.4 + 0.5 * abs(math.sin(t * 2 + kk)))
    # timeline barcode: in-market days
    x0, y0, w, h = 90, 400, 900, 120
    card(ctx, x0 - 20, y0 - 60, w + 40, h + 130, C["cream"], 1, 14)
    text(ctx, "IN THE MARKET", x0, y0 - 18, 24, C["ink"], 0.6, MONO, True)
    k = ease_io(prog(t, s0 + 0.1, 1.6))
    upto = int(N * k)
    rect(ctx, x0, y0, w * k, h, (0xD8, 0xCE, 0xB4))
    for i in range(0, upto):
        if POSV[i] > 0:
            rect(ctx, x0 + i / N * w, y0, w / N + 0.6, h, (0x12, 0x9E, 0x5E))
    for yr in (2005, 2010, 2015, 2020, 2024):
        i = di(f"{yr}-01-01")
        text(ctx, str(yr), x0 + i / N * w, y0 + h + 40, 22, C["ink"], 0.55, MONO, True, "center")
    # donut
    cx, cy, r = 330, 900, 170
    d = ease_io(prog(t, T["ten3"], 0.8))
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["grey"])); ctx.set_line_width(70); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.105 * d); ctx.set_source_rgba(*rgba(C["green"])); ctx.set_line_width(70); ctx.stroke()
    text(ctx, f"{10.5 * d:.0f}%", cx, cy + 20, 90, C["green"], 1, MONO, True, "center")
    text(ctx, "INVESTED", cx, cy + 75, 28, C["cream"], 0.8, MONO, True, "center")
    q = back(prog(t, T["ninety"], 0.35))
    if q > 0:
        ctx.save(); ctx.translate(780, 900); ctx.rotate(0.05); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -200, -130, 400, 260, C["cream"], 1, 18)
        text(ctx, "90%", 0, 10, 110, C["red"], 1, HEAD, True, "center")
        text(ctx, "IN CASH", 0, 80, 40, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    tag(ctx, 780, 1110, "DOING NOTHING", C["grey"], back(prog(t, T["nothing"], 0.35)), 34, -0.04, C["white"])
    bunting(ctx, "THE PROBLEM", t, s0, [C["blue"], C["grey"], C["blue"], C["cream"]])
    rocco(ctx, t, "night", lambda e: "sleep" if e != "talk" else e)


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    card(ctx, 70, 400, 940, 720, (0x14, 0x18, 0x1C), 1, 20, border=C["yellow"])
    text(ctx, "$10,000 IN · SPY 2005-2024", W / 2, 470, 30, C["yellow"], 1, MONO, True, "center")
    a = ease_io(prog(t, T["sixteen2"] - 0.4, 1.0)); b = ease_io(prog(t, T["s71"] - 0.5, 1.0))
    flip_counter(ctx, 110, 520, 860, 190, "2-DAY RSI", money(10000 + 6525 * a) if t >= T["sixteen2"] - 0.5 else "—", C["red"], 1, 96)
    flip_counter(ctx, 110, 750, 860, 190, "BUY & HOLD", money(10000 + 60985 * b) if t >= T["buy2"] - 0.2 else "—", C["green"], 1, 96)
    box = (130, 975, 820, 110)
    k = ease_io(prog(t, s0 + 0.2, 2.5))
    up = int(1 + (N - 2) * k)
    xs, ys = series_xy(BHV, 0, N - 1, up, box, 0, 75000, 4); poly(ctx, xs, ys, C["green"], 5)
    xs, ys = series_xy(CONN, 0, N - 1, up, box, 0, 75000, 4); poly(ctx, xs, ys, C["red"], 6, 1, glow=True)
    bunting(ctx, "FINAL SCORE", t, s0)
    rocco(ctx, t, "race", prop=prop_flag)


def s_fees(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x2A, 0x36), (0x12, 0x15, 0x1C))
    base, top = 1060, 640
    vmin, vmax = 10000, 17000
    def yv(v):
        return base - (v - vmin) / (vmax - vmin) * (base - top)
    rect(ctx, 100, base, 880, 8, C["cream"])
    text(ctx, "FEE PER TRADE", W / 2, 1160, 30, C["cream"], 0.8, MONO, True, "center")
    for k, ((lab, v), tt) in enumerate(zip(FEES, (s0 + 0.1, T["broker"], T["more"]))):
        g = ease(prog(t, tt, 0.6))
        hgt = (base - yv(v)) * g
        x = 150 + k * 280
        card(ctx, x, base - hgt, 220, max(4, hgt), [C["green"], C["orange"], C["red"]][k], 1, 8)
        if g > 0.1:
            text(ctx, money_k(v * g + vmin * (1 - g)), x + 110, base - hgt - 20, 46, C["cream"], 1, HEAD, True, "center")
        text(ctx, lab, x + 110, base + 50, 34, C["cream"], 1, MONO, True, "center")
    p = back(prog(t, T["five"], 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 450); ctx.rotate(-0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -400, -70, 800, 140, C["red"], 1, 16)
        text(ctx, "+$533 IN 20 YEARS", 0, 24, 64, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "HIGHER FEES?", t, s0, [C["red"], C["ink"], C["red"], C["yellow"]])
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def s_verdict(ctx, t, s0, s1):
    bg_fill(ctx, (0xD9, 0xF2, 0xEA), (0xA8, 0xDD, 0xCB))
    for i in range(0, W, 90):
        rect(ctx, i, 0, 45, H, (0xFF, 0xFF, 0xFF), 0.12)
    for k, (lab, sub, tt, ok, x) in enumerate((("73%", "WIN RATE", T["win"], True, 285), ("$16K", "AFTER 20 YRS", T["profit"], False, 795))):
        p = back(prog(t, tt, 0.35))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(x, 560); ctx.rotate(-0.04 + k * 0.08); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -220, -170, 440, 340, C["cream"], 1, 18)
        text(ctx, lab, 0, -40, 96, C["ink"], 1, HEAD, True, "center")
        text(ctx, sub, 0, 20, 30, C["ink"], 0.7, MONO, True, "center")
        ctx.new_path(); ctx.arc(0, 100, 46, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"] if ok else C["red"])); ctx.fill()
        if ok:
            check(ctx, -22, 102, 46, C["ink"], 1, 9)
        else:
            ctx.new_path(); ctx.move_to(-20, 80); ctx.line_to(20, 120); ctx.move_to(20, 80); ctx.line_to(-20, 120)
            ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(9); ctx.stroke()
        ctx.restore()
    sk = prog(t, T["profit"] + 0.15, 0.3)
    if sk > 0:
        sc = 2.2 - 1.2 * ease(sk); a = clamp(sk * 2)
        ctx.save(); ctx.translate(W / 2, 960); ctx.rotate(-0.1); ctx.scale(sc, sc)
        rrect(ctx, -380, -110, 760, 220, 14); ctx.set_source_rgba(*rgba(C["cream"], 0.94 * a)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["red"], a)); ctx.set_line_width(10); ctx.stroke()
        text(ctx, "WIN RATE", 0, -20, 70, C["red"], a, HEAD, True, "center")
        text(ctx, "IS NOT PROFIT", 0, 70, 70, C["red"], a, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor", lambda e: "smug" if (e != "talk" and t >= T["profit"]) else e)


def s_outro(ctx, t, s0, s1):
    bg_fill(ctx, (0x6F, 0xC3, 0xE6), (0xBF, 0xE6, 0xF2))
    for k in range(4):
        x = (k * 310 + t * 50) % (W + 300) - 150
        y = 420 + (k % 2) * 160
        for dx, dy, r in ((0, 0, 40), (40, -14, 48), (86, 0, 38)):
            ctx.new_path(); ctx.arc(x + dx, y + dy, r, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.92); ctx.fill()
    rect(ctx, 0, 1460, W, H - 1460, (0x5C, 0xA8, 0x4A))
    p = back(prog(t, T["three_s"] - 0.3, 0.4))
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
    bunting(ctx, "WHO WON?", t, s0)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "title": s_title, "rules": s_rules, "test": s_test, "trades": s_trades, "problem": s_problem,
            "score": s_score, "fees": s_fees, "verdict": s_verdict, "outro": s_outro}
