T = dict(
    two=wt("Two", 1), trades=wt("trades"), market=wt("market"), out1=wt("out", 1), in1=wt("in", 1),
    this=wt("This"), table=wt("table"), macd1=wt("MACD", 1), crossover=wt("crossover"), twelve=wt("Twelve", 1),
    t26=wt("twenty-six", 1), nine=wt("nine"), rules=wt("The", 1), macd2=wt("MACD", 2), above=wt("above"), signal=wt("signal"),
    buy1=wt("Buy", 1), crosses=wt("Crosses"), below=wt("below"), sell=wt("Sell"),
    twenty=wt("Twenty", 1), ten=wt("ten"), fees1=wt("fees"),
    good=wt("Good"), dodged=wt("dodged"), covid=wt("Covid"), four=wt("four"), t34=wt("thirty-four"),
    worst=wt("Worst"), t26b=wt("twenty-six", 2), f55=wt("fifty-five"),
    bad=wt("bad"), the2=wt("The", 2), win=wt("Win"), f47=wt("forty-seven"),
    In=wt("In"), cash=wt("cash"), half1=wt("half", 1), half2=wt("half", 2), grew=wt("grew"), eight=wt("eight"),
    the3=wt("The", 3), held=wt("held"), seven2=wt("seven", 2),
    final=wt("Final"), t22=wt("twenty-two"), buy2=wt("Buy", 2), s73=wt("seventy-three"),
    It=wt("It"), beat=wt("beat"), three=wt("three"), twenty_l=wt("twenty"),
    fees2=wt("Fees"), side=wt("side"), twelve2=wt("Twelve", 2), twenty2=wt("Twenty", 2), seventeen=wt("seventeen"),
    dollars2=wt("dollars", 2), verdict=wt("Verdict"), shield=wt("shield"), not_=wt("not"), machine=wt("machine"),
    follow=wt("Follow"),
)
SCENES = [
    (0.0, "hook"), (T["this"] - 0.12, "title"), (T["rules"] - 0.1, "rules"), (T["twenty"] - 0.1, "test"),
    (T["good"] - 0.1, "crash"), (T["worst"] - 0.1, "drawdown"), (T["the2"] - 0.1, "bad"), (T["In"] - 0.1, "cash"),
    (T["final"] - 0.1, "score"), (T["It"] - 0.1, "years"), (T["fees2"] - 0.1, "fees"), (T["verdict"] - 0.08, "verdict"),
    (T["follow"] - 0.12, "outro"),
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
        lift += hop(t, T["trades"], 140) + hop(t, T["out1"], 150, 0.55) + hop(t, T["in1"], 120)
    elif name == "title":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["table"], 110) + hop(t, T["twelve"], 90, 0.35) + hop(t, T["t26"], 100, 0.35) + hop(t, T["nine"], 120, 0.4)
    elif name == "rules":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["buy1"], 130) + hop(t, T["sell"], 130)
    elif name == "test":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["ten"], 110) + hop(t, T["fees1"], 90)
    elif name == "crash":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["four"], 60) + hop(t, T["t34"], 55)
    elif name == "drawdown":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift += hop(t, T["t26b"], 120) + hop(t, T["f55"], 130)
    elif name == "bad":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["f47"], 150, 0.55)
    elif name == "cash":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["eight"], 140) + hop(t, T["seven2"], 170, 0.6)
    elif name == "score":
        x = 40 + (math.sin(u * 1.3) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.3) < 0
        lift += hop(t, T["t22"], 120) + hop(t, T["s73"], 140)
    elif name == "years":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["three"], 90)
    elif name == "fees":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["twelve2"], 130) + hop(t, T["seventeen"], 150)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["shield"], 120) + hop(t, T["machine"], 170, 0.6)
    elif name == "outro":
        px = 24; x = 20; y = lerp(1950, 1290, back(prog(u, 0, 0.6))); lift = abs(math.sin(u * 3.0)) * 40 if u > 0.8 else 0
    return x, y, px, flip, moving, lift
