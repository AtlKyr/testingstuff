# ================================================================ Autopsy #23 scenes (10% stop-loss on the whole market)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD
PCOL = (0xFF, 0x6B, 0x3D)    # PANIC SELLER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x1C, 0x10, 0x3A), (0x05, 0x03, 0x10)
RBOX = (110, 620, 860, 320)
LCOL = (0xFF, 0xA8, 0x1E)    # THE 200-DAY LINE rule
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
    tag(ctx, 160, 66, "CASE #23", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["alarm"] - SC["question"]))
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

LCOL = (0xFF, 0x8A, 0x3D)   # PROFIT TAKER (orange)
YCOL = (0xFF, 0x5C, 0x5C)   # yield line


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2007, 2009, 2011)):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 2, up)
    if curtain is not None:
        up = min(up, curtain)
    for i0, i1 in ZONES:   # cash zones of the profit taker (only up to the visible point)
        if i0 > up:
            break
        x0 = sx_of(i0, S0, xe, RBOX); x1 = sx_of(min(i1, up), S0, xe, RBOX)
        rect(ctx, x0, by, max(3, x1 - x0), bh, LCOL, 0.22 * a)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), S0, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(RV[S0:hi]), np.nanmax(BV[S0:hi]))))
    vmin = 5000.0
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    tips = []
    for arr, col in ((BV, HCOL), (RV, LCOL)):
        xs, ys = series_xy(arr, S0, xe, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (lx, ly) = tips
    lead_l = RV[up] > BV[up] + 1
    off = 0 if abs(hy - ly) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_l else 0), 4, "tophat", t, "sad" if lead_l else "smug", False, True)
    mini_rocco(ctx, lx, ly - 4 - (0 if lead_l else off), 4, "race", t, "smug" if lead_l else "sad", False, True)
    if curtain is not None:
        xc = sx_of(curtain, S0, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("10% STOP-LOSS", LCOL), ("JUST HOLD", HCOL))):
        rect(ctx, bx + bw - 300, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 260, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + bh - 60, 30, 18, LCOL, 0.35)
    text(ctx, "= IN CASH", bx + 60, by + bh - 45, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2010-12-31"); XE2 = N - 1
YR2 = (2006, 2010, 2014, 2018, 2022)


def yield_gauge(ctx, cx, cy, s, t, val=5.0, a=1.0):
    """a pressure gauge with the needle in the red at ~5%"""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 150, math.pi, 2 * math.pi); ctx.close_path()
    ctx.set_source_rgba(*rgba((0x0C, 0x10, 0x1C), a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(10); ctx.stroke()
    for k, col in enumerate((GRNC, GOLD, REDC)):
        ctx.new_path(); ctx.arc(0, 0, 118, math.pi + k * math.pi / 3, math.pi + (k + 1) * math.pi / 3)
        ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(30); ctx.stroke()
    ang = math.pi + math.pi * (0.86 + 0.04 * math.sin(t * 9))
    ctx.new_path(); ctx.move_to(0, 0); ctx.line_to(math.cos(ang) * 120, math.sin(ang) * 120)
    ctx.set_source_rgba(*rgba(C["white"], a)); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 18, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: -10% / STOP-LOSS?)
def shield(ctx, cx, cy, s, t, col=HCOL, a=1.0, crack=False):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.sin(t * 3) * 0.06); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -130); ctx.curve_to(70, -100, 110, -100, 120, -110); ctx.curve_to(125, 20, 80, 100, 0, 150)
    ctx.curve_to(-80, 100, -125, 20, -120, -110); ctx.curve_to(-110, -100, -70, -100, 0, -130); ctx.close_path()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(12); ctx.stroke()
    ctx.new_path(); ctx.move_to(-50, 0); ctx.line_to(-12, 40); ctx.line_to(55, -40)
    ctx.set_source_rgba(*rgba(C["white"], a)); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if crack:
        ctx.new_path(); ctx.move_to(10, -130); ctx.line_to(-15, -60); ctx.line_to(20, -10); ctx.line_to(-10, 60); ctx.line_to(5, 150)
        ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x14), (0x08, 0x02, 0x06))
    god_rays(ctx, W / 2, 560, t, 0.09, REDC, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, u * 1500, 4, 40, (0xFF, 0x80, 0x80), 0.14)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(470 + shake, 550); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "-10%", 0, 0, 330, REDC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    arrow_down(ctx, 900, 440 + math.sin(t * 6) * 10, 0.5 * s_, REDC)
    ctx.save(); ctx.translate(540, 780); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "STOP-LOSS?", 0, 0, fit(ctx, "STOP-LOSS?", 200, 1000), C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    shield(ctx, 250, 1040, 0.75 * max(p, 1e-3), t)
    if show_tag:
        tag(ctx, 540, 200, "THE WHOLE S&P 500", C["cream"], p, 44, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 the question
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "A 10% STOP", W / 2, 520, 170, GOLD, back(prog(t, T["ten1"] - 0.2, 0.3)), 980, -0.03, 18)
    big_title(ctx, "ON THE WHOLE MARKET?", W / 2, 680, 100, C["white"], back(prog(t, T["whole"] - 0.2, 0.3)), 980, 0.02, 14)
    shield(ctx, 760, 960, 0.8, t, a=ease(prog(t, s0, 0.4)))
    bunting(ctx, "THE QUESTION", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess (race starts under the cards)
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "IT", "PROTECTS", LCOL, -230, ta), ("B", "IT", "COSTS YOU", HCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -135, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, -12, fit(ctx, l1, 56, 250), C["ink"], 1, HEAD, True, "center")
        text(ctx, l2, 60, 52, fit(ctx, l2, 56, 250), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["rules"] + 5.0, di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"], T["B"], 420, T["costs"])
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["costs"], T["costs"] + 2.4, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 the clue: one number
def evidence(ctx, cx, cy, t, a=1.0, label="ONE NUMBER"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "?? OF ?? SELLS", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE NUMBER IS HIDING...", W / 2, 425, 92, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["number1"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["costs"], T["costs"] + 2.4, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 5 rules
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("-10% FROM THE TOP", "SELL", LCOL, 290, T["sell"]),
                                                 ("+10% OFF THE LOW", "BUY BACK", GRNC, 790, T["buy"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        if k == 0:
            arrow_down(ctx, -175, 0, 0.42, C["white"])
        else:
            arrow_up(ctx, -175, 0, 0.42, C["white"])
        text(ctx, title, 45, -12, fit(ctx, title, 52, 330), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 45, 62, fit(ctx, l1, 64, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 6 2008: stop fires early, pulls ahead
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["ahead1"] + 0.3, di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "JAN 2008: THE STOP FIRES", C["red"], back(prog(t, T["fires"] - 0.15, 0.3)), 46, -0.03, C["white"])
    tag(ctx, 540, 530, "STOP-LOSS PULLS AHEAD", LCOL, back(prog(t, T["ahead1"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 7 whipsaws: 2009 -> 2019, 2018 sold & bought back higher
def s_whip(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x06), (0x0C, 0x06, 0x02))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        x = (k * 173) % W
        rect(ctx, x, 1300 - u * 1300, 6, 30, GOLD, 0.12)
    xe = int(XE1 + (XE2 - XE1) * ease_io(prog(t, s0, 1.2)))
    pts = [(s0 + 0.1, di("2009-03-09")), (T["eighteen"], di("2018-01-31")), (T["higher1"] + 0.3, di("2019-01-31"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, xe, curtain=up + 1, years=YR2)
    tag(ctx, 540, 440, "THE WHIPSAWS", C["red"], back(prog(t, T["whipsaws"] - 0.15, 0.3)), 50, -0.03, C["white"])
    if t > T["sold"] - 0.15:
        tag(ctx, 540, 530, "2018: SOLD... BOUGHT BACK HIGHER", GOLD, back(prog(t, T["sold"] - 0.15, 0.3)), 38, 0.02, C["ink"])
    bunting(ctx, "2009-2019", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("sad" if t > T["higher1"] else "smug") if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 8 2020: out before the worst, back near the bottom -> ahead again
P0, P1 = di("2020-01-02"), di("2020-06-30")


def zoom_chart(ctx, box, i0, i1, k, t, marks, a=1.0, labels=()):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    seg = CL[i0:i1 + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    xs, ys = series_xy(CL, i0, i1, up, box, lo, hi, 1)
    poly(ctx, xs, ys, C["white"], 8, a, glow=True)
    for mi, lab, col, tt in marks:
        if i0 <= mi <= up and t >= tt:
            sx = sx_of(mi, i0, i1, box); sy = by + bh - (OP[mi] - lo) / (hi - lo) * bh
            pp = back(prog(t, tt, 0.3))
            ctx.save(); ctx.translate(sx, sy + (60 if lab.startswith("BUY") else -60)); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            card(ctx, -56, -26, 112, 52, col, 1, 10, border=C["ink"]); text(ctx, lab, 0, 12, 30, C["ink"], 1, HEAD, True, "center")
            ctx.restore()
            ctx.new_path(); ctx.arc(sx, sy, 10, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    for lab, d in labels:
        text(ctx, lab, sx_of(di(d), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    big_title(ctx, "2020", W / 2, 490, 150, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
    k = ease_io(prog(t, s0 + 0.3, 2.6))
    zoom_chart(ctx, (150, 570, 780, 330), P0, P1, k, t, [(SELLI[11], "SELL", LCOL, T["out1"]), (BUYI[11], "BUY", GRNC, T["bottom"] - 0.2)],
               labels=(("JAN", "2020-01-02"), ("MAR", "2020-03-02"), ("MAY", "2020-05-01"), ("JUN", "2020-06-30")))
    if t > T["Ahead"] - 0.15:
        pp = back(prog(t, T["Ahead"] - 0.15, 0.35))
        ctx.save(); ctx.translate(540, 1060); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "AHEAD AGAIN!", 0, 0, 110, GRNC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "THE CRASH", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("smug" if t > T["bottom"] else "shock") if e != "talk" else e)


# ---------------------------------------------------------------- 9 remember that hidden number -> 15 sells, 9 bought back higher
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["Fifteen"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 500, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT HIDDEN NUMBER?", W / 2, 650, 100, C["white"], r, 980, 0, 14)
    else:
        p = back(prog(t, T["Fifteen"] - 0.12, 0.35))
        big_title(ctx, "15 SELLS", W / 2, 500, 150, GOLD, p, 960, -0.03, 16)
        cw, ch, gap = 150, 110, 18
        for n, pr in enumerate(PAIRS):
            row, col = divmod(n, 5)
            x = 540 - (5 * cw + 4 * gap) / 2 + col * (cw + gap); y = 580 + row * (ch + gap)
            tp = T["Fifteen"] + n * 0.07
            pk = back(prog(t, tp, 0.3))
            if pk <= 0:
                continue
            hi_ = pr[2] > 0
            colr = (C["red"] if hi_ else GRNC) if t > T["Nine"] - 0.1 else (0x3A, 0x40, 0x50)
            ctx.save(); ctx.translate(x + cw / 2, y + ch / 2); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            card(ctx, -cw / 2, -ch / 2, cw, ch, colr, 1, 14, border=C["ink"])
            text(ctx, pr[0][:4], 0, -8, 34, C["white"], 1, MONO, True, "center", outline=5, ocol=C["ink"])
            if t > T["Nine"] - 0.1:
                if hi_:
                    arrow_up(ctx, 0, 30, 0.16, C["white"])
                else:
                    arrow_down(ctx, 0, 30, 0.16, C["ink"])
            ctx.restore()
        if t > T["Nine"] - 0.1:
            tag(ctx, 540, 1000, "9 TIMES: BOUGHT BACK HIGHER", C["red"], back(prog(t, T["Nine"] - 0.1, 0.3)), 42, 0.02, C["white"])
    bunting(ctx, "THE HIDDEN NUMBER", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["Nine"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 2022: shaken out three times
Z0, Z1 = di("2022-01-03"), di("2022-12-30")


def s_y2022(ctx, t, s0, s1):
    rain_bg(ctx, t)
    big_title(ctx, "2022", W / 2, 490, 150, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
    k = ease_io(prog(t, s0 + 0.2, 2.2))
    marks = []
    for n in (12, 13, 14):
        marks.append((SELLI[n], "SELL", LCOL, s0 + 0.2 + 2.2 * (SELLI[n] - Z0) / (Z1 - Z0)))
        if BUYI[n] <= Z1:
            marks.append((BUYI[n], "BUY", GRNC, s0 + 0.2 + 2.2 * (BUYI[n] - Z0) / (Z1 - Z0)))
    zoom_chart(ctx, (150, 590, 780, 330), Z0, Z1, k, t, marks,
               labels=(("JAN", "2022-01-03"), ("APR", "2022-04-01"), ("JUL", "2022-07-01"), ("OCT", "2022-10-03")))
    if t > T["three"] - 0.15:
        tag(ctx, 540, 1080, "SHAKEN OUT 3 TIMES", C["red"], back(prog(t, T["three"] - 0.15, 0.3)), 46, 0.02, C["white"])
    bunting(ctx, "THE SHAKEOUT", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


# ---------------------------------------------------------------- 11 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"REBUY AT +15%: {money(SC_['0.1/0.15'])}  ·  5% STOP: {money(SC_['0.05/0.1'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · 10% STOP-LOSS (0.05% FEES)", money(RULE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · JUST HOLDING", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["SOFTENED THE CRASHES..."], W / 2, 470, T["softened"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    stamp_box(ctx, ["CHARGED FOR", "EVERY FALSE ALARM."], W / 2 + 10, 700, T["charged"] - 0.1, t, C["red"], 860, 70, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["false"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 880); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #24", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules, "crash": s_crash,
            "whip": s_whip, "y2020": s_y2020, "remember": s_remember, "y2022": s_y2022, "score": s_score, "verdict": s_verdict, "loop": s_loop}
