# ================================================================ Autopsy #8 scenes (overnight vs intraday)
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


def sun(ctx, cx, cy, r, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 0.6)
    for k in range(12):
        ctx.save(); ctx.rotate(k * math.pi / 6)
        rect(ctx, r + 12, -9, 34 + 10 * math.sin(t * 4 + k), 18, C["yellow"], a)
        ctx.restore()
    ctx.restore()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0xFF, 0xD2, 0x4A), a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()


MOONC = (0xE8, 0xE4, 0xFF)
NAVY, NAVY2 = (0x1A, 0x1F, 0x4A), (0x08, 0x0B, 0x22)
SKY, SKY2 = (0x8F, 0xD3, 0xF2), (0xFF, 0xE3, 0x9A)
NIGHTCOL = (0x9B, 0x7B, 0xFF)    # night trader line
DAYCOL = C["yellow"]             # day trader line


def moon(ctx, cx, cy, r, a=1.0, glow=True):
    if glow:
        g = cairo.RadialGradient(cx, cy, r * 0.6, cx, cy, r * 2.4)
        g.add_color_stop_rgba(0, 0.9, 0.9, 1, 0.35 * a); g.add_color_stop_rgba(1, 0.9, 0.9, 1, 0)
        ctx.set_source(g); ctx.new_path(); ctx.arc(cx, cy, r * 2.4, 0, 2 * math.pi); ctx.fill()
    ctx.push_group()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(MOONC, 1)); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR); ctx.new_path(); ctx.arc(cx + r * 0.45, cy - r * 0.25, r * 0.85, 0, 2 * math.pi); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


def stars(ctx, t, n=40, y0=0, y1=H, seed=1, a=1.0):
    rr = random.Random(seed)
    for k in range(n):
        x = rr.random() * W; y = y0 + rr.random() * (y1 - y0); s = 3 + rr.random() * 5
        tw_ = 0.35 + 0.65 * abs(math.sin(t * (1 + rr.random() * 2) + k))
        rect(ctx, x, y, s, s, C["white"], tw_ * a)


def night_bg(ctx, t, seed=1):
    bg_fill(ctx, NAVY, NAVY2); stars(ctx, t, 50, 0, 1300, seed)


def day_bg(ctx, t):
    bg_fill(ctx, SKY, SKY2)
    for k in range(4):
        x = (k * 310 + t * 50) % (W + 300) - 150
        cloud(ctx, x, 380 + (k % 2) * 180, 1.0)


def cloud(ctx, x, y, s, col=(0xFF, 0xFF, 0xFF), a=0.92):
    for dx, dy, r in ((0, 0, 40), (40, -14, 48), (86, 0, 38)):
        ctx.new_path(); ctx.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def mini_rocco(ctx, x, y, px, costume, t, expr="neutral", flip=False, run=True):
    bob = abs(math.sin(t * 12)) * px * 2 if run else abs(math.sin(t * 3)) * px
    ctx.save(); ctx.translate(x, y - bob)
    if flip:
        ctx.scale(-1, 1)
    ctx.rotate(math.sin(t * 12) * 0.06 if run else 0)
    ctx.translate(-RCOLS * px / 2, -RROWS * px)
    draw_rocco(ctx, 0, 0, px, expr, costume)
    ctx.restore()


