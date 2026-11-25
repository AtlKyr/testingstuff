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


# ================================================================ #34 overrides (8% off the record: buy monthly, or wait for dips?)
LCOL = (0xFF, 0x8A, 0x3D)   # B: WAITS FOR DIPS (orange)
TAGC = (0xF5, 0xE6, 0xC8)


def price_tag(ctx, cx, cy, s, label, col=TAGC, fg=None, a=1.0, rot=-0.12):
    """a shop price tag with a string hole"""
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-150, -60); ctx.line_to(110, -60); ctx.line_to(160, 0); ctx.line_to(110, 60); ctx.line_to(-150, 60); ctx.close_path()
    ctx.set_source_rgba(0, 0, 0, 0.35 * a); ctx.save(); ctx.translate(8, 10); ctx.fill_preserve(); ctx.restore(); ctx.new_path()
    ctx.move_to(-150, -60); ctx.line_to(110, -60); ctx.line_to(160, 0); ctx.line_to(110, 60); ctx.line_to(-150, 60); ctx.close_path()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(9); ctx.stroke()
    ctx.new_path(); ctx.arc(118, 0, 13, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke()
    text(ctx, label, -20, 26, fit(ctx, label, 74, 240), fg or C["ink"], a, HEAD, True, "center")
    ctx.restore()


def prop_tag(ctx, x, y, px, t):
    sw = math.sin(t * 4) * 0.15
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + 70, y - 120)
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    price_tag(ctx, x + 70, y - 190, 0.62, "-8%", REDC, C["white"], 1, -1.35 + sw)


def jar(ctx, cx, cy, s, fill, t, label=None, a=1.0):
    """a glass cash jar that fills with bills (fill 0..1)"""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    card(ctx, -130, -170, 260, 330, (0x9F, 0xD8, 0xF0), 0.25 * a, 40, shadow=False, border=C["white"])
    h = 300 * clamp(fill)
    for k in range(int(h // 22)):
        yy = 150 - 22 * (k + 1) + 4
        rect(ctx, -110 + (k % 2) * 8, yy, 212, 18, GRNC if k % 3 else (0x16, 0xB0, 0x6A), a)
        rect(ctx, -20 + (k % 2) * 8, yy + 4, 30, 10, (0x0B, 0x5A, 0x34), a)
    rect(ctx, -110, -200, 220, 34, (0x8B, 0x5A, 0x2B), a)
    if label:
        text(ctx, label, 0, 230, fit(ctx, label, 64, 420), GOLD, a, HEAD, True, "center", outline=10, ocol=C["ink"])
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #34", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(A_V), 805, 78, fit(ctx, money(A_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["eighteen"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    i = s0_   # orange bands = B is sitting on a cash pile (>= $1,000)
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
    vmax = max(4000.0, 1.12 * float(max(np.nanmax(AV[s0_:hi]), np.nanmax(BW[s0_:hi]))))
    vmin = 0.0
    xs, ys = series_xy(PUTV, s0_, xe, up, RBOX, vmin, vmax, 3)
    for q in range(0, len(xs) - 1, 2):
        poly(ctx, xs[q:q + 2], ys[q:q + 2], C["white"], 3, 0.45)
    tips = []
    for arr, col in ((AV, HCOL), (BW, LCOL)):
        xs, ys = series_xy(arr, s0_, xe, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (lx, ly) = tips
    off = 0 if abs(hy - ly) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - off, 4, "tophat", t, "smug", False, True)
    mini_rocco(ctx, lx, ly - 4, 4, "fire", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("A · BUYS MONTHLY", HCOL), ("B · WAITS FOR DIPS", LCOL))):
        rect(ctx, bx + bw - 350, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 310, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + bh - 40, 30, 18, LCOL, 0.35)
    text(ctx, "= B WAITS IN CASH", bx + 60, by + bh - 24, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2007-12-31"); XE2 = N - 1
XE3 = di("2013-12-31")


# ---------------------------------------------------------------- 1 hook (frame 0: S&P / -8% / BUY NOW?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x08, 0x14), (0x08, 0x02, 0x06))
    god_rays(ctx, W / 2, 620, t, 0.08, REDC, 14, 1400)
    for k in range(26):
        u = ((t * 0.6) + k / 26) % 1
        rect(ctx, (k * 157) % W, 1700 - u * 1800, 5, 5, GOLD, 0.25)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 285); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "S&P", 0, 0, 200, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(520 + shake, 660); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "-8%", 0, 0, 400, REDC, 1, HEAD, True, "center", outline=28, ocol=C["ink"])
    ctx.restore()
    bp = 1.0 + 0.12 * math.sin(math.pi * prog(tl, T["Buy"] - 0.1, 0.35))
    ctx.save(); ctx.translate(540, 885); ctx.rotate(0.03); ctx.scale(max(s_ * bp, 1e-3), max(s_ * bp, 1e-3))
    text(ctx, "BUY NOW?", 0, 0, 180, GOLD, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= T["record"] - 0.1:
        tag(ctx, 540, 965, "FROM ITS RECORD · 6 RED DAYS IN A ROW", C["cream"], back(prog(tl, T["record"] - 0.1, 0.3)), 30, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_tag)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_tag)


