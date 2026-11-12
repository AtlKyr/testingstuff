T = dict(
    crashed=wt("crashed"), four=wt("four"), jumped=wt("jumped"), two1=wt("two"), One1=wt("One"), simple=wt("simple"), line1=wt("line"),
    dodge=wt("dodge"), A=wt("A"), beats=wt("beats"), B=wt("B"), holding1=wt("holding"), wins=wt("wins"), But=wt("But"), trap1=wt("trap"),
    hiding=wt("hiding"), chart1=wt("chart"), rule=wt("rule"), above=wt("above"), average=wt("average"), Below=wt("Below"), cash=wt("cash"),
    Two2=wt("Two"), sinks=wt("sinks"), thirtysix=wt("thirty-six"), Almost=wt("Almost"), flat=wt("flat"),
    For=wt("For"), six=wt("six"), leads=wt("leads"), Then=wt("Then"), slipping=wt("slipping"), Remember=wt("Remember"),
    Down=wt("Down"), up=wt("up"), down2=wt("down"), whipsaw=wt("whipsaw"), Fortyone=wt("Forty-one"), fakeouts=wt("fakeouts"),
    within=wt("within"), Most=wt("Most"), lost=wt("lost"), In2=wt("In"), sold=wt("sold"), crash2=wt("crash"), bought=wt("bought"),
    bounce=wt("bounce"), Final=wt("Final"), score=wt("score"), fortythree=wt("forty-three"), Just3=wt("Just"),
    seventy=wt("seventy"), Less=wt("Less"), half=wt("half"), pain=wt("pain"), Way=wt("Way"), money2=wt("money", 2),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["fortythree"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.5
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["One1"] - 0.1, "line"), (T["A"] - 0.12, "guess"), (T["But"] - 0.1, "trap"), (T["rule"] - 0.25, "rules"),
    (T["Two2"] - 0.1, "crash"), (T["For"] - 0.1, "leads"), (T["Remember"] - 0.1, "remember"), (T["Fortyone"] - 0.15, "fakeouts"),
    (T["In2"] - 0.1, "covid"), (T["Final"] - 0.1, "score"), (T["Less"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["four"], 70) + hop(tl, T["two1"], 70)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "line":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["simple"], 60) + hop(t, T["dodge"], 70)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["beats"], 50) + hop(t, T["holding1"], 50)
    elif name == "trap":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["above"], 45) + hop(t, T["Below"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["thirtysix"], 50) + hop(t, T["flat"], 60)
    elif name == "leads":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["six"], 50) + hop(t, T["leads"], 40)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Down"], 40) + hop(t, T["up"], 70) + hop(t, T["down2"], 40) + hop(t, T["whipsaw"], 60)
    elif name == "fakeouts":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift = 0
    elif name == "covid":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["sold"], 40) + hop(t, T["bounce"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["fortythree"], 35) + hop(t, T["seventy"], 45)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["half"], 90) + hop(t, T["Way"], 110, 0.55)
    return x, y, px, flip, moving, lift
