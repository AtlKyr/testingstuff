T = dict(
    hundred0=wt("hundred"), only1=wt("only"), red1=wt("red"), days1=wt("days"), Two1=wt("Two"), five1=wt("five"), month=wt("month"),
    A=wt("A"), arrives=wt("arrives"), B=wt("B"), waits1=wt("waits"), red2=wt("red", 2), percent1=wt("percent"), Who=wt("Who"),
    richer=wt("richer"), quiet1=wt("quiet"), answer=wt("answer"), rule=wt("rule"), paychecks=wt("paychecks"), buying1=wt("buying"),
    Two2=wt("Two", 2), everywhere=wt("everywhere"), B2=wt("B", 2), panic=wt("panic"), cheap=wt("cheap"), ahead=wt("ahead"),
    But=wt("But"), barely=wt("barely"), Then=wt("Then"), calms=wt("calms"), B3=wt("B", 3), waits2=wt("waits", 2),
    waits3=wt("waits", 3), Remember=wt("Remember"), Two3=wt("Two", 3), seventeen=wt("seventeen"), four1=wt("four"),
    His=wt("His"), September=wt("September"), cash=wt("cash"), five2=wt("five", 2), months=wt("months"), bought=wt("bought"),
    fifteen=wt("fifteen"), higher=wt("higher"), Final=wt("Final"), A2=wt("A", 2), ninety=wt("ninety"), B4=wt("B", 4),
    eightyeight=wt("eighty-eight"), Red=wt("Red"), wealth=wt("wealth"), Paydays=wt("Paydays"),
)
T["rev1"] = T["ninety"] + 0.1
T["rev2"] = T["eightyeight"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Two1"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (wt("One") - 0.15, "clue"),
    (wt("The") - 0.1, "rules"), (T["Two2"] - 0.1, "y2008"), (T["Then"] - 0.1, "calm"),
    (T["Remember"] - 0.1, "remember"), (T["His"] - 0.1, "sept"), (T["Final"] - 0.1, "score"),
    (T["Red"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["red1"], 80) if tl < 4 else 0)
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
        lift += hop(t, T["five1"], 60)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["paychecks"], 45) + hop(t, T["buying1"], 45)
    elif name == "y2008":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["cheap"], 40) + hop(t, T["ahead"], 50)
    elif name == "calm":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["waits2"], 30)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift = 0
    elif name == "sept":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["months"], 40) + hop(t, T["fifteen"], 60)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["ninety"], 35) + hop(t, T["eightyeight"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["wealth"], 90) + hop(t, T["Paydays"], 110, 0.55)
    return x, y, px, flip, moving, lift
