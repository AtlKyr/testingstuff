T = dict(
    Inflation=wt("Inflation"), hot=wt("hot"), Fed1=wt("Fed"), raise_=wt("raise"), December=wt("December"),
    So=wt("So"), sell1=wt("sell"), hikes1=wt("hikes"), A=wt("A"), wait=wt("wait"), B=wt("B"), hold1=wt("hold"),
    The2=wt("The", 1), answer=wt("answer"), one1=wt("one"), cycle1=wt("cycle"),
    The3=wt("The", 2), rule=wt("rule"), sell3=wt("sell", 3), hike1=wt("hike"), buy=wt("buy"), six=wt("six"), months=wt("months"),
    Two1=wt("Two"), five=wt("five"), Hike=wt("Hike"), seller1=wt("seller"), sits=wt("sits"), stocks1=wt("stocks"), climbing=wt("climbing"),
    Then=wt("Then"), eight=wt("eight"), Hes=wt("He's"), time=wt("time"), crash=wt("crash"),
    Now=wt("Now"), strange=wt("strange"), twentynine=wt("twenty-nine"), thirtytwo=wt("thirty-two"), higher1=wt("higher"), later=wt("later"),
    Remember=wt("Remember"), cycle2=wt("cycle", 2), Twenty=wt("Twenty"), fastest=wt("fastest"), decades=wt("decades"),
    By=wt("By"), last=wt("last"), higher2=wt("higher", 2), first=wt("first"),
    Final=wt("Final"), score=wt("score"), thirtyfive=wt("thirty-five"), Buy2=wt("Buy"), seventy=wt("seventy"),
    Rate=wt("Rate"), headlines=wt("headlines"), They=wt("They"), exit=wt("exit"), sign=wt("sign"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["thirtyfive"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.4
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Fed1"] - 0.35, "news"), (T["So"] - 0.1, "question"), (T["A"] - 0.12, "guess"),
    (T["The2"] - 0.1, "hidden"), (T["The3"] - 0.1, "rules"), (T["Two1"] - 0.1, "race05"), (T["Then"] - 0.1, "race08"),
    (T["Now"] - 0.1, "strange"), (T["Remember"] - 0.1, "remember"), (T["Final"] - 0.1, "score"), (T["Rate"] - 0.1, "verdict"),
    (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["hot"], 70)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "news":
        k = prog(u, 0, 0.5); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["raise_"], 70) + hop(t, T["December"], 70)
    elif name == "question":
        x = lerp(-300, 700, prog(u, 0, s1 - s0)); moving = True
        lift += hop(t, T["sell1"], 60) + hop(t, T["hikes1"], 80)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["wait"], 60) + hop(t, T["B"], 60) + hop(t, T["hold1"], 70)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift += hop(t, T["one1"], 40)
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell3"], 50) + hop(t, T["buy"], 50)
    elif name == "race05":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift += hop(t, T["Hike"], 60) + hop(t, T["climbing"], 60)
    elif name == "race08":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Hes"], 50) + hop(t, T["crash"], 70)
    elif name == "strange":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["twentynine"], 70) + hop(t, T["thirtytwo"], 50) + hop(t, T["later"], 60)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Twenty"], 40) + hop(t, T["first"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["thirtyfive"], 35) + hop(t, T["seventy"], 45)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["headlines"], 100) + hop(t, T["exit"], 120, 0.55)
    return x, y, px, flip, moving, lift
