T = dict(
    best=wt("best"), August=wt("August"), two1=wt("two"), percent1=wt("percent"), Lock=wt("Lock"), profits1=wt("profits"),
    A=wt("A"), hold1=wt("hold"), B=wt("B"), One1=wt("One"), spring1=wt("spring"), race=wt("race"),
    rule=wt("rule"), big=wt("big"), sell=wt("sell"), month1=wt("month"), back1=wt("back"),
    Two=wt("Two"), Big=wt("Big"), crash=wt("mid-crash"), aside=wt("aside"),
    pulls=wt("pulls"), ahead=wt("ahead"), March1=wt("March"), five1=wt("five"), dollars=wt("dollars"),
    Remember=wt("Remember"), spring2=wt("spring", 2), roars=wt("roars"), cashes=wt("cashes"), time=wt("time"),
    One2=wt("One", 2), sale=wt("sale"), later=wt("later"), fourteen=wt("fourteen"), higher=wt("higher"),
    lead=wt("lead"), gone=wt("gone"), good=wt("good"),
    Final=wt("Final"), seventytwo=wt("seventy-two"), fiftyeight=wt("fifty-eight"),
    Locking=wt("Locking"), locked=wt("locked"), out=wt("out", 2), Wait=wt("Wait"), week3=wt("week", 3), wins=wt("wins"),
)
T["rev1"] = T["seventytwo"] + 0.1
T["rev2"] = T["fiftyeight"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["best"] - 0.1, "point"), (T["Lock"] - 0.12, "guess"), (T["One1"] - 0.1, "clue"),
    (wt("The", 2) - 0.1, "rules"), (T["Two"] - 0.1, "crash"), (wt("The", 3) - 0.1, "ahead"),
    (T["Remember"] - 0.1, "remember"), (T["One2"] - 0.1, "sale"), (T["lead"] - 0.25, "gone"), (T["Final"] - 0.1, "score"),
    (T["Locking"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["August"], 80) if tl < 3 else idle(tl)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "point":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["two1"], 60) + hop(t, T["percent1"], 50)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell"], 45) + hop(t, T["back1"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["crash"], 40)
    elif name == "ahead":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ahead"], 60) + hop(t, T["five1"], 60)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["spring2"], 60) + hop(t, T["cashes"], 40)
    elif name == "sale":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift = 0
    elif name == "gone":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["gone"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; y = 1380
        lift += hop(t, T["seventytwo"], 35) + hop(t, T["fiftyeight"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["locked"], 90) + hop(t, T["wins"], 110, 0.55)
    return x, y, px, flip, moving, lift
