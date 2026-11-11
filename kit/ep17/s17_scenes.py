# ================================================================ Autopsy #17 scenes (is 2007 happening again?)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD
PCOL = (0xFF, 0x6B, 0x3D)    # PANIC SELLER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x1C, 0x10, 0x3A), (0x05, 0x03, 0x10)
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
    a = ease(prog(t, SC["top"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #17", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(HOLD_V), 805, 78, fit(ctx, money(HOLD_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["top"]) / (T["twice"] - SC["top"]))
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







# ---------------------------------------------------------------- race chart (Oct 2007 -> 2024, two top buyers)
XE = di("2013-12-31")


def race_chart(ctx, t, up, zones=(), curtain=None):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), B0, XE, RBOX); x1 = sx_of(di(d1), B0, XE, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2008, 2009, 2010, 2011, 2012, 2013):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), B0, XE, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    up = max(B0 + 2, up)
    lim = curtain if curtain is not None else up
    vmax = max(13000.0, 1.15 * float(max(np.nanmax(HV[B0:min(up, lim) + 1]), np.nanmax(PV[B0:min(up, lim) + 1]))))
    vmin = 3000.0
    yb = RBOX[1] + RBOX[3] - (10000 - vmin) / (vmax - vmin) * RBOX[3]
    for j in range(22):
        rect(ctx, RBOX[0] + j * 40, yb - 2, 22, 4, GOLD, 0.55)
    text(ctx, "$10,000 PAID", RBOX[0] + RBOX[2] - 10, yb - 12, 22, GOLD, 0.9, MONO, True, "right")
    if curtain is not None:
        up = min(up, curtain)
    tips = []
    for arr, col in ((HV, HCOL), (PV, PCOL)):
        xs, ys = series_xy(arr, B0, XE, up, RBOX, vmin, vmax, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        tips.append((xs[-1], ys[-1]))
    (hx, hy), (px_, py_) = tips
    lead_p = PV[up] > HV[up]
    off = 0 if abs(hy - py_) > 60 else 60
    mini_rocco(ctx, hx, hy - 4 - (off if lead_p else 0), 4, "tophat", t, "sad" if lead_p else "smug", False, True)
    mini_rocco(ctx, px_, py_ - 4 - (0 if lead_p else off), 4, "fire", t, "smug" if lead_p else "sad", False, True)
    if curtain is not None:
        xc = sx_of(curtain, B0, XE, RBOX) + 14
        curtain_box(ctx, t, xc, RBOX[1] - 10, RBOX[0] + RBOX[2] + 10, RBOX[3] + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("PANIC SELLER", PCOL), ("HOLDER", HCOL))):
        rect(ctx, RBOX[0] + 150 + k * 360, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 196 + k * 360, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")


def peak_mountain(ctx, cx, base, w, h, t, col=None, a=1.0, k=1.0):
    """generic 2003-2009 shaped price mountain with a sharp crash (drawn shape, not data)"""
    pts = [(0, 0.10), (0.15, 0.30), (0.30, 0.50), (0.45, 0.72), (0.55, 1.0), (0.62, 0.80), (0.70, 0.55), (0.80, 0.18), (0.88, 0.05),
           (1.0, 0.25)]
    n = max(2, int(len(pts) * k))
    xs = [cx - w / 2 + u * w for u, _ in pts[:n]]; ys = [base - v * h for _, v in pts[:n]]
    poly(ctx, xs, ys, col or C["white"], 10, a, glow=True)
    return cx - w / 2 + 0.55 * w, base - h


# ---------------------------------------------------------------- 1 hook (frame 0: 2007 / AGAIN?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 620, t, 0.08, C["red"], 14, 1400)
    for k in range(30):
        u = ((t * 0.3) + k / 30) % 1
        rect(ctx, (k * 137) % W, u * 1500, 4, 40, REDC, 0.16)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 540); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "2007", 0, 0, fit(ctx, "2007", 330, 900), C["red"], 1, HEAD, True, "center", outline=26, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 770); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "AGAIN?", 0, 0, fit(ctx, "AGAIN?", 230, 940), C["white"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    peak_mountain(ctx, 300, 1180, 420, 300 * max(p, 1e-3), t, C["red"], 0.9)
    if show_tag:
        tag(ctx, 540, 180, "EVERYONE'S ASKING", C["cream"], p, 46, -0.04)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 you bought the exact top
def s_top(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x2A, 0x06), (0x10, 0x0A, 0x02))
    god_rays(ctx, W / 2, 650, t, 0.12, GOLD, 16, 1500)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "YOU BOUGHT", W / 2, 440, 110, C["white"], p, 900, -0.02, 12)
    q = back(prog(t, T["exact"] - 0.15, 0.3))
    big_title(ctx, "THE EXACT TOP", W / 2, 590, 140, GOLD, q, 980, 0.02, 16)
    k = ease(prog(t, s0 + 0.1, 1.2))
    px_, py_ = peak_mountain(ctx, 540, 1150, 760, 330, t, C["white"], 1, 0.55 + 0.45 * k)
    f = back(prog(t, T["top1"] - 0.1, 0.35))
    if f > 0:
        ctx.save(); ctx.translate(px_, py_); ctx.scale(max(f, 1e-3), max(f, 1e-3))
        rect(ctx, -4, -120, 8, 120, C["ink"])
        ctx.new_path(); ctx.move_to(4, -120); ctx.line_to(110, -95); ctx.line_to(4, -70); ctx.close_path()
        ctx.set_source_rgba(*rgba(C["red"])); ctx.fill()
        ctx.new_path(); ctx.arc(0, 0, 16, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD)); ctx.fill()
        ctx.restore()
    tag(ctx, px_ + 250, py_ - 30, "OCT 2007 · RECORD HIGH", C["cream"], back(prog(t, T["October"] - 0.15, 0.3)), 34, -0.03)
    bunting(ctx, "THE TOP", t, s0, [GOLD, C["ink"], C["red"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 3 how long to break even?
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x0E, 0x2A, 0x4A), (0x03, 0x0A, 0x16))
    speed_lines(ctx, t)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "HOW LONG", W / 2, 470, 200, C["white"], p, 960, -0.03, 20)
    q = back(prog(t, T["even1"] - 0.3, 0.3))
    big_title(ctx, "TO BREAK EVEN?", W / 2, 650, 130, GOLD, q, 980, 0.02, 14)
    hourglass(ctx, 300, 930, 0.9 * max(p, 1e-3), t)
    clock(ctx, 780, 930, 130 * max(q, 1e-3) + 1, t, 4.0)
    bunting(ctx, "THE QUESTION", t, s0, [HCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


# ---------------------------------------------------------------- 4 guess
def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(10):
        u = ((t - s0) * 0.4 + k / 10) % 1
        hourglass(ctx, (k * 211 + 80) % W, 1300 - u * 1150, 0.2, t + k)
    hp = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "BACK TO EVEN IN...", W / 2, 420, 90, C["white"], hp, 980, 0, 12)
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "UNDER", "5 YEARS", GRNC, -225, T["A"]),
                                                        ("B", "OVER", "5 YEARS", PCOL, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["years2"]
        hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -40, 200, C["ink"], 1, HEAD, True, "center")
        if k == 0:
            arrow_down(ctx, 0, 30, 0.3, C["white"])
        else:
            arrow_up(ctx, 0, 30, 0.3, C["white"])
        text(ctx, sub1, 0, 115, fit(ctx, sub1, 50, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 160, fit(ctx, sub2, 44, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["years2"] - 0.2, T["years2"] + 2.3, "guess", y=1080)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 5 hidden: one thing most people forget
def thing_file(ctx, cx, cy, t, a, inner="?????????"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.04)
    card(ctx, -330, -150, 660, 300, (0xC8, 0x9B, 0x5A), a, 18, border=C["ink"])
    card(ctx, -330, -190, 240, 60, (0xC8, 0x9B, 0x5A), a, 12, shadow=False, border=C["ink"])
    text(ctx, "EVIDENCE", -210, -148, 30, C["ink"], a, TAGF, False, "center")
    text(ctx, "THE FORGOTTEN THING", 0, -60, fit(ctx, "THE FORGOTTEN THING", 70, 600), C["ink"], a, HEAD, True, "center")
    rect(ctx, -270, 0, 540, 110, (0x05, 0x05, 0x05), a)
    text(ctx, inner, 0, 78, 56, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 6, 0, 12, 110, GOLD, 0.7 * a)
    ctx.restore()


def s_hidden(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    stars(ctx, t, 30, 180, 1150, 5, 0.6)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "ONE THING PEOPLE FORGET...", W / 2, 420, 84, C["white"], p, 980, 0, 12)
    q = back(prog(t, T["forget"] - 0.35, 0.4))
    if q > 0:
        ctx.save(); ctx.translate(540, 730); ctx.scale(max(q, 1e-3), max(q, 1e-3)); thing_file(ctx, 0, 0, t, 1); ctx.restore()
    sticker(ctx, t, T["years2"] - 0.2, T["years2"] + 2.3, "guess", y=1080)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 6 rules: two top buyers (+ race starts underneath)
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt, hw) in enumerate((("HOLDER", "HOLDS NO MATTER WHAT", HCOL, 290, T["One2"], T["holds"]),
                                                     ("PANIC SELLER", "SELLS AT -40%, BACK AT A RECORD", PCOL, 790, T["The1"], T["record"]))):
        p = back(prog(t, tt - 0.12, 0.4))
        if p <= 0:
            continue
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, hw - 0.05, 0.4))
        ctx.save(); ctx.translate(x, 470); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
        card(ctx, -230, -110, 460, 220, col, 1, 22, border=C["ink"])
        if k == 0:
            hourglass(ctx, -165, 0, 0.45, t)
        else:
            arrow_down(ctx, -165, 0, 0.4, C["white"])
        text(ctx, title, 40, -10, fit(ctx, title, 76, 310), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 40, 55, fit(ctx, l1, 36, 310), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    rc = ease(prog(t, s0 + 0.05, 0.4))
    if rc > 0:
        up = race_idx(t, [(s0 + 0.3, B0 + 2), (s1, di("2008-01-31"))])
        ctx.save(); ctx.translate(0, (1 - rc) * 200)
        race_chart(ctx, t, up)
        ctx.restore()
    bunting(ctx, "TWO TOP BUYERS", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2008-01-31")), (T["sells2"] + 0.1, I_SELL), (s1, I_SELL + 5)]
    race_chart(ctx, t, race_idx(t, pts), [("2008-01-01", "2009-03-09", C["red"], 0.2)])
    tag(ctx, 540, 440, "2008: DOWN 40%", C["red"], back(prog(t, T["Down"] - 0.15, 0.3)), 46, -0.03, C["white"])
    if t > T["sells2"] - 0.1:
        stamp_box(ctx, ["HE SELLS"], 540, 535, T["sells2"] - 0.1, t, C["red"], 360, 54, 0.04)
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: "shock" if e != "talk" else e, prop=prop_umbrella if False else None)


def s_waits(ctx, t, s0, s1):
    bg_fill(ctx, (0x0B, 0x10, 0x2A), (0x02, 0x03, 0x0A))
    stars(ctx, t, 50, 160, 1200, 7, 0.8)
    moon(ctx, 960, 330, 50)
    pts = [(s0 + 0.1, I_SELL + 5), (s1 - 0.2, I_BUY - 3)]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, [(SELL_D, BUY_D, PCOL, 0.10)], curtain=I_BUY - 3 if t > s1 - 0.25 else None)
    yr = DATES[min(up, N - 1)].year
    tag(ctx, 540, 440, "HE WAITS..." if t < T["waits2"] - 0.1 else "...AND WAITS", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 46, -0.03)
    tag(ctx, 540, 524, f"IN CASH · {yr}", PCOL, 1, 38, 0.02)
    zz = (t * 0.8) % 1
    text(ctx, "Z", 930 + zz * 50, 1300 - zz * 120, 40 + zz * 40, C["white"], 1 - zz, HEAD, True, "center", outline=6, ocol=C["ink"])
    bunting(ctx, "THE WAIT", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: "sleep" if (e != "talk" and t > T["waits1"]) else e)


