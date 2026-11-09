# ================================================================ Autopsy #12 scenes (wait for the dip vs buy at records)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD (buys at records)
PCOL = (0xFF, 0x9F, 0x1C)    # WAITER
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




BG0, BG1 = (0x06, 0x22, 0x18), (0x02, 0x08, 0x06)
NAVYA, NAVYB = (0x18, 0x1E, 0x52), (0x05, 0x07, 0x1A)
RBOX = (110, 620, 860, 420)
STAMP_OR, STAMP_GR = (0xD0, 0x50, 0x00), (0x0B, 0x8A, 0x4C)


def trophy(ctx, cx, cy, s, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.sin(t * 2) * 0.06); ctx.scale(s, s)
    col = GOLD
    ctx.new_path(); ctx.move_to(-80, -90); ctx.line_to(80, -90); ctx.curve_to(80, 10, 40, 40, 0, 40); ctx.curve_to(-40, 40, -80, 10, -80, -90)
    ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke()
    for sg in (-1, 1):
        ctx.new_path(); ctx.arc(sg * 88, -45, 30, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(12); ctx.stroke()
    rect(ctx, -14, 40, 28, 40, col, a); card(ctx, -60, 78, 120, 34, (0x8B, 0x5A, 0x2B), a, 6, shadow=False, border=C["ink"])
    rect(ctx, -50, -78, 22, 70, C["white"], 0.45 * a)
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["news"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #12", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["news"]) / (T["never"] - SC["news"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: BUY NOW | WAIT?)
def hook_draw(ctx, t, tl, show_tag=True):
    # left: green "buy now" world, right: navy "wait" world, diagonal split
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, 270, 700, t, 0.08, GRNC, 12, 1100)
    ctx.save(); ctx.new_path(); ctx.move_to(600, 0); ctx.line_to(W, 0); ctx.line_to(W, H); ctx.line_to(480, H); ctx.close_path(); ctx.clip()
    bg_fill(ctx, NAVYA, NAVYB)
    stars(ctx, t, 30, 0, 1400, 4)
    hourglass(ctx, 830, 1060, 0.9, t)
    ctx.restore()
    ctx.new_path(); ctx.move_to(600, 0); ctx.line_to(480, H); ctx.set_source_rgba(*rgba(GOLD)); ctx.set_line_width(10); ctx.stroke()
    for k in range(6):                      # rising green candles on the left
        u = (t * 0.25 + k / 6) % 1
        candle(ctx, 30 + (k * 97) % 420, 1500 - u * 1500, 40, 100, GRNC, 0.22, 22)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(275 + shake, 610); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "BUY", 0, 0, 250, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    text(ctx, "NOW", 0, 250, 250, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    s2 = max(p * sc * (1 + 0.04 * math.sin(t * 5 + 1)), 1e-3)
    ctx.save(); ctx.translate(800, 720); ctx.rotate(0.05); ctx.scale(s2, s2)
    sz = fit(ctx, "WAIT?", 230, 470)
    text(ctx, "WAIT?", 0, 0, sz, GOLD, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    ob = max(p * (1 + 0.08 * math.sin(t * 7)), 1e-3)
    ctx.save(); ctx.translate(545, 455); ctx.scale(ob, ob)
    ctx.new_path(); ctx.arc(0, 0, 70, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["red"])); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(8); ctx.stroke()
    text(ctx, "OR", 0, 26, 74, C["white"], 1, HEAD, True, "center")
    ctx.restore()
    if show_tag:
        tag(ctx, 540, 225, "S&P 500 -5.6%", C["red"], p, 64, -0.04, C["white"])


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 news: S&P -5.6% from its record -> wait for the dip?
_NEWS = [0.0, 0.08, 0.05, 0.16, 0.12, 0.25, 0.22, 0.36, 0.33, 0.48, 0.45, 0.6, 0.57, 0.72, 0.7, 0.86, 0.83, 1.0, 0.9, 0.93, 0.8, 0.84, 0.72]


def s_news(ctx, t, s0, s1):
    rain_bg(ctx, t)
    bx = (140, 520, 800, 430)
    card(ctx, bx[0] - 30, bx[1] - 40, bx[2] + 60, bx[3] + 80, (0x0C, 0x10, 0x1C), 0.9, 18, border=C["grey"])
    g = prog(t, s0, 1.2); n = len(_NEWS)
    up = min(n - 1, 1 + int(g * (n - 1)))
    xs = [bx[0] + i / (n - 1) * bx[2] for i in range(up + 1)]
    ys = [bx[1] + bx[3] - _NEWS[i] * bx[3] for i in range(up + 1)]
    pk = 17
    poly(ctx, xs[:min(len(xs), pk + 1)], ys[:min(len(ys), pk + 1)], GRNC, 9, 1, glow=True)
    if up > pk:
        poly(ctx, xs[pk:], ys[pk:], REDC, 9, 1, glow=True)
        xr = bx[0] + pk / (n - 1) * bx[2]; yr = bx[1]
        for k in range(14):
            rect(ctx, bx[0] + k * 60, yr, 34, 3, GOLD, 0.7)
        trophy(ctx, xr - 10, yr - 70, 0.42, t)
        text(ctx, "RECORD", xr - 130, yr - 22, 30, GOLD, 1, MONO, True, "right", outline=5, ocol=C["ink"])
    q = back(prog(t, T["five"] - 0.08, 0.3))
    if q > 0:
        ctx.save(); ctx.translate(700, 860); ctx.rotate(0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        text(ctx, "-5.6%", 0, 0, 170, REDC, 1, HEAD, True, "center", outline=18, ocol=C["ink"])
        ctx.restore()
    tag(ctx, 540, 420, "S&P 500 · FROM ITS RECORD", C["white"], back(prog(t, T["record1"] - 0.2, 0.3)), 40, -0.03)
    w_ = back(prog(t, T["waiting"] - 0.1, 0.35))
    if w_ > 0:
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, T["smart"] - 0.05, 0.45))
        ctx.save(); ctx.translate(540, 1110); ctx.rotate(-0.03); ctx.scale(max(w_ * hl, 1e-3), max(w_ * hl, 1e-3))
        card(ctx, -440, -80, 880, 130, GOLD, 1, 24, border=C["ink"])
        text(ctx, "WAIT FOR THE DIP?", 0, 22, fit(ctx, "WAIT FOR THE DIP?", 90, 820), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE NEWS", t, s0, [C["red"], C["ink"], C["red"], C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if (e != "talk" and t > T["five"]) else e)


# ---------------------------------------------------------------- 3 guess: A the patient waiter / B buys at records
def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(18):
        u = ((t - s0) * 0.45 + k / 18) % 1
        candle(ctx, (k * 211) % W, 1300 - u * 1150, 30, 70, GRNC if k % 3 else REDC, 0.25 * (1 - u), 16)
    hp = back(prog(t, s0 + 0.03, 0.3))
    ctx.save(); ctx.translate(W / 2, 420); ctx.scale(max(hp, 1e-3), max(hp, 1e-3))
    text(ctx, "WHO ENDS UP RICHER?", 0, 0, fit(ctx, "WHO ENDS UP RICHER?", 92, 980), C["white"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
    ctx.restore()
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "THE PATIENT", "WAITER", PCOL, -225, T["A"]),
                                                        ("B", "BUYS AT", "RECORD HIGHS", HCOL, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["Guess"]
        hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -60, 170, C["ink"], 1, HEAD, True, "center")
        if k == 0:
            hourglass(ctx, 0, 30, 0.42, t)
        else:
            trophy(ctx, 0, 30, 0.5, t)
        text(ctx, sub1, 0, 115, fit(ctx, sub1, 44, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 160, fit(ctx, sub2, 44, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["Guess"] - 0.15, T["Guess"] + 2.3, "guess", y=1080)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 hidden: the answer hides in one long wait
def wait_file(ctx, cx, cy, t, a, opened=False, label="?? MONTHS"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.04)
    card(ctx, -330, -150, 660, 300, (0xC8, 0x9B, 0x5A), a, 18, border=C["ink"])
    card(ctx, -330, -190, 240, 60, (0xC8, 0x9B, 0x5A), a, 12, shadow=False, border=C["ink"])
    text(ctx, "EVIDENCE", -210, -148, 30, C["ink"], a, TAGF, False, "center")
    text(ctx, "ONE LONG WAIT", 0, -60, 70, C["ink"], a, HEAD, True, "center")
    if not opened:
        rect(ctx, -270, 0, 540, 110, (0x05, 0x05, 0x05), a)
        text(ctx, "IN CASH: ?? MONTHS", 0, 72, 44, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    else:
        text(ctx, label, 0, 90, 100, C["red"], a, HEAD, True, "center", outline=10, ocol=C["ink"])
    ctx.restore()


def s_hidden(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    p = back(prog(t, s0 + 0.03, 0.3))
    text(ctx, "THE ANSWER HIDES IN...", W / 2, 440, fit(ctx, "THE ANSWER HIDES IN...", 90, 980) * max(p, 0.01), C["white"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
    q = back(prog(t, T["one1"] - 0.1, 0.4))
    if q > 0:
        ctx.save(); ctx.translate(540, 760); ctx.scale(max(q, 1e-3), max(q, 1e-3)); wait_file(ctx, 0, 0, t, 1); ctx.restore()
    hourglass(ctx, 900, 1030, 0.55 * back(prog(t, T["long1"] - 0.1, 0.4)) + 1e-3, t * 2)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 5 rules: buy after -5%, sell at every new record
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, fg, y, tt) in enumerate((("BUY", "AFTER A 5% DROP", GRNC, C["ink"], 470, T["buy"]),
                                                     ("SELL", "AT EVERY NEW RECORD", REDC, C["white"], 790, T["sell"]))):
        p = back(prog(t, tt - 0.12, 0.4))
        if p <= 0:
            continue
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, (T["drop"] if k == 0 else T["record3"]) - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.025 if k == 0 else 0.025); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
        card(ctx, -460, -130, 920, 260, col, 1, 22, border=C["ink"])
        card(ctx, -430, -100, 200, 200, C["dark"], 1, 16, shadow=False)
        if k == 0:
            arrow_up(ctx, -330, 0, 0.75, GRNC)
        else:
            trophy(ctx, -330, -5, 0.6, t)
        text(ctx, title, 110, -10, 110, fg, 1, HEAD, True, "center", outline=8 if k else 0, ocol=C["ink"])
        text(ctx, l1, 110, 80, fit(ctx, l1, 54, 600), fg, 1, HEAD, True, "center", outline=5 if k else 0, ocol=C["ink"])
        ctx.restore()
    # start line: both racers ready
    r = back(prog(t, T["record3"] - 0.1, 0.35))
    if r > 0:
        rect(ctx, 120, 1060, 840, 8, C["white"], 0.8 * r)
        for j in range(12):
            rect(ctx, 120 + j * 70, 1068, 35, 14, C["ink"] if j % 2 else C["white"], r)
        mini_rocco(ctx, 330, 1058, 6, "race", t, "smug", False, True)
        mini_rocco(ctx, 560, 1058, 6, "tophat", t, "neutral", False, True)
        tag(ctx, 540, 990, "$10,000 EACH · 2005-2024", GOLD, r, 32, 0.02)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if (e != "talk" and t > T["record3"]) else e)


# ---------------------------------------------------------------- race chart
def race_chart(ctx, t, up, zones=(), cut=None, curtain=0.0):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), 0, N - 1, RBOX); x1 = sx_of(di(d1), 0, N - 1, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    # record-high days: little gold ticks at the top as the race passes them
    for ri in NEWREC_I:
        if ri > up:
            break
        xx = sx_of(ri, 0, N - 1, RBOX)
        rect(ctx, xx - 1, RBOX[1] + 4, 3, 16, GOLD, 0.8)
    # waiter in/out strip
    for i in range(0, up, 6):
        xx = sx_of(i, 0, N - 1, RBOX)
        rect(ctx, xx, RBOX[1] + RBOX[3] + 6, max(2, RBOX[2] / N * 6 + 1), 10, PCOL if INM[i] else (0x55, 0x5B, 0x60), 0.9)
    vmax = max(15000.0, 1.2 * float(max(np.nanmax(SV[:up + 1]), np.nanmax(JV[:up + 1]))))
    vmin = 6000.0
    tips = []
    for arr, col in ((SV, HCOL), (JV, PCOL)):
        xs, ys = series_xy(arr, 0, N - 1, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (px_, py_) = tips
    lead_w = JV[up] > SV[up]
    off = 0 if abs(hy - py_) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_w else 0), 4, "tophat", t, "sad" if lead_w else "smug", False, True)
    mini_rocco(ctx, px_, py_ - 4 - (0 if lead_w else off), 4, "race", t, "smug" if lead_w else "sad", False, True)
    if cut is not None and curtain > 0:
        xc = sx_of(di(cut), 0, N - 1, RBOX)
        curtain_box(ctx, t, xc, RBOX[1] - 30, RBOX[0] + RBOX[2] + 30, (RBOX[3] + 60) * ease(curtain))
    for k, (lab, col) in enumerate((("WAITER", PCOL), ("BUY & HOLD", HCOL))):
        rect(ctx, RBOX[0] + 200 + k * 300, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 246 + k * 300, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")


def s_race07(ctx, t, s0, s1):
    late = t >= T["Two2"] - 0.1
    if late:
        rain_bg(ctx, t)
    else:
        stadium(ctx, t)
    pts = [(s0 + 0.15, 1), (T["sells"], di("2007-06-01")), (T["cheaper"] + 0.2, di("2007-12-31")),
           (T["Two2"], di("2007-12-31")), (T["both"] + 0.3, di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), [("2007-10-10", "2009-03-09", C["red"], 0.2)] if late else [])
    if not late:
        tag(ctx, 540, 440, "2007: SELLS THE TOP", PCOL, back(prog(t, T["sells"] - 0.1, 0.3)), 38, -0.03)
        tag(ctx, 540, 524, "BUYS BACK CHEAPER · LEADS", GRNC, back(prog(t, T["cheaper"] - 0.1, 0.3)), 34, 0.02)
    else:
        tag(ctx, 540, 440, "2008", C["red"], back(prog(t, T["Two2"] - 0.05, 0.3)), 40, -0.03, C["white"])
        tag(ctx, 540, 524, "CRUSHES THEM BOTH", C["red"], back(prog(t, T["crushes"] - 0.05, 0.3)), 38, 0.02, C["white"])
    bunting(ctx, "2008" if late else "THE RACE", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("shock" if t > T["crushes"] else "smug") if e != "talk" else e, prop=prop_flag)


def s_race13(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x2A, 0x3A), (0x04, 0x0A, 0x12))
    god_rays(ctx, W / 2, 300, t, 0.05, GOLD, 12, 1300)
    pts = [(s0 + 0.1, di("2009-03-09")), (T["everywhere"] + 0.3, di("2013-12-31")), (T["catches"] + 0.3, di("2014-12-31")),
           (T["leads2"] + 0.3, di("2015-12-31")), (T["winner"], di("2016-07-12"))]
    race_chart(ctx, t, race_idx(t, pts), [("2013-01-01", "2013-12-31", GOLD, 0.10)])
    if t < T["Tw15"] - 0.1:
        tag(ctx, 540, 440, "2013: RECORDS EVERYWHERE", GOLD, back(prog(t, T["Tw13"] - 0.05, 0.3)), 36, -0.03)
        tag(ctx, 540, 524, "BUY & HOLD CATCHES UP", HCOL, back(prog(t, T["Buy2"] - 0.1, 0.3)), 36, 0.02)
    elif t < T["Seventeen"] - 0.1:
        tag(ctx, 540, 440, "2015", C["cream"], back(prog(t, T["Tw15"] - 0.05, 0.3)), 40, -0.03)
        tag(ctx, 540, 524, "WAITER LEADS AGAIN", PCOL, back(prog(t, T["leads2"] - 0.1, 0.3)), 38, 0.02)
    else:
        tag(ctx, 540, 440, f"{NTR} TRADES", PCOL, back(prog(t, T["Seventeen"] - 0.08, 0.3)), 44, -0.03)
        tag(ctx, 540, 524, f"{NTR} WINNERS", GRNC, back(prog(t, T["winner"] - 0.12, 0.3)), 44, 0.03)
        if t > T["winner"]:
            stamp_box(ctx, ["100% WINNERS"], 640, 760, T["winner"] + 0.05, t, STAMP_GR, 520, 70, -0.06)
    bunting(ctx, "2013-2016", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 7 drought: the dip stopped coming (zoom 2016-07 -> 2018-02)
_d0, _d1 = di("2016-07-01"), di("2018-02-28")
D_P = PX[_d0:_d1 + 1] / PX[_d0]; D_N = len(D_P)
D_REC = [i - _d0 for i in NEWREC_I if _d0 <= i <= _d1]
_s, _b = di(SELLS[6]), di(BUYS[7])
DBOX = (110, 600, 860, 440)


def s_drought(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x34), (0x03, 0x04, 0x10))
    stars(ctx, t, 40, 0, 1300, 9)
    moon(ctx, 900, 330, 50)
    card(ctx, DBOX[0] - 30, DBOX[1] - 30, DBOX[2] + 60, DBOX[3] + 120, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    vmin, vmax = 0.92, float(D_P.max()) + 0.05
    up = max(1, int((D_N - 1) * ease_io(prog(t, s0 + 0.1, T["Remember"] - s0 - 0.2))))
    xs, ys = series_xy(D_P, 0, D_N - 1, up, DBOX, vmin, vmax, 1)
    poly(ctx, xs, ys, HCOL, 8, 1, glow=True)
    for ri in D_REC:
        if ri > up:
            break
        xx = sx_of(ri, 0, D_N - 1, DBOX)
        rect(ctx, xx - 1, DBOX[1] + 4, 3, 18, GOLD, 0.85)
    xs_ = sx_of(_s - _d0, 0, D_N - 1, DBOX); xb_ = sx_of(min(up, _b - _d0), 0, D_N - 1, DBOX)
    yflat = sy_of(1.0, vmin, vmax, DBOX)
    rect(ctx, xs_, yflat - 4, max(4, xb_ - xs_), 8, PCOL)
    text(ctx, "WAITER: IN CASH", xs_ + 10, yflat + 44, 28, PCOL, 1, MONO, True, "left", outline=5, ocol=C["ink"])
    text(ctx, "GOLD = NEW RECORD", DBOX[0] + DBOX[2], DBOX[1] + DBOX[3] + 60, 24, GOLD, 0.9, MONO, True, "right")
    for m, lab in ((0, "JUL '16"), (_b - _d0, "FEB '18")):
        text(ctx, lab, sx_of(m, 0, D_N - 1, DBOX), DBOX[1] + DBOX[3] + 60, 24, C["white"], 0.8, MONO, True, "center")
    if t < T["Remember"] - 0.1:
        tag(ctx, 540, 450, "THE DIP STOPPED COMING", C["red"], back(prog(t, T["stopped"] - 0.1, 0.3)), 40, -0.03, C["white"])
    else:
        r = back(prog(t, T["Remember"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 450); ctx.rotate(-0.03); ctx.scale(max(r, 1e-3), max(r, 1e-3))
        text(ctx, "REMEMBER THAT WAIT?", 0, 20, fit(ctx, "REMEMBER THAT WAIT?", 96, 980), GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "2016-2018", t, s0, [C["blue"], C["ink"], PCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("sleep" if t < T["Remember"] else "shock") if e != "talk" else e)


# ---------------------------------------------------------------- 8 the wait: 19 months in cash, bought back 21% higher


def s_wait(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0C, 0x14), (0x08, 0x02, 0x04))
    skyline(ctx, 1300, t, 5, (0x16, 0x10, 0x1E))
    for i in range(0, W, 80):
        rect(ctx, (i + t * 50) % (W + 80) - 80, 0, 2, H, C["red"], 0.08)
    # calendar flipping months
    m = int(clamp(prog(t, T["Nineteen"] - 0.1, 0.55)) * MONTHS_CASH)
    p = back(prog(t, s0 + 0.03, 0.35))
    ctx.save(); ctx.translate(540, 620); ctx.rotate(-0.04 + 0.02 * math.sin(t * 3)); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -260, -230, 520, 440, C["white"], 1, 26, border=C["ink"])
    rect(ctx, -260, -230, 520, 110, C["red"])
    for k in (-150, 150):
        rect(ctx, k - 12, -260, 24, 70, C["ink"])
    text(ctx, "MONTHS IN CASH", 0, -150, 50, C["white"], 1, HEAD, True, "center")
    text(ctx, str(max(1, m)), 0, 150, 260, C["ink"], 1, HEAD, True, "center")
    ctx.restore()
    q = back(prog(t, T["prices"] - 0.1, 0.35))
    if q > 0:
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, T["higher"] - 0.05, 0.45))
        ctx.save(); ctx.translate(540, 1000); ctx.rotate(0.03); ctx.scale(max(q * hl, 1e-3), max(q * hl, 1e-3))
        card(ctx, -440, -80, 880, 150, C["dark"], 1, 22, border=REDC)
        text(ctx, f"BOUGHT BACK +{REBUY_PCT}% HIGHER", 0, 24, fit(ctx, f"BOUGHT BACK +{REBUY_PCT}% HIGHER", 70, 820), REDC, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "THE LONG WAIT", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


# ---------------------------------------------------------------- 9 final score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 420, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 460, 900, 220, "A · THE PATIENT WAITER", money(WV), PCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 710, 900, 220, "B · BUYS AT RECORDS (HOLDS)", money(BH_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 735, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    sticker(ctx, t, T["rev2"] + 0.35, T["follow"], "right", y=1060)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 10 verdict + FOLLOW (no spoken outro)
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x06, 0x08), 0.8)
    stamp_box(ctx, ["PERFECT TRADES.", "STILL LOST."], W / 2, 520, T["Perfect"] - 0.05, t, STAMP_OR, 820, 84, -0.05)
    stamp_box(ctx, ["THE DIP MAY", "NEVER COME."], W / 2 + 10, 860, T["dip4"] - 0.05, t, STAMP_GR, 760, 84, 0.04)
    sticker(ctx, t, T["rev2"] + 0.35, T["never"] + 0.1, "right", y=1060)
    fb = back(prog(t, T["never"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1075); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #13", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "news": s_news, "guess": s_guess, "hidden": s_hidden, "rules": s_rules, "race07": s_race07,
            "race13": s_race13, "drought": s_drought, "wait": s_wait, "score": s_score, "verdict": s_verdict, "loop": s_loop}
