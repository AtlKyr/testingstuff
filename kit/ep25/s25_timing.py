T = dict(
    worst=wt("worst"), timer=wt("timer"), Every=wt("Every"), highest=wt("highest"), Does=wt("Does"), money=wt("money"),
    A=wt("A"), yes=wt("yes"), B=wt("B"), no=wt("no"), One=wt("One"), habit=wt("habit"), hides=wt("hides"),
    He=wt("He"), invests=wt("invests"), thousand1=wt("thousand"), twenty1=wt("twenty"), years=wt("years"), twin=wt("twin"), lowest=wt("lowest"),
    Two=wt("Two"), exact=wt("exact"), top=wt("top"), January=wt("January"), top2=wt("top", 2), again=wt("again"),
    By=wt("By"), March=wt("March"), down=wt("down"), half=wt("half"), twin2=wt("twin", 2), bottom=wt("bottom"),
    Then=wt("Then"), first=wt("first"), right=wt("right"), drop=wt("drop"), Remember=wt("Remember"), never=wt("never"),
    sold=wt("sold"), Not=wt("Not"), eight2=wt("eight", 2), Not2=wt("Not", 2), twenty3=wt("twenty", 3),
    Final=wt("Final"), Perfect=wt("Perfect"), ninetysix=wt("ninety-six"), Worst=wt("Worst"), seventythree=wt("seventy-three"),
    Worst2=wt("Worst", 2), ever=wt("ever"), still2=wt("still", 2), tripled=wt("tripled"), money2=wt("money", 2),
)
T["rev1"] = T["ninetysix"] + 0.1
T["rev2"] = T["seventythree"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Every"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (T["One"] - 0.1, "clue"),
    (T["He"] - 0.1, "rules"), (T["Two"] - 0.1, "y2007"), (T["By"] - 0.1, "y2009"), (T["Then"] - 0.1, "y2022"),
    (T["Remember"] - 0.1, "remember"), (T["Final"] - 0.1, "score"),
    (T["Worst2"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["worst"], 80) if tl < 4 else 0)
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
        lift += hop(t, T["highest"], 60) + hop(t, T["money"], 50)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["thousand1"], 45) + hop(t, T["lowest"], 45)
    elif name == "y2007":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["top"], 40) + hop(t, T["again"], 50)
    elif name == "y2009":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift = 0
    elif name == "y2022":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["first"], 40) + hop(t, T["drop"], 50)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["never"], 50) + hop(t, T["sold"], 60)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; y = 1380
        lift += hop(t, T["ninetysix"], 35) + hop(t, T["seventythree"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ever"], 90) + hop(t, T["tripled"], 110, 0.55)
    return x, y, px, flip, moving, lift
