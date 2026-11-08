# ================================================================ timeline (long #2)
def _prev_end(ch):
    k = int(ch[2:]) - 1
    ws = [w for w in WORDS if w["ch"] == f"ch{k}"]
    return ws[-1]["end"]


def c(ch, off=1.6):
    return max(_prev_end(ch) + 0.15, CHSTART[ch] - off)


def R(costume, **kw):
    d = dict(costume=costume); d.update(kw); return d


SAD = lambda e, t: "sad" if e != "talk" else e
SMUG = lambda e, t: "smug" if e != "talk" else e
SHOCK = lambda e, t: "shock" if e != "talk" else e

SCENES = [
    # ---- ch0 cold open
    (0.0, s_hook1, R("fire", enter="none", shake=(0.0, 4.4), expr=SHOCK), None, None),
    (A("ch0", "Its") - 0.1, s_hook2, R("detective", enter="drop", expr=SHOCK), None, None),
    (A("ch0", "Around") - 0.1, s_hook3, R("tophat", shake=(A("ch0", "gone"), A("ch0", "session") + 0.5), expr=SAD), None, None),
    (A("ch0", "So") - 0.1, s_hook4, R("party", pace=True), "THE ONLY QUESTION", [C["red"], C["ink"]]),
    (A("ch0", "went") - 0.3, s_hook5, R("lab", hops=[A("ch0", "Thirty-nine")]), "20 YEARS OF CRASHES", None),
    (A("ch0", "followed") - 0.2, s_hook6, R("detective", prop=prop_magnifier), "I FOLLOWED EVERY ONE", None),
    (A("ch0", "Before") - 0.1, s_guess, R("party", enter="drop", hops=[A("ch0", "A", 4), A("ch0", "B")]), None, None),
    (A("ch0", "And", 2) - 0.1, s_tease, R("tophat", float=True, expr=SMUG), "COMING UP", [C["purple"], C["yellow"]]),
    # ---- ch1 what happened
    (c("ch1"), chapter_card("CHAPTER 1", "WHAT JUST HAPPENED", "the week the Nasdaq cracked", C["red"]), R("doctor", enter="none"), None, None),
    (A("ch1", "On", 1) - 0.1, s_record, R("crown", expr=SMUG, hops=[A("ch1", "record")]), "OCTOBER 6", [C["green"], C["yellow"]]),
    (A("ch1", "Then") - 0.1, s_selloff, R("fire", shake=(A("ch1", "Thursday"), A("ch1", "twenty", 2) + 0.4), expr=SHOCK), "THURSDAY, NOV 5", [C["red"], C["ink"]]),
    (A("ch1", "That") - 0.1, s_correction, R("doctor"), "OFFICIAL", [C["red"], C["white"]]),
    (A("ch1", "Friday") - 0.3, s_bounce, R("party", hops=[A("ch1", "bounced")]), "FRIDAY", [C["green"], C["white"]]),
    (A("ch1", "One", 2) - 0.1, s_world, R("night", expr=SAD), None, None),
    # ---- ch2 39 crash days
    (c("ch2"), chapter_card("CHAPTER 2", "39 CRASH DAYS", "every -4% day since 2005", C["yellow"]), R("doctor", enter="none"), None, None),
    (A("ch2", "used") - 0.3, s_method, R("lab", hops=[A("ch2", "marked")]), "THE TEST", None),
    (A("ch2", "And") - 0.1, s_timeline39, R("detective", prop=prop_magnifier), "WHERE THEY LAND", None),
    (A("ch2", "worst") - 0.25, s_worst, R("fire", shake=(A("ch2", "Minus"), A("ch2", "day") + 0.5), expr=SHOCK), "THE WORST ONE", [C["red"], C["ink"]]),
    (A("ch2", "So") - 0.1, s_morning, R("grad"), None, None),
    # ---- ch3 next day / month
    (c("ch3"), chapter_card("CHAPTER 3", "THE MORNING AFTER", "a day later, a month later", C["blue"]), R("doctor", enter="none"), None, None),
    (A("ch3", "fifty-nine") - 0.8, s_nextday, R("grad", hops=[A("ch3", "bounce")]), None, None),
    (A("ch3", "But") - 0.1, s_month, R("night", expr=SAD), None, None),
    (A("ch3", "In") - 0.1, s_sep08, R("fire", prop=prop_umbrella, expr=SHOCK), "SEPTEMBER 2008", [C["red"], C["ink"]]),
    (A("ch3", "If") - 0.1, s_coin, R("tophat", expr=SMUG), "A QUICK RESCUE?", [C["purple"], C["yellow"]]),
    (A("ch3", "So", 3) - 0.1, s_getout, R("race", pace=True), None, None),
    # ---- ch4 panic seller
    (c("ch4"), chapter_card("CHAPTER 4", "THE PANIC SELLER", "sell after the crash, buy back later", C["purple"]), R("doctor", enter="none"), None, None),
    (A("ch4", "Ten") - 0.3, s_two, R("detective", hops=[A("ch4", "holder"), A("ch4", "panic")]), "TWO INVESTORS", [C["green"], C["red"]]),
    (A("ch4", "Two", 1) - 0.1, s_race, R("race", prop=prop_flag, shake=(A("ch4", "rebound"), A("ch4", "behind") + 0.5)), "THE RACE", None),
    (A("ch4", "Final") - 0.1, score_scene([("THE HOLDER", 10000, 70214, A("ch4", "seventy"), C["white"]),
                                            ("PANIC SELLER", 10000, 80518, A("ch4", "eighty"), C["red"])],
                                           "$10,000 EACH · SPY 2005-2024 · FEES INCLUDED", "ch4", ("PANIC WON?!", A("ch4", "won"), C["yellow"])),
     R("crown", expr=SHOCK, hops=[A("ch4", "won")]), "FINAL SCORE", None),
    (A("ch4", "Not") - 0.1, s_windows, R("lab", hops=[A("ch4", "narrow")]), "NOT SO FAST", [C["red"], C["yellow"]]),
    (A("ch4", "problem") - 0.6, s_hindsight, R("detective", prop=prop_magnifier), "THE PROBLEM", [C["red"], C["ink"]]),
    # ---- ch5 second trap
    (c("ch5"), chapter_card("CHAPTER 5", "THE SECOND TRAP", "where the best days hide", C["yellow"]), R("doctor", enter="none"), None, None),
    (A("ch5", "I") - 0.1, s_best10, R("lab", hops=[A("ch5", "Nine")]), "THE 10 BEST DAYS", [C["yellow"], C["white"]]),
    (A("ch5", "October") - 0.3, s_bestcards, R("party"), "RIGHT NEXT TO THE CRASHES", None),
    (A("ch5", "hide") - 0.8, s_hide, R("tophat", expr=SMUG), "THE PATTERN", [C["purple"], C["yellow"]]),
    (A("ch5", "Sell") - 0.1, s_doors, R("night", expr=SAD, side="L"), "SELL AFTER THE CRASH...", [C["red"], C["ink"]]),
    # ---- ch6 the answer
    (c("ch6"), chapter_card("CHAPTER 6", "THE ANSWER", "39 crash days, one year later", C["green"]), R("doctor", enter="none"), None, None),
    (A("ch6", "Your") - 0.1, s_answer, R("party", enter="drop", hops=[A("ch6", "Thirty-six", 1), A("ch6", "Thirty-six", 2)]), None, None),
    (A("ch6", "typical") - 0.2, s_tiles, R("crown", expr=SMUG), "ALL 39, ONE YEAR LATER", [C["green"], C["white"]]),
    (A("ch6", "And") - 0.1, s_lehman, R("doctor", expr=SAD), "THE ONLY 3 LOSERS", [C["red"], C["ink"]]),
    (A("ch6", "Now") - 0.1, s_honest, R("grad"), None, None),
    (A("ch6", "Verdict") - 0.1, s_verdict, R("doctor", expr=SMUG), "VERDICT", [C["green"], C["white"]]),
    # ---- ch7 outro
    (A("ch7", "This") - 0.1, s_outro, R("tophat", hops=[A("ch7", "Next"), A("ch7", "subscribe")]), "WHAT'S NEXT?", None),
]
BOUNDS = [s[0] for s in SCENES[1:]]
CARDS = [s[0] for s in SCENES if s[1].__name__ == "f" and s[3] is None and s[2].get("enter") == "none" and s[0] > 1]


