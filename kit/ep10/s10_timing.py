T = dict(
    SPY1=wt("SPY"), falls=wt("falls"), three1=wt("three"), days1=wt("days"), row=wt("row"),
    Do=wt("Do"), buy1=wt("buy"), panic1=wt("panic"), just1=wt("just"), hold=wt("hold"), Make=wt("Make"), guess=wt("guess"),
    And1=wt("And"), twenty1=wt("twenty"), years=wt("years"), answer=wt("answer"), flipping=wt("flipping"),
    Rule=wt("Rule"), three2=wt("three", 2), red1=wt("red"), closes=wt("closes"), buy2=wt("buy", 2), open=wt("open"),
    First=wt("First"), green=wt("green"), sell=wt("sell"),
    Ten=wt("Ten"), each=wt("each"), Panic=wt("Panic"), versus=wt("versus"), holder=wt("holder"),
    Two=wt("Two"), eight1=wt("eight"), collapses=wt("collapses"), panic2=wt("panic", 2), lead=wt("lead"),
    Tw10=wt("Twenty"), ten1=wt("ten"), Tw11=wt("Twenty", 2), eleven=wt("eleven"), Still=wt("Still"), leading=wt("leading"),
    So=wt("So"), why=wt("why"), nobody=wt("nobody"), this=wt("this"),
    Tw12=wt("Twenty", 3), twelve=wt("twelve"), something=wt("something"), changes=wt("changes"),
    Covid=wt("Covid"), dodges=wt("dodges"), crash=wt("crash"), misses=wt("misses"), rebound=wt("rebound"),
    Heres=wt("Here's"), catch=wt("catch"), After=wt("After"), three3=wt("three", 3), red2=wt("red", 2), SPY2=wt("SPY", 2),
    bounce1=wt("bounce"), often=wt("often"), edge=wt("edge"), real1=wt("real"),
    But=wt("But"), tiny=wt("tiny"), invested=wt("invested"), eight2=wt("eight", 2), percent=wt("percent"), time=wt("time"),
    fees1=wt("fees"), eat=wt("eat"), half=wt("half"), profit=wt("profit"),
    Final=wt("Final"), score=wt("score"), Just=wt("Just"), holding=wt("holding"), seventy=wt("seventy"),
    Buying=wt("Buying"), panic3=wt("panic", 3), fourteen=wt("fourteen"),
    Double=wt("Double"), fees2=wt("fees", 2), Barely=wt("Barely"), above=wt("above"), ten2=wt("ten", 2),
    Verdict=wt("Verdict"), bounce2=wt("bounce", 2), real2=wt("real", 2), money=wt("money"), isnt=wt("isn't"),
)
T["rev1"] = T["seventy"] + 0.12      # first final number tears off here (>= 75% of runtime)
T["rev2"] = T["fourteen"] + 0.1
T["follow"] = END + 0.35
SCENES = [
    (0.0, "hook"), (T["Do"] - 0.15, "guess"), (T["Rule"] - 0.1, "rules"), (T["Ten"] - 0.1, "start"), (T["Two"] - 0.1, "crash08"),
    (T["Tw10"] - 0.1, "lead"), (T["Covid"] - 0.1, "covid"), (T["Heres"] - 0.1, "catch"), (T["But"] - 0.1, "tiny"),
    (T["Final"] - 0.1, "score"), (T["Double"] - 0.1, "double"), (T["Verdict"] - 0.1, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 230 + math.sin(tl * 1.6) * 30; y = 1345
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["three1"], 60) + hop(tl, T["row"], 50)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["panic1"], 70) + hop(t, T["hold"], 80) + hop(t, T["flipping"], 70)
    elif name == "rules":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["three2"], 90) + hop(t, T["green"], 90) + hop(t, T["sell"], 70)
    elif name == "start":
        flip = True; x = 640; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["each"], 120) + hop(t, T["holder"], 140, 0.55)
    elif name == "crash08":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["collapses"], 70) + hop(t, T["lead"], 80)
    elif name == "lead":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift += hop(t, T["Still"], 70) + hop(t, T["why"], 80) + hop(t, T["twelve"], 70)
    elif name == "covid":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["dodges"], 60) + hop(t, T["rebound"], 70)
    elif name == "catch":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["catch"], 110) + hop(t, T["bounce1"], 70) + hop(t, T["edge"], 90)
    elif name == "tiny":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["eight2"], 70) + hop(t, T["half"], 80)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["seventy"], 140) + hop(t, T["fourteen"], 120)
    elif name == "double":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["fees2"], 70) + hop(t, T["Barely"], 80)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["bounce2"], 110) + hop(t, T["money"], 150, 0.55)
    return x, y, px, flip, moving, lift
