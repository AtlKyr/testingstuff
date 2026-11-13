# ================================================================ Autopsy #21 scenes (Friday the 13th)
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
    a = ease(prog(t, SC["unlucky"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #21", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["unlucky"]) / (T["dollars"] - SC["unlucky"]))
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

LCOL = (0xB8, 0x7C, 0xFF)   # SKIPPER (purple)


def race_chart(ctx, t, up, xe, curtain=None, a=1.0, years=(2005, 2006, 2007, 2008, 2009, 2010)):
    bx, by, bw, bh = RBOX
    card(ctx, bx - 30, by - 30, bw + 60, bh + 100, (0x0C, 0x10, 0x1C), 0.92 * a, 18, border=C["grey"])
    up = max(S0 + 2, up)
    if curtain is not None:
        up = min(up, curtain)
    for i in F13:   # every Friday the 13th: a small red tick
        if i > min(up, xe):
            break
        x0 = sx_of(i, S0, xe, RBOX)
        rect(ctx, x0 - 2, by + bh - 26, 4, 26, C["red"], 0.9 * a)
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
    off = 0 if abs(hy - ly) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - off, 4, "tophat", t, "smug", False, True)
    mini_rocco(ctx, lx, ly - 4, 4, "night", t, "neutral", False, True)
    if curtain is not None:
        xc = sx_of(curtain, S0, xe, RBOX) + 14
        if xc < bx + bw - 120:
            curtain_box(ctx, t, xc, by - 10, bx + bw + 10, bh + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("SKIPPER", LCOL), ("HOLDER", HCOL))):
        rect(ctx, bx + bw - 260, by + bh - 62 + k * 34, 30, 10, col)
        text(ctx, lab, bx + bw - 220, by + bh - 50 + k * 34, 24, col, 1, MONO, True, "left")
    rect(ctx, bx + 20, by + bh - 62, 4, 22, C["red"])
    text(ctx, "= FRIDAY 13TH", bx + 34, by + bh - 45, 22, C["white"], 0.8, MONO, True, "left")


XE1 = di("2010-12-31"); XE2 = N - 1
YR2 = (2006, 2010, 2014, 2018, 2022)


def calendar(ctx, cx, cy, s, t, top="FRIDAY", num="13", a=1.0, rot=-0.04, numcol=None):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    card(ctx, -170, -190, 340, 380, C["white"], a, 26, border=C["ink"])
    ctx.save(); rrect(ctx, -170, -190, 340, 110, 26); ctx.clip(); rect(ctx, -170, -190, 340, 110, REDC, a); ctx.restore()
    rect(ctx, -170, -100, 340, 10, C["ink"], a)
    for xx in (-90, 90):
        rect(ctx, xx - 10, -215, 20, 60, C["ink"], a)
    text(ctx, top, 0, -112, fit(ctx, top, 70, 300), C["white"], a, HEAD, True, "center")
    text(ctx, num, 0, 150, 230, numcol or C["ink"], a, HEAD, True, "center")
    ctx.restore()


def black_cat(ctx, x, y, s, t, walk=True, flip=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    K = (0x0A, 0x0A, 0x10); RIM = (0xB8, 0xA8, 0xF0)
    ph = math.sin(t * 10) if walk else 0
    for pas in (0, 1):
        col = RIM if pas == 0 else K
        g = 7 if pas == 0 else 0
        ctx.set_source_rgba(*rgba(col))
        ctx.new_path(); ctx.save(); ctx.scale(1.6, 1); ctx.arc(0, 0, 60 + g / 1.6, 0, 2 * math.pi); ctx.restore(); ctx.fill()
        ctx.new_path(); ctx.arc(105, -55, 42 + g, 0, 2 * math.pi); ctx.fill()
        for ex in (80, 125):
            ctx.new_path(); ctx.move_to(ex - 18 - g, -85 + g); ctx.line_to(ex - 4, -125 - g); ctx.line_to(ex + 14 + g, -85 + g); ctx.close_path(); ctx.fill()
        for k, lx in enumerate((-60, -30, 40, 70)):
            sw = ph * 16 * (1 if k % 2 else -1)
            rect(ctx, lx + sw - g, 35, 16 + 2 * g, 55 + g, col)
        ctx.new_path(); ctx.move_to(-90, -10); ctx.curve_to(-160, -40, -150, -130 + 10 * math.sin(t * 4), -110, -150)
        ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(16 + 2 * g); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    for ex in (92, 120):
        ctx.new_path(); ctx.arc(ex, -60, 8, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD)); ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: calendar FRIDAY 13 / SKIP IT?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, (0x1C, 0x0E, 0x30), (0x04, 0x02, 0x08))
    moon(ctx, 880, 300, 70, 1.0)
    stars(ctx, t, 40, 100, 1100, 9, 0.8)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    calendar(ctx, 540 + shake, 470, 1.05 * s_, t)
    ctx.save(); ctx.translate(540, 860); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "SKIP IT?", 0, 0, 220, GOLD, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    black_cat(ctx, 230 + math.sin(t * 1.3) * 40, 1080, 0.85 * max(p, 1e-3), t)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 the unluckiest day