# ---------------------------------------------------------------- mystery HUD (case tag + redacted winner + progress)
def hud(ctx, t):
    a = ease(prog(t, SC["case"], 0.4))
    if a <= 0:
        return
    rv = t >= T["seventy"]
    tag(ctx, 150, 66, "CASE #8", C["cream"], a, 26, -0.03)
    lab = "WINNER:"
    text(ctx, lab, 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["seventy"], 0.35))
        card(ctx, 655, 38, 300, 54, C["green"], a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["case"]) / (T["pays"] - SC["case"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: DAY or NIGHT?)
def hook_draw(ctx, t, tl):
    # split screen: day left, night right, diagonal seam
    bg_fill(ctx, SKY, SKY2)
    sun(ctx, 210, 470, 70, t)
    cloud(ctx, (t * 40) % 600 - 100, 760, 0.9)
    ctx.save(); ctx.new_path(); ctx.move_to(620, 0); ctx.line_to(W, 0); ctx.line_to(W, H); ctx.line_to(400, H); ctx.close_path(); ctx.clip()
    bg_fill(ctx, NAVY, NAVY2); stars(ctx, t, 40, 0, 1300, 2)
    moon(ctx, 860, 470, 70)
    ctx.restore()
    ctx.new_path(); ctx.move_to(620, 0); ctx.line_to(400, H); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(12); ctx.stroke()
    # giant words, already visible at frame 0
    p = back(prog(tl, -0.12, 0.3)); sc = 1.0 + 0.12 * (1 - ease(prog(tl, -0.05, 0.3)))
    hl_d = 1 + 0.12 * math.sin(math.pi * prog(tl, T["open1"] - 0.1, 0.5))
    hl_n = 1 + 0.12 * math.sin(math.pi * prog(tl, T["sleep"] - 0.1, 0.5))
    for wd, x, y, col, oc, hl, rot in (("DAY", 290, 760, C["yellow"], C["ink"], hl_d, -0.06), ("NIGHT", 770, 900, MOONC, C["ink"], hl_n, 0.05)):
        s_ = max(p * sc * hl * (1 + 0.03 * math.sin(t * 6)), 1e-3)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s_, s_)
        text(ctx, wd, 0, 0, 190 if wd == "DAY" else 140, col, 1, HEAD, True, "center", outline=26, ocol=oc)
        ctx.restore()
    q = back(prog(tl, -0.3, 0.3))
    ctx.save(); ctx.translate(530, 1020); ctx.rotate(-0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
    text(ctx, "or", -150, -10, 80, C["white"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    qq = 1 + 0.08 * math.sin(t * 7)
    ctx.save(); ctx.translate(560, 1090); ctx.rotate(0.1 + math.sin(t * 3) * 0.05); ctx.scale(max(q * qq, 1e-3), max(q * qq, 1e-3))
    text(ctx, "?", 0, 0, 300, C["red"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    # bell rings on "open" (market open), on the day side
    b = prog(t, T["market1"] - 0.1, 1.2)
    if 0 < b < 1:
        ang = math.sin(b * 30) * 0.4 * (1 - b)
        ctx.save(); ctx.translate(200, 280); ctx.rotate(ang)
        ctx.new_path(); ctx.move_to(-60, 60); ctx.curve_to(-60, -60, 60, -60, 60, 60); ctx.close_path()
        ctx.set_source_rgba(*rgba(C["yellow"])); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(7); ctx.stroke()
        ctx.new_path(); ctx.arc(0, 72, 16, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()
        ctx.restore()
        tag(ctx, 330, 360, "MARKET OPEN", C["cream"], back(prog(t, T["market1"], 0.3)), 30, -0.04)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 night ("only while you sleep" + guess)
def bed(ctx, x, y, t):
    card(ctx, x, y, 520, 120, (0x7A, 0x4A, 0x2A), 1, 12)
    card(ctx, x + 20, y - 60, 480, 80, (0xCF, 0xD6, 0xF5), 1, 18, shadow=False)
    rect(ctx, x, y - 140, 26, 260, (0x5A, 0x34, 0x1C)); rect(ctx, x + 494, y - 90, 26, 210, (0x5A, 0x34, 0x1C))


def s_night(ctx, t, s0, s1):
    night_bg(ctx, t, 4)
    moon(ctx, 820, 330 + math.sin(t) * 10, 90)
    skyline(ctx, 1240, t, 5, (0x14, 0x18, 0x36))
    # stock certificate held overnight
    p = back(prog(t, s0 + 0.1, 0.4))
    if p > 0:
        ctx.save(); ctx.translate(300, 500); ctx.rotate(-0.08 + math.sin(t * 2) * 0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -190, -110, 380, 220, C["cream"], 1, 12, border=NIGHTCOL)
        text(ctx, "SPY", 0, -10, 90, NIGHTCOL, 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        text(ctx, "HELD OVERNIGHT", 0, 60, 30, C["ink"], 1, MONO, True, "center")
        ctx.restore()
    for k in range(3):   # Zzz
        u = ((t - s0) * 0.7 + k / 3) % 1
        if t < T["guess"]:
            text(ctx, "z", 780 + u * 140 + k * 10, 1000 - u * 260, 50 + k * 16, C["white"], 1 - u, HEAD, True, "center")
    # guess panel (A/B)
    g = back(prog(t, T["guess"] - 0.05, 0.35))
    if g > 0:
        ctx.save(); ctx.translate(W / 2, 830); ctx.scale(max(g, 1e-3), max(g, 1e-3))
        card(ctx, -440, -170, 880, 340, C["dark"], 1, 22, border=C["white"])
        text(ctx, "GUESS WHO WINS", 0, -105, 46, C["white"], 1, HEAD, True, "center")
        blink = int(t * 4) % 2
        for k, (lab, col, fg, x) in enumerate((("A  DAY", C["yellow"], C["ink"], -210), ("B  NIGHT", NIGHTCOL, C["white"], 210))):
            on = (blink == k)
            card(ctx, x - 190, -50, 380, 170, col, 1, 18, border=C["white"] if on else C["ink"])
            text(ctx, lab, x, 60, fit(ctx, lab, 72, 340), fg, 1, HEAD, True, "center")
        ctx.restore()
    rocco(ctx, t, "night", lambda e: ("sleep" if (t < T["guess"] and e != "talk") else ("shock" if e != "talk" else e)))


# ---------------------------------------------------------------- 3 case file
def s_case(ctx, t, s0, s1):
    bg_fill(ctx, (0x23, 0x3B, 0x2E), (0x0E, 0x1A, 0x13))
    for i in range(0, W, 90):
        rect(ctx, (i + t * 30) % (W + 90) - 90, 0, 2, H, C["white"], 0.05)
    p = back(prog(t, s0 + 0.05, 0.4))
    ctx.save(); ctx.translate(W / 2, 760); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -420, -330, 300, 80, (0xD9, 0xB0, 0x6A), 1, 12, shadow=False)
    card(ctx, -420, -280, 840, 600, (0xE2, 0xBC, 0x76), 1, 16)
    card(ctx, -380, -240, 760, 520, C["cream"], 1, 8, shadow=False)
    text(ctx, "CASE #8", -340, -170, 64, C["red"], 1, HEAD, True, "left")
    text(ctx, "NIGHT vs DAY · SPY", -340, -115, 32, C["ink"], 0.8, MONO, True, "left")
    text(ctx, "THE ANSWER:", -340, -10, 46, C["ink"], 1, HEAD, True, "left")
    rect(ctx, -340, 30, 680, 90, (0x08, 0x08, 0x08))
    for k in range(6):
        rect(ctx, -330 + k * 112, 50, 90, 6, (0x30, 0x30, 0x30))
    ctx.restore()
    tag(ctx, 640, 1080, "ONE TINY NUMBER", C["red"], back(prog(t, T["tiny1"], 0.3)), 40, -0.05, C["white"])
    # magnifier sweeping over the redacted bar
    mx = 540 + math.sin(t * 2.2) * 260
    ctx.new_path(); ctx.arc(mx, 840, 80, 0, 2 * math.pi); ctx.set_source_rgba(0.7, 0.9, 1, 0.25); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(14); ctx.stroke()
    ctx.new_path(); ctx.move_to(mx + 56, 896); ctx.line_to(mx + 130, 980); ctx.set_line_width(22); ctx.set_source_rgba(*rgba((0x6B, 0x4A, 0x2E))); ctx.stroke()
    text(ctx, "?", mx, 870, 90, C["yellow"], 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    bunting(ctx, "THE MYSTERY", t, s0, [C["red"], C["ink"], C["yellow"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 4 rules (two big icons)
def rule_card(ctx, x, y, p, dark, title, l1, l2, t, t1, t2, icon):
    if p <= 0:
        return
    bgc, fg = (NAVY, C["white"]) if dark else ((0xFF, 0xE0, 0x7A), C["ink"])
    ctx.save(); ctx.translate(x, y); ctx.rotate(-0.025 if not dark else 0.025); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -460, -175, 920, 350, bgc, 1, 22, border=C["ink"])
    if icon == "sun":
        sun(ctx, -340, -50, 62, t)
    else:
        moon(ctx, -340, -50, 68, glow=False); stars(ctx, t, 8, -170, -100, 9)
    text(ctx, title, -340, 120, 40, fg, 1, HEAD, True, "center")
    for k, (ln, tt, col, arrow) in enumerate(((l1, t1, C["green"], 1), (l2, t2, C["red"], -1))):
        q = back(prog(t, tt - 0.05, 0.3))
        if q <= 0:
            continue
        yy = -60 + k * 140
        ctx.save(); ctx.translate(90, yy); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -280, -55, 560, 110, col, 1, 14)
        ctx.new_path(); ctx.move_to(-235, 18 * arrow); ctx.line_to(-205, -22 * arrow); ctx.line_to(-175, 18 * arrow); ctx.close_path()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.fill()
        text(ctx, ln, 30, 18, fit(ctx, ln, 50, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    ctx.restore()


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    clock(ctx, 920, 1120, 70, t, 3.0)
    rule_card(ctx, W / 2, 540, back(prog(t, T["day1"] - 0.1, 0.4)), False, "DAY", "BUY at the OPEN", "SELL at the CLOSE",
              t, T["buys"], T["sells"], "sun")
    rule_card(ctx, W / 2, 935, back(prog(t, T["night1"] - 0.1, 0.4)), True, "NIGHT", "BUY at the CLOSE", "SELL next OPEN",
              t, T["night1"] + 0.25, T["opposite"], "moon")
    bunting(ctx, "THE RULES", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab")


# ---------------------------------------------------------------- 5 race start
def s_start(ctx, t, s0, s1):
    stadium(ctx, t)
    # track lanes
    for k, col in enumerate((DAYCOL, NIGHTCOL)):
        y = 820 + k * 200
        rect(ctx, 0, y, W, 150, (0xB8, 0x4A, 0x32))
        rect(ctx, 0, y, W, 6, C["white"]); rect(ctx, 0, y + 144, W, 6, C["white"])
    rect(ctx, 250, 820, 16, 350, C["white"])    # start line
    go = t >= T["each"]
    for k, (cos, col, lab) in enumerate((("straw", DAYCOL, "DAY"), ("night", NIGHTCOL, "NIGHT"))):
        run = prog(t, T["each"], 2.5)
        x = 180 + ease_io(run) * (700 if k == 1 else 640)
        mini_rocco(ctx, x, 950 + k * 200, 7, cos, t + k * 0.3, "shock" if go else "neutral", False, go)
        tag(ctx, x, 830 + k * 200 - 20, lab, col, back(prog(t, s0 + 0.2 + k * 0.15, 0.3)), 30, 0.02, C["ink"])
    tag(ctx, 300, 470, "SPY · 20 YEARS", C["cream"], back(prog(t, T["twenty1"], 0.3)), 40, -0.05)
    q = back(prog(t, T["ten"] - 0.05, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(760, 600); ctx.rotate(0.05); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        coin(ctx, -150, 0, 70, t)
        text(ctx, "$10,000", 70, 22, 64, C["yellow"], 1, MONO, True, "center", outline=8, ocol=C["ink"])
        text(ctx, "EACH", 70, 80, 32, C["white"], 1, MONO, True, "center", outline=5, ocol=C["ink"])
        ctx.restore()
    stamp_box(ctx, ["GO!"], 540, 700, T["each"], t, C["green"], 360, 110, -0.08)
    bunting(ctx, "THE RACE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "race", prop=prop_flag)


# ---------------------------------------------------------------- 6-8 race chart (before fees)
RBOX = (110, 600, 860, 470)
VMIN, VMAX = 4000, 50000


def race_idx(t):
    """map time -> index of the race (continuous across the three race scenes)"""
    pts = [(SC["crash08"] + 0.2, 0), (T["ahead"] + 0.4, di("2009-03-09")), (SC["covid"] + 0.3, di("2019-12-31")),
           (T["overnight"] + 0.4, di("2020-06-30")), (SC["closed"] + 0.2, di("2020-12-31")), (T["closed"] + 0.2, N - 1)]
    if t <= pts[0][0]:
        return 1
    for (a, ia), (b, ib) in zip(pts, pts[1:]):
        if t <= b:
            return int(ia + (ib - ia) * ease_io((t - a) / (b - a)))
    return N - 1


def zone(ctx, d0, d1, col, a, label=None, la=0.0):
    x0 = RBOX[0] + di(d0) / (N - 1) * RBOX[2]; x1 = RBOX[0] + di(d1) / (N - 1) * RBOX[2]
    rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)


def race_vmax(up):
    return max(16000.0, 1.12 * float(np.nanmax(NG[:up + 1])))


def race_chart(ctx, t, zones=()):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 110, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for z in zones:
        zone(ctx, *z)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    year_axis(ctx, RBOX, 0, N - 1, [2005, 2008, 2012, 2016, 2020, 2024], 0.7, 26)
    text(ctx, "BEFORE FEES", RBOX[0] + 10, RBOX[1] + 36, 24, C["grey"], 0.9, MONO, True, "left")
    up = race_idx(t)
    vmax = race_vmax(up)
    for arr, col, cos, ex in ((DG, DAYCOL, "straw", "sad"), (NG, NIGHTCOL, "night", "smug")):
        xs, ys = series_xy(arr, 0, N - 1, up, RBOX, VMIN, vmax, 3)
        poly(ctx, xs, ys, col, 7, 1, glow=True)
        mini_rocco(ctx, xs[-1], ys[-1] - 4, 4, cos, t, ex)


def s_crash08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.25)])
    lab = "2008 CRASH: HITS IN DAYLIGHT" if t >= T["daylight"] - 0.05 else "2008 CRASH"
    tag(ctx, 540, 440, lab, C["red"], back(prog(t, T["y2008"], 0.3)), 34, -0.03, C["white"])
    tag(ctx, 540, 522, "NIGHT PULLS AHEAD", NIGHTCOL, back(prog(t, T["ahead"] - 0.1, 0.3)), 34, 0.02, C["white"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], C["red"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["crash"]) else e)


def s_covid(ctx, t, s0, s1):
    night_bg(ctx, t, 7)
    moon(ctx, 900, 1180, 60)
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.12), ("2020-02-20", "2020-03-23", NIGHTCOL, 0.55)])
    tag(ctx, 540, 440, "2020: COVID", C["purple"], back(prog(t, T["covid"] - 0.05, 0.3)), 36, -0.03, C["white"])
    tag(ctx, 540, 522, "STRIKES OVERNIGHT", MOONC, back(prog(t, T["overnight"] - 0.05, 0.3)), 34, 0.02)
    bunting(ctx, "2020", t, s0, [C["purple"], C["ink"], C["purple"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def s_closed(ctx, t, s0, s1):
    night_bg(ctx, t, 9)
    skyline(ctx, 1250, t, 8, (0x12, 0x16, 0x30))
    race_chart(ctx, t, [("2007-10-10", "2009-03-09", C["red"], 0.12), ("2020-02-20", "2020-03-23", NIGHTCOL, 0.3)])
    # gap bracket at the end
    g = ease(prog(t, T["gains"], 0.5))
    if g > 0:
        x = RBOX[0] + RBOX[2] + 4
        vm = race_vmax(N - 1)
        y1 = RBOX[1] + RBOX[3] - (NG[-1] - VMIN) / (vm - VMIN) * RBOX[3]
        y2 = RBOX[1] + RBOX[3] - (DG[-1] - VMIN) / (vm - VMIN) * RBOX[3]
        ctx.new_path(); ctx.move_to(x, y2); ctx.line_to(x + 30 * g, y2); ctx.line_to(x + 30 * g, y2 + (y1 - y2) * g); ctx.line_to(x, y2 + (y1 - y2) * g)
        ctx.set_source_rgba(*rgba(C["green"])); ctx.set_line_width(8); ctx.stroke()
    stamp_box(ctx, ["MOST GAINS:", "WHILE CLOSED"], 540, 470, T["closed"] - 0.1, t, NIGHTCOL, 700, 62, -0.04)
    bunting(ctx, "2024", t, s0, [NIGHTCOL, C["yellow"], NIGHTCOL, C["white"]])
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 9 twist: the tiny number
def s_tiny(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0E, 0x14), (0x0A, 0x04, 0x06))
    god_rays(ctx, W / 2, 700, t, 0.06, C["red"], 14, 1400)
    p = back(prog(t, s0 + 0.05, 0.35))
    ctx.save(); ctx.translate(W / 2, 720); ctx.rotate(0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -420, -240, 840, 480, C["cream"], 1, 14)
    text(ctx, "THE TINY NUMBER", 0, -160, 44, C["ink"], 1, HEAD, True, "center")
    tear = ease(prog(t, T["point"] - 0.1, 0.45))
    big = "0.05%"
    text(ctx, big, 0, 70, 210, C["red"], 1, MONO, True, "center", outline=10, ocol=C["ink"])
    if tear < 1:   # redaction bar flies off
        ctx.save(); ctx.translate(tear * 900, -tear * 300); ctx.rotate(tear * 0.8)
        rect(ctx, -380, -90, 760, 200, (0x08, 0x08, 0x08))
        ctx.restore()
    text(ctx, "PER TRADE", 0, 180, 40, C["ink"], ease(prog(t, T["percent"], 0.3)), MONO, True, "center")
    ctx.restore()
    tag(ctx, 700, 1080, "THE FEE", C["red"], back(prog(t, T["percent"] + 0.4, 0.3)), 44, -0.05, C["white"])
    bunting(ctx, "THE TWIST", t, s0, [C["red"], C["ink"], C["red"], C["yellow"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["point"]) else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 fees x2 a day x 5,000 days
def campfire(ctx, cx, cy, t):
    for k in range(6):
        u = ((t * 0.7 + k / 6) % 1)
        x = cx - 170 + k * 68 + math.sin(t * 3 + k) * 30
        y = cy - 560 + u * 480
        ctx.save(); ctx.translate(x, y); ctx.rotate(math.sin(t * 4 + k) * 0.6)
        card(ctx, -46, -24, 92, 48, (0x8F, 0xD1, 0x8B), 1 - u * 0.7, 6, shadow=False, border=(0x2E, 0x6B, 0x34))
        text(ctx, "$", 0, 13, 34, (0x2E, 0x6B, 0x34), 1 - u * 0.7, HEAD, True, "center")
        ctx.restore()
    for k in range(4):
        rect(ctx, cx - 170 + k * 20, cy + 10 - k * 6, 300 - k * 40, 26, (0x6B, 0x3E, 0x1E))
    for k, (col, sc) in enumerate(((C["red"], 1.0), (C["orange"], 0.75), (C["yellow"], 0.45))):
        ctx.new_path(); ctx.move_to(cx - 170 * sc, cy + 10)
        for q in range(9):
            xx = cx - 170 * sc + (q + 0.5) * 340 * sc / 9
            hh = (150 + 90 * math.sin(t * 9 + q * 1.7 + k)) * sc * (1.3 if q in (3, 4, 5) else 0.9)
            ctx.line_to(xx, cy - hh); ctx.line_to(cx - 170 * sc + (q + 1) * 340 * sc / 9, cy + 10)
        ctx.close_path(); ctx.set_source_rgba(*rgba(col, 0.95)); ctx.fill()


def s_fees(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x14, 0x0A), (0x10, 0x05, 0x02))
    for k in range(30):
        x = (k * 131 + math.sin(t + k) * 40) % W; y = H - ((k * 97 + t * 260) % 1500)
        rect(ctx, x, y, 6, 6, C["orange"], 0.5)
    campfire(ctx, 540, 1000, t)
    a = ease_io(prog(t, T["five2"] - 0.1, 1.2))
    flip_counter(ctx, 140, 380, 800, 200, "FEE PAID", f"{int(1 + (2 * NDAYS - 1) * a):,} TIMES" if t >= T["five2"] - 0.1 else "...", C["red"], 1, 84)
    tag(ctx, 300, 650, "x2 A DAY", C["yellow"], back(prog(t, T["twice"] - 0.05, 0.3)), 44, -0.06)
    tag(ctx, 760, 650, f"{NDAYS:,} DAYS", C["cream"], back(prog(t, T["five2"] - 0.05, 0.3)), 44, 0.05)
    bunting(ctx, "THE FEE", t, s0, [C["red"], C["orange"], C["yellow"], C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["days"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 11 final score (with fees)
def redacted_counter(ctx, x, y, w, h, label, value, col, t_rev, t, icon=None):
    card(ctx, x, y, w, h, C["dark"], 1, 16)
    text(ctx, label, x + 30, y + 46, 30, C["grey"], 1, MONO, True, "left")
    if icon == "sun":
        sun(ctx, x + w - 60, y + 45, 22, t)
    elif icon == "moon":
        moon(ctx, x + w - 60, y + 45, 26, glow=False)
    if t >= t_rev:
        p = back(prog(t, t_rev, 0.35))
        sz = fit(ctx, value, 110, w - 80, MONO) * max(p, 0.01)
        text(ctx, value, x + w / 2, y + h - 40, sz, col, 1, MONO, True, "center")
        tear = ease(prog(t, t_rev, 0.4))
        if tear < 1:
            ctx.save(); ctx.translate(x + w / 2 + tear * 700, y + h / 2 + 20 - tear * 260); ctx.rotate(tear * 1.2)
            rect(ctx, -w / 2 + 30, -60, w - 60, 120, (0x05, 0x05, 0x05)); ctx.restore()
    else:
        rect(ctx, x + 30, y + 70, w - 60, h - 95, (0x05, 0x05, 0x05))
        text(ctx, "$??,???", x + w / 2, y + h - 48, 76, (0x55, 0x5B, 0x60), 1, MONO, True, "center")


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · WITH 0.05% FEES", W / 2, 420, 32, C["yellow"], 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 460, 900, 200, "DAY TRADER", "$" + f"{DF_V:,}", C["red"], T["n97"] - 0.05, t, "sun")
    redacted_counter(ctx, 90, 690, 900, 200, "NIGHT TRADER", "$" + f"{NF_V:,}", C["red"], T["three"] - 0.05, t, "moon")
    redacted_counter(ctx, 90, 920, 900, 200, "BUY & HOLD", money(BH_V), C["green"], 999, t)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["n97"]) else e, prop=prop_coin)


def s_holder(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x3A, 0x2A), (0x05, 0x12, 0x0C))
    god_rays(ctx, W / 2, 700, t, 0.12, C["green"], 16, 1500)
    for k in range(30):
        u = ((t - s0) * 0.8 + k / 30) % 1
        rect(ctx, (k * 173) % W, 300 + u * 1000, 14, 8, [C["green"], C["yellow"], C["white"]][k % 3], 1 - u)
    redacted_counter(ctx, 90, 460, 900, 200, "DAY TRADER", "$" + f"{DF_V:,}", C["red"], 0, t, "sun")
    redacted_counter(ctx, 90, 690, 900, 200, "NIGHT TRADER", "$" + f"{NF_V:,}", C["red"], 0, t, "moon")
    a = ease_io(prog(t, T["seventy"] - 0.35, 0.8))
    p = back(prog(t, s0 + 0.05, 0.35))
    ctx.save(); ctx.translate(540, 1020); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -470, -110, 940, 220, C["dark"], 1, 18, border=C["green"])
    text(ctx, "BUY & HOLD", -430, -55, 34, C["green"], 1, MONO, True, "left")
    if t >= T["seventy"] - 0.35:
        v = money(10000 + (BH_V - 10000) * a)
        text(ctx, v, 0, 75, 120, C["green"], 1, MONO, True, "center", outline=6, ocol=C["ink"])
        tear = ease(prog(t, T["seventy"] - 0.35, 0.4))
        if tear < 1:
            ctx.save(); ctx.translate(tear * 800, 20 - tear * 300); ctx.rotate(tear * 1.1); rect(ctx, -420, -50, 840, 130, (0x05, 0x05, 0x05)); ctx.restore()
    else:
        rect(ctx, -420, -30, 840, 120, (0x05, 0x05, 0x05))
        text(ctx, "$??,???", 0, 55, 80, (0x55, 0x5B, 0x60), 1, MONO, True, "center")
    ctx.restore()
    bunting(ctx, "THE WINNER", t, s0, [C["green"], C["yellow"], C["green"], C["white"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 12 zero fees
def hbar(ctx, y, lab, v, g, col, vmax, fg=None):
    card(ctx, 90, y, 900, 150, C["dark"], 1, 16)
    text(ctx, lab, 120, y + 46, 30, col, 1, MONO, True, "left")
    w_ = (840 * v / vmax) * g
    if w_ > 2:
        card(ctx, 120, y + 70, w_, 56, col, 1, 10, shadow=False)
    if g > 0.05:
        s = money(v * g)
        text(ctx, s, 960, y + 46, 40, C["white"], 1, MONO, True, "right")


def s_zerofee(ctx, t, s0, s1):
    day_bg(ctx, t)
    text(ctx, "WITH ZERO FEES?", W / 2, 440, 76, C["white"], back(prog(t, T["zero2"] - 0.1, 0.3)), HEAD, True, "center", outline=14, ocol=C["ink"])
    vmax = BH_V * 1.02
    hbar(ctx, 500, "DAY TRADER", DG_V, ease_io(prog(t, T["fees"], 0.8)), DAYCOL, vmax)
    hbar(ctx, 680, "NIGHT TRADER", NG_V, ease_io(prog(t, T["night4"], 1.6)), NIGHTCOL, vmax)
    hbar(ctx, 860, "BUY & HOLD", BH_V, 1.0, C["green"], vmax)
    tag(ctx, 640, 1100, "STILL BEHIND", C["red"], back(prog(t, T["f47"] + 0.4, 0.3)), 40, -0.04, C["white"])
    bunting(ctx, "NO FEES AT ALL", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["f47"]) else e)


# ---------------------------------------------------------------- 13 verdict + FOLLOW (no spoken outro)
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3)   # same DAY|NIGHT world as frame 0 (sets up the loop)
    rect(ctx, 0, 0, W, H, (0x05, 0x08, 0x14), 0.6)
    stamp_box(ctx, ["THE MARKET", "PAYS AT NIGHT."], W / 2, 560, T["pays"] - 0.05, t, NIGHTCOL, 820, 92, -0.06)
    stamp_box(ctx, ["ONLY HOLDERS", "COLLECT."], W / 2 + 20, 920, T["holders"] - 0.05, t, C["green"], 820, 92, 0.04)
    fb = back(prog(t, T["only"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2 + 160, 1130); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -290, -50, 580, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #9", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], NIGHTCOL, C["yellow"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "night": s_night, "case": s_case, "rules": s_rules, "start": s_start, "crash08": s_crash08,
            "covid": s_covid, "closed": s_closed, "tiny": s_tiny, "fees": s_fees, "score": s_score, "holder": s_holder,
            "zerofee": s_zerofee, "verdict": s_verdict, "loop": s_loop}
