T = dict(
    Its=wt("It's"), Monday1=wt("Monday"), supposedly=wt("supposedly"), worst1=wt("worst"), stocks=wt("stocks"),
    What=wt("What"), skipped=wt("skipped"), Monday2=wt("Monday", 2), A=wt("A"), beat=wt("beat"), market=wt("market"),
    B=wt("B"), fall=wt("fall"), behind1=wt("behind"), Guess=wt("Guess"), answer=wt("answer"), hides=wt("hides"),
    one1=wt("one"), Monday3=wt("Monday", 3), Rule=wt("Rule"), sell=wt("sell"), Fridays=wt("Friday's"), buy=wt("buy"),
    Mondays_=wt("Monday's"), Two1=wt("Two"), eight1=wt("eight"), Mondays=wt("Mondays"), lose=wt("lose"), ten=wt("ten"),
    skipper1=wt("skipper"), dodges=wt("dodges"), still1=wt("still"), trails=wt("trails"), Tw20=wt("Twenty"),
    worst2=wt("worst", 2), Monday4=wt("Monday", 4), Dodged=wt("Dodged"), Still2=wt("Still"), behind2=wt("behind", 2),
    Tw22=wt("Twenty", 2), t22=wt("twenty-two"), same=wt("same"), story=wt("story"), Remember=wt("Remember"),
    one2=wt("one", 2), Monday5=wt("Monday", 5), October=wt("October"), thirteenth=wt("thirteenth"), eight2=wt("eight", 2),
    Plus=wt("Plus"), fourteen=wt("fourteen"), best=wt("best"), years2=wt("years", 2), skipper2=wt("skipper", 2),
    missed=wt("missed"), Final=wt("Final"), score=wt("score"), t23=wt("twenty-three"), Just=wt("Just"), holding=wt("holding"),
    seventy=wt("seventy"), Even=wt("Even"), zero=wt("zero"), fees=wt("fees"), skipping1=wt("skipping"), lost=wt("lost"),
    Monday6=wt("Monday", 7), never=wt("never"), problem=wt("problem"), Skipping2=wt("Skipping"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["t23"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["zero"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["supposedly"] - 0.1, "monday"), (T["A"] - 0.12, "guess"), (T["answer"] - 0.12, "hidden"),
    (T["Rule"] - 0.1, "rules"), (T["Two1"] - 0.1, "race08"), (T["Tw20"] - 0.1, "race20"), (T["Remember"] - 0.1, "remember"),
    (T["Final"] - 0.1, "score"), (T["Monday6"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["Monday1"], 60)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "monday":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["worst1"], 70) + hop(t, T["skipped"], 70)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["beat"], 60) + hop(t, T["fall"], 70) + hop(t, T["Guess"], 70)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift += hop(t, T["one1"], 40)
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell"], 50) + hop(t, T["buy"], 50)
    elif name == "race08":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift += hop(t, T["ten"], 60) + hop(t, T["trails"], 60)
    elif name == "race20":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Monday4"], 60) + hop(t, T["Dodged"], 60) + hop(t, T["same"], 60)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["thirteenth"], 70) + hop(t, T["fourteen"], 90) + hop(t, T["missed"], 70)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["t23"], 35) + hop(t, T["seventy"], 45) + hop(t, T["zero"], 25)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["never"], 100) + hop(t, T["Skipping2"], 120, 0.55)
    return x, y, px, flip, moving, lift
