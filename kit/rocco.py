"""Rocco - Strategy Autopsy pixel raccoon mascot (original character)."""
import math
import cairo

PAL = {
    "K": (0x14, 0x18, 0x1C), "g": (0x8A, 0x94, 0x9B), "D": (0x3A, 0x42, 0x48), "M": (0x1A, 0x1D, 0x20),
    "W": (0xF2, 0xF0, 0xE8), "l": (0xC9, 0xD0, 0xD4), "P": (0x0E, 0x10, 0x12), "N": (0x0E, 0x10, 0x12),
    "R": (0xFF, 0x4D, 0x6A), "E": (0x22, 0xE5, 0x8B), "e": (0x17, 0xA8, 0x66),
    # costume colors
    "b": (0x6B, 0x4A, 0x2E), "c": (0x4A, 0x33, 0x20),          # brown hat
    "y": (0xF2, 0xB1, 0x34), "Y": (0xC9, 0x8A, 0x1C),          # yellow / gold
    "r": (0xD9, 0x3A, 0x3A), "q": (0xA8, 0x26, 0x2A),          # firefighter red
    "u": (0x3D, 0x7D, 0xD8), "v": (0x2A, 0x5A, 0xA8),          # blue
    "p": (0xB0, 0x5C, 0xD8), "s": (0xFF, 0xE0, 0x66),          # party purple / star
    "S": (0x9A, 0xA4, 0xAA), "w": (0xFF, 0xFF, 0xFF),          # steel, pure white
    "z": (0x22, 0x26, 0x2B),                                   # top hat black
}

BASE = [
    ".KK............KK.....",
    "KDDK..........KDDK....",
    "KDlDKKKKKKKKKKDlDK....",
    "KDDggggggggggggDDK....",
    ".KggggggggggggggK.....",
    "KggWWWWggggWWWWggK....",
    "KgMMMMMMWWMMMMMMgK....",
    "KMMWPMMMWWMMMPWMMK....",
    "KgMMMMMMWWMMMMMMgK....",
    "KggWWWWWNNWWWWWggK....",
    ".KggWWWKWWKWWWggK.....",
    "..KKggWWKKWWggKK......",
    "..KggggggggggggK...KK.",
    ".KgggllllllllgggK.KDDK",
    ".KggKllllllllKggKKggK.",
    ".KKK.KllllllK.KKKDDK..",
    ".....KllllllK..KggK...",
    ".....KggggggKKKDDK....",
    ".....KggKKggK.KKK.....",
    ".....KDDKKDDK.........",
    ".....KKKKKKKK.........",
]
COLS = max(len(r) for r in BASE)
BASE = [r.ljust(COLS, ".") for r in BASE]
ROWS = len(BASE)

EXPR = {
    "neutral": [],
    "talk": [(10, 7, "KRRK"), (11, 8, "RR")],
    "shock": [(6, 3, "WW"), (6, 13, "WW"), (7, 3, "WP"), (7, 13, "PW"), (10, 7, "WKKW"), (11, 7, "KRRK")],
    "smug": [(7, 3, "KP"), (7, 13, "PK"), (10, 7, "WWWK"), (11, 8, "KK")],
    "blink": [(7, 3, "MM"), (7, 13, "MM")],
    "sleep": [(7, 3, "KK"), (7, 13, "KK"), (10, 7, "WKKW"), (11, 8, "WW")],
    "sad": [(10, 7, "WKKW"), (11, 7, "K..K")],
}

