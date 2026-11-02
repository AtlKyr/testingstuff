# ================================================================ Autopsy #5 scenes (Sell in May)
SKY = ((0x4F, 0xB3, 0xE8), (0xF7, 0xC9, 0x7A))


def sun(ctx, cx, cy, r, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 0.6)
    for k in range(12):
        ctx.save(); ctx.rotate(k * math.pi / 6)
        rect(ctx, r + 12, -9, 34 + 10 * math.sin(t * 4 + k), 18, C["yellow"], a)
        ctx.restore()
    ctx.restore()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0xFF, 0xD2, 0x4A), a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()


def cloud(ctx, x, y, s, col=(0xFF, 0xFF, 0xFF), a=0.92):
    for dx, dy, r in ((0, 0, 40), (40, -14, 48), (86, 0, 38)):
        ctx.new_path(); ctx.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def sunny_bg(ctx, t, rays=True):
    bg_fill(ctx, *SKY)
    if rays:
        god_rays(ctx, 900, 330, t, 0.10, C["white"], 14, 1500)
    for k in range(3):
        x = (k * 410 + t * 60) % (W + 300) - 200
        cloud(ctx, x, 560 + (k % 2) * 380, 1.0 + 0.3 * (k % 2), a=0.55)


def snow_bg(ctx, t):
    bg_fill(ctx, (0x1C, 0x2C, 0x52), (0x0A, 0x12, 0x26))
    for k in range(90):
        x = (k * 131 + math.sin(t * 1.3 + k) * 30) % W
        y = ((k * 223) + t * (120 + (k % 5) * 40)) % (H + 40) - 20
        ctx.new_path(); ctx.arc(x, y, 3 + (k % 4), 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.55); ctx.fill()


def fit(ctx, s, size, maxw, f=HEAD):
    while tw(ctx, s, size, f) > maxw and size > 10:
        size -= 2
    return size