# ---------------------------------------------------------------- 9 strange: bought back at nearly double
def price_tag(ctx, x, y, label, h, col, p, t):
    if p <= 0:
        return
    rect(ctx, x - 90, 1010 - h * p, 180, h * p, col)
    ctx.save(); ctx.new_path(); ctx.rectangle(x - 90, 1010 - h * p, 180, h * p); ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(7); ctx.stroke(); ctx.restore()
    text(ctx, label, x, 1060, 40, C["white"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])


def s_strange(ctx, t, s0, s1):
    bg_fill(ctx, (0x2A, 0x08, 0x12), (0x08, 0x02, 0x04))
    for k in range(40):
        u = ((t - s0) * 0.35 + k / 40) % 1
        rect(ctx, (k * 137) % W, u * 1300, 4, 46, REDC, 0.18)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "NOW THE STRANGE PART", W / 2, 430, 96, GOLD, p, 980, -0.02, 12)
    hs = 220.0; hb = hs * (1 + MISSED / 100)
    price_tag(ctx, 330, 0, "SOLD AT", hs, PCOL, ease(prog(t, T["Heres"] + 0.2, 0.6)), t)
    price_tag(ctx, 750, 0, "BOUGHT BACK", hb, C["red"], ease(prog(t, T["back"] - 0.1 if "back" in T else T["double"] - 0.4, 0.6)), t)
    q = back(prog(t, T["double"] - 0.1, 0.35))
    big_title(ctx, "NEARLY DOUBLE", W / 2, 590, 120, C["red"], q, 960, -0.02, 14)
    if t > T["sold"] - 0.1:
        stamp_box(ctx, ["x2"], 540, 830, T["sold"] - 0.1, t, C["red"], 180, 80, -0.08)
    bunting(ctx, "STRANGE", t, s0, [C["red"], C["ink"], GOLD, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("shock" if t > T["double"] else "neutral") if e != "talk" else e)


# ---------------------------------------------------------------- 10 remember: dividends
def be_chart(ctx, t, k1, k2):
    bx, by, bw, bh = 120, 600, 840, 360
    card(ctx, bx - 20, by - 20, bw + 40, bh + 40, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    i0, i1 = B0, I_BEP + 60
    lo, hi = 4000.0, 11500.0
    yb = by + bh - (10000 - lo) / (hi - lo) * bh
    for j in range(21):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, GOLD, 0.7)
    text(ctx, "BREAK EVEN", bx + 12, yb - 14, 24, GOLD, 0.9, MONO, True, "left")
    for arr, col, k, lab in ((PRICE_V, (0x9A, 0xA0, 0xA8), k2, "PRICE ONLY"), (HV, GRNC, k1, "WITH DIVIDENDS")):
        n = int(i0 + 2 + (i1 - i0 - 2) * k)
        xs, ys = series_xy(arr, i0, i1, n, (bx, by, bw, bh), lo, hi, 3)
        poly(ctx, xs, ys, col, 8, 1, glow=True)
        if k > 0.05:
            ctx.new_path(); ctx.arc(xs[-1], ys[-1], 12, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col)); ctx.fill()
    for yr in (2008, 2010, 2012):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), i0, i1, (bx, by, bw, bh)), by + bh + 2, 22, C["white"], 0.7, MONO, True, "center")
    return (bx, by, bw, bh, i0, i1, yb)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x3A), (0x04, 0x05, 0x14))
    god_rays(ctx, W / 2, 700, t, 0.07, GOLD, 14, 1400)
    if t < T["Dividends"] - 0.1:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THE FORGOTTEN THING?", W / 2, 670, 100, C["white"], r, 980, 0, 12)
        ctx.save(); ctx.translate(540, 950); ctx.scale(0.72, 0.72); thing_file(ctx, 0, 0, t, 1); ctx.restore()
    else:
        p = back(prog(t, T["Dividends"] - 0.1, 0.35))
        pulse = 1 + 0.03 * math.sin(t * 7)
        big_title(ctx, "DIVIDENDS", W / 2, 500, 170, GRNC, p * pulse, 960, -0.02, 18)
        k1 = ease_io(clamp((t - T["With"] + 0.2) / max(0.5, T["half"] - T["With"] + 0.2)))
        k2 = ease_io(clamp((t - T["Without"] + 0.1) / max(0.5, T["five3"] + 0.3 - T["Without"])))
        g = be_chart(ctx, t, k1 * (I_BET - B0) / (I_BEP + 60 - B0) if t < T["Without"] else 1.0 if False else max(k1 * (I_BET - B0) / (I_BEP + 60 - B0), 0), k2)
        bx, by, bw, bh, i0, i1, yb = g
        if t > T["four"] - 0.1:
            x = sx_of(I_BET, i0, i1, (bx, by, bw, bh))
            tag(ctx, x - 40, yb - 70, "4.5 YEARS", GRNC, back(prog(t, T["four"] - 0.1, 0.3)), 36, -0.03)
        if t > T["five3"] - 0.1:
            x = sx_of(I_BEP, i0, i1, (bx, by, bw, bh))
            tag(ctx, min(x, 860), yb + 70, "5+ YEARS", C["grey"], back(prog(t, T["five3"] - 0.1, 0.3)), 34, 0.03, C["ink"])
        tag(ctx, 540, 1085, "SAME TOP · SAME $10,000", C["cream"], back(prog(t, T["With"] - 0.1, 0.3)), 36, -0.015)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], C["blue"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["half"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 11 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -42, 900, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=PCOL)
        s_ = "SELL AT -20%, -30% OR -50% INSTEAD: ALL LOST TO HOLDING"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 860, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 AT THE 2007 TOP · 2024", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · PANIC SELLER (0.05% FEES)", money(PAN_V), PCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · HOLDER", money(HOLD_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["Selling"] - 0.15, "right", y=1080)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x04, 0x02, 0x0A), 0.8)
    stamp_box(ctx, ["BUYING THE TOP HURT."], W / 2, 495, T["Buying"] - 0.05, t, STAMP_OR, 860, 80, -0.05)
    stamp_box(ctx, ["SELLING THE BOTTOM", "HURT TWICE."], W / 2 + 10, 770, T["Selling"] - 0.05, t, C["red"], 860, 80, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["Selling"] - 0.15, "right", y=1080)
    fb = back(prog(t, T["Selling"] + 0.1, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1070); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #18", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "top": s_top, "question": s_question, "guess": s_guess, "hidden": s_hidden, "rules": s_rules,
            "crash": s_crash, "waits": s_waits, "strange": s_strange, "remember": s_remember, "score": s_score,
            "verdict": s_verdict, "loop": s_loop}
