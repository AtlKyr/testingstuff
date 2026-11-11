# ================================================================ Autopsy #16 scenes (sell when the Fed hikes?)
HCOL = (0x4F, 0xC3, 0xF7)    # BUY & HOLD
PCOL = (0xFF, 0x6B, 0x3D)    # HIKE SELLER
GOLD = (0xFF, 0xD2, 0x4A)
REDC = (0xF0, 0x3E, 0x5A)
GRNC = (0x22, 0xE5, 0x8B)
BG0, BG1 = (0x3A, 0x0E, 0x10), (0x0C, 0x02, 0x04)
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
    a = ease(prog(t, SC["news"], 0.4))
    if a <= 0:
        return
    rv = t >= T["rev2"]
    tag(ctx, 160, 66, "CASE #16", C["cream"], a, 26, -0.03)
    text(ctx, "WINNER:", 640, 76, 26, C["white"], a, MONO, True, "right", outline=6, ocol=C["ink"])
    if not rv:
        card(ctx, 655, 38, 300, 54, (0x05, 0x05, 0x05), a, 8, shadow=False, border=C["grey"])
        text(ctx, "$??,???", 805, 78, 36, C["grey"], a, MONO, True, "center")
    else:
        p = back(prog(t, T["rev2"], 0.35))
        card(ctx, 655, 38, 300, 54, HCOL, a, 8, shadow=False)
        text(ctx, money(BH_V), 805, 78, fit(ctx, money(BH_V), 36, 280, MONO) * max(p, 0.01), C["ink"], a, MONO, True, "center")
    k = clamp((t - SC["news"]) / (T["exit"] - SC["news"]))
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





def race_chart(ctx, t, up, zones=(), marks=False, curtain=None):
    card(ctx, RBOX[0] - 30, RBOX[1] - 30, RBOX[2] + 60, RBOX[3] + 150, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    for d0, d1, col, a in zones:
        x0 = sx_of(di(d0), 0, N - 1, RBOX); x1 = sx_of(di(d1), 0, N - 1, RBOX)
        rect(ctx, x0, RBOX[1], max(6, x1 - x0), RBOX[3], col, a)
    for k in range(1, 5):
        rect(ctx, RBOX[0], RBOX[1] + k * RBOX[3] / 5, RBOX[2], 2, C["white"], 0.08)
    for yr in (2005, 2008, 2012, 2016, 2020, 2024):
        text(ctx, str(yr), sx_of(di(f"{yr}-01-01"), 0, N - 1, RBOX), RBOX[1] + RBOX[3] + 50, 26, C["white"], 0.75, MONO, True, "center")
    if marks:                                  # every Fed hike = one red tick on the floor; seller's cash time = grey band
        j0 = None
        for i in range(0, up + 1, 3):
            if INM[i] == 0 and j0 is None: j0 = i
            if (INM[i] == 1 or i + 3 > up) and j0 is not None:
                x0 = sx_of(j0, 0, N - 1, RBOX); x1 = sx_of(i, 0, N - 1, RBOX)
                rect(ctx, x0, RBOX[1] + RBOX[3] - 14, max(3, x1 - x0), 14, PCOL, 0.55); j0 = None
        for i in HIKE_I:
            if i > up:
                break
            rect(ctx, sx_of(i, 0, N - 1, RBOX) - 2, RBOX[1] + RBOX[3] - 52, 4, 36, C["red"], 0.95)
    vmax = max(14000.0, 1.2 * float(max(np.nanmax(SV[:up + 1]), np.nanmax(JV[:up + 1]))))
    if curtain is not None:
        vmax = 1.25 * float(max(np.nanmax(SV[:curtain + 1]), np.nanmax(JV[:curtain + 1]))); up = min(up, curtain)
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
    if curtain is not None:
        xc = sx_of(curtain, 0, N - 1, RBOX) + 14
        curtain_box(ctx, t, xc, RBOX[1] - 10, RBOX[0] + RBOX[2] + 10, RBOX[3] + 20, "CLASSIFIED")
    for k, (lab, col) in enumerate((("HIKE SELLER", PCOL), ("BUY & HOLD", HCOL))):
        rect(ctx, RBOX[0] + 150 + k * 360, RBOX[1] + RBOX[3] + 87, 36, 10, col)
        text(ctx, lab, RBOX[0] + 196 + k * 360, RBOX[1] + RBOX[3] + 101, 26, col, 1, MONO, True, "left")




# ---------------------------------------------------------------- props for #16
def pct_badge(ctx, x, y, s, t, col=None, a=1.0):
    """a round '%' token with an up arrow (a rate hike)"""
    col = col or C["red"]
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.sin(t * 2 + x) * 0.12); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 70, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(8); ctx.stroke()
    text(ctx, "%", 0, 34, 96, C["white"], a, HEAD, True, "center")
    ctx.restore()


