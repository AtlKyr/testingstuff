"""Strategy Autopsy - long-form #2: The Nasdaq just crashed (16:9, Rocco engine)."""
import sys, json, math, subprocess, random
import numpy as np
import pandas as pd
import cairo
from rocco import draw_rocco, ROWS as RROWS, COLS as RCOLS
import rocco as _rocco

W, H, FPS = 1920, 1080, 30
AUDIO = "final_mix_long.wav"
_WJ = json.load(open("words_long.json"))
WORDS = _WJ["words"]
CHSTART = _WJ["chstart"]
END = WORDS[-1]["end"]
TOTAL = END + 2.2

HEAD, MONO, INTER = "Space Grotesk", "JetBrains Mono", "Inter"
C = dict(
    ink=(0x14, 0x18, 0x1C), cream=(0xF4, 0xEC, 0xD8), paper=(0xEE, 0xE4, 0xCC), green=(0x22, 0xE5, 0x8B),
    red=(0xFF, 0x4D, 0x6A), blue=(0x3D, 0x7D, 0xD8), yellow=(0xF2, 0xB1, 0x34), grey=(0x8A, 0x94, 0x9B),
    white=(0xF7, 0xF4, 0xEC), dark=(0x1B, 0x22, 0x27), purple=(0x8E, 0x5C, 0xD8), orange=(0xE8, 0x87, 0x3A),
)
FLAGCOLS = [C["red"], C["green"], C["blue"], C["yellow"]]
_rocco.COSTUME["crown"] = [(-4, 4, "y..y..y..y"), (-3, 4, "yy.yyyy.yy"), (-2, 4, "yyyyyyyyyy"),
                           (-1, 4, "yRyyEEyyRy"), (0, 4, "YYYYYYYYYY")]
_rocco.COSTUME["doctor"] = [(2, 3, "KKKKKKKKKKKKK"), (1, 7, "KSSSSK"), (0, 7, "KwwwSK"), (-1, 8, "KKKK"),
                            (12, 3, "wwwwwwwwwwww"), (13, 2, "wwwwDwwwwDwwww"), (14, 2, "ww"), (14, 5, "wwwSSwSwww"),
                            (14, 14, "ww"), (15, 6, "wwSwwS"), (16, 6, "wwwSSw")]


def A(ch, word, nth=1):
    k = 0
    for w in WORDS:
        if w["ch"] == ch and w["text"].strip(".,?:…—!;") == word:
            k += 1
            if k == nth:
                return w["start"]
    raise KeyError((ch, word, nth))


# ---------------------------------------------------------------- data
_spy = pd.read_csv("spy.csv", parse_dates=["Date"]).set_index("Date").sort_index().loc["2005-01-01":"2024-12-31"]
DATES = _spy.index
N = len(DATES)
ADJ = _spy["Adj Close"].values
RET = np.r_[0.0, ADJ[1:] / ADJ[:-1] - 1]
BH = ADJ / ADJ[0] * 10000
L2 = json.load(open("l2.json"))
CRASH = L2["crash_idx"]
EQP = np.load("eq_panic21.npy")
EQB = np.load("eq_bh.npy")
PANIC = {int(k): v[0] for k, v in L2["panic"].items()}
Y1 = [r["y1"] for r in L2["rows"]]
BEST10 = [int(np.searchsorted(DATES, pd.Timestamp(b[0]))) for b in L2["best10"]]
# out-of-market flags for the 21-day panic seller
OUT = np.zeros(N, bool)
_o = -1
for _i in range(N - 1):
    if _o < _i and RET[_i] <= -0.04:
        _o = _i + 1 + 21
        OUT[_i + 1:_o] = True


def di(d):
    return int(np.searchsorted(DATES, pd.Timestamp(d)))


# paper grain + vignette for 16:9
rng = np.random.default_rng(7)
_gr = (rng.random((H // 2, W // 2)) * 255).astype(np.uint8)
_grain = np.zeros((H // 2, W // 2, 4), dtype=np.uint8)
_grain[..., 0] = _gr; _grain[..., 1] = _gr; _grain[..., 2] = _gr; _grain[..., 3] = 255
GRAIN = cairo.ImageSurface.create_for_data(memoryview(_grain), cairo.FORMAT_RGB24, W // 2, H // 2)


def paper_grain(ctx, a=0.06):
    ctx.save(); ctx.scale(2, 2); ctx.set_source_surface(GRAIN, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_NEAREST)
    ctx.paint_with_alpha(a); ctx.restore()


_vg = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
_vc = cairo.Context(_vg)
_vgr = cairo.RadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, W * 0.62)
_vgr.add_color_stop_rgba(0, 0, 0, 0, 0); _vgr.add_color_stop_rgba(1, 0, 0, 0, 0.42)
_vc.set_source(_vgr); _vc.paint()
VIGNETTE = _vg
