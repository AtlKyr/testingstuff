T = dict(
    Nasdaq=wt("Nasdaq"), percent1=wt("percent"), bell=wt("bell"), Red=wt("Red"), morning1=wt("morning"), Sit=wt("Sit"), A=wt("A"),
    hold=wt("hold"), B=wt("B"), trap=wt("trap"), next1=wt("next"), rule=wt("rule"), opens=wt("opens"), lower=wt("lower"),
    sell2=wt("sell"), buy=wt("buy"), next2=wt("next", 2), Two=wt("Two"), thirtyone=wt("thirty-one"), dodges=wt("dodges"),
    eleven=wt("eleven"), ahead=wt("ahead"), Then=wt("Then"), flips=wt("flips"), Every=wt("Every"), scare=wt("scare"),
    steps=wt("steps"), Remember=wt("Remember"), More=wt("More"), half=wt("half"), higher=wt("higher"), sold1=wt("sold"),
    One=wt("One"), Friday=wt("Friday"), October=wt("October"), sold2=wt("sold", 2), Monday=wt("Monday"), paid=wt("paid"),
    eight2=wt("eight", 3), Final=wt("Final"), Just=wt("Just"), seventy=wt("seventy"), Sitting=wt("Sitting"),
    fiftyone=wt("fifty-one"), Even=wt("Even"), zero=wt("zero"), loses=wt("loses"), Red2=wt("Red", 2), hurt=wt("hurt"),
    Leaving=wt("Leaving"),
)
T["rev1"] = T["seventy"] + 0.1
T["rev2"] = T["fiftyone"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Red"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (T["trap"] - 0.25, "clue"),
    (T["rule"] - 0.15, "rules"), (T["Two"] - 0.1, "crash"), (T["Then"] - 0.1, "flip"),
    (T["Remember"] - 0.1, "remember"), (T["One"] - 0.1, "oct08"), (T["Final"] - 0.1, "score"),
    (T["Even"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["percent1"], 80) if tl < 4 else 0)
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
        lift += hop(t, T["morning1"], 60)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell2"], 45) + hop(t, T["buy"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["thirtyone"], 40) + hop(t, T["ahead"], 50)
    elif name == "flip":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["flips"], 40) + hop(t, T["steps"], 40)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift = 0
    elif name == "oct08":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Monday"], 40) + hop(t, T["eight2"], 60)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["seventy"], 35) + hop(t, T["fiftyone"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["hurt"], 90) + hop(t, T["Leaving"], 110, 0.55)
    return x, y, px, flip, moving, lift
