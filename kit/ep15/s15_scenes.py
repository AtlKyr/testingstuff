# ================================================================ Autopsy #15 scenes (all in today, or drip it in over 12 months?)
HCOL = (0x4F, 0xC3, 0xF7)    # THE DRIPPER (1/12 every month)
PCOL = (0xFF, 0x9F, 0x1C)    # ALL-IN (everything on day one)
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x14, 0x2E, 0x6E), (0x04, 0x08, 0x1C)
STAMP_OR, STAMP_GR, STAMP_BL = (0xD0, 0x50, 0x00), (0x0B, 0x8A, 0x4C), (0x0B, 0x5A, 0xC0)
GX0, GY0, CW, RH, NROW = 215, 606, 61, 70, 6   # round grid: rows 2005..2010 x 12 months (2011-2023 classified until the score)


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
    a = ease(prog(t, SC["choice"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #15", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "??????", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, PCOL, a, 8, shadow=False)
        s_ = f"ALL-IN {L_WINS}-{D_WINS}"
        text(ctx, s_, 805, 78, fit(ctx, s_, 34, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["choice"]) / (T["pay"] - SC["choice"]))
    rect(ctx, 60, 112, 960, 16, (0, 0, 0), 0.55 * a)
    rect(ctx, 60, 112, 960 * k, 16, C["red"] if k < 1 else C["green"], a)
    text(ctx, f"AUTOPSY PROGRESS {int(k * 100)}%", 540, 147, 20, C["white"], 0.8 * a, MONO, True, "center", outline=5, ocol=C["ink"])


def gcoin(ctx, x, y, r, t, a=1.0, ph=0.0):
    sq = abs(math.cos(t * 3 + ph)) * 0.5 + 0.5
    ctx.save(); ctx.translate(x, y); ctx.scale(sq, 1)
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(GOLD, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(max(3, r * 0.12)); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, r * 0.68, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0xE0, 0x9A, 0x10), a)); ctx.set_line_width(max(2, r * 0.08)); ctx.stroke()
    text(ctx, "$", 0, r * 0.38, r * 1.1, C["ink"], a, HEAD, True, "center")
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: $10,000 / ALL IN / OR DRIP?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 620, t, 0.09, GOLD, 14, 1400)
    for k in range(12):                      # falling coins
        u = (t * 0.22 + k / 12) % 1
        gcoin(ctx, (k * 197 + 60) % (W - 60), -100 + u * 1500, 22 + 6 * (k % 3), t, 0.16, k)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 480); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "$10,000", 0, 0, fit(ctx, "$10,000", 290, 960), GOLD, 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(520, 690); ctx.rotate(0.03); ctx.scale(s_, s_)
    text(ctx, "ALL IN", 0, 0, fit(ctx, "ALL IN", 200, 900), PCOL, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(560, 890); ctx.rotate(-0.02); ctx.scale(s_, s_)
    text(ctx, "OR DRIP?", 0, 0, fit(ctx, "OR DRIP?", 200, 940), HCOL, 1, HEAD, True, "center", outline=22, ocol=C["ink"])
    ctx.restore()
    pp = max(p, 1e-3)
    gcoin(ctx, 170, 1060 + math.sin(t * 4) * 8, 74 * pp, t * 0.3, 1, 0)
    text(ctx, "VS", 300, 1080, 54 * pp, C["white"], 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    for k in range(12):
        gcoin(ctx, 385 + k * 54, 1060 + math.sin(t * 5 + k * 0.6) * 12, 23 * pp, t * 0.3, 1, k * 0.5)
    if show_tag:
        tag(ctx, 540, 190, "YOU HAVE", C["cream"], p, 52, -0.04)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if e != "talk" else e, prop=prop_coin)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "tophat", lambda e: "shock", prop=prop_coin)


