# ================================================================ Autopsy #24 scenes (sell when the fear gauge spikes?)
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
    tag(ctx, 160, 66, "CASE #24", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["trap2"] - SC["question"]))
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
    for k, (lab, col) in enumerate((("FEAR SELLER", LCOL), ("SIT TIGHT", HCOL))):
        rect(ctx, bx + bw - 300, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 260, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + bh - 60, 30, 18, LCOL, 0.35)
    text(ctx, "= IN CASH", bx + 60, by + bh - 45, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2010-12-31"); XE2 = N - 1
YR2 = (2006, 2010, 2014, 2018, 2022)


def fear_gauge(ctx, cx, cy, s, t, val=0.86, a=1.0):
    """a pressure gauge with the needle in the red at ~5%"""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 150, math.pi, 2 * math.pi); ctx.close_path()
    ctx.set_source_rgba(*rgba((0x0C, 0x10, 0x1C), a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(10); ctx.stroke()
    for k, col in enumerate((GRNC, GOLD, REDC)):
        ctx.new_path(); ctx.arc(0, 0, 118, math.pi + k * math.pi / 3, math.pi + (k + 1) * math.pi / 3)
        ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(30); ctx.stroke()
    ang = math.pi + math.pi * (val + 0.04 * math.sin(t * 9))
    ctx.new_path(); ctx.move_to(0, 0); ctx.line_to(math.cos(ang) * 120, math.sin(ang) * 120)
    ctx.set_source_rgba(*rgba(C["white"], a)); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 18, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
    ctx.restore()


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




# ---------------------------------------------------------------- 1 hook (frame 0: +70% / FEAR?)
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
    ctx.save(); ctx.translate(470 + shake, 560); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "+70%", 0, 0, 320, REDC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    arrow_up(ctx, 920, 420 + math.sin(t * 6) * 10, 0.5 * s_, REDC)
    ctx.save(); ctx.translate(540, 790); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "FEAR?", 0, 0, 230, C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    fear_gauge(ctx, 270, 1080, 0.85 * max(p, 1e-3), t, 0.9)
    if show_tag:
        tag(ctx, 540, 200, "WALL STREET'S FEAR GAUGE · 1 DAY", C["cream"], p, 40, -0.03)


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
    big_title(ctx, "FEAR SPIKES.", W / 2, 520, 170, GOLD, back(prog(t, T["spikes"] - 0.2, 0.3)), 980, -0.03, 18)
    big_title(ctx, "DO YOU SELL?", W / 2, 690, 130, C["white"], back(prog(t, T["sell"] - 0.2, 0.3)), 980, 0.02, 14)
    fear_gauge(ctx, 760, 970, 0.8, t, 0.92, a=ease(prog(t, s0, 0.4)))
    bunting(ctx, "THE QUESTION", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess (race starts under the cards)
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "SELL", "THE FEAR", LCOL, -230, ta), ("B", "SIT", "TIGHT", HCOL, 230, tb))):
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


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["crash"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"], T["B"], 420, T["B"] + 0.3)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 the clue: the way back in
def evidence(ctx, cx, cy, t, a=1.0, label="THE WAY BACK IN"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "BOUGHT BACK ???", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "THE TRAP IS...", W / 2, 425, 100, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["way"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 5 rules
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("FEAR HITS 30", "SELL", LCOL, 290, T["thirty"]),
                                                 ("BACK UNDER 20", "BUY BACK", GRNC, 790, T["twenty1"]))):
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


# ---------------------------------------------------------------- 6 2008: dodges the crash, pulls way ahead
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["ahead"] + 0.3, di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "SEPT 2008: FEAR HITS 30 - SOLD", C["red"], back(prog(t, T["dodges"] - 0.15, 0.3)), 40, -0.03, C["white"])
    tag(ctx, 540, 530, "FEAR SELLER PULLS WAY AHEAD", LCOL, back(prog(t, T["pulls"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 7 fear stays high -> back in late 2009 at the same price, rebound missed
def s_rebuy(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x06), (0x0C, 0x06, 0x02))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        x = (k * 173) % W
        rect(ctx, x, 1300 - u * 1300, 6, 30, GOLD, 0.12)
    pts = [(s0 + 0.1, di("2009-03-09")), (T["late"], di("2009-12-23")), (T["missed"] + 0.3, di("2010-04-23"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE1, curtain=up + 1)
    if t > T["buys"] - 0.15:
        tag(ctx, 540, 440, "DEC 2009: BOUGHT BACK", GRNC, back(prog(t, T["buys"] - 0.15, 0.3)), 44, -0.03, C["ink"])
    if t > T["same"] - 0.15:
        tag(ctx, 540, 530, "AT ALMOST THE SAME PRICE", GOLD, back(prog(t, T["same"] - 0.15, 0.3)), 42, 0.02, C["ink"])
    if t > T["missed"] - 0.15:
        pp = back(prog(t, T["missed"] - 0.15, 0.35))
        ctx.save(); ctx.translate(540, 1060); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "REBOUND MISSED", 0, 0, 100, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "2009", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("sad" if t > T["rebound"] else "neutral") if e != "talk" else e)


# ---------------------------------------------------------------- 8 2020: sells in the Covid crash, then waits for calm
P0, P1 = di("2020-01-02"), di("2021-03-31")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    big_title(ctx, "2020", W / 2, 490, 150, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
    # draw only up to the "waits" moment -> the line keeps climbing while it waits; the rebuy stays hidden
    kmax = (di("2020-08-31") - P0) / (P1 - P0)
    k = kmax * ease_io(prog(t, s0 + 0.3, max(0.5, T["calm"] - s0 - 0.3)))
    zoom_chart(ctx, (150, 590, 780, 330), P0, P1, k, t, [(SELLI[9], "SELL", LCOL, T["sells"])],
               labels=(("JAN 20", "2020-01-02"), ("JUN", "2020-06-01"), ("NOV", "2020-11-02"), ("MAR 21", "2021-03-31")))
    if t > T["waits"] - 0.15:
        a = ease(prog(t, T["waits"] - 0.15, 0.3))
        hourglass(ctx, 840, 1090, 0.55 * a, t)
        tag(ctx, 470, 1060, "WAITING FOR CALM...", GOLD, back(prog(t, T["waits"] - 0.15, 0.3)), 44, -0.02, C["ink"])
    bunting(ctx, "THE COVID CRASH", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("smug" if t < T["waits"] else "sleep") if e != "talk" else e)


# ---------------------------------------------------------------- 9 remember the way back in -> fear above 20 ~1 year, bought back +39%
V0, V1 = di("2020-01-02"), di("2021-03-31")


def vix_chart(ctx, box, t, k, a=1.0):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    lo, hi = 10.0, 85.0
    y20 = by + bh - (20 - lo) / (hi - lo) * bh
    for j in range(26):
        rect(ctx, bx + j * 30, y20 - 2, 18, 4, GRNC, 0.9)
    text(ctx, "CALM = UNDER 20", bx + bw - 10, y20 + 34, 24, GRNC, 1, MONO, True, "right")
    up = int(V0 + 2 + (V1 - V0 - 2) * clamp(k))
    xs, ys = series_xy(VX, V0, V1, up, box, lo, hi, 1)
    poly(ctx, xs, ys, C["red"], 7, a, glow=True)
    text(ctx, "FEAR GAUGE", bx + 10, by + 30, 26, C["red"], 1, MONO, True, "left")
    for lab, d in (("JAN 20", "2020-01-02"), ("JUN", "2020-06-01"), ("NOV", "2020-11-02"), ("MAR 21", "2021-03-31")):
        text(ctx, lab, sx_of(di(d), V0, V1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["Fear1"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THE WAY BACK IN?", W / 2, 680, 110, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    elif t < T["bought"] - 0.12:
        k = ease_io(prog(t, T["Fear1"] - 0.1, T["year"] - T["Fear1"] + 0.2))
        vix_chart(ctx, (150, 520, 780, 360), t, k)
        if t > T["year"] - 0.15:
            tag(ctx, 540, 1040, "ABOVE 20 FOR ALMOST A YEAR", C["red"], back(prog(t, T["year"] - 0.15, 0.3)), 42, 0.02, C["white"])
    else:
        zoom_chart(ctx, (150, 560, 780, 330), P0, P1, 1.0, t, [(SELLI[9], "SELL", LCOL, 0), (BUYI[9], "BUY", GRNC, T["bought"])],
                   labels=(("JAN 20", "2020-01-02"), ("JUN", "2020-06-01"), ("NOV", "2020-11-02"), ("MAR 21", "2021-03-31")))
        if t > T["thirtynine"] - 0.1:
            pp = back(prog(t, T["thirtynine"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1050); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "BOUGHT BACK +39%", 0, 0, 104, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
            ctx.restore()
        if t > T["bought"] - 0.1:
            tag(ctx, 540, 470, "354 DAYS AFTER THE SELL", GOLD, back(prog(t, T["bought"] - 0.1, 0.3)), 44, -0.02, C["ink"])
    bunting(ctx, "THE WAY BACK IN", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["thirtynine"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"11 TRIGGER COMBOS TESTED: ALL LOST · BEST {money(max(SC_.values()))}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "B · SIT TIGHT", money(HOLD_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "A · FEAR SELLER (0.05% FEES)", money(RULE_V), LCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 470, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 11 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["SELLING FEAR FELT SAFE..."], W / 2, 470, T["Selling"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    stamp_box(ctx, ["BUYING BACK", "WAS THE TRAP."], W / 2 + 10, 680, T["Buying"] - 0.1, t, C["red"], 860, 70, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["Buying"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 860); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #25", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules, "crash": s_crash,
            "rebuy": s_rebuy, "y2020": s_y2020, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #26 overrides (red mornings: sit out the day?)
LCOL = (0xFF, 0x8A, 0x3D)   # THE SITTER (orange)
SUNR = (0xFF, 0x7A, 0x45)


def hud(ctx, t):
    a = ease(prog(t, SC["question"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #26", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["Leaving"] - SC["question"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2007, 2009, 2011)):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 2, up)
    if curtain is not None:
        up = min(up, curtain)
    for si in SELLI:   # one red tick per red-morning exit
        if si > up or si > xe:
            break
        x0 = sx_of(si, S0, xe, RBOX)
        rect(ctx, x0 - 1.5, by + bh - 34, 3, 34, C["red"], 0.75 * a)
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
    mini_rocco(ctx, lx, ly - 4 - (0 if lead_l else off), 4, "night", t, "smug" if lead_l else "sad", False, True)
    if curtain is not None:
        xc = sx_of(curtain, S0, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("A · SITS OUT", LCOL), ("B · JUST HOLDS", HCOL))):
        rect(ctx, bx + bw - 330, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 290, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + 10, 4, 26, C["red"])
    text(ctx, "= RED-MORNING EXIT", bx + 34, by + 32, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2011-12-30"); XE2 = N - 1


def sunrise(ctx, cx, cy, r, t, col=SUNR, a=1.0):
    g = cairo.RadialGradient(cx, cy, r * 0.5, cx, cy, r * 2.6)
    g.add_color_stop_rgba(0, col[0] / 255, col[1] / 255, col[2] / 255, 0.45 * a); g.add_color_stop_rgba(1, col[0] / 255, col[1] / 255, col[2] / 255, 0)
    ctx.set_source(g); ctx.new_path(); ctx.arc(cx, cy, r * 2.6, 0, 2 * math.pi); ctx.fill()
    ctx.new_path(); ctx.arc(cx, cy, r, math.pi, 2 * math.pi); ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def gap_candles(ctx, x, y, s, t, a=1.0):
    """yesterday green candle, today's candle opens far below (red), with a dashed 'gap' line"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    candle(ctx, -150, -160, 90, 170, GRNC, a, 40)
    for j in range(8):
        rect(ctx, -60 + j * 30, -160, 18, 5, C["white"], 0.6 * a)
    dy = 40 + 10 * math.sin(t * 5)
    candle(ctx, 60, -160 + 120 + dy * 0.2, 90, 150, REDC, a, 40)
    text(ctx, "GAP", 105, -190, 40, C["white"], a, HEAD, True, "center", outline=6, ocol=C["ink"])
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: -1% / SIT OUT?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x40, 0x10, 0x16), (0x08, 0x02, 0x06))
    sunrise(ctx, 540, 1180, 230, t, SUNR, 0.9)
    god_rays(ctx, W / 2, 1180, t, 0.08, SUNR, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, u * 1500, 4, 40, (0xFF, 0x80, 0x80), 0.12)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(470 + shake, 560); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "-1%", 0, 0, 330, REDC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    arrow_down(ctx, 900, 430 + math.sin(t * 6) * 10, 0.5 * s_, REDC)
    ctx.save(); ctx.translate(540, 790); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "SIT OUT?", 0, 0, 210, C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    if show_tag:
        tag(ctx, 540, 200, "RED MORNING · NASDAQ FUTURES ALMOST -1% TODAY", C["cream"], p, 34, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 red morning
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x16, 0x20), (0x0A, 0x04, 0x08))
    sunrise(ctx, 540, 1150, 200, t, REDC, 0.8)
    big_title(ctx, "RED MORNING.", W / 2, 520, 170, REDC, back(prog(t, s0 + 0.02, 0.3)), 980, -0.03, 18)
    gap_candles(ctx, 540, 930, 1.0 * ease(prog(t, s0 + 0.1, 0.35)) + 1e-3, t)
    bunting(ctx, "9:30 AM", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess (race starts under the cards)
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "SIT OUT", "THE DAY", LCOL, -230, ta), ("B", "JUST", "HOLD", HCOL, 230, tb))):
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


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["crash"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"], T["B"], 420, T["B"] + 0.3)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="THE NEXT MORNING"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "BOUGHT BACK AT ???", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "THE TRAP IS...", W / 2, 425, 100, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["next1"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("OPENS -1%", "SELL AT OPEN", LCOL, 290, T["opens"]),
                                                 ("NEXT MORNING", "BUY BACK", GRNC, 790, T["buy"]))):
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
        text(ctx, l1, 45, 62, fit(ctx, l1, 60, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["dodges"], di("2008-12-31")), (T["ahead"] + 0.3, di("2011-12-30"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "2008: 31 RED MORNINGS", C["red"], back(prog(t, T["thirtyone"] - 0.15, 0.3)), 44, -0.03, C["white"])
    tag(ctx, 540, 530, "BY 2011: THE SITTER LEADS", LCOL, back(prog(t, T["eleven"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("smug" if t > T["ahead"] else "shock") if e != "talk" else e)


def s_flip(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x06), (0x0C, 0x06, 0x02))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GOLD, 0.12)
    pts = [(s0 + 0.1, di("2011-12-30")), (T["steps"] + 0.4, di("2016-12-30"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE2, curtain=up + 1, years=(2006, 2010, 2014, 2018, 2022))
    tag(ctx, 540, 440, "THEN IT FLIPS", C["red"], back(prog(t, T["flips"] - 0.15, 0.3)), 48, -0.03, C["white"])
    tag(ctx, 540, 530, "EVERY SCARE: OUT FOR A DAY", GOLD, back(prog(t, T["Every"] - 0.1, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "2012 - 2016", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("sad" if t > T["flips"] else "neutral") if e != "talk" else e, prop=prop_flag)


def dot_grid(ctx, t, t0, x0, y0, a=1.0):
    """215 exits, one dot each: gold = bought back HIGHER next morning, grey = lower"""
    ups = [p for p in range(TRADES)]
    hi_ = HIGHER
    for k in range(TRADES):
        cx = x0 + (k % 18) * 46; cy = y0 + (k // 18) * 30
        pk = prog(t, t0 + k * 0.012, 0.15)
        col = GOLD if k < hi_ else (0x60, 0x66, 0x70)
        rect(ctx, cx, cy, 34, 20, col if pk > 0.5 else (0x30, 0x34, 0x3A), a)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["More"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THE NEXT MORNING?", W / 2, 680, 110, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    else:
        big_title(ctx, "BOUGHT BACK HIGHER?", W / 2, 520, 96, C["white"], back(prog(t, T["More"] - 0.1, 0.3)), 980, -0.02, 12)
        dot_grid(ctx, t, T["More"], 135, 590)
        if t > T["higher"] - 0.15:
            tag(ctx, 540, 1040, f"{HIGHER} OF {TRADES} TIMES: YES", GOLD, back(prog(t, T["higher"] - 0.15, 0.3)), 46, 0.02, C["ink"])
    bunting(ctx, "THE NEXT MORNING", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["higher"] else "smug") if e != "talk" else e, prop=prop_magnifier)


Q0, Q1 = di("2008-09-29"), di("2008-10-31")
_qs, _qb = di("2008-10-10"), di("2008-10-13")


def s_oct08(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    big_title(ctx, "OCTOBER 2008", W / 2, 490, 130, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
    k = ease_io(prog(t, s0 + 0.2, max(0.5, T["Monday"] - s0)))
    zoom_chart(ctx, (150, 590, 780, 330), Q0, Q1, k, t, [(_qs, "SELL", LCOL, T["sold2"]), (_qb, "BUY", GRNC, T["paid"])],
               labels=(("SEP 29", "2008-09-29"), ("OCT 10", "2008-10-10"), ("OCT 31", "2008-10-31")))
    if T["Friday"] - 0.1 < t < T["eight2"] - 0.15:
        tag(ctx, 300, 1060, "FRI OPEN: SOLD", LCOL, back(prog(t, T["Friday"] - 0.1, 0.3)), 34, -0.03, C["ink"])
    if T["Monday"] - 0.1 < t < T["eight2"] - 0.15:
        tag(ctx, 780, 1060, "MON OPEN: BOUGHT", GRNC, back(prog(t, T["Monday"] - 0.1, 0.3)), 34, 0.03, C["ink"])
    if t > T["eight2"] - 0.1:
        pp = back(prog(t, T["eight2"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1040); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "PAID +8% MORE", 0, 0, 110, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "ONE WEEKEND", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("shock" if t > T["paid"] else "smug") if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"ZERO FEES: {money(_R['fees']['0'])} · 6 TRIGGERS (-0.5% TO -3%): ALL LOST"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "B · JUST HOLD", money(HOLD_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "A · SIT OUT RED MORNINGS (0.05% FEES)", money(RULE_V), LCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 470, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["ZERO FEES? STILL LOST."], W / 2, 470, T["Even"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    stamp_box(ctx, ["RED MORNINGS DON'T HURT.", "LEAVING DOES."], W / 2 + 10, 690, T["Red2"] - 0.1, t, C["red"], 900, 66, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["Leaving"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 862); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #27", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules, "crash": s_crash,
            "flip": s_flip, "remember": s_remember, "oct08": s_oct08, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #27 overrides (only buy red days?)
LCOL = (0xFF, 0x6B, 0x6B)   # B: RED-DAY BUYER
RBOX = (110, 640, 860, 300)


def hud(ctx, t):
    a = ease(prog(t, SC["question"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #27", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 600, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 615, 38, 340, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 785, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 615, 38, 340, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(A_V), 785, 78, fit(ctx, money(A_V), 36, 320, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["Paydays"] - SC["question"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def tug(ctx, t, up, y=1035, a=1.0):
    """who's ahead? knot moves toward the leader (scale +-$600, no numbers)"""
    d = (BV[up] - AV[up]) / 600.0
    d = max(-1, min(1, d))
    rect(ctx, 190, y - 6, 700, 12, C["white"], 0.35 * a)
    card(ctx, 110, y - 34, 76, 68, HCOL, a, 14, shadow=False, border=C["ink"]); text(ctx, "A", 148, y + 22, 54, C["ink"], a, HEAD, True, "center")
    card(ctx, 894, y - 34, 76, 68, LCOL, a, 14, shadow=False, border=C["ink"]); text(ctx, "B", 932, y + 22, 54, C["ink"], a, HEAD, True, "center")
    kx = 540 + d * 330
    ctx.new_path(); ctx.arc(kx, y, 24 + 3 * math.sin(t * 8), 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()
    text(ctx, "WHO'S AHEAD?", 540, y - 40, 26, C["white"], 0.85 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2007, 2009, 2011), show_tug=True):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 25, up)
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), S0, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(8000.0, 1.15 * float(max(np.nanmax(AV[S0:hi]), np.nanmax(BV[S0:hi]))))
    xs, ys = series_xy(PUT, S0, xe, up, RBOX, 0, vmax, 3)
    for j in range(0, len(xs) - 1, 2):
        poly(ctx, xs[j:j + 2], ys[j:j + 2], C["white"], 3, 0.45 * a)
    tips = []
    for arr, col, wdt in ((AV, HCOL, 10), (BV, LCOL, 5)):
        xs, ys = series_xy(arr, S0, xe, up, RBOX, 0, vmax, 3)
        poly(ctx, xs, ys, col, wdt, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (ax, ay), (bx2, by2) = tips
    mini_rocco(ctx, ax - 18, ay - 4, 4, "tophat", t, "smug", False, True)
    mini_rocco(ctx, bx2 + 18, by2 - 4 + 0, 4, "detective", t, "neutral", True, True)
    if curtain is not None:
        xc = sx_of(curtain, S0, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("A · BUYS RIGHT AWAY", HCOL), ("B · WAITS FOR RED", LCOL))):
        rect(ctx, bx + 20, by + 18 + k * 34, 30, 10, col)
        text(ctx, lab, bx + 60, by + 30 + k * 34, 24, col, 1, MONO, True, "left")
    text(ctx, "- - MONEY PUT IN", bx + bw - 20, by + bh - 20, 22, C["white"], 0.6, MONO, True, "right")
    if show_tug:
        tug(ctx, t, up, 1095, a)


XE1 = di("2009-12-31"); XE2 = di("2017-08-31")


def red_candle_big(ctx, x, y, s, t, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    candle(ctx, -50, -120, 100, 240, REDC, a, 60)
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: BUY ONLY / RED DAYS?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x14), (0x08, 0x02, 0x06))
    god_rays(ctx, W / 2, 620, t, 0.09, REDC, 14, 1400)
    for k in range(24):
        u = ((t * 0.25) + k / 24) % 1
        cx = (k * 211) % W
        red_candle_big(ctx, cx, u * 1600 - 100, 0.25, t, 0.22)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 520); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "BUY ONLY", 0, 0, 220, C["white"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 770); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "RED DAYS?", 0, 0, 230, REDC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    if show_tag:
        tag(ctx, 540, 200, "EVERYONE'S RULE · TESTED FOR 20 YEARS", C["cream"], p, 38, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


def coin_stack(ctx, x, y, n, t, a=1.0, col=GOLD):
    for k in range(n):
        yy = y - k * 26
        ctx.save(); ctx.translate(x, yy); ctx.scale(1, 0.38)
        ctx.new_path(); ctx.arc(0, 0, 60, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(10); ctx.stroke(); ctx.restore()
        rect(ctx, x - 60, yy, 120, 12, (0xC8, 0x90, 0x20), a)


def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x24, 0x20), (0x03, 0x08, 0x06))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    big_title(ctx, "TWO INVESTORS", W / 2, 500, 140, C["white"], back(prog(t, s0 + 0.02, 0.3)), 980, -0.03, 16)
    big_title(ctx, "$500 A MONTH", W / 2, 680, 150, GOLD, back(prog(t, T["five1"] - 0.15, 0.3)), 980, 0.02, 16)
    n = int(clamp((t - T["five1"]) / 1.2) * 5)
    if n > 0:
        coin_stack(ctx, 300, 1000, n, t); coin_stack(ctx, 780, 1000, n, t)
    bunting(ctx, "THE BET", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "BUYS", "RIGHT AWAY", HCOL, -230, ta), ("B", "WAITS FOR", "A -1% DAY", LCOL, 230, tb))):
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


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 25), (SC["y2008"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"], T["B"], 420, T["Who"])
    rc = ease(prog(t, T["B"] + 0.3, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, show_tug=False); ctx.restore()
    sticker(ctx, t, T["Who"], T["Who"] + 2.6, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE QUIET YEAR"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "YEAR: ???? · RED DAYS: ??", 0, 42, 36, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "THE ANSWER HIDES...", W / 2, 425, 96, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["quiet1"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 535); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, show_tug=False)
    sticker(ctx, t, T["Who"], T["Who"] + 2.6, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("SAME $500", "EVERY MONTH", GOLD, 290, T["paychecks"]),
                                                 ("ONLY CHANGE", "THE BUY DAY", GRNC, 790, T["buying1"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, -12, fit(ctx, title, 56, 420), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 62, fit(ctx, l1, 60, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["ahead"] + 0.3, di("2008-12-31")), (T["barely"] + 0.4, di("2009-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "2008: RED DAYS EVERYWHERE", C["red"], back(prog(t, T["everywhere"] - 0.3, 0.3)), 42, -0.02, C["white"])
    if t > T["ahead"] - 0.15:
        tag(ctx, 540, 530, "B PULLS AHEAD" if t < T["barely"] - 0.1 else "...BY A HAIR", LCOL, back(prog(t, T["ahead"] - 0.15, 0.3)), 42, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("smug" if t > T["ahead"] else "shock") if e != "talk" else e)


def s_calm(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x36), (0x03, 0x08, 0x10))
    sun(ctx, 920, 330, 50, t, 0.8)
    for k in range(5):
        cloud(ctx, ((t * 40 + k * 260) % 1300) - 150, 260 + k * 20, 0.8, a=0.5)
    pts = [(s0 + 0.1, di("2009-12-31")), (T["waits3"] + 0.3, di("2017-08-31"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE2, curtain=up + 1, years=(2006, 2009, 2012, 2015))
    tag(ctx, 540, 440, "THE MARKET CALMS DOWN", GRNC, back(prog(t, T["calms"] - 0.15, 0.3)), 44, -0.03, C["ink"])
    if t > T["waits2"] - 0.15:
        tag(ctx, 470, 530, "B WAITS..." if t < T["waits3"] - 0.1 else "B WAITS... AND WAITS", GOLD, back(prog(t, T["waits2"] - 0.15, 0.3)), 42, 0.02, C["ink"])
        hourglass(ctx, 930, 530, 0.3, t)
    bunting(ctx, "THE CALM YEARS", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if e != "talk" else e)


def cal_2017(ctx, t, t0, x0, y0, a=1.0):
    """12 month cells; the 4 real days down >= 1% in 2017 drop in as red pins"""
    ms = "JFMAMJJASOND"
    for m in range(12):
        cx = x0 + (m % 6) * 140; cy = y0 + (m // 6) * 170
        pk = back(prog(t, t0 + m * 0.05, 0.3))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(cx + 60, cy + 70); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -60, -70, 120, 140, C["cream"], a, 12, shadow=False, border=C["ink"])
        rect(ctx, -60, -70, 120, 34, GRNC, a)
        text(ctx, ms[m], 0, -42, 30, C["ink"], a, HEAD, True, "center")
        ctx.restore()
    for k, i in enumerate(RED17):
        d = DATES[i]; m = d.month - 1
        cx = x0 + (m % 6) * 140 + 60 + (d.day - 15) * 2.4; cy = y0 + (m // 6) * 170 + 90
        pk = back(prog(t, T["four1"] - 0.2 + k * 0.15, 0.3))
        if pk > 0:
            ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            candle(ctx, -14, -26, 28, 52, REDC, a, 14); ctx.restore()


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["Two3"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT QUIET YEAR?", W / 2, 680, 110, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    else:
        big_title(ctx, "2017", W / 2, 520, 150, C["white"], back(prog(t, T["Two3"] - 0.1, 0.3)), 900, -0.02, 16)
        cal_2017(ctx, t, T["Two3"], 130, 600)
        if t > T["four1"] - 0.15:
            tag(ctx, 540, 1040, "ONLY 4 DAYS DOWN 1%+ ALL YEAR", C["red"], back(prog(t, T["four1"] - 0.15, 0.3)), 42, 0.02, C["white"])
    bunting(ctx, "THE QUIET YEAR", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["four1"] else "smug") if e != "talk" else e, prop=prop_magnifier)


Q0, Q1 = di("2017-08-01"), di("2018-02-28")


def s_sept(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x06), (0x0C, 0x06, 0x02))
    big_title(ctx, "SEPT 2017 MONEY", W / 2, 480, 120, GOLD, back(prog(t, s0 + 0.03, 0.3)), 980, -0.03, 14)
    k = ease_io(prog(t, s0 + 0.2, max(0.5, T["bought"] - s0)))
    zoom_chart(ctx, (150, 580, 780, 300), Q0, Q1, k, t, [(_sep, "A BUYS", HCOL, s0 + 0.4), (_buy, "B BUYS", LCOL, T["bought"])],
               labels=(("AUG 17", "2017-08-01"), ("NOV", "2017-11-01"), ("FEB 18", "2018-02-01")))
    nm = int(clamp((t - T["cash"]) / max(0.3, T["months"] - T["cash"])) * 5)
    if T["cash"] - 0.1 < t < T["fifteen"] - 0.15:
        coin_stack(ctx, 900, 1110, max(1, nm), t)
        tag(ctx, 430, 1060, f"IN CASH: {max(1, nm)} MONTH{'S' if nm > 1 else ''}", GOLD, back(prog(t, T["cash"] - 0.1, 0.3)), 44, -0.02, C["ink"])
    if t > T["fifteen"] - 0.1:
        pp = back(prog(t, T["fifteen"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1050); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "BOUGHT +15% HIGHER", 0, 0, 100, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "FIVE MONTHS", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("shock" if t > T["fifteen"] else "neutral") if e != "talk" else e, prop=prop_flag)


def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"GAP {money(GAP)} · ANY RED DAY: {money(_R['scan']['0.0'])} · -2% DAYS: {money(_R['scan']['-0.02'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$500 A MONTH · $120,000 PUT IN · 2005-2024", W / 2, 420, 30, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · BUYS RIGHT AWAY", money(A_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · WAITS FOR A -1% DAY", money(B_V), LCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 470, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["RED DAYS DON'T BUILD WEALTH."], W / 2, 470, T["Red"] - 0.05, t, STAMP_OR, 900, 62, -0.05)
    stamp_box(ctx, ["PAYDAYS DO."], W / 2 + 10, 660, T["Paydays"] - 0.1, t, STAMP_GR, 760, 90, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["Paydays"] + 0.2, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #28", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules, "y2008": s_y2008,
            "calm": s_calm, "remember": s_remember, "sept": s_sept, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #30 overrides (catch the falling knife or wait for green?)
ACOL = (0xFF, 0x8A, 0x3D)   # A: buys right away (the knife)
BCOL = (0x22, 0xE5, 0x8B)   # B: waits for green
HCOL = ACOL; LCOL = BCOL
RBOX = (110, 640, 860, 300)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #30", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 600, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 615, 38, 340, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 785, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 615, 38, 340, 54, ACOL, a, 8, shadow=False)
        text(ctx, money(A_V), 785, 78, fit(ctx, money(A_V), 36, 320, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["cost"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2007, 2009, 2011), show_tug=False):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 25, up)
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), S0, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(3000.0, 1.15 * float(max(np.nanmax(AV[S0:hi]), np.nanmax(BV[S0:hi]))))
    xs, ys = series_xy(PUT, S0, xe, up, RBOX, 0, vmax, 3)
    for j in range(0, len(xs) - 1, 2):
        poly(ctx, xs[j:j + 2], ys[j:j + 2], C["white"], 3, 0.45 * a)
    tips = []
    for arr, col, wdt in ((AV, ACOL, 10), (BV, BCOL, 5)):
        xs, ys = series_xy(arr, S0, xe, up, RBOX, 0, vmax, 3)
        poly(ctx, xs, ys, col, wdt, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (ax, ay), (bx2, by2) = tips
    mini_rocco(ctx, ax - 18, ay - 4, 4, "fire", t, "shock", False, True)
    mini_rocco(ctx, bx2 + 18, by2 - 4 + 0, 4, "detective", t, "neutral", True, True)
    for k, (lab, col) in enumerate((("A · BUYS RIGHT AWAY", ACOL), ("B · WAITS FOR GREEN", BCOL))):
        rect(ctx, bx + 20, by + 18 + k * 34, 30, 10, col)
        text(ctx, lab, bx + 60, by + 30 + k * 34, 24, col, 1, MONO, True, "left")
    text(ctx, "- - MONEY PUT IN", bx + bw - 20, by + bh - 20, 22, C["white"], 0.6, MONO, True, "right")


XE1 = di("2010-12-31"); XE2 = di("2018-11-30")


def knife(ctx, x, y, s, rot, a=1.0):
    """simple kitchen-knife icon: steel blade + wooden handle (generic)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-20, -150); ctx.line_to(22, -150); ctx.line_to(22, 40); ctx.curve_to(10, 10, -10, -60, -20, -150)
    ctx.close_path()
    ctx.new_path(); ctx.move_to(0, -170); ctx.curve_to(30, -120, 26, -40, 24, 40); ctx.line_to(-22, 40); ctx.line_to(-22, -110)
    ctx.curve_to(-20, -140, -10, -160, 0, -170); ctx.close_path()
    ctx.set_source_rgba(0.86, 0.9, 0.95, a); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke()
    rect(ctx, -6, -150, 6, 180, C["white"], 0.6 * a)
    card(ctx, -28, 40, 56, 120, (0x8A, 0x55, 0x2E), a, 12, shadow=False, border=C["ink"])
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: S&P: 4 RED DAYS / BUY NOW?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x14), (0x08, 0x02, 0x06))
    god_rays(ctx, W / 2, 620, t, 0.09, REDC, 14, 1400)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    # four falling red candles, stepping down
    for k in range(4):
        cy = 880 + k * 70 + math.sin(t * 3 + k) * 6
        candle(ctx, 150 + k * 110, cy - 60, 70, 130, REDC, 1, 30)
    # falling knife on the right
    knife(ctx, 900, 820 + ((t * 0.0) % 1) + math.sin(t * 5) * 14, 0.9, 3.0 + math.sin(t * 2) * 0.08, 1)
    ctx.save(); ctx.translate(540 + shake, 330); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "S&P: 4 RED DAYS", 0, 0, fit(ctx, "S&P: 4 RED DAYS", 170, 1000), C["white"], 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 560); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "BUY NOW?", 0, 0, 230, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "BUY", "NOW", ACOL, -230, ta), ("B", "WAIT FOR", "GREEN", BCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -135, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, -12, fit(ctx, l1, 60, 250), C["ink"], 1, HEAD, True, "center")
        text(ctx, l2, 60, 56, fit(ctx, l2, 64, 250), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B1"], S0 + 25), (SC["years"], XE1)])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A1"], T["B1"], 420, T["B1"] + 0.4)
    rc = ease(prog(t, T["B1"] + 0.1, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B1"] + 0.2, T["B1"] + 2.9, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B1"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE WEEK"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "MONTH: ??? · YEAR: ????", 0, 42, 36, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE WEEK DECIDES IT", W / 2, 425, 96, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["October1"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 535); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["B1"] + 0.2, T["B1"] + 2.9, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 330, "$1,000 AFTER EVERY 4 RED DAYS IN A ROW", GOLD, back(prog(t, T["thousand1"] - 0.15, 0.3)), 34, -0.02, C["ink"])
    for k, (title, l1, col, x, tt) in enumerate((("A BUYS", "NEXT MORNING", ACOL, 290, T["A2"]),
                                                 ("B WAITS", "FOR A GREEN DAY", BCOL, 790, T["B2"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 475); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -95, 470, 190, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, -10, fit(ctx, title, 64, 420), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 58, fit(ctx, l1, 50, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def s_years(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x36), (0x03, 0x08, 0x10))
    sun(ctx, 920, 330, 50, t, 0.8)
    pts = [(s0 + 0.1, XE1), (s1 - 0.2, XE2)]
    race_chart(ctx, t, race_idx(t, pts), XE2, years=(2006, 2009, 2012, 2015, 2018))
    tag(ctx, 540, 440, "NECK AND NECK", GOLD, back(prog(t, T["neck"] - 0.2, 0.3)), 52, -0.03, C["ink"])
    bunting(ctx, "THE YEARS", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "neutral" if e != "talk" else e, prop=prop_flag)


def candle_zoom(ctx, box, i0, i1, k, t, marks, a=1.0, labels=(), hl=None):
    """daily candles (adj OHLC) for a short window; marks = (idx, label, col, t_show) at the OPEN"""
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    lo = float(min(OP[i0:i1 + 1].min(), CL[i0:i1 + 1].min())) * 0.97; hi_ = float(max(OP[i0:i1 + 1].max(), CL[i0:i1 + 1].max())) * 1.03
    n = i1 - i0 + 1; cw = bw / n
    up = int(i0 + (n - 1) * clamp(k))
    yv = lambda v: by + bh - (v - lo) / (hi_ - lo) * bh
    for i in range(i0, up + 1):
        o, c = OP[i], CL[i]
        col = GRNC if CL[i] >= CL[i - 1] else REDC
        x = bx + (i - i0) * cw + cw * 0.18
        y0, y1 = yv(max(o, c)), yv(min(o, c))
        glow_ = (hl is not None and i == hl)
        if glow_:
            rect(ctx, x - 8, by - 10, cw * 0.64 + 16, bh + 20, GRNC, 0.18 + 0.1 * math.sin(t * 8))
        card(ctx, x, y0, cw * 0.64, max(6, y1 - y0), col, a, 6, shadow=False, border=C["ink"])
    for mi, lab, col, tt in marks:
        if i0 <= mi <= up and t >= tt:
            sx = bx + (mi - i0) * cw + cw * 0.5; sy = yv(OP[mi])
            pp = back(prog(t, tt, 0.3))
            ctx.save(); ctx.translate(sx, sy + 70); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            card(ctx, -66, -26, 132, 52, col, 1, 10, border=C["ink"]); text(ctx, lab, 0, 12, 30, C["ink"], 1, HEAD, True, "center")
            ctx.restore()
            rect(ctx, sx - 36, sy - 3, 72, 6, col, 1)
    for lab, d in labels:
        text(ctx, lab, bx + (di(d) - i0) * cw + cw * 0.5, by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")


X0, X1 = di("2018-12-12"), di("2019-01-04")


def s_xmas(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x18), (0x02, 0x06, 0x04))
    stars(ctx, t, 50, 160, 1150, 9, 0.6)
    big_title(ctx, "CHRISTMAS 2018", W / 2, 470, 120, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.03, 14)
    k = ease_io(prog(t, s0 + 0.2, max(0.5, T["cheaper"] - s0)))
    candle_zoom(ctx, (130, 570, 820, 330), X0, X1, k, t, [(K18, "A BUYS", ACOL, T["A3"]), (W18, "B BUYS", BCOL, T["B3"] + 0.3)],
                labels=(("DEC 12", "2018-12-12"), ("DEC 24", "2018-12-24"), ("JAN 4", "2019-01-04")))
    if t > T["cheaper"] - 0.4:
        pp = back(prog(t, T["cheaper"] - 0.4, 0.35))
        ctx.save(); ctx.translate(540, 1045); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "B PAYS 4% LESS", 0, 0, 104, GRNC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "THE KNIFE", t, s0, [C["red"], C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("smug" if t > T["cheaper"] else "shock") if e != "talk" else e, prop=prop_coin)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["So"] + 0.0 or t < s0:
        pass
    if t < T["pays"] + 0.3 and t >= SC["remember"] and False:
        pass
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "THAT OCTOBER", W / 2, 500, 150, GOLD, r, 960, 0, 16)
    big_title(ctx, "WEEK...", W / 2, 660, 130, C["white"], r, 980, 0, 14)
    if t > T["Two2"] - 0.15:
        pk = back(prog(t, T["Two2"] - 0.15, 0.35))
        ctx.save(); ctx.translate(540, 880); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, "2008", 0, 0, 240, REDC, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
        ctx.restore()
    else:
        evidence(ctx, 540, 880, t, ease(prog(t, s0 + 0.2, 0.3)))
    bunting(ctx, "THE WEEK", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["Two2"] else "smug") if e != "talk" else e, prop=prop_magnifier)


Q0, Q1 = di("2008-10-03"), di("2008-10-17")


def s_oct08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    k = ease_io(prog(t, s0 + 0.1, max(0.5, T["Green"] + 0.3 - s0)))
    hl = ROCKET if t > T["Green"] - 0.1 else None
    candle_zoom(ctx, (130, 520, 820, 380), Q0, Q1, k, t, [(K08, "A BUYS", ACOL, T["A4"]), (W08, "B BUYS", BCOL, T["B5"])],
                labels=(("OCT 3", "2008-10-03"), ("OCT 10", "2008-10-10"), ("OCT 17", "2008-10-17")), hl=hl)
    if T["three"] - 0.15 < t < T["Green"] - 0.15:
        tag(ctx, 540, 450, "3 MORE RED DAYS", C["red"], back(prog(t, T["three"] - 0.15, 0.3)), 48, -0.02, C["white"])
    if T["Green"] - 0.15 < t < T["B5"] - 0.1:
        tag(ctx, 540, 450, "+14.5% · BIGGEST DAY IN 20 YEARS", GRNC, back(prog(t, T["Green"] - 0.15, 0.3)), 38, -0.02, C["ink"])
    if t > T["B5"] - 0.1:
        tag(ctx, 540, 450, "B BUYS THE NEXT MORNING", BCOL, back(prog(t, T["B5"] - 0.1, 0.3)), 42, -0.02, C["ink"])
    if t > T["seven"] - 0.1:
        pp = back(prog(t, T["seven"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1060); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "B PAYS 7% MORE", 0, 0, 104, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    bunting(ctx, "OCTOBER 2008", t, s0, [C["red"], C["ink"], GRNC, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("shock" if t > T["Green"] else "sad") if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=ACOL)
        s_ = f"B PAID MORE 70/107 TIMES · 3 RED DAYS: A +{money(SCAN3[0] - SCAN3[1])} · 5: A +{money(SCAN5[0] - SCAN5[1])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "107 STREAKS · $107,000 PUT IN EACH · 2005-2024", W / 2, 420, 30, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "B · WAITS FOR GREEN", money(B_V), BCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "A · BUYS RIGHT AWAY", money(A_V), ACOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["WAITING FELT SAFER."], W / 2, 470, T["Waiting"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    stamp_box(ctx, ["IT JUST COST MORE."], W / 2 + 10, 660, T["cost"] - 0.1, t, STAMP_GR, 820, 74, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["cost"] + 0.2, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #31", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "rules": s_rules, "years": s_years, "xmas": s_xmas,
            "remember": s_remember, "oct08": s_oct08, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #31 overrides (check the 200-day line monthly, or never?)
ACOL = (0xB3, 0x8C, 0xFF)   # A: monthly checker
BCOL = (0x4F, 0xC3, 0xF7)   # B: never checks (buy & hold)
DCOL = (0x9A, 0xA0, 0xA6)   # ghost: daily checker
HCOL = ACOL; LCOL = BCOL


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #31", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 600, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 615, 38, 340, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 785, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 615, 38, 340, 54, BCOL, a, 8, shadow=False)
        text(ctx, money(B_V), 785, 78, fit(ctx, money(B_V), 36, 320, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["both"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2006, 2008, 2010), show_tug=False, ghost=False):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 25, up)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), S0, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = 1.15 * float(max(np.nanmax(AV[S0:hi]), np.nanmax(BV[S0:hi])))
    xs, ys = series_xy(PUT, S0, xe, up, RBOX, 0, vmax, 3)
    for j in range(0, len(xs) - 1, 2):
        poly(ctx, xs[j:j + 2], ys[j:j + 2], C["white"], 3, 0.45 * a)
    if ghost:
        xs, ys = series_xy(DV, S0, xe, up, RBOX, 0, vmax, 3)
        poly(ctx, xs, ys, DCOL, 4, 0.6 * a)
    tips = []
    for arr, col, wdt in ((AV, ACOL, 9), (BV, BCOL, 6)):
        xs, ys = series_xy(arr, S0, xe, up, RBOX, 0, vmax, 3)
        poly(ctx, xs, ys, col, wdt, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (ax, ay), (bx2, by2) = tips
    mini_rocco(ctx, ax - 18, ay - 4, 4, "detective", t, "smug", False, True)
    mini_rocco(ctx, bx2 + 18, by2 - 4, 4, "night", t, "sleep", True, True)
    if curtain is not None:
        xc = sx_of(up, S0, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    labs = [("A · CHECKS MONTHLY", ACOL), ("B · NEVER CHECKS", BCOL)] + ([("DAILY CHECKER", DCOL)] if ghost else [])
    for k, (lab, col) in enumerate(labs):
        rect(ctx, bx + 20, by + 18 + k * 34, 30, 10, col)
        text(ctx, lab, bx + 60, by + 30 + k * 34, 24, col, 1, MONO, True, "left")
    text(ctx, "- - $10,000 START", bx + bw - 20, by + bh - 20, 22, C["white"], 0.6, MONO, True, "right")


XE1 = di("2010-06-30"); XE2 = di("2019-12-31")


# ---------------------------------------------------------------- 1 hook (frame 0: 64 TRADES / ONE RULE)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x1E, 0x10, 0x3A), (0x06, 0x03, 0x10))
    god_rays(ctx, W / 2, 620, t, 0.09, ACOL, 14, 1400)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    # 64 trade chips, flickering buy/sell
    for k in range(64):
        cx = 175 + (k % 16) * 49; cy = 740 + (k // 16) * 52
        on = (int(t * 6 + k * 1.7) % 3) == 0
        card(ctx, cx - 19, cy - 19, 38, 38, GRNC if (k % 2 == 0) ^ on else C["red"], 0.95, 8, shadow=False, border=C["ink"])
    ctx.save(); ctx.translate(540 + shake, 360); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "64 TRADES", 0, 0, 250, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 570); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "ONE RULE", 0, 0, 170, C["white"], 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "CHECK", "MONTHLY", ACOL, -230, ta), ("B", "NEVER", "CHECK", BCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -135, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, -12, fit(ctx, l1, 60, 250), C["ink"], 1, HEAD, True, "center")
        text(ctx, l2, 60, 56, fit(ctx, l2, 60, 250), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B1"], S0 + 25), (SC["y2008"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A1"], T["B1"], 420, T["B1"] + 0.4)
    rc = ease(prog(t, T["B1"] + 0.1, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B1"] + 0.2, T["B1"] + 2.9, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B1"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE CHOPPY YEAR"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "YEAR: ???? · TRADES: ??", 0, 42, 36, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE YEAR SETTLES IT", W / 2, 425, 96, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["choppy1"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 535); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["B1"] + 0.2, T["B1"] + 2.9, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 330, "THE 200-DAY AVERAGE RULE", GOLD, back(prog(t, T["twohundred"] - 0.15, 0.3)), 38, -0.02, C["ink"])
    for k, (title, l1, col, x, tt) in enumerate((("ABOVE THE LINE", "OWN THE S&P", GRNC, 290, T["own"]),
                                                 ("BELOW THE LINE", "SIT IN CASH", C["red"], 790, T["cash"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 475); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -95, 470, 190, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, -10, fit(ctx, title, 52, 420), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 58, fit(ctx, l1, 56, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def barcode(ctx, x, y, w, h, arr, i0, i1, col, a=1.0, k=1.0):
    n = i1 - i0; up = int(i0 + n * clamp(k))
    rect(ctx, x, y, w, h, (0xD8, 0xDC, 0xE0), 0.25 * a)
    step_ = max(1, n // 400)
    for i in range(i0, up, step_):
        if arr[i] == 1:
            rect(ctx, x + (i - i0) / n * w, y, w / n * step_ + 0.6, h, col, a)


def s_daily(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x18), (0x0A, 0x03, 0x06))
    for k in range(18):
        u = ((t * 0.4) + k / 18) % 1
        rect(ctx, (k * 157) % W, u * 1700, 3, 40, C["red"], 0.15)
    i0, i1 = S0, N - 1
    kd = ease_io(prog(t, T["Checked1"], 1.2))
    km = ease_io(prog(t, T["Checked2"], 1.0))
    big_title(ctx, "CHECKED EVERY DAY", W / 2, 430, 92, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    card(ctx, 90, 500, 900, 470, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    text(ctx, "DAILY · IN THE MARKET:", 130, 560, 30, DCOL, 1, MONO, True, "left")
    barcode(ctx, 130, 580, 820, 90, IND, i0, i1, DCOL, 1, kd)
    if t > T["faked"] - 0.15:
        tag(ctx, 760, 560, "64 TRADES · 41 FAKE-OUTS", C["red"], back(prog(t, T["faked"] - 0.15, 0.3)), 30, 0.02, C["white"])
    if t > T["Checked2"] - 0.15:
        text(ctx, "MONTHLY · IN THE MARKET:", 130, 760, 30, ACOL, 1, MONO, True, "left")
        barcode(ctx, 130, 780, 820, 90, INM, i0, i1, ACOL, 1, km)
    if t > T["calms"] - 0.15:
        tag(ctx, 760, 760, "12 TRADES", ACOL, back(prog(t, T["calms"] - 0.15, 0.3)), 34, 0.02, C["ink"])
    for yr in (2006, 2010, 2015, 2020, 2024):
        text(ctx, str(yr), 130 + (di(f"{yr}-01-01") - i0) / (i1 - i0) * 820, 920, 24, C["white"], 0.7, MONO, True, "center")
    bunting(ctx, "DAY VS MONTH", t, s0, [C["red"], C["ink"], ACOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("smug" if t > T["calms"] else "shock") if e != "talk" else e, prop=prop_flag)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["crash"] + 0.3, di("2008-10-31")), (T["twice"] + 0.2, LOW09), (s1 - 0.1, XE1)]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "A SELLS: JANUARY 2008", ACOL, back(prog(t, T["sells"] - 0.15, 0.3)), 42, -0.02, C["ink"])
    if t > T["twice"] - 0.15:
        tag(ctx, 540, 530, "AT THE BOTTOM: 2X THE HOLDER", GOLD, back(prog(t, T["twice"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], ACOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("smug" if t > T["twice"] else "shock") if e != "talk" else e)


def s_decade(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x36), (0x03, 0x08, 0x10))
    sun(ctx, 920, 330, 50, t, 0.8)
    pts = [(s0 + 0.1, XE1), (T["ahead"] + 0.2, di("2019-06-30"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE2, curtain=True, years=(2006, 2010, 2014, 2018))
    tag(ctx, 540, 440, "10 YEARS LATER: STILL AHEAD", ACOL, back(prog(t, T["ahead"] - 0.3, 0.3)), 42, -0.03, C["ink"])
    if t > T["So"] - 0.15:
        tag(ctx, 540, 530, "SO CHECKING LESS WINS?", GOLD, back(prog(t, T["So"] - 0.15, 0.3)), 42, 0.02, C["ink"])
    bunting(ctx, "THE LEAD", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "REMEMBER", W / 2, 500, 170, GOLD, r, 960, 0, 16)
    big_title(ctx, "THAT CHOPPY YEAR?", W / 2, 660, 106, C["white"], r, 980, 0, 14)
    if t > T["Twenty"] - 0.15:
        pk = back(prog(t, T["Twenty"] - 0.15, 0.35))
        ctx.save(); ctx.translate(540, 880); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, "2022", 0, 0, 240, C["red"], 1, HEAD, True, "center", outline=22, ocol=C["ink"])
        ctx.restore()
    else:
        evidence(ctx, 540, 880, t, ease(prog(t, s0 + 0.2, 0.3)))
    bunting(ctx, "THE CHOPPY YEAR", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["Twenty"] else "smug") if e != "talk" else e, prop=prop_magnifier)


Q0, Q1 = di("2022-01-03"), di("2023-02-28")


def s_y2022(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x18), (0x0A, 0x03, 0x06))
    k = ease_io(prog(t, s0 + 0.1, max(0.5, T["loses2"] + 0.4 - s0)))
    (b1, s1_), (b2, s2_) = T22
    zoom_chart(ctx, (150, 560, 780, 330), Q0, Q1, k, t,
               [(b1, "BUY", ACOL, T["buys"]), (s1_, "SELL", C["red"], T["sells2"]), (b2, "BUY", ACOL, T["Buys"]), (s2_, "SELL", C["red"], T["loses2"])],
               labels=(("JAN 22", "2022-01-03"), ("JUL", "2022-07-01"), ("JAN 23", "2023-01-03")))
    if T["nine"] - 0.1 < t < T["Buys"] - 0.1:
        pp = back(prog(t, T["nine"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1050); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "-9%", 0, 0, 130, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"]); ctx.restore()
    if T["loses2"] - 0.1 < t < T["holder2"] - 0.1:
        pp = back(prog(t, T["loses2"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1050); ctx.rotate(0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        text(ctx, "-6% AGAIN", 0, 0, 120, C["red"], 1, HEAD, True, "center", outline=14, ocol=C["ink"]); ctx.restore()
    if t > T["holder2"] - 0.1:
        tag(ctx, 540, 1050, "NOV 2022: THE HOLDER PASSES HIM", BCOL, back(prog(t, T["holder2"] - 0.1, 0.3)), 40, -0.02, C["ink"])
    tag(ctx, 540, 470, "A · THE MONTHLY CHECKER IN 2022", ACOL, back(prog(t, s0 + 0.05, 0.3)), 34, -0.02, C["ink"])
    bunting(ctx, "2022", t, s0, [C["red"], C["ink"], ACOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=ACOL)
        s_ = f"SAME RULE CHECKED DAILY: {money(D_V)} · WEEKLY: {money(WK_V)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · OCT 2005 - DEC 2024 · FEES INCLUDED", W / 2, 420, 30, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · CHECKS MONTHLY", money(A_V), ACOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · NEVER CHECKS", money(B_V), BCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.82)
    stamp_box(ctx, ["MONTHLY BEAT DAILY."], W / 2, 470, T["Monthly"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    stamp_box(ctx, ["NEVER CHECKING BEAT BOTH."], W / 2 + 10, 660, T["Never2"] - 0.1, t, STAMP_GR, 900, 62, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["both"] + 0.2, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #32", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "rules": s_rules, "daily": s_daily, "y2008": s_y2008,
            "decade": s_decade, "remember": s_remember, "y2022": s_y2022, "score": s_score, "verdict": s_verdict, "loop": s_loop}
