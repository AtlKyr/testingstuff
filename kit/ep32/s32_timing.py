T = dict(
    Five=wt("Five"), red1=wt("red"), days1=wt("days"), fortythree=wt("forty-three"), times1=wt("times"),
    It1=wt("It"), happened=wt("happened"), again=wt("again"), Sell=wt("Sell"), A=wt("A"), sit=wt("sit"), B=wt("B"),
    The1=wt("The"), clue=wt("clue"), six1=wt("six"), rule=wt("rule"), fifth=wt("fifth"), sell=wt("sell"), wait=wt("wait"),
    month=wt("month"), In=wt("In"), eight=wt("eight"), sneaks=wt("sneaks"), ahead=wt("ahead"), Then=wt("Then"),
    bounces=wt("bounces"), Streak=wt("Streak"), climbs=wt("climbs"), By=wt("By"), ten=wt("ten"), gone=wt("gone"),
    Twenty=wt("Twenty"), sells=wt("sells"), crash=wt("crash"), rebuys=wt("rebuys"), lower=wt("lower"), catch=wt("catch"),
    Remember=wt("Remember"), six2=wt("six", 2), After=wt("After"), green=wt("green"), twentyseven=wt("twenty-seven"),
    fortythree2=wt("forty-three", 2), It3=wt("It", 3), usually=wt("usually"), bounce=wt("bounce"), Now=wt("Now"),
    scoreboard=wt("scoreboard"), seller2=wt("seller", 2), forty=wt("forty"), Sitting=wt("Sitting"), seventy=wt("seventy"),
    Five2=wt("Five", 2), warning=wt("warning"), Mostly=wt("Mostly"), discount=wt("discount"),
)
T["rev1"] = T["forty"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["It1"] - 0.1, "question"), (T["Sell"] - 0.12, "guess"), (T["The1"] - 0.12, "clue"),
    (T["rule"] - 0.25, "rules"), (T["In"] - 0.1, "crash"), (T["Then"] - 0.1, "bounces"), (T["Twenty"] - 0.1, "y2020"),
    (T["Remember"] - 0.1, "remember"), (T["Now"] - 0.15, "score"), (T["Five2"] - 0.15, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    # frame 0: big, facing the viewer, already hopping (first 0.3 s)
    px = 24; x = 600 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["fortythree"], 80) + hop(tl, T["times1"], 50) if tl < 4 else 0)
    return x, y, px, False, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "question":
        k = prog(u, 0, 0.4); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["again"], 60)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["sell"], 45) + hop(t, T["month"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sneaks"], 50)
    elif name == "bounces":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "y2020":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["rebuys"], 40) + hop(t, T["catch"], 40)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["twentyseven"] - 0.2:
            x = 40; moving = False; lift = idle(u) + hop(t, T["twentyseven"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["forty"], 35) + hop(t, T["seventy"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["warning"], 80) + hop(t, T["discount"], 100, 0.55)
    return x, y, px, flip, moving, lift
