T = dict(
    jumped=wt("jumped"), two1=wt("two"), percent1=wt("percent"), Its=wt("Its"), best=wt("best"), April=wt("April"),
    So=wt("So"), chase=wt("chase"), bounce1=wt("bounce"), A=wt("A"), wins=wt("wins"), B=wt("B"), hold1=wt("hold"),
    The2=wt("The", 2), answer=wt("answer"), hides=wt("hides"), one1=wt("one"), number1=wt("number"),
    The3=wt("The", 3), rule=wt("rule"), buy2=wt("buy", 2), jump=wt("jump"), hold2=wt("hold", 2), month=wt("month"),
    Two1=wt("Two"), eight=wt("eight"), Thirty=wt("Thirty"), year=wt("year"), chaser2=wt("chaser", 2), buys=wt("buys"),
    all=wt("all"), sinks=wt("sinks"), anyway=wt("anyway"), Then=wt("Then"), calm=wt("calm"), Stocks=wt("Stocks"),
    climb=wt("climb"), vanish=wt("vanish"), sits=wt("sits"), cash=wt("cash"), Now=wt("Now"), strange=wt("strange"),
    Four=wt("Four"), five=wt("five"), came=wt("came"), already=wt("already"), deep=wt("deep"), hole=wt("hole"),
    Remember=wt("Remember"), number2=wt("number", 2), Two2=wt("Two", 2), three2=wt("three", 2), Thats=wt("That's"),
    whole=wt("whole"), erased=wt("erased"), within=wt("within"), months=wt("months"), Final=wt("Final"), score=wt("score"),
    chaser4=wt("chaser", 4), twenty=wt("twenty"), Buy=wt("Buy"), seventy=wt("seventy"), A2=wt("A", 2), green=wt("green"),
    isnt=wt("isn't"), allclear=wt("all-clear"), Its2=wt("It's"), symptom=wt("symptom"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["twenty"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.4
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Its"] - 0.1, "bestday"), (T["So"] - 0.1, "chase"), (T["A"] - 0.12, "guess"), (T["The2"] - 0.1, "hidden"),
    (T["The3"] - 0.1, "rules"), (T["Two1"] - 0.1, "race08"), (T["Then"] - 0.1, "calm"), (T["Now"] - 0.1, "strange"),
    (T["Remember"] - 0.1, "remember"), (T["Final"] - 0.1, "score"), (T["A2"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["jumped"], 70) + hop(tl, T["two1"], 60)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "bestday":
        k = prog(u, 0, 0.5); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["best"], 80) + hop(t, T["April"], 70)
    elif name == "chase":
        x = lerp(-300, 700, prog(u, 0, s1 - s0)); moving = True
        lift += hop(t, T["chase"], 70) + hop(t, T["bounce1"], 90)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["wins"], 60) + hop(t, T["B"], 60) + hop(t, T["hold1"], 70)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift += hop(t, T["one1"], 40)
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["buy2"], 50) + hop(t, T["hold2"], 50)
    elif name == "race08":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift += hop(t, T["Thirty"], 60) + hop(t, T["sinks"], 60)
    elif name == "calm":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["climb"], 60) + hop(t, T["vanish"], 60)
        if t > T["sits"]:
            lift = abs(math.sin(u * 1.2)) * 6
    elif name == "strange":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Four"], 70) + hop(t, T["already"], 60) + hop(t, T["hole"], 70)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Two2"], 40) + hop(t, T["erased"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["twenty"], 35) + hop(t, T["seventy"], 45)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["allclear"], 100) + hop(t, T["symptom"], 120, 0.55)
    return x, y, px, flip, moving, lift