# ---------------------------------------------------------------- 2 choice: all in today / or drip it in monthly for a year
def s_choice(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x18, 0x30), (0x04, 0x06, 0x10))
    # left: ALL IN
    lp = back(prog(t, s0 + 0.03, 0.3))
    card(ctx, 40, 370, 480, 760, (0x5A, 0x2E, 0x06), 0.92 * clamp(lp), 26, border=PCOL)
    big_title(ctx, "ALL IN", 280, 500, 150, PCOL, lp, 440, -0.03, 14)
    tag(ctx, 280, 590, "TODAY", GOLD, back(prog(t, T["today"] - 0.1, 0.3)), 50, 0.02)
    piggy(ctx, 280, 960, 1.0 * max(lp, 1e-3), t)
    dk = prog(t, T["All"] + 0.05, 0.55)
    if 0 < dk < 1:
        gcoin(ctx, 280, 620 + ease(dk) * 250, 70, t, 1)
    # right: DRIP
    rp = back(prog(t, T["drip1"] - 0.2, 0.3))
    if rp > 0:
        card(ctx, 560, 370, 480, 760, (0x06, 0x30, 0x52), 0.92 * clamp(rp), 26, border=HCOL)
        big_title(ctx, "DRIP IT", 800, 500, 150, HCOL, rp, 440, 0.03, 14)
        tag(ctx, 800, 590, "12 MONTHS", GOLD, back(prog(t, T["monthly"] - 0.1, 0.3)), 50, -0.02)
        span = max(0.6, T["year1"] + 0.25 - T["drip1"])
        for k in range(12):
            tk = T["drip1"] + 0.1 + k * span / 12
            cx = 612 + (k % 4) * 125; cy = 720 + (k // 4) * 130
            card(ctx, cx - 50, cy - 50, 100, 100, (0x04, 0x10, 0x20), 0.9, 12, shadow=False, border=C["grey"])
            text(ctx, MONTHS[k], cx, cy + 68, 20, C["white"], 0.7, MONO, True, "center")
            dk = prog(t, tk, 0.3)
            if dk > 0:
                gcoin(ctx, cx, cy - (1 - ease(dk)) * 200, 34, t, clamp(dk * 2), k)
    op = back(prog(t, T["or_"] - 0.1, 0.3))
    if op > 0:
        ctx.save(); ctx.translate(540, 760); ctx.scale(max(op, 1e-3), max(op, 1e-3))
        ctx.new_path(); ctx.arc(0, 0, 62, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["white"])); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(8); ctx.stroke()
        text(ctx, "OR", 0, 22, 62, C["ink"], 1, HEAD, True, "center"); ctx.restore()
    bunting(ctx, "THE CHOICE", t, s0, [PCOL, C["ink"], HCOL, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 3 guess
def s_guess(ctx, t, s0, s1):
    bg_fill(ctx, (0x24, 0x10, 0x3A), (0x08, 0x04, 0x14))
    for k in range(16):
        u = ((t - s0) * 0.45 + k / 16) % 1
        gcoin(ctx, (k * 211) % W, 1300 - u * 1150, 20, t, 0.22 * (1 - u), k)
    hp = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "$10,000. WHO ENDS UP AHEAD?", W / 2, 420, 84, C["white"], hp, 980, 0, 12)
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "ALL IN", "ON DAY ONE", PCOL, -225, T["A"]),
                                                        ("B", "THE DRIP", "OVER 12 MONTHS", HCOL, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["drip2"]
        hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -40, 200, C["ink"], 1, HEAD, True, "center")
        if k == 0:
            gcoin(ctx, 0, 25, 40, t * 0.2, 1)
        else:
            for q in range(4):
                gcoin(ctx, -66 + q * 44, 25, 17, t * 0.2, 1, q)
        text(ctx, sub1, 0, 115, fit(ctx, sub1, 50, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 162, fit(ctx, sub2, 40, 360), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["drip2"] - 0.1, T["drip2"] + 2.3, "guess", y=1080)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 4 hidden: one starting month changes everything
def month_file(ctx, cx, cy, t, a):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.04)
    card(ctx, -330, -150, 660, 300, (0xC8, 0x9B, 0x5A), a, 18, border=C["ink"])
    card(ctx, -330, -190, 240, 60, (0xC8, 0x9B, 0x5A), a, 12, shadow=False, border=C["ink"])
    text(ctx, "EVIDENCE", -210, -148, 30, C["ink"], a, TAGF, False, "center")
    text(ctx, "ONE START MONTH", 0, -60, 70, C["ink"], a, HEAD, True, "center")
    rect(ctx, -270, 0, 540, 110, (0x05, 0x05, 0x05), a)
    text(ctx, "???? 20??", 0, 74, 50, (0x70, 0x76, 0x7B), a, MONO, True, "center")
    sx = -270 + ((t * 0.9) % 1) * 540
    rect(ctx, sx - 6, 0, 12, 110, GOLD, 0.7 * a)
    ctx.restore()


