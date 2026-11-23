def wi(i):
    return WORDS[i]["start"]


assert WORDS[0]["text"] == "A" and WORDS[7]["text"] == "Sell," and WORDS[12]["text"] == "B?" and WORDS[13]["text"] == "Watch"
assert WORDS[18]["text"] == "The" and WORDS[34]["text"] == "Two" and WORDS[47]["text"] == "December" and WORDS[70]["text"] == "So"
assert WORDS[91]["text"] == "Then" and WORDS[106]["text"] == "He" and WORDS[118]["text"] == "Final" and WORDS[123]["text"] == "twenty-nine"
assert WORDS[127]["text"] == "seventy-one" and WORDS[129]["text"] == "Six" and WORDS[137]["text"] == "higher."
T = dict(
    death=wi(1), year=wi(6), Sell=wi(7), A=wi(8), B=wi(12), Watch=wi(13), April=wi(15), The=wi(18), short=wi(20), long=wi(25),
    He=wi(27), sits=wi(30), Two=wi(34), first=wi(38), sells=wi(41), climbs=wi(44), December=wi(47), another=wi(51),
    He2=wi(53), crash=wi(58), buys=wi(60), forty=wi(63), Now=wi(66), ahead=wi(69), So=wi(70), works=wi(73), Twenty=wi(74),
    eleven=wi(77), crosses=wi(80), rips=wi(85), lead=wi(88), gone=wi(90), Then=wi(91), April2=wi(93), twenty2=wi(97),
    cross2=wi(99), bottom=wi(105), He3=wi(106), year2=wi(109), buys2=wi(112), sixty=wi(115), Final=wi(118),
    twentynine=wi(123), seventyone=wi(127), Six=wi(129), eight=wi(132), bought=wi(135), higher=wi(137),
)
T["rev1"] = T["twentynine"] + 0.1
T["rev2"] = T["seventyone"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Sell"] - 0.12, "guess"), (T["The"] - 0.12, "rules"), (T["Two"] - 0.12, "y2006"),
    (T["December"] - 0.12, "y2008"), (T["So"] - 0.12, "y2011"), (T["Then"] - 0.12, "remember"), (T["He3"] - 0.12, "rebuy"),
    (T["Final"] - 0.15, "score"), (T["Six"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["y2011"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["year"], 80) if tl < 3 else 0)
    return x, y, px, False, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "guess":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["April"], 50)
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["long"], 45) + hop(t, T["sits"], 40)
    elif name == "y2006":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "y2008":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["forty"], 40) + hop(t, T["ahead"], 60)
    elif name == "y2011":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["rips"], 30)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["cross2"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["bottom"], 40)
    elif name == "rebuy":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sixty"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); moving = 0 < k < 1; flip = True; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift += hop(t, T["eight"], 80) + hop(t, T["higher"], 100, 0.55)
    return x, y, px, flip, moving, lift
