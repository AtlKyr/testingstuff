T = dict(
    two=wt("Two"), traders=wt("traders"), market1=wt("market", 1), open1=wt("open"), other=wt("The", 1), sleep=wt("sleep"),
    guess=wt("Guess"), wins=wt("wins"), answer=wt("answer"), tiny1=wt("tiny", 1), number1=wt("number", 1),
    day1=wt("Day", 1), buys=wt("buys"), bell=wt("bell"), sells=wt("sells"), close=wt("close"), night1=wt("Night", 1),
    opposite=wt("opposite"), twenty1=wt("Twenty"), spy=wt("SPY"), ten=wt("ten"), each=wt("each"),
    y2008=wt("Two", 2), eight1=wt("eight", 1), crash=wt("crash"), daylight=wt("daylight"), night2=wt("Night", 2), ahead=wt("ahead"),
    then=wt("Then"), covid=wt("Covid"), overnight=wt("overnight"),
    but=wt("But"), t24=wt("twenty-four"), most=wt("most"), gains=wt("gains"), closed=wt("closed"),
    now=wt("Now"), tiny2=wt("tiny", 2), point=wt("Point"), percent=wt("percent"), the3=wt("The", 3), fee=wt("fee"),
    paid=wt("Paid"), twice=wt("twice"), five2=wt("five", 2), days=wt("days"),
    final=wt("Final"), score=wt("score"), day2=wt("Day", 2), n97=wt("ninety-seven"), night3=wt("Night", 3), three=wt("three"),
    eight2=wt("eight", 2), buy=wt("Buy"), hold=wt("hold"), seventy=wt("seventy"),
    And=wt("And"), zero2=wt("zero", 2), fees=wt("fees"), night4=wt("Night", 4), still=wt("still"), f47=wt("forty-seven"),
    verdict=wt("Verdict"), pays=wt("pays"), night5=wt("night"), only=wt("Only"), holders=wt("holders"), collect=wt("collect"),
)
T["follow"] = END + 0.45
SCENES = [
    (0.0, "hook"), (T["other"] - 0.1, "night"), (T["answer"] - 0.1, "case"), (T["day1"] - 0.1, "rules"),
    (T["twenty1"] - 0.1, "start"), (T["y2008"] - 0.1, "crash08"), (T["then"] - 0.1, "covid"), (T["but"] - 0.1, "closed"),
    (T["now"] - 0.1, "tiny"), (T["the3"] - 0.1, "fees"), (T["final"] - 0.1, "score"), (T["buy"] - 0.1, "holder"),
    (T["And"] - 0.1, "zerofee"), (T["verdict"] - 0.1, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    # big detective close-up, already on screen at frame 0, hops at t=0 and on key words
    px = 24; x = 270 + math.sin(tl * 1.6) * 30; y = 1290
    lift = idle(tl) + hop(tl, -0.05, 120, 0.45) + hop(tl, T["open1"], 90) + hop(tl, T["traders"], 70)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1310, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "night":
        k = prog(u, 0, 0.7); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift = (idle(u) * 0.2 if t < T["guess"] else idle(u)) + hop(t, T["guess"], 150) + hop(t, T["wins"], 90)
    elif name == "case":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["tiny1"], 120) + hop(t, T["number1"], 80)
    elif name == "rules":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5)))
        lift += hop(t, T["buys"], 90) + hop(t, T["sells"], 90) + hop(t, T["night1"], 110) + hop(t, T["opposite"], 80)
    elif name == "start":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["ten"], 110) + hop(t, T["each"], 160, 0.55)
    elif name == "crash08":
        k = prog(u, 0, 0.7); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["daylight"], 55) + hop(t, T["ahead"], 60)
    elif name == "covid":
        k = prog(u, 0, 0.6); x = lerp(-450, 30, ease(k)); moving = k < 1
        lift += hop(t, T["overnight"], 60)
    elif name == "closed":
        x = 40 + (math.sin(u * 1.5 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.5 - 1.57) < 0
        lift += hop(t, T["gains"], 50) + hop(t, T["closed"], 60)
    elif name == "tiny":
        k = prog(u, 0, 0.6); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["point"], 120) + hop(t, T["percent"], 90)
    elif name == "fees":
        x = 40 + (math.sin(u * 1.7) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.7) < 0
        lift += hop(t, T["twice"], 110) + hop(t, T["days"], 130)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["n97"], 120) + hop(t, T["three"], 120) + hop(t, T["eight2"], 80)
    elif name == "holder":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.45)))
        lift += hop(t, T["seventy"], 170, 0.55)
    elif name == "zerofee":
        k = prog(u, 0, 0.6); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["zero2"], 100) + hop(t, T["f47"], 140)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["pays"], 120) + hop(t, T["holders"], 150, 0.55)
    return x, y, px, flip, moving, lift