def s_hidden(ctx, t, s0, s1):
    grid_bg(ctx, (0x2A, 0x2F, 0x5E), (0x10, 0x12, 0x2A))
    stars(ctx, t, 30, 180, 1150, 5, 0.6)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "ONE STARTING MONTH", W / 2, 420, 100, C["white"], p, 980, 0, 12)
    q = back(prog(t, T["changes"] - 0.15, 0.3))
    big_title(ctx, "CHANGES EVERYTHING", W / 2, 540, 100, GOLD, q, 980, -0.02, 12)
    r = back(prog(t, s0 + 0.25, 0.4))
    if r > 0:
        ctx.save(); ctx.translate(540, 800); ctx.scale(max(r, 1e-3), max(r, 1e-3)); month_file(ctx, 0, 0, t, 1); ctx.restore()
    sticker(ctx, t, T["drip2"] - 0.1, T["drip2"] + 2.3, "guess", y=1080)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- the race: one cell per round (start month), coloured by its winner
def round_grid(ctx, t, upto, curtain_row=None, streak=0.0, header=0.0):
    """rows 2005..2010 are shown big (one cell = one start month); 2011-2023 stay under the CLASSIFIED strip until the score."""
    card(ctx, 100, 592, 880, 548, (0x0C, 0x10, 0x1C), 0.94, 18, border=C["grey"])
    for m in range(12):
        text(ctx, MONTHS[m][0], GX0 + m * CW + CW / 2, GY0 + 16, 20, C["white"], 0.6, MONO, True, "center")
    for r in range(NROW):
        text(ctx, str(2005 + r), GX0 - 14, GY0 + 24 + r * RH + RH / 2 + 8, 24, C["white"], 0.85, MONO, True, "right")
    upto = max(0, min(NROW * 12, upto))
    for j in range(NROW * 12):
        x = GX0 + (j % 12) * CW; y = GY0 + 24 + (j // 12) * RH
        if j < upto:
            col = PCOL if WIN[j] else HCOL
            pk = 1 - clamp((upto - 1 - j) / 3.0) if j >= upto - 3 else 0
            g = 3 - pk * 5
            card(ctx, x + g, y + g, CW - 2 * g, RH - 2 * g, col, 1, 8, shadow=False, border=C["ink"])
            if WIN[j]:
                ctx.new_path(); ctx.arc(x + CW / 2, y + RH / 2, 11, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], 0.55)); ctx.fill()
            else:
                for q in range(3):
                    ctx.new_path(); ctx.arc(x + CW / 2 - 14 + q * 14, y + RH / 2, 4.5, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], 0.55)); ctx.fill()
        else:
            card(ctx, x + 3, y + 3, CW - 6, RH - 6, (0x2A, 0x30, 0x3C), 1, 8, shadow=False)
    if streak > 0:
        a, b = ri(STREAK_A), ri(STREAK_B)
        for j in range(a, min(b, upto - 1) + 1):
            x = GX0 + (j % 12) * CW; y = GY0 + 24 + (j // 12) * RH
            rrect(ctx, x + 3, y + 3, CW - 6, RH - 6, 8); ctx.set_source_rgba(*rgba(C["white"], streak * (0.65 + 0.35 * math.sin(t * 8 + j * 0.5))))
            ctx.set_line_width(5); ctx.stroke()
    top = GY0 + 24 + NROW * RH + 6; hh = 1128 - top
    ctx.save(); ctx.rectangle(112, top, 856, hh); ctx.clip()
    rect(ctx, 112, top, 856, hh, (0x05, 0x05, 0x05))
    for j in range(24):
        ctx.save(); ctx.translate(100 + j * 60 + ((t * 30) % 60), top - 10); ctx.rotate(0.6); rect(ctx, 0, 0, 18, 30, GOLD, 0.9); ctx.restore()
    text(ctx, "2011-2023: CLASSIFIED", 500, top + hh - 14, 40, C["red"], 1, HEAD, True, "center", outline=6, ocol=C["ink"])
    qs = 1 + 0.12 * math.sin(t * 7)
    text(ctx, "?", 880, top + hh - 8, 62 * qs, GOLD, 1, HEAD, True, "center", outline=8, ocol=C["ink"])
    ctx.restore()
    if 0 < upto < NROW * 12:
        j = upto - 1
        mini_rocco(ctx, GX0 + (j % 12) * CW + CW / 2, GY0 + 24 + (j // 12) * RH + 6, 3, "race", t, "smug", False, True)
    if header > 0:
        text(ctx, "EVERY START MONTH = ONE ROUND", W / 2, 578, 30, GOLD, header, MONO, True, "center", outline=6, ocol=C["ink"])


def fill_n(t, pts):
    if t <= pts[0][0]:
        return pts[0][1]
    for (a, ia), (b, ib) in zip(pts, pts[1:]):
        if t <= b:
            return int(round(ia + (ib - ia) * clamp((t - a) / max(1e-3, b - a))))
    return pts[-1][1]


R_RULES_END = 5
R_0506 = 24


# ---------------------------------------------------------------- 5 rules (+ the round grid starts underneath)
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, x, tt) in enumerate((("ALL-IN", "100% ON DAY ONE", PCOL, 290, T["rule"] - 0.05),
                                                 ("DRIPPER", "1/12 EVERY MONTH", HCOL, 790, T["rule"] + 0.45))):
        p = back(prog(t, tt, 0.4))
        if p <= 0:
            continue
        ctx.save(); ctx.translate(x, 440); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(p, 1e-3), max(p, 1e-3))
        card(ctx, -230, -95, 460, 190, col, 1, 22, border=C["ink"])
        if k == 0:
            gcoin(ctx, -160, 0, 48, t * 0.3, 1)
        else:
            for q in range(3):
                gcoin(ctx, -190 + q * 34, -30 + q * 30, 20, t * 0.3, 1, q)
        text(ctx, title, 50, -8, fit(ctx, title, 80, 290), C["ink"], 1, HEAD, True, "center")
        text(ctx, l1, 50, 56, fit(ctx, l1, 38, 290), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    rc = ease(prog(t, s0 + 0.1, 0.4))
    if rc > 0:
        n = fill_n(t, [(T["one_r"] - 0.1, 0), (T["one_r"] + 0.05, 1), (s1, R_RULES_END)])
        ctx.save(); ctx.translate(0, (1 - rc) * 200)
        round_grid(ctx, t, n, header=clamp((t - T["every1"]) / 0.3))
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_r0506(ctx, t, s0, s1):
    bg_fill(ctx, (0x0B, 0x4A, 0x3A), (0x03, 0x14, 0x10))
    god_rays(ctx, W / 2, 700, t, 0.07, PCOL, 14, 1400)
    n = fill_n(t, [(s0, R_RULES_END), (T["round3"] + 0.5, R_0506)])
    round_grid(ctx, t, n)
    tag(ctx, 540, 440, "2005 - 2006", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03)
    if t < T["money"] - 0.25:
        tag(ctx, 540, 524, "ALL-IN: ROUND AFTER ROUND", PCOL, back(prog(t, T["takes"] - 0.15, 0.3)), 38, 0.02)
    else:
        tag(ctx, 540, 524, "ITS MONEY WORKS LONGER", GOLD, back(prog(t, T["money"] - 0.25, 0.3)), 40, 0.02)
    bunting(ctx, "ROUND 1-24", t, s0, [PCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "race", lambda e: "smug" if e != "talk" else e, prop=prop_flag)


def s_crash(ctx, t, s0, s1):
    rain_bg(ctx, t)
    n = fill_n(t, [(s0, R_0506), (T["row"] + 0.3, ri(STREAK_B) + 1)])
    round_grid(ctx, t, n, streak=clamp((t - T["nineteen"]) / 0.3))
    tag(ctx, 540, 440, "THEN THE CRASH", C["red"], back(prog(t, T["crash"] - 0.3, 0.3)), 46, -0.03, C["white"])
    if t < T["buying"] - 0.15:
        tag(ctx, 540, 524, f"DRIPPER: {STREAK_N} ROUNDS IN A ROW", HCOL, back(prog(t, T["nineteen"] - 0.1, 0.3)), 38, 0.02)
    else:
        tag(ctx, 540, 524, "BUYING CHEAPER EVERY MONTH", HCOL, back(prog(t, T["buying"] - 0.15, 0.3)), 36, 0.02)
    bunting(ctx, "THE CRASH", t, s0, [C["red"], C["ink"], HCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("shock" if t > T["nineteen"] else "sad") if e != "talk" else e)


def s_after(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x6F, 0xC8), (0x0B, 0x2A, 0x5E))
    sun(ctx, 965, 345, 40, t)
    for k in range(4):
        cloud(ctx, ((t - s0) * 40 + k * 330) % (W + 300) - 200, 250 + (k % 2) * 110 + k * 20, 0.9, a=0.5)
    n = fill_n(t, [(s0, ri(STREAK_B) + 1), (s1 - 0.25, ri("2010-12") + 1)])
    round_grid(ctx, t, n)
    tag(ctx, 540, 440, "AFTER THAT...", C["cream"], back(prog(t, s0 + 0.05, 0.3)), 44, -0.03)
    tag(ctx, 540, 524, "ALL-IN RUNS AWAY AGAIN", PCOL, back(prog(t, T["allin2"] - 0.15, 0.3)), 40, 0.02)
    bunting(ctx, "2009 - 2010", t, s0, [PCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "smug" if e != "talk" else e)


# ---------------------------------------------------------------- 9 remember: June 2008, a year later $6,872 vs $9,654
def one_round_chart(ctx, t, k):
    bx, by, bw, bh = 130, 560, 820, 400
    card(ctx, bx - 30, by - 30, bw + 60, bh + 90, (0x0C, 0x10, 0x1C), 0.94, 18, border=C["grey"])
    vmin, vmax = 4500.0, 10800.0
    yy = lambda v: by + bh - (v - vmin) / (vmax - vmin) * bh
    for j in range(21):
        rect(ctx, bx + j * 40, yy(10000) - 2, 22, 4, C["white"], 0.55)
    text(ctx, "$10,000", bx + 6, yy(10000) - 12, 24, C["white"], 0.8, MONO, True, "left")
    text(ctx, f"{MONTHS[W_M - 1]} {W_Y}", bx, by + bh + 42, 24, C["white"], 0.8, MONO, True, "left")
    text(ctx, f"{MONTHS[W_M - 1]} {W_Y + 1}", bx + bw, by + bh + 42, 24, C["white"], 0.8, MONO, True, "right")
    n = len(PL); up = max(2, int(k * (n - 1)) + 1)
    ends = []
    for arr, col in ((PD_, HCOL), (PL, PCOL)):
        xs = [bx + i / (n - 1) * bw for i in range(0, up, 2)]; ys = [yy(arr[i]) for i in range(0, up, 2)]
        poly(ctx, xs, ys, col, 8, 1, glow=True); ends.append((xs[-1], ys[-1]))
    mini_rocco(ctx, ends[0][0], ends[0][1] - 4, 4, "tophat", t, "smug", False, k < 1)
    mini_rocco(ctx, ends[1][0], ends[1][1] - 4, 4, "race", t, "sad", False, k < 1)


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x3A), (0x04, 0x05, 0x14))
    god_rays(ctx, W / 2, 700, t, 0.07, GOLD, 14, 1400)
    if t < T["June"] - 0.1:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT ONE START MONTH?", W / 2, 670, 104, C["white"], r, 980, 0, 12)
        ctx.save(); ctx.translate(540, 950); ctx.scale(0.72, 0.72); month_file(ctx, 0, 0, t, 1); ctx.restore()
    else:
        p = back(prog(t, T["June"] - 0.1, 0.35))
        s_ = "START: JUNE 2008"
        assert (W_Y, W_M) == (2008, 6)
        if t < T["later"] - 0.5:
            pulse = 1 + 0.03 * math.sin(t * 7)
            big_title(ctx, "JUNE 2008", W / 2, 640, 230, C["red"], p * pulse, 960, -0.03, 20)
            tag(ctx, 540, 800, "THE WORST MONTH TO GO ALL IN", C["cream"], back(prog(t, T["eight"] - 0.1, 0.3)), 42, 0.02)
            gcoin(ctx, 540, 990, 60 * max(p, 0.01), t, 1)
        else:
            tag(ctx, 540, 440, s_, C["red"], 1, 50, -0.02, C["white"])
            k = clamp((t - (T["later"] - 0.4)) / max(0.5, T["left"] - (T["later"] - 0.4)))
            one_round_chart(ctx, t, k)
            a = back(prog(t, T["sixtynine"] - 0.05, 0.35)); b = back(prog(t, T["ninetysix"] - 0.05, 0.35))
            tag(ctx, 300, 1100, f"ALL-IN: {money(W_L)}", PCOL, a, 44, -0.02)
            tag(ctx, 790, 1100, f"DRIPPER: {money(W_D)}", HCOL, b, 42, 0.02)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], C["blue"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("shock" if t > T["sixtynine"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 10 final score
def round_counter(ctx, x, y, w, h, label, value, col, t_rev, t):
    card(ctx, x, y, w, h, C["dark"], 1, 16)
    text(ctx, label, x + 30, y + 46, 30, C["grey"], 1, MONO, True, "left")
    if t >= t_rev:
        p = back(prog(t, t_rev, 0.35))
        text(ctx, value, x + w / 2 - 70, y + h - 36, fit(ctx, value, 118, w - 240, MONO) * max(p, 0.01), col, 1, MONO, True, "center")
        tear = ease(prog(t, t_rev, 0.4))
        if tear < 1:
            ctx.save(); ctx.translate(x + w / 2 + tear * 700, y + h / 2 + 20 - tear * 260); ctx.rotate(tear * 1.2)
            rect(ctx, -w / 2 + 30, -60, w - 60, 120, (0x05, 0x05, 0x05)); ctx.restore()
    else:
        rect(ctx, x + 30, y + 70, w - 60, h - 95, (0x05, 0x05, 0x05))
        text(ctx, "??? ROUNDS", x + w / 2, y + h - 48, 70, (0x55, 0x5B, 0x60), 1, MONO, True, "center")


def lead_card(ctx, t):
    if t >= T["Average"] - 0.1:
        a = back(prog(t, T["Average"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -46, 900, 92, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=PCOL)
        s_ = "AVG LEAD AFTER 1 YEAR:"
        text(ctx, s_, -420, 14, 34, C["white"], 1, MONO, True, "left")
        if t >= T["rev3"]:
            q = back(prog(t, T["rev3"], 0.3))
            text(ctx, "+" + money(AVG_GAP), 400, 20, 58 * max(q, 0.01), PCOL, 1, MONO, True, "right")
        else:
            text(ctx, "+$???", 400, 16, 44, (0x70, 0x76, 0x7B), 1, MONO, True, "right")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, f"{NR} ROUNDS · START MONTHS 2005-2023", W / 2, 420, 34, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    round_counter(ctx, 90, 450, 900, 210, "A · ALL-IN: ROUNDS WON", f"{L_WINS} ROUNDS", PCOL, T["rev1"], t)
    round_counter(ctx, 90, 680, 900, 210, "B · THE DRIPPER: ROUNDS WON", f"{D_WINS} ROUNDS", HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 880, 505, T["rev2"] + 0.25, t, STAMP_GR, 190, 38, 0.1)
    lead_card(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.4, T["Its2"] - 0.15, "right", y=1085)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev1"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 11 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x02, 0x04, 0x0C), 0.82)
    stamp_box(ctx, ["DRIPPING ISN'T", "A BETTER RETURN."], W / 2, 495, T["isnt"] - 0.3, t, STAMP_OR, 880, 80, -0.05)
    stamp_box(ctx, ["IT'S INSURANCE."], W / 2 + 10, 765, T["Its2"] - 0.05, t, STAMP_BL, 760, 92, 0.04)
    stamp_box(ctx, ["...AND YOU PAY FOR IT."], W / 2 - 10, 940, T["pay"] - 0.35, t, (0xC0, 0x20, 0x40), 700, 54, -0.03)
    sticker(ctx, t, T["rev2"] + 0.4, T["Its2"] - 0.15, "right", y=1085)
    fb = back(prog(t, T["pay"] + 0.05, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1090); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #16", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "choice": s_choice, "guess": s_guess, "hidden": s_hidden, "rules": s_rules, "r0506": s_r0506,
            "crash": s_crash, "after": s_after, "remember": s_remember, "score": s_score, "verdict": s_verdict, "loop": s_loop}
