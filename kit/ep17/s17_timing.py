T = dict(
    Everyones=wt("Everyone's"), seven1=wt("seven"), again=wt("again"), Say=wt("Say"), exact=wt("exact"), top1=wt("top"),
    October=wt("October"), How=wt("How"), long=wt("long"), even1=wt("even"), A=wt("A"), under=wt("under"), B=wt("B"),
    over1=wt("over"), years2=wt("years", 2), One1=wt("One"), forget=wt("forget"), decides=wt("decides"),
    Two1=wt("Two"), investors=wt("investors"), One2=wt("One", 2), holds=wt("holds"), The1=wt("The"), sells1=wt("sells"),
    forty1=wt("forty"), comes=wt("comes"), record=wt("record"), Two2=wt("Two", 2), eight=wt("eight"), Down=wt("Down"),
    sells2=wt("sells", 2), Then=wt("Then"), waits1=wt("waits"), waits2=wt("waits", 2), Heres=wt("Here's"), strange=wt("strange"),
    double=wt("double"), sold=wt("sold"), Remember=wt("Remember"), forgotten=wt("forgotten"), Dividends=wt("Dividends"),
    With=wt("With"), four=wt("four"), half=wt("half"), Without=wt("Without"), five3=wt("five", 3),
    Final=wt("Final"), score=wt("score"), panic=wt("panic"), twentysix=wt("twenty-six"), fiftytwo=wt("fifty-two"),
    Buying=wt("Buying"), hurt1=wt("hurt"), Selling=wt("Selling"), bottom=wt("bottom"), twice=wt("twice"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["twentysix"] + 0.1
T["rev2"] = T["fiftytwo"] + 0.1
T["rev3"] = T["rev2"] + 0.4
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Say"] - 0.1, "top"), (T["How"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (T["One1"] - 0.1, "hidden"),
    (T["Two1"] - 0.1, "rules"), (T["Two2"] - 0.1, "crash"), (T["Then"] - 0.1, "waits"), (T["Heres"] - 0.1, "strange"),
    (T["Remember"] - 0.1, "remember"), (T["Final"] - 0.1, "score"), (T["Buying"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["seven1"], 70)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "top":
        k = prog(u, 0, 0.5); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["top1"], 80) + hop(t, T["October"], 60)
    elif name == "question":
        x = lerp(-300, 700, prog(u, 0, s1 - s0)); moving = True
        lift += hop(t, T["long"], 60) + hop(t, T["even1"], 70)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["under"], 60) + hop(t, T["B"], 60) + hop(t, T["years2"], 70)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift += hop(t, T["forget"], 40)
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["holds"], 50) + hop(t, T["sells1"], 50)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Down"], 50) + hop(t, T["sells2"], 70)
    elif name == "waits":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        if t > T["waits1"]:
            lift = abs(math.sin(u * 1.2)) * 6
    elif name == "strange":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift += hop(t, T["double"], 70) + hop(t, T["sold"], 50)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Dividends"], 40) + hop(t, T["half"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["twentysix"], 35) + hop(t, T["fiftytwo"], 45)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["hurt1"], 100) + hop(t, T["twice"], 120, 0.55)
    return x, y, px, flip, moving, lift