# costume patches: (row, col, string). Rows < 0 sit above the head.
COSTUME = {
    "none": [],
    "grad": [(-3, 3, "KKKKKKKKKKKK"), (-2, 1, "KzzzzzzzzzzzzzzK"), (-1, 3, "KKzzzzzzzzKK"),
             (0, 4, "KzzzzzzzzzK"), (1, 4, "KKKKKKKKKK"), (-2, 15, "Ky"), (-1, 16, "y"), (0, 16, "yK"), (1, 16, "yy")],
    "lab": [(2, 3, "KKKKKKKKKKKKK"), (3, 3, "KuuKSSSSSKuuK"), (4, 3, "KuuK.....KuuK"), (5, 3, "KKKK.....KKKK"),
            (12, 3, "wwwwwwwwwwww"), (13, 2, "wwwwDwwwwDwwww"), (14, 2, "ww"), (14, 5, "wwwDwwDwww"), (14, 14, "ww"),
            (15, 6, "wwDwwD"), (16, 6, "wwwwww")],
    "race": [(-1, 3, "KKKKKKKKKKKK"), (0, 2, "KEEEEEEEEEEEEK"), (1, 2, "KEEwwEEEEEEEEK"),
             (2, 2, "KeeeeeeeeeeeeKKKK"), (3, 13, "KEEEEEK")],
    "detective": [(-2, 4, "KKKKKKKKKK"), (-1, 3, "KbbbbbbbbbbK"), (0, 3, "KbbbbbbbbbbK"),
                  (1, 0, "KKccccccccccccccKK"), (2, 0, "KbbbbbbbbbbbbbbbbK"), (3, 1, "KKKKKKKKKKKKKKKK")],
    "night": [(-2, 13, "KK"), (-1, 11, "KuuK"), (0, 8, "KKuuuvK"), (1, 3, "KKKKKuuuuvvK"),
              (2, 2, "KuuuuuuuuuuuuuK"), (3, 2, "KwwwwwwwwwwwwwwK"), (-3, 14, "ww"), (-2, 15, "w")],
    "party": [(-4, 8, "KK"), (-3, 7, "KppK"), (-2, 6, "KpspK"), (-1, 5, "KpppspK"), (0, 5, "KspppppK"),
              (1, 4, "KpppspppK"), (2, 4, "KKKKKKKKK"), (-5, 8, "ss")],
    "fire": [(-2, 4, "KKKKKKKKKK"), (-1, 3, "KrrrrryrrrrK"), (0, 2, "KrrrryyyrrrrK"), (1, 2, "KrrrrryrrrrrK"),
             (2, 0, "KKqqqqqqqqqqqqqqKK"), (3, 0, "KqqqqqqqqqqqqqqqqK")],
    "tophat": [(-5, 5, "KKKKKKKK"), (-4, 5, "KzzzzzzK"), (-3, 5, "KzzzzzzK"), (-2, 5, "KEEEEEEK"),
               (-1, 5, "KzzzzzzK"), (0, 2, "KKKzzzzzzKKK"), (1, 2, "KzzzzzzzzzzzzK")],
}


def build(expr="neutral", costume="none"):
    rows = [list(r) for r in BASE]
    over = {}
    for patch in (EXPR.get(expr, []), COSTUME.get(costume, [])):
        for (rj, ci, s) in patch:
            for k, ch in enumerate(s):
                if ch == ".":
                    continue
                if 0 <= rj < ROWS and 0 <= ci + k < COLS:
                    rows[rj][ci + k] = ch
                else:
                    over[(ci + k, rj)] = ch
    return rows, over


def draw_rocco(ctx, x, y, px, expr="neutral", costume="none", alpha=1.0):
    """x,y = top-left of the base grid."""
    rows, over = build(expr, costume)

    def cell(i, j, ch):
        r, g, b = PAL[ch]
        ctx.set_source_rgba(r / 255, g / 255, b / 255, alpha)
        ctx.rectangle(x + i * px, y + j * px, px + 0.6, px + 0.6)
        ctx.fill()

    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                cell(i, j, ch)
    for (i, j), ch in over.items():
        cell(i, j, ch)


# right paw (raised-arm anchor) in grid units, for props
PAW = (16.0, 14.0)

if __name__ == "__main__":
    items = [("neutral", "none"), ("talk", "none"), ("shock", "none"), ("smug", "none"), ("sleep", "night"),
             ("talk", "grad"), ("neutral", "lab"), ("talk", "race"), ("smug", "detective"), ("neutral", "party"),
             ("shock", "fire"), ("talk", "tophat")]
    W, H = 1900, 900
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0x1E / 255, 0x2A / 255, 0x30 / 255); ctx.paint()
    px = 12
    for k, (e, c) in enumerate(items):
        col, row = k % 6, k // 6
        x = 40 + col * 310
        y = 120 + row * 410
        draw_rocco(ctx, x, y, px, e, c)
        ctx.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(22); ctx.set_source_rgb(0.9, 0.9, 0.88)
        ctx.move_to(x, y + ROWS * px + 40); ctx.show_text(f"{e} / {c}")
    surf.write_to_png("rocco_sheet.png")
