# ================================================================ helpers copied from ep08


MOONC = (0xE8, 0xE4, 0xFF)


NAVY, NAVY2 = (0x1A, 0x1F, 0x4A), (0x08, 0x0B, 0x22)


def fit(ctx, s, size, maxw, f=HEAD):
    while tw(ctx, s, size, f) > maxw and size > 10:
        size -= 2
    return size


def xmark(ctx, x, y, s, col, w=9):
    ctx.new_path(); ctx.move_to(x - s, y - s); ctx.line_to(x + s, y + s); ctx.move_to(x + s, y - s); ctx.line_to(x - s, y + s)
    ctx.set_source_rgba(*rgba(col)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def stamp_box(ctx, lines, x, y, t0, t, col, w=820, size=78, rot=-0.1):
    sk = prog(t, t0, 0.3)
    if sk <= 0:
        return
    sc = 2.2 - 1.2 * ease(sk); a = clamp(sk * 2)
    h = 70 + len(lines) * size * 1.1
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    rrect(ctx, -w / 2, -h / 2, w, h, 14); ctx.set_source_rgba(*rgba(C["cream"], 0.95 * a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(col, a)); ctx.set_line_width(10); ctx.stroke()
    for k, ln in enumerate(lines):
        sz = fit(ctx, ln, size, w - 60)
        text(ctx, ln, 0, -h / 2 + 35 + size * 0.9 + k * size * 1.1, sz, col, a, HEAD, True, "center")
    ctx.restore()


def sun(ctx, cx, cy, r, t, a=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(t * 0.6)
    for k in range(12):
        ctx.save(); ctx.rotate(k * math.pi / 6)
        rect(ctx, r + 12, -9, 34 + 10 * math.sin(t * 4 + k), 18, C["yellow"], a)
        ctx.restore()
    ctx.restore()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba((0xFF, 0xD2, 0x4A), a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()


def moon(ctx, cx, cy, r, a=1.0, glow=True):
    if glow:
        g = cairo.RadialGradient(cx, cy, r * 0.6, cx, cy, r * 2.4)
        g.add_color_stop_rgba(0, 0.9, 0.9, 1, 0.35 * a); g.add_color_stop_rgba(1, 0.9, 0.9, 1, 0)
        ctx.set_source(g); ctx.new_path(); ctx.arc(cx, cy, r * 2.4, 0, 2 * math.pi); ctx.fill()
    ctx.push_group()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(MOONC, 1)); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR); ctx.new_path(); ctx.arc(cx + r * 0.45, cy - r * 0.25, r * 0.85, 0, 2 * math.pi); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


def stars(ctx, t, n=40, y0=0, y1=H, seed=1, a=1.0):
    rr = random.Random(seed)
    for k in range(n):
        x = rr.random() * W; y = y0 + rr.random() * (y1 - y0); s = 3 + rr.random() * 5
        tw_ = 0.35 + 0.65 * abs(math.sin(t * (1 + rr.random() * 2) + k))
        rect(ctx, x, y, s, s, C["white"], tw_ * a)


def cloud(ctx, x, y, s, col=(0xFF, 0xFF, 0xFF), a=0.92):
    for dx, dy, r in ((0, 0, 40), (40, -14, 48), (86, 0, 38)):
        ctx.new_path(); ctx.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(col, a)); ctx.fill()


def mini_rocco(ctx, x, y, px, costume, t, expr="neutral", flip=False, run=True):
    bob = abs(math.sin(t * 12)) * px * 2 if run else abs(math.sin(t * 3)) * px
    ctx.save(); ctx.translate(x, y - bob)
    if flip:
        ctx.scale(-1, 1)
    ctx.rotate(math.sin(t * 12) * 0.06 if run else 0)
    ctx.translate(-RCOLS * px / 2, -RROWS * px)
    draw_rocco(ctx, 0, 0, px, expr, costume)
    ctx.restore()


def redacted_counter(ctx, x, y, w, h, label, value, col, t_rev, t, icon=None):
    card(ctx, x, y, w, h, C["dark"], 1, 16)
    text(ctx, label, x + 30, y + 46, 30, C["grey"], 1, MONO, True, "left")
    if icon == "sun":
        sun(ctx, x + w - 60, y + 45, 22, t)
    elif icon == "moon":
        moon(ctx, x + w - 60, y + 45, 26, glow=False)
    if t >= t_rev:
        p = back(prog(t, t_rev, 0.35))
        sz = fit(ctx, value, 110, w - 80, MONO) * max(p, 0.01)
        text(ctx, value, x + w / 2, y + h - 40, sz, col, 1, MONO, True, "center")
        tear = ease(prog(t, t_rev, 0.4))
        if tear < 1:
            ctx.save(); ctx.translate(x + w / 2 + tear * 700, y + h / 2 + 20 - tear * 260); ctx.rotate(tear * 1.2)
            rect(ctx, -w / 2 + 30, -60, w - 60, 120, (0x05, 0x05, 0x05)); ctx.restore()
    else:
        rect(ctx, x + 30, y + 70, w - 60, h - 95, (0x05, 0x05, 0x05))
        text(ctx, "$??,???", x + w / 2, y + h - 48, 76, (0x55, 0x5B, 0x60), 1, MONO, True, "center")


