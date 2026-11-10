# ================================================================ Autopsy #14 scenes (chase the big green day?)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD
PCOL = (0xFF, 0x9F, 0x1C)    # BOUNCE CHASER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x06, 0x3A, 0x2A), (0x02, 0x0C, 0x09)
RBOX = (110, 660, 860, 380)
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
    a = ease(prog(t, SC["bestday"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #14", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["bestday"]) / (T["symptom"] - SC["bestday"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: +2.35% / CHASE IT?)
CND = [(-70, 150, REDC), (-10, 190, REDC), (60, 120, GRNC), (40, 200, REDC), (130, 170, REDC)]


def candle_row(ctx, cx, cy, s, t, grow=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    x = -420
    for k, (top, h, col) in enumerate(CND):
        bob = math.sin(t * 3 + k) * 5
        candle(ctx, x, top - 80 + bob, 74, h * 0.62, col, 1, 26)
        x += 112
    gh = 280 * grow
    pulse = 1 + 0.05 * math.sin(t * 8)
    g = cairo.RadialGradient(x + 85, 60, 20, x + 85, 60, 320)
    g.add_color_stop_rgba(0, 0.13, 0.9, 0.55, 0.45); g.add_color_stop_rgba(1, 0.13, 0.9, 0.55, 0)
    ctx.set_source(g); ctx.new_path(); ctx.arc(x + 85, 60, 320, 0, 2 * math.pi); ctx.fill()
    candle(ctx, x + 20, 130 - gh * pulse, 130, gh * pulse, GRNC, 1, 34)
    arrow_up(ctx, x + 85, 130 - gh * pulse - 90 + math.sin(t * 9) * 8, 0.4, GOLD)
    ctx.restore()


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 620, t, 0.09, GRNC, 14, 1400)
    for k in range(12):                      # rising arrows
        u = (t * 0.25 + k / 12) % 1
        arrow_up(ctx, (k * 197 + 60) % (W - 60), 1500 - u * 1700, 0.3 + 0.12 * (k % 3), GRNC, 0.16)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 520); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, NEWS_PCT, 0, 0, fit(ctx, NEWS_PCT, 300, 940), GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "CHASE IT?", 0, 0, fit(ctx, "CHASE IT?", 230, 960), C["white"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    candle_row(ctx, 560, 1045, 0.88 * max(p, 1e-3), t)
    if show_tag:
        tag(ctx, 540, 180, "S&P 500 · BEST DAY SINCE APRIL", C["cream"], p, 46, -0.04)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 best day since April
def s_bestday(ctx, t, s0, s1):
    bg_fill(ctx, (0x0B, 0x5C, 0x3C), (0x03, 0x1A, 0x10))
    god_rays(ctx, W / 2, 640, t, 0.14, GOLD, 16, 1500)
    for k in range(14):                       # confetti
        u = ((t - s0) * 0.5 + k / 14) % 1
        rect(ctx, (k * 157 + 30) % W, 200 + u * 1000, 16, 26, [GOLD, GRNC, C["white"], HCOL][k % 4], 0.7 * (1 - u))
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "BEST DAY", W / 2, 540, 190, GOLD, p, 960, -0.03, 18)
    q = back(prog(t, T["April"] - 0.3, 0.3))
    big_title(ctx, "SINCE APRIL", W / 2, 700, 140, C["white"], q, 960, 0.02, 14)
    r = back(prog(t, s0 + 0.15, 0.4))
    if r > 0:
        ctx.save(); ctx.translate(310, 960); ctx.rotate(-0.05 + 0.02 * math.sin(t * 3)); ctx.scale(max(r, 1e-3), max(r, 1e-3))
        card(ctx, -210, -150, 420, 300, C["white"], 1, 26, border=C["ink"])
        rect(ctx, -210, -150, 420, 86, C["red"])
        text(ctx, "S&P 500 · NOV 9", 0, -92, 40, C["white"], 1, HEAD, True, "center")
        text(ctx, NEWS_PCT, 0, 80, fit(ctx, NEWS_PCT, 130, 380), STAMP_GR, 1, HEAD, True, "center")
        ctx.restore()
    star(ctx, 790, 960, 120 * back(prog(t, T["best"] - 0.1, 0.4)) + 1, GOLD, 1, t * 1.5)
    text(ctx, "#1", 790, 985, 70 * back(prog(t, T["best"], 0.3)) + 1, C["ink"], 1, HEAD, True, "center")
    bunting(ctx, "THE NEWS", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 3 chase the bounce?
def s_chase(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x1E, 0x06), (0x12, 0x08, 0x02))
    speed_lines(ctx, t)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "SHOULD YOU", W / 2, 440, 84, C["white"], p, 900, -0.02, 12)
    q = back(prog(t, T["chase"] - 0.12, 0.3))
    big_title(ctx, "CHASE", W / 2, 690, 240, PCOL, q, 960, -0.03, 22)
    r = back(prog(t, T["bounce1"] - 0.25, 0.3))
    big_title(ctx, "THE BOUNCE?", W / 2, 870, 160, GOLD, r, 980, 0.02, 16)
    # bouncing ball + dotted path
    u = (t - s0)
    for k in range(14):
        uu = u - k * 0.05
        bx = 80 + (uu * 420) % 920; by = 1095 - abs(math.sin(uu * 5.2)) * 150
        ctx.new_path(); ctx.arc(bx, by, 30 if k == 0 else 9, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba(GRNC, 1 if k == 0 else 0.5 - k * 0.03)); ctx.fill()
        if k == 0:
            ctx.new_path(); ctx.arc(bx, by, 30, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(7); ctx.stroke()
    rect(ctx, 60, 1122, 960, 8, C["white"], 0.5)
    bunting(ctx, "THE QUESTION", t, s0, [PCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 4 guess
def hold_icon(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for dx in (-34, 34):
        card(ctx, dx - 22, -80, 44, 160, col, 1, 10, shadow=False, border=C["ink"])
    ctx.restore()


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(18):
        u = ((t - s0) * 0.45 + k / 18) % 1
        candle(ctx, (k * 211) % W, 1300 - u * 1150, 30, 70, GRNC if k % 3 else REDC, 0.25 * (1 - u), 16)
    hp = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "BUY AFTER EVERY BIG JUMP...", W / 2, 420, 84, C["white"], hp, 980, 0, 12)
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "THE CHASER", "WINS", PCOL, -225, T["A"]),
                                                        ("B", "BUY & HOLD", "WINS", HCOL, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["hold1"]
        hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -40, 200, C["ink"], 1, HEAD, True, "center")
        if k == 0:
            arrow_up(ctx, 0, 30, 0.35, C["white"])
        else:
            hold_icon(ctx, 0, 30, 0.42, C["white"])
        text(ctx, sub1, 0, 115, fit(ctx, sub1, 50, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 160, fit(ctx, sub2, 44, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["hold1"] - 0.2, T["hold1"] + 2.3, "guess", y=1080)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 5 hidden: the answer hides in one number
def num_file(ctx, cx, cy, t, a):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.04)
    card(ctx, -330, -150, 660, 300, (0xC8, 0x9B, 0x5A), a, 18, border=C["ink"])
    card(ctx, -330, -190, 240, 60, (0xC8, 0x9B, 0x5A), a, 12, shadow=False, border=C["ink"])
    text(ctx, "EVIDENCE", -210, -148, 30, C["ink"], a, TAGF, False, "center")
    text(ctx, "ONE NUMBER", 0, -60, 76, C["ink"], a, HEAD, True, "center")
    rect(ctx, -270, 0, 540, 110, (0x05, 0x05, 0x05), a)
    text(ctx, "? OUT OF ?", 0, 74, 50, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 6, 0, 12, 110, GOLD, 0.7 * a)
    ctx.restore()


def s_hidden(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    stars(ctx, t, 30, 180, 1150, 5, 0.6)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "THE ANSWER HIDES IN...", W / 2, 420, 90, C["white"], p, 980, 0, 12)
    q = back(prog(t, T["one1"] - 0.35, 0.4))
    if q > 0:
        ctx.save(); ctx.translate(540, 730); ctx.scale(max(q, 1e-3), max(q, 1e-3)); num_file(ctx, 0, 0, t, 1); ctx.restore()
    sticker(ctx, t, T["hold1"] - 0.2, T["hold1"] + 2.3, "guess", y=1080)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- race chart
def race_chart(ctx, t, up, zones=(), marks=False):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), 0, N - 1, RBOX); x1 = sx_of(di(d1), 0, N - 1, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    if marks:                                  # every +2% day = one green tick on the floor of the chart
        for i in BIG_I:
            if i > up:
                break
            rect(ctx, sx_of(i, 0, N - 1, RBOX) - 1.5, RBOX[1] + RBOX[3] - 34, 3, 34, GRNC, 0.9)
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
    for k, (lab, col) in enumerate((("BOUNCE CHASER", PCOL), ("BUY & HOLD", HCOL))):
        rect(ctx, RBOX[0] + 150 + k * 360, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 196 + k * 360, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")


# ---------------------------------------------------------------- 6 rules (+ the race starts underneath)
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, fg, x, tt, hw) in enumerate((("BUY", "AFTER A +2% DAY", GRNC, C["ink"], 290, T["buy2"], T["jump"]),
                                                         ("HOLD", "ONE MONTH", GOLD, C["ink"], 790, T["hold2"], T["month"]))):
        p = back(prog(t, tt - 0.12, 0.4))
        if p <= 0:
            continue
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, hw - 0.05, 0.4))
        ctx.save(); ctx.translate(x, 470); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
        card(ctx, -230, -110, 460, 220, col, 1, 22, border=C["ink"])
        if k == 0:
            arrow_up(ctx, -160, 0, 0.42, C["white"])
        else:
            hourglass(ctx, -160, 0, 0.5, t)
        text(ctx, title, 40, -10, fit(ctx, title, 84, 300), fg, 1, HEAD, True, "center")
        text(ctx, l1, 40, 60, fit(ctx, l1, 40, 300), fg, 1, HEAD, True, "center")
        ctx.restore()
    rc = ease(prog(t, s0 + 0.05, 0.4))
    if rc > 0:
        up = race_idx(t, [(s0 + 0.3, 1), (s1, di("2007-06-29"))])
        ctx.save(); ctx.translate(0, (1 - rc) * 200)
        race_chart(ctx, t, up, marks=True)
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_race08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-06-29")), (T["year"] + 0.3, di("2008-10-10")), (T["anyway"] + 0.4, di("2008-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), [("2008-01-01", "2008-12-31", C["red"], 0.22)], marks=True)
    tag(ctx, 540, 440, f"2008: {BY_YEAR[2008]} BIG JUMPS", GRNC, back(prog(t, T["Thirty"] - 0.1, 0.3)), 44, -0.03)
    if t < T["sinks"] - 0.25:
        tag(ctx, 540, 524, "THE CHASER BUYS THEM ALL", PCOL, back(prog(t, T["buys"] - 0.1, 0.3)), 36, 0.02)
    else:
        tag(ctx, 540, 524, "...AND SINKS ANYWAY", C["red"], back(prog(t, T["sinks"] - 0.25, 0.3)), 40, 0.02, C["white"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("shock" if t > T["sinks"] else "smug") if e != "talk" else e)


def s_calm(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x6F, 0xC8), (0x0B, 0x2A, 0x5E))
    sun(ctx, 965, 345, 40, t)
    for k in range(4):
        cloud(ctx, ((t - s0) * 40 + k * 330) % (W + 300) - 200, 250 + (k % 2) * 110 + k * 20, 0.9, a=0.5)
    pts = [(s0 + 0.1, di("2008-12-31")), (T["climb"] + 0.5, di("2013-12-31")), (T["vanish"] + 0.6, di("2017-12-29")),
           (s1, di("2017-12-29"))]
    race_chart(ctx, t, race_idx(t, pts), [("2012-01-01", "2017-12-29", GOLD, 0.10)], marks=True)
    if t < T["vanish"] - 0.25:
        tag(ctx, 540, 440, "THE CALM YEARS", C["cream"], back(prog(t, T["calm"] - 0.25, 0.3)), 44, -0.03)
    else:
        tag(ctx, 540, 440, "2017: ZERO BIG JUMPS", GOLD, back(prog(t, T["vanish"] - 0.25, 0.3)), 44, -0.03)
    if t < T["sits"] - 0.3:
        tag(ctx, 540, 524, "STOCKS CLIMB", HCOL, back(prog(t, T["Stocks"] - 0.1, 0.3)), 40, 0.02)
    else:
        tag(ctx, 540, 524, "THE CHASER SITS IN CASH", PCOL, back(prog(t, T["sits"] - 0.3, 0.3)), 38, 0.02)
        zz = (t * 0.8) % 1
        text(ctx, "Z", 930 + zz * 50, 1300 - zz * 120, 40 + zz * 40, C["white"], 1 - zz, HEAD, True, "center", outline=6, ocol=C["ink"])
    bunting(ctx, "CALM YEARS", t, s0, [HCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if (e != "talk" and t > T["sits"]) else e)


# ---------------------------------------------------------------- 9 strange: 4 of 5 big jumps came inside a hole
def s_strange(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    for k in range(40):                       # slow red rain
        u = ((t - s0) * 0.35 + k / 40) % 1
        rect(ctx, (k * 137) % W, u * 1300, 4, 46, REDC, 0.18)
    if t < T["Four"] - 0.15:
        p = back(prog(t, s0 + 0.03, 0.3))
        big_title(ctx, "NOW THE STRANGE PART", W / 2, 430, 96, GOLD, p, 980, -0.02, 12)
    else:
        text(ctx, f"{N_BIG} BIG JUMPS · 2005-2024", W / 2, 430, 50, C["white"], 1, MONO, True, "center", outline=7, ocol=C["ink"])
    cols, sp = 20, 46
    x0 = (W - cols * sp) / 2 + sp / 2; y0 = 520
    kk = prog(t, T["Four"], max(0.5, T["hole"] - T["Four"] - 0.4))
    nred = int(N_DEEP * ease_io(kk))
    for j in range(N_BIG):
        ap = clamp((t - s0 - 0.1 - j * 0.006) / 0.2)
        if ap <= 0:
            continue
        cx = x0 + (j % cols) * sp; cy = y0 + (j // cols) * sp
        red = j < nred
        s = 17 * ap * (1 + (0.25 * math.sin(t * 9 + j) if (red and j >= nred - 6) else 0))
        ctx.new_path(); ctx.arc(cx, cy + (8 if red else 0), s, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba(REDC if red else GRNC, 1)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(4); ctx.stroke()
    q = back(prog(t, T["Four"] - 0.1, 0.35))
    big_title(ctx, "4 OUT OF 5", W / 2, 1000, 140, GOLD, q, 900, -0.02, 16)
    r = back(prog(t, T["already"] - 0.15, 0.3))
    tag(ctx, 540, 1095, "MARKET ALREADY DOWN 10%+", C["red"], r, 44, 0.015, C["white"])
    bunting(ctx, "STRANGE", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("shock" if t > T["Four"] else "neutral") if e != "talk" else e)


# ---------------------------------------------------------------- 10 remember: 2 out of 3 bounces erased within 3 months
BPTS = [(0.00, 0.00), (0.10, -0.03), (0.18, 0.02), (0.22, 0.62), (0.30, 0.50), (0.38, 0.74), (0.46, 0.42), (0.54, 0.56),
        (0.62, 0.20), (0.70, 0.30), (0.78, -0.12), (0.86, -0.04), (0.93, -0.38), (1.00, -0.52)]


def bounce_diagram(ctx, t, k):
    bx, by, bw, bh = 120, 590, 840, 380
    card(ctx, bx - 20, by - 20, bw + 40, bh + 40, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    base = by + bh * 0.58
    for j in range(21):
        rect(ctx, bx + j * 40, base - 2, 22, 4, C["white"], 0.6)
    text(ctx, "PRICE BEFORE THE JUMP", bx + 12, base + 34, 24, C["white"], 0.8, MONO, True, "left")
    n = max(2, int(1 + k * (len(BPTS) - 1)))
    frac = k * (len(BPTS) - 1) - (n - 1) if n < len(BPTS) else 0
    pts = BPTS[:n]
    if n < len(BPTS) and frac > 0:
        (a0, b0), (a1, b1) = BPTS[n - 1], BPTS[n]
        pts = pts + [(a0 + (a1 - a0) * frac, b0 + (b1 - b0) * frac)]
    xs = [bx + 20 + u * (bw - 60) for u, _ in pts]; ys = [base - v * bh * 0.52 for _, v in pts]
    up_n = [i for i, (u, v) in enumerate(pts) if u <= 0.62]
    if len(up_n) > 1:
        poly(ctx, xs[:len(up_n)], ys[:len(up_n)], GRNC, 9, 1, glow=True)
    if len(pts) > len(up_n):
        poly(ctx, xs[len(up_n) - 1:], ys[len(up_n) - 1:], REDC, 9, 1, glow=True)
    ctx.new_path(); ctx.arc(xs[-1], ys[-1], 15, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["white"])); ctx.fill()
    if k > 0.2:
        tag(ctx, bx + 300, by + 30, "THE BIG JUMP", GRNC, back(clamp((k - 0.2) / 0.1)), 26, -0.03)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x3A), (0x04, 0x05, 0x14))
    god_rays(ctx, W / 2, 700, t, 0.07, GOLD, 14, 1400)
    if t < T["Two2"] - 0.1:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT ONE NUMBER?", W / 2, 670, 110, C["white"], r, 980, 0, 12)
        ctx.save(); ctx.translate(540, 950); ctx.scale(0.72, 0.72); num_file(ctx, 0, 0, t, 1); ctx.restore()
    else:
        p = back(prog(t, T["Two2"] - 0.1, 0.35))
        pulse = 1 + 0.03 * math.sin(t * 7)
        big_title(ctx, "2 OUT OF 3", W / 2, 500, 190, GOLD, p * pulse, 960, -0.02, 18)
        k = clamp((t - T["Thats"]) / max(0.5, T["erased"] + 0.25 - T["Thats"]))
        if t > T["Thats"] - 0.2:
            bounce_diagram(ctx, t, ease_io(k))
        if t > T["erased"] - 0.05:
            stamp_box(ctx, ["BOUNCE ERASED"], 765, 660, T["erased"] - 0.05, t, C["red"], 400, 50, 0.05)
        w = back(prog(t, T["within"] - 0.1, 0.3))
        if w > 0:
            s_ = f"{ERASED} OF {ERASED_N} · WITHIN 3 MONTHS"
            tag(ctx, 540, 1085, s_, C["cream"], w, 40, -0.015)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], C["blue"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["erased"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 11 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -42, 900, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=PCOL)
        s_ = "HOLD 1 DAY ... 1 YEAR: CHASER NEVER WON"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 860, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 420, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · BOUNCE CHASER (0.05% FEES)", money(CHV), PCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["Its2"] - 0.15, "right", y=1080)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x02, 0x08, 0x06), 0.8)
    stamp_box(ctx, ["A BIG GREEN DAY", "ISN'T AN ALL-CLEAR."], W / 2, 495, T["green"] - 0.1, t, STAMP_OR, 880, 80, -0.05)
    stamp_box(ctx, ["IT'S A SYMPTOM."], W / 2 + 10, 765, T["Its2"] - 0.05, t, C["red"], 760, 92, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["Its2"] - 0.15, "right", y=1080)
    fb = back(prog(t, T["Its2"] + 0.1, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1070); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #15", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "bestday": s_bestday, "chase": s_chase, "guess": s_guess, "hidden": s_hidden, "rules": s_rules,
            "race08": s_race08, "calm": s_calm, "strange": s_strange, "remember": s_remember, "score": s_score,
            "verdict": s_verdict, "loop": s_loop}
