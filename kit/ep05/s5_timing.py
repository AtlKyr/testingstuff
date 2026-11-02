T = dict(
    seventeen=wt("Seventeen"), up=wt("up"), skipped=wt("skipped"), single=wt("single"), this2=wt("This", 2),
    table=wt("table"), may=wt("May", 1), away=wt("away"), rules=wt("The", 1), sell=wt("sell", 1), buy1=wt("Buy", 1),
    cash1=wt("Cash", 1), twenty=wt("Twenty", 1), ten=wt("ten", 1), fees1=wt("fees", 1), and1=wt("And", 1), dodged=wt("dodged"),
    crash=wt("crash"), summer08=wt("Summer", 1), t29=wt("twenty-nine"), cash2=wt("cash", 1), worst=wt("Worst"),
    t36=wt("thirty-six"), f55=wt("fifty-five"), but=wt("But"), winters=wt("Winters"), three=wt("three"), times=wt("times"),
    summers2=wt("Summers", 1), doubled=wt("doubled"), skip=wt("Skip"), half=wt("half"), final=wt("Final"),
    t35=wt("thirty-five"), buy2=wt("Buy", 2), s71=wt("seventy-one"), flip=wt("Flip"), nineteen=wt("Nineteen"),
    real1=wt("real", 1), and2=wt("And", 2), fees2=wt("fees", 2), two2=wt("two", 2), year=wt("year"),
    verdict=wt("Verdict"), real2=wt("real", 2), bad=wt("Bad"), trade=wt("trade"), follow=wt("Follow"),
)
SCENES = [
    (0.0, "hook"), (T["this2"] - 0.12, "title"), (T["rules"] - 0.1, "rules"), (T["twenty"] - 0.1, "test"),
    (T["and1"] - 0.1, "crash"), (T["worst"] - 0.1, "drawdown"), (T["but"] - 0.1, "problem"), (T["summers2"] - 0.1, "summers"),
    (T["final"] - 0.1, "score"), (T["flip"] - 0.1, "flip"), (T["verdict"] - 0.08, "verdict"), (T["follow"] - 0.12, "outro"),
]
BOUNDS = [s for s, _ in SCENES[1:]]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1310, False, False, idle(t - s0), 40
    if name == "hook":
        k = prog(u, 0, 0.5); x = lerp(-200, 40, ease(k)); moving = k < 1
        lift += hop(t, T["up"], 130) + hop(t, T["skipped"], 150, 0.55)
    elif name == "title":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["table"], 110) + hop(t, T["away"], 130)
    elif name == "rules":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sell"], 110) + hop(t, T["buy1"], 110) + hop(t, T["cash1"], 120)
    elif name == "test":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["ten"], 110)
    elif name == "crash":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["t29"], 140) + hop(t, T["cash2"], 120)
    elif name == "drawdown":
        x = 40 + (math.sin(u * 1.5 - 1.57) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.5 - 1.57) < 0
        lift += hop(t, T["t36"], 120) + hop(t, T["f55"], 120)
    elif name == "problem":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["three"], 150)
    elif name == "summers":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["doubled"], 130) + hop(t, T["half"], 160, 0.55)
    elif name == "score":
        x = 40 + (math.sin(u * 1.3) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.3) < 0
        lift += hop(t, T["t35"], 120) + hop(t, T["s71"], 140)
    elif name == "flip":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["nineteen"], 120) + hop(t, T["real1"], 140) + hop(t, T["two2"], 100)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-300, 40, ease(k)); moving = k < 1
        lift += hop(t, T["real2"], 120) + hop(t, T["trade"], 170, 0.6)
    elif name == "outro":
        px = 24; x = 20; y = lerp(1950, 1290, back(prog(u, 0, 0.6))); lift = abs(math.sin(u * 3.0)) * 40 if u > 0.8 else 0
    return x, y, px, flip, moving, lift
