T = dict(
    hears=wt("hears"), always=wt("always"), stoploss1=wt("stop-loss"), What=wt("What"), ten1=wt("ten"), whole=wt("whole"), market=wt("market"),
    A=wt("A"), protects=wt("protects"), B=wt("B"), costs=wt("costs"), One=wt("One"), number1=wt("number"), sells1=wt("sells"),
    rule=wt("rule"), sell=wt("sell"), top=wt("top"), buy=wt("buy"), bounce=wt("bounce"),
    Two=wt("Two"), fires=wt("fires"), pulls=wt("pulls"), ahead1=wt("ahead"), Then=wt("Then"), whipsaws=wt("whipsaws"),
    eighteen=wt("eighteen"), sold=wt("sold"), higher1=wt("higher"), Twenty2=wt("Twenty", 2), out1=wt("out"), worst=wt("worst"), bottom=wt("bottom"),
    Ahead=wt("Ahead"), Remember=wt("Remember"), number2=wt("number", 2), Fifteen=wt("Fifteen"), Nine=wt("Nine"), higher2=wt("higher", 2),
    And=wt("And"), twentytwo=wt("twenty-two"), shook=wt("shook"), three=wt("three"),
    Final=wt("Final"), sixtyfive=wt("sixty-five"), seventy=wt("seventy"),
    It=wt("It", 1), softened=wt("softened"), charged=wt("charged"), false=wt("false"), alarm=wt("alarm"),
)
T["rev1"] = T["sixtyfive"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["What"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (T["One"] - 0.1, "clue"),
    (wt("The") - 0.1, "rules"), (T["Two"] - 0.1, "crash"), (T["Then"] - 0.1, "whip"), (T["Twenty2"] - 0.1, "y2020"),
    (T["Remember"] - 0.1, "remember"), (T["And"] - 0.1, "y2022"), (T["Final"] - 0.1, "score"),
    (T["It"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["stoploss1"], 80) if tl < 4 else 0)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "question":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ten1"], 60) + hop(t, T["whole"], 50)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell"], 45) + hop(t, T["buy"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["fires"], 40) + hop(t, T["ahead1"], 50)
    elif name == "whip":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift = 0
    elif name == "y2020":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["bottom"], 40) + hop(t, T["Ahead"], 70)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Fifteen"], 50) + hop(t, T["Nine"], 50)
    elif name == "y2022":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["three"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; y = 1380
        lift += hop(t, T["sixtyfive"], 35) + hop(t, T["seventy"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["softened"], 90) + hop(t, T["false"], 110, 0.55)
    return x, y, px, flip, moving, lift
