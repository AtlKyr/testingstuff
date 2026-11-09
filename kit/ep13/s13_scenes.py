# ================================================================ Autopsy #13 scenes (the Monday effect)
HCOL = (0x4F, 0xC3, 0xF7)    # HOLDER
PCOL = (0xFF, 0x9F, 0x1C)    # MONDAY SKIPPER
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


BG0, BG1 = (0x3A, 0x12, 0x4A), (0x0C, 0x04, 0x14)
RBOX = (110, 660, 860, 380)
STAMP_OR, STAMP_GR = (0xD0, 0x50, 0x00), (0x0B, 0x8A, 0x4C)
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]


def week_strip(ctx, cx, cy, s, t, xmon=1.0, a=1.0, glow_mon=False):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for k, d in enumerate(DAYS):
        x = -400 + k * 200
        bob = math.sin(t * 4 + k) * 6
        col = REDC if k == 0 else C["cream"]
        card(ctx, x - 85, -95 + bob, 170, 190, col, a, 18, border=C["ink"])
        rect(ctx, x - 85, -95 + bob, 170, 46, C["ink"], 0.85 * a)
        text(ctx, d, x, -60 + bob, 34, C["white"], a, TAGF, False, "center")
        if k == 0 and xmon > 0:
            xmark(ctx, x, 30 + bob, 50 * xmon, C["white"], 16)
        elif k > 0:
            check(ctx, x - 35, 30 + bob, 34, GRNC, a, 10)
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["monday"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #13", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["monday"]) / (T["Skipping2"] - SC["monday"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: SKIP MONDAYS?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 620, t, 0.08, PCOL, 14, 1400)
    for k in range(10):                      # drifting calendar pages
        u = (t * 0.22 + k / 10) % 1
        x = (k * 173 + 40) % (W - 80)
        ctx.save(); ctx.translate(x, 1500 - u * 1700); ctx.rotate(math.sin(t + k) * 0.4)
        card(ctx, -40, -46, 80, 92, C["cream"], 0.18, 8, shadow=False)
        ctx.restore()
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 500); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "SKIP", 0, 0, 260, C["white"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 745); ctx.rotate(0.03); ctx.scale(s_, s_)
    sz = fit(ctx, "MONDAYS?", 250, 1000)
    text(ctx, "MONDAYS?", 0, 0, sz, PCOL, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    week_strip(ctx, 540, 985, 0.85 * max(p, 1e-3), t)
    if show_tag:
        tag(ctx, 540, 180, "20 YEARS OF SPY", C["cream"], p, 52, -0.04)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 monday: "the worst day for stocks?"
def coffee(ctx, cx, cy, s, t):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for k in range(3):
        ph = t * 2 + k * 1.3
        ctx.new_path(); ctx.move_to(-30 + k * 30, -110)
        ctx.curve_to(-50 + k * 30 + math.sin(ph) * 20, -160, -10 + k * 30 + math.sin(ph) * 20, -190, -30 + k * 30, -240)
        ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(8); ctx.stroke()
    card(ctx, -90, -100, 180, 200, C["cream"], 1, 22, border=C["ink"])
    ctx.new_path(); ctx.arc(110, 0, 45, -1.3, 1.3); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(14); ctx.stroke()
    text(ctx, "MON", 0, 25, 56, REDC, 1, HEAD, True, "center")
    ctx.restore()


def s_monday(ctx, t, s0, s1):
    rain_bg(ctx, t)
    p = back(prog(t, s0 + 0.03, 0.3))
    ctx.save(); ctx.translate(W / 2, 470); ctx.rotate(-0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    text(ctx, "IT'S MONDAY", 0, 0, 150, C["white"], 1, HEAD, True, "center", outline=16, ocol=C["ink"])
    ctx.restore()
    q = back(prog(t, T["worst1"] - 0.1, 0.3))
    if q > 0:
        ctx.save(); ctx.translate(W / 2, 640); ctx.rotate(0.03); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -440, -70, 880, 120, REDC, 1, 22, border=C["ink"])
        text(ctx, "\"WORST DAY FOR STOCKS\"", 0, 22, fit(ctx, "\"WORST DAY FOR STOCKS\"", 70, 820), C["white"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        ctx.restore()
    coffee(ctx, 300, 930, 0.9 * back(prog(t, s0 + 0.2, 0.4)) + 1e-3, t)
    r = back(prog(t, T["skipped"] - 0.1, 0.35))
    if r > 0:
        ctx.save(); ctx.translate(760, 930); ctx.rotate(-0.08); ctx.scale(max(r, 1e-3), max(r, 1e-3))
        card(ctx, -180, -90, 360, 180, GOLD, 1, 20, border=C["ink"])
        text(ctx, "SKIP IT?", 0, 30, 90, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "MONDAY", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if (e != "talk" and t < T["worst1"]) else e)


# ---------------------------------------------------------------- 3 guess
def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(18):
        u = ((t - s0) * 0.45 + k / 18) % 1
        candle(ctx, (k * 211) % W, 1300 - u * 1150, 30, 70, GRNC if k % 3 else REDC, 0.25 * (1 - u), 16)
    hp = back(prog(t, s0 + 0.03, 0.3))
    ctx.save(); ctx.translate(W / 2, 420); ctx.scale(max(hp, 1e-3), max(hp, 1e-3))
    text(ctx, "SKIP EVERY MONDAY AND...", 0, 0, fit(ctx, "SKIP EVERY MONDAY AND...", 84, 980), C["white"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
    ctx.restore()
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "YOU BEAT", "THE MARKET", GRNC, -225, T["A"]),
                                                        ("B", "YOU FALL", "BEHIND", REDC, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["Guess"]
        hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -40, 200, C["ink"], 1, HEAD, True, "center")
        if k == 0:
            arrow_up(ctx, 0, 30, 0.35, C["white"])
        else:
            arrow_down(ctx, 0, 30, 0.35, C["white"])
        text(ctx, sub1, 0, 115, fit(ctx, sub1, 50, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 160, fit(ctx, sub2, 44, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["Guess"] - 0.15, T["Guess"] + 2.3, "guess", y=1080)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 hidden: the answer hides in one Monday
def day_file(ctx, cx, cy, t, a, opened=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.04)
    card(ctx, -330, -150, 660, 300, (0xC8, 0x9B, 0x5A), a, 18, border=C["ink"])
    card(ctx, -330, -190, 240, 60, (0xC8, 0x9B, 0x5A), a, 12, shadow=False, border=C["ink"])
    text(ctx, "EVIDENCE", -210, -148, 30, C["ink"], a, TAGF, False, "center")
    text(ctx, "ONE MONDAY", 0, -60, 76, C["ink"], a, HEAD, True, "center")
    rect(ctx, -270, 0, 540, 110, (0x05, 0x05, 0x05), a)
    text(ctx, "DATE: ??/??/????", 0, 72, 44, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    ctx.restore()


def s_hidden(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    p = back(prog(t, s0 + 0.03, 0.3))
    text(ctx, "THE ANSWER HIDES IN...", W / 2, 440, fit(ctx, "THE ANSWER HIDES IN...", 90, 980) * max(p, 0.01), C["white"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
    q = back(prog(t, T["one1"] - 0.15, 0.4))
    if q > 0:
        ctx.save(); ctx.translate(540, 760); ctx.scale(max(q, 1e-3), max(q, 1e-3)); day_file(ctx, 0, 0, t, 1); ctx.restore()
    qs = 1 + 0.1 * math.sin(t * 7)
    ctx.save(); ctx.translate(900, 1040); ctx.scale(qs, qs)
    text(ctx, "?", 0, 0, 160 * back(prog(t, T["Monday3"] - 0.1, 0.4)) + 1, GOLD, 1, HEAD, True, "center", outline=12, ocol=C["ink"]); ctx.restore()
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- race chart
def race_chart(ctx, t, up, zones=(), ticks=False):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), 0, N - 1, RBOX); x1 = sx_of(di(d1), 0, N - 1, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    vmax = max(14000.0, 1.2 * float(max(np.nanmax(SV[:up + 1]), np.nanmax(JV[:up + 1]))))
    vmin = 6000.0
    tips = []
    for arr, col in ((SV, HCOL), (JV, PCOL)):
        xs, ys = series_xy(arr, 0, N - 1, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (px_, py_) = tips
    lead_s = JV[up] > SV[up]
    off = 0 if abs(hy - py_) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_s else 0), 4, "tophat", t, "sad" if lead_s else "smug", False, True)
    mini_rocco(ctx, px_, py_ - 4 - (0 if lead_s else off), 4, "race", t, "smug" if lead_s else "sad", False, True)
    for k, (lab, col) in enumerate((("MONDAY SKIPPER", PCOL), ("HOLDER", HCOL))):
        rect(ctx, RBOX[0] + 150 + k * 360, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 196 + k * 360, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")


# ---------------------------------------------------------------- 5 rules (+ the race starts underneath)
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, fg, x, tt) in enumerate((("SELL", "FRIDAY CLOSE", REDC, C["white"], 290, T["sell"]),
                                                     ("BUY BACK", "MONDAY CLOSE", GRNC, C["ink"], 790, T["buy"]))):
        p = back(prog(t, tt - 0.12, 0.4))
        if p <= 0:
            continue
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, (T["Fridays"] if k == 0 else T["Mondays_"]) - 0.05, 0.4))
        ctx.save(); ctx.translate(x, 470); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
        card(ctx, -230, -110, 460, 220, col, 1, 22, border=C["ink"])
        if k == 0:
            arrow_down(ctx, -160, 0, 0.42, C["white"])
        else:
            arrow_up(ctx, -160, 0, 0.42, C["white"])
        text(ctx, title, 40, -10, fit(ctx, title, 84, 300), fg, 1, HEAD, True, "center", outline=6 if k == 0 else 0, ocol=C["ink"])
        text(ctx, l1, 40, 60, fit(ctx, l1, 40, 300), fg, 1, HEAD, True, "center", outline=4 if k == 0 else 0, ocol=C["ink"])
        ctx.restore()
    rc = ease(prog(t, s0 + 0.1, 0.4))
    if rc > 0:
        up = race_idx(t, [(s0 + 0.3, 1), (s1, di("2007-06-29"))])
        ctx.save(); ctx.translate(0, (1 - rc) * 200)
        race_chart(ctx, t, up)
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_race08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-06-29")), (T["ten"], di("2008-10-10")), (T["trails"] + 0.3, di("2008-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), [("2008-01-01", "2008-12-31", C["red"], 0.22)])
    tag(ctx, 540, 440, f"2008: MONDAYS {MON_08:.1f}%", C["red"], back(prog(t, T["Mondays"] - 0.1, 0.3)), 40, -0.03, C["white"])
    if t < T["still1"] - 0.1:
        tag(ctx, 540, 524, "THE SKIPPER DODGES IT", PCOL, back(prog(t, T["dodges"] - 0.1, 0.3)), 36, 0.02)
    else:
        tag(ctx, 540, 524, "...AND STILL TRAILS", HCOL, back(prog(t, T["still1"] - 0.1, 0.3)), 38, 0.02)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("shock" if t > T["trails"] else "smug") if e != "talk" else e, prop=prop_flag)


def s_race20(ctx, t, s0, s1):
    late = t >= T["Tw22"] - 0.1
    if late:
        stadium(ctx, t)
    else:
        bg_fill(ctx, (0x2A, 0x10, 0x3A), (0x0A, 0x04, 0x12)); stars(ctx, t, 40, 0, 1300, 7)
    pts = [(s0 + 0.1, di("2008-12-31")), (T["Monday4"], di("2020-03-16")), (T["behind2"] + 0.2, di("2020-12-31")),
           (T["Tw22"], di("2020-12-31")), (T["story"] + 0.3, di("2022-12-30"))]
    race_chart(ctx, t, race_idx(t, pts), [("2020-02-19", "2020-03-23", C["purple"], 0.35), ("2022-01-03", "2022-12-30", C["red"], 0.15 if late else 0)])
    if not late:
        tag(ctx, 540, 440, f"2020: WORST DAY {WORST_PCT:.1f}%", C["purple"], back(prog(t, T["worst2"] - 0.1, 0.3)), 38, -0.03, C["white"])
        if t < T["Dodged"] - 0.1:
            tag(ctx, 540, 524, "...IT WAS A MONDAY", GOLD, back(prog(t, T["Monday4"] - 0.15, 0.3)), 38, 0.02)
        else:
            tag(ctx, 540, 524, "DODGED. STILL BEHIND.", PCOL, back(prog(t, T["Dodged"] - 0.1, 0.3)), 38, 0.02)
    else:
        tag(ctx, 540, 440, "2022", C["cream"], back(prog(t, T["Tw22"] - 0.05, 0.3)), 40, -0.03)
        tag(ctx, 540, 524, "SAME STORY", HCOL, back(prog(t, T["same"] - 0.1, 0.3)), 40, 0.02)
    bunting(ctx, "2022" if late else "2020", t, s0, [C["purple"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire" if not late else "crown", lambda e: ("shock" if t < T["Tw22"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 7 remember: Oct 13, 2008, +14.5%
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x0C, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    god_rays(ctx, W / 2, 700, t, 0.08, GRNC, 14, 1400)
    if t < T["October"] - 0.1:
        r = back(prog(t, s0 + 0.03, 0.35))
        ctx.save(); ctx.translate(540, 560); ctx.scale(max(r, 1e-3), max(r, 1e-3))
        text(ctx, "REMEMBER", 0, 0, 170, GOLD, 1, HEAD, True, "center", outline=16, ocol=C["ink"])
        text(ctx, "THAT ONE MONDAY?", 0, 150, fit(ctx, "THAT ONE MONDAY?", 110, 980), C["white"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
        ctx.restore()
        ctx.save(); ctx.translate(540, 980); ctx.scale(0.8, 0.8); day_file(ctx, 0, 0, t, 1); ctx.restore()
    else:
        p = back(prog(t, T["October"] - 0.1, 0.35))
        ctx.save(); ctx.translate(310, 600); ctx.rotate(-0.05 + 0.02 * math.sin(t * 3)); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -200, -190, 400, 380, C["white"], 1, 26, border=C["ink"])
        rect(ctx, -200, -190, 400, 100, C["red"])
        text(ctx, "OCT 2008", 0, -120, 54, C["white"], 1, HEAD, True, "center")
        text(ctx, str(BEST_DATE.day), 0, 120, 210, C["ink"], 1, HEAD, True, "center")
        text(ctx, "MONDAY", 0, 165, 34, REDC, 1, TAGF, False, "center")
        ctx.restore()
        q = back(prog(t, T["fourteen"] - 0.1, 0.35))
        if q > 0:
            ctx.save(); ctx.translate(780, 640); ctx.rotate(0.05); ctx.scale(max(q, 1e-3), max(q, 1e-3))
            text(ctx, f"+{BEST_PCT}%", 0, 0, fit(ctx, f"+{BEST_PCT}%", 170, 520), GRNC, 1, HEAD, True, "center", outline=16, ocol=C["ink"])
            ctx.restore()
        tag(ctx, 540, 900, "BEST DAY IN 20 YEARS", GOLD, back(prog(t, T["best"] - 0.1, 0.3)), 44, -0.02)
        if t > T["missed"] - 0.1:
            stamp_box(ctx, ["SKIPPER: MISSED IT"], 560, 1080, T["missed"] - 0.05, t, C["red"], 700, 64, 0.04)
    bunting(ctx, "THE CLUE", t, s0, [C["green"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("shock" if t > T["fourteen"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 8 final score
def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 420, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · MONDAY SKIPPER (0.05% FEES)", money(SKV), PCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · JUST HOLDING", money(BH_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 952); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -42, 900, 84, (0x05, 0x05, 0x05), 0.9, 14, shadow=False, border=PCOL)
        s_ = f"SKIPPER WITH ZERO FEES: {money(SK0)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 860, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()
    sticker(ctx, t, T["rev2"] + 0.35, T["Skipping2"] + 0.1, "right", y=1080)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 9 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x06, 0x04, 0x0A), 0.8)
    stamp_box(ctx, ["MONDAY WAS NEVER", "THE PROBLEM."], W / 2, 520, T["never"] - 0.1, t, STAMP_OR, 860, 80, -0.05)
    stamp_box(ctx, ["SKIPPING IT WAS."], W / 2 + 10, 820, T["Skipping2"] - 0.05, t, STAMP_GR, 760, 92, 0.04)
    sticker(ctx, t, T["rev2"] + 0.35, T["Skipping2"] + 0.1, "right", y=1080)
    fb = back(prog(t, T["Skipping2"] + 0.15, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1060); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #14", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "monday": s_monday, "guess": s_guess, "hidden": s_hidden, "rules": s_rules, "race08": s_race08,
            "race20": s_race20, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}
