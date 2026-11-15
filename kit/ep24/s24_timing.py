T = dict(
    gauge=wt("gauge"), seventy=wt("seventy"), day=wt("day"), When=wt("When"), spikes=wt("spikes"), sell=wt("sell"), A=wt("A"),
    sit=wt("sit"), B=wt("B"), trap=wt("trap"), way=wt("way"), back1=wt("back"), rule=wt("rule"), thirty=wt("thirty"), sell2=wt("sell", 2),
    Back=wt("Back"), twenty1=wt("twenty"), buy=wt("buy"), Two=wt("Two"), dodges=wt("dodges"), crash1=wt("crash"), pulls=wt("pulls"),
    ahead=wt("ahead"), But=wt("But"), stays=wt("stays"), buys=wt("buys"), late=wt("late"), same=wt("same"), price=wt("price"),
    rebound=wt("rebound"), missed=wt("missed"), Then=wt("Then"), twenty2=wt("twenty", 2), sells=wt("sells"), Covid=wt("Covid"),
    bottom=wt("bottom"), Then2=wt("Then", 2), waits=wt("waits"), calm=wt("calm"), Remember=wt("Remember"), Fear1=wt("Fear"),
    stayed=wt("stayed"), year=wt("year"), bought=wt("bought"), thirtynine=wt("thirty-nine"), higher=wt("higher"),
    Final=wt("Final"), Sit=wt("Sit"), seventy2=wt("seventy", 2), Fear2=wt("Fear", 2), twentytwo=wt("twenty-two"),
    Selling=wt("Selling"), safe=wt("safe"), Buying=wt("Buying"), trap2=wt("trap", 2),
)
T["rev1"] = T["seventy2"] + 0.1
T["rev2"] = T["twentytwo"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["When"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (wt("The") - 0.1, "clue"),
    (wt("The", 2) - 0.1, "rules"), (T["Two"] - 0.1, "crash"), (T["But"] - 0.1, "rebuy"), (T["Then"] - 0.1, "y2020"),
    (T["Remember"] - 0.1, "remember"), (T["Final"] - 0.1, "score"),
    (T["Selling"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["seventy"], 80) if tl < 4 else 0)
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
        lift += hop(t, T["spikes"], 60) + hop(t, T["sell"], 50)
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
        lift += hop(t, T["dodges"], 40) + hop(t, T["ahead"], 50)
    elif name == "rebuy":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift = 0
    elif name == "y2020":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["sells"], 40) + hop(t, T["bottom"], 50)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["year"], 50) + hop(t, T["thirtynine"], 60)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; y = 1380
        lift += hop(t, T["seventy2"], 35) + hop(t, T["twentytwo"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["safe"], 90) + hop(t, T["trap2"], 110, 0.55)
    return x, y, px, flip, moving, lift
