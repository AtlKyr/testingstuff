T = dict(
    winners=wt("Winners"), twice=wt("twice"), losers=wt("losers"), every=wt("Every"), book=wt("book's"), dream=wt("dream"),
    still=wt("still"), crushed=wt("crushed"),
    this=wt("This"), table=wt("table"), turtle1=wt("Turtle", 1), breakout=wt("breakout"),
    rules=wt("The", 1), above=wt("above"), high=wt("high"), buy1=wt("Buy", 1), below=wt("below"), low1=wt("low", 1), sell=wt("Sell"),
    twenty=wt("Twenty"), ten=wt("ten"), fees1=wt("fees"),
    e85=wt("Eighty-five"), trades=wt("trades"), win=wt("Win"), f56=wt("fifty-six"), half1=wt("half", 1),
    covid1=wt("Covid", 1), four=wt("four"), t34=wt("thirty-four"),
    worst=wt("Worst"), t27=wt("twenty-seven"), f55=wt("fifty-five", 1),
    catch=wt("The", 2), only=wt("only"), breakouts=wt("breakouts"),
    after=wt("After"), covid2=wt("Covid", 2), low2=wt("low", 2), waited=wt("waited"), three=wt("three"), weeks=wt("weeks"),
    market1=wt("market", 1), bounced=wt("bounced"), t24=wt("twenty-four"),
    And=wt("And"), sat=wt("sat"), cash=wt("cash"), half2=wt("half", 2), market2=wt("market", 2), doubled=wt("doubled"),
    final=wt("Final"), turtle2=wt("Turtle", 2), thirty=wt("thirty"), buy2=wt("Buy", 2), s71=wt("seventy-one"),
    original=wt("The", 4), f55b=wt("fifty-five", 2), version=wt("version"), seventeen=wt("Seventeen"),
    fees2=wt("Fees"), side=wt("side"), t23=wt("Twenty-three"),
    verdict=wt("Verdict"), seatbelt=wt("seatbelt"), slow=wt("slow"), engine=wt("engine"),
    follow=wt("Follow"),
)
SCENES = [
    (0.0, "hook"), (T["this"] - 0.12, "title"), (T["rules"] - 0.1, "rules"), (T["twenty"] - 0.1, "test"),
    (T["e85"] - 0.1, "stats"), (T["covid1"] - 0.1, "crash"), (T["worst"] - 0.1, "drawdown"), (T["catch"] - 0.1, "catch"),
    (T["after"] - 0.1, "rebound"), (T["And"] - 0.1, "cash"), (T["final"] - 0.1, "score"), (T["original"] - 0.1, "original"),
    (T["fees2"] - 0.1, "fees"), (T["verdict"] - 0.08, "verdict"), (T["follow"] + 0.1, "outro"),
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
        lift += hop(t, T["twice"], 150) + hop(t, T["losers"], 110) + hop(t, T["crushed"], 160, 0.55)
    elif name == "title":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["table"], 110) + hop(t, T["turtle1"], 130)
    elif name == "rules":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["buy1"], 130) + hop(t, T["sell"], 130)
    elif name == "test":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["ten"], 110) + hop(t, T["fees1"], 90)
    elif name == "stats":
        x = 40 + (math.sin(u * 1.5 - 1.57) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.5 - 1.57) < 0
        lift += hop(t, T["e85"], 120) + hop(t, T["f56"], 150)
    elif name == "crash":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["four"], 60) + hop(t, T["t34"], 55)
    elif name == "drawdown":
        x = 40 + (math.sin(u * 1.6 + 1.57) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6 + 1.57) < 0
        lift += hop(t, T["t27"], 120) + hop(t, T["f55"], 130)
    elif name == "catch":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["breakouts"], 140)
    elif name == "rebound":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["three"], 90) + hop(t, T["t24"], 120)
    elif name == "cash":
        k = prog(u, 0, 0.8); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift = (idle(u) * 0.3 if t < T["market2"] else idle(u)) + hop(t, T["doubled"], 150, 0.6)
    elif name == "score":
        x = 40 + (math.sin(u * 1.3) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.3) < 0
        lift += hop(t, T["thirty"], 120) + hop(t, T["s71"], 140)
    elif name == "original":
        k = prog(u, 0, 0.7); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["f55b"], 110) + hop(t, T["seventeen"], 150)
    elif name == "fees":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["t23"], 150)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["seatbelt"], 120) + hop(t, T["slow"], 100, 0.6)
    elif name == "outro":
        px = 24; x = 20; y = lerp(1950, 1290, back(prog(u, 0, 0.6))); lift = abs(math.sin(u * 3.0)) * 40 if u > 0.8 else 0
    return x, y, px, flip, moving, lift