def s_unlucky(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x0C, 0x22), (0x02, 0x02, 0x06))
    for k in range(40):
        u = ((t - s0) * 0.5 + k / 40) % 1
        rect(ctx, (k * 137) % W, u * 1300, 3, 40, (0x80, 0x90, 0xC0), 0.18)
    big_title(ctx, "THE UNLUCKIEST", W / 2, 520, 140, C["white"], back(prog(t, T["unluckiest"] - 0.25, 0.3)), 980, -0.03, 16)
    big_title(ctx, "DAY?", W / 2, 700, 170, REDC, back(prog(t, T["unluckiest"] + 0.2, 0.3)), 980, 0.03, 16)
    # ladder + walking cat
    lx = 760
    for sx in (-60, 60):
        rect(ctx, lx + sx, 700, 14, 420, (0x8B, 0x5A, 0x2B))
    for k in range(6):
        rect(ctx, lx - 60, 740 + k * 70, 134, 12, (0x8B, 0x5A, 0x2B))
    cx = 1200 - ((t - s0) / max(0.1, s1 - s0)) * 1500
    black_cat(ctx, cx, 1110, 0.8, t, flip=True)
    bunting(ctx, "FRIDAY THE 13TH", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 what if you skipped every one (35 calendar pages)
def cal_grid(ctx, t, t0, cols=None, y0=420, a=1.0):
    for k in range(35):
        cx = 150 + (k % 7) * 130; cy = y0 + (k // 7) * 125
        q = back(prog(t, t0 + k * 0.03, 0.25))
        if q <= 0:
            continue
        ctx.save(); ctx.translate(cx, cy); ctx.scale(max(q, 1e-3), max(q, 1e-3)); ctx.rotate(((k * 37) % 7 - 3) * 0.02)
        col = cols[k] if cols else C["white"]
        card(ctx, -52, -52, 104, 104, col, a, 12, shadow=False, border=C["ink"])
        rect(ctx, -52, -52, 104, 26, REDC, a)
        text(ctx, "13", 0, 40, 54, C["ink"], a, HEAD, True, "center")
        ctx.restore()


def s_whatif(ctx, t, s0, s1):
    grid_bg(ctx, (0x22, 0x18, 0x40), (0x08, 0x06, 0x16))
    big_title(ctx, "SKIP EVERY ONE?", W / 2, 480, 120, GOLD, back(prog(t, T["skipped"] - 0.2, 0.3)), 980, -0.02, 16)
    cal_grid(ctx, t, T["every"] - 0.1, y0=600)
    if t > T["market1"] - 0.2:
        x_ = ease(prog(t, T["market1"] - 0.2, 0.5))
        for k in range(35):
            if k / 35 < x_:
                cx = 150 + (k % 7) * 130; cy = 600 + (k // 7) * 125
                xmark(ctx, cx, cy, 34, C["red"], 10)
    bunting(ctx, "THE IDEA", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 4 guess (race starts under the cards)
def ab_cards(ctx, t, ta, tb, y=420, blink_on=None):
    blink = int(t * 4) % 2
    for k, (lab, l1, l2, col, x, tt) in enumerate((("A", "SKIPPER", "DODGES?", LCOL, -230, ta), ("B", "HOLDER", "WINS?", HCOL, 230, tb))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = blink_on is not None and t > blink_on and blink == k
        ctx.save(); ctx.translate(W / 2 + x, y); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
        card(ctx, -210, -110, 420, 210, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, -130, 50, 150, C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 60, -12, fit(ctx, l1, 56, 230), C["ink"], 1, HEAD, True, "center")
        text(ctx, l2, 60, 52, fit(ctx, l2, 56, 230), C["ink"], 1, HEAD, True, "center")
        ctx.restore()


RACE1 = lambda t: race_idx(t, [(T["B"], S0 + 2), (SC["count"], di("2007-06-29"))])


def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    ab_cards(ctx, t, T["A"], T["B"], 420, T["wins"])
    rc = ease(prog(t, T["B"] - 0.2, 0.4))
    if rc > 0:
        ctx.save(); ctx.translate(0, (1 - rc) * 300); race_chart(ctx, t, RACE1(t), XE1, a=rc); ctx.restore()
    sticker(ctx, t, T["wins"] - 0.1, T["wins"] + 2.3, "guess", y=1085)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 5 the clue: one Friday
def evidence(ctx, cx, cy, t, a=1.0, label="THE DATE"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.03)
    card(ctx, -300, -70, 600, 140, (0xC8, 0x9B, 0x5A), a, 16, border=C["ink"])
    text(ctx, "EVIDENCE: " + label, -270, -22, 30, C["ink"], a, TAGF, False, "left")
    rect(ctx, -270, 0, 540, 52, (0x05, 0x05, 0x05), a)
    text(ctx, "FRI ??/13/20??", 0, 42, 40, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 5, 0, 10, 52, GOLD, 0.7 * a)
    ctx.restore()


def s_clue(ctx, t, s0, s1):
    bg_fill(ctx, (0x12, 0x18, 0x36), (0x03, 0x05, 0x10))
    stars(ctx, t, 30, 180, 1150, 5, 0.5)
    big_title(ctx, "ONE FRIDAY IS HIDING...", W / 2, 425, 92, C["white"], back(prog(t, s0 + 0.03, 0.3)), 980, -0.02, 12)
    q = back(prog(t, T["Friday3"] - 0.1, 0.35))
    if q > 0:
        ctx.save(); ctx.translate(540, 515); ctx.scale(max(q * 0.88, 1e-3), max(q * 0.88, 1e-3)); evidence(ctx, 0, 0, t); ctx.restore()
    race_chart(ctx, t, RACE1(t), XE1)
    sticker(ctx, t, T["wins"] - 0.1, T["wins"] + 2.3, "guess", y=1085)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 6 rules
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("THURSDAY CLOSE", "SELL", REDC, 290, T["sell"]),
                                                 ("FRIDAY 13 CLOSE", "BUY BACK", GRNC, 790, T["buy"]))):
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
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 7 35 times in 20 years
def s_count(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x10, 0x30), (0x08, 0x03, 0x0A))
    big_title(ctx, "35 TIMES IN 20 YEARS", W / 2, 480, 110, GOLD, back(prog(t, T["Thirtyfive"] - 0.15, 0.3)), 980, -0.02, 14)
    cal_grid(ctx, t, s0 + 0.05, y0=600)
    bunting(ctx, "THE COUNT", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 8 2008-09: neck and neck
def s_neck(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-06-29")), (T["neck1"] + 0.4, di("2010-12-31"))]
    race_chart(ctx, t, race_idx(t, pts), XE1)
    tag(ctx, 540, 440, "2008 & 2009", C["red"], back(prog(t, T["Through"], 0.3)), 50, -0.03, C["white"])
    if t > T["neck1"] - 0.15:
        tag(ctx, 540, 530, "NECK AND NECK", GOLD, back(prog(t, T["neck1"] - 0.15, 0.3)), 46, 0.02, C["ink"])
    bunting(ctx, "THE RACE", t, s0, [C["red"], C["ink"], LCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 9 the unlucky days? 20 of 35 went up
UPCOL = [GRNC if d[1] > 0 else REDC for d in DAYS]


def s_updays(ctx, t, s0, s1):
    bg_fill(ctx, (0x0A, 0x2A, 0x1C), (0x02, 0x08, 0x05))
    god_rays(ctx, W / 2, 700, t, 0.07, GRNC, 16, 1500)
    if t < T["Twenty"] - 0.1:
        big_title(ctx, "THE UNLUCKY DAYS?", W / 2, 480, 110, C["white"], back(prog(t, s0 + 0.05, 0.3)), 980, -0.02, 14)
        cal_grid(ctx, t, s0 - 2, y0=600)
    else:
        big_title(ctx, "20 OF 35 WENT UP", W / 2, 480, 110, GRNC, back(prog(t, T["Twenty"] - 0.1, 0.3)), 980, -0.02, 14)
        k = prog(t, T["Twenty"], 1.6)
        cols = [UPCOL[i] if i / 35 < k else C["white"] for i in range(35)]
        cal_grid(ctx, t, s0 - 2, cols=cols, y0=600)
    bunting(ctx, "BAD LUCK?", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: ("shock" if t > T["up"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 10 remember that one Friday -> March 13 2020
def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    for k in range(40):
        u = ((t - s0) * 0.35 + k / 40) % 1
        rect(ctx, (k * 137) % W, u * 1300, 4, 46, REDC, 0.16)
    if t < T["March"] - 0.12:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 500, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT ONE FRIDAY?", W / 2, 650, 104, C["white"], r, 980, 0, 14)
    else:
        p = back(prog(t, T["March"] - 0.12, 0.35))
        calendar(ctx, 540, 640, 1.0 * max(p, 1e-3), t, "MARCH 2020", "13", rot=0.03)
        if t > T["Covid"] - 0.1:
            tag(ctx, 540, 1000 + 40, "THE COVID PANIC", REDC, back(prog(t, T["Covid"] - 0.1, 0.3)), 52, -0.03, C["white"])
    bunting(ctx, "THE ONE FRIDAY", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["March"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 11 +8.55% that day; skipper was out
def s_jump(ctx, t, s0, s1):
    bg_fill(ctx, (0x06, 0x30, 0x1A), (0x01, 0x0A, 0x05))
    god_rays(ctx, W / 2, 620, t, 0.12, GRNC, 16, 1500)
    k = ease(prog(t, T["jumped"] - 0.1, 0.8))
    if k > 0:
        h = 520 * k
        candle(ctx, 110, 1020 - h, 110, h, GRNC, 1, 40)
    p = back(prog(t, T["eight"] - 0.1, 0.35))
    v = f"+{_R['best'][1]:.2f}%"
    big_title(ctx, v, 650, 640, 190, GRNC, p, 560, -0.04, 20)
    text(ctx, "MARCH 13, 2020 · ONE DAY", 640, 740, 32, C["white"], ease(prog(t, T["eight"], 0.3)), MONO, True, "center", outline=6, ocol=C["ink"])
    if t > T["out"] - 0.25:
        tag(ctx, 640, 860, "SKIPPER: OUT", LCOL, back(prog(t, T["out"] - 0.25, 0.3)), 56, 0.03, C["ink"])
    bunting(ctx, "THAT DAY", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("sleep" if t > T["out"] - 0.2 else "shock") if e != "talk" else e)


# ---------------------------------------------------------------- 12 the gap never closed
def s_gap(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    pts = [(s0 + 0.05, di("2019-12-31")), (T["gap"], di("2020-03-31")), (T["closed"] + 0.4, di("2021-12-31"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, XE2, curtain=up + 1, years=YR2)
    tag(ctx, 540, 440, "THE GAP OPENS", GOLD, back(prog(t, T["gap"] - 0.15, 0.3)), 50, -0.03, C["ink"])
    if t > T["closed"] - 0.2:
        tag(ctx, 540, 530, "...AND NEVER CLOSES", C["red"], back(prog(t, T["closed"] - 0.2, 0.3)), 44, 0.02, C["white"])
    bunting(ctx, "AFTER 2020", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: ("sad" if t > T["closed"] else "shock") if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 13 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -460, -42, 920, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=LCOL)
        s_ = f"NO FEES: {money(_R['final_nofee'])}  ·  HAD IT HELD MAR 13 2020: {money(_R['final_if_held_best'])}"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 870, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 · 2005 TO 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · THE SKIPPER (0.05% FEES)", money(SKIP_V), LCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · THE HOLDER", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 14 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["SUPERSTITION COST..."], W / 2, 470, T["Superstition"] - 0.05, t, STAMP_OR, 860, 76, -0.05)
    stamp_box(ctx, ["$10,000."], W / 2 + 10, 700, T["ten"] - 0.1, t, C["red"], 620, 110, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, END + 0.05, "right", y=1085)
    fb = back(prog(t, T["Superstition"] + 0.6, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 850); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #22", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "unlucky": s_unlucky, "whatif": s_whatif, "guess": s_guess, "clue": s_clue, "rules": s_rules,
            "count": s_count, "neck": s_neck, "updays": s_updays, "remember": s_remember, "jump": s_jump, "gap": s_gap,
            "score": s_score, "verdict": s_verdict, "loop": s_loop}