def scene_at(t):
    cur = 0
    for k, s in enumerate(SCENES):
        if t >= s[0]:
            cur = k
    s0 = SCENES[cur][0]
    s1 = SCENES[cur + 1][0] if cur + 1 < len(SCENES) else TOTAL
    return cur, s0, s1


# ---------------------------------------------------------------- VFX moments
def _ev(t, x, y, pal, sz=1.0):
    return (t, x, y, pal, sz)


EVENTS = [
    _ev(0.05, 700, 470, [C["red"], C["white"]], 1.4),
    _ev(A("ch0", "worst"), 700, 760, [C["red"], C["white"]], 1.2),
    _ev(A("ch0", "trillion"), 700, 380, [C["green"], C["white"]]),
    _ev(A("ch0", "Do"), 700, 520, [C["red"], C["white"]], 1.2),
    _ev(A("ch0", "Thirty-nine"), 700, 835, [C["red"], C["yellow"]], 1.3),
    _ev(A("ch0", "A", 4), 420, 520, [C["red"], C["white"]]), _ev(A("ch0", "B"), 980, 520, [C["green"], C["white"]]),
    _ev(A("ch0", "Lock"), 970, 740, [C["yellow"], C["white"]], 1.2),
    _ev(A("ch0", "wouldn't"), 700, 760, [C["red"], C["purple"]], 1.2),
    _ev(A("ch1", "record"), 900, 300, [C["green"], C["yellow"]]),
    _ev(A("ch1", "twelve"), 470, 340, [C["red"], C["white"]], 1.2),
    _ev(A("ch1", "correction"), 920, 470, [C["red"], C["white"]], 1.3),
    _ev(A("ch1", "first"), 1000, 640, [C["yellow"], C["white"]], 1.2),
    _ev(A("ch2", "Thirty-nine"), 600, 630, [C["yellow"], C["green"]]),
    _ev(A("ch2", "Sixteen"), 240, 760, [C["red"], C["yellow"]]), _ev(A("ch2", "Nine"), 1140, 760, [C["red"], C["yellow"]]),
    _ev(A("ch2", "Minus"), 700, 240, [C["red"], C["white"]], 1.3),
    _ev(A("ch3", "fifty-nine"), 460, 500, [C["yellow"], C["white"]]),
    _ev(A("ch3", "worse"), 700, 400, [C["red"], C["white"]], 1.3),
    _ev(A("ch3", "sixteen"), 900, 560, [C["red"], C["ink"]], 1.2),
    _ev(A("ch3", "coin"), 1000, 300, [C["yellow"], C["white"]], 1.2),
    _ev(A("ch4", "Fees"), 1100, 830, [C["yellow"], C["white"]]),
    _ev(A("ch4", "ahead"), 700, 450, [C["green"], C["white"]]),
    _ev(A("ch4", "behind"), 1000, 450, [C["grey"], C["white"]]),
    _ev(A("ch4", "front"), 1080, 400, [C["green"], C["yellow"]], 1.2),
    _ev(A("ch4", "eighty"), 700, 680, [C["red"], C["yellow"]], 1.3),
    _ev(A("ch4", "won"), 1050, 830, FLAGCOLS, 1.6),
    _ev(A("ch4", "narrow"), 710, 330, [C["green"], C["white"]], 1.2),
    _ev(A("ch4", "looking"), 560, 760, [C["red"], C["white"]], 1.3),
    _ev(A("ch5", "Nine"), 900, 700, [C["yellow"], C["white"]], 1.3),
    _ev(A("ch5", "October"), 400, 520, [C["green"], C["yellow"]]), _ev(A("ch5", "March"), 1000, 520, [C["green"], C["yellow"]]),
    _ev(A("ch5", "earlier"), 640, 640, [C["red"], C["white"]], 1.2),
    _ev(A("ch5", "doors"), 640, 600, [C["yellow"], C["white"]], 1.2),
    _ev(A("ch6", "Thirty-six", 1), 700, 450, [C["green"], C["yellow"], C["white"]], 1.8),
    _ev(A("ch6", "Ninety-two"), 1150, 600, [C["green"], C["white"]], 1.2),
    _ev(A("ch6", "better"), 900, 470, [C["green"], C["yellow"]], 1.3),
    _ev(A("ch6", "Lehman"), 640, 720, [C["red"], C["ink"]], 1.2),
    _ev(A("ch6", "dot-com"), 300, 520, [C["red"], C["white"]]),
    _ev(A("ch6", "loud"), 700, 560, [C["red"], C["white"]], 1.4),
    _ev(A("ch6", "quiet"), 700, 760, [C["green"], C["white"], C["yellow"]], 1.6),
    _ev(A("ch7", "subscribe"), 640, 760, FLAGCOLS, 1.3),
]
PUNCH = [e[0] for e in EVENTS if e[4] >= 1.2]
FLASH = [0.05, A("ch1", "correction"), A("ch4", "won"), A("ch6", "Thirty-six", 1), A("ch6", "loud")]


def render(out, t0=0.0, t1=None, preview=0):
    t1 = TOTAL if t1 is None else t1
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-profile:v", "high", "-level", "4.2",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        t = f / FPS
        frame(ctx, t)
        surf.flush()
        proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close(); proc.wait()


def frame(ctx, t):
    t_glob[0] = t
    k, s0, s1 = scene_at(t)
    st, fn, spec, title, cols = SCENES[k]
    ctx.save()
    z = (1 + 0.025 * prog(t, s0, max(0.5, s1 - s0))) * punch(t)
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2)
    fn(ctx, t, s0, s1)
    if title:
        bunting(ctx, title, t, s0, cols)
    rocco(ctx, t, s0, spec)
    bursts(ctx, t)
    ctx.restore()
    vignette(ctx)
    captions(ctx, t)
    paper_grain(ctx, 0.05)
    flash(ctx, t)
    wipe(ctx, t)


def snap(path, t):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    frame(ctx, t)
    surf.write_to_png(path)


if __name__ == "__main__":
    if sys.argv[1] == "snap":
        snap(sys.argv[2], float(sys.argv[3]))
    else:
        out = sys.argv[1]
        a = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
        b = float(sys.argv[3]) if len(sys.argv) > 3 else None
        render(out, a, b)