def bank_building(ctx, cx, base, s, t, a=1.0):
    """generic columned bank building (not any real logo)"""
    ctx.save(); ctx.translate(cx, base); ctx.scale(s, s)
    stone = (0xE9, 0xE2, 0xD0)
    ctx.new_path(); ctx.move_to(-260, -330); ctx.line_to(0, -450); ctx.line_to(260, -330); ctx.close_path()
    ctx.set_source_rgba(*rgba(stone, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(8); ctx.stroke()
    rect(ctx, -270, -335, 540, 40, stone, a); rect(ctx, -290, -30, 580, 30, stone, a); rect(ctx, -310, 0, 620, 26, stone, a)
    for k in range(6):
        x = -225 + k * 90
        rect(ctx, x - 22, -295, 44, 265, stone, a)
        for j in range(3):
            rect(ctx, x - 14 + j * 12, -290, 4, 255, (0xC9, 0xC0, 0xA8), a)
    text(ctx, "RATES", 0, -368, 40, C["ink"], a, HEAD, True, "center")
    ctx.restore()


def cpi_card(ctx, x, y, t, p, rot=-0.04):
    if p <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + 0.015 * math.sin(t * 3)); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -230, -160, 460, 320, C["white"], 1, 26, border=C["ink"])
    rect(ctx, -230, -160, 460, 86, C["red"])
    text(ctx, "INFLATION · NOV 10", 0, -101, 38, C["white"], 1, HEAD, True, "center")
    text(ctx, "HOTTER", 0, 10, 92, STAMP_OR, 1, HEAD, True, "center")
    text(ctx, "THAN EXPECTED", 0, 90, 46, C["ink"], 1, HEAD, True, "center")
    ctx.restore()


def calendar_dec(ctx, x, y, t, p):
    if p <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(0.05 + 0.02 * math.sin(t * 2.5)); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -150, -150, 300, 300, C["white"], 1, 22, border=C["ink"])
    rect(ctx, -150, -150, 300, 80, C["red"])
    text(ctx, "DEC", 0, -92, 54, C["white"], 1, HEAD, True, "center")
    text(ctx, "HIKE?", 0, 70, 96, C["ink"], 1, HEAD, True, "center")
    ctx.restore()


