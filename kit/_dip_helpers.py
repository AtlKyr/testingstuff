# ================================================================ Autopsy #3 scenes
def rain_bg(ctx, t, flash_mod=13):
    bg_fill(ctx, (0x2A, 0x1A, 0x2E), (0x10, 0x0A, 0x14))
    if int(t * 10) % flash_mod == 0:
        ctx.set_source_rgba(1, 1, 1, 0.14); ctx.paint()
    for k in range(80):
        x = (k * 97 + t * 260) % (W + 200) - 100
        y = ((k * 211) + t * 1400) % (H + 200) - 100
        ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x - 12, y + 40); ctx.set_source_rgba(0.8, 0.85, 1, 0.22); ctx.set_line_width(3); ctx.stroke()


def grid_bg(ctx, top=(0x14, 0x2B, 0x3A), bot=(0x0B, 0x16, 0x1F)):
    bg_fill(ctx, top, bot)
    for i in range(0, W, 60):
        rect(ctx, i, 0, 2, H, C["blue"], 0.10)
    for j in range(0, H, 60):
        rect(ctx, 0, j, W, 2, C["blue"], 0.10)


def big_card(ctx, label, x, y, p, col, fg=None, size=96, rot=-0.05, w=None):
    if p <= 0:
        return
    w = w or tw(ctx, label, size) + 90
    h = size * 1.45
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(p, 1e-3), max(p, 1e-3))
    card(ctx, -w / 2, -h / 2, w, h, col, 1, 18)
    text(ctx, label, 0, size * 0.36, size, fg or C["white"], 1, HEAD, True, "center")
    ctx.restore()


def piggy(ctx, cx, cy, s, t, a=1.0):
    pink, dark = (0xF2, 0x9C, 0xB8), (0xC4, 0x5E, 0x84)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for lx in (-60, -20, 25, 60):                       # legs
        rrect(ctx, lx - 14, 50, 28, 46, 6); ctx.set_source_rgba(*rgba(dark, a)); ctx.fill()
    ctx.new_path(); ctx.save(); ctx.scale(1.25, 1); ctx.arc(0, 0, 90, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*rgba(pink, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(6); ctx.stroke()
    ctx.new_path(); ctx.save(); ctx.translate(112, 4); ctx.scale(0.8, 1); ctx.arc(0, 0, 30, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*rgba(dark, a)); ctx.fill_preserve(); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(5); ctx.stroke()
    for nx in (104, 120):
        ctx.new_path(); ctx.arc(nx, 4, 5, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
    ctx.new_path(); ctx.arc(60, -30, 9, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()
    ctx.new_path(); ctx.move_to(30, -78); ctx.line_to(55, -120); ctx.line_to(70, -72); ctx.close_path()
    ctx.set_source_rgba(*rgba(dark, a)); ctx.fill()
    rrect(ctx, -40, -92, 70, 12, 6); ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.fill()     # coin slot
    ctx.restore()


def coin(ctx, x, y, r, t, a=1.0):
    sx = abs(math.cos(t * 7))
    ctx.save(); ctx.translate(x, y); ctx.scale(max(0.12, sx), 1)
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["yellow"], a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba((0xC9, 0x8A, 0x1C), a)); ctx.set_line_width(r * 0.16); ctx.stroke()
    if sx > 0.45:
        text(ctx, "$", 0, r * 0.36, r, (0x8A, 0x5A, 0x10), a, HEAD, True, "center")
    ctx.restore()


def star(ctx, x, y, r, col, a=1.0, rot=0.0):
    ctx.new_path()
    for k in range(10):
        ang = rot - math.pi / 2 + k * math.pi / 5
        rr_ = r if k % 2 == 0 else r * 0.45
        (ctx.move_to if k == 0 else ctx.line_to)(x + math.cos(ang) * rr_, y + math.sin(ang) * rr_)
    ctx.close_path(); ctx.set_source_rgba(*rgba(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"], a)); ctx.set_line_width(4); ctx.stroke()


def clock(ctx, cx, cy, r, t, speed=1.0):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*rgba(C["cream"])); ctx.fill_preserve()
    ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(10); ctx.stroke()
    for k in range(12):
        a = k * math.pi / 6
        rect(ctx, cx + math.cos(a) * r * 0.8 - 5, cy + math.sin(a) * r * 0.8 - 5, 10, 10, C["ink"])
    for ln, sp, wd in ((r * 0.75, 6.0 * speed, 7), (r * 0.5, 0.5 * speed, 11)):
        a = t * sp - math.pi / 2
        ctx.new_path(); ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(a) * ln, cy + math.sin(a) * ln)
        ctx.set_source_rgba(*rgba(C["ink"])); ctx.set_line_width(wd); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def sx_of(i, i0, i1, box):
    return box[0] + (i - i0) / (i1 - i0) * box[2]


def sy_of(v, vmin, vmax, box):
    return box[1] + box[3] - (v - vmin) / (vmax - vmin) * box[3]


def year_axis(ctx, box, i0, i1, years, a=0.6, size=24):
    for yr in years:
        i = di(f"{yr}-01-01")
        text(ctx, str(yr), sx_of(i, i0, i1, box), box[1] + box[3] + 46, size, C["ink"], a, MONO, True, "center")


def money_k(v):
    return "${:,.0f}K".format(v / 1000)




def stadium(ctx, t):
    bg_fill(ctx, (0x10, 0x16, 0x2A), (0x06, 0x0A, 0x14))
    for k, (cx, ph) in enumerate(((120, 0), (960, 1.7))):
        ang = math.sin(t * 0.9 + ph) * 0.35
        ctx.save(); ctx.translate(cx, 300); ctx.rotate(ang)
        g = cairo.LinearGradient(0, 0, 0, 1500)
        g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.22); g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0)
        ctx.set_source(g); ctx.new_path(); ctx.move_to(-30, 0); ctx.line_to(30, 0); ctx.line_to(320, 1500); ctx.line_to(-320, 1500); ctx.close_path(); ctx.fill()
        ctx.restore()
        ctx.new_path(); ctx.arc(cx, 300, 34, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.95, 0.8, 1); ctx.fill()
    rect(ctx, 0, 1300, W, H - 1300, (0x2E, 0x7D, 0x32))
    for k in range(9):
        rect(ctx, k * 130 - 20, 1300, 65, H - 1300, (0x36, 0x8F, 0x3A))


