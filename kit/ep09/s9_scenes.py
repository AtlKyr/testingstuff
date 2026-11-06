# ================================================================ Autopsy #9 scenes (missing the 10 best days)
SCOL = (0x4F, 0xC3, 0xF7)    # STAYER (never sells)
JCOL = (0xFF, 0x9F, 0x1C)    # JUMPER (skips the 10 best days)
GOLD = (0xFF, 0xD2, 0x4A)
BG0, BG1 = (0x16, 0x12, 0x30), (0x05, 0x04, 0x10)


def star_shape(ctx, x, y, r, col, a=1.0, rot=0.0, outline=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.new_path()
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        ang = -math.pi / 2 + k * math.pi / 5
        (ctx.move_to if k == 0 else ctx.line_to)(math.cos(ang) * rr, math.sin(ang) * rr)
    ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    if outline:
        ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(max(2, r * 0.16)); ctx.stroke()
    else:
        ctx.new_path()
    ctx.restore()


def day_grid(ctx, t, a=1.0, glow=True):
    """5,033 trading days as tiny cells; the 10 best days glow gold"""
    cols, cw, x0, y0 = 72, 13, 72, 250
    rows = (N + cols - 1) // cols
    ctx.set_source_rgba(1, 1, 1, 0.07 * a)
    for r_ in range(rows):
        ctx.rectangle(x0, y0 + r_ * cw * 1.0, cols * cw - 3, cw - 3)
    ctx.fill()
    for k, d in enumerate(BEST):
        i = di(d); cx = x0 + (i % cols) * cw; cy = y0 + (i // cols) * cw
        pul = 0.6 + 0.4 * abs(math.sin(t * 3 + k))
        if glow:
            ctx.new_path(); ctx.arc(cx + 5, cy + 5, 26 * pul, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.82, 0.3, 0.22 * a); ctx.fill()
        rect(ctx, cx - 2, cy - 2, cw + 1, cw + 1, GOLD, a * pul)


def hud(ctx, t):
    a = ease(prog(t, SC["case"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev1"]
    tag(ctx, 150, 66, "CASE #9", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev1"], 0.35))
        card(ctx, 655, 38, 300, 54, C["green"], a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["case"]) / (T["stay"] - SC["case"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: MISS 10 DAYS?)
def hook_draw(ctx, t, tl):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 700, t, 0.07, GOLD, 14, 1400)
    day_grid(ctx, t, 0.9)
    rect(ctx, 0, 0, W, H, BG1, 0.35)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    hl = 1 + 0.12 * math.sin(math.pi * prog(tl, T["ten1"] - 0.1, 0.5))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    ctx.save(); ctx.translate(430, 520); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "MISS", 0, 0, 190, C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    s2 = max(p * sc * hl * wob, 1e-3)
    ctx.save(); ctx.translate(540, 880); ctx.rotate(0.03); ctx.scale(s2, s2)
    text(ctx, "10 DAYS", 0, 0, 250, GOLD, 1, HEAD, True, "center", outline=26, ocol=C["ink"])
    ctx.restore()
    q = back(prog(tl, -0.3, 0.3)); qq = 1 + 0.08 * math.sin(t * 7)
    ctx.save(); ctx.translate(820, 560); ctx.rotate(0.14 + math.sin(t * 3) * 0.06); ctx.scale(max(q * qq, 1e-3), max(q * qq, 1e-3))
    text(ctx, "?", 0, 0, 300, C["red"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    tag(ctx, 540, 1000, "IN 20 YEARS", C["cream"], back(prog(t, T["twenty1"] - 0.05, 0.3)), 44, -0.03)
    # price tag swinging in on "cost"
    c = back(prog(t, T["cost"] - 0.1, 0.35))
    if c > 0:
        ctx.save(); ctx.translate(250, 260); ctx.rotate(-0.12 + math.sin(t * 5) * 0.08); ctx.scale(max(c, 1e-3), max(c, 1e-3))
        card(ctx, -130, -60, 260, 120, C["red"], 1, 18, border=C["ink"])
        ctx.new_path(); ctx.arc(-95, 0, 12, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()
        text(ctx, "COST?", 20, 22, 62, C["white"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        ctx.restore()
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 guess: scratch or disaster?
def bandaid(ctx, x, y, s, rot):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -90, -30, 180, 60, (0xF2, 0xC2, 0x8E), 1, 30, shadow=False, border=C["ink"])
    rect(ctx, -32, -24, 64, 48, (0xE0, 0xA8, 0x70))
    for i in range(3):
        for j in range(2):
            rect(ctx, -22 + i * 18, -14 + j * 18, 6, 6, (0xB8, 0x80, 0x50))
    ctx.restore()


def boom(ctx, x, y, r, t):
    ctx.save(); ctx.translate(x, y); ctx.rotate(t * 0.8)
    for col, sc in ((C["red"], 1.0), (C["orange"], 0.72), (GOLD, 0.45)):
        ctx.new_path()
        for k in range(24):
            rr = r * sc * (1.0 if k % 2 == 0 else 0.55 + 0.08 * math.sin(t * 9 + k))
            ang = k * math.pi / 12
            (ctx.move_to if k == 0 else ctx.line_to)(math.cos(ang) * rr, math.sin(ang) * rr)
        ctx.close_path(); ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        star_shape(ctx, (k * 197) % W, 1300 - u * 1100, 8 + (k % 3) * 4, GOLD, 0.5 * (1 - u), t + k, False)
    text(ctx, "WHAT DOES IT COST?", W / 2, 420, 84, C["white"], back(prog(t, s0 + 0.05, 0.3)), HEAD, True, "center", outline=14, ocol=C["ink"])
    g = back(prog(t, s0 + 0.08, 0.35))
    if g > 0:
        ctx.save(); ctx.translate(W / 2, 760); ctx.scale(max(g, 1e-3), max(g, 1e-3))
        card(ctx, -470, -230, 940, 460, C["dark"], 1, 22, border=C["white"])
        text(ctx, "YOUR GUESS?", 0, -160, 50, GOLD, 1, HEAD, True, "center")
        blink = int(t * 4) % 2
        for k, (lab, col, fg, x, tt) in enumerate((("A  SCRATCH", (0x8F, 0xD3, 0xF2), C["ink"], -225, T["scratch"]),
                                                   ("B  DISASTER", C["red"], C["white"], 225, T["disaster"]))):
            on = (blink == k)
            hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
            ctx.save(); ctx.translate(x, 60); ctx.scale(hl, hl)
            card(ctx, -205, -170, 410, 300, col, 1, 18, border=C["white"] if on else C["ink"])
            if k == 0:
                bandaid(ctx, 0, -60, 1.0, -0.3 + math.sin(t * 3) * 0.1)
            else:
                boom(ctx, 0, -60, 80, t)
            text(ctx, lab, 0, 90, fit(ctx, lab, 64, 370), fg, 1, HEAD, True, "center")
            ctx.restore()
        ctx.restore()
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["disaster"]) else e)


# ---------------------------------------------------------------- 3 case file: where do the 10 days hide?
def s_case(ctx, t, s0, s1):
    bg_fill(ctx, (0x23, 0x3B, 0x2E), (0x0E, 0x1A, 0x13))
    for i in range(0, W, 90):
        rect(ctx, (i + t * 30) % (W + 90) - 90, 0, 2, H, C["white"], 0.05)
    p = back(prog(t, s0 + 0.05, 0.4))
    ctx.save(); ctx.translate(W / 2, 720); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -420, -330, 300, 80, (0xD9, 0xB0, 0x6A), 1, 12, shadow=False)
    card(ctx, -420, -280, 840, 600, (0xE2, 0xBC, 0x76), 1, 16)
    card(ctx, -380, -240, 760, 520, C["cream"], 1, 8, shadow=False)
    text(ctx, "CASE #9", -340, -165, 64, C["red"], 1, HEAD, True, "left")
    text(ctx, "THE 10 MISSING DAYS · SPY", -340, -110, 30, C["ink"], 0.8, MONO, True, "left")
    text(ctx, "WHERE THEY HIDE:", -340, -10, 46, C["ink"], 1, HEAD, True, "left")
    rect(ctx, -340, 30, 680, 90, (0x08, 0x08, 0x08))
    for k in range(6):
        rect(ctx, -330 + k * 112, 50, 90, 6, (0x30, 0x30, 0x30))
    text(ctx, "WHEN THEY HAPPENED:", -340, 190, 34, C["ink"], 1, HEAD, True, "left")
    rect(ctx, -340, 215, 520, 50, (0x08, 0x08, 0x08))
    ctx.restore()
    tag(ctx, 620, 1090, "WHERE NOBODY LOOKS", C["red"], back(prog(t, T["nobody"] - 0.05, 0.3)), 40, -0.04, C["white"])
    mx = 540 + math.sin(t * 2.2) * 260
    ctx.new_path(); ctx.arc(mx, 800, 80, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.25); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(14); ctx.stroke()
    ctx.new_path(); ctx.move_to(mx + 56, 856); ctx.line_to(mx + 130, 940); ctx.set_line_width(22); ctx.set_source_rgba(*rgba((0x6B, 0x4A, 0x2E))); ctx.stroke()
    text(ctx, "?", mx, 830, 90, GOLD, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    bunting(ctx, "THE MYSTERY", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 4 race start: two investors
def s_start(ctx, t, s0, s1):
    stadium(ctx, t)
    for k in range(2):
        y = 820 + k * 200
        rect(ctx, 0, y, W, 150, (0xB8, 0x4A, 0x32))
        rect(ctx, 0, y, W, 6, C["white"]); rect(ctx, 0, y + 144, W, 6, C["white"])
    rect(ctx, 250, 820, 16, 350, C["white"])
    go = t >= T["each"]
    for k, (cos, col, lab) in enumerate((("tophat", SCOL, "STAYER"), ("race", JCOL, "JUMPER"))):
        run = prog(t, T["each"], 2.0)
        x = 180 + ease_io(run) * 420
        mini_rocco(ctx, x, 950 + k * 200, 7, cos, t + k * 0.3, "smug" if go else "neutral", False, go)
        tag(ctx, x + 10, 810 + k * 200, lab, col, back(prog(t, T["investors"] - 0.05 + k * 0.15, 0.3)), 30, 0.02, C["ink"])
    q = back(prog(t, T["ten3"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(560, 560); ctx.rotate(0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        coin(ctx, -190, 0, 70, t)
        text(ctx, "$10,000", 60, 22, 76, GOLD, 1, MONO, True, "center", outline=8, ocol=C["ink"])
        text(ctx, "EACH", 60, 84, 34, C["white"], 1, MONO, True, "center", outline=5, ocol=C["ink"])
        ctx.restore()
    stamp_box(ctx, ["GO!"], 820, 420, T["each"], t, C["green"], 300, 100, -0.08)
    bunting(ctx, "TWO INVESTORS", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "race", prop=prop_flag)


# ---------------------------------------------------------------- 5 rules: two big icons
def chair(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    col = (0x8B, 0x5A, 0x2B)
    rect(ctx, -50, -90, 16, 150, col); rect(ctx, 34, -10, 16, 70, col); rect(ctx, -50, -10, 100, 18, col)
    rect(ctx, -50, -90, 90, 14, col); rect(ctx, -50, -60, 90, 10, col)
    ctx.restore()


def mini_cal(ctx, x, y, s, t, t_x):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    card(ctx, -70, -70, 140, 140, C["white"], 1, 10, shadow=False, border=C["ink"])
    rect(ctx, -70, -70, 140, 34, C["red"])
    for i in range(4):
        for j in range(3):
            rect(ctx, -56 + i * 30, -24 + j * 30, 20, 20, GOLD if (i + j) % 3 == 0 else (0xCC, 0xCC, 0xCC))
    xk = ease(prog(t, t_x, 0.3))
    if xk > 0:
        xmark(ctx, 0, 10, 55 * xk, C["red"], 12)
    ctx.restore()


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    for k, (title, l1, col, fg, y, tt, icon) in enumerate((("STAYER", "NEVER SELLS", SCOL, C["ink"], 540, T["one"], "chair"),
                                                           ("JUMPER", "SKIPS THE 10 BEST DAYS", JCOL, C["ink"], 920, T["other"], "cal"))):
        p = back(prog(t, tt - 0.1, 0.4))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.025 if k == 0 else 0.025); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -460, -160, 920, 320, col, 1, 22, border=C["ink"])
        card(ctx, -430, -130, 220, 260, C["dark"], 1, 16, shadow=False)
        if icon == "chair":
            chair(ctx, -320, 20, 1.3, t)
            mini_rocco(ctx, -330, 30, 5, "tophat", t, "smug", False, False)
        else:
            mini_cal(ctx, -320, 0, 1.2, t, T["best1"])
        text(ctx, title, 110, -50, 74, fg, 1, HEAD, True, "center")
        q = back(prog(t, (T["never"] if k == 0 else T["skips"]) - 0.05, 0.3))
        if q > 0:
            ctx.save(); ctx.translate(110, 70); ctx.scale(max(q, 1e-3), max(q, 1e-3))
            card(ctx, -300, -50, 600, 100, C["dark"], 1, 14, shadow=False)
            text(ctx, l1, 0, 18, fit(ctx, l1, 52, 560), C["white"], 1, HEAD, True, "center")
            ctx.restore()
        ctx.restore()
    tag(ctx, 800, 1130, "SPY · 2005-2024", C["cream"], back(prog(t, T["spy"] - 0.05, 0.3)), 34, 0.04)
    bunting(ctx, "THE RULES", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab")


# ---------------------------------------------------------------- 6-8 race chart
RBOX = (110, 620, 860, 450)


def race_idx(t):
    pts = [(SC["even"] + 0.2, 0), (T["even"] + 0.3, di("2008-09-30")), (SC["crash08"] + 0.15, di("2008-09-30")),
           (T["opens1"] + 0.2, di("2009-06-30")), (T["grow"] + 0.5, di("2019-12-31")), (SC["covid"] + 0.15, di("2019-12-31")),
           (T["again"] + 0.3, di("2021-06-30"))]
    if t <= pts[0][0]:
        return 1
    for (a, ia), (b, ib) in zip(pts, pts[1:]):
        if t <= b:
            return int(ia + (ib - ia) * ease_io((t - a) / max(1e-3, b - a)))
    return pts[-1][1]


def race_chart(ctx, t, zones=()):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 110, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = RBOX[0] + di(d0) / (N - 1) * RBOX[2]; x1 = RBOX[0] + di(d1) / (N - 1) * RBOX[2]
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    up = race_idx(t)
    vmax = max(16000.0, 1.15 * float(np.nanmax(SV[:up + 1])))
    tips = []
    for arr, col, w_ in ((SV, SCOL, 9), (JV, JCOL, 6)):
        xs, ys = series_xy(arr, 0, N - 1, up, RBOX, 0, vmax, 3)
        poly(ctx, xs, ys, col, w_, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (sx, sy), (jx, jy) = tips
    gap = jy - sy
    if gap > 30:    # gap bracket
        rect(ctx, sx + 14, sy, 6, gap, C["red"], 0.9)
    off = 0 if gap > 60 else 60     # keep the two minis apart while the lines overlap
    mini_rocco(ctx, sx, sy - 4 - off, 4, "tophat", t, "smug", False, False)
    mini_rocco(ctx, jx, jy - 4, 4, "race", t, "neutral" if gap < 30 else "sad", False, True)
    # legend
    for k, (lab, col) in enumerate((("STAYER", SCOL), ("JUMPER", JCOL))):
        rect(ctx, RBOX[0] + 420 + k * 230, RBOX[1] + RBOX[3] - 30, 36, 10, col)
        text(ctx, lab, RBOX[0] + 466 + k * 230, RBOX[1] + RBOX[3] - 14, 24, col, 1, MONO, True, "left")


def s_even(ctx, t, s0, s1):
    stadium(ctx, t)
    race_chart(ctx, t)
    tag(ctx, 540, 440, "2005-2007", C["cream"], back(prog(t, T["two2"], 0.3)), 36, -0.03)
    tag(ctx, 540, 524, "DEAD EVEN", GOLD, back(prog(t, T["dead"] - 0.05, 0.3)), 40, 0.02)
    bunting(ctx, "THE RACE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e)


def s_crash08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.25)])
    tag(ctx, 540, 440, "2008 CRASH", C["red"], back(prog(t, T["then"], 0.3)), 38, -0.03, C["white"])
    lab = "WATCH IT GROW" if t >= T["watch"] - 0.05 else "A GAP OPENS"
    tag(ctx, 540, 524, lab, JCOL, back(prog(t, T["gap"] - 0.05, 0.3)), 36, 0.02)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], C["red"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["crashes1"]) else e)


def s_covid(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x3A), (0x0A, 0x04, 0x12))
    stars(ctx, t, 40, 0, 1300, 7)
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.12), ("2020-02-20", "2020-03-23", C["purple"], 0.6)])
    tag(ctx, 540, 440, "2020: COVID", C["purple"], back(prog(t, T["covid"] - 0.05, 0.3)), 38, -0.03, C["white"])
    tag(ctx, 540, 524, "AGAIN", C["red"], back(prog(t, T["again"] - 0.05, 0.3)), 38, 0.02, C["white"])
    bunting(ctx, "2020", t, s0, [C["purple"], C["ink"], C["purple"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


# ---------------------------------------------------------------- 9 twist: all 10 best days inside crashes
PBOX = (110, 560, 860, 470)


def s_weird(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0E, 0x14), (0x0A, 0x04, 0x06))
    god_rays(ctx, W / 2, 760, t, 0.05, GOLD, 14, 1400)
    card(ctx, PBOX[0] - 30, PBOX[1] - 30, PBOX[2] + 60, PBOX[3] + 110, (0x0C, 0x10, 0x1C), 0.94, 18, border=C["grey"])
    za = ease(prog(t, T["middle"] - 0.2, 0.5))
    for i0, i1 in ZONES:
        x0 = sx_of(i0, 0, N - 1, PBOX); x1 = sx_of(i1, 0, N - 1, PBOX)
        rect(ctx, x0, PBOX[1], max(8, x1 - x0), PBOX[3], C["red"], 0.12 + 0.3 * za)
    if za > 0:
        text(ctx, "CRASH", sx_of(ZONES[0][0], 0, N - 1, PBOX) + 6, PBOX[1] + 40, 26, C["red"], za, MONO, True, "left")
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, PBOX), PBOX[1] + PBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    vmax = float(SPYC.max()) * 1.05
    xs, ys = series_xy(SPYC, 0, N - 1, N - 1, PBOX, 0, vmax, 3)
    poly(ctx, xs, ys, C["white"], 5, 0.9)
    text(ctx, "SPY", PBOX[0] + 10, PBOX[1] + 40, 28, C["white"], 0.9, MONO, True, "left")
    # 10 stars drop in one by one between "All" and "crashes"
    order = sorted(range(10), key=lambda k: BEST[k])
    span = max(0.6, T["crashes2"] - T["All"])
    for n_, k in enumerate(order):
        tt = T["All"] + n_ * span / 10
        p = back(prog(t, tt, 0.3))
        if p <= 0:
            continue
        i = di(BEST[k])
        x = sx_of(i, 0, N - 1, PBOX); y = sy_of(SPYC[i], 0, vmax, PBOX)
        jit = (n_ % 5) * 26 - 52
        star_shape(ctx, x + (n_ % 2) * 14 - 7, y - 40 - abs(jit), 22 * p, GOLD, 1, t * 0.5 + n_)
    cnt = sum(1 for n_ in range(10) if t >= T["All"] + n_ * span / 10)
    if cnt:
        flip_counter(ctx, 640, 380, 340, 130, "BEST DAYS", f"{cnt}/10", GOLD, 1, 64)
    tag(ctx, 330, 440, "THE WEIRD PART", C["red"], back(prog(t, T["weird"] - 0.05, 0.3)), 36, -0.04, C["white"])
    tag(ctx, 540, 1120, "ALL INSIDE CRASHES", GOLD, back(prog(t, T["crashes2"] - 0.05, 0.3)), 42, -0.03)
    bunting(ctx, "THE TWIST", t, s0, [C["red"], GOLD, C["red"], C["ink"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["weird"]) else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 best days next to the worst days (daily bars)
def bar_window(ctx, box, d0, d1, t, t0, dur, title):
    i0, i1 = di(d0), di(d1)
    card(ctx, box[0] - 20, box[1] - 70, box[2] + 40, box[3] + 100, (0x0C, 0x10, 0x1C), 0.95, 16, border=C["grey"])
    text(ctx, title, box[0], box[1] - 24, 30, C["white"], 1, MONO, True, "left")
    mid = box[1] + box[3] / 2
    rect(ctx, box[0], mid, box[2], 2, C["white"], 0.4)
    n = i1 - i0 + 1; bw = box[2] / n
    shown = int(n * clamp((t - t0) / dur))
    bset = set(di(d) for d in BEST); wset = set(di(d) for d in WORST)
    for k in range(shown):
        i = i0 + k; r = RET[i]; h = r / 0.15 * box[3] / 2
        col = GOLD if i in bset else (C["red"] if i in wset else (0x5A, 0x64, 0x6B))
        x = box[0] + k * bw
        if h >= 0:
            rect(ctx, x + 1, mid - h, bw - 2, h, col)
        else:
            rect(ctx, x + 1, mid, bw - 2, -h, col)
        if i in bset:
            star_shape(ctx, x + bw / 2, mid - h - 22, 14, GOLD, 1, t)
        if i in wset:
            xmark(ctx, x + bw / 2, mid - h + 22, 10, C["red"], 6)


def s_worst(ctx, t, s0, s1):
    rain_bg(ctx, t)
    bar_window(ctx, (110, 480, 860, 210), "2008-09-15", "2008-12-15", t, s0 + 0.1, 1.6, "FALL 2008 · DAILY MOVES")
    bar_window(ctx, (110, 810, 860, 210), "2020-02-24", "2020-04-20", t, s0 + 0.4, 1.4, "SPRING 2020 · DAILY MOVES")
    # legend
    star_shape(ctx, 150, 375, 16, GOLD, 1, 0); text(ctx, "BEST 10 DAYS", 178, 385, 28, GOLD, 1, MONO, True, "left", outline=5, ocol=C["ink"])
    xmark(ctx, 560, 375, 12, C["red"], 7); text(ctx, "WORST 10 DAYS", 586, 385, 28, C["red"], 1, MONO, True, "left", outline=5, ocol=C["ink"])
    hl = 1 + 0.1 * math.sin(math.pi * prog(t, T["worst1"] - 0.05, 0.5))
    tag(ctx, 540, 1110, f"{NEAR} OF 10: WITHIN 2 WEEKS", C["red"], back(prog(t, T["Seven"] - 0.05, 0.3)) * hl, 42, -0.03, C["white"])
    bunting(ctx, "BEST vs WORST", t, s0, [GOLD, C["red"], GOLD, C["ink"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["worst1"]) else e)


# ---------------------------------------------------------------- 11 dodge the panic -> miss the rescue
def rocket(ctx, x, y, s, t, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(6):   # flame
        u = (t * 6 + k / 6) % 1
        ctx.new_path(); ctx.arc(math.sin(k * 2.1 + t * 9) * 12, 120 + u * 140, 30 * (1 - u), 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba([C["orange"], GOLD, C["red"]][k % 3], a * (1 - u))); ctx.fill()
    ctx.new_path(); ctx.move_to(0, -150); ctx.curve_to(70, -80, 60, 60, 50, 110); ctx.line_to(-50, 110); ctx.curve_to(-60, 60, -70, -80, 0, -150)
    ctx.close_path(); ctx.set_source_rgba(*rgba(C["green"], a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke()
    ctx.new_path(); ctx.arc(0, -40, 24, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["white"], a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()
    for sgn in (-1, 1):
        ctx.new_path(); ctx.move_to(sgn * 50, 40); ctx.line_to(sgn * 95, 120); ctx.line_to(sgn * 48, 110); ctx.close_path()
        ctx.set_source_rgba(*rgba(C["red"], a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.stroke()
    ctx.restore()


def s_rescue(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x2A, 0x3A), (0x04, 0x0C, 0x14))
    skyline(ctx, 1250, t, 4, (0x0E, 0x1C, 0x2A))
    # EXIT door on the left
    card(ctx, 40, 860, 240, 400, (0x3A, 0x2A, 0x1A), 1, 10, border=C["ink"])
    tag(ctx, 160, 820, "EXIT", C["green"], 1.0, 40, 0.0, C["white"])
    text(ctx, "PANIC!", 540, 470, 120, C["red"], back(prog(t, T["panic"] - 0.1, 0.3)), HEAD, True, "center", outline=16, ocol=C["ink"])
    # the rescue rocket launches on "rescue" without him
    lp = prog(t, T["miss2"] - 0.1, 1.4)
    ry = 1000 - 900 * (lp ** 2)
    rocket(ctx, 800, ry, 1.0, t)
    tag(ctx, 800, ry + 300 if lp > 0 else 1180, "BEST DAY", GOLD, back(prog(t, s0 + 0.15, 0.3)), 34, 0.03)
    tag(ctx, 560, 640, "MISSED THE REBOUND", JCOL, back(prog(t, T["rescue"] - 0.05, 0.3)), 40, -0.03)
    bunting(ctx, "THE TRAP", t, s0, [C["red"], C["green"], C["red"], C["ink"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e, prop=prop_umbrella)


# ---------------------------------------------------------------- 12 final score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 430, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 480, 900, 230, "STAYER · NEVER SOLD", money(BH_V), C["green"], T["rev1"], t)
    redacted_counter(ctx, 90, 760, 900, 230, "JUMPER · SKIPPED 10 DAYS", money(J_V), C["red"], T["t31"] - 0.05, t)
    if t >= T["rev1"]:
        stamp_box(ctx, ["WINNER"], 830, 495, T["rev1"] + 0.25, t, C["green"], 260, 50, 0.1)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev1"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 13 more than half gone
def s_half(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x0E, 0x14), (0x10, 0x04, 0x06))
    god_rays(ctx, W / 2, 700, t, 0.06, C["red"], 14, 1400)
    base = 1120; hmax = 640
    for k, (lab, v, col, x) in enumerate((("STAYER", BH_V, SCOL, 300), ("JUMPER", J_V, JCOL, 780))):
        g = ease_io(prog(t, s0 + 0.05 + k * 0.15, 0.6))
        h = hmax * v / BH_V * g
        card(ctx, x - 150, base - h, 300, max(h, 4), col, 1, 12, border=C["ink"])
        for j in range(int(h // 40)):   # stacked bills
            rect(ctx, x - 130, base - 30 - j * 40, 260, 4, C["ink"], 0.25)
        text(ctx, lab, x, base + 50, 40, col, 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        if g > 0.9:
            text(ctx, money(v), x, base - h + 70, 44, C["white"], 1, MONO, True, "center", outline=7, ocol=C["ink"])
    # half line
    hy = base - hmax * 0.5
    for k in range(12):
        rect(ctx, 120 + k * 72, hy, 44, 6, C["white"], 0.8)
    text(ctx, "HALF", 1000, hy - 14, 30, C["white"], 0.9, MONO, True, "right", outline=5, ocol=C["ink"])
    stamp_box(ctx, [f"-{GAP_PCT:.0f}%"], 760, 520, T["gone"] - 0.05, t, C["red"], 380, 120, 0.08)
    bunting(ctx, "THE DAMAGE", t, s0, [C["red"], C["ink"], C["red"], C["white"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


# ---------------------------------------------------------------- 14 dodge the worst days too?
def hbar(ctx, y, lab, v, g, col, vmax):
    card(ctx, 90, y, 900, 160, C["dark"], 1, 16)
    text(ctx, lab, 120, y + 48, 30, col, 1, MONO, True, "left")
    w_ = (840 * v / vmax) * g
    if w_ > 2:
        card(ctx, 120, y + 76, w_, 56, col, 1, 10, shadow=False)
    if g > 0.05:
        text(ctx, money(v * g), 960, y + 48, 38, C["white"], 1, MONO, True, "right")


def s_both(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x3A, 0x2A), (0x05, 0x12, 0x0C))
    god_rays(ctx, W / 2, 700, t, 0.08, C["green"], 16, 1500)
    text(ctx, "SKIP THE 10 WORST TOO?", W / 2, 440, 72, C["white"], back(prog(t, T["dodge2"] - 0.05, 0.3)), HEAD, True, "center", outline=14, ocol=C["ink"])
    vmax = BOTH_V * 1.02
    hbar(ctx, 500, "NEVER SOLD", BH_V, 1.0, C["green"], vmax)
    hbar(ctx, 690, "SKIP 10 BEST", J_V, 1.0, JCOL, vmax)
    hbar(ctx, 880, "SKIP 10 BEST + 10 WORST", BOTH_V, ease_io(prog(t, T["worst2"], 1.2)), SCOL, vmax)
    tag(ctx, 700, 1110, "A HAIR AHEAD", GOLD, back(prog(t, T["hair"] - 0.05, 0.3)), 40, -0.04)
    tag(ctx, 300, 1110, "HINDSIGHT ONLY", C["cream"], back(prog(t, T["ahead"] + 0.1, 0.3)), 30, 0.04)
    bunting(ctx, "WHAT IF?", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "shock" if (e != "talk" and t > T["too"]) else e)


# ---------------------------------------------------------------- 15 verdict + FOLLOW (no spoken outro)
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3)
    rect(ctx, 0, 0, W, H, (0x05, 0x04, 0x10), 0.62)
    stamp_box(ctx, ["THE BEST DAYS HIDE", "INSIDE THE WORST."], W / 2, 560, T["best3"] - 0.05, t, GOLD, 880, 84, -0.05)
    stamp_box(ctx, ["STAY SEATED."], W / 2 + 10, 900, T["stay"] - 0.05, t, C["green"], 760, 110, 0.04)
    fb = back(prog(t, T["worst3"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2 + 160, 1120); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #10", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "case": s_case, "start": s_start, "rules": s_rules, "even": s_even,
            "crash08": s_crash08, "covid": s_covid, "weird": s_weird, "worst": s_worst, "rescue": s_rescue, "score": s_score,
            "half": s_half, "both": s_both, "verdict": s_verdict, "loop": s_loop}