# ---------------------------------------------------------------- 2 guess
def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "BUY", "MONTHLY", HCOL, -230, ta), ("B", "WAIT FOR", "DIPS", LCOL, 230, tb))):
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


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["summer"], di("2007-08-10"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"] - 0.4, T["B"], 420, T["B"] + 0.3)
    if t < T["B"] - 0.2:
        price_tag(ctx, 540, 860, 1.1 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "-8%", REDC, C["white"], 1, -0.1 + 0.05 * math.sin(t * 5))
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="THE PRICE TAG"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "PAID: $???.??", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE PRICE TAG", W / 2, 425, 110, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["tag1"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("$500 A MONTH", "BUY NOW", HCOL, 290, T["five"]),
                                                 ("$500 TO CASH", "BUY AT -8%", LCOL, 790, T["eight2"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        text(ctx, "A" if k == 0 else "B", -175, 40, 110, C["ink"], 1, HEAD, True, "center")
        text(ctx, title, 45, -12, fit(ctx, title, 52, 330), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 45, 62, fit(ctx, l1, 60, 330), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


# ---------------------------------------------------------------- 5 2005-2007: no dip, the cash pile grows
def s_wait(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x14, 0x2C), (0x03, 0x04, 0x0C))
    stars(ctx, t, 40, 160, 1200, 3, 0.7)
    race_chart(ctx, t, RACE1(t), XE1)
    tag(ctx, 540, 440, "2005 - 2007: NO 8% DIP", C["white"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["cash"] - 0.15:
        fill = clamp(prog(t, T["cash"] - 0.1, T["sixteen"] - T["cash"] + 0.2))
        jar(ctx, 860, 1500, 0.62 * back(prog(t, T["cash"] - 0.15, 0.35)) + 1e-3, fill, t,
            "$16,000 WAITING" if t > T["sixteen"] - 0.1 else None)
    bunting(ctx, "WAITING", t, s0, [C["blue"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if e != "talk" else e)


# ---------------------------------------------------------------- 6 summer 2007: the dip comes, all in... then 2008
def s_summer(ctx, t, s0, s1):
    if t < T["Then"] - 0.1:
        bg_fill(ctx, (0x4A, 0x2A, 0x10), (0x12, 0x08, 0x04))
        sun(ctx, 900, 250, 70, t, 0.8)
    else:
        rain_bg(ctx, t)
    pts = [(T["dip2"] - 0.2, di("2007-08-16")), (T["Then"], di("2007-10-09")), (T["crushes"] + 0.5, di("2009-03-09"))]
    xe = di("2009-12-31")
    race_chart(ctx, t, race_idx(t, pts), xe, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "AUG 2007: -9% FROM THE RECORD", C["red"], back(prog(t, T["dip2"] - 0.15, 0.3)), 40, -0.03, C["white"])
    if T["spends"] - 0.15 < t < T["Then"] - 0.1:
        tag(ctx, 540, 530, "ALL $16,000 IN!", GRNC, back(prog(t, T["spends"] - 0.15, 0.3)), 48, 0.02, C["ink"])
    if t > T["eight3"] - 0.15:
        tag(ctx, 540, 530, "2008: BOTH CRUSHED", LCOL, back(prog(t, T["eight3"] - 0.15, 0.3)), 48, 0.02, C["ink"])
    bunting(ctx, "2007 - 2009", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire" if t > T["Then"] else "party", lambda e: ("shock" if t > T["crushes"] else "smug") if e != "talk" else e,
          prop=prop_umbrella if t > T["Then"] else prop_flag)


# ---------------------------------------------------------------- 7 the strange part: calm market, B waits again
def s_calm(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GRNC, 0.12)
    pts = [(T["After"], di("2009-03-09")), (T["waits"] + 0.3, di("2013-03-28"))]
    race_chart(ctx, t, race_idx(t, pts), XE3, years=(2005, 2009, 2013))
    if t < T["After"] - 0.1:
        big_title(ctx, "THE STRANGE PART", W / 2, 470, 100, GOLD, back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    else:
        tag(ctx, 540, 440, "2009 - 2013: BOTH BUY EVERY MONTH", C["white"], back(prog(t, T["After"] - 0.1, 0.3)), 36, -0.03, C["ink"])
    if t > T["waits"] - 0.15:
        tag(ctx, 540, 530, "2013: B WAITS AGAIN...", LCOL, back(prog(t, T["waits"] - 0.15, 0.3)), 46, 0.02, C["ink"])
    bunting(ctx, "2009 - 2013", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 8 remember the price tag: waited 2.5 years, paid +36% (adj)
def wait_chart(ctx, box, t, k, a=1.0):
    bx, by, bw, bh = box
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    i0, i1 = di("2012-12-03"), di("2015-10-30")
    seg = OP[i0:i1 + 1]
    vmin, vmax = float(seg.min()) * 0.95, float(seg.max()) * 1.05
    up = int(i0 + (i1 - i0) * clamp(k))
    xs, ys = series_xy(OP, i0, i1, max(up, i0 + 2), box, vmin, vmax, 2)
    poly(ctx, xs, ys, C["white"], 6, a, glow=True)
    for yr in (2013, 2014, 2015):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), i0, i1, box), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    for idx, lab, col in ((QA0, "DAY ONE", HCOL), (QA1, "THE 'SALE'", REDC)):
        if up >= idx:
            x = sx_of(idx, i0, i1, box); y = sy_of(OP[idx], vmin, vmax, box)
            ctx.new_path(); ctx.arc(x, y, 16, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()
            rect(ctx, x - 2, y + (20 if idx == QA0 else -110), 4, 90, col, a)
            text(ctx, lab, x + (10 if idx == QA0 else -10), y + (140 if idx == QA0 else -125), 30, col, a, MONO, True, "left" if idx == QA0 else "right",
                 outline=6, ocol=C["ink"])
    if up >= QA0:
        xa = sx_of(QA0, i0, i1, box); xb = sx_of(min(up, QA1), i0, i1, box)
        rect(ctx, xa, by, max(2, xb - xa), bh, LCOL, 0.2 * a)


def wait_tags(ctx, t, t0, tr, x0, y0):
    for k, (lab, a_, b_) in enumerate(WAITS):
        cx = x0 + (k % 3) * 310; cy = y0 + (k // 3) * 170
        pk = back(prog(t, t0 + k * 0.1, 0.28))
        if pk <= 0:
            continue
        red = t > tr + k * 0.08
        price_tag(ctx, cx, cy, 0.85 * pk + 1e-3, lab, REDC if red else TAGC, C["white"] if red else C["ink"], 1, (-0.1, 0.06, -0.04, 0.08, -0.07, 0.03)[k])


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["He"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "THAT PRICE", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "TAG?", W / 2, 690, 170, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    elif t < T["Every"] - 0.12:
        k = prog(t, T["He"], T["sale1"] - T["He"] + 0.6)
        wait_chart(ctx, RBOX, t, k)
        tag(ctx, 540, 440, "FEB 2013 - AUG 2015: B WAITS", C["white"], back(prog(t, T["He"] - 0.1, 0.3)), 40, -0.03, C["ink"])
        if t > T["half"] - 0.1:
            tag(ctx, 540, 530, "2 1/2 YEARS OF CASH", LCOL, back(prog(t, T["half"] - 0.1, 0.3)), 44, 0.02, C["ink"])
        if t > T["thirtysix"] - 0.1:
            pp = back(prog(t, T["thirtysix"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1050); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "PAID +36% MORE", 0, 0, fit(ctx, "PAID +36% MORE", 110, 1000), REDC, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            ctx.restore()
            s_ = f"DIVIDEND-ADJUSTED PRICE · RAW SPY PRICE +{RAW_RISE * 100:.0f}%"
            text(ctx, s_, 540, 1112, fit(ctx, s_, 26, 900, MONO), C["white"], 0.85 * pp, MONO, True, "center", outline=5, ocol=C["ink"])
    else:
        big_title(ctx, "EVERY LONG WAIT", W / 2, 470, 104, C["white"], back(prog(t, T["Every"] - 0.1, 0.3)), 980, -0.02, 12)
        wait_tags(ctx, t, T["Every"] - 0.05, T["ended"] - 0.1, 230, 650)
        if t > T["Every"] + 1.2:
            s_ = "6 OF 6 WAITS (6+ MONTHS): THE 'DIP' COST MORE"
            text(ctx, s_, 540, 1010, fit(ctx, s_, 40, 980, MONO), GOLD, back(prog(t, T["Every"] + 1.2, 0.3)), MONO, True, "center", outline=6, ocol=C["ink"])
    bunting(ctx, "THE PRICE TAG", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["thirtysix"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 9 score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"6 DIP TRIGGERS (-3% TO -20%): ALL BEHIND · BEST {money(BEST_SCAN)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$120,000 PUT IN EACH · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · BUYS EVERY MONTH (0.05% FEES)", money(A_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · WAITS FOR -8% DIPS", money(B_V), LCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 470, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["THE 'SALE' COST", "-" + money(GAP_V)], W / 2, 520, T["The2"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["eighteen"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #35", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "rules": s_rules, "wait": s_wait, "summer": s_summer,
            "calm": s_calm, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #35 overrides (the 1% fee)
LCOL = (0xFF, 0x8A, 0x3D)   # 1% FEE (orange)
ENVC = (0xF3, 0xEC, 0xDC)


def envelope(ctx, cx, cy, s, label=None, a=1.0, rot=-0.08, col=ENVC, stampc=REDC):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -170, -110, 340, 220, col, a, 12, border=C["ink"])
    ctx.new_path(); ctx.move_to(-170, -110); ctx.line_to(0, 10); ctx.line_to(170, -110)
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(7); ctx.stroke()
    rect(ctx, 100, -95, 52, 60, stampc, a)
    text(ctx, "BILL", -100, 85, 44, C["ink"], a, HEAD, True, "center")
    if label:
        text(ctx, label, 40, 85, fit(ctx, label, 44, 200, MONO), REDC, a, MONO, True, "center")
    ctx.restore()


def prop_bill(ctx, x, y, px, t):
    envelope(ctx, x + 60, y - 170 + math.sin(t * 3) * 8, 0.5, None, 1, -0.25 + 0.08 * math.sin(t * 4))


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev4"]
    tag(ctx, 160, 66, "CASE #35", C["cream"], a, 26, -0.03)
    text(ctx, "REAL COST:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev4"], 0.35))
        card(ctx, 655, 38, 300, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(GAP_V), 805, 78, fit(ctx, money(GAP_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["fifth"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(NF[s0_:hi]), np.nanmax(FE[s0_:hi]))))
    vmin = 5000.0
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    xa = sx_of(s0_, s0_, xe, RBOX)
    xs1, ys1 = series_xy(NF, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(FE, s0_, xe, up, RBOX, vmin, vmax, 3)
    ctx.new_path(); ctx.move_to(xs1[0], ys1[0])
    for x, y in zip(xs1, ys1):
        ctx.line_to(x, y)
    for x, y in zip(xs2[::-1], ys2[::-1]):
        ctx.line_to(x, y)
    ctx.close_path(); ctx.set_source_rgba(*rgba(REDC, 0.35 * a)); ctx.fill()
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 8, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "smug", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "fire", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("NO FEE", HCOL), ("1% FEE A YEAR", LCOL))):
        rect(ctx, bx + 30, by + 22 + k * 34, 30, 10, col)
        text(ctx, lab, bx + 70, by + 34 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + bw - 330, by + bh - 40, 30, 18, REDC, 0.45)
    text(ctx, "= THE GAP", bx + bw - 290, by + bh - 24, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2007-12-31"); XE2 = N - 1


# ---------------------------------------------------------------- 1 hook (frame 0: 1% FEE: / 240 / BILLS)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x0A, 0x2A, 0x2E), (0x02, 0x08, 0x0A))
    god_rays(ctx, W / 2, 620, t, 0.08, GOLD, 14, 1400)
    for k in range(26):
        u = ((t * 0.6) + k / 26) % 1
        rect(ctx, (k * 157) % W, 1700 - u * 1800, 5, 5, GOLD, 0.25)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 275); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "1% FEE:", 0, 0, 180, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(530 + shake, 660); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "240", 0, 0, 400, GOLD, 1, HEAD, True, "center", outline=28, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 880); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "BILLS", 0, 0, 190, REDC, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= T["bills1"] - 0.1:
        tag(ctx, 540, 965, "ONE EVERY MONTH · 20 YEARS", C["cream"], back(prog(tl, T["bills1"] - 0.1, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if e != "talk" else e, prop=prop_bill)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "tophat", lambda e: "shock", prop=prop_bill)


def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "COSTS A", "LITTLE", GRNC, -230, ta), ("B", "COSTS", "A LOT", REDC, 230, tb))):
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


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["year1"], di("2005-12-30")), (SC["crash"], di("2007-10-09"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards2(ctx, t, T["A"] - 0.4, T["B"], 420, T["B"] + 0.3)
    if t < T["B"] - 0.2:
        envelope(ctx, 540, 860, 1.2 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "1%", 1, -0.08 + 0.05 * math.sin(t * 5))
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def evidence(ctx, cx, cy, t, a=1.0, label="THE HIDDEN COST"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "NOT ON ANY BILL", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "THE WORST COST", W / 2, 425, 110, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["never"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("$10,000 IN SPY", "NO FEE", HCOL, 290, T["ten"]),
                                                 ("$10,000 IN SPY", "1% A YEAR", LCOL, 790, T["fee2"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, -12, fit(ctx, title, 52, 420), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 62, fit(ctx, l1, 66, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    bunting(ctx, "THE SETUP", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def s_year1(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    race_chart(ctx, t, RACE1(t), XE1)
    tag(ctx, 540, 440, f"2005: 12 BILLS = ${YEARLY[2005]}", C["white"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["Who"] - 0.15:
        tag(ctx, 540, 530, "WHO WOULD NOTICE?", GOLD, back(prog(t, T["Who"] - 0.15, 0.3)), 48, 0.02, C["ink"])
    for k in range(5):
        pk = back(prog(t, s0 + 0.3 + k * 0.25, 0.3))
        if pk > 0:
            envelope(ctx, 640 + (k % 3) * 120, 1480 + (k // 3) * 110, 0.42 * pk + 1e-3, None, 1, (-0.2, 0.1, -0.05, 0.15, -0.1)[k])
    bunting(ctx, "YEAR ONE", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.2, di("2007-10-09")), (T["crashes"] + 0.6, di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), di("2009-12-31"), years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: THE MARKET CRASHES", C["red"], back(prog(t, T["eight"] - 0.15, 0.3)), 44, -0.03, C["white"])
    if t > T["still"] - 0.15:
        tag(ctx, 540, 530, "THE BILL STILL ARRIVES", LCOL, back(prog(t, T["still"] - 0.15, 0.3)), 48, 0.02, C["ink"])
        envelope(ctx, 300, 1500, 0.6 * back(prog(t, T["still"] - 0.1, 0.35)) + 1e-3, "2008", 1, -0.12 + 0.04 * math.sin(t * 6))
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e, prop=prop_umbrella)


def fee_bars(ctx, t, t0, x0, y0, w, h, a=1.0):
    mx = max(YEARLY.values())
    bw = w / 20
    for k, yr in enumerate(range(2005, 2025)):
        pk = ease(prog(t, t0 + k * 0.08, 0.3))
        if pk <= 0:
            continue
        hh = h * YEARLY[yr] / mx * pk
        rect(ctx, x0 + k * bw + 3, y0 + h - hh, bw - 6, hh, REDC if yr != 2008 else LCOL, a)
    text(ctx, "2005", x0, y0 + h + 34, 24, C["white"], 0.75, MONO, True, "left")
    text(ctx, "2024", x0 + w, y0 + h + 34, 24, C["white"], 0.75, MONO, True, "right")
    text(ctx, "YEARLY FEE BILL", x0 + w / 2, y0 - 16, 26, GOLD, a, MONO, True, "center", outline=5, ocol=C["ink"])


def s_bull(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GRNC, 0.12)
    pts = [(s0 + 0.2, di("2009-03-09")), (T["grow"] + 0.6, di("2021-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2021-12-31"), years=(2005, 2010, 2015, 2020))
    tag(ctx, 540, 440, "2009 - 2021: THE BULL MARKET", C["white"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    if t > T["bills2"] - 0.15:
        tag(ctx, 540, 530, "...AND THE BILLS GROW", LCOL, back(prog(t, T["bills2"] - 0.15, 0.3)), 46, 0.02, C["ink"])
        fee_bars(ctx, t, T["bills2"] - 0.1, 560, 1420, 440, 200)
    bunting(ctx, "THE BULL RUN", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 40, 160, 1200, 7, 0.7)
    if t < T["Each"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "THE COST NO", W / 2, 520, 150, GOLD, r, 960, 0, 16)
        big_title(ctx, "BILL SHOWS?", W / 2, 690, 150, C["white"], r, 980, 0, 14)
        evidence(ctx, 540, 900, t, ease(prog(t, s0 + 0.2, 0.3)))
    else:
        tag(ctx, 540, 450, "$1 OF FEES PAID IN 2005...", C["white"], back(prog(t, T["Each"] - 0.1, 0.3)), 44, -0.03, C["ink"])
        coin(ctx, 540, 640, 80 * back(prog(t, T["dollar"] - 0.15, 0.35)) + 1e-3, t)
        if t > T["stopped"] - 0.1:
            tag(ctx, 540, 790, "...STOPPED GROWING", REDC, back(prog(t, T["stopped"] - 0.1, 0.3)), 44, 0.03, C["white"])
        if t > T["Left"] - 0.1:
            for k in range(7):
                pk = back(prog(t, T["Left"] + k * 0.18, 0.3))
                if pk > 0:
                    coin(ctx, 150 + k * 130, 930, 48 * pk + 1e-3, t + k)
        if t > T["seven"] - 0.1:
            pp = back(prog(t, T["seven"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1110); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "INVESTED: ~$7 BY 2024", 0, 0, fit(ctx, "INVESTED: ~$7 BY 2024", 96, 1000), HCOL, 1, HEAD, True, "center", outline=12, ocol=C["ink"])
            ctx.restore()
    bunting(ctx, "THE HIDDEN COST", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["seven"] else "smug") if e != "talk" else e, prop=prop_magnifier)


def footnote(ctx, t):
    if t >= T["Real"] - 0.1:
        a = back(prog(t, T["Real"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"0.5% FEE: {money(SCAN['0.005'])} · 2% FEE: {money(SCAN['0.02'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 IN SPY · 2005 TO 2024", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "NO FEE", money(NF_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "1% FEE A YEAR", money(FE_V), LCOL, T["rev2"], t)
    if t > T["Bills"] - 0.1:
        tag(ctx, 300, 880, f"BILLS: {money(PAID_V)}", C["cream"], back(prog(t, T["Bills"] - 0.1, 0.3)), 40, -0.03, C["ink"])
    if t > T["Real"] - 0.1:
        tag(ctx, 780, 880, f"REAL COST: {money(GAP_V)}", REDC, back(prog(t, T["Real"] - 0.1, 0.3)), 40, 0.03, C["white"])
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["1% A YEAR ATE", f"{_R['share_of_gain_lost'] * 100:.0f}% OF THE GAINS"], W / 2, 520, T["One3"] - 0.05, t, STAMP_OR, 860, 70, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["fifth"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #36", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "rules": s_rules, "year1": s_year1, "crash": s_crash,
            "bull": s_bull, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #36 overrides (S&P correction: sell at -10%, buy back at -20% or a new record)
LCOL = (0xFF, 0x8A, 0x3D)   # CORRECTION RULE (orange)
TAGC = (0xF5, 0xE6, 0xC8)


def prop_tag36(ctx, x, y, px, t):
    sw = math.sin(t * 4) * 0.15
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + 70, y - 120)
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    price_tag(ctx, x + 70, y - 190, 0.62, "-10%", REDC, C["white"], 1, -1.35 + sw)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #36", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(RULE_V), 805, 78, fit(ctx, money(RULE_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["loses"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for i0, i1 in ZONES:
        if i0 > up or i1 < s0_ or i0 > xe:
            continue
        xa = sx_of(max(i0, s0_), s0_, xe, RBOX); xb = sx_of(min(i1, up, xe), s0_, xe, RBOX)
        rect(ctx, xa, by, max(2, xb - xa), bh, LCOL, 0.18 * a)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.9 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 3)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 8, 1, glow=True)
    for lst, col, lab in ((SELLS, REDC, "SELL"), (BUYS, GRNC, "BUY")):
        for i in lst:
            if s0_ <= i <= up and i <= xe:
                sx = sx_of(i, s0_, xe, RBOX); sy = by + bh - (SV[i] - vmin) / (vmax - vmin) * bh
                ctx.new_path(); ctx.arc(sx, sy, 11, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill_preserve()
                ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(3); ctx.stroke()
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "smug", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "fire", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("B: RIDE IT OUT", HCOL), ("A: BAIL AT -10%", LCOL))):
        rect(ctx, bx + bw - 330, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2019-06-28")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x0C, 0x14), (0x08, 0x02, 0x06))
    god_rays(ctx, W / 2, 620, t, 0.09, REDC, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, u * 1500, 4, 40, (0xFF, 0x80, 0x80), 0.14)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540, 285); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "-10% OFF", 0, 0, fit(ctx, "-10% OFF", 170, 980), C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 445); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "A RECORD:", 0, 0, 120, GOLD, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(520 + shake, 830); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "6", 0, 0, 430, REDC, 1, HEAD, True, "center", outline=30, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 1010); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "TIMES", 0, 0, 170, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= T["times"] - 0.1:
        tag(ctx, 540, 1110, "SPY · 2005 TO 2024", C["cream"], back(prog(tl, T["times"] - 0.1, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e, prop=prop_tag36)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "fire", lambda e: "shock", prop=prop_tag36)


def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "BAIL OUT", "AT -10%", LCOL, -230, ta), ("B", "RIDE IT", "OUT", HCOL, 230, tb))):
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


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["rules"], di("2007-10-09")), (SC["y2008"], di("2007-12-31"))])


def evidence(ctx, cx, cy, t, a=1.0, label="ONE CHRISTMAS EVE"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "DEC 24, 20??", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def xmas_tree(ctx, cx, cy, s, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for k, (w, y) in enumerate(((150, -40), (120, -120), (90, -190))):
        ctx.new_path(); ctx.move_to(-w, y + 70); ctx.line_to(w, y + 70); ctx.line_to(0, y - 40); ctx.close_path()
        ctx.set_source_rgba(*rgba((0x1E, 0x9E, 0x5A), a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()
    rect(ctx, -22, 30, 44, 50, (0x8B, 0x5A, 0x2B), a)
    for k in range(9):
        bx_ = ((k * 53) % 200) - 100; by_ = -150 + (k * 37) % 190
        on = (int(t * 4) + k) % 3 != 0
        ctx.new_path(); ctx.arc(bx_ * (0.4 + (by_ + 150) / 400), by_, 9, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgba((GOLD, REDC, C["white"])[k % 3], a if on else 0.35 * a)); ctx.fill()
    ctx.save(); ctx.translate(0, -235); ctx.rotate(t * 0.8); text(ctx, "*", 0, 40, 110, GOLD, a, HEAD, True, "center"); ctx.restore()
    ctx.restore()


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards2(ctx, t, T["A"] - 0.5, T["B"] - 0.1, 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Christmas"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    if t > T["Eve"] - 0.1:
        xmas_tree(ctx, 860, 1520, 0.9 * back(prog(t, T["Eve"] - 0.1, 0.35)) + 1e-3, t)
    if t < T["B"] - 0.2:
        price_tag(ctx, 540, 860, 1.4 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "-10%", REDC, C["white"], 1, -0.1 + 0.05 * math.sin(t * 5))
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE NIGHT DECIDES IT", W / 2, 425, 104, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["Christmas"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    xmas_tree(ctx, 860, 1520, 0.9 * back(prog(t, T["Eve"] - 0.1, 0.35)) + 1e-3, t)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_news(ctx, t, s0, s1):
    bg_fill(ctx, (0x30, 0x08, 0x10), (0x06, 0x02, 0x04))
    for k in range(3):
        rect(ctx, 0, 300 + k * 6, W, 3, REDC, 0.25)
    ticker = "S&P 500 -3.7%  ·  NASDAQ -5.3%  ·  WORST WEEK IN 18+ MONTHS  ·  "
    xo = -((t - s0) * 260) % 1400
    rect(ctx, 0, 1760, W, 64, (0x05, 0x05, 0x05), 0.9)
    for j in range(3):
        text(ctx, ticker, xo + j * 1400, 1805, 34, GOLD, 1, MONO, True, "left")
    tag(ctx, 540, 450, "FRIDAY, NOV 20", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    p = back(prog(t, s0 + 0.2, 0.35))
    big_title(ctx, "S&P 500: -3.7%", W / 2, 640, 170, REDC, p, 980, -0.03, 16)
    p2 = back(prog(t, s0 + 0.8, 0.35))
    if p2 > 0:
        tag(ctx, 540, 770, "WEEK: -8.6%", C["white"], p2, 50, 0.03, C["ink"])
    if t > T["correction"] - 0.15:
        stamp_box(ctx, ["CORRECTION", ">10% BELOW THE OCT 6 RECORD"], W / 2, 960, T["correction"] - 0.1, t, STAMP_OR, 900, 64, -0.05)
    bunting(ctx, "THE NEWS", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("SELL", "SPY -10% UNDER RECORD", REDC, 290, T["ten"]),
                                                 ("BUY BACK", "-20% OR A NEW RECORD", GRNC, 790, T["Buy"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        (arrow_down if k == 0 else arrow_up)(ctx, -170, -20, 0.28, C["ink"])
        text(ctx, title, 40, -10, fit(ctx, title, 76, 300), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 66, fit(ctx, l1, 46, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["cheaper"] + 0.2, di("2008-08-29"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: SOLD EARLY", C["white"], back(prog(t, s0 + 0.3, 0.3)), 46, -0.03, C["ink"])
    if t > T["cheaper"] - 0.15:
        tag(ctx, 540, 530, "...BOUGHT BACK CHEAPER", GRNC, back(prog(t, T["cheaper"] - 0.15, 0.3)), 46, 0.02, C["ink"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_umbrella)


def s_miss(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x22), (0x04, 0x05, 0x0A))
    for k in range(30):
        u = ((t - s0) * 0.9 + k / 30) % 1
        rect(ctx, (k * 131) % W, u * 1900, 3, 36, (0x9A, 0xB0, 0xD0), 0.18)
    pts = [(s0 + 0.1, di("2009-12-31")), (T["higher1"] + 0.3, di("2016-07-29")), (T["again"] + 0.3, di("2018-08-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, years=(2005, 2010, 2015, 2019))
    tag(ctx, 540, 440, "2015: NO CRASH -> BOUGHT BACK HIGHER", C["red"], back(prog(t, T["crash"] - 0.15, 0.3)), 34, -0.03, C["white"])
    if t > T["Early"] - 0.15:
        tag(ctx, 540, 530, "EARLY 2018: HIGHER AGAIN", LCOL, back(prog(t, T["Early"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "NO CRASH CAME", t, s0, [C["grey"], C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


DDBOX = (120, 560, 840, 320)
I_FS = di("2018-09-20"); I_FE = di("2019-01-10")


def dd_chart(ctx, t, up, a=1.0, show_cross=False):
    bx, by, bw, bh = DDBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.94 * a, 18, border=C["grey"])
    lo, hi = -0.235, 0.01
    def yy(v): return by + bh - (v - lo) / (hi - lo) * bh
    for lv, lab in ((0, "RECORD"), (-0.10, "-10%: SELL")):
        rect(ctx, bx, yy(lv) - 1, bw, 2, C["white"], 0.2)
        text(ctx, lab, bx + 10, yy(lv) - 10, 22, C["white"], 0.6, MONO, True, "left")
    y20 = yy(-0.20)
    for j in range(26):
        rect(ctx, bx + j * 33, y20 - 3, 20, 6, GRNC, 0.9)
    text(ctx, "-20%: BUY BACK LINE", bx + bw - 10, y20 - 14, 24, GRNC, 1, MONO, True, "right", outline=5, ocol=C["ink"])
    up = max(I_FS + 2, min(up, I_FE))
    xs = [bx + (i - I_FS) / (I_FE - I_FS) * bw for i in range(I_FS, up + 1)]
    ys = [yy(DDN[i]) for i in range(I_FS, up + 1)]
    poly(ctx, xs, ys, REDC, 7, 1, glow=True)
    for d_, lab in (("2018-10-01", "OCT"), ("2018-11-01", "NOV"), ("2018-12-03", "DEC"), ("2019-01-02", "JAN")):
        text(ctx, lab, bx + (di(d_) - I_FS) / (I_FE - I_FS) * bw, by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    i_s = SELLS[3]
    if i_s <= up:
        sx = bx + (i_s - I_FS) / (I_FE - I_FS) * bw
        ctx.new_path(); ctx.arc(sx, yy(DDN[i_s - 1]), 12, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(REDC)); ctx.fill()
        text(ctx, "SOLD", sx, yy(DDN[i_s - 1]) - 22, 26, REDC, 1, HEAD, True, "center", outline=5, ocol=C["ink"])
    if show_cross and up >= I_XMAS:
        sx = bx + (I_XMAS - I_FS) / (I_FE - I_FS) * bw; sy = yy(DDN[I_XMAS])
        r = 26 + 6 * math.sin(t * 8)
        ctx.new_path(); ctx.arc(sx, sy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD)); ctx.set_line_width(7); ctx.stroke()
    return xs[-1], ys[-1]


def s_fall(ctx, t, s0, s1):
    bg_fill(ctx, (0x14, 0x10, 0x2A), (0x04, 0x03, 0x0A))
    stars(ctx, t, 30, 160, 1150, 9, 0.5)
    up = race_idx(t, [(s0 + 0.2, I_FS + 2), (T["December"] + 0.4, di("2018-12-21"))])
    x, y = dd_chart(ctx, t, up)
    q = 1 + 0.12 * math.sin(t * 7)
    ctx.save(); ctx.translate(x + 40, y + 10); ctx.scale(q, q)
    text(ctx, "?", 0, 0, 90, GOLD, 1, HEAD, True, "center", outline=10, ocol=C["ink"]); ctx.restore()
    tag(ctx, 540, 450, "FALL 2018: ANOTHER SLIDE", C["white"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    bunting(ctx, "LATE 2018", t, s0, [C["blue"], C["ink"], REDC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


def cal_page(ctx, cx, cy, s, top, big, a=1.0, rot=-0.06):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -150, -160, 300, 320, C["white"], a, 16, border=C["ink"])
    rect(ctx, -150, -160, 300, 80, REDC, a)
    text(ctx, top, 0, -105, 44, C["white"], a, HEAD, True, "center")
    text(ctx, big, 0, 90, 170, C["ink"], a, HEAD, True, "center")
    ctx.restore()


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x18), (0x02, 0x08, 0x05))
    stars(ctx, t, 40, 160, 1200, 7, 0.6)
    if t < T["SPY2"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER THAT", W / 2, 470, 140, C["white"], r, 960, 0, 14)
        big_title(ctx, "CHRISTMAS EVE?", W / 2, 630, 140, GOLD, r, 980, 0, 14)
        cal_page(ctx, 300, 940, 0.9 * back(prog(t, s0 + 0.2, 0.35)) + 1e-3, "DEC 2018", "24", 1, -0.08 + 0.03 * math.sin(t * 4))
        xmas_tree(ctx, 780, 1020, 0.85, t)
    else:
        up = race_idx(t, [(T["SPY2"], di("2018-12-21")), (T["two1"] + 0.2, I_XMAS), (T["cheap"] + 0.3, di("2019-01-10"))])
        dd_chart(ctx, t, up, show_cross=t > T["two1"])
        tag(ctx, 540, 450, "DEC 24, 2018 · SPY CLOSE", C["cream"], back(prog(t, T["SPY2"] - 0.1, 0.3)), 40, -0.03, C["ink"])
        if t > T["twenty3"] - 0.1:
            pp = back(prog(t, T["twenty3"] - 0.1, 0.35))
            ctx.save(); ctx.translate(540, 1070); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, "-20.2%", 0, 0, 150, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
            ctx.restore()
        if t > T["Two2"] - 0.1:
            tag(ctx, 300, 1170, "LINE: -20%", GRNC, back(prog(t, T["Two2"] - 0.1, 0.3)), 34, -0.03, C["ink"])
            tag(ctx, 780, 1170, "PAST IT BY 0.2", GOLD, back(prog(t, T["tenths1"] - 0.1, 0.3)), 34, 0.03, C["ink"])
        if t > T["cheap"] - 0.15:
            stamp_box(ctx, ["BOUGHT BACK", f"{XMAS_CHEAPER}% CHEAPER"], 540, 690, T["cheap"] - 0.1, t, STAMP_GR, 640, 60, -0.06)
        text(ctx, "SPY PRICE (S&P INDEX THAT DAY: -19.8%)", 945, 592, 20, C["white"], 0.75, MONO, True, "right", outline=4, ocol=C["ink"])
    bunting(ctx, "CHRISTMAS EVE", t, s0, [C["green"], C["ink"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("shock" if t > T["two1"] else "smug") if e != "talk" else e, prop=prop_magnifier if t < T["tenths1"] else None)


I_20A, I_20B = di("2020-02-03"), di("2020-04-30")
I_22A, I_22B = di("2022-01-03"), di("2022-07-29")


def s_more(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GRNC, 0.12)
    k1 = prog(t, s0 + 0.1, 1.2); k2 = prog(t, T["twentytwo"] - 0.2, 1.2)
    zoom_chart(ctx, (140, 470, 360, 300), I_20A, I_20B, k1, t,
               [(SELLS[4], "SELL", REDC, s0 + 0.5), (BUYS[4], "BUY", GRNC, s0 + 0.8)], labels=(("2020", "2020-03-16"),))
    if t > T["twentytwo"] - 0.3:
        zoom_chart(ctx, (580, 470, 360, 300), I_22A, I_22B, k2, t,
                   [(SELLS[5], "SELL", REDC, T["twentytwo"] + 0.2), (BUYS[5], "BUY", GRNC, T["twentytwo"] + 0.5)], labels=(("2022", "2022-04-14"),))
    if t > T["bargains"] - 0.15:
        tag(ctx, 540, 900, "TWO MORE BARGAINS", GRNC, back(prog(t, T["bargains"] - 0.15, 0.3)), 50, -0.03, C["ink"])
    bunting(ctx, "2020 + 2022", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def footnote(ctx, t):
    if t >= T["Move"] - 0.1:
        a = back(prog(t, T["Move"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -470, -42, 940, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"LINE -20.2%: {money(LINE202)} · -8%/-20%: {money(SCAN['0.08/0.2'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 890, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 IN SPY · 2005 TO 2024", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "B: RIDE IT OUT", money(HOLD_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "A: BAIL AT -10%", money(RULE_V), LCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["IT WON.", "THANKS TO ONE NIGHT"], W / 2, 520, T["won"] - 0.1, t, STAMP_OR, 820, 76, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["loses"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #37", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "news": s_news, "rules": s_rules, "y2008": s_y2008,
            "miss": s_miss, "fall": s_fall, "remember": s_remember, "more": s_more, "score": s_score, "verdict": s_verdict,
            "loop": s_loop}


# ================================================================ #37 overrides (2x the S&P: twice the money?)
LCOL = (0xFF, 0x6B, 0x3D)   # 2X FUND (hot orange)


def prop_tag37(ctx, x, y, px, t):
    sw = math.sin(t * 4) * 0.15
    ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + 70, y - 120)
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
    price_tag(ctx, x + 70, y - 190, 0.62, "2X", GOLD, C["ink"], 1, -1.35 + sw)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #37", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(TWO_V), 805, 78, fit(ctx, money(TWO_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["vanished"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 3)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 8, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "smug", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "race", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("1X: THE S&P", HCOL), ("2X DAILY FUND", LCOL))):
        rect(ctx, bx + bw - 300, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 265, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2015-06-30")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x2A, 0x16, 0x06), (0x08, 0x04, 0x02))
    god_rays(ctx, W / 2, 520, t, 0.09, GOLD, 14, 1400)
    for k in range(26):
        u = ((t * 0.6) + k / 26) % 1
        rect(ctx, (k * 157) % W, 1700 - u * 1800, 5, 5, GOLD, 0.25)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 470); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "2X", 0, 0, 420, GOLD, 1, HEAD, True, "center", outline=30, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 650); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "THE S&P", 0, 0, 170, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 860); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "2X THE MONEY?", 0, 0, fit(ctx, "2X THE MONEY?", 150, 980), REDC, 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= T["money"] - 0.1:
        tag(ctx, 540, 990, "20 YEARS · $10,000", C["cream"], back(prog(tl, T["money"] - 0.1, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "race", lambda e: "shock" if e != "talk" else e, prop=prop_tag37)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "race", lambda e: "shock", prop=prop_tag37)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE MARCH"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "MARCH 20??", 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def ab_cards2(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "RICH", "", GRNC, -230, ta), ("B", "WRECKED", "", REDC, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -135, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, 30, fit(ctx, l1, 80, 250), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["ahead"], di("2005-12-30")), (SC["crash"], di("2007-10-09"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Keep"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards2(ctx, t, T["A"] - 0.5, T["B"] - 0.1, 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["one"] - 0.15, 0.35)) if "one" in T else back(prog(t, T["March"] - 0.4, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    if t < T["B"] - 0.2:
        price_tag(ctx, 540, 860, 1.4 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "2X", GOLD, C["ink"], 1, -0.1 + 0.05 * math.sin(t * 5))
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


def cal_page37(ctx, cx, cy, s, top, big, a=1.0, rot=-0.06):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -150, -160, 300, 320, C["white"], a, 16, border=C["ink"])
    rect(ctx, -150, -160, 300, 80, REDC, a)
    text(ctx, top, 0, -105, fit(ctx, top, 44, 280), C["white"], a, HEAD, True, "center")
    text(ctx, big, 0, 90, fit(ctx, big, 170, 270), C["ink"], a, HEAD, True, "center")
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "WATCH ONE MARCH", W / 2, 425, 110, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["March"] - 0.15, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


def s_setup(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("$10,000", "IN THE S&P", HCOL, 290, T["One"]),
                                                 ("$10,000", "IN A 2X FUND", LCOL, 790, T["other"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, -12, fit(ctx, title, 70, 420), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 62, fit(ctx, l1, 60, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t < T["One"] - 0.2:
        for k in range(2):
            pk = back(prog(t, T["ten"] - 0.1 + k * 0.2, 0.3))
            if pk > 0:
                coin(ctx, 380 + k * 320, 460, 80 * pk + 1e-3, t + k)
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    if t > T["twice"] - 0.1:
        pp = back(prog(t, T["twice"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1050); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
        card(ctx, -400, -60, 800, 120, (0x05, 0x05, 0x05), 0.92, 20, shadow=False, border=GOLD)
        s_ = "S&P +1%  =  FUND +2%" if t < T["every"] - 0.1 else "RESET EVERY DAY"
        text(ctx, s_, 0, 22, fit(ctx, s_, 64, 740), GOLD, 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE SETUP", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def s_ahead(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2006 - 2007", C["white"], back(prog(t, s0 + 0.05, 0.3)), 46, -0.03, C["ink"])
    if t > T["ahead"] - 0.4:
        tag(ctx, 540, 530, "THE 2X FUND PULLS AHEAD", GRNC, back(prog(t, T["ahead"] - 0.4, 0.3)), 44, 0.02, C["ink"])
    bunting(ctx, "EASY MONEY", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def day_bars(ctx, t, t0, x0, y0, a=1.0):
    for k, (lab, v, col) in enumerate((("S&P", -1, HCOL), ("2X", -2, LCOL))):
        pk = ease(prog(t, t0 + k * 0.35, 0.35))
        if pk <= 0:
            continue
        x = x0 + k * 220
        hh = 60 * (-v) * pk
        rect(ctx, x, y0, 140, hh, col, a)
        text(ctx, f"{v}%", x + 70, y0 + hh + 60, 56, col, a, HEAD, True, "center", outline=8, ocol=C["ink"])
        text(ctx, lab, x + 70, y0 - 16, 36, C["white"], a, HEAD, True, "center", outline=6, ocol=C["ink"])


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.2, di("2007-10-09")), (T["him"] + 0.4, di("2008-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008", C["red"], back(prog(t, T["eight"] - 0.15, 0.3)), 56, -0.03, C["white"])
    if t > T["Every"] - 0.15:
        tag(ctx, 540, 530, "EVERY DROP, DOUBLED", LCOL, back(prog(t, T["Every"] - 0.15, 0.3)), 46, 0.02, C["ink"])
        day_bars(ctx, t, T["Every"] + 0.2, 600, 1330)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x10), (0x06, 0x02, 0x04))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["Two3"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 470, 150, C["white"], r, 960, 0, 14)
        big_title(ctx, "THAT MARCH?", W / 2, 640, 150, GOLD, r, 980, 0, 14)
        cal_page37(ctx, 540, 960, 0.9 * back(prog(t, s0 + 0.2, 0.35)) + 1e-3, "MARCH 20??", "?", 1, -0.06 + 0.03 * math.sin(t * 4))
    else:
        pts = [(T["Two3"], di("2008-12-31")), (T["nine"] + 0.4, I_LOW)]
        race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
        cal_page37(ctx, 230, 470, 0.55 * back(prog(t, T["Two3"] - 0.1, 0.35)) + 1e-3, "MARCH 2009", "9", 1, -0.1)
        if t > T["His"] - 0.1:
            tag(ctx, 640, 440, "HIS $10,000...", C["white"], back(prog(t, T["His"] - 0.1, 0.3)), 44, 0.03, C["ink"])
        if t > T["shrunk"] + 0.2:
            pp = back(prog(t, T["shrunk"] + 0.2, 0.35))
            ctx.save(); ctx.translate(540, 1110); ctx.rotate(-0.04); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, money(LOW_V), 0, 0, 160, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
            ctx.restore()
        if t > T["hundred"] + 0.2:
            tag(ctx, 640, 530, "-75% OF WHAT HE PUT IN", GOLD, back(prog(t, T["hundred"] + 0.2, 0.3)), 34, 0.03, C["ink"])
    bunting(ctx, "MARCH 2009", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: ("shock" if t > T["shrunk"] else "sad") if e != "talk" else e)


def s_behind(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x22), (0x04, 0x05, 0x0A))
    pts = [(s0 + 0.1, I_LOW), (T["fourteen"] + 0.2, I_AHEAD)]
    race_chart(ctx, t, race_idx(t, pts), XE2, years=(2005, 2009, 2013))
    tag(ctx, 540, 440, "STILL BEHIND THE S&P...", C["white"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    if t > T["fourteen"] - 0.15:
        tag(ctx, 540, 530, "...UNTIL MARCH 2014", GOLD, back(prog(t, T["fourteen"] - 0.15, 0.3)), 48, 0.02, C["ink"])
    hourglass(ctx, 860, 1480, 0.6, t)
    bunting(ctx, "5 YEARS LATER", t, s0, [C["grey"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


def s_bull(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x2A, 0x1C), (0x02, 0x0A, 0x06))
    for k in range(24):
        u = ((t - s0) * 0.5 + k / 24) % 1
        rect(ctx, (k * 173) % W, 1300 - u * 1300, 6, 30, GRNC, 0.12)
    pts = [(s0 + 0.1, I_AHEAD), (T["doubled"] + 0.3, di("2014-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2014-12-31"), years=(2005, 2009, 2013))
    tag(ctx, 540, 440, "THE BULL MARKET...", C["white"], back(prog(t, s0 + 0.05, 0.3)), 46, -0.03, C["ink"])
    if t > T["doubled"] - 0.15:
        tag(ctx, 540, 530, "...DOUBLED", GRNC, back(prog(t, T["doubled"] - 0.15, 0.3)), 56, 0.02, C["ink"])
    bunting(ctx, "THE BULL RUN", t, s0, [GOLD, C["ink"], C["green"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e)


def year_bars(ctx, t, t0, x0, y0, r1, r2, lab_):
    for k, (lab, v, col) in enumerate((("S&P", r1, HCOL), ("2X", r2, LCOL))):
        pk = ease(prog(t, t0 + k * 0.35, 0.4))
        if pk <= 0:
            continue
        x = x0 + k * 300
        hh = 600 * (-v) * pk
        rect(ctx, x, y0, 200, hh, col)
        text(ctx, f"{v * 100:.0f}%", x + 100, y0 + hh + 70, 70, col, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        text(ctx, lab, x + 100, y0 - 20, 44, C["white"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])


def s_y2022(ctx, t, s0, s1):
    rain_bg(ctx, t)
    tag(ctx, 540, 450, "2022", C["red"], back(prog(t, s0 + 0.05, 0.3)), 60, -0.03, C["white"])
    year_bars(ctx, t, s0 + 0.3, 290, 640, R22[0], R22[1], "2022")
    if t > T["brutal"] - 0.15:
        tag(ctx, 540, 1040, "BRUTAL AGAIN", REDC, back(prog(t, T["brutal"] - 0.15, 0.3)), 46, 0.03, C["white"])
    bunting(ctx, "2022", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


def s_costs(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x14, 0x06), (0x06, 0x04, 0x02))
    tag(ctx, 540, 450, "THE HIDDEN COSTS", GOLD, back(prog(t, s0 + 0.05, 0.3)), 52, -0.03, C["ink"])
    for k, (l1, l2, col) in enumerate((("FUND FEE", "0.89% A YEAR", LCOL), ("BORROWING", "T-BILL RATE", REDC))):
        pk = back(prog(t, s0 + 0.4 + k * 0.4, 0.35))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(290 + k * 500, 680); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -225, -100, 450, 200, col, 1, 22, border=C["ink"])
        text(ctx, l1, 0, -10, fit(ctx, l1, 66, 400), C["ink"], 1, HEAD, True, "center")
        text(ctx, l2, 0, 60, fit(ctx, l2, 50, 400), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    for k in range(12):
        u = ((t - s0) * 0.8 + k / 12) % 1
        coin(ctx, 120 + (k * 89) % 840, 860 + u * 260, 30, t + k, 1 - u)
    if t > T["every"] - 0.1 and t > T["day2"] - 0.2:
        tag(ctx, 540, 1150, "EVERY SINGLE DAY", C["white"], back(prog(t, T["day2"] - 0.2, 0.3)), 40, 0.03, C["ink"])
    bunting(ctx, "THE CUT", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def footnote(ctx, t):
    if t >= T["But"] - 0.1:
        a = back(prog(t, T["But"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -470, -42, 940, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"2X LOW: {money(LOW_V)} (MAR 2009) · 3X FUND: {money(THREE_V)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 890, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "1X: THE S&P", money(ONE_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "2X DAILY FUND", money(TWO_V), LCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["TWICE THE MONEY.", "AFTER A -75% HOLE."], W / 2, 520, T["Twice3"] - 0.05, t, STAMP_OR, 880, 70, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["vanished"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #38", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "clue": s_clue, "setup": s_setup, "ahead": s_ahead, "crash": s_crash,
            "remember": s_remember, "behind": s_behind, "bull": s_bull, "y2022": s_y2022, "costs": s_costs,
            "score": s_score, "verdict": s_verdict, "loop": s_loop}

# ================================================================ #39 overrides (dividends: pocket the checks or reinvest?)
LCOL = (0xFF, 0x8A, 0x2B)   # POCKETS (orange)
HCOL = (0x4F, 0xC3, 0xF7)   # REINVESTS (blue)
CHKC = (0xF4, 0xEB, 0xD0)


def dcheck(ctx, cx, cy, s, amount="$??", date="", a=1.0, rot=-0.06, glow=False):
    """a generic dividend check (original drawing)"""
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    if glow:
        ctx.save(); ctx.set_source_rgba(1, 0.82, 0.3, 0.35); rrect(ctx, -270, -140, 540, 280, 30); ctx.fill(); ctx.restore()
    card(ctx, -240, -115, 480, 230, CHKC, a, 14, border=C["ink"])
    rect(ctx, -240, -115, 480, 40, GRNC, a)
    text(ctx, "DIVIDEND", -220, -84, 30, C["ink"], a, HEAD, True, "left")
    text(ctx, date, 220, -84, 26, C["ink"], a, MONO, True, "right")
    text(ctx, "PAY TO: YOU", -220, -20, 28, C["ink"], a, MONO, True, "left")
    card(ctx, 40, -50, 180, 70, C["white"], a, 8, shadow=False, border=C["ink"])
    text(ctx, amount, 130, 0, fit(ctx, amount, 52, 160, HEAD), (0x0B, 0x8A, 0x4C), a, HEAD, True, "center")
    for k in range(3):
        rect(ctx, -220, 40 + k * 22, 300 - k * 70, 6, C["ink"], 0.35 * a)
    ctx.new_path(); ctx.move_to(110, 80); ctx.curve_to(140, 50, 170, 100, 210, 70)
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def check_rain(ctx, t, n=14, a=0.55):
    for k in range(n):
        u = ((t * 0.16) + k / n) % 1
        x = (k * 197) % W + math.sin(t * 1.1 + k) * 30
        dcheck(ctx, x, -100 + u * 2100, 0.22, "$", "", a, math.sin(t + k) * 0.5)


def prop_check(ctx, x, y, px, t):
    dcheck(ctx, x + 70, y - 170 + math.sin(t * 3) * 8, 0.42, "$", "", 1, -0.25 + 0.08 * math.sin(t * 4))


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #39", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(REIN_V), 805, 78, fit(ctx, money(REIN_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["wasnt"] - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 3)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "crown", t, "smug", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "tophat", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("REINVESTS THE CHECKS", HCOL), ("POCKETS THE CHECKS", LCOL))):
        rect(ctx, bx + bw - 360, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 325, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2017-06-30")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x06, 0x2A, 0x1A), (0x02, 0x08, 0x05))
    god_rays(ctx, W / 2, 520, t, 0.08, GRNC, 14, 1400)
    check_rain(ctx, t, 12, 0.45)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 520); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "80", 0, 0, 440, GOLD, 1, HEAD, True, "center", outline=32, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 700); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "CHECKS", 0, 0, 180, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 880); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "20 YEARS", 0, 0, 150, GRNC, 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 1010, "SPY DIVIDENDS · 2005-2024", C["cream"], back(prog(tl, 1.0, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_check)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_check)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE TINY CHECK", hidden="DEC 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def ab_cards3(ctx, t, ta, tb, la, lb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, col, x, tt) in enumerate((("A", la, LCOL, -230, ta), ("B", lb, HCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -135, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, 30, fit(ctx, l1, 80, 250), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["split"], di("2005-12-30")), (SC["y2007"], di("2006-12-29")),
                               (SC["crash"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.4, T["B"] - 0.6, "POCKET", "REINVEST", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["tiny"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1, "ONE TINY CHECK", "DEC 20??"); ctx.restore()
    if t < T["B"] - 0.2:
        dcheck(ctx, 540, 860, 1.1 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "$", "", 1, -0.08 + 0.04 * math.sin(t * 5))
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.5, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


def s_setup(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 440, "$10,000 OF SPY EACH · 2005", C["white"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    if t < T["Every"] - 0.1:
        for k in range(2):
            pk = back(prog(t, T["ten"] - 0.1 + k * 0.25, 0.3))
            if pk > 0:
                coin(ctx, 380 + k * 320, 1100, 60 * pk + 1e-3, t + k)
    else:
        tag(ctx, 540, 530, "EVERY 3 MONTHS: A CHECK", GRNC, back(prog(t, T["Every"] - 0.1, 0.3)), 42, 0.02, C["ink"])
        for k in range(4):
            pk = back(prog(t, T["pays"] - 0.2 + k * 0.12, 0.3))
            if pk > 0:
                dcheck(ctx, 200 + k * 230, 1100, 0.36 * pk + 1e-3, "$", f"Q{k + 1}", 1, -0.1 + k * 0.07)
    bunting(ctx, "THE SETUP", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def share_stack(ctx, cx, cy, s, n, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for k in range(n):
        y = -k * 46
        card(ctx, -120, y - 40, 240, 40, HCOL, a, 8, shadow=False, border=C["ink"])
        text(ctx, "SPY", 0, y - 9, 30, C["ink"], a, HEAD, True, "center")
    ctx.restore()


def s_split(ctx, t, s0, s1):
    bg_fill(ctx, (0x22, 0x18, 0x10), (0x06, 0x04, 0x03))
    stars(ctx, t, 20, 180, 1150, 3, 0.3)
    pk1 = back(prog(t, s0 + 0.05, 0.35))
    if pk1 > 0:
        tag(ctx, 290, 450, "HE: KEEPS THE CASH", LCOL, pk1, 38, -0.03, C["ink"])
        jar(ctx, 290, 760, 0.85 * pk1 + 1e-3, clamp((t - s0) / 2.5) * 0.6, t)
    if t > T["She"] - 0.15:
        pk2 = back(prog(t, T["She"] - 0.15, 0.35))
        tag(ctx, 790, 450, "SHE: BUYS MORE SPY", HCOL, pk2, 38, 0.03, C["ink"])
        n = 1 + int(clamp((t - T["She"]) / 1.5) * 6)
        share_stack(ctx, 790, 960, 1.0 * pk2 + 1e-3, n, t)
    bunting(ctx, "TWO CHOICES", t, s0, [LCOL, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e, prop=prop_check)


def s_y2007(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2005 - 2007", C["white"], back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["ink"])
    if t > T["neck"] - 0.2:
        tag(ctx, 540, 530, "NECK AND NECK", GOLD, back(prog(t, T["neck"] - 0.2, 0.3)), 50, 0.02, C["ink"])
    bunting(ctx, "ROUND 1", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.2, di("2007-12-31")), (T["lead"] - 0.1, I_LOW)]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008 - 2009", C["red"], back(prog(t, s0 + 0.05, 0.3)), 56, -0.03, C["white"])
    if t > T["pile"] - 0.2:
        tag(ctx, 540, 530, "MARCH 2009: HE LEADS", LCOL, back(prog(t, T["pile"] - 0.2, 0.3)), 46, 0.02, C["ink"])
        jar(ctx, 900, 470, 0.32 * back(prog(t, T["pile"] - 0.2, 0.35)) + 1e-3, 0.35, t)
    if t > T["So"] - 0.1:
        pk = back(prog(t, T["So"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1115); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -330, -60, 660, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "POCKETING WINS?", 0, 24, 66, GOLD, 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE CRASH", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "THAT TINY", W / 2, 480, 140, C["white"], r, 960, 0, 14)
    big_title(ctx, "CHECK.", W / 2, 640, 150, GOLD, r, 980, 0, 14)
    amt = "$??" if t < T["fiftynine"] - 0.1 else f"${CHK_V:.0f}"
    dt = "" if t < T["December"] - 0.1 else "DEC 19, 2008"
    pg = back(prog(t, s0 + 0.2, 0.35))
    dcheck(ctx, 540, 930, 1.25 * pg + 1e-3, amt, dt, 1, -0.05 + 0.02 * math.sin(t * 4), glow=t > T["fiftynine"] - 0.1)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


QB0, QB1 = di("2008-06-02"), di("2009-12-31")
QBI = di(CHK_D)


def bottom_chart(ctx, t, up_k, x0, y0, w, h, a=1.0):
    seg = RAWC[QB0:QB1 + 1]
    vmin, vmax = seg.min() * 0.92, seg.max() * 1.05
    card(ctx, x0 - 20, y0 - 20, w + 40, h + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    n = int((QB1 - QB0) * up_k) + 1
    xs = [x0 + k / (QB1 - QB0) * w for k in range(n)]
    ys = [y0 + h - (seg[k] - vmin) / (vmax - vmin) * h for k in range(n)]
    if n > 1:
        poly(ctx, xs, ys, C["white"], 5, a, glow=False)
    for yr, d_ in ((2008, "2008-06-02"), (2009, "2009-01-02")):
        text(ctx, str(yr), x0 + (di(d_) - QB0) / (QB1 - QB0) * w + 40, y0 + h + 40, 24, C["white"], 0.7, MONO, True, "center")
    kk = QBI - QB0
    if n > kk:
        px_ = x0 + kk / (QB1 - QB0) * w; py_ = y0 + h - (seg[kk] - vmin) / (vmax - vmin) * h
        rr = 16 + 4 * math.sin(t * 8)
        ctx.arc(px_, py_, rr, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD, a)); ctx.fill()
        tag(ctx, px_ + 10, py_ - 70, "SHE BUYS HERE", GOLD, back(prog(t, T["bought"], 0.3)), 30, 0.03, C["ink"])


def s_bottom(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    tag(ctx, 540, 440, "SPY PRICE · 2008-2009", C["white"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    bottom_chart(ctx, t, ease(prog(t, s0 + 0.1, 1.2)), 130, 520, 820, 300)
    if t > T["By"] - 0.1:
        pk = back(prog(t, T["By"] - 0.1, 0.35))
        dcheck(ctx, 280, 1030, 0.42 * pk + 1e-3, f"${CHK_V:.0f}", "2008", 1, -0.1)
        text(ctx, "BY 2024", 540, 1000, 44 * pk + 1, C["white"], 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        arrow_up(ctx, 540, 1060, 0.3 * pk + 0.01, GRNC) if False else None
    if t > T["five2"] - 0.1:
        pk = back(prog(t, T["five2"] - 0.1, 0.35))
        ctx.save(); ctx.translate(800, 1050); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, "$" + f"{round(CHK_G):,}", 0, 0, 130, GOLD, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
    if t > T["five2"] - 0.1:
        god_rays(ctx, 800, 1010, t, 0.05, GOLD, 10, 500)
    bunting(ctx, "NEAR THE BOTTOM", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("shock" if t > T["thirty"] else "smug") if e != "talk" else e)


def s_every(ctx, t, s0, s1):
    bg_fill(ctx, (0x06, 0x22, 0x16), (0x02, 0x08, 0x05))
    pts = [(s0 + 0.1, I_LOW), (T["years2"] + 0.3, di("2016-12-30"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2016-12-30"), years=(2005, 2010, 2015))
    tag(ctx, 540, 440, "EVERY CHECK, QUIETLY", GRNC, back(prog(t, s0 + 0.05, 0.3)), 46, -0.03, C["ink"])
    for k in range(80):
        pk = ease(prog(t, s0 + 0.2 + k * 0.035, 0.2))
        if pk <= 0:
            continue
        x = 130 + (k % 20) * 42; y = 1000 + (k // 20) * 34
        rect(ctx, x, y, 34 * pk, 24, GRNC if k % 2 else (0x16, 0xB0, 0x6A), 1)
    bunting(ctx, "20 YEARS", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "smug" if e != "talk" else e)


def s_jar(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x16, 0x06), (0x08, 0x04, 0x02))
    for k in range(12):
        u = ((t - s0) * 0.8 + k / 12) % 1
        coin(ctx, 120 + (k * 89) % 840, 460 + u * 500, 28, t + k, 1 - u)
    tag(ctx, 540, 440, "HIS 80 CHECKS, ADDED UP", LCOL, back(prog(t, s0 + 0.05, 0.3)), 42, -0.03, C["ink"])
    pk = back(prog(t, s0 + 0.15, 0.35))
    jar(ctx, 540, 760, 1.0 * pk + 1e-3, 0.95, t, money(JAR_V) if t > T["sixtyeight"] - 0.1 else None)
    bunting(ctx, "THE CASH JAR", t, s0, [LCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def footnote(ctx, t):
    if t >= T["The"] - 0.1:
        a = back(prog(t, T["The"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -470, -42, 940, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"HIS CHECKS: {money(JAR_V)} · HERS, REINVESTED: {money(REIN_V - SHARES_V)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 38, 890, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 OF SPY · 2005 TO 2024", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "POCKETED THE CHECKS", money(POCK_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "REINVESTED THEM", money(REIN_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "FINAL TALLY", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["THE CHECKS WERE SMALL.", "WHAT THEY GREW INTO WASN'T."], W / 2, 540, T["The"] - 0.05, t, STAMP_GR, 940, 62, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["grew"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #40", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e, prop=prop_check if t > T["grew"] else None)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "setup": s_setup, "split": s_split, "y2007": s_y2007, "crash": s_crash,
            "remember": s_remember, "bottom": s_bottom, "every": s_every, "jar": s_jar, "score": s_score, "verdict": s_verdict,
            "loop": s_loop}


# ================================================================ #40 overrides (sell the +2% opening pop, back in a week?)
LCOL = (0xFF, 0x8A, 0x2B)   # SELLS THE POP (orange)
HCOL = (0x4F, 0xC3, 0xF7)   # HOLDS (blue)
BALC = (0x22, 0xE5, 0x8B)


def balloon(ctx, cx, cy, s, label="+2%", t=0.0, a=1.0, col=BALC, string=True):
    """a party balloon with a label (original drawing)"""
    ctx.save(); ctx.translate(cx, cy + math.sin(t * 3 + cx) * 6); ctx.scale(s, s)
    if string:
        ctx.new_path(); ctx.move_to(0, 120)
        ctx.curve_to(-20, 170, 20, 210, 0, 260); ctx.set_source_rgba(*rgba(C["white"], 0.8 * a)); ctx.set_line_width(4); ctx.stroke()
    ctx.save(); ctx.scale(1, 1.18); ctx.new_path(); ctx.arc(0, 0, 100, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(14); ctx.stroke_preserve()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill()
    ctx.new_path(); ctx.move_to(-14, 128); ctx.line_to(14, 128); ctx.line_to(0, 112); ctx.close_path()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill()
    ctx.save(); ctx.scale(1, 1.3); ctx.new_path(); ctx.arc(-42, -40, 18, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 0.45 * a); ctx.fill()
    text(ctx, label, 0, 26, fit(ctx, label, 78, 170, HEAD), C["ink"], a, HEAD, True, "center")
    ctx.restore()


def prop_balloon(ctx, x, y, px, t):
    sw = math.sin(t * 2.6) * 10
    ctx.new_path(); ctx.move_to(x, y); ctx.curve_to(x + 30, y - 80, x + 60 + sw, y - 140, x + 70 + sw, y - 200)
    ctx.set_source_rgba(*rgba(C["white"], 0.9)); ctx.set_line_width(4); ctx.stroke()
    balloon(ctx, x + 70 + sw, y - 330, 0.62, "+2%", t, 1, BALC, False)


def balloon_rise(ctx, t, n=10, a=0.35):
    cols = [BALC, GOLD, HCOL, LCOL]
    for k in range(n):
        u = ((t * 0.09) + k / n) % 1
        x = (k * 211) % W + math.sin(t * 0.9 + k) * 30
        balloon(ctx, x, 2050 - u * 2300, 0.3, "", t + k, a, cols[k % 4], True)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #40", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["more"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    for si in SELL_I:
        if s0_ <= si <= up:
            sx = sx_of(si, s0_, xe, RBOX)
            rect(ctx, sx - 2, by + bh - 26, 4, 26, LCOL, 0.9 * a)
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 3)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "party", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("HOLDS", HCOL), ("SELLS THE POP", LCOL))):
        rect(ctx, bx + bw - 300, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 265, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2020-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x06, 0x2A, 0x1A), (0x02, 0x08, 0x05))
    god_rays(ctx, W / 2, 480, t, 0.08, GRNC, 14, 1400)
    balloon_rise(ctx, t, 9, 0.35)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 500); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "48", 0, 0, 460, GOLD, 1, HEAD, True, "center", outline=32, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 700); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "BIG OPENING", 0, 0, 150, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 880); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "POPS", 0, 0, 190, GRNC, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 1010, "SPY OPENS +2% OR MORE · 2005-2024", C["cream"], back(prog(tl, 1.0, 0.3)), 30, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_balloon)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_balloon)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE SPRING TUESDAY", hidden="MAR ??, 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["news"], di("2005-12-30")), (SC["rules"], di("2006-12-29")),
                               (SC["y2008"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Mark"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.45, T["B"] - 0.5, "SELL", "HOLD", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Mark"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    if t < T["B"] - 0.2:
        balloon(ctx, 540, 850, 1.1 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, "+2%", t)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Mark"] else None)


def s_news(ctx, t, s0, s1):
    bg_fill(ctx, (0x08, 0x26, 0x18), (0x02, 0x06, 0x04))
    for k in range(3):
        rect(ctx, 0, 300 + k * 6, W, 3, GRNC, 0.25)
    ticker = "S&P 500 FUTURES +2.2% TO +2.6%  ·  LAST WEEK S&P 500 -8.6%  ·  7 RED DAYS IN A ROW  ·  "
    xo = -((t - s0) * 260) % 1700
    rect(ctx, 0, 1760, W, 64, (0x05, 0x05, 0x05), 0.9)
    for j in range(3):
        text(ctx, ticker, xo + j * 1700, 1805, 34, GOLD, 1, MONO, True, "left")
    tag(ctx, 540, 450, "TODAY · BEFORE THE OPENING BELL", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    p = back(prog(t, T["futures"] - 0.1, 0.35))
    big_title(ctx, "S&P FUTURES: +2%", W / 2, 620, 150, GRNC, p, 980, -0.03, 16)
    if t < T["seven"] - 0.15:
        balloon(ctx, 760, 880, 0.9 * back(prog(t, T["two"] - 0.1, 0.35)) + 1e-3, "+2%", t)
        arrow_up(ctx, 330, 900 + math.sin(t * 6) * 10, 0.5 * back(prog(t, T["two"] - 0.1, 0.35)) + 1e-3, GRNC)
    if t > T["seven"] - 0.15:
        red_streak(ctx, 200, 790, t, T["seven"] - 0.15, 7, 0.82, 1, 0.09)
        tag(ctx, 540, 1110, "AFTER 7 STRAIGHT RED DAYS", REDC, back(prog(t, T["red"] - 0.1, 0.3)), 44, 0.02, C["white"])
    bunting(ctx, "THE NEWS", t, s0, [GRNC, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("SELL", "OPENS +2%? AT THAT OPEN", LCOL, 290, T["SPY"]),
                                                 ("BUY BACK", "1 WEEK LATER", HCOL, 790, T["Buy"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 465); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -105, 470, 210, col, 1, 22, border=C["ink"])
        (arrow_down if k == 0 else arrow_up)(ctx, -170, -20, 0.28, C["ink"])
        text(ctx, title, 40, -10, fit(ctx, title, 76, 300), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 0, 66, fit(ctx, l1, 46, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 1100, "$10,000 · FEES INCLUDED", C["white"], back(prog(t, T["week"], 0.3)), 34, -0.02, C["ink"])
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_coin)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-12-31")), (T["ahead"] + 0.2, di("2008-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: HE SELLS THE POPS", C["white"], back(prog(t, s0 + 0.2, 0.3)), 44, -0.03, C["ink"])
    if t > T["ahead"] - 0.2:
        tag(ctx, 540, 530, "HE'S AHEAD", LCOL, back(prog(t, T["ahead"] - 0.2, 0.3)), 56, 0.02, C["ink"])
    bunting(ctx, "ROUND 1", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_trails(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x05, 0x0C))
    stars(ctx, t, 30, 180, 1200, 9, 0.4)
    pts = [(s0 + 0.1, di("2008-12-31")), (T["trails"] + 0.4, di("2019-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2019-12-31"), years=(2005, 2010, 2015, 2020))
    tag(ctx, 540, 440, "THE REBOUND", HCOL, back(prog(t, T["rebound"] - 0.1, 0.3)), 50, -0.03, C["ink"])
    if t > T["For"] - 0.15:
        tag(ctx, 540, 530, "FOR YEARS: BEHIND", C["white"], back(prog(t, T["For"] - 0.15, 0.3)), 50, 0.02, C["ink"])
    bunting(ctx, "ROUND 2", t, s0, [HCOL, C["ink"], C["grey"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


QA0, QA1 = di("2020-02-18"), di("2020-03-20")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x30, 0x0A, 0x12), (0x06, 0x02, 0x04))
    tag(ctx, 540, 440, "2020: THE CRASH", REDC, back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["white"])
    k = ease(prog(t, s0 + 0.2, T["cheaper2"] - s0))
    zoom_chart(ctx, (130, 560, 820, 360), QA0, QA1, k, t,
               [(I_S10, "SELL", LCOL, T["sells"] if False else T["He"]), (I_B17, "BUY", GRNC, T["cheaper2"] - 0.1)],
               labels=(("FEB", "2020-02-24"), ("MAR", "2020-03-09")))
    if t > T["front"] - 0.2:
        pk = back(prog(t, T["front"] - 0.2, 0.35))
        ctx.save(); ctx.translate(540, 1090); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -360, -60, 720, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "BACK IN FRONT!", 0, 26, 74, LCOL, 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "ROUND 3", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "THAT SPRING", W / 2, 470, 140, C["white"], r, 960, 0, 14)
    big_title(ctx, "TUESDAY.", W / 2, 620, 150, GOLD, r, 980, 0, 14)
    if t > T["March"] - 0.15:
        pk = back(prog(t, T["March"] - 0.15, 0.35))
        cal_page(ctx, 300, 900, 0.95 * pk + 1e-3, "MAR 2020", "24" if t > T["twentyfourth"] - 0.1 else "??", 1, -0.06)
        tag(ctx, 300, 1110, "TUESDAY", C["cream"], pk, 34, 0.03, C["ink"])
    if t > T["five"] - 0.15:
        pk = back(prog(t, T["five"] - 0.15, 0.35))
        balloon(ctx, 780, 860, 0.95 * pk + 1e-3, f"+{GAP24 * 100:.1f}%", t)
        tag(ctx, 780, 1110, "SPY OPENS", GRNC, pk, 36, -0.03, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["five"]) else e)


QB0_, QB1_ = di("2020-03-16"), di("2020-04-03")


def s_rebuy(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    tag(ctx, 540, 440, "SPY · MARCH 16 - APRIL 3, 2020", C["white"], back(prog(t, s0 + 0.05, 0.3)), 36, -0.03, C["ink"])
    k = ease(prog(t, s0 + 0.1, T["pays"] - s0))
    zoom_chart(ctx, (130, 560, 820, 330), QB0_, QB1_, k, t,
               [(I_T24, "SELL", LCOL, T["sells2"] - 0.05), (I_B31, "BUY", REDC, T["pays"] - 0.1)],
               labels=(("MAR 24", "2020-03-24"), ("MAR 31", "2020-03-31")))
    if t > T["eleven"] - 0.1:
        pk = back(prog(t, T["eleven"] - 0.1, 0.35))
        ctx.save(); ctx.translate(780, 1010); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, f"+{REB24 * 100:.0f}%", 0, 0, 130, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
        tag(ctx, 780, 1080, "TO GET BACK IN", C["white"], pk, 32, 0.03, C["ink"])
    if t > T["never"] - 0.15:
        stamp_box(ctx, ["HE NEVER", "LEADS AGAIN"], 340, 1020, T["never"] - 0.1, t, STAMP_OR, 440, 50, -0.06)
    bunting(ctx, "ONE WEEK LATER", t, s0, [C["blue"], C["ink"], REDC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: ("sad" if t > T["eleven"] else "neutral") if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["He4"] - 0.1:
        a = back(prog(t, T["He4"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"SAME RULE, BACK IN 3 DAYS: {money(SC3)} · IN 2 WEEKS: {money(SC10)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024 · 33 SELLS", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "SOLD EVERY POP", money(RULE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "HELD", money(HOLD_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "THE TALLY", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["CHEAPER, 17 OF 33 TIMES.", "HOLDING STILL PAID MORE."], W / 2, 540, T["He4"] - 0.05, t, STAMP_GR, 940, 62, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Holding2"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #41", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "news": s_news, "rules": s_rules, "y2008": s_y2008, "trails": s_trails,
            "y2020": s_y2020, "remember": s_remember, "rebuy": s_rebuy, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #41 overrides (60/40: still the safe bet?)
LCOL = (0xFF, 0x8A, 0x2B)   # ALL STOCKS (orange)  -> HV
HCOL = (0x4F, 0xC3, 0xF7)   # 60/40 (blue)         -> SV
BNDC = (0xFF, 0xD2, 0x4A)   # bonds (gold)


def shield(ctx, cx, cy, s, t, col=HCOL, a=1.0, crack=False, label=None):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.sin(t * 3) * 0.06); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -130); ctx.curve_to(70, -100, 110, -100, 120, -110); ctx.curve_to(125, 20, 80, 100, 0, 150)
    ctx.curve_to(-80, 100, -125, 20, -120, -110); ctx.curve_to(-110, -100, -70, -100, 0, -130); ctx.close_path()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(12); ctx.stroke()
    if label:
        text(ctx, label, 0, 26, fit(ctx, label, 74, 200, HEAD), C["ink"], a, HEAD, True, "center")
    if crack:
        ctx.new_path(); ctx.move_to(10, -130); ctx.line_to(-15, -60); ctx.line_to(20, -10); ctx.line_to(-10, 60); ctx.line_to(5, 150)
        ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def prop_shield(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 40, y - 60)
    if fl:
        ctx.scale(-1, 1)
    shield(ctx, 0, 0, 0.42, t, HCOL, 1, False, "60/40")
    ctx.restore()


def pie(ctx, cx, cy, r, frac, t, a=1.0, la="SPY", lb="BONDS", k=1.0):
    ang0 = -math.pi / 2
    ctx.new_path(); ctx.move_to(cx, cy); ctx.arc(cx, cy, r, ang0, ang0 + 2 * math.pi * frac * k); ctx.close_path()
    ctx.set_source_rgba(*rgba(LCOL, a)); ctx.fill()
    if frac < 1:
        ctx.new_path(); ctx.move_to(cx, cy); ctx.arc(cx, cy, r, ang0 + 2 * math.pi * frac * k, ang0 + 2 * math.pi * k); ctx.close_path()
        ctx.set_source_rgba(*rgba(BNDC, a)); ctx.fill()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(10); ctx.stroke()
    if k >= 1:
        if frac >= 1:
            text(ctx, "100%", cx, cy - 4, 64, C["ink"], a, HEAD, True, "center"); text(ctx, la, cx, cy + 50, 40, C["ink"], a, HEAD, True, "center")
        else:
            text(ctx, f"{frac * 100:.0f}%", cx + r * 0.42, cy + r * 0.1, 50, C["ink"], a, HEAD, True, "center")
            text(ctx, la, cx + r * 0.42, cy + r * 0.1 + 42, 30, C["ink"], a, HEAD, True, "center")
            text(ctx, f"{(1 - frac) * 100:.0f}%", cx - r * 0.45, cy - r * 0.05, 46, C["ink"], a, HEAD, True, "center")
            text(ctx, lb, cx - r * 0.45, cy - r * 0.05 + 38, 26, C["ink"], a, HEAD, True, "center")


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #41", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["bigger"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 3)
    poly(ctx, xs2, ys2, HCOL, 8, 1, glow=True); poly(ctx, xs1, ys1, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "race", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "tophat", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("ALL STOCKS", LCOL), ("60/40", HCOL))):
        rect(ctx, bx + bw - 260, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 225, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2015-12-31"); XE3 = di("2020-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x0A, 0x1E, 0x3A), (0x02, 0x05, 0x0C))
    god_rays(ctx, W / 2, 480, t, 0.08, HCOL, 14, 1400)
    stars(ctx, t, 40, 0, 1500, 4, 0.5)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 520); ctx.rotate(-0.05); ctx.scale(s_, s_)
    text(ctx, "60/40", 0, 0, 380, BNDC, 1, HEAD, True, "center", outline=30, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "STILL SAFE?", 0, 0, 190, C["white"], 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 900, "60% STOCKS · 40% BONDS", C["cream"], back(prog(tl, 1.0, 0.3)), 34, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_shield)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_shield)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE UGLY YEAR", hidden="20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def ab_cards4(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, col, x, tt) in enumerate((("A", "ALL STOCKS", LCOL, -230, ta), ("B", "60/40", HCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -135, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, 30, fit(ctx, l1, 80, 250), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["setup"], di("2005-06-30")), (SC["split"], di("2006-12-29")),
                               (SC["crash"], di("2007-12-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards4(ctx, t, T["A"] - 0.6, T["B"] - 0.9, 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["One"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    if t < T["B"] - 0.2:
        shield(ctx, 540, 860, 1.1 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, t, HCOL, 1, False, "60/40")
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["One"] else None)


def s_setup(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 440, "$10,000 EACH · 2005", C["white"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["ink"])
    race_chart(ctx, t, RACE1(t), XE1, years=(2005, 2007, 2009))
    if t > T["He"] - 0.15:
        pk = back(prog(t, T["He"] - 0.15, 0.35))
        tag(ctx, 540, 530, "HE: 100% SPY", LCOL, pk, 44, 0.03, C["ink"])
    bunting(ctx, "THE SETUP", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_split(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x05, 0x0C))
    stars(ctx, t, 20, 180, 1150, 3, 0.3)
    pk1 = back(prog(t, s0 + 0.05, 0.35))
    tag(ctx, 540, 450, "SHE: 60% SPY · 40% 10-YEAR TREASURIES", HCOL, pk1, 36, -0.03, C["ink"])
    fr = 0.6 if t > T["forty"] - 0.1 else 1.0
    pie(ctx, 540, 760, 230 * pk1 + 1, fr if t > T["sixty"] - 0.1 else 1.0, t, 1, "SPY", "BONDS", ease(prog(t, s0 + 0.1, 0.8)))
    if t > T["rebalances"] - 0.15:
        pk2 = back(prog(t, T["rebalances"] - 0.15, 0.35))
        cal_page(ctx, 250, 1050, 0.5 * pk2 + 1e-3, "EVERY", "JAN", 1, -0.06)
        tag(ctx, 700, 1060, "REBALANCES BACK TO 60/40", GOLD, pk2, 32, 0.03, C["ink"])
    bunting(ctx, "TWO PORTFOLIOS", t, s0, [LCOL, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e, prop=prop_shield)


def bars2(ctx, t, t0, t1, x0, y0, r1, r2, l1, l2, c1, c2, sc=600):
    for k, (lab, v, col, tt) in enumerate(((l1, r1, c1, t0), (l2, r2, c2, t1))):
        pk = ease(prog(t, tt - 0.1, 0.4))
        if pk <= 0:
            continue
        x = x0 + k * 300
        hh = sc * (-v) * pk
        rect(ctx, x, y0, 200, hh, col)
        text(ctx, f"{v * 100:.0f}%", x + 100, y0 + hh + 70, 70, col, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
        text(ctx, lab, x + 100, y0 - 20, 40, C["white"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.2, di("2007-12-31")), (T["lead"] + 0.2, di("2009-12-31"))]
    if t < T["lead"] - 0.2:
        tag(ctx, 540, 440, "2008", C["red"], back(prog(t, s0 + 0.05, 0.3)), 60, -0.03, C["white"])
        bars2(ctx, t, T["thirtyseven"], T["fourteen"], 240, 600, S08, P08, "ALL STOCKS", "60/40", LCOL, HCOL, 900)
    else:
        race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
        tag(ctx, 540, 440, "SHE TAKES THE LEAD", HCOL, back(prog(t, T["lead"] - 0.2, 0.3)), 50, -0.03, C["ink"])
        if t > T["years"] - 0.1:
            tag(ctx, 540, 530, "AND HOLDS IT FOR YEARS", C["white"], back(prog(t, T["years"] - 0.1, 0.3)), 42, 0.02, C["ink"])
    bunting(ctx, "THE CRASH", t, s0, [C["red"], C["ink"], HCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


def s_bull(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    pts = [(s0 + 0.1, di("2009-12-31")), (T["fourteen2"] + 0.3, di("2014-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2014-12-31"), years=(2005, 2010, 2015))
    if t < T["Then2"] - 0.1:
        pk = back(prog(t, T["bonds"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 470); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -300, -60, 600, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "BONDS WIN?", 0, 26, 74, GOLD, 1, HEAD, True, "center")
        ctx.restore()
    else:
        tag(ctx, 540, 440, "THE BULL MARKET RUNS", GRNC, back(prog(t, T["Then2"], 0.3)), 46, -0.03, C["ink"])
        if t > T["passes"] - 0.1:
            tag(ctx, 540, 530, "2014: HE PASSES HER", LCOL, back(prog(t, T["passes"] - 0.1, 0.3)), 46, 0.02, C["ink"])
    bunting(ctx, "ROUND 2", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x30, 0x0A, 0x12), (0x06, 0x02, 0x04))
    pts = [(s0 + 0.1, di("2014-12-31")), (T["front"], di("2020-03-23"))]
    race_chart(ctx, t, race_idx(t, pts), XE3, curtain=di("2020-03-23"), years=(2005, 2010, 2015, 2020))
    tag(ctx, 540, 440, "2020: THE CRASH", REDC, back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["white"])
    if t > T["front"] - 0.1:
        tag(ctx, 540, 530, "SHE'S BACK IN FRONT...", HCOL, back(prog(t, T["front"] - 0.1, 0.3)), 44, 0.02, C["ink"])
    if t > T["briefly"] - 0.1:
        stamp_box(ctx, ["BRIEFLY."], 540, 1110, T["briefly"] - 0.1, t, STAMP_OR, 420, 70, -0.06)
    bunting(ctx, "ROUND 3", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "THE UGLY YEAR:", W / 2, 470, 120, C["white"], r, 960, 0, 14)
    if t > T["twentytwo"] - 0.15:
        big_title(ctx, "2022", W / 2, 640, 190, GOLD, back(prog(t, T["twentytwo"] - 0.15, 0.35)), 980, 0, 16)
    if t > T["Stocks2"] - 0.1:
        bars2(ctx, t, T["eighteen"], 1e9, 240, 780, S22, B22, "STOCKS", "BONDS", LCOL, BNDC, 1500)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["eighteen"]) else e)


def s_shieldsc(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0A, 0x10), (0x06, 0x02, 0x04))
    big_title(ctx, "2022", W / 2, 470, 120, GOLD, 1, 980, 0, 14)
    bars2(ctx, t, -1, T["sixteen"], 240, 600, S22, B22, "STOCKS", "BONDS", LCOL, BNDC, 1500)
    if t > T["shield"] - 0.15:
        pk = back(prog(t, T["shield"] - 0.15, 0.35))
        shield(ctx, 540, 1045, 0.72 * pk + 1e-3, t, HCOL, 1, t > T["cracked"] - 0.05, "60/40")
        if t > T["cracked"] - 0.05:
            tag(ctx, 830, 1100, f"60/40: {P22 * 100:.0f}%", HCOL, back(prog(t, T["cracked"], 0.3)), 38, 0.04, C["ink"])
    bunting(ctx, "THE SHIELD", t, s0, [HCOL, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Her2"] - 0.1:
        a = back(prog(t, T["Her2"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"WORST DROP: 60/40 {MDD_P * 100:.0f}% · STOCKS {MDD_H * 100:.0f}% · 80/20: {money(SC80)}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "60/40", money(RULE_V), HCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "ALL STOCKS", money(HOLD_V), LCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "FINAL COUNT", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["HER WORST DROP: HALF OF HIS.", "HIS ENDING: FAR BIGGER."], W / 2, 540, T["Her2"] - 0.05, t, STAMP_GR, 940, 60, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["His"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #42", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "setup": s_setup, "split": s_split, "crash": s_crash, "bull": s_bull,
            "y2020": s_y2020, "remember": s_remember, "shieldsc": s_shieldsc, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #42 overrides (death cross: sell for a year?)
LCOL = (0xFF, 0x8A, 0x2B)   # SELLS AT THE CROSS (orange) -> SV
HCOL = (0x4F, 0xC3, 0xF7)   # IGNORES IT (blue)           -> HV
SKC = (0xF0, 0x3E, 0x5A)


def xmark_big(ctx, cx, cy, s, col=SKC, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for sgn in (1, -1):
        ctx.new_path(); ctx.move_to(-60, -60 * sgn); ctx.line_to(60, 60 * sgn)
        ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(40); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        ctx.new_path(); ctx.move_to(-60, -60 * sgn); ctx.line_to(60, 60 * sgn)
        ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(24); ctx.stroke()
    ctx.restore()


def cross_chart(ctx, box, i0, i1, k, t, xi=None, a=1.0, labels=()):
    """real SPY price + 50-day (orange) + 200-day (white dashed-ish) averages; red X on the death cross"""
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    seg = np.r_[CL[i0:i1 + 1], M50[i0:i1 + 1], M200[i0:i1 + 1]]
    lo, hi = float(np.nanmin(seg)) * 0.97, float(np.nanmax(seg)) * 1.03
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    xs, ys = series_xy(CL, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, (0x9A, 0xA4, 0xB0), 3, 0.7 * a, glow=False)
    xs, ys = series_xy(M200, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, C["white"], 7, a, glow=True)
    xs, ys = series_xy(M50, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, GOLD, 7, a, glow=True)
    text(ctx, "SHORT-TERM AVG", bx + 10, by + 30, 24, GOLD, a, MONO, True, "left")
    text(ctx, "LONG-TERM AVG", bx + 10, by + 60, 24, C["white"], a, MONO, True, "left")
    if xi is not None and up >= xi:
        sx = sx_of(xi, i0, i1, box); sy = by + bh - (M50[xi] - lo) / (hi - lo) * bh
        xmark_big(ctx, sx, sy, 0.55 * back(prog(t, T["long"], 0.35)) + 0.01)
    for lab, d in labels:
        text(ctx, lab, sx_of(di(d), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")


def prop_x(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 50, y - 90)
    if fl:
        ctx.scale(-1, 1)
    ctx.rotate(math.sin(t * 4) * 0.1)
    card(ctx, -70, -45, 140, 90, C["white"], 1, 12, border=C["ink"])
    xmark_big(ctx, 0, 0, 0.42)
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #42", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["higher"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2006, 2007, 2008), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = S0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    for si, bi in zip(SELL_I, BUY_I):
        if s0_ <= si <= up:
            x1 = sx_of(si, s0_, xe, RBOX); x2 = sx_of(min(bi, up), s0_, xe, RBOX)
            rect(ctx, x1, by + bh - 18, max(2, x2 - x1), 18, LCOL, 0.35 * a)
            xmark_big(ctx, x1, by + bh - 30, 0.13)
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 3)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 3)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "fire", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("IGNORES IT", HCOL), ("SELLS AT THE CROSS", LCOL))):
        rect(ctx, bx + bw - 330, by + 20 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + 30 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-12-31"); XE2 = di("2012-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x3A, 0x08, 0x10), (0x06, 0x02, 0x04))
    god_rays(ctx, W / 2, 480, t, 0.08, SKC, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, u * 1500, 4, 40, (0xFF, 0x80, 0x80), 0.12)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 440); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "DEATH CROSS:", 0, 0, 170, SKC, 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 680); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "SELL", 0, 0, 200, C["white"], 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "1 YEAR?", 0, 0, 250, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 1040, "SPY · EVERY DEATH CROSS · 2005-2024", C["cream"], back(prog(tl, 1.0, 0.3)), 30, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_x)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_x)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE APRIL FOOLS' DAY", hidden="APR 1, 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["rules"], di("2006-03-31")), (SC["y2006"], di("2006-07-25")),
                               (SC["y2008"], di("2007-12-28"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.45, T["B"] - 0.8, "SELL", "IGNORE", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Watch"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    if t < T["B"] - 0.2:
        xmark_big(ctx, 540, 860, 1.2 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2006, 2007, 2008, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], SKC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


QR0, QR1 = di("2007-07-02"), di("2008-03-31")


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 440, "THE DEATH CROSS", SKC, back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["white"])
    cross_chart(ctx, (130, 540, 820, 300), QR0, QR1, ease(prog(t, T["short"] - 0.2, 1.6)), t, di("2007-12-28"),
                labels=(("SEP 2007", "2007-09-04"), ("JAN 2008", "2008-01-02")))
    for k, (title, col, x, tt) in enumerate((("SELL NEXT OPEN", LCOL, 290, T["He"]), ("WAIT 1 YEAR", HCOL, 790, T["sits"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1050); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -230, -60, 460, 120, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 22, fit(ctx, title, 60, 420), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_y2006(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    pts = [(s0 + 0.1, di("2006-07-25")), (T["climbs"] + 0.8, di("2007-07-27"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2006, 2007, 2008, 2009))
    tag(ctx, 540, 440, "2006: THE FIRST CROSS", SKC, back(prog(t, T["first"] - 0.1, 0.3)), 46, -0.03, C["white"])
    if t > T["climbs"] - 0.15:
        tag(ctx, 540, 530, "THE MARKET CLIMBS WITHOUT HIM", HCOL, back(prog(t, T["climbs"] - 0.15, 0.3)), 38, 0.02, C["ink"])
    bunting(ctx, "ROUND 1", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "sad" if (e != "talk" and t > T["climbs"]) else e, prop=prop_flag)


QD0, QD1 = di("2007-10-01"), di("2009-01-30")


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    if t < T["Now"] - 0.15:
        tag(ctx, 540, 440, "DEC 2007: ANOTHER CROSS", SKC, back(prog(t, s0 + 0.05, 0.3)), 44, -0.03, C["white"])
        k = ease(prog(t, s0 + 0.1, T["forty"] - s0 - 0.1))
        zoom_chart(ctx, (130, 560, 820, 330), QD0, QD1, k, t,
                   [(I_S07, "SELL", LCOL, T["He2"]), (I_B08, "BUY", GRNC, T["forty"] - 0.2)],
                   labels=(("2008", "2008-01-02"), ("2009", "2009-01-02")))
        if t > T["forty"] - 0.1:
            pk = back(prog(t, T["forty"] - 0.1, 0.35))
            ctx.save(); ctx.translate(760, 1010); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            text(ctx, "~40% CHEAPER", 0, 0, 80, GRNC, 1, HEAD, True, "center", outline=10, ocol=C["ink"])
            ctx.restore()
    else:
        race_chart(ctx, t, race_idx(t, [(T["Now"], di("2008-12-30")), (T["ahead"] + 0.4, di("2009-12-31"))]), XE1, years=(2006, 2007, 2008, 2009))
        tag(ctx, 540, 440, "HE'S WAY AHEAD!", LCOL, back(prog(t, T["Now"] - 0.1, 0.3)), 56, -0.03, C["ink"])
    bunting(ctx, "ROUND 2", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown" if t > T["Now"] else "fire", lambda e: "smug" if e != "talk" else e)


def s_y2011(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x05, 0x0C))
    stars(ctx, t, 30, 180, 1200, 9, 0.4)
    pts = [(T["Twenty"], di("2009-12-31")), (T["gone"] + 0.3, di("2012-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2012-12-31"), years=(2006, 2008, 2010, 2012))
    if t < T["Twenty"] - 0.1:
        pk = back(prog(t, T["works"] - 0.2, 0.35))
        ctx.save(); ctx.translate(540, 470); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -330, -60, 660, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "THE CROSS WORKS?", 0, 26, 66, GOLD, 1, HEAD, True, "center")
        ctx.restore()
    else:
        tag(ctx, 540, 440, "2010 + 2011: TWO MORE CROSSES", SKC, back(prog(t, T["Twenty"] - 0.1, 0.3)), 38, -0.03, C["white"])
        if t > T["rips"] - 0.15:
            tag(ctx, 540, 530, "THE MARKET RIPS HIGHER", HCOL, back(prog(t, T["rips"] - 0.15, 0.3)), 44, 0.02, C["ink"])
    if t > T["lead"] - 0.1:
        stamp_box(ctx, ["LEAD: GONE"], 540, 1100, T["lead"] - 0.05, t, STAMP_OR, 480, 64, -0.06)
    bunting(ctx, "ROUND 3", t, s0, [HCOL, C["ink"], C["grey"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if (e != "talk" and t > T["rips"]) else e)


QF0, QF1 = di("2020-02-03"), di("2020-04-09")


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    r = back(prog(t, s0 + 0.03, 0.35))
    big_title(ctx, "APRIL FOOLS' DAY.", W / 2, 460, 120, GOLD, r, 980, 0, 14)
    if t > T["April2"] - 0.15:
        pk = back(prog(t, T["April2"] - 0.15, 0.35))
        cal_page(ctx, 210, 640, 0.55 * pk + 1e-3, "APR 2020" if t > T["twenty2"] - 0.1 else "APR 20??", "1", 1, -0.06)
    if t > T["cross2"] - 0.2:
        k = ease(prog(t, T["cross2"] - 0.2, 1.4))
        cross_chart(ctx, (330, 560, 640, 320), QF0, QF1, k, t, di("2020-03-31"), labels=(("FEB", "2020-02-10"), ("MAR 31", "2020-03-31")))
        if t > T["bottom"] - 0.1:
            bx, by, bw, bh = (330, 560, 640, 320)
            seg = np.r_[CL[QF0:QF1 + 1], M50[QF0:QF1 + 1], M200[QF0:QF1 + 1]]
            lo, hi = float(np.nanmin(seg)) * 0.97, float(np.nanmax(seg)) * 1.03
            sx = sx_of(I_BOT20, QF0, QF1, (330, 560, 640, 320)); sy = by + bh - (CL[I_BOT20] - lo) / (hi - lo) * bh
            ctx.new_path(); ctx.arc(sx, sy, 16 + 4 * math.sin(t * 8), 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GRNC)); ctx.fill()
            tag(ctx, sx - 40, sy + 70, "THE BOTTOM: MAR 23", GRNC, back(prog(t, T["bottom"], 0.3)), 28, 0.03, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], SKC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if (e != "talk" and t > T["bottom"]) else e)


QG0, QG1 = di("2020-03-02"), di("2021-04-30")


def s_rebuy(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    tag(ctx, 540, 440, "SPY · MARCH 2020 - APRIL 2021", C["white"], back(prog(t, s0 + 0.05, 0.3)), 36, -0.03, C["ink"])
    k = ease(prog(t, s0 + 0.1, T["buys2"] - s0))
    zoom_chart(ctx, (130, 560, 820, 330), QG0, QG1, k, t,
               [(I_S20, "SELL", LCOL, s0 + 0.2), (I_B21, "BUY", REDC, T["buys2"] - 0.1)],
               labels=(("APR 2020", "2020-04-01"), ("APR 2021", "2021-04-01")))
    if t > T["sixty"] - 0.1:
        pk = back(prog(t, T["sixty"] - 0.1, 0.35))
        ctx.save(); ctx.translate(560, 1020); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        text(ctx, "OVER +60%", 0, 0, 120, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
        ctx.restore()
        tag(ctx, 560, 1100, "TO GET BACK IN", C["white"], pk, 32, 0.03, C["ink"])
    bunting(ctx, "ONE YEAR LATER", t, s0, [C["blue"], C["ink"], REDC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: ("sad" if t > T["sixty"] else "neutral") if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Six"] - 0.1:
        a = back(prog(t, T["Six"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"WAIT 1 MONTH: {money(_R['scan']['21'])} · BACK AT THE GOLDEN CROSS: {money(_R['golden'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · OCT 2005 TO 2024 · 8 SELLS", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "SOLD AT EVERY CROSS", money(RULE_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "IGNORED IT", money(HOLD_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "FINAL TALLY", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["6 OF 8 SELLS:", "BOUGHT BACK HIGHER."], W / 2, 540, T["Six"] - 0.05, t, STAMP_OR, 900, 66, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["bought"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #43", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "rules": s_rules, "y2006": s_y2006, "y2008": s_y2008, "y2011": s_y2011,
            "remember": s_remember, "rebuy": s_rebuy, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #43 overrides (+4.7% day: jump in or wait for the dip?)
LCOL = (0x22, 0xE5, 0x8B)   # A: JUMPS IN (green)
HCOL = (0x4F, 0xC3, 0xF7)   # B: WAITS FOR THE DIP (blue)


def gcandle(ctx, cx, cy, s, col=GRNC, a=1.0, wob=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(wob); ctx.scale(s, s)
    rect(ctx, -6, -150, 12, 300, C["ink"], a)
    card(ctx, -45, -110, 90, 220, col, a, 10, shadow=False, border=C["ink"])
    rect(ctx, -30, -95, 14, 150, C["white"], 0.35 * a)
    ctx.restore()


def prop_candle(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 40, y - 100)
    if fl:
        ctx.scale(-1, 1)
    gcandle(ctx, 0, 0, 0.42, GRNC, 1, math.sin(t * 4) * 0.12)
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #43", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 600, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 615, 38, 340, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$???,???", 785, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 615, 38, 340, 54, LCOL, a, 8, shadow=False)
        text(ctx, money(A_V), 785, 78, fit(ctx, money(A_V), 36, 320, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["inn"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2008, 2009), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = X0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(12000.0, 1.15 * float(max(np.nanmax(CUMA[s0_:hi]), np.nanmax(CUMB[s0_:hi]))))
    vmin = min(-6000.0, 1.15 * float(min(np.nanmin(CUMA[s0_:hi]), np.nanmin(CUMB[s0_:hi]))))
    yb = by + bh - (0 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$0 PROFIT", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    for i in RI:
        if s0_ <= i <= up:
            xx = sx_of(i, s0_, xe, RBOX)
            card(ctx, xx - 5, by + bh - 34, 10, 26, GRNC, 0.9 * a, 2, shadow=False)
    xs1, ys1 = series_xy(CUMB, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(CUMA, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "detective", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "party", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("B: WAITS FOR THE DIP", HCOL), ("A: JUMPS IN", LCOL))):
        rect(ctx, bx + bw - 330, by + bh - 80 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + bh - 70 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-06-30"); XE2 = di("2021-01-01")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x06, 0x30, 0x1C), (0x01, 0x08, 0x04))
    god_rays(ctx, W / 2, 480, t, 0.09, GRNC, 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, 1500 - u * 1500, 4, 40, (0x80, 0xFF, 0xB0), 0.12)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(510 + shake, 500); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "+4.7%", 0, 0, 270, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    arrow_up(ctx, 960, 235 + math.sin(t * 6) * 10, 0.42 * s_, GRNC)
    ctx.save(); ctx.translate(540, 650); ctx.rotate(0.02); ctx.scale(s_, s_)
    text(ctx, "IN ONE DAY", 0, 0, 110, C["white"], 1, HEAD, True, "center", outline=14, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.03); ctx.scale(s_, s_)
    text(ctx, "BUY NOW?", 0, 0, 240, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 1040, "S&P 500 · MONDAY, NOV 23, 2026", C["cream"], back(prog(tl, 1.0, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_candle)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_candle)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE MARCH MORNING", hidden="MAR ??, 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], X0 + 2), (SC["news"], di("2008-02-15"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.45, T["B"] - 0.5, "JUMP IN", "WAIT", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Watch"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    if t < T["B"] - 0.2:
        gcandle(ctx, 540, 860, 1.1 * back(prog(t, s0 + 0.05, 0.3)) + 1e-3, GRNC, 1, math.sin(t * 5) * 0.08)
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2008, 2009)); ctx.restore()
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


def s_news(ctx, t, s0, s1):
    bg_fill(ctx, (0x08, 0x26, 0x18), (0x02, 0x06, 0x04))
    for k in range(3):
        rect(ctx, 0, 300 + k * 6, W, 3, GRNC, 0.25)
    ticker = "S&P 500 +4.73% TO 7,237.17  ·  DOW +1,448 (+3.0%)  ·  NASDAQ +6.5%  ·  7-DAY LOSING STREAK OVER  ·  "
    xo = -((t - s0) * 260) % 2100
    rect(ctx, 0, 1760, W, 64, (0x05, 0x05, 0x05), 0.9)
    for j in range(3):
        text(ctx, ticker, xo + j * 2100, 1805, 34, GOLD, 1, MONO, True, "left")
    tag(ctx, 540, 450, "MONDAY · NOV 23, 2026", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    p = back(prog(t, s0 + 0.1, 0.35))
    big_title(ctx, "S&P 500: +4.7%", W / 2, 620, 150, GRNC, p, 980, -0.03, 16)
    text(ctx, "CLOSE 7,237.17", W / 2, 720, 44, C["white"], p, MONO, True, "center", outline=6, ocol=C["ink"])
    for j in range(5):
        hh = 80 + j * 35
        gcandle(ctx, 300 + j * 120, 930 - hh * 0.3, 0.4 + 0.12 * j * back(prog(t, s0 + 0.2 + j * 0.12, 0.3)) + 1e-3, GRNC if j == 4 else REDC, 1, 0)
    if t > T["best"] - 0.15:
        tag(ctx, 540, 1110, "BEST DAY SINCE APRIL 2025", GOLD, back(prog(t, T["best"] - 0.15, 0.3)), 50, 0.02, C["ink"])
    bunting(ctx, "THE NEWS", t, s0, [GRNC, C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


def s_count(ctx, t, s0, s1):
    grid_bg(ctx, (0x0E, 0x2A, 0x1E), (0x05, 0x10, 0x0A))
    tag(ctx, 540, 440, "SPY: UP 4% OR MORE IN ONE DAY", GRNC, back(prog(t, s0 + 0.05, 0.3)), 42, -0.03, C["ink"])
    # 27 candles, one per monster day, grouped by year
    yrs = [x["day"][:4] for x in ROWS]
    for k in range(27):
        tt = s0 + 0.15 + k * (T["twentyseven"] - s0 - 0.1) / 27
        pk = back(prog(t, tt, 0.25))
        if pk <= 0:
            continue
        cx = 150 + (k % 9) * 97; cy = 610 + (k // 9) * 175
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        gcandle(ctx, 0, 0, 0.36, GRNC)
        text(ctx, yrs[k], 0, 82, 22, C["white"], 0.85, MONO, True, "center")
        ctx.restore()
    if t > T["twentyseven"] - 0.1 and t < T["twins"] - 0.15:
        pk = back(prog(t, T["twentyseven"] - 0.1, 0.35))
        big_title(ctx, "27 TIMES", W / 2, 1110, 120, GOLD, pk, 700, -0.04, 14)
    if t > T["twins"] - 0.15:
        pk = back(prog(t, T["twins"] - 0.15, 0.35))
        for k, (lab, col, x) in enumerate((("A", LCOL, 330), ("B", HCOL, 750))):
            ctx.save(); ctx.translate(x, 1080); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            card(ctx, -170, -60, 340, 120, col, 1, 22, border=C["ink"])
            text(ctx, lab, -105, 40, 110, C["ink"], 1, HEAD, True, "center")
            text(ctx, "$10,000", 45, 20, fit(ctx, "$10,000", 52, 190, MONO), C["ink"], 1, MONO, True, "center")
            ctx.restore()
    bunting(ctx, "THE CASE FILE", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "shock" if (e != "talk" and t > T["twentyseven"]) else e)


def rule_diagram(ctx, t, t0, cx=540, cy=760):
    """schematic: a jump, the dashed START line, the price falls back below it -> B's buy dot"""
    k = ease(prog(t, t0, 1.6))
    pts = [(-380, 60), (-300, 70), (-220, 50), (-200, -150), (-100, -130), (0, -60), (80, 40), (160, 110), (260, 80), (380, -40)]
    card(ctx, cx - 440, cy - 230, 880, 400, (0x0C, 0x10, 0x1C), 0.9, 16, border=C["grey"])
    for j in range(24):
        rect(ctx, cx - 400 + j * 34, cy + 55, 20, 4, GOLD, 0.8)
    text(ctx, "THE START", cx - 400, cy + 95, 26, GOLD, 1, MONO, True, "left")
    n = max(2, int(len(pts) * k) + 1)
    ctx.new_path(); ctx.move_to(cx + pts[0][0], cy + pts[0][1])
    for x_, y_ in pts[1:n]:
        ctx.line_to(cx + x_, cy + y_)
    ctx.set_source_rgba(*rgba(C["white"])); ctx.set_line_width(8); ctx.stroke()
    if n >= 4:
        text(ctx, "+4%", cx - 260, cy - 170, 44, GRNC, 1, HEAD, True, "center", outline=6, ocol=C["ink"])
        ctx.new_path(); ctx.arc(cx - 100, cy - 130, 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(LCOL)); ctx.fill()
        text(ctx, "A BUYS", cx - 100, cy - 160, 28, LCOL, 1, MONO, True, "center", outline=5, ocol=C["ink"])
    if n >= 8:
        ctx.new_path(); ctx.arc(cx + 120, cy + 75, 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(HCOL)); ctx.fill()
        text(ctx, "B BUYS", cx + 190, cy + 140, 28, HCOL, 1, MONO, True, "center", outline=5, ocol=C["ink"])


def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    tag(ctx, 540, 440, "THE RULES", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 46, -0.03, C["ink"])
    rule_diagram(ctx, t, s0 + 0.1)
    for k, (title, col, x, tt) in enumerate((("A: NEXT MORNING", LCOL, 290, T["A2"]), ("B: BELOW THE START", HCOL, 790, T["drop"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1060); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 56, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["year"] - 0.15:
        tag(ctx, 540, 1140, "SCORED 1 YEAR LATER", GOLD, back(prog(t, T["year"] - 0.15, 0.3)), 34, 0.02, C["ink"])
    bunting(ctx, "THE RULES", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


def s_y2008(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2008-02-15")), (T["every"] + 0.4, di("2008-12-31")), (T["ahead"], di("2009-02-27"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2008, 2009))
    tag(ctx, 540, 440, "2008: THE DIP CAME BACK EVERY TIME", HCOL, back(prog(t, s0 + 0.05, 0.3)), 38, -0.03, C["ink"])
    if t > T["pulls"] - 0.15:
        tag(ctx, 540, 530, "B PULLS WAY AHEAD", HCOL, back(prog(t, T["pulls"] - 0.15, 0.3)), 50, 0.02, C["ink"])
    bunting(ctx, "ROUND 1-11", t, s0, [C["red"], C["ink"], HCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


def s_rounds(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x03, 0x05, 0x0C))
    stars(ctx, t, 30, 180, 1200, 9, 0.4)
    nb = 0
    for k in range(27):
        tt = s0 + 0.2 + k * (T["rounds"] - s0 - 0.1) / 27
        on = t >= tt
        cx = 150 + (k % 9) * 97; cy = 520 + (k // 9) * 120
        col = (HCOL if WINB[k] else LCOL) if on else (0x30, 0x36, 0x40)
        if on and WINB[k]:
            nb += 1
        pk = 1 + 0.25 * (1 - ease(prog(t, tt, 0.25))) if on else 1
        ctx.save(); ctx.translate(cx, cy); ctx.scale(pk, pk)
        card(ctx, -42, -42, 84, 84, col, 1, 12, shadow=False, border=C["ink"])
        text(ctx, "B" if (on and WINB[k]) else ("A" if on else "?"), 0, 18, 50, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
        if k % 9 == 0:
            text(ctx, ROWS[k]["day"][:4], 60, cy + 10, 22, C["white"], 0.7, MONO, True, "center")
    pk = back(prog(t, s0 + 0.1, 0.3))
    ctx.save(); ctx.translate(540, 440); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
    card(ctx, -330, -50, 660, 100, (0x05, 0x05, 0x05), 0.92, 18, shadow=False, border=HCOL)
    text(ctx, f"B WINS {nb} OF 27 ROUNDS", 0, 20, fit(ctx, "B WINS 19 OF 27 ROUNDS", 60, 620), HCOL, 1, HEAD, True, "center")
    ctx.restore()
    if t > T["So"] - 0.15:
        q = back(prog(t, T["So"] - 0.15, 0.35))
        ctx.save(); ctx.translate(540, 950); ctx.rotate(-0.04); ctx.scale(max(q, 1e-3), max(q, 1e-3))
        card(ctx, -340, -60, 680, 120, GOLD, 1, 22, border=C["ink"])
        text(ctx, "SO PATIENCE PAYS?", 0, 26, 70, C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "ALL 27 ROUNDS", t, s0, [HCOL, C["ink"], C["grey"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


QM0, QM1 = di("2009-02-02"), di("2010-03-12")


def start_line(ctx, box, i0, i1, lvl, col=GOLD, label="THE START"):
    bx, by, bw, bh = box
    seg = CL[i0:i1 + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
    yy = by + bh - (lvl - lo) / (hi - lo) * bh
    for j in range(int(bw / 34)):
        rect(ctx, bx + j * 34, yy - 2, 20, 4, col, 0.9)
    text(ctx, label, bx + bw - 10, yy + 34, 24, col, 1, MONO, True, "right", outline=4, ocol=C["ink"])
    return lo, hi


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["bottom"] - 0.15:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "THAT MARCH MORNING?", W / 2, 470, 120, GOLD, r, 980, 0, 14)
        if t > T["Two2"] - 0.15:
            pk = back(prog(t, T["Two2"] - 0.15, 0.35))
            cal_page(ctx, 540, 820, 0.9 * pk + 1e-3, "MAR 2009" if t > T["nine"] - 0.1 else "MAR 20??", "10", 1, -0.06 + 0.03 * math.sin(t * 4))
    else:
        box = (130, 560, 820, 330)
        k = ease(prog(t, T["bottom"] - 0.15, 1.4))
        zoom_chart(ctx, box, QM0, QM1, k, t, [(I_M09 + 1, "A BUYS", LCOL, T["bottom"])],
                   labels=(("MAR 2009", "2009-03-10"), ("MAR 2010", "2010-03-01")))
        start_line(ctx, box, QM0, QM1, CL[I_M09P], GOLD, "THE START: MAR 9 CLOSE")
        tag(ctx, 540, 450, "MAR 10, 2009 · +6% · A DAY AFTER THE BOTTOM", C["cream"], back(prog(t, T["bottom"] - 0.1, 0.3)), 32, -0.03, C["ink"])
        if t > T["never"] - 0.1:
            stamp_box(ctx, ["THE DIP NEVER CAME"], 540, 1010, T["never"] - 0.05, t, STAMP_OR, 760, 60, -0.06)
        if t > T["cash"] - 0.15:
            hourglass(ctx, 900, 1110, 0.4, t)
            tag(ctx, 540, 1120, "B: IN CASH ALL YEAR", HCOL, back(prog(t, T["cash"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective" if t < T["bottom"] else "night", lambda e: "shock" if (e != "talk" and t > T["never"]) else e,
          prop=prop_magnifier if t < T["bottom"] else None)


QT0, QT1 = di("2020-03-02"), di("2021-04-09")


def s_y2020(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    tag(ctx, 540, 450, "MARCH 24 + APRIL 6, 2020", C["white"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    box = (130, 560, 820, 330)
    k = ease(prog(t, s0 + 0.1, 1.3))
    zoom_chart(ctx, box, QT0, QT1, k, t, [(I_M24 + 1, "A BUYS", LCOL, s0 + 0.5), (I_A06 + 1, "A BUYS", LCOL, s0 + 0.9)],
               labels=(("MAR 2020", "2020-03-10"), ("APR 2021", "2021-04-01")))
    start_line(ctx, box, QT0, QT1, CL[I_M24 - 1], GOLD, "START: MAR 23")
    if t > T["same"] - 0.15:
        stamp_box(ctx, ["NO DIP. AGAIN."], 540, 1060, T["same"] - 0.1, t, STAMP_OR, 620, 64, -0.05)
    bunting(ctx, "2020", t, s0, [C["blue"], C["ink"], GRNC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Twenty2"] - 0.1:
        a = back(prog(t, T["Twenty2"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"WAIT MAX 1 MONTH, THEN BUY ANYWAY: {money(_R['var']['21'])} · WAITING WINS"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "27 ROUNDS · $10,000 EACH · 1 YEAR", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "A: JUMPED IN", money(A_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "B: WAITED FOR THE DIP", money(B_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "ALL ROUNDS ADDED UP", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["20 DIPS CAME BACK.", "7 DIDN'T: THE BOTTOM WAS IN."], W / 2, 540, T["Twenty2"] - 0.05, t, STAMP_GR, 940, 60, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["bottom2"], 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #44", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "news": s_news, "count": s_count, "rules": s_rules, "y2008": s_y2008,
            "rounds": s_rounds, "remember": s_remember, "y2020": s_y2020, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #45 overrides (Bollinger Bands)
LCOL = (0xC0, 0x7C, 0xFF)   # A: THE BANDS (violet)
HCOL = (0x4F, 0xC3, 0xF7)   # B: BUY & HOLD (blue)


def bb_chart(ctx, box, i0, i1, k, t, marks=True, a=1.0, labels=(), tmark=None):
    bx, by, bw, bh = box
    card(ctx, bx - 20, by - 20, bw + 40, bh + 70, (0x0C, 0x10, 0x1C), 0.92 * a, 16, border=C["grey"])
    seg = np.r_[CL[i0:i1 + 1], BLO[i0:i1 + 1], BUP[i0:i1 + 1]]
    lo, hi = float(np.nanmin(seg)) * 0.98, float(np.nanmax(seg)) * 1.02
    up = int(i0 + 2 + (i1 - i0 - 2) * clamp(k))
    # band fill
    xs_u, ys_u = series_xy(BUP, i0, i1, up, box, lo, hi, 1); xs_l, ys_l = series_xy(BLO, i0, i1, up, box, lo, hi, 1)
    ctx.new_path(); ctx.move_to(xs_u[0], ys_u[0])
    for x_, y_ in zip(xs_u, ys_u):
        ctx.line_to(x_, y_)
    for x_, y_ in zip(xs_l[::-1], ys_l[::-1]):
        ctx.line_to(x_, y_)
    ctx.close_path(); ctx.set_source_rgba(*rgba(LCOL, 0.16 * a)); ctx.fill()
    poly(ctx, xs_u, ys_u, LCOL, 4, 0.9 * a, glow=False); poly(ctx, xs_l, ys_l, LCOL, 4, 0.9 * a, glow=False)
    xs, ys = series_xy(BMID, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, GOLD, 3, 0.8 * a, glow=False)
    xs, ys = series_xy(CL, i0, i1, up, box, lo, hi, 1); poly(ctx, xs, ys, C["white"], 6, a, glow=True)
    if marks:
        for bi, si in zip(TB_I, TS_I):
            for mi, lab, col, dy in ((bi, "BUY", GRNC, 60), (si, "SELL", REDC, -60)):
                if i0 <= mi <= up and (tmark is None or t >= tmark):
                    sx = sx_of(mi, i0, i1, box); sy = by + bh - (OP[mi] - lo) / (hi - lo) * bh
                    ctx.new_path(); ctx.arc(sx, sy, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
                    card(ctx, sx - 44, sy + dy - 20, 88, 40, col, 1, 8, border=C["ink"])
                    text(ctx, lab, sx, sy + dy + 10, 24, C["ink"], 1, HEAD, True, "center")
    for lab, d in labels:
        text(ctx, lab, sx_of(di(d), i0, i1, box), by + bh + 40, 24, C["white"], 0.7, MONO, True, "center")
    return lo, hi


def prop_band(ctx, x, y, px, t):
    fl = motion(t)[3]
    ctx.save(); ctx.translate(x + 60, y - 120)
    if fl:
        ctx.scale(-1, 1)
    ctx.rotate(math.sin(t * 4) * 0.1)
    card(ctx, -70, -50, 140, 100, (0x0C, 0x10, 0x1C), 1, 12, border=C["white"])
    for k, col in enumerate((LCOL, GOLD, LCOL)):
        ctx.new_path(); ctx.move_to(-55, -25 + k * 25)
        for j in range(12):
            ctx.line_to(-55 + j * 10, -25 + k * 25 + math.sin(j * 0.8 + t * 3) * 8)
        ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #45", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["big"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = 0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    # IN-MARKET barcode
    xs_ = None
    for bi, si in zip(TB_I, TS_I):
        if s0_ <= bi <= up:
            x1 = sx_of(bi, s0_, xe, RBOX); x2 = sx_of(min(si, up), s0_, xe, RBOX)
            rect(ctx, x1, by + bh - 16, max(2, x2 - x1), 16, LCOL, 0.55 * a)
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "lab", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("BOLLINGER BANDS", LCOL))):
        rect(ctx, bx + bw - 300, by + 20 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 265, by + 30 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-06-30"); XE2 = di("2014-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x20, 0x0C, 0x3A), (0x05, 0x02, 0x0C))
    god_rays(ctx, W / 2, 480, t, 0.08, LCOL, 14, 1400)
    for k in range(3):
        ctx.new_path()
        for j in range(60):
            x_ = j * 19; y_ = 1180 + (k - 1) * 90 + math.sin(j * 0.25 + t * 2) * 50
            (ctx.move_to if j == 0 else ctx.line_to)(x_, y_)
        ctx.set_source_rgba(*rgba(LCOL if k != 1 else GOLD, 0.35)); ctx.set_line_width(6); ctx.stroke()
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 500); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "65 WINS", 0, 0, 250, GRNC, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "20 LOSSES", 0, 0, 200, REDC, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 1.0:
        tag(ctx, 540, 920, "BOLLINGER BANDS · SPY · 20 YEARS", C["cream"], back(prog(tl, 1.0, 0.3)), 32, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "lab", lambda e: "shock" if e != "talk" else e, prop=prop_band)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "lab", lambda e: "shock", prop=prop_band)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE SEPTEMBER TRADE", hidden="SEP ??, 20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -320, -70, 640, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -290, -22, fit(ctx, "EVIDENCE: " + label, 30, 580, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -290, 0, 580, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -290 + ((t * 0.9) % 1) * 580
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["bands"], di("2005-06-30"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.5, T["B"] - 0.6, "BANDS", "HOLD", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Watch"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    elif t > s0:
        bb_chart(ctx, (180, 620, 720, 260), di("2018-01-02"), di("2018-04-30"), 1.0, t, marks=False)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


QB0, QB1 = di("2018-01-02"), di("2018-04-30")


def s_bands(ctx, t, s0, s1):
    grid_bg(ctx, (0x1E, 0x12, 0x36), (0x0B, 0x07, 0x16))
    tag(ctx, 540, 440, "BOLLINGER BANDS (20 DAYS, 2 STDEV)", LCOL, back(prog(t, s0 + 0.05, 0.3)), 36, -0.03, C["ink"])
    k = ease(prog(t, s0 + 0.1, 1.6))
    bb_chart(ctx, (130, 540, 820, 330), QB0, QB1, k, t, marks=t > T["Buy"] - 0.2, labels=(("JAN 2018", "2018-01-10"), ("APR 2018", "2018-04-20")))
    for kk, (title, col, x, tt) in enumerate((("BELOW LOWER BAND: BUY", GRNC, 290, T["Buy"]), ("BACK TO MIDDLE: SELL", REDC, 790, T["Sell"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1060); ctx.rotate(-0.03 if kk == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 50, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


def s_wins(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x22, 0x14), (0x03, 0x08, 0x04))
    sun(ctx, 900, 250, 60, t, 0.6)
    pts = [(s0 + 0.1, di("2005-06-30")), (T["Then"], di("2007-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "$10,000 · SPY · FROM 2005", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    if t > T["Small"] - 0.15:
        tag(ctx, 540, 530, "SMALL BOUNCES, SMALL WINS", GRNC, back(prog(t, T["Small"] - 0.15, 0.3)), 42, 0.02, C["ink"])
        nw = 0
        for kk, (bi, w) in enumerate(zip(TB_I, TWIN)):
            if TRD[kk][0] > "2007-12-31":
                break
            tt = T["Small"] + kk * 0.12
            if t >= tt:
                card(ctx, 120 + (kk % 12) * 72, 1060 + (kk // 12) * 66, 58, 54, GRNC if w else REDC, 1, 10, shadow=False, border=C["ink"])
    bunting(ctx, "2005-2007", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2008-01-02")), (T["ahead"], di("2009-03-09"))]
    race_chart(ctx, t, race_idx(t, pts), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 440, "2008: THE CRASH", REDC, back(prog(t, s0 + 0.05, 0.3)), 50, -0.03, C["white"])
    if t > T["half"] - 0.15:
        tag(ctx, 540, 530, "HALF THE TIME IN CASH", GOLD, back(prog(t, T["half"] - 0.15, 0.3)), 40, 0.02, C["ink"])
    if t > T["ahead"] - 0.15:
        stamp_box(ctx, ["WAY AHEAD!"], 540, 1090, T["ahead"] - 0.1, t, STAMP_GR, 520, 70, -0.05)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown" if t > T["ahead"] else "fire", lambda e: "smug" if e != "talk" else e)


QS0, QS1 = di("2008-08-01"), di("2008-11-14")


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["That"] - 0.1:
        pk = back(prog(t, s0 + 0.05, 0.35))
        ctx.save(); ctx.translate(540, 560); ctx.rotate(-0.04); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -360, -60, 720, 120, (0x05, 0x05, 0x05), 0.92, 22, shadow=False, border=GOLD)
        text(ctx, "SO THE BANDS WORK?", 0, 26, 70, GOLD, 1, HEAD, True, "center")
        ctx.restore()
    elif t < T["bought"] - 0.15:
        r = back(prog(t, T["That"] - 0.1, 0.35))
        big_title(ctx, "THAT SEPTEMBER TRADE?", W / 2, 500, 110, GOLD, r, 980, 0, 14)
    else:
        box = (130, 560, 820, 330)
        k = ease(prog(t, T["bought"] - 0.15, T["Sold"] - T["bought"] + 0.5))
        lo, hi = bb_chart(ctx, box, QS0, QS1, k, t, marks=True, labels=(("AUG 2008", "2008-08-11"), ("NOV 2008", "2008-11-07")))
        tag(ctx, 540, 450, "BOUGHT: SEP 5, 2008", GRNC, back(prog(t, T["bought"] - 0.1, 0.3)), 40, -0.03, C["ink"])
        if t > T["Lehman"] - 0.1:
            sx = sx_of(I_LEH, QS0, QS1, box)
            for j in range(10):
                rect(ctx, sx - 2, box[1] + j * 34, 4, 20, REDC, 0.9)
            tag(ctx, sx + 120, box[1] + 30, "LEHMAN: SEP 15", REDC, back(prog(t, T["Lehman"] - 0.1, 0.3)), 26, 0.03, C["white"])
        if t > T["twentytwo"] - 0.15:
            pk = back(prog(t, T["twentytwo"] - 0.15, 0.35))
            ctx.save(); ctx.translate(560, 1040); ctx.rotate(-0.05); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            text(ctx, f"{SEP_R * 100:.1f}%", 0, 0, 130, REDC, 1, HEAD, True, "center", outline=14, ocol=C["ink"])
            ctx.restore()
            tag(ctx, 560, 1120, "SOLD OCT 31", C["white"], pk, 30, 0.03, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective" if t < T["bought"] else "fire", lambda e: "shock" if (e != "talk" and t > T["twentytwo"]) else e,
          prop=prop_magnifier if t < T["bought"] else None)


def s_erased(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x10), (0x06, 0x02, 0x04))
    big_title(ctx, "ONE LOSS =", W / 2, 470, 120, C["white"], back(prog(t, s0 + 0.05, 0.35)), 900, -0.03, 14)
    for kk in range(9):
        tt = T["eight"] - 0.3 + kk * 0.08
        pk = back(prog(t, tt, 0.3))
        if pk <= 0:
            continue
        cx = 180 + (kk % 5) * 180; cy = 660 + (kk // 5) * 200
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -70, -70, 140, 140, GRNC if kk < 8 else (0x30, 0x36, 0x40), 1, 20, border=C["ink"])
        text(ctx, "WIN" if kk < 8 else "+", 0, 18, 50, C["ink"], 1, HEAD, True, "center")
        if kk < 8 and t > T["eight"] + 0.6:
            xmark(ctx, 0, 0, 50, C["red"], 12)
        ctx.restore()
    if t > T["eight"] + 0.3:
        tag(ctx, 540, 1110, "MORE THAN 8 AVERAGE WINS", REDC, back(prog(t, T["eight"] + 0.3, 0.3)), 44, 0.02, C["white"])
    bunting(ctx, "THE DAMAGE", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "sad" if e != "talk" else e)


def s_cash(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x14, 0x2A), (0x02, 0x04, 0x0A))
    stars(ctx, t, 30, 180, 1200, 9, 0.4)
    pts = [(s0 + 0.1, di("2009-06-30")), (T["five"] + 0.3, di("2013-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2013-12-31"), years=(2005, 2008, 2011, 2014))
    tag(ctx, 540, 440, "CASH 4 DAYS OUT OF 5", HCOL, back(prog(t, T["Cash"] - 0.15, 0.3)), 50, -0.03, C["ink"])
    bunting(ctx, "AFTER 2009", t, s0, [C["blue"], C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sad" if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Winning"] - 0.1:
        a = back(prog(t, T["Winning"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 1010); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = "85 TRADES · 76% WINNERS · EXIT AT THE UPPER BAND INSTEAD: $35,467"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · MAR 2005 TO 2024 · 85 TRADES", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "BOLLINGER BANDS", money(BB_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "FINAL COUNT", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["WINNING OFTEN", "ISN'T WINNING BIG."], W / 2, 540, T["Winning"] - 0.05, t, STAMP_OR, 880, 70, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["big"] - 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #46", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "bands": s_bands, "wins": s_wins, "crash": s_crash, "remember": s_remember,
            "erased": s_erased, "cash": s_cash, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #46 overrides (Dow 50,000: sell the milestone?)
LCOL = (0xFF, 0x9E, 0x2C)   # A: MILESTONE SELLER (orange)
HCOL = (0x4F, 0xC3, 0xF7)   # B: BUY & HOLD (blue)
STONE = (0xB8, 0xBE, 0xC8)
NAVY0, NAVY1 = (0x0C, 0x18, 0x3A), (0x02, 0x05, 0x10)


def milestone(ctx, cx, cy, s, label, a=1.0, col=STONE, rot=0.0, glow=False, t=0.0):
    """a roadside milestone stone (rounded top) with a carved number (original drawing)"""
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    if glow:
        for r_, al in ((150, 0.10), (120, 0.14)):
            ctx.new_path(); ctx.arc(0, -40, r_, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD, al * a * (0.8 + 0.2 * math.sin(t * 5)))); ctx.fill()
    ctx.save(); ctx.translate(10, 12)
    ctx.new_path(); ctx.move_to(-90, 90); ctx.line_to(-90, -40); ctx.arc(0, -40, 90, math.pi, 0); ctx.line_to(90, 90); ctx.close_path()
    ctx.set_source_rgba(0, 0, 0, 0.35 * a); ctx.fill(); ctx.restore()
    ctx.new_path(); ctx.move_to(-90, 90); ctx.line_to(-90, -40); ctx.arc(0, -40, 90, math.pi, 0); ctx.line_to(90, 90); ctx.close_path()
    ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(9); ctx.stroke()
    ctx.new_path(); ctx.arc(-30, -70, 22, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.25 * a); ctx.fill()
    rect(ctx, -110, 84, 220, 22, (0x3A, 0x2A, 0x1A), a)
    text(ctx, label, 0, 10, fit(ctx, label, 64, 150, HEAD), C["ink"], a, HEAD, True, "center")
    ctx.restore()


def prop_stone(ctx, x, y, px, t):
    sw = math.sin(t * 4) * 0.08
    milestone(ctx, x + 75, y - 150, 0.62, "50K", 1, GOLD, -0.15 + sw)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #46", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["seventeen"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = 0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    # OUT-OF-MARKET bands (sold at a milestone, waiting 3 months)
    for si, bi in zip(MS_SI, MS_BI):
        if s0_ <= si <= up:
            x1 = sx_of(si, s0_, xe, RBOX); x2 = sx_of(min(bi, up), s0_, xe, RBOX)
            rect(ctx, x1, by, max(3, x2 - x1), bh, LCOL, 0.20 * a)
            rect(ctx, x1, by + bh - 16, max(3, x2 - x1), 16, LCOL, 0.85 * a)
            ctx.save(); ctx.translate(x1, by - 2); ctx.rotate(math.pi / 4)
            rect(ctx, -9, -9, 18, 18, GOLD, a); ctx.restore()
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "race", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("MILESTONE SELLER", LCOL))):
        rect(ctx, bx + bw - 330, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")


XE1 = di("2009-06-30"); XE2 = di("2021-12-31")


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, NAVY0, NAVY1)
    god_rays(ctx, W / 2, 470, t, 0.09, GOLD, 14, 1400)
    for k in range(26):
        u = ((t * 0.25) + k / 26) % 1
        rect(ctx, (k * 151) % W, 1500 - u * 1500, 5, 30, GOLD, 0.12)
    skyline(ctx, 1240, t, 5, (0x10, 0x1C, 0x3C), True)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 330); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "THE DOW", 0, 0, 170, C["white"], 1, HEAD, True, "center", outline=20, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 610); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "50,000", 0, 0, 270, GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    milestone(ctx, 190, 1060, 1.05 * max(p, 1e-3), "50K", 1, STONE, -0.06, True, t)
    if show_tag and tl >= T["SPY"] - 0.15:
        tag(ctx, 540, 800, "SPY HIT 10 ROUND-NUMBER MILESTONES", C["cream"], back(prog(tl, T["SPY"] - 0.15, 0.3)), 34, -0.03)
    if show_tag and tl >= 0.7:
        tag(ctx, 540, 150, "DOW CLOSE NOV 24: 50,018.70", HCOL, back(prog(tl, 0.7, 0.3)), 30, 0.02, C["ink"])


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_stone)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_stone)


def evidence(ctx, cx, cy, t, a=1.0, label="ONE MILESTONE BEFORE 2008", hidden="SPY $1?? · ??? 2007"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -340, -70, 680, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -310, -22, fit(ctx, "EVIDENCE: " + label, 30, 620, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -310, 0, 620, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -310 + ((t * 0.9) % 1) * 620
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["headline"], di("2005-09-30")), (SC["rule"], di("2006-06-30")),
                               (SC["s200"], di("2007-03-30"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["One"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.5, T["Hold"] - 0.1, "SELL IT", "HOLD", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["One"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    else:
        milestone(ctx, 540, 820, 1.3, "50K", 1, GOLD, 0.04 * math.sin(t * 3), True, t)
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["One"] else None)


def newspaper(ctx, cx, cy, s, head1, head2, a=1.0, rot=-0.05):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -400, -230, 800, 460, (0xF4, 0xEE, 0xDF), a, 10, border=C["ink"])
    text(ctx, "THE DAILY TICKER", 0, -170, 50, C["ink"], a, HEAD, True, "center")
    rect(ctx, -370, -150, 740, 6, C["ink"], a); rect(ctx, -370, -138, 740, 2, C["ink"], a)
    text(ctx, head1, 0, -50, fit(ctx, head1, 110, 720), C["ink"], a, HEAD, True, "center")
    text(ctx, head2, 0, 60, fit(ctx, head2, 80, 720), (0x6A, 0x5A, 0x4A), a, HEAD, True, "center")
    for j in range(5):
        rect(ctx, -370, 110 + j * 22, 340 if j % 2 else 300, 8, (0x9A, 0x90, 0x80), a)
        rect(ctx, 30, 110 + j * 22, 340, 8, (0x9A, 0x90, 0x80), a)
    ctx.restore()


def s_headline(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x1C, 0x36), (0x06, 0x08, 0x12))
    for k, lv in enumerate(MS_LV):
        tt = s0 + 0.1 + k * 0.12
        pk = back(prog(t, tt, 0.3))
        if pk > 0:
            milestone(ctx, 130 + (k % 5) * 205, 520 + (k // 5) * 270, 0.78 * pk, f"${lv}", 1, STONE, (-1) ** k * 0.04)
    q = back(prog(t, T["headline"] - 0.15, 0.35))
    if q > 0:
        newspaper(ctx, 540, 720, q * 1.0, "A NEW ROUND NUMBER!", "RECORD HIGHS EVERYWHERE", 1, -0.04)
    if t > T["top"] - 0.15:
        stamp_box(ctx, ["THE TOP IS IN!"], 540, 1050, T["top"] - 0.1, t, C["red"], 760, 86, -0.07)
    bunting(ctx, "THE HEADLINE", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if (e != "talk" and t > T["top"]) else e)


def s_rule(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x12, 0x30), (0x06, 0x03, 0x0C))
    race_chart(ctx, t, race_idx(t, [(s0, di("2007-03-30")), (s1, di("2007-07-31"))]), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 450, "$10,000 · SPY · FROM 2005", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    for kk, (title, col, x, tt) in enumerate((("MILESTONE: SELL", REDC, 290, T["sells"]), ("3 MONTHS: BUY BACK", GRNC, 790, T["buys"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1080); ctx.rotate(-0.03 if kk == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 50, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["sells"] + 0.25:
        text(ctx, "NEXT OPEN", 290, 1165, 24, C["white"], 0.8, MONO, True, "center", outline=5, ocol=C["ink"])
    if t > T["three"]:
        text(ctx, "63 TRADING DAYS", 790, 1165, 24, C["white"], 0.8, MONO, True, "center", outline=5, ocol=C["ink"])
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


Q14A, Q14B = di("2014-06-02"), di("2015-01-30")


def s_s200(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x22, 0x2A), (0x02, 0x06, 0x08))
    sun(ctx, 920, 250, 55, t, 0.5)
    if t > T["two"] - 0.15:
        tag(ctx, 540, 450, "SPY HITS $200 · AUG 2014", GOLD, back(prog(t, T["two"] - 0.15, 0.3)), 44, -0.03, C["ink"])
    box = (130, 560, 820, 330)
    k = ease(prog(t, s0 + 0.1, T["more"] - s0))
    zoom_chart(ctx, box, Q14A, Q14B, k, t, [(I_14S, "SELL", REDC, T["sells2"] - 0.1), (I_14B, "BUY", GRNC, T["Three"] + 0.3)],
               labels=(("JUN 2014", "2014-06-16"), ("JAN 2015", "2015-01-16")))
    if t > T["sells2"]:
        seg = CL[Q14A:Q14B + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
        yl = box[1] + box[3] - (OP[I_14S] - lo) / (hi - lo) * box[3]
        for j in range(20):
            rect(ctx, box[0] + j * 42, yl - 2, 24, 4, REDC, 0.7)
    if t > T["more"] - 0.12:
        stamp_box(ctx, ["PAID MORE"], 540, 1060, T["more"] - 0.1, t, STAMP_OR, 560, 80, -0.06)
    bunting(ctx, "MILESTONE #2", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "sad" if (e != "talk" and t > T["more"]) else e, prop=prop_flag)


LAD = [(250, T["Two"]), (350, T["threefifty"]), (400, T["four"])]


def s_ladder(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0E, 0x16), (0x08, 0x02, 0x05))
    pts = [(s0 + 0.1, di("2015-01-30")), (T["Seven"], di("2021-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE2, curtain=di("2021-12-31"), years=(2005, 2010, 2015, 2020))
    if t < T["Seven"] - 0.15:
        for k, (lv, tt) in enumerate(LAD):
            pk = back(prog(t, tt - 0.12, 0.35))
            if pk > 0:
                milestone(ctx, 250 + k * 290, 470, 0.62 * pk, f"${lv}", 1, STONE, (-1) ** k * 0.05)
                if t > tt + 0.35:
                    tag(ctx, 250 + k * 290, 540, "HIGHER", REDC, back(prog(t, tt + 0.35, 0.3)), 30, 0.04, C["white"])
    else:
        tag(ctx, 540, 450, "BOUGHT BACK HIGHER", REDC, back(prog(t, T["Seven"] - 0.15, 0.3)), 46, -0.03, C["white"])
    if t > T["Seven"] - 0.1:
        done = [k for k in range(len(MTR)) if "buy" in MTR[k]]
        for j, k in enumerate(done):
            tt = T["Seven"] - 0.1 + j * 0.1
            pk = back(prog(t, tt, 0.3))
            if pk <= 0:
                continue
            cx = 120 + j * 105; cy = 1085
            ctx.save(); ctx.translate(cx, cy); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
            card(ctx, -46, -46, 92, 92, REDC if MS_HIGHER[k] else (0x30, 0x36, 0x40), 1, 14, border=C["ink"])
            text(ctx, f"{MS_LV[k]}", 0, 12, 34, C["white"], 1, HEAD, True, "center")
            ctx.restore()
    bunting(ctx, "2015-2021", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


QM0, QM1 = di("2007-03-01"), di("2009-04-30")


def m07_chart(ctx, t, k, marks):
    box = (130, 560, 820, 330)
    zoom_chart(ctx, box, QM0, QM1, k, t, marks, labels=(("2007", "2007-06-15"), ("2008", "2008-06-16"), ("2009", "2009-03-02")))
    return box


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["May"] - 0.15:
        r = back(prog(t, s0 + 0.05, 0.35))
        big_title(ctx, "THAT MILESTONE", W / 2, 520, 120, GOLD, r, 980, -0.03, 14)
        big_title(ctx, "BEFORE 2008?", W / 2, 680, 120, C["white"], back(prog(t, s0 + 0.3, 0.35)), 980, 0.02, 14)
        milestone(ctx, 540, 960, 0.9, "$1??", 1, STONE, 0.04 * math.sin(t * 3), True, t)
    else:
        k = ease(prog(t, T["May"] - 0.15, T["cheaper"] + 0.4 - T["May"])) * (di("2007-09-14") - QM0) / (QM1 - QM0)
        m07_chart(ctx, t, k, [(I_M07S, "SELL", REDC, T["sells3"] - 0.1), (I_M07B, "BUY", GRNC, T["cheaper"] - 0.1)])
        tag(ctx, 540, 450, "SPY HITS $150 · MAY 2007", GOLD, back(prog(t, T["May"] - 0.1, 0.3)), 44, -0.03, C["ink"])
        if t > T["cheaper"] - 0.1:
            tag(ctx, 560, 1070, "BOUGHT BACK CHEAPER · AUG 3", GRNC, back(prog(t, T["cheaper"] - 0.1, 0.3)), 40, 0.03, C["ink"])
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if (e != "talk" and t > T["cheaper"]) else e, prop=prop_magnifier)


def s_genius(ctx, t, s0, s1):
    if t > T["never"] - 0.2:
        rain_bg(ctx, t)
    else:
        bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    f1 = (di("2007-09-14") - QM0) / (QM1 - QM0); f2 = (I_TOP07 + 8 - QM0) / (QM1 - QM0)
    if t < T["top2"]:
        k = lerp(f1, f2, ease(prog(t, T["August"] - 0.2, T["top2"] - T["August"] + 0.2)))
    else:
        k = lerp(f2, 1.0, ease(prog(t, T["never"] - 0.3, 1.0)))
    box = m07_chart(ctx, t, k, [(I_M07S, "SELL", REDC, 0), (I_M07B, "BUY", GRNC, 0)])
    tag(ctx, 540, 450, "SPY HITS $150 · MAY 2007", GOLD, 1, 44, -0.03, C["ink"])
    if t < T["August"]:
        stamp_box(ctx, ["GENIUS?"], 540, 1060, T["Genius"] - 0.05, t, STAMP_GR, 520, 90, -0.06)
    if t > T["top2"] - 0.15:
        seg = CL[QM0:QM1 + 1]; lo, hi = float(seg.min()) * 0.96, float(seg.max()) * 1.04
        sx = sx_of(I_TOP07, QM0, QM1, box); sy = box[1] + box[3] - (CL[I_TOP07] - lo) / (hi - lo) * box[3]
        pk = back(prog(t, T["top2"] - 0.15, 0.3))
        ctx.new_path(); ctx.arc(sx, sy, 22 * pk + 1e-3, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD)); ctx.set_line_width(6); ctx.stroke()
        tag(ctx, sx + 90, sy - 50, "THE TOP · OCT 2007", GOLD, pk, 26, 0.03, C["ink"])
    if t > T["never"] - 0.15:
        tag(ctx, 540, 1070, "HE RODE THE WHOLE CRASH", REDC, back(prog(t, T["never"] - 0.15, 0.3)), 46, 0.03, C["white"])
    bunting(ctx, "2007-2009", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "crown" if t < T["August"] else "none", lambda e: ("smug" if t < T["August"] else "sad") if e != "talk" else e)


def footnote(ctx, t):
    if t >= T["Round"] - 0.1:
        a = back(prog(t, T["Round"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 985); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"BUY BACK AFTER 1 MONTH INSTEAD: {money(VAR['21'])} (WINS) · 6 MONTHS: {money(VAR['126'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024 · 10 MILESTONES", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "MILESTONE SELLER", money(MS_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "THE TOTALS", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["MILESTONES", "AREN'T TOPS."], W / 2, 540, T["Round"] - 0.05, t, STAMP_OR, 820, 80, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["Selling"] - 0.3, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #47", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "headline": s_headline, "rule": s_rule, "s200": s_s200, "ladder": s_ladder,
            "remember": s_remember, "genius": s_genius, "score": s_score, "verdict": s_verdict, "loop": s_loop}


# ================================================================ #47 overrides (after a 20% year, sit out the next?)
LCOL = (0xFF, 0x9E, 0x2C)
HCOL = (0x4F, 0xC3, 0xF7)


def hud(ctx, t):
    a = ease(prog(t, SC["guess"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #47", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["guess"]) / (T["seventeen"] + 0.4 - SC["guess"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007), x0=None):
    bx, by, bw, bh = RBOX
    s0_ = 0 if x0 is None else x0
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(s0_ + 2, min(up, N - 1))
    if curtain is not None:
        up = min(up, curtain)
    for k in range(1, 5):
        rect(ctx, bx, by + k * bh / 5, bw, 2, C["white"], 0.08)
    for yr in years:
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), s0_, xe, RBOX), by + bh + 42, 26, C["white"], 0.75, MONO, True, "center")
    hi = up + 1
    vmax = max(14000.0, 1.12 * float(max(np.nanmax(HV[s0_:hi]), np.nanmax(SV[s0_:hi]))))
    vmin = min(5000.0, 0.85 * float(min(np.nanmin(HV[s0_:hi]), np.nanmin(SV[s0_:hi]))))
    yb = by + bh - (10000 - vmin) / (vmax - vmin) * bh
    for j in range(22):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.25)
    text(ctx, "$10K", bx + 8, yb - 8, 20, C["white"], 0.6, MONO, True, "left")
    # OUT-OF-MARKET bands (sold at a milestone, waiting 3 months)
    for si, bi in zip(MS_SI, MS_BI):
        if s0_ <= si <= up:
            x1 = sx_of(si, s0_, xe, RBOX); x2 = sx_of(min(bi, up), s0_, xe, RBOX)
            rect(ctx, x1, by, max(3, x2 - x1), bh, LCOL, 0.20 * a)
            rect(ctx, x1, by + bh - 16, max(3, x2 - x1), 16, LCOL, 0.85 * a)
            ctx.save(); ctx.translate(x1, by - 2); ctx.rotate(math.pi / 4)
            rect(ctx, -9, -9, 18, 18, GOLD, a); ctx.restore()
    xs1, ys1 = series_xy(HV, s0_, xe, up, RBOX, vmin, vmax, 1)
    xs2, ys2 = series_xy(SV, s0_, xe, up, RBOX, vmin, vmax, 1)
    poly(ctx, xs1, ys1, HCOL, 8, 1, glow=True); poly(ctx, xs2, ys2, LCOL, 7, 1, glow=True)
    off = 0 if abs(ys1[-1] - ys2[-1]) > 60 else 60
    mini_rocco(ctx, xs1[-1], ys1[-1] - 4 - off, 4, "tophat", t, "neutral", False, True)
    mini_rocco(ctx, xs2[-1], ys2[-1] - 4, 4, "race", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, s0_, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("BUY & HOLD", HCOL), ("SITS OUT", LCOL))):
        rect(ctx, bx + bw - 330, by + bh - 70 + k * 30, 26, 10, col)
        text(ctx, lab, bx + bw - 295, by + bh - 60 + k * 30, 22, col, 1, MONO, True, "left")






XE1 = di("2009-06-30"); XE3 = di("2024-12-31")
GRN0, GRN1 = (0x0C, 0x30, 0x1E), (0x02, 0x0A, 0x06)


def prop_cal(ctx, x, y, px, t):
    sw = math.sin(t * 4) * 0.08
    cal_page(ctx, x + 80, y - 160, 0.45, "NEXT YEAR", "20??", 1, -0.12 + sw)


def year_tile(ctx, cx, cy, y, t, show_dir=True, cash=None, q=False, a=1.0, s=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    up = YR[y] > 0
    col = (0x30, 0x36, 0x40) if (not show_dir or q) else (GRNC if up else REDC)
    card(ctx, -80, -52, 160, 104, col, a, 14, border=C["ink"])
    text(ctx, str(y), 0, -8, 40, C["white"] if not show_dir or q else C["ink"], a, HEAD, True, "center")
    if q:
        text(ctx, "?", 0, 40, 40, GOLD, a, HEAD, True, "center")
    elif show_dir:
        (arrow_up if up else arrow_down)(ctx, 0, 30, 0.18, C["white"], a)
    if cash is not None and cash > 0:
        ctx.save(); ctx.rotate(-0.18); ctx.scale(max(cash, 1e-3), max(cash, 1e-3))
        card(ctx, -70, -22, 140, 44, LCOL, a, 8, shadow=False, border=C["ink"])
        text(ctx, "CASH", 0, 14, 34, C["ink"], a, HEAD, True, "center")
        ctx.restore()
    ctx.restore()


def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, GRN0, GRN1)
    god_rays(ctx, W / 2, 470, t, 0.09, GRNC, 14, 1400)
    for k in range(12):
        u = ((t * 0.35) + k / 12) % 1
        arrow_up(ctx, (k * 211) % W + 40, 1700 - u * 1700, 0.22, GRNC, 0.18)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 470); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "+20%", 0, 0, 330, GRNC, 1, HEAD, True, "center", outline=26, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 720); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "SIT OUT NEXT?", 0, 0, 150, C["white"], 1, HEAD, True, "center", outline=18, ocol=C["ink"])
    ctx.restore()
    if show_tag and tl >= 0.8:
        tag(ctx, 540, 860, "ONE BIG YEAR IN THE S&P (SPY)", C["cream"], back(prog(tl, 0.8, 0.3)), 34, -0.03)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e, prop=prop_cal)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05, False)
    rocco(ctx, t, "party", lambda e: "shock", prop=prop_cal)


def evidence(ctx, cx, cy, t, a=1.0, label="THE VERY LAST YEAR", hidden="20??: ??%"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -340, -70, 680, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -310, -22, fit(ctx, "EVIDENCE: " + label, 30, 620, TAGF), C["ink"], a, TAGF, False, "left")
    rect(ctx, -310, 0, 620, 52, (0x05, 0x05, 0x05), a)
    text(ctx, hidden, 0, 42, 34, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -310 + ((t * 0.9) % 1) * 620
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], 2), (SC["belief"], di("2005-09-30")), (SC["rule"], di("2006-09-29")),
                               (SC["y2010"], di("2009-03-31"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x26, 0x30), (0x03, 0x08, 0x0C))
    stars(ctx, t, 30, 180, 1150, 5, 0.4)
    sh = ease(prog(t, T["Watch"] - 0.15, 0.35))
    ctx.save(); ctx.translate(W / 2, 420 - 40 * sh); ctx.scale(1 - 0.38 * sh, 1 - 0.38 * sh); ctx.translate(-W / 2, -420)
    ab_cards3(ctx, t, T["A"] - 0.5, T["stay"] - 0.1, "CASH OUT", "STAY IN", 420, T["B"] + 0.3)
    ctx.restore()
    q = back(prog(t, T["Watch"] - 0.2, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 520); ctx.scale(max(q * 0.78, 1e-3), max(q * 0.78, 1e-3))
        evidence(ctx, 0, 0, t, 1); ctx.restore()
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc, years=(2005, 2007, 2009)); ctx.restore()
    else:
        cal_page(ctx, 540, 840, 1.0, "NEXT YEAR", "20??", 1, -0.05 + 0.03 * math.sin(t * 4))
    sticker(ctx, t, T["B"] + 0.1, T["B"] + 2.2, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["B"]) else e, prop=prop_magnifier if t > T["Watch"] else None)


def s_belief(ctx, t, s0, s1):
    grid_bg(ctx, (0x20, 0x16, 0x30), (0x07, 0x05, 0x10))
    r = back(prog(t, T["what"] - 0.15, 0.35))
    if r > 0:
        big_title(ctx, "WHAT GOES UP", W / 2, 520, 130, GOLD, r, 980, -0.03, 14)
    if t > T["must"] - 0.15:
        big_title(ctx, "MUST COME DOWN?", W / 2, 690, 120, REDC, back(prog(t, T["must"] - 0.15, 0.35)), 980, 0.02, 14)
    # a ball thrown up, then falling
    if t > T["what"]:
        u = t - T["what"]
        yb = 1080 - 260 * math.sin(min(math.pi, u / (T["down"] + 0.4 - T["what"]) * math.pi))
        ctx.new_path(); ctx.arc(820, yb, 46, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GRNC)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(8); ctx.stroke()
        text(ctx, "$", 820, yb + 18, 52, C["ink"], 1, HEAD, True, "center")
    if t < T["what"] - 0.15:
        tag(ctx, 540, 600, "EVERYONE SAYS IT", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 60, -0.03, C["ink"])
    bunting(ctx, "THE BELIEF", t, s0, [GOLD, C["ink"], REDC, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "smug" if e != "talk" else e)


def s_rule(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x12, 0x30), (0x06, 0x03, 0x0C))
    race_chart(ctx, t, race_idx(t, [(s0, di("2006-09-29")), (s1, di("2009-03-31"))]), XE1, years=(2005, 2007, 2009))
    tag(ctx, 540, 450, "$10,000 · SPY · FROM 2005", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 40, -0.03, C["ink"])
    for kk, (title, col, x, tt) in enumerate((("YEAR UP 20%+", GRNC, 290, T["twentyp"]), ("NEXT YEAR: CASH", LCOL, 790, T["cash"]))):
        pk = back(prog(t, tt - 0.12, 0.4))
        if pk <= 0:
            continue
        ctx.save(); ctx.translate(x, 1080); ctx.rotate(-0.03 if kk == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -235, -55, 470, 110, col, 1, 22, border=C["ink"])
        text(ctx, title, 0, 20, fit(ctx, title, 52, 430), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    if t > T["cash"] + 0.25:
        text(ctx, "SELL 1ST OPEN · BUY BACK 1ST OPEN AFTER", 540, 1165, 24, C["white"], 0.8, MONO, True, "center", outline=5, ocol=C["ink"])
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_y2010(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x22, 0x2A), (0x02, 0x06, 0x08))
    sun(ctx, 920, 250, 55, t, 0.5)
    p1 = back(prog(t, s0 + 0.05, 0.35))
    cal_page(ctx, 320, 700, 1.0 * p1 + 1e-3, "2009", "UP", 1, -0.07)
    tag(ctx, 320, 900, "BIG YEAR: 20%+", GRNC, p1, 34, -0.03, C["ink"])
    p2 = back(prog(t, T["ten"] - 0.1, 0.35))
    if p2 > 0:
        cal_page(ctx, 760, 700, 1.0 * p2, "2010", "OUT", 1, 0.06)
    if t > T["skips"] - 0.1:
        stamp_box(ctx, ["SKIPPED"], 760, 720, T["skips"] - 0.1, t, STAMP_OR, 380, 60, -0.12)
    if t > T["climbs"] - 0.15:
        pk = ease(prog(t, T["climbs"] - 0.15, 0.6))
        arrow_up(ctx, 760, 980 - 120 * pk, 0.55 * max(pk, 0.01), GRNC)
        tag(ctx, 540, 1090, "THE MARKET CLIMBS ANYWAY", GRNC, back(prog(t, T["climbs"] - 0.1, 0.3)), 40, 0.02, C["ink"])
    bunting(ctx, "2009-2010", t, s0, [GOLD, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "sad" if (e != "talk" and t > T["climbs"]) else e, prop=prop_flag)


GRID_Y = {y: (150 + ((y - 2005) % 5) * 195, 520 + ((y - 2005) // 5) * 135) for y in range(2005, 2025)}


def s_skips(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x0E, 0x16), (0x08, 0x02, 0x05))
    cash_t = {2010: s0, 2014: T["fourteen"], 2018: T["eighteen"], 2020: T["twenty20"], 2022: T["Four"], 2024: T["Four"]}
    for y in range(2005, 2025):
        cx, cy = GRID_Y[y]
        pk = back(prog(t, s0 + 0.05 + (y - 2005) * 0.03, 0.3))
        if pk <= 0:
            continue
        ct = cash_t.get(y)
        cash = back(prog(t, ct - 0.12, 0.3)) if (ct is not None and t > ct - 0.12) else None
        show = y not in cash_t or t > T["Four"] - 0.1
        q = y in (2022, 2024)
        a = 1.0 if (y in cash_t or t < T["Four"] - 0.1) else 0.35
        year_tile(ctx, cx, cy, y, t, show, cash, q, a, 0.95 * pk)
    if t > T["Four"] - 0.1:
        tag(ctx, 540, 1110, "4 OF 6 SKIPPED YEARS STILL WENT UP", GRNC, back(prog(t, T["Four"] - 0.1, 0.3)), 38, -0.02, C["ink"])
    tag(ctx, 540, 445, "SPY CALENDAR YEARS · WITH DIVIDENDS", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 32, -0.03, C["ink"])
    bunting(ctx, "SAME MOVE", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "sad" if e != "talk" else e)


def s_y2022(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2010-06-30")), (T["bear"], di("2022-12-30"))]
    race_chart(ctx, t, race_idx(t, pts), XE3, curtain=di("2022-12-30"), years=(2005, 2010, 2015, 2020))
    tag(ctx, 540, 450, "2022: A BEAR MARKET", REDC, back(prog(t, T["tt22"] - 0.15, 0.3)), 50, -0.03, C["white"])
    if t > T["smart"] - 0.15:
        stamp_box(ctx, ["SKEPTIC: RIGHT!"], 540, 1085, T["smart"] - 0.1, t, STAMP_GR, 640, 70, -0.05)
    bunting(ctx, "2022", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "night" if t < T["Finally"] else "crown", lambda e: "smug" if e != "talk" else e)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x20, 0x08), (0x06, 0x05, 0x02))
    stars(ctx, t, 40, 160, 1200, 7, 0.5)
    if t < T["And"] - 0.12:
        r = back(prog(t, s0 + 0.05, 0.35))
        big_title(ctx, "SO BIG YEARS", W / 2, 540, 130, C["white"], r, 980, -0.03, 14)
        big_title(ctx, "REALLY WARN US?", W / 2, 700, 120, GOLD, back(prog(t, T["warn"] - 0.2, 0.35)), 980, 0.02, 14)
    else:
        r = back(prog(t, T["And"] - 0.12, 0.35))
        big_title(ctx, "THAT VERY", W / 2, 520, 130, C["white"], r, 980, -0.03, 14)
        big_title(ctx, "LAST YEAR?", W / 2, 680, 140, GOLD, back(prog(t, T["last2"] - 0.2, 0.35)), 980, 0.02, 14)
        cal_page(ctx, 540, 960, 0.8 * back(prog(t, T["last2"] - 0.1, 0.35)) + 1e-3, "THE LAST ONE", "20??", 1, -0.05 + 0.03 * math.sin(t * 4))
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], LCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "shock" if (e != "talk" and t > T["last2"]) else e, prop=prop_magnifier)


def s_lastyear(ctx, t, s0, s1):
    bg_fill(ctx, GRN0, GRN1)
    god_rays(ctx, 760, 700, t, 0.07 if t > T["soars"] else 0.0, GRNC, 14, 1200)
    p1 = back(prog(t, s0 + 0.05, 0.35))
    cal_page(ctx, 300, 640, 0.85 * p1 + 1e-3, "2023", "UP", 1, -0.07)
    tag(ctx, 300, 790, "HUGE YEAR: 20%+", GRNC, back(prog(t, T["huge"] - 0.1, 0.3)) if t > T["huge"] - 0.1 else 0, 32, -0.03, C["ink"])
    p2 = back(prog(t, T["tt24"] - 0.2, 0.35))
    if p2 > 0:
        cal_page(ctx, 760, 640, 0.85 * p2, "2024", "OUT", 1, 0.06)
    if t > T["skips2"] - 0.1:
        stamp_box(ctx, ["SKIPPED"], 760, 650, T["skips2"] - 0.1, t, STAMP_OR, 360, 58, -0.12)
    if t > T["soars"] - 0.15:
        k = ease(prog(t, T["soars"] - 0.15, 0.9))
        arrow_up(ctx, 790, 1010 - 90 * k, 0.85 * max(k, 0.01), GRNC)
        if t > T["tf"] - 0.1:
            pp = back(prog(t, T["tf"] - 0.1, 0.35))
            ctx.save(); ctx.translate(360, 1000); ctx.rotate(-0.05); ctx.scale(max(pp, 1e-3), max(pp, 1e-3))
            text(ctx, f"+{YR[2024] * 100:.0f}%", 0, 0, 150, GRNC, 1, HEAD, True, "center", outline=16, ocol=C["ink"])
            ctx.restore()
            text(ctx, "SPY 2024 · WITH DIVIDENDS", 360, 1050, 24, C["white"], 0.85, MONO, True, "center", outline=5, ocol=C["ink"])
    if t > T["Without"] - 0.1:
        stamp_box(ctx, ["WITHOUT HIM"], 760, 1120, T["Without"] - 0.05, t, C["red"], 560, 64, -0.05)
    bunting(ctx, "THE LAST YEAR", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "none", lambda e: "shock" if (e != "talk" and t > T["soars"]) else e)


def footnote(ctx, t):
    if t >= T["Big"] - 0.1:
        a = back(prog(t, T["Big"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 985); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -480, -42, 960, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=HCOL)
        s_ = f"EVERY TRIGGER LOSES: +10% {money(THS['0.1'])} · +25% {money(THS['0.25'])} · +30% {money(THS['0.3'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 36, 910, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024 · 6 YEARS IN CASH", W / 2, 400, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 420, 900, 190, "SITS OUT", money(SO_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 625, 900, 190, "STAYS IN", money(BH_V), HCOL, T["rev2"], t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    bunting(ctx, "SCOREBOARD", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["BIG YEARS AREN'T", "WARNINGS."], W / 2, 540, T["Big"] - 0.05, t, STAMP_OR, 860, 76, -0.05)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1110)
    fb = back(prog(t, T["warnings"] + 0.1, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 845); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #48", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "guess": s_guess, "belief": s_belief, "rule": s_rule, "y2010": s_y2010, "skips": s_skips,
            "y2022": s_y2022, "remember": s_remember, "lastyear": s_lastyear, "score": s_score, "verdict": s_verdict, "loop": s_loop}
