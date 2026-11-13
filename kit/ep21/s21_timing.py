T = dict(
    Friday1=wt("Friday"), thirteenth1=wt("thirteenth"), supposedly=wt("supposedly"), unluckiest=wt("unluckiest"), What=wt("What"),
    skipped=wt("skipped"), every=wt("every"), market1=wt("market"), A=wt("A"), dodges=wt("dodges"), luck=wt("luck"), B=wt("B"),
    holder1=wt("holder"), wins=wt("wins"), But=wt("But"), Friday3=wt("Friday", 3), answer=wt("answer"), The1=wt("The"),
    sell=wt("sell"), Thursdays=wt("Thursday's"), buy=wt("buy"), Fridays=wt("Friday's"), Thirtyfive=wt("Thirty-five"),
    years=wt("years"), Through=wt("Through"), nine=wt("nine"), neck1=wt("neck"), And2=wt("And"), unlucky=wt("unlucky"),
    Twenty=wt("Twenty"), thirtyfive2=wt("thirty-five"), up=wt("up"), Remember=wt("Remember"), March=wt("March"),
    Covid=wt("Covid"), jumped=wt("jumped"), eight=wt("eight", 2), percent=wt("percent"), skipper3=wt("skipper", 3), out=wt("out"),
    From=wt("From"), gap=wt("gap"), closed=wt("closed"), Final=wt("Final"), sixty=wt("sixty"), seventy=wt("seventy"),
    Superstition=wt("Superstition"), ten=wt("ten"), dollars=wt("dollars"),
)
T["themarket"] = T["jumped"] - 0.45
T["rev1"] = T["sixty"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.6
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["supposedly"] - 0.1, "unlucky"), (T["What"] - 0.1, "whatif"), (T["A"] - 0.12, "guess"), (T["But"] - 0.1, "clue"),
    (T["The1"] - 0.15, "rules"), (T["Thirtyfive"] - 0.1, "count"), (T["Through"] - 0.1, "neck"), (T["And2"] - 0.1, "updays"),
    (T["Remember"] - 0.1, "remember"), (T["themarket"] - 0.1, "jump"), (T["From"] - 0.1, "gap"), (T["Final"] - 0.1, "score"),
    (T["Superstition"] - 0.1, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 600 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["thirteenth1"], 80)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "unlucky":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["unluckiest"], 60)
    elif name == "whatif":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["skipped"], 60) + hop(t, T["every"], 50)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["dodges"], 40) + hop(t, T["wins"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell"], 45) + hop(t, T["buy"], 45)
    elif name == "count":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Thirtyfive"], 50)
    elif name == "neck":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift = 0
    elif name == "updays":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Twenty"], 50) + hop(t, T["up"], 60)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["March"], 60) + hop(t, T["Covid"], 50)
    elif name == "jump":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["eight"], 70)
    elif name == "gap":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["gap"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["sixty"], 35) + hop(t, T["seventy"], 40)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Superstition"], 90) + hop(t, T["ten"], 110, 0.55)
    return x, y, px, flip, moving, lift
