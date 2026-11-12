# ================================================================ Autopsy #19 scenes ($500 a month -> $100K)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD
PCOL = (0xFF, 0x6B, 0x3D)    # PANIC SELLER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x1C, 0x10, 0x3A), (0x05, 0x03, 0x10)
RBOX = (110, 620, 860, 320)
LCOL = (0xFF, 0xA8, 0x1E)    # money put in
VCOL = (0x22, 0xE5, 0x8B)    # what it is worth
STAMP_OR, STAMP_GR = (0xD0, 0x50, 0x00), (0x0B, 0x8A, 0x4C)


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



def big_title(ctx, s, x, y, size, col, p, maxw=980, rot=0.0, outline=14):
    if p <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    text(ctx, s, 0, 0, fit(ctx, s, size, maxw), col, 1, HEAD, True, "center", outline=outline, ocol=C["ink"])
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["question"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #19", C["cream"], a, 26, -0.03)
    text(ctx, "WORTH:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 805, 78, 34, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, VCOL, a, 8, shadow=False)
        text(ctx, money(FINAL_V), 805, 78, fit(ctx, money(FINAL_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["snowballs"] - SC["question"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])



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









# ---------------------------------------------------------------- race: money put in vs what it's worth (2005 -> 2016, rest classified)
XE = di("2016-12-30")


def race_chart(ctx, t, up, zones=(), curtain=None, a=1.0, goal=False):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    for d0, d1, col, za in zones:
        x0 = sx_of(di(d0), 0, XE, RBOX); x1 = sx_of(di(d1), 0, XE, RBOX)
        rect(ctx, x0, by, max(6, x1 - x0), bh, col, za)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in (2005, 2007, 2009, 2011, 2013, 2015):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, XE, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    up = max(2, up)
    lim = curtain if curtain is not None else up
    hi = min(up, lim) + 1
    vmax = max(30000.0, 1.15 * float(max(np.nanmax(VV[:hi]), np.nanmax(IV[:hi]))))
    if goal:
        vmax = max(vmax, 118000.0)
    vmin = 0.0
    if goal:
        yg = by + bh - (100000 - vmin) / (vmax - vmin) * bh
        for j in range(22):
            rect(ctx, bx + j * 40, yg - 2, 22, 5, GOLD, 0.8)
        text(ctx, "$100K", bx + 10, yg - 12, 26, GOLD, 1, MONO, True, "left")
    if curtain is not None:
        up = min(up, curtain)
    tips = []
    for arr, col in ((IV, LCOL), (VV, VCOL)):
        xs, ys = series_xy(arr, 0, XE, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (ix, iy), (vx, vy) = tips
    off = 0 if abs(iy - vy) > 60 else 60
    under = VV[up] < IV[up]
    mini_rocco(ctx, vx, vy - 4 - (0 if under else off), 4, "tophat", t, "sad" if under else "smug", False, True)
    if curtain is not None:
        xc = sx_of(curtain, 0, XE, RBOX) + 14
        curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("WORTH", VCOL), ("PUT IN", LCOL))):
        rect(ctx, bx + bw - 340, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 300, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")


def coin_rain(ctx, t, n=16, a=1.0, seed=3):
    for k in range(n):
        u = ((t * 0.35) + k / n) % 1
        coin(ctx, (k * 173 + seed * 41) % (W - 80) + 40, -60 + u * 1500, 26, t + k, a)


def evidence(ctx, cx, cy, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -80, 640, 160, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: THE 2ND $100K", -290, -30, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 56, (0x05, 0x05, 0x05), a)
    text(ctx, "TOOK ?? YEARS", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 56, GOLD, 0.7 * a)
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: $500/MO -> $100K WHEN?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x0A, 0x2A, 0x20), (0x02, 0x08, 0x06))
    god_rays(ctx, W / 2, 600, t, 0.08, VCOL, 14, 1400)
    coin_rain(ctx, t, 14, 0.5)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 470); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "$500/MO", 0, 0, fit(ctx, "$500/MO", 230, 900), GOLD, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    arrow_down(ctx, 540, 600 + math.sin(t * 6) * 8, 0.3 * s_, C["white"])
    ctx.save(); ctx.translate(540, 830); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "$100K", 0, 0, fit(ctx, "$100K", 250, 900), VCOL, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 1010); ctx.rotate(-0.02); ctx.scale(s_, s_)
    text(ctx, "WHEN?", 0, 0, 160, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    if show_tag:
        tag(ctx, 540, 200, "INTO THE S&P 500 · SINCE 2005", C["cream"], p, 40, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 when do you hit $100K?
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x2A, 0x4A), (0x03, 0x0A, 0x16))
    speed_lines(ctx, t)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "WHEN DO YOU HIT", W / 2, 440, 120, C["white"], p, 960, -0.03, 14)
    q = back(prog(t, T["thousand2"] - 0.3, 0.3))
    big_title(ctx, "$100,000?", W / 2, 640, 200, VCOL, q, 980, 0.02, 20)
    # finish line flag
    for j in range(8):
        for r in range(2):
            rect(ctx, 220 + j * 80, 820 + r * 40, 40, 40, C["white"] if (j + r) % 2 == 0 else C["ink"], max(q, 0))
            rect(ctx, 260 + j * 80, 820 + r * 40, 40, 40, C["ink"] if (j + r) % 2 == 0 else C["white"], max(q, 0))
    clock(ctx, 540, 1030, 90 * max(p, 1e-3) + 1, t, 5.0)
    bunting(ctx, "THE GOAL", t, s0, [VCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 3 guess
def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(10):
        u = ((t - s0) * 0.4 + k / 10) % 1
        hourglass(ctx, (k * 211 + 80) % W, 1300 - u * 1150, 0.2, t + k)
    hp = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "$100K IN...", W / 2, 420, 110, C["white"], hp, 980, 0, 12)
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "UNDER", "10 YEARS", VCOL, -225, T["A"]),
                                                        ("B", "OVER", "10 YEARS", LCOL, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["ten2"]
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -40, 200, C["ink"], 1, HEAD, True, "center")
        text(ctx, sub1, 0, 75, fit(ctx, sub1, 60, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 140, fit(ctx, sub2, 56, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["ten2"] - 0.1, T["ten2"] + 2.4, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 hidden: the second $100K (race starts)
def s_hidden(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "THE REAL SHOCK...", W / 2, 420, 110, GOLD, p, 980, -0.02, 14)
    q = back(prog(t, T["second1"] - 0.3, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 508); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    rc = ease(prog(t, T["second1"], 0.4))
    if rc > 0:
        up = race_idx(t, [(T["second1"] + 0.2, 2), (SC["rules"] + 5.0, di("2007-10-09"))])
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, up, a=rc); ctx.restore()
    sticker(ctx, t, T["ten2"] - 0.1, T["ten2"] + 2.4, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 5 rules
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("$500 EVERY MONTH", "SAME DAY", VCOL, 290, T["buy"]),
                                                 ("NEVER SELL", "FEES INCLUDED", LCOL, 790, T["never"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        if k == 0:
            coin(ctx, -175, 0, 48, t)
        else:
            xmark(ctx, -175, 0, 34, C["red"], 14)
        text(ctx, title, 45, -12, fit(ctx, title, 52, 330), C["ink"], 1, HEAD, True, "center")
        sub = l1 if (k == 0 or t > T["fees"] - 0.1) else "EVER"
        text(ctx, sub, 45, 62, fit(ctx, sub, 50, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    up = race_idx(t, [(T["second1"] + 0.2, 2), (SC["rules"] + 5.0, di("2007-10-09"))])
    race_chart(ctx, t, up)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 6 2008: put in $25,500, worth $14,440
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-10-09")), (T["worth1"], ILOW), (s1, ILOW + 3)]
    race_chart(ctx, t, race_idx(t, pts), [("2008-01-01", "2009-03-09", C["red"], 0.18)])
    tag(ctx, 540, 440, f"PUT IN: {money(GAP[2])}", LCOL, back(prog(t, T["twentyfive"] - 0.15, 0.3)), 48, -0.03, C["ink"])
    tag(ctx, 540, 530, f"WORTH: {money(GAP[1])}", C["red"], back(prog(t, T["fourteen1"] - 0.15, 0.3)), 48, 0.02, C["white"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 7 most people quit... you keep buying
def s_quit(ctx, t, s0, s1):
    bg_fill(ctx, (0x0B, 0x10, 0x2A), (0x02, 0x03, 0x0A))
    if t > T["keep"] - 0.1:
        coin_rain(ctx, t, 18, 0.8, 7)
    pts = [(s0 + 0.1, ILOW + 3), (T["single"] + 0.6, di("2014-06-30"))]
    race_chart(ctx, t, race_idx(t, pts), [("2009-03-09", "2014-06-30", VCOL, 0.06)])
    if t < T["keep"] - 0.15:
        stamp_box(ctx, ["MOST PEOPLE QUIT HERE"], 540, 470, s0 + 0.05, t, C["red"], 900, 62, -0.04)
    else:
        q = back(prog(t, T["keep"] - 0.15, 0.3))
        big_title(ctx, "YOU KEEP BUYING", W / 2, 470, 110, VCOL, q, 980, 0.02, 14)
        tag(ctx, 540, 545, "CHEAP SHARES, EVERY MONTH", C["cream"], back(prog(t, T["cheap"] - 0.1, 0.3)), 34, -0.02)
    bunting(ctx, "DON'T QUIT", t, s0, [VCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("smug" if t > T["keep"] else "sad") if e != "talk" else e, prop=prop_coin)


# ---------------------------------------------------------------- 8 Aug 2014: $100,000 (A wins)
def s_hit(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x2A, 0x06), (0x10, 0x0A, 0x02))
    god_rays(ctx, W / 2, 700, t, 0.10, GOLD, 16, 1500)
    pts = [(s0 + 0.1, di("2014-06-30")), (T["one3"] + 0.2, I100)]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, curtain=I100 + 25 if t > T["one3"] + 0.3 else None, goal=True)
    tag(ctx, 540, 440, "AUG 2014: $100,000", VCOL, back(prog(t, T["one3"] - 0.1, 0.3)), 50, -0.03, C["ink"])
    tag(ctx, 540, 530, "9 YEARS, 7 MONTHS", C["cream"], back(prog(t, T["Nine"] - 0.1, 0.3)), 44, 0.02)
    if t > T["A2"] - 0.1:
        stamp_box(ctx, ["A WINS"], 830, 1080, T["A2"] - 0.1, t, STAMP_GR, 300, 70, 0.08)
    bunting(ctx, "$100K", t, s0, [GOLD, C["ink"], VCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 9 remember the 2nd $100K -> the snowball bars
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x3A), (0x04, 0x05, 0x14))
    god_rays(ctx, W / 2, 700, t, 0.07, GOLD, 14, 1400)
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "REMEMBER", W / 2, 420, 150, GOLD, r, 960, 0, 16)
    big_title(ctx, "THE 2ND $100K?", W / 2, 560, 100, C["white"], r, 980, 0, 12)
    rows = (("1ST $100K", M1, "9 YRS 7 MO", s0 + 0.3, C["grey"]), ("2ND $100K", M2, "UNDER 5 YEARS", T["five2"] - 0.6, VCOL),
            ("3RD $100K", M3, "UNDER 2 YEARS", T["Under"] - 0.4, GOLD))
    for k, (lab, mo, sub, tt, col) in enumerate(rows):
        g = ease_io(prog(t, tt, 0.7))
        y = 720 + k * 140
        if g <= 0:
            if t > s0 + 0.3:
                text(ctx, lab, 100, y + 14, 36, C["white"], 0.8, MONO, True, "left", outline=5, ocol=C["ink"])
                rect(ctx, 370, y - 30, 300, 60, (0x05, 0x05, 0x05)); text(ctx, "??? YEARS", 520, y + 14, 34, (0x70, 0x76, 0x7B), 1, MONO, True, "center")
            continue
        text(ctx, lab, 100, y + 14, 36, C["white"], 1, MONO, True, "left", outline=5, ocol=C["ink"])
        L = 560 * mo / M1
        card(ctx, 370, y - 42, max(20, L * g), 84, col, 1, 14, border=C["ink"])
        if g > 0.9:
            if L > 300:
                text(ctx, sub, 370 + 20, y + 16, 42, C["ink"], 1, HEAD, True, "left")
            else:
                text(ctx, sub, 370 + L + 18, y + 16, 42, col, 1, HEAD, True, "left", outline=7, ocol=C["ink"])
    # rolling snowball
    sx = 120 + ((t - s0) * 160) % 900; rr = 30 + 10 * prog(t, s0, s1 - s0)
    ctx.new_path(); ctx.arc(sx, 1150 - rr, rr, 0, 2 * math.pi); ctx.set_source_rgba(0.95, 0.97, 1, 0.9); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], C["blue"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["five2"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -42, 900, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=VCOL)
        s_ = f"$100K -> $200K -> $300K: {M1} -> {M2} -> {M3} MONTHS"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 860, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$500/MONTH · JAN 2005 TO DEC 2024", W / 2, 420, 32, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "YOU PUT IN (240 MONTHS)", money(INV_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "IT'S WORTH (DIVIDENDS IN, 0.05% FEES)", money(FINAL_V), VCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["x4"], 880, 700, T["rev2"] + 0.25, t, STAMP_GR, 160, 52, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.4, T["Then2"] - 0.15, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 11 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["THE FIRST $100K", "IS THE HARDEST."], W / 2, 470, T["first"] - 0.05, t, STAMP_OR, 860, 76, -0.05)
    stamp_box(ctx, ["THEN IT SNOWBALLS."], W / 2 + 10, 740, T["Then2"] - 0.05, t, STAMP_GR, 860, 80, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.4, T["Then2"] - 0.15, "right", y=1085)
    fb = back(prog(t, T["snowballs"] + 0.1, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1085); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #20", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "hidden": s_hidden, "rules": s_rules, "crash": s_crash,
            "quit": s_quit, "hit": s_hit, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}
