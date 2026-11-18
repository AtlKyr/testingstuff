T = dict(
    four1=wt("four"), straight=wt("straight"), Buy=wt("Buy"), A1=wt("A"), Wait=wt("Wait"), B1=wt("B"), One=wt("One"),
    October1=wt("October"), Two1=wt("Two"), thousand1=wt("thousand"), streak=wt("streak"), A2=wt("A", 2), morning1=wt("morning"),
    B2=wt("B", 2), green2=wt("green", 2), For=wt("For"), neck=wt("neck"), Christmas=wt("Christmas"), A3=wt("A", 3),
    knife=wt("knife"), B3=wt("B", 3), cheaper=wt("cheaper"), So=wt("So"), pays=wt("pays"), Now=wt("Now"), October2=wt("October", 2),
    Two2=wt("Two", 2), A4=wt("A", 4), three=wt("three"), B4=wt("B", 4), Green=wt("Green"), biggest=wt("biggest"),
    B5=wt("B", 5), seven=wt("seven"), higher=wt("higher"), Final=wt("Final"), fortyeight=wt("forty-eight"), fifty=wt("fifty"),
    Waiting=wt("Waiting"), safer=wt("safer"), cost=wt("cost"),
)
T["rev1"] = T["fortyeight"] + 0.1
T["rev2"] = T["fifty"] + 0.1
T["rev3"] = T["rev2"] + 0.8
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Buy"] - 0.12, "guess"), (T["One"] - 0.12, "clue"), (T["Two1"] - 0.1, "rules"),
    (T["For"] - 0.1, "years"), (T["Christmas"] - 0.1, "xmas"), (T["Now"] - 0.1, "remember"), (T["A4"] - 0.1, "oct08"),
    (T["Final"] - 0.1, "score"), (T["Waiting"] - 0.1, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 560 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["four1"], 80) if tl < 4 else 0)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


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
        lift += hop(t, T["A1"], 40) + hop(t, T["B1"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A2"], 45) + hop(t, T["B2"], 45)
    elif name == "years":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "xmas":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["knife"], 40) + hop(t, T["cheaper"], 60)
    elif name == "remember":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Two2"], 60)
    elif name == "oct08":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Green"], 50) + hop(t, T["seven"], 60)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; y = 1380
        lift += hop(t, T["fortyeight"], 35) + hop(t, T["fifty"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["safer"], 80) + hop(t, T["cost"], 100, 0.55)
    return x, y, px, flip, moving, lift
