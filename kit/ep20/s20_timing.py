T = dict(
    ten=wt("ten-year"), five=wt("five"), Its=wt("It's"), full1=wt("full"), point1=wt("point"), year1=wt("year"), So=wt("So"),
    sell1=wt("sell"), stocks=wt("stocks"), spike=wt("spike"), A=wt("A"), hide=wt("hide"), B=wt("B"), hold=wt("hold"),
    But=wt("But"), year2=wt("year", 2), answer=wt("answer"), rule1=wt("rule"), jumps=wt("jumps"), cash1=wt("cash"),
    Two=wt("Two"), fell=wt("fell"), stayed=wt("stayed"), crashed=wt("crashed"), everyone=wt("everyone"),
    Twenty1=wt("Twenty"), thirteen=wt("thirteen"), sells=wt("sells"), less=wt("less"), rally1=wt("rally"),
    Remember=wt("Remember"), twentytwo=wt("twenty-two"), exploded=wt("exploded"), The3=wt("The", 3), hid=wt("hid"),
    seven=wt("seven"), Holders=wt("Holders"), nineteen=wt("nineteen"), It=wt("It"), almost=wt("almost"), up2=wt("up", 2),
    Then=wt("Then"), twentythree=wt("twenty-three"), out=wt("out"), half2=wt("half", 2), rally2=wt("rally", 2),
    Final=wt("Final"), fiftyeight=wt("fifty-eight"), Just2=wt("Just"), sixtysix=wt("sixty-six"),
    Nudge=wt("Nudge"), trigger=wt("trigger"), winner=wt("winner"), flip=wt("flip"),
)
T["rev1"] = T["fiftyeight"] + 0.1
T["rev2"] = T["sixtysix"] + 0.1
T["rev3"] = T["rev2"] + 0.6
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Its"] - 0.1, "point"), (T["So"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (T["But"] - 0.1, "clue"),
    (wt("The", 2) - 0.2, "rules"), (T["Two"] - 0.1, "crash"), (T["Twenty1"] - 0.1, "y2013"),
    (T["Remember"] - 0.1, "remember"), (T["The3"] - 0.1, "y2022"), (T["It"] - 0.1, "caught"), (T["Final"] - 0.1, "score"),
    (T["Nudge"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["five"], 80)
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
        lift += hop(t, T["full1"], 60) + hop(t, T["point1"], 60)
    elif name == "question":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sell1"], 60) + hop(t, T["spike"], 70)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["hide"], 40) + hop(t, T["hold"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 40; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["jumps"], 45) + hop(t, T["cash1"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["crashed"], 40)
    elif name == "y2013":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sells"], 40) + hop(t, T["less"], 40)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["twentytwo"], 60) + hop(t, T["exploded"], 60)
    elif name == "y2022":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift = 0
    elif name == "caught":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["almost"], 40) + hop(t, T["out"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["fiftyeight"], 35) + hop(t, T["sixtysix"], 40)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["trigger"], 90) + hop(t, T["flip"], 110, 0.55)
    return x, y, px, flip, moving, lift