# ---------------------------------------------------------------- 1 hook (frame 0: FED HIKES / SELL?)
def hook_draw(ctx, t, tl, show_tag=True):
    bg_fill(ctx, BG0, BG1)
    god_rays(ctx, W / 2, 620, t, 0.09, C["red"], 14, 1400)
    for k in range(12):                      # rising % tokens
        u = (t * 0.22 + k / 12) % 1
        pct_badge(ctx, (k * 197 + 60) % (W - 60), 1500 - u * 1700, 0.35 + 0.12 * (k % 3), t, C["red"], 0.2)
    p = back(prog(tl, -0.35, 0.3)); sc = 1.0 + 0.1 * (1 - ease(prog(tl, -0.05, 0.3)))
    wob = 1 + 0.03 * math.sin(t * 6)
    s_ = max(p * sc * wob, 1e-3)
    shake = math.sin(t * 40) * 6 * (1 - prog(tl, 0, 0.5))
    ctx.save(); ctx.translate(540 + shake, 500); ctx.rotate(-0.04); ctx.scale(s_, s_)
    text(ctx, "FED HIKES.", 0, 0, fit(ctx, "FED HIKES.", 240, 960), C["white"], 1, HEAD, True, "center", outline=24, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(0.03); ctx.scale(s_ * 1.04, s_ * 1.04)
    text(ctx, "SELL?", 0, 0, fit(ctx, "SELL?", 280, 900), C["red"], 1, HEAD, True, "center", outline=26, ocol=C["ink"])
    ctx.restore()
    ctx.save(); ctx.translate(0, 0)
    bank_building(ctx, 330, 1180, 0.62 * max(p, 1e-3), t)
    ctx.restore()
    arrow_up(ctx, 330, 860 + math.sin(t * 7) * 10 - 40, 0.42 * max(p, 1e-3), C["red"])
    if show_tag:
        tag(ctx, 540, 180, "INFLATION CAME IN HOT", C["cream"], p, 46, -0.04)


def s_hook(ctx, t, s0, s1):
    hook_draw(ctx, t, t)
    rocco(ctx, t, "detective", lambda e: "shock" if e != "talk" else e, prop=prop_magnifier)


def s_loop(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.03 + (t - s0) * 0.05)
    rocco(ctx, t, "detective", lambda e: "shock", prop=prop_magnifier)


# ---------------------------------------------------------------- 2 the news
def s_news(ctx, t, s0, s1):
    bg_fill(ctx, (0x5C, 0x12, 0x1A), (0x1A, 0x04, 0x08))
    ticker_band(ctx, 1010, t, "  OCT CPI HOTTER THAN EXPECTED  ·  FED OFFICIALS EYE A DECEMBER HIKE  ·  NASDAQ -0.7%  ·", C["ink"], C["cream"], 260)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "BREAKING", W / 2, 470, 150, C["white"], p, 900, -0.03, 16)
    cpi_card(ctx, 300, 780, t, back(prog(t, s0 + 0.12, 0.4)))
    calendar_dec(ctx, 790, 780, t, back(prog(t, T["December"] - 0.3, 0.35)))
    pct_badge(ctx, 790, 560, 0.8 * back(prog(t, T["raise_"] - 0.15, 0.3)) + 1e-3, t)
    bunting(ctx, "THE NEWS", t, s0, [C["red"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "party", lambda e: "shock" if e != "talk" else e)


# ---------------------------------------------------------------- 3 the question
def s_question(ctx, t, s0, s1):
    bg_fill(ctx, (0x3A, 0x1E, 0x06), (0x12, 0x08, 0x02))
    speed_lines(ctx, t)
    p = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "DO YOU", W / 2, 440, 96, C["white"], p, 900, -0.02, 12)
    q = back(prog(t, T["sell1"] - 0.12, 0.3))
    big_title(ctx, "SELL", W / 2, 690, 260, PCOL, q, 960, -0.03, 22)
    r = back(prog(t, T["Fed1"] - 0.25 if False else T["hikes1"] - 0.4, 0.3))
    big_title(ctx, "WHEN THE FED HIKES?", W / 2, 870, 110, GOLD, r, 980, 0.02, 14)
    for k in range(5):
        pct_badge(ctx, 140 + k * 200, 1060 - abs(math.sin(t * 4 + k)) * 60, 0.55, t, C["red"], 0.9 * r)
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
    for k in range(14):
        u = ((t - s0) * 0.45 + k / 14) % 1
        pct_badge(ctx, (k * 211) % W, 1300 - u * 1150, 0.35, t, C["red"], 0.22 * (1 - u))
    hp = back(prog(t, s0 + 0.03, 0.3))
    big_title(ctx, "THE FED RAISES RATES...", W / 2, 420, 84, C["white"], hp, 980, 0, 12)
    blink = int(t * 4) % 2
    for k, (lab, sub1, sub2, col, x, tt) in enumerate((("A", "SELL", "AND WAIT", PCOL, -225, T["A"]),
                                                        ("B", "JUST", "HOLD", HCOL, 225, T["B"]))):
        if t < tt - 0.15:
            continue
        pk = back(prog(t, tt - 0.15, 0.35))
        on = (blink == k) and t > T["hold1"]
        hl = 1 + 0.1 * math.sin(math.pi * prog(t, tt - 0.05, 0.4))
        ctx.save(); ctx.translate(W / 2 + x, 760); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(pk * hl, 1e-3), max(pk * hl, 1e-3))
        card(ctx, -205, -230, 410, 400, col, 1, 22, border=C["white"] if on else C["ink"])
        text(ctx, lab, 0, -40, 200, C["ink"], 1, HEAD, True, "center")
        if k == 0:
            arrow_down(ctx, 0, 30, 0.35, C["white"])
        else:
            hold_icon(ctx, 0, 30, 0.42, C["white"])
        text(ctx, sub1, 0, 115, fit(ctx, sub1, 50, 380), C["ink"], 1, HEAD, True, "center")
        text(ctx, sub2, 0, 160, fit(ctx, sub2, 44, 380), C["ink"], 1, HEAD, True, "center")
        ctx.restore()
    sticker(ctx, t, T["hold1"] - 0.2, T["hold1"] + 2.3, "guess", y=1080)
    bunting(ctx, "YOUR GUESS", t, s0, [GOLD, C["ink"], C["purple"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "crown", lambda e: "shock" if (e != "talk" and t > T["B"]) else e)


# ---------------------------------------------------------------- 5 hidden: one hiking cycle
def cycle_file(ctx, cx, cy, t, a, label="ONE HIKING CYCLE", inner="20??"):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.04)
    card(ctx, -330, -150, 660, 300, (0xC8, 0x9B, 0x5A), a, 18, border=C["ink"])
    card(ctx, -330, -190, 240, 60, (0xC8, 0x9B, 0x5A), a, 12, shadow=False, border=C["ink"])
    text(ctx, "EVIDENCE", -210, -148, 30, C["ink"], a, TAGF, False, "center")
    text(ctx, label, 0, -60, fit(ctx, label, 76, 600), C["ink"], a, HEAD, True, "center")
    rect(ctx, -270, 0, 540, 110, (0x05, 0x05, 0x05), a)
    text(ctx, inner, 0, 78, 64, (0x70, 0x76, 0x7B), a, MONO, True, "center")
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
        ctx.save(); ctx.translate(540, 730); ctx.scale(max(q, 1e-3), max(q, 1e-3)); cycle_file(ctx, 0, 0, t, 1); ctx.restore()
    sticker(ctx, t, T["hold1"] - 0.2, T["hold1"] + 2.3, "guess", y=1080)
    bunting(ctx, "THE CLUE", t, s0, [C["blue"], C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: "smug" if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 6 rules (+ the race starts underneath)
def s_rules(ctx, t, s0, s1):
    grid_bg(ctx, (0x14, 0x2B, 0x3A), (0x0B, 0x16, 0x1F))
    for k, (title, l1, col, fg, x, tt, hw) in enumerate((("SELL", "DAY AFTER A HIKE", PCOL, C["ink"], 290, T["sell3"], T["hike1"]),
                                                         ("BUY BACK", "6 QUIET MONTHS", GRNC, C["ink"], 790, T["buy"], T["months"]))):
        p = back(prog(t, tt - 0.12, 0.4))
        if p <= 0:
            continue
        hl = 1 + 0.08 * math.sin(math.pi * prog(t, hw - 0.05, 0.4))
        ctx.save(); ctx.translate(x, 470); ctx.rotate(-0.03 if k == 0 else 0.03); ctx.scale(max(p * hl, 1e-3), max(p * hl, 1e-3))
        card(ctx, -230, -110, 460, 220, col, 1, 22, border=C["ink"])
        if k == 0:
            arrow_down(ctx, -160, 0, 0.42, C["white"])
        else:
            hourglass(ctx, -160, 0, 0.5, t)
        text(ctx, title, 40, -10, fit(ctx, title, 84, 300), fg, 1, HEAD, True, "center")
        text(ctx, l1, 40, 60, fit(ctx, l1, 40, 300), fg, 1, HEAD, True, "center")
        ctx.restore()
    rc = ease(prog(t, s0 + 0.05, 0.4))
    if rc > 0:
        up = race_idx(t, [(s0 + 0.3, 1), (s1, di("2005-02-01"))])
        ctx.save(); ctx.translate(0, (1 - rc) * 200)
        race_chart(ctx, t, up, marks=True)
        ctx.restore()
    bunting(ctx, "THE RULE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "lab", lambda e: "smug" if e != "talk" else e)


def s_race05(ctx, t, s0, s1):
    bg_fill(ctx, (0x1E, 0x6F, 0xC8), (0x0B, 0x2A, 0x5E))
    sun(ctx, 965, 345, 40, t)
    for k in range(4):
        cloud(ctx, ((t - s0) * 40 + k * 330) % (W + 300) - 200, 250 + (k % 2) * 110 + k * 20, 0.9, a=0.5)
    pts = [(s0 + 0.1, di("2005-02-01")), (T["climbing"] + 0.6, di("2007-06-29")), (s1, di("2007-06-29"))]
    race_chart(ctx, t, race_idx(t, pts), [("2005-02-03", "2006-12-29", PCOL, 0.14)], marks=True)
    tag(ctx, 540, 440, "2005: HIKE AFTER HIKE", C["red"], back(prog(t, T["Hike"] - 0.15, 0.3)), 44, -0.03, C["white"])
    if t < T["stocks1"] - 0.25:
        tag(ctx, 540, 524, "THE SELLER SITS OUT", PCOL, back(prog(t, T["seller1"] - 0.15, 0.3)), 38, 0.02)
    else:
        tag(ctx, 540, 524, "STOCKS KEEP CLIMBING", HCOL, back(prog(t, T["stocks1"] - 0.25, 0.3)), 40, 0.02)
    bunting(ctx, "2005", t, s0, [HCOL, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "night", lambda e: ("sleep" if t < T["stocks1"] else "shock") if e != "talk" else e)


def s_race08(ctx, t, s0, s1):
    rain_bg(ctx, t)
    pts = [(s0 + 0.1, di("2007-06-29")), (T["Hes"], di("2007-12-31")), (T["crash"] + 0.4, di("2009-03-09")), (s1, di("2009-03-09"))]
    up = race_idx(t, pts)
    race_chart(ctx, t, up, [("2008-01-01", "2009-03-09", C["red"], 0.22)], marks=True,
               curtain=di("2009-03-09") if t > T["crash"] + 0.45 else None)
    tag(ctx, 540, 440, "2007: HE'S BACK IN", PCOL, back(prog(t, T["Hes"] - 0.15, 0.3)), 44, -0.03)
    tag(ctx, 540, 524, "...JUST IN TIME FOR THE CRASH", C["red"], back(prog(t, T["time"] - 0.15, 0.3)), 36, 0.02, C["white"])
    bunting(ctx, "2008", t, s0, [C["red"], C["ink"], PCOL, C["grey"]])
    hud(ctx, t)
    rocco(ctx, t, "fire", lambda e: ("shock" if t > T["crash"] else "smug") if e != "talk" else e)


# ---------------------------------------------------------------- 9 strange: 29 of 32 hikes -> higher a year later
def s_strange(ctx, t, s0, s1):
    bg_fill(ctx, (0x06, 0x3A, 0x2A), (0x02, 0x0C, 0x09))
    for k in range(10):
        u = ((t - s0) * 0.3 + k / 10) % 1
        arrow_up(ctx, (k * 197 + 60) % (W - 60), 1400 - u * 1300, 0.25, GRNC, 0.15)
    if t < T["twentynine"] - 0.15:
        p = back(prog(t, s0 + 0.03, 0.3))
        big_title(ctx, "NOW THE STRANGE PART", W / 2, 430, 96, GOLD, p, 980, -0.02, 12)
    else:
        text(ctx, "EVERY FED HIKE · 2005-2023", W / 2, 430, 50, C["white"], 1, MONO, True, "center", outline=7, ocol=C["ink"])
    cols, sp = 8, 112
    x0 = (W - cols * sp) / 2 + sp / 2; y0 = 530
    kk = prog(t, T["thirtytwo"], max(0.5, T["later"] - T["thirtytwo"]))
    shown = int(NH * ease_io(kk))
    for j in range(NH):
        ap = clamp((t - s0 - 0.1 - j * 0.02) / 0.2)
        if ap <= 0:
            continue
        cx = x0 + (j % cols) * sp; cy = y0 + (j // cols) * 100
        val = FWD[j][1]
        col = (GRNC if val > 0 else REDC) if j < shown else (0x7A, 0x80, 0x88)
        s = 40 * ap * (1 + (0.18 * math.sin(t * 9 + j) if (j < shown and j >= shown - 3) else 0))
        ctx.new_path(); ctx.arc(cx, cy, s, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, 1)); ctx.fill_preserve()
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(5); ctx.stroke()
        if j < shown:
            if val > 0:
                arrow_up(ctx, cx, cy + 4, 0.18, C["white"])
            else:
                arrow_down(ctx, cx, cy - 4, 0.18, C["white"])
        else:
            text(ctx, "%", cx, cy + 16, 40, C["white"], 0.8 * ap, HEAD, True, "center")
    q = back(prog(t, T["twentynine"] - 0.1, 0.35))
    big_title(ctx, f"{UP} OF {NH}", W / 2, 1010, 150, GOLD, q, 900, -0.02, 16)
    r = back(prog(t, T["higher1"] - 0.15, 0.3))
    tag(ctx, 540, 1095, "HIGHER ONE YEAR LATER", GRNC, r, 44, 0.015)
    bunting(ctx, "STRANGE", t, s0, [GRNC, C["ink"], GOLD, C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "grad", lambda e: ("shock" if t > T["twentynine"] else "neutral") if e != "talk" else e)


# ---------------------------------------------------------------- 10 remember: 2022, fastest in four decades
def cyc_chart(ctx, t, k):
    bx, by, bw, bh = 120, 600, 840, 360
    card(ctx, bx - 20, by - 20, bw + 40, bh + 40, (0x0C, 0x10, 0x1C), 0.92, 18, border=C["grey"])
    i0, i1 = HIKE_I[21], HIKE_I[31]
    seg = _c["C"].values[i0:i1 + 1]
    lo, hi = seg.min() * 0.97, seg.max() * 1.03
    base = seg[0]
    yb = by + bh - (base - lo) / (hi - lo) * bh
    for j in range(21):
        rect(ctx, bx + j * 40, yb - 2, 22, 4, C["white"], 0.6)
    text(ctx, "FIRST HIKE", bx + 12, yb + 34, 24, C["white"], 0.8, MONO, True, "left")
    n = max(2, int(len(seg) * k))
    xs = [bx + 10 + j / (len(seg) - 1) * (bw - 20) for j in range(n)]
    ys = [by + bh - (v - lo) / (hi - lo) * bh for v in seg[:n]]
    poly(ctx, xs, ys, HCOL, 8, 1, glow=True)
    for hidx in HIKE_I[21:32]:
        j = hidx - i0
        if j < n:
            x = bx + 10 + j / (len(seg) - 1) * (bw - 20)
            rect(ctx, x - 2, by + bh - 34, 4, 34, C["red"], 0.95)
    ctx.new_path(); ctx.arc(xs[-1], ys[-1], 14, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["white"])); ctx.fill()
    text(ctx, "11 HIKES", bx + bw - 20, by + bh - 44, 26, C["red"], 1, MONO, True, "right", outline=5, ocol=C["ink"])


def s_remember(ctx, t, s0, s1):
    bg_fill(ctx, (0x10, 0x14, 0x3A), (0x04, 0x05, 0x14))
    god_rays(ctx, W / 2, 700, t, 0.07, GOLD, 14, 1400)
    if t < T["Twenty"] - 0.1:
        r = back(prog(t, s0 + 0.03, 0.35))
        big_title(ctx, "REMEMBER", W / 2, 520, 170, GOLD, r, 960, 0, 16)
        big_title(ctx, "THAT ONE CYCLE?", W / 2, 670, 110, C["white"], r, 980, 0, 12)
        ctx.save(); ctx.translate(540, 950); ctx.scale(0.72, 0.72); cycle_file(ctx, 0, 0, t, 1); ctx.restore()
    else:
        p = back(prog(t, T["Twenty"] - 0.1, 0.35))
        pulse = 1 + 0.03 * math.sin(t * 7)
        big_title(ctx, "2022", W / 2, 500, 200, GOLD, p * pulse, 960, -0.02, 18)
        tag(ctx, 540, 1085, "FASTEST HIKES IN 4 DECADES", C["red"], back(prog(t, T["fastest"] - 0.15, 0.3)), 40, -0.015, C["white"])
        k = clamp((t - T["By"] + 0.3) / max(0.5, T["higher2"] + 0.2 - T["By"] + 0.3))
        if t > T["fastest"] - 0.1:
            cyc_chart(ctx, t, ease_io(k) if t > T["By"] - 0.3 else 0.02 + 0.1 * prog(t, T["fastest"], 1.0))
        if t > T["higher2"] - 0.05:
            stamp_box(ctx, ["HIGHER THAN", "AT THE FIRST HIKE"], 700, 700, T["higher2"] - 0.05, t, STAMP_GR, 440, 40, 0.05)
    bunting(ctx, "THE CLUE", t, s0, [GOLD, C["ink"], C["blue"], C["cream"]])
    hud(ctx, t)
    rocco(ctx, t, "detective", lambda e: ("shock" if t > T["higher2"] else "smug") if e != "talk" else e, prop=prop_magnifier)


# ---------------------------------------------------------------- 11 final score
def footnote(ctx, t):
    if t >= T["rev3"] - 0.1:
        a = back(prog(t, T["rev3"] - 0.1, 0.35))
        ctx.save(); ctx.translate(540, 962); ctx.scale(max(a, 1e-3), max(a, 1e-3))
        card(ctx, -450, -42, 900, 84, (0x05, 0x05, 0x05), 0.92, 14, shadow=False, border=PCOL)
        s_ = f"OTHER WAITS (1 WEEK - 1 YEAR): {WAIT_N - WAIT_WINS} OF {WAIT_N} LOST"
        text(ctx, s_, 0, 14, fit(ctx, s_, 40, 860, MONO), C["white"], 1, MONO, True, "center")
        ctx.restore()


def s_score(ctx, t, s0, s1):
    stadium(ctx, t)
    text(ctx, "$10,000 EACH · 2005-2024", W / 2, 420, 36, GOLD, 1, MONO, True, "center", outline=6, ocol=C["ink"])
    redacted_counter(ctx, 90, 450, 900, 210, "A · HIKE SELLER (0.05% FEES)", money(SEL_V), PCOL, T["rev1"], t)
    redacted_counter(ctx, 90, 680, 900, 210, "B · BUY & HOLD", money(BH_V), HCOL, T["rev2"], t)
    if t >= T["rev2"]:
        stamp_box(ctx, ["WINNER"], 870, 700, T["rev2"] + 0.25, t, STAMP_GR, 210, 42, 0.1)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["They"] - 0.15, "right", y=1080)
    bunting(ctx, "FINAL SCORE", t, s0)
    hud(ctx, t)
    rocco(ctx, t, "tophat", lambda e: "shock" if (e != "talk" and t > T["rev2"]) else e, prop=prop_coin)


# ---------------------------------------------------------------- 12 verdict + FOLLOW
def s_verdict(ctx, t, s0, s1):
    hook_draw(ctx, t, 0.3, False)
    rect(ctx, 0, 0, W, H, (0x08, 0x02, 0x03), 0.8)
    stamp_box(ctx, ["RATE HIKES", "MAKE HEADLINES."], W / 2, 495, T["Rate"] - 0.05, t, STAMP_OR, 800, 84, -0.05)
    stamp_box(ctx, ["NOT AN EXIT SIGN."], W / 2 + 10, 765, T["They"] - 0.05, t, C["red"], 800, 84, 0.04)
    footnote(ctx, t)
    sticker(ctx, t, T["rev2"] + 0.35, T["They"] - 0.15, "right", y=1080)
    fb = back(prog(t, T["They"] + 0.1, 0.35))
    if fb > 0:
        pulse = 1 + 0.04 * math.sin(t * 8)
        ctx.save(); ctx.translate(W / 2, 1070); ctx.scale(max(fb * pulse, 1e-3), max(fb * pulse, 1e-3))
        card(ctx, -300, -50, 600, 100, C["red"], 1, 50)
        text(ctx, "FOLLOW for case #17", 0, 18, 46, C["white"], 1, HEAD, True, "center")
        ctx.restore()
    bunting(ctx, "VERDICT", t, s0, [C["green"], C["white"], GOLD, C["red"]])
    hud(ctx, t)
    rocco(ctx, t, "doctor", lambda e: "smug" if e != "talk" else e)


SCENE_FN = {"hook": s_hook, "news": s_news, "question": s_question, "guess": s_guess, "hidden": s_hidden, "rules": s_rules,
            "race05": s_race05, "race08": s_race08, "strange": s_strange, "remember": s_remember, "score": s_score,
            "verdict": s_verdict, "loop": s_loop}
