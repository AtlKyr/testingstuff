T = dict(
    The=wt("The"), eight1=wt("eight"), record=wt("record"), Buy=wt("Buy"), A=wt("A"), B=wt("B"), One=wt("One"), tag1=wt("tag"),
    Both=wt("Both"), five=wt("five"), eight2=wt("eight", 2), top=wt("top"), Two=wt("Two"), dip1=wt("dip"), cash=wt("cash"),
    sixteen=wt("sixteen"), Summer=wt("Summer"), dip2=wt("dip", 2), spends=wt("spends"), eight3=wt("eight", 3), crushes=wt("crushes"),
    Heres=wt("Here's"), strange=wt("strange"), After=wt("After"), calms=wt("calms"), waits=wt("waits"), Remember=wt("Remember"),
    He=wt("He"), half=wt("half"), sale1=wt("sale"), paid=wt("paid"), thirtysix=wt("thirty-six"), day=wt("day"), Every=wt("Every"),
    Final=wt("Final"), Then=wt("Then"), ended=wt("ended"), four1=wt("four"), four2=wt("four", 2), The2=wt("The", 2), cost=wt("cost"), eighteen=wt("eighteen"),
)
T["rev1"] = T["four1"] + 0.1
T["rev2"] = T["four2"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Buy"] - 0.12, "guess"), (T["One"] - 0.12, "clue"), (T["Both"] - 0.15, "rules"),
    (T["Two"] - 0.1, "wait"), (T["Summer"] - 0.1, "summer"), (T["Heres"] - 0.12, "calm"), (T["Remember"] - 0.1, "remember"),
    (T["Final"] - 0.15, "score"), (T["The2"] - 0.15, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["eight1"], 80) + hop(tl, T["record"], 50) if tl < 3 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["five"], 45) + hop(t, T["eight2"], 45)
    elif name == "wait":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; lift = (0 if k < 1 else idle(u)) + hop(t, T["sixteen"], 50)
    elif name == "summer":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["dip2"], 60) + hop(t, T["spends"], 50)
    elif name == "calm":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["paid"] - 0.3:
            x = 40; moving = False; lift = idle(u) + hop(t, T["thirtysix"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["cost"], 80) + hop(t, T["eighteen"], 100, 0.55)
    return x, y, px, flip, moving, lift
