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
    for k, (lab, col) in enumerate((("A · SITS OUT", LCOL), ("B · SITS TIGHT", HCOL))):
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


# ================================================================ #28 overrides (after a -2% day: sell, or hold?)
LCOL = (0xFF, 0x8A, 0x3D)   # THE 2% SELLER (orange)


def hud(ctx, t):
    a = ease(prog(t, SC["question"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #28", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["thirty"] - SC["question"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2007, 2009, 2011), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, up)
    if curtain is not None:
        up = min(up, curtain)
    i = s0_   # orange cash bands
    while i <= min(up, xe):
        if not INN[i]:
            j = i
            while j <= min(up, xe) and not INN[j]:
                j += 1
            xa = sx_of(i, s0_, xe, RBOX); xb = sx_of(j, s0_, xe, RBOX)
            rect(ctx, xa, by, max(2, xb - xa), bh, LCOL, 0.22 * a)
            i = j
        i += 1
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(RV[s0_:hi]), np.nanmax(BV[s0_:hi]))))
    vmin = 5000.0 if x0 is None else 0.8 * float(min(np.nanmin(RV[s0_:hi]), np.nanmin(BV[s0_:hi])))
    if x0 is None:
        yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
        for j in range(22):
            rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    tips = []
    for arr, col in ((BV, HCOL), (RV, LCOL)):
        xs, ys = series_xy(arr, s0_, xe, up, RBOX, vmin, vmax, 3 if x0 is None else 1)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (lx, ly) = tips
    lead_l = RV[up] > BV[up] + 1
    off = 0 if abs(hy - ly) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_l else 0), 4, "tophat", t, "sad" if lead_l else "smug", False, True)
    mini_rocco(ctx, lx, ly - 4 - (0 if lead_l else off), 4, "fire", t, "smug" if lead_l else "sad", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("A · BUYS THE FEAR", LCOL), ("B · JUST HOLDS", HCOL))):
        rect(ctx, bx + bw - 350, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 310, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + bh - 40, 30, 18, LCOL, 0.35)
    text(ctx, "= IN CASH", bx + 60, by + bh - 24, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = N - 1


def bolt(ctx, x, y, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.new_path()
    for px_, py_ in ((10, -100), (-40, 10), (0, 10), (-20, 100), (50, -20), (10, -20), (30, -100)):
        ctx.line_to(px_, py_)
    ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke(); ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: -2% DROPS / 65% / STRIKE AGAIN)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x18), (0x06, 0x02, 0x08))
    god_rays(ctx, W / 2, 600, t, 0.08, REDC, 14, 1400)
    for k in range(34):   # rain
        u = ((t * 0.9) + k / 34) % 1
        rect(ctx, (k * 131) % W, u * 1700 - 100, 4, 46, (0xC0, 0xC8, 0xFF), 0.16)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 250); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "-2% DROPS:", 0, 0, 120, C["white"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(500 + shake, 610); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "65%", 0, 0, 320, REDC, 1, HEAD, True, "center", outline=26, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 800); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "STRIKE AGAIN", 0, 0, 170, GOLD, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    bolt(ctx, 930, 470 + math.sin(t * 7) * 8, 1.0 * s_, GOLD)
    # picture changes every ~2 s: candle 1 on "drops", bolt + candle 2 on "strike", tag on "within"
    c1 = back(prog(tl, T["drops"] - 0.1, 0.3)); c2 = back(prog(tl, T["strike"] - 0.1, 0.3))
    if c1 > 0:
        ctx.save(); ctx.translate(140, 1085); ctx.scale(max(c1, 1e-3), max(c1, 1e-3)); candle(ctx, -40, -60, 80, 120, REDC, 1, 25)
        text(ctx, "-2%", 0, -100, 50, C["white"], 1, HEAD, True, "center", outline=6, ocol=C["ink"]); ctx.restore()
    if c2 > 0:
        ctx.save(); ctx.translate(300, 1110); ctx.scale(max(c2, 1e-3), max(c2, 1e-3)); candle(ctx, -40, -50, 80, 110, REDC, 1, 25)
        text(ctx, "AGAIN", 0, -90, 44, GOLD, 1, HEAD, True, "center", outline=6, ocol=C["ink"]); ctx.restore()
    if show_tag and tl >= T["within"] - 0.12:
        tag(ctx, 540, 905, "WITHIN 2 WEEKS · SPY 2005-2024", C["cream"], back(prog(tl, T["within"] - 0.12, 0.3)), 34, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "fire", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 Monday came close
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x16, 0x20), (0x0A, 0x04, 0x08))
    big_title(ctx, "MONDAY:", W / 2, 470, 130, C["white"], back(prog(t, s0 + 0.02, 0.3)), 980, -0.03, 14)
    big_title(ctx, "S&P -1.9%", W / 2, 660, 190, REDC, back(prog(t, s0 + 0.1, 0.3)), 1000, 0.02, 20)
    pk = back(prog(t, T["close"] - 0.1, 0.3))
    if pk > 0:
        tag(ctx, 540, 820, "3RD STRAIGHT LOSS · NOV 16", GOLD, pk, 40, -0.02, C["ink"])
    ctx.save(); ctx.translate(540, 1000); s = ease(prog(t, s0 + 0.15, 0.35)) + 1e-3; ctx.scale(s, s)
    for k in range(3):
        candle(ctx, -200 + k * 150, -100 + k * 40, 90, 120 + k * 30, REDC, 1, 30)
    ctx.restore()
    bunting(ctx, "THE NEWS", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "SELL", "THE DROP", LCOL, -230, ta), ("B", "JUST", "HOLD", HCOL, 230, tb))):
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
    ab_cards2(ctx, t, T["A"] - 0.4, T["B"], 420, T["B"] + 0.3)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="10 HIDDEN DAYS"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "?? ?? ?? ?? ?? ?? ?? ?? ?? ??", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "10 DAYS DECIDE IT", W / 2, 425, 96, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["panic"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("A -2% DAY", "SELL", LCOL, 290, T["drop"]),
                                                 ("2 CALM WEEKS", "BUY BACK", GRNC, 790, T["buy"]))):
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
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 6 2008: out again and again
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (s1 - 0.2, di("2008-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: 39 DAYS OF -2% OR WORSE", C["red"], back(prog(t, T["eight"] - 0.15, 0.3)), 40, -0.03, C["white"])
    tag(ctx, 540, 530, "OUT. IN. OUT AGAIN.", LCOL, back(prog(t, T["again2"] - 0.6, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "shock" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 7 the 10 worst days dodged, leads at the 2009 bottom
def day_cards(ctx, t, idxs, t0, x0, y0, col, mark, a=1.0, step=0.12, special=None):
    for k, i in enumerate(idxs):
        cx = x0 + (k % 5) * 176; cy = y0 + (k // 5) * 150
        pk = back(prog(t, t0 + k * step, 0.25))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(cx + 80, cy + 60); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -80, -60, 160, 120, col, a, 14, border=C["ink"])
        d = DATES[i]
        text(ctx, d.strftime("%b %y").upper(), 0, -18, 26, C["ink"], a, MONO, True, "center")
        pct = f"{RR[i] * 100:+.1f}%"
        text(ctx, pct, 0, 26, 40, C["ink"], a, HEAD, True, "center")
        ctx.restore()
    for k, i in enumerate(idxs):
        tm = mark(k)
        if tm is None or t < tm:
            continue
        cx = x0 + (k % 5) * 176 + 80; cy = y0 + (k // 5) * 150 + 60
        pp = back(prog(t, tm, 0.25))
        ctx.save(); ctx.translate(cx, cy + 66); ctx.rotate(-0.08); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        lab, c2 = ("SOLD AM", GOLD) if special == k else ("OUT", C["white"])
        card(ctx, -62, -18, 124, 36, (0x05, 0x05, 0x05), 0.95, 8, shadow=False, border=c2)
        text(ctx, lab, 0, 11, 24, c2, 1, HEAD, True, "center")
        ctx.restore()


def s_dodge(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, u * 1300, 5, 34, (0xFF, 0x90, 0x90), 0.10)
    if t < T["leads"] - 0.3:
        big_title(ctx, "THE 10 WORST DAYS", W / 2, 440, 96, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
        day_cards(ctx, t, WORST, T["ten1"] - 0.1, 100, 530, REDC, lambda k: T["worst"] + 0.15 + k * 0.1)
        if t > T["worst"] + 1.2:
            pk = back(prog(t, T["worst"] + 1.2, 0.3))
            ctx.save(); ctx.translate(540, 1020); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            text(ctx, "DODGED ALL 10", 0, 0, 110, GRNC, 1, HEAD, True, "center", outline=14, ocol=C["ink"]); ctx.restore()
    else:
        pts = [(T["leads"] - 0.3, di("2008-12-31")), (T["five"] + 0.3, di("2009-03-09"))]
        race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
        tag(ctx, 540, 440, "MARCH 2009: THE BOTTOM", C["white"], back(prog(t, T["leads"] - 0.3, 0.3)), 40, -0.03, C["ink"])
        if t > T["five"] - 0.15:
            tag(ctx, 540, 530, f"SELLER LEADS BY +{money(LEAD_V)}", LCOL, back(prog(t, T["five"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2008 - 2009", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 8 2020: one last lead at the bottom
P0, P1 = di("2020-01-02"), di("2020-12-31")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 9, 0.5)
    if t < T["Twenty"] - 0.1:
        big_title(ctx, "SO FEAR WINS?", W / 2, 620, 150, GOLD, back(prog(t, s0 + 0.03, 0.3)), 980, -0.03, 16)
        hourglass(ctx, 540, 900, 0.6, t)
    else:
        big_title(ctx, "2020", W / 2, 470, 130, C["white"], back(prog(t, T["Twenty"] - 0.1, 0.3)), 900, -0.03, 16)
        lo = di("2020-03-23")
        k = ease_io(prog(t, T["Twenty"], max(0.5, T["bottom2"] - T["Twenty"])))
        up = int(P0 + 2 + (lo - P0 - 2) * k)
        box = (150, 570, 780, 330)
        card(ctx, box[0] - 20, box[1] - 20, box[2] + 40, box[3] + 70, (0x0C, 0x10, 0x1C), 0.92, 16, border=C["grey"])
        seg = np.concatenate([RV[P0:P1 + 1], BV[P0:P1 + 1]]); vlo, vhi = float(seg.min()) * 0.95, float(BV[P0:lo + 1].max()) * 1.05
        for arr, col in ((BV, HCOL), (RV, LCOL)):
            xs, ys = series_xy(arr, P0, P1, up, box, vlo, vhi, 1)
            poly(ctx, xs, ys, col, 7, 1, glow=True)
        for lab, d in (("JAN", "2020-01-02"), ("MAR 23", "2020-03-23"), ("JUL", "2020-07-01"), ("DEC", "2020-12-31")):
            text(ctx, lab, sx_of(di(d), P0, P1, box), box[1] + box[3] + 40, 24, C["white"], 0.7, MONO, True, "center")
        if t > T["lead"] - 0.15:
            tag(ctx, 540, 1060, "MAR 23, 2020: SELLER AHEAD", LCOL, back(prog(t, T["lead"] - 0.15, 0.3)), 40, -0.02, C["ink"])
        if t > T["bottom2"] - 0.1:
            tag(ctx, 540, 1110, "= THE CRASH LOW", C["cream"], back(prog(t, T["bottom2"] - 0.1, 0.3)), 30, 0.02)
    bunting(ctx, "THE COVID CRASH", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 9 waits for calm, market leaves
def s_leaves(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x06), (0x0C, 0x06, 0x02))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GOLD, 0.12)
    x0 = di("2020-01-02"); xe = di("2021-12-31")
    pts = [(s0 + 0.1, di("2020-03-23")), (T["leaves"] + 0.6, di("2021-06-30"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, xe, curtain=up + 1, years=(2020, 2021), x0=x0)
    if t > T["waits"] - 0.15:
        tag(ctx, 540, 440, "WAITING FOR 2 CALM WEEKS...", GOLD, back(prog(t, T["waits"] - 0.15, 0.3)), 40, -0.03, C["ink"])
    if t > T["leaves"] - 0.15:
        tag(ctx, 540, 530, "THE MARKET DIDN'T WAIT", HCOL, back(prog(t, T["leaves"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2020 - 2021", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("sleep" if t < T["leaves"] else "sad") if e != "talk" else e)


# ---------------------------------------------------------------- 10 remember the 10 hidden days -> the 10 best days
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["best"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "THOSE 10", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "HIDDEN DAYS?", W / 2, 680, 120, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    else:
        big_title(ctx, "THE 10 BEST DAYS", W / 2, 440, 104, GRNC, back(prog(t, T["best"] - 0.1, 0.3)), 980, -0.02, 12)
        day_cards(ctx, t, BEST, T["best"], 100, 530, GRNC,
                  lambda k: T["sold"] if INN[BEST[k] - 1] else T["missed"] + 0.1 + k * 0.08,
                  special=[k for k, i in enumerate(BEST) if INN[i - 1]][0])
        if t > T["tenth"] - 0.1:
            pp = back(prog(t, T["tenth"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1010); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "MISSED 9 · SOLD THE 10TH AT OPEN", 0, 0, fit(ctx, "MISSED 9 · SOLD THE 10TH AT OPEN", 80, 1000), C["red"], 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            ctx.restore()
    bunting(ctx, "THE HIDDEN DAYS", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["missed"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 11 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"OTHER TRIGGERS: -3% {money(_R['scan']['-0.03/10'])} (WON) · -1.5% {money(_R['scan']['-0.015/10'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "B · JUST HOLD", money(HOLD_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "A · SELL AFTER -2% DAYS (0.05% FEES)", money(RULE_V), LCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 470, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "THE BILL", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["THE FEAR WAS RIGHT."], W / 2, 470, T["fear2"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    gap = money(HOLD_V - RULE_V)
    stamp_box(ctx, ["ACTING ON IT", f"COST {gap}."], W / 2 + 10, 690, T["Acting"] - 0.1, t, C["red"], 860, 70, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["cost"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 865); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #29", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules, "crash": s_crash,
            "dodge": s_dodge, "y2020": s_y2020, "leaves": s_leaves, "remember": s_remember, "score": s_score,
            "verdict": s_verdict, "loop": s_loop}


# ================================================================ #32 overrides: 5 red days in a row -> sell, back in a month
LCOL = (0xFF, 0x8A, 0x3D)   # THE STREAK SELLER (orange)


def hud(ctx, t):
    a = ease(prog(t, SC["question"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #32", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["question"]) / (T["discount"] - SC["question"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def circle(ctx, x, y, r, col, a=1.0):
    ctx.new_path(); ctx.arc(x, y, r + 4, 0, 6.2832); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
    ctx.new_path(); ctx.arc(x, y, r, 0, 6.2832); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def red_streak(ctx, x0, y0, t, t0, n=5, s=1.0, a=1.0, step=0.18):
    """five red candles stepping down, each pops in"""
    for k in range(n):
        pk = back(prog(t, t0 + k * step, 0.28))
        if pk <= 0:
            continue
        cx = x0 + k * 112 * s; cy = y0 + k * 34 * s
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk * s, 1e-3), max(pk * s, 1e-3))
        candle(ctx, -36, -60, 72, 120, REDC, a, 26)
        text(ctx, str(k + 1), 0, 100, 34, C["white"], a, HEAD, True, "center", outline=5, ocol=C["ink"])
        ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: 5 RED DAYS: / 43 / TIMES)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x18), (0x06, 0x02, 0x08))
    god_rays(ctx, W / 2, 600, t, 0.08, REDC, 14, 1400)
    for k in range(30):
        u = ((t * 0.7) + k / 30) % 1
        rect(ctx, (k * 131) % W, u * 1700 - 100, 4, 40, (0xFF, 0x9A, 0xA8), 0.12)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 260); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "5 RED DAYS:", 0, 0, 150, C["white"], 1, HEAD, True, "center", outline=16, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(520 + shake, 650); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "43", 0, 0, 400, REDC, 1, HEAD, True, "center", outline=28, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 840); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "TIMES", 0, 0, 170, GOLD, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    # picture change: the five red candles march in on "red days", tag on "times"
    if tl > T["red1"] - 0.15:
        red_streak(ctx, 110, 1000, tl, T["red1"] - 0.15, 5, 0.62, step=0.14)
    if show_tag and tl >= T["times1"] - 0.1:
        tag(ctx, 540, 925, "IN A ROW · SPY 2005-2024", C["cream"], back(prog(tl, T["times1"] - 0.1, 0.3)), 34, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "fire", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 it just happened again (news)
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x16, 0x20), (0x0A, 0x04, 0x08))
    big_title(ctx, "NOV 18, 2026", W / 2, 470, 110, C["white"], back(prog(t, s0 + 0.02, 0.3)), 980, -0.03, 14)
    big_title(ctx, "S&P: 5TH RED DAY", W / 2, 640, 140, REDC, back(prog(t, s0 + 0.1, 0.3)), 1000, 0.02, 18)
    pk = back(prog(t, T["happened"] - 0.1, 0.3))
    if pk > 0:
        tag(ctx, 540, 790, "LONGEST LOSING STREAK SINCE JUNE", GOLD, pk, 38, -0.02, C["ink"])
    red_streak(ctx, 300, 930, t, s0 + 0.05, 5, 0.75, step=0.08)
    bunting(ctx, "IT'S BACK", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "SELL", "ON DAY 6", LCOL, -230, ta), ("B", "SIT", "TIGHT", HCOL, 230, tb))):
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


XE1 = di("2009-12-31")
RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["crash"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"] - 0.4, T["B"], 420, T["B"] + 0.3)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="DAY SIX"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "UP?  DOWN?  ?? / 43", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "WATCH DAY SIX", W / 2, 425, 110, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["six1"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("5TH RED CLOSE", "SELL", LCOL, 290, T["sell"]),
                                                 ("1 MONTH LATER", "BUY BACK", GRNC, 790, T["month"]))):
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
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 6 2008: the seller sneaks ahead
def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (s1 - 0.2, di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: THE CRASH", C["red"], back(prog(t, T["eight"] - 0.15, 0.3)), 44, -0.03, C["white"])
    if t > T["sneaks"] - 0.15:
        tag(ctx, 540, 530, "THE SELLER SNEAKS AHEAD", LCOL, back(prog(t, T["sneaks"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 7 the bounces: steps aside, lead gone by 2010
XE3 = di("2012-12-31")


def s_bounces(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x1A, 0x06), (0x0C, 0x06, 0x02))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GOLD, 0.12)
    pts = [(s0 + 0.1, di("2009-03-09")), (T["ten"] + 0.2, di("2010-07-06")), (T["gone"] + 0.6, di("2010-12-31"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE3, curtain=up + 1, years=(2005, 2008, 2011))
    if t < T["By"] - 0.1:
        tag(ctx, 540, 440, "THEN COME THE BOUNCES", GRNC, back(prog(t, T["bounces"] - 0.15, 0.3)), 44, -0.03, C["ink"])
        if t > T["Streak"] - 0.1:
            tag(ctx, 540, 530, "SELL... WAIT... MISS THE CLIMB", LCOL, back(prog(t, T["Streak"] - 0.1, 0.3)), 40, 0.02, C["ink"])
    else:
        tag(ctx, 540, 440, "JULY 2010", C["white"], back(prog(t, T["By"] - 0.1, 0.3)), 44, -0.03, C["ink"])
        if t > T["gone"] - 0.15:
            tag(ctx, 540, 530, "LEAD GONE. FOR GOOD.", HCOL, back(prog(t, T["gone"] - 0.15, 0.3)), 48, 0.02, C["ink"])
    bunting(ctx, "2009 - 2010", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("sad" if t > T["gone"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 8 2020: sells into the crash, rebuys lower, still behind
P0, P1 = di("2020-01-02"), di("2020-06-30")
SELL20, BUY20 = di("2020-02-27"), di("2020-03-27")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x30), (0x03, 0x04, 0x0C))
    stars(ctx, t, 30, 180, 1150, 9, 0.5)
    if t < T["catch"] - 0.25:
        big_title(ctx, "2020", W / 2, 460, 130, C["white"], back(prog(t, s0 + 0.03, 0.3)), 900, -0.03, 16)
        k = ease_io(prog(t, T["sells"] - 0.2, max(0.6, T["lower"] - T["sells"] + 0.4)))
        up = int(P0 + 2 + (P1 - P0 - 2) * k)
        box = (150, 570, 780, 330)
        card(ctx, box[0] - 20, box[1] - 20, box[2] + 40, box[3] + 70, (0x0C, 0x10, 0x1C), 0.92, 16, border=C["grey"])
        seg = CL[P0:P1 + 1]; vlo, vhi = float(seg.min()) * 0.95, float(seg.max()) * 1.05
        xs, ys = series_xy(CL, P0, P1, up, box, vlo, vhi, 1)
        poly(ctx, xs, ys, C["white"], 6, 1, glow=True)
        for lab, d in (("JAN", "2020-01-02"), ("MAR", "2020-03-02"), ("JUN", "2020-06-01")):
            text(ctx, lab, sx_of(di(d), P0, P1, box), box[1] + box[3] + 40, 24, C["white"], 0.7, MONO, True, "center")
        for idx, lab, col, tt, dy in ((SELL20, "SELL", LCOL, T["sells"], -70), (BUY20, "BUY", GRNC, T["rebuys"], 70)):
            if up >= idx and t > tt - 0.1:
                px_ = sx_of(idx, P0, P1, box); py_ = box[1] + box[3] - (CL[idx] - vlo) / (vhi - vlo) * box[3]
                pp = back(prog(t, tt - 0.1, 0.3))
                circle(ctx, px_, py_, 12, col, 1)
                tag(ctx, px_, py_ + dy, lab, col, pp, 34, 0, C["ink"])
        if t > T["lower"] - 0.1:
            tag(ctx, 540, 1060, "BOUGHT BACK 17% LOWER", GRNC, back(prog(t, T["lower"] - 0.1, 0.3)), 40, -0.02, C["ink"])
    else:
        up = race_idx(t, [(T["catch"] - 0.25, di("2019-12-31")), (s1 - 0.2, di("2020-12-31"))])
        race_chart(ctx, t, up, di("2021-06-30"), curtain=up + 1, years=(2005, 2010, 2015, 2020))
        tag(ctx, 540, 440, "...AND STILL CAN'T CATCH UP", HCOL, back(prog(t, T["catch"] - 0.2, 0.3)), 42, -0.03, C["ink"])
    bunting(ctx, "THE COVID CRASH", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("sad" if t > T["catch"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 9 remember day six -> 27 of 43 green
def d6_grid(ctx, t, t0, tg, x0, y0, a=1.0):
    """43 cards, one per five-day streak (by year); turn green/red on 'green'"""
    for k, (i, r6) in enumerate(zip(EVI, D6)):
        cx = x0 + (k % 9) * 100; cy = y0 + (k // 9) * 86
        pk = back(prog(t, t0 + k * 0.02, 0.25))
        if pk <= 0:
            continue
        col = (0x3A, 0x40, 0x48)
        if t > tg + k * 0.03:
            col = GRNC if r6 > 0 else REDC
        ctx.save(); ctx.translate(cx + 44, cy + 40); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -44, -38, 88, 76, col, a, 12, shadow=False, border=C["ink"])
        text(ctx, "'" + DATES[i].strftime("%y"), 0, 12, 30, C["ink"] if t > tg + k * 0.03 else C["white"], a, MONO, True, "center")
        ctx.restore()


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["After"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "DAY SIX?", W / 2, 560, 220, GOLD, r, 960, 0, 18)
        evidence(ctx, 540, 820, t, ease(prog(t, s0 + 0.2, 0.3)))
    else:
        big_title(ctx, "DAY 6 AFTER EVERY STREAK", W / 2, 440, 84, C["white"], back(prog(t, T["After"] - 0.1, 0.3)), 980, -0.02, 12)
        d6_grid(ctx, t, T["After"], T["green"], 90, 500)
        if t > T["twentyseven"] - 0.1:
            pp = back(prog(t, T["twentyseven"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1020); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "27 OF 43 CLOSED GREEN", 0, 0, fit(ctx, "27 OF 43 CLOSED GREEN", 96, 1000), GRNC, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            ctx.restore()
        if t > T["usually"] - 0.1:
            tag(ctx, 540, 1110, "IT SOLD RIGHT BEFORE THE BOUNCE", LCOL, back(prog(t, T["usually"] - 0.1, 0.3)), 36, 0.02, C["ink"])
    bunting(ctx, "DAY SIX", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["green"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 10 score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"OTHER WAITS: 2 WEEKS {money(_R['scan']['10'])} (WON) · 3 MONTHS {money(_R['scan']['63'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · SELLS AFTER 5 RED DAYS (0.05% FEES)", money(RULE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · SITS TIGHT", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["FELT LIKE A WARNING..."], W / 2, 470, T["Five2"] - 0.05, t, STAMP_OR, 860, 66, -0.05)
    stamp_box(ctx, ["MOSTLY A DISCOUNT."], W / 2 + 10, 690, T["Mostly"] - 0.1, t, STAMP_GR, 860, 74, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["discount"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 865); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #33", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "question": s_question, "guess": s_guess, "clue": s_clue, "rules": s_rules, "crash": s_crash,
            "bounces": s_bounces, "y2020": s_y2020, "remember": s_remember, "score": s_score,
            "verdict": s_verdict, "loop": s_loop}


# ================================================================ #33 overrides: be greedy when others are fearful (VIX >= 30 -> buy)
LCOL = (0xFF, 0xB0, 0x2E)   # THE FEAR BUYER (amber)
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



def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #33", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["didnt"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


# ---------------------------------------------------------------- 1 hook (frame 0: FEAR 30+ / BUY?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x2E, 0x0A, 0x30), (0x06, 0x02, 0x0A))
    god_rays(ctx, W / 2, 620, t, 0.08, GOLD, 14, 1400)
    for k in range(26):
        u = ((t * 0.6) + k / 26) % 1
        rect(ctx, (k * 157) % W, 1700 - u * 1800, 5, 5, GOLD, 0.25)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 270); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "FEAR", 0, 0, 190, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(520 + shake, 640); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "30+", 0, 0, 380, REDC, 1, HEAD, True, "center", outline=28, ocol=C["ink"])
    ctx.restore()
    bp = 1.0 + 0.12 * math.sin(math.pi * prog(tl, T["buy1"] - 0.1, 0.35))
    ctx.save(); ctx.translate(540, 850); ctx.rotate(0.03); ctx.scale(max(s_ * bp, 1e-3), max(s_ * bp, 1e-3))
    text(ctx, "BUY?", 0, 0, 190, GOLD, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    gk = ease(prog(tl, T["hits"] - 0.2, 0.4))
    if gk > 0:
        fear_gauge(ctx, 170, 1060, 0.62 * gk + 1e-3, t, 0.18 + 0.7 * ease(prog(tl, T["hits"], 0.6)))
    if show_tag and tl >= T["thirty1"] - 0.1:
        tag(ctx, 540, 955, "VIX = WALL STREET'S FEAR GAUGE", C["cream"], back(prog(tl, T["thirty1"] - 0.1, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if e != "talk" else e, prop=prop_coin)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "tophat", lambda e: "shock", prop=prop_coin)


# ---------------------------------------------------------------- 2 guess
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "BUY THE", "PANIC", LCOL, -230, ta), ("B", "JUST", "HOLD", HCOL, 230, tb))):
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


XE1 = di("2009-12-31")
RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["spike"], di("2007-08-10"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"] - 0.4, T["B"], 420, T["B"] + 0.3)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="THE QUIET STRETCH"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "FROM ????  TO ????", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE QUIET STRETCH", W / 2, 425, 104, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["quiet1"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("FEAR 30+", "BUY", GRNC, 290, T["buy2"]),
                                                 ("1 CALM YEAR", "SELL", LCOL, 790, T["year"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        if k == 0:
            arrow_up(ctx, -175, 0, 0.42, C["white"])
        else:
            arrow_down(ctx, -175, 0, 0.42, C["white"])
        text(ctx, title, 45, -12, fit(ctx, title, 52, 330), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 45, 62, fit(ctx, l1, 64, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t < T["calm"] - 0.3:
        fear_gauge(ctx, 540, 1060, 0.5, t, 0.86)
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 5 at first: no fear, waits in cash
def s_wait(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x14, 0x2C), (0x03, 0x04, 0x0C))
    stars(ctx, t, 40, 160, 1200, 3, 0.7)
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2005 - 2007: NO FEAR", C["white"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["cash1"] - 0.15:
        tag(ctx, 540, 530, "IT SITS IN CASH", LCOL, back(prog(t, T["cash1"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "WAITING", t, s0, [C["blue"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if e != "talk" else e)


# ---------------------------------------------------------------- 6 Aug 2007: fear spikes, it jumps in before the crash
def s_spike(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(T["jumps"] - 0.2, di("2007-08-16")), (T["Ouch"] + 0.2, di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "AUG 2007: FEAR HITS 30", C["red"], back(prog(t, T["seven"] - 0.15, 0.3)), 44, -0.03, C["white"])
    if t > T["jumps"] - 0.15:
        tag(ctx, 540, 530, "FIRST BUY... RIGHT BEFORE 2008", LCOL, back(prog(t, T["jumps"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    if t < T["jumps"]:
        fear_gauge(ctx, 860, 1060, 0.45, t, 0.9)
    bunting(ctx, "2007 - 2009", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("shock" if t > T["crash"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 7 holds on, buys every scare: 5 trades, 5 winners
def trade_cards(ctx, t, t0, tw, x0, y0):
    for k, tr in enumerate(TRD):
        cx = x0 + k * 182; cy = y0
        pk = back(prog(t, t0 + k * 0.12, 0.28))
        if pk <= 0:
            continue
        won = t > tw + k * 0.1
        ctx.save(); ctx.translate(cx + 80, cy + 70); ctx.rotate((-0.04, 0.03, -0.02, 0.04, -0.03)[k]); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -80, -70, 160, 140, GRNC if won else (0x3A, 0x40, 0x48), 1, 16, border=C["ink"])
        text(ctx, "BUY", 0, -30, 26, C["ink"] if won else C["white"], 1, TAGF, False, "center")
        text(ctx, tr[0][:4], 0, 20, 52, C["ink"] if won else C["white"], 1, HEAD, True, "center")
        if won:
            text(ctx, "WIN", 0, 58, 30, C["ink"], 1, HEAD, True, "center")
        ctx.restore()


def s_trades(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GRNC, 0.12)
    if t < T["So"] - 0.1:
        big_title(ctx, "EVERY SCARE AFTER", W / 2, 440, 100, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
        trade_cards(ctx, t, T["Five"] - 0.1, T["winners"] - 0.1, 90, 560)
        if t > T["winners"] - 0.1:
            pp = back(prog(t, T["winners"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "5 TRADES · 5 WINNERS", 0, 0, fit(ctx, "5 TRADES · 5 WINNERS", 100, 1000), GRNC, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            ctx.restore()
    else:
        big_title(ctx, "SO IT WINS?", W / 2, 640, 180, GOLD, back(prog(t, T["So"] - 0.1, 0.3)), 980, -0.03, 18)
        trade_cards(ctx, t, -10, -10, 90, 760)
    bunting(ctx, "PERFECT RECORD", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 8 remember the quiet stretch: Dec 2012 - Aug 2015 in cash, market +40%
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["From"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "THAT QUIET", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "STRETCH?", W / 2, 690, 150, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    else:
        x0 = di("2012-01-03"); xe = di("2015-12-31")
        up = race_idx(t, [(T["From"], QA0), (T["Almost"] + 0.4, QA1)])
        race_chart(ctx, t, up, xe, years=(2012, 2013, 2014, 2015), x0=x0)
        tag(ctx, 540, 440, "DEC 2012 - AUG 2015: NO FEAR", C["white"], back(prog(t, T["From"] - 0.1, 0.3)), 40, -0.03, C["ink"])
        if t > T["Almost"] - 0.1:
            tag(ctx, 540, 530, "ALMOST 3 YEARS IN CASH", LCOL, back(prog(t, T["Almost"] - 0.1, 0.3)), 44, 0.02, C["ink"])
        if t > T["forty"] - 0.1:
            pp = back(prog(t, T["forty"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1060); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "MARKET +40% WITHOUT IT", 0, 0, fit(ctx, "MARKET +40% WITHOUT IT", 92, 1000), HCOL, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            ctx.restore()
    bunting(ctx, "THE QUIET STRETCH", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["forty"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 9 score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"12 VARIANTS (VIX 25-40, HOLD 3M-2Y): ALL LOST · BEST {money(max(_R['scan'].values()))}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · BUYS WHEN FEAR HITS 30 (0.05% FEES)", money(RULE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · JUST HOLDS", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["GREEDY IN FEAR: WORKED."], W / 2, 470, T["Being"] - 0.05, t, STAMP_GR, 860, 64, -0.05)
    stamp_box(ctx, ["WAITING FOR FEAR: DIDN'T."], W / 2 + 10, 690, T["Waiting"] - 0.1, t, STAMP_OR, 860, 64, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["didnt"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 865); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #34", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "rules": s_rules, "wait": s_wait, "spike": s_spike,
            "trades": s_trades, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}
