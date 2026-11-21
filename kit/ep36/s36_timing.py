T = dict(
    Ten=wt("Ten"), six=wt("six"), times=wt("times"), Bail=wt("Bail"), A=wt("A"), ride=wt("ride"), B=wt("B"),
    One=wt("One"), Christmas=wt("Christmas"), Eve=wt("Eve"), Friday=wt("Friday"), correction=wt("correction"),
    The=wt("The"), rule=wt("rule"), ten=wt("ten"), sell=wt("sell"), Buy=wt("Buy"), twenty1=wt("twenty"), new=wt("new"),
    Two=wt("Two"), cheaper=wt("cheaper"), Twenty1=wt("Twenty"), crash=wt("crash"), higher1=wt("higher"),
    Early=wt("Early"), again=wt("again"), That=wt("That"), slide=wt("slide"), December=wt("December"),
    Remember=wt("Remember"), SPY2=wt("SPY", 2), twenty3=wt("twenty", 3), two1=wt("two"), Two2=wt("Two", 2),
    tenths1=wt("tenths"), line1=wt("line"), cheap=wt("cheap"), Twenty2=wt("Twenty", 2), twentytwo=wt("twenty-two"),
    bargains=wt("bargains"), Final=wt("Final"), seventy=wt("seventy"), eightyfive=wt("eighty-five"), It=wt("It"),
    won=wt("won"), Move=wt("Move"), tenths2=wt("tenths", 2), loses=wt("loses"),
)
T["rev1"] = T["seventy"] + 0.1
T["rev2"] = T["eightyfive"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Bail"] - 0.12, "guess"), (T["Friday"] - 0.12, "news"),
    (T["The"] - 0.12, "rules"), (T["Two"] - 0.12, "y2008"), (T["Twenty1"] - 0.12, "miss"), (T["That"] - 0.12, "fall"),
    (T["Remember"] - 0.1, "remember"), (T["Twenty2"] - 0.12, "more"), (T["Final"] - 0.15, "score"),
    (T["It"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["six"], 80) if tl < 3 else 0)
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
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["Eve"], 50)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "news":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["correction"], 50)
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sell"], 45) + hop(t, T["new"], 45)
    elif name == "y2008":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["cheaper"], 50)
    elif name == "miss":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "fall":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["tenths1"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["cheap"], 45)
    elif name == "more":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["bargains"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["won"], 80) + hop(t, T["loses"], 100, 0.55)
    return x, y, px, flip, moving, lift
