T = dict(
    SP=wt("S&P"), fell=wt("fell"), five=wt("five"), record1=wt("record"), Was=wt("Was"), waiting=wt("waiting"), dip1=wt("dip"),
    smart=wt("smart"), A=wt("A"), patient=wt("patient"), waiter1=wt("waiter"), B=wt("B"), buying1=wt("buying"),
    record2=wt("record", 2), highs=wt("highs"), Guess=wt("Guess"), answer=wt("answer"), hides=wt("hides"), one1=wt("one"),
    long1=wt("long"), wait1=wt("wait"), Rule=wt("Rule"), buy=wt("buy"), five2=wt("five", 2), drop=wt("drop"), sell=wt("sell"),
    new=wt("new"), record3=wt("record", 3), Two1=wt("Two"), seven1=wt("seven"), sells=wt("sells"), top=wt("top"),
    buys=wt("buys"), cheaper=wt("cheaper"), leads1=wt("leads"), Two2=wt("Two", 2), eight=wt("eight"), crushes=wt("crushes"),
    both=wt("both"), Tw13=wt("Twenty"), thirteen=wt("thirteen"), records1=wt("records"), everywhere=wt("everywhere"),
    Buy2=wt("Buy"), hold=wt("hold"), catches=wt("catches"), Tw15=wt("Twenty", 2), fifteen=wt("fifteen"), leads2=wt("leads", 2),
    Seventeen=wt("Seventeen"), trades1=wt("trades"), every2=wt("every", 2), winner=wt("winner"),
    Then=wt("Then"), stopped=wt("stopped"), coming=wt("coming"), Remember=wt("Remember"), long2=wt("long", 2), wait2=wt("wait", 2),
    Nineteen=wt("Nineteen"), months=wt("months"), cash=wt("cash"), When=wt("When"), came=wt("came"), prices=wt("prices"),
    higher=wt("higher"), Final=wt("Final"), score=wt("score"), waiter4=wt("waiter", 4), f49=wt("forty-nine"),
    Buying2=wt("Buying"), records2=wt("records", 2), seventy=wt("seventy"), Perfect=wt("Perfect"), still=wt("still"),
    lost=wt("lost"), dip4=wt("dip", 4), never=wt("never"), come=wt("come"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["f49"] + 0.1           # first final number tears off here (>= 75% of runtime)
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["five"] - 0.12, "news"), (T["A"] - 0.12, "guess"), (T["answer"] - 0.12, "hidden"), (T["Rule"] - 0.1, "rules"),
    (T["Two1"] - 0.1, "race07"), (T["Tw13"] - 0.1, "race13"), (T["Then"] - 0.1, "drought"), (T["Nineteen"] - 0.1, "wait"),
    (T["Final"] - 0.1, "score"), (T["Perfect"] - 0.1, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 410 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["five"], 60)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "news":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["five"], 70) + hop(t, T["record1"], 90) + hop(t, T["smart"], 70)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["waiter1"], 70) + hop(t, T["highs"], 80) + hop(t, T["Guess"], 70)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift += hop(t, T["long1"], 40)
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["drop"], 60) + hop(t, T["record3"], 60)
    elif name == "race07":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift += hop(t, T["cheaper"], 60) + hop(t, T["crushes"], 60)
    elif name == "race13":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["everywhere"], 60) + hop(t, T["leads2"], 60) + hop(t, T["Seventeen"], 70) + hop(t, T["winner"], 70)
    elif name == "drought":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Remember"], 90)
    elif name == "wait":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["Nineteen"], 100) + hop(t, T["higher"], 80)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["f49"], 80) + hop(t, T["seventy"], 110)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Perfect"], 100) + hop(t, T["never"], 130, 0.55)
    return x, y, px, flip, moving, lift