def xmark(ctx, x, y, s, col, w=9):
    ctx.new_path(); ctx.move_to(x - s, y - s); ctx.line_to(x + s, y + s); ctx.move_to(x + s, y - s); ctx.line_to(x - s, y + s)
    ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def stamp_box(ctx, lines, x, y, t0, t, col, w=820, size=78, rot=-0.1):
    sk = prog(t, t0, 0.3)
    if sk <= 0:
        return
    sc = 2.2 - 1.2 * ease(sk); a = clamp(sk * 2)
    h = 70 + len(lines) * size * 1.1
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    rrect(ctx, -w / 2, -h / 2, w, h, 14); ctx.set_source_rgba(*rgba(C["cream"], 0.95 * a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(10); ctx.stroke()
    for k, ln in enumerate(lines):
        sz = fit(ctx, ln, size, w - 60)
        text(ctx, ln, 0, -h / 2 + 35 + size * 0.9 + k * size * 1.1, sz, col, a, HEAD, True, "center")
    ctx.restore()


# ---------------------------------------------------------------- 1 hook
def summer_tile(ctx, cx, cy, w, h, yr, r, p, grey):
    if p <= 0:
        return
    ok = r > 0
    ctx.save(); ctx.translate(cx, cy); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -w / 2, -h / 2, w, h, C["green"] if ok else C["red"], 1, 12)
    text(ctx, str(yr), 0, -h / 2 + 38, 30, C["ink"], 0.85, MONO, True, "center")
    text(ctx, f"{r:+.0f}%", 0, h / 2 - 22, 44, C["ink"] if ok else C["white"], 1, HEAD, True, "center")
    if grey > 0:
        rrect(ctx, -w / 2, -h / 2, w, h, 12); ctx.set_source_rgba(0.35, 0.37, 0.40, 0.72 * grey); ctx.fill()
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    sunny_bg(ctx, t)
    sun(ctx, 975, 150, 52, t)
    # sand + bouncing beach ball + info card fill the lower half
    rect(ctx, 0, 1700, W, H - 1700, (0xE8, 0xC9, 0x8A))
    bb = abs(math.sin(t * 3.2)) * 220
    ctx.save(); ctx.translate(860, 1600 - bb); ctx.rotate(t * 3)
    for q in range(6):
        ctx.new_path(); ctx.move_to(0, 0); ctx.arc(0, 0, 70, q * math.pi / 3, (q + 1) * math.pi / 3); ctx.close_path()
        ctx.set_source_rgba(*rgba([C["red"], C["white"], C["blue"], C["yellow"], C["white"], C["green"]][q])); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, 70, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    tag(ctx, 760, 1830, "SPY · MAY-OCT · 2005-2024", C["cream"], back(prog(t, 2.6, 0.35)), 28, 0.02)
    # giant number slams at frame 0
    p = back(prog(t, 0.0, 0.3))
    sc = 1.0 + 0.6 * (1 - ease(prog(t, 0.0, 0.25)))
    ctx.save(); ctx.translate(W / 2 - 60, 300); ctx.rotate(-0.04); ctx.scale(max(p * sc, 1e-3), max(p * sc, 1e-3))
    text(ctx, "17 OF 20", 0, 70, 200, C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    tag(ctx, W / 2, 470, "SUMMERS WENT UP", C["yellow"], back(prog(t, wt("summers") - 0.1, 0.35)), 40, 0.03)
    grey = ease(prog(t, T["skipped"], 0.4))
    tw_, th_, gap = 172, 120, 16
    x0 = W / 2 - (5 * tw_ + 4 * gap) / 2
    for k, sm in enumerate(SUMMERS):
        rr_, cc = divmod(k, 5)
        tt = 0.25 + k * 0.12
        summer_tile(ctx, x0 + cc * (tw_ + gap) + tw_ / 2, 590 + rr_ * (th_ + gap) + th_ / 2, tw_, th_, sm["y"], sm["r"],
                    back(prog(t, tt, 0.3)), grey)
    stamp_box(ctx, ["SKIPPED"], W / 2, 830, T["skipped"], t, C["red"], 700, 120, -0.12)
    rocco(ctx, t, "straw", lambda e: "shock" if (e != "talk" and t > T["skipped"]) else e)


# ---------------------------------------------------------------- 2 title
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
    # patient: a seasonal wave (green winters, grey summers)
    k = ease_io(prog(t, s0 + 0.15, 1.1))
    n = 120
    pts = [(160 + i / n * 600, 780 - 70 * math.sin(i / n * 4 * math.pi) - i * 0.9) for i in range(int(n * k) + 1)]
    for i in range(1, len(pts)):
        ph = (i / n * 2) % 1
        col = C["green"] if ph < 0.5 else (0x9A, 0xA4, 0xAA)
        poly(ctx, [pts[i - 1][0], pts[i][0]], [pts[i - 1][1], pts[i][1]], col, 10, 1)
    # calendar monitor
    card(ctx, 780, 470, 230, 210, C["cream"], 1, 12)
    rect(ctx, 784, 474, 222, 54, C["red"])
    text(ctx, "CALENDAR", 895, 511, 26, C["white"], 1, MONO, True, "center")
    mon = "MAY" if t >= T["may"] else ["APR", "APR", "MAR"][int(t * 2) % 3]
    pm = back(prog(t, T["may"], 0.3)) if t >= T["may"] else 1
    ctx.save(); ctx.translate(895, 610); ctx.scale(1, max(pm, 1e-3))
    text(ctx, mon, 0, 30, 84, C["ink"], 1, HEAD, True, "center")
    ctx.restore()
    p = back(prog(t, T["table"], 0.4))
    if p > 0:
        ctx.save(); ctx.translate(250, 1030); ctx.rotate(-0.12 + math.sin(t * 3) * 0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        ctx.new_path(); ctx.move_to(-10, -150); ctx.line_to(0, -40); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
        card(ctx, -160, -45, 350, 120, (0xF2, 0xE2, 0xB0), 1, 10)
        text(ctx, "PATIENT #5", 15, -5, 26, (0x5A, 0x64, 0x6B), 1, MONO, True, "center")
        text(ctx, "SELL IN MAY", 15, 52, 46, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    tag(ctx, 690, 760, "...AND GO AWAY", C["yellow"], back(prog(t, T["away"] - 0.15, 0.35)), 40, -0.05)
    bunting(ctx, "STRATEGY AUTOPSY", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor")


# ---------------------------------------------------------------- 3 rules
MONTHS = "JFMAMJJASOND"


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx)
    items = [("SELL", "END OF APRIL", T["sell"], C["red"]),
             ("BUY", "END OF OCTOBER", T["buy1"], C["green"]),
             ("CASH", "ALL SUMMER", T["cash1"], C["yellow"])]
    for k, (lab, sub, tt, col) in enumerate(items):
        p = back(prog(t, tt, 0.35))
        if p <= 0:
            continue
        y = 450 + k * 200
        ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.025 + k * 0.025); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -440, -85, 880, 170, C["cream"], 1, 16)
        rect(ctx, -436, -81, 220, 162, col)
        text(ctx, lab, -326, 20, 54, C["ink"] if col == C["yellow"] else C["white"], 1, HEAD, True, "center")
        text(ctx, sub, 110, 16, fit(ctx, sub, 48, 600), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    # 12-month strip: months light up as the rules are spoken
    x0, y0, mw = 90, 1040, 75
    a = ease(prog(t, s0 + 0.2, 0.4))
    for m in range(12):
        winter = m in (10, 11, 0, 1, 2, 3)
        lit = prog(t, (T["buy1"] if winter else T["cash1"]) + (m % 6) * 0.05, 0.25)
        col = C["green"] if winter else C["yellow"]
        bc = tuple(int(lerp(0x3A, c_, lit)) for c_ in col)
        card(ctx, x0 + m * mw, y0, mw - 8, 90, bc, a, 8, shadow=False)
        text(ctx, MONTHS[m], x0 + m * mw + (mw - 8) / 2, y0 + 60, 40, C["ink"] if lit > 0.5 else C["white"], a, MONO, True, "center")
    bunting(ctx, "THE RULES", t, s0)
    rocco(ctx, t, "lab")


# ---------------------------------------------------------------- 4 test
def s_test(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    x, y, w, h = 120, 400, 840, 380
    card(ctx, x, y, w, h, (0x0E, 0x14, 0x18), 1, 14, border=C["green"])
    for k, col in enumerate((C["red"], C["yellow"], C["green"])):
        ctx.new_path(); ctx.arc(x + 30 + k * 30, y + 30, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    cmd = "> backtest sell_in_may SPY"
    nch = int(len(cmd) * prog(t, s0 + 0.05, 0.8))
    text(ctx, cmd[:nch] + ("_" if int(t * 3) % 2 == 0 and nch < len(cmd) else ""), x + 26, y + 100, 34, C["green"], 1, MONO, True)
    for k, ln in enumerate([f"{N:,} trading days, 2005-2024", "next-open fills, 0.05% fees", f"in market: {TIM:.0f}% of days", "running... done."]):
        la = prog(t, s0 + 0.7 + k * 0.3, 0.2)
        if la > 0:
            text(ctx, ln, x + 26, y + 160 + k * 50, 28, (0xB8, 0xC4, 0xCC), la, MONO, False)
    for k, (lab, tt) in enumerate((("20 YEARS", T["twenty"]), ("$10,000 START", T["ten"]), ("FEES INCLUDED", T["fees1"]))):
        p = back(prog(t, tt, 0.35))
        if p > 0:
            ctx.save(); ctx.translate(W / 2 - 60 + k * 60, 880 + k * 105); ctx.rotate(-0.03 + k * 0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
            card(ctx, -300, -44, 600, 88, C["cream"], 1, 12)
            ctx.new_path(); ctx.arc(-245, 0, 28, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"])); ctx.fill()
            check(ctx, -260, 2, 30, C["ink"], 1, 7)
            text(ctx, lab, 20, 15, 44, C["ink"], 1, HEAD, True, "center")
            ctx.restore()
    if t >= T["ten"]:
        coin(ctx, 260, 1560 - abs(math.sin((t - T["ten"]) * 4)) * 120, 60, t)
    bunting(ctx, "THE TEST", t, s0)
    rocco(ctx, t, "detective", prop=prop_magnifier)


# ---------------------------------------------------------------- 5 crash (summer 2008)
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t, 11)
    i0, i1 = di("2008-01-02"), di("2008-12-31")
    a_, b_ = di("2008-05-01"), di("2008-11-03")
    box = (110, 430, 860, 470)
    seg = CLOSE[i0:i1 + 1]; vmin, vmax = seg.min() * 0.95, seg.max() * 1.03
    card(ctx, box[0] - 30, box[1] - 40, box[2] + 60, box[3] + 120, C["cream"], 1, 16)
    # summer zone
    xa, xb = sx_of(a_, i0, i1, box), sx_of(b_, i0, i1, box)
    za = ease(prog(t, T["summer08"], 0.4))
    rect(ctx, xa, box[1], (xb - xa) * za, box[3], (0xFF, 0xD2, 0x4A), 0.45)
    if za > 0.5:
        text(ctx, "MAY - OCT 2008", (xa + xb) / 2, box[1] + 40, 30, C["ink"], 0.8, MONO, True, "center")
    k = ease_io(prog(t, s0 + 0.2, 2.6))
    up = int(i0 + 1 + (i1 - i0 - 1) * k)
    xs, ys = series_xy(CLOSE, i0, i1, up, box, vmin, vmax, 1)
    poly(ctx, xs, ys, C["ink"], 6)
    if up > a_:
        xs, ys = series_xy(CLOSE, a_, b_, min(up, b_), (xa, box[1], xb - xa, box[3]), vmin, vmax, 1)
        xs = [sx_of(a_ + (xx - xa) / max(1, xb - xa) * (b_ - a_), i0, i1, box) for xx in xs]
        poly(ctx, xs, ys, C["red"], 9, 1, glow=True)
    for mm, lab in ((0, "JAN"), (4, "MAY"), (10, "NOV")):
        i = di(f"2008-{mm + 1:02d}-01")
        text(ctx, lab, sx_of(i, i0, i1, box), box[1] + box[3] + 50, 26, C["ink"], 0.6, MONO, True, "center")
    q = back(prog(t, T["t29"], 0.35))
    if q > 0:
        ctx.save(); ctx.translate(700, 760); ctx.rotate(0.06); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -170, -80, 340, 160, C["red"], 1, 16)
        text(ctx, f"{S2008:.0f}%", 0, 34, 100, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    tag(ctx, 640, 1090, "STRATEGY: IN CASH", C["green"], back(prog(t, T["cash2"] - 0.1, 0.35)), 42, -0.04)
    tag(ctx, 840, 1010, "CRASH", C["yellow"], back(prog(t, T["crash"], 0.3)), 40, 0.06) if t < T["cash2"] - 0.1 else None
    bunting(ctx, "DODGED IT?", t, s0, [C["red"], C["grey"], C["red"], C["yellow"]])
    rocco(ctx, t, "fire", lambda e: "smug" if (e != "talk" and t > T["cash2"]) else ("shock" if e != "talk" and t > T["crash"] else e),
          prop=prop_umbrella)


# ---------------------------------------------------------------- 6 drawdown
def s_drawdown(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x14, 0x1C), (0x12, 0x08, 0x0C))
    box = (110, 450, 860, 360)
    card(ctx, box[0] - 30, box[1] - 70, box[2] + 60, box[3] + 140, (0x0E, 0x14, 0x18), 1, 16, border=C["grey"])
    text(ctx, "DROP FROM THE PEAK", W / 2, box[1] - 22, 28, C["grey"], 1, MONO, True, "center")
    k = ease_io(prog(t, s0 + 0.15, 1.4))
    up = int(1 + (N - 2) * k)
    xs, ys = series_xy(BH_DD, 0, N - 1, up, box, -60, 0, 3)
    ctx.new_path(); ctx.move_to(box[0], box[1])
    for x_, y_ in zip(xs, ys):
        ctx.line_to(x_, y_)
    ctx.line_to(xs[-1], box[1]); ctx.close_path(); ctx.set_source_rgba(*rgba(C["red"], 0.45)); ctx.fill()
    poly(ctx, xs, ys, C["red"], 4)
    xs, ys = series_xy(SIM_DD, 0, N - 1, up, box, -60, 0, 3)
    poly(ctx, xs, ys, C["green"], 6, 1, glow=True)
    for yr in (2005, 2010, 2015, 2020, 2024):
        i = di(f"{yr}-01-01")
        text(ctx, str(yr), sx_of(i, 0, N - 1, box), box[1] + box[3] + 44, 24, C["grey"], 0.9, MONO, True, "center")
    for v in (-20, -40):
        yy = sy_of(v, -60, 0, box); rect(ctx, box[0], yy, box[2], 2, C["white"], 0.15)
        text(ctx, f"{v}%", box[0] + 6, yy - 8, 20, C["grey"], 0.8, MONO, True)
    a = ease_io(prog(t, T["t36"] - 0.2, 0.6)); b = ease_io(prog(t, T["f55"] - 0.2, 0.6))
    if t >= T["t36"] - 0.2:
        flip_counter(ctx, 60, 925, 470, 150, "SELL IN MAY", f"{SIM_DDV * a:.0f}%", C["green"], 1, 80)
    if t >= T["f55"] - 0.2:
        flip_counter(ctx, 550, 925, 470, 150, "BUY & HOLD", f"{BH_DDV * b:.0f}%", C["red"], 1, 80)
    bunting(ctx, "WORST DROP", t, s0, [C["green"], C["red"], C["green"], C["red"]])
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 7/8 winter vs summer bars
BASE_Y, TOP_Y = 1110, 600


def season_bars(ctx, t, gw, gs, show_s, xcross=0.0):
    hmax = BASE_Y - TOP_Y
    rect(ctx, 90, BASE_Y, 900, 8, C["cream"])
    for k, (lab, mult, g, col, x) in enumerate((("NOV-APR", WMULT, gw, (0x7F, 0xC8, 0xF8), 170), ("MAY-OCT", SMULT, gs, (0xFF, 0xC2, 0x3A), 590))):
        if k == 1 and not show_s:
            ctx.save(); ctx.set_dash([18, 12]); rrect(ctx, x, BASE_Y - 200, 320, 200, 8)
            ctx.set_source_rgba(*rgba(C["cream"], 0.6)); ctx.set_line_width(5); ctx.stroke(); ctx.restore()
            text(ctx, "?", x + 160, BASE_Y - 60, 110, C["cream"], 0.6, HEAD, True, "center")
            text(ctx, lab, x + 160, BASE_Y + 56, 38, C["cream"], 1, MONO, True, "center")
            continue
        hh = hmax * (mult - 1 + 1) / 3.8 * g
        hh = max(6, hh)
        card(ctx, x, BASE_Y - hh, 320, hh, col, 1, 10)
        if hh > 120:
            if k == 0:
                for q in range(int(hh / 70)):
                    xx = x + 50 + (q * 97) % 220; yy = BASE_Y - 40 - q * 70 + math.sin(t * 2 + q) * 6
                    ctx.save(); ctx.translate(xx, yy); ctx.rotate(t + q)
                    for r_ in range(3):
                        ctx.rotate(math.pi / 3); rect(ctx, -16, -3, 32, 6, C["white"], 0.8)
                    ctx.restore()
            else:
                sun(ctx, x + 160, BASE_Y - hh / 2, min(50, hh / 5), t, 0.9)
        val = 1 + (mult - 1) * g
        text(ctx, f"×{val:.2f}", x + 160, BASE_Y - hh - 24, 72, C["white"], 1, HEAD, True, "center", outline=10, ocol=C["ink"])
        text(ctx, lab, x + 160, BASE_Y + 56, 38, C["cream"], 1, MONO, True, "center")
        if k == 1 and xcross > 0:
            xmark(ctx, x + 160, BASE_Y - hh / 2, 120 * ease(xcross), C["red"], 22)


def s_problem(ctx, t, s0, s1):
    snow_bg(ctx, t)
    gw = ease_io(prog(t, T["winters"], T["times"] - T["winters"]))
    p = back(prog(t, s0 + 0.15, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 470); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -420, -55, 840, 110, C["cream"], 1, 14)
        text(ctx, "WHERE DID THE GAINS COME FROM?", 0, 16, fit(ctx, "WHERE DID THE GAINS COME FROM?", 46, 780), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    season_bars(ctx, t, gw, 0, False)
    tag(ctx, 330, 700, "WINTERS", (0x7F, 0xC8, 0xF8), back(prog(t, T["winters"], 0.35)), 44, -0.05) if gw < 0.6 else None
    bunting(ctx, "THE PROBLEM", t, s0, [C["blue"], C["white"], C["blue"], C["cream"]])
    rocco(ctx, t, "night")


def s_summers(ctx, t, s0, s1):
    sunny_bg(ctx, t, rays=True)
    rect(ctx, 60, 520, 960, 660, C["ink"], 0.35)
    gs = ease_io(prog(t, T["summers2"] + 0.1, T["doubled"] - T["summers2"] + 0.2))
    season_bars(ctx, t, 1, gs, True, prog(t, T["skip"], 0.3))
    p = back(prog(t, T["half"] - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 420); ctx.rotate(-0.04); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -420, -62, 840, 124, C["red"], 1, 16)
        text(ctx, "SKIP IT = END WITH HALF", 0, 22, fit(ctx, "SKIP IT = END WITH HALF", 60, 780), C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "BUT SUMMERS...", t, s0, [C["yellow"], C["red"], C["yellow"], C["white"]])
    rocco(ctx, t, "straw", lambda e: "sad" if (e != "talk" and t > T["skip"]) else e)


# ---------------------------------------------------------------- 9 score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    card(ctx, 70, 400, 940, 720, (0x14, 0x18, 0x1C), 1, 20, border=C["yellow"])
    text(ctx, "$10,000 IN · SPY 2005-2024", W / 2, 470, 30, C["yellow"], 1, MONO, True, "center")
    a = ease_io(prog(t, T["t35"] - 0.3, 0.9)); b = ease_io(prog(t, T["s71"] - 0.5, 1.0))
    flip_counter(ctx, 110, 520, 860, 190, "SELL IN MAY", money(10000 + (SIM_V - 10000) * a) if t >= T["t35"] - 0.4 else "—", C["red"], 1, 96)
    flip_counter(ctx, 110, 750, 860, 190, "BUY & HOLD", money(10000 + (BH_V - 10000) * b) if t >= T["buy2"] - 0.2 else "—", C["green"], 1, 96)
    box = (130, 975, 820, 120)
    k = ease_io(prog(t, s0 + 0.2, 2.8))
    up = int(1 + (N - 2) * k)
    xs, ys = series_xy(BHV, 0, N - 1, up, box, 0, 75000, 4); poly(ctx, xs, ys, C["green"], 5)
    xs, ys = series_xy(SIMV, 0, N - 1, up, box, 0, 75000, 4); poly(ctx, xs, ys, C["red"], 6, 1, glow=True)
    bunting(ctx, "FINAL SCORE", t, s0)
    rocco(ctx, t, "race", prop=prop_flag)


# ---------------------------------------------------------------- 10 flip it (summers only + fees)
def hbar(ctx, y, lab, v, g, col, vmax=75000):
    x0, wmax = 90, 900
    card(ctx, x0, y, wmax, 104, (0x1B, 0x22, 0x27), 1, 12, shadow=False, border=(0x3A, 0x42, 0x48))
    w_ = max(10, (wmax - 8) * (v / vmax) * g)
    rrect(ctx, x0 + 4, y + 4, w_, 96, 10); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    text(ctx, lab, x0 + 24, y + 42, 28, C["white"], 1, MONO, True, outline=6, ocol=C["ink"])
    text(ctx, money(v * g) if g > 0 else "?", x0 + 24, y + 88, 40, C["white"], 1, HEAD, True, outline=8, ocol=C["ink"])


def s_flip(ctx, t, s0, s1):
    bg_fill(ctx, (0x2E, 0x1F, 0x4A), (0x12, 0x0C, 0x20))
    for kk in range(30):
        x = (kk * 173 + t * 40 * (1 + kk % 3)) % (W + 40) - 20
        rect(ctx, x, 380 + (kk * 97) % 780, 6, 6, C["yellow"], 0.3 + 0.4 * abs(math.sin(t * 3 + kk)))
    a = ease(prog(t, s0 + 0.1, 0.5))
    g = ease_io(prog(t, T["nineteen"] - 0.3, 0.8))
    hbar(ctx, 420, "BUY & HOLD", BH_V, a, C["green"])
    hbar(ctx, 545, "SELL IN MAY (WINTERS)", SIM_V, a, (0x7F, 0xC8, 0xF8))
    hbar(ctx, 670, "SUMMERS ONLY", SUMONLY_V, g, C["orange"])
    tag(ctx, W / 2, 850, "THE PATTERN IS REAL", C["green"], back(prog(t, T["real1"] - 0.1, 0.35)), 46, -0.04)
    p = back(prog(t, T["fees2"] - 0.1, 0.35))
    if p > 0:
        ctx.save(); ctx.translate(W / 2, 1050); ctx.rotate(0.02); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -440, -85, 880, 170, C["cream"], 1, 16)
        text(ctx, "FEES x4 (0.20%)", -410, -30, 34, C["ink"], 0.75, MONO, True)
        fv = FEES[2][1]
        text(ctx, f"{money(SIM_V)} → {money(fv)}", -410, 30, 50, C["ink"], 1, HEAD, True)
        q = back(prog(t, T["two2"], 0.3))
        if q > 0:
            ctx.save(); ctx.translate(250, -95); ctx.rotate(0.08); ctx.scale(max(q, 1e-3), max(q, 1e-3))
            card(ctx, -170, -36, 340, 72, C["yellow"], 1, 10)
            text(ctx, "2 TRADES/YR", 0, 14, 38, C["ink"], 1, MONO, True, "center")
            ctx.restore()
        ctx.restore()
    bunting(ctx, "SUMMERS ONLY?", t, s0, [C["orange"], C["purple"], C["orange"], C["yellow"]])
    rocco(ctx, t, "grad", lambda e: "smug" if (e != "talk" and t > T["real1"]) else e)


# ---------------------------------------------------------------- 11 verdict
def s_verdict(ctx, t, s0, s1):
    bg_fill(ctx, (0xD9, 0xF2, 0xEA), (0xA8, 0xDD, 0xCB))
    for i in range(0, W, 90):
        rect(ctx, (i + t * 40) % (W + 90) - 90, 0, 45, H, (0xFF, 0xFF, 0xFF), 0.12)
    cards = (("×3.61 > ×1.96", "WINTER VS SUMMER", T["real2"], True, 285),
             ("$35K < $71K", "VS BUY & HOLD", T["bad"], False, 795))
    for k, (lab, sub, tt, ok, x) in enumerate(cards):
        p = back(prog(t, tt, 0.35))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(x, 560); ctx.rotate(-0.04 + k * 0.08); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -230, -170, 460, 340, C["cream"], 1, 18)
        text(ctx, lab, 0, -40, fit(ctx, lab, 80, 410), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub, 0, 20, 28, C["ink"], 0.7, MONO, True, "center")
        ctx.new_path(); ctx.arc(0, 100, 46, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["green"] if ok else C["red"])); ctx.fill()
        if ok:
            check(ctx, -22, 102, 46, C["ink"], 1, 9)
        else:
            xmark(ctx, 0, 100, 20, C["ink"], 9)
        ctx.restore()
    stamp_box(ctx, ["REAL PATTERN.", "BAD TRADE."], W / 2, 960, T["trade"] + 0.1, t, C["red"], 800, 76, -0.1)
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], C["green"], C["blue"]])
    rocco(ctx, t, "doctor", lambda e: "sad" if (e != "talk" and t >= T["trade"]) else e)


# ---------------------------------------------------------------- 12 outro
def s_outro(ctx, t, s0, s1):
    bg_fill(ctx, (0x6F, 0xC3, 0xE6), (0xBF, 0xE6, 0xF2))
    for k in range(4):
        x = (k * 310 + t * 50) % (W + 300) - 150
        cloud(ctx, x, 420 + (k % 2) * 160, 1.0)
    sun(ctx, 120, 320, 50, t)
    rect(ctx, 0, 1460, W, H - 1460, (0x5C, 0xA8, 0x4A))
    p = back(prog(t, s0 + 0.15, 0.4))
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
    bunting(ctx, "NEXT AUTOPSY?", t, s0)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "title": s_title, "rules": s_rules, "test": s_test, "crash": s_crash, "drawdown": s_drawdown,
            "problem": s_problem, "summers": s_summers, "score": s_score, "flip": s_flip, "verdict": s_verdict, "outro": s_outro}
