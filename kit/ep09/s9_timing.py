T = dict(
    miss=wt("Miss"), ten1=wt("ten"), days1=wt("days"), twenty1=wt("twenty"), years=wt("years"), what=wt("What"), cost=wt("cost"),
    A=wt("A"), scratch=wt("scratch"), disaster=wt("disaster"),
    And=wt("And"), ten2=wt("ten", 2), hide1=wt("hide"), nobody=wt("nobody"), look=wt("look"),
    two1=wt("Two"), investors=wt("investors"), ten3=wt("ten", 3), each=wt("each"),
    one=wt("One"), never=wt("never"), sells=wt("sells"), other=wt("other"), skips=wt("skips"), best1=wt("best"), spy=wt("SPY"),
    two2=wt("Two", 2), five=wt("five"), seven1=wt("seven"), dead=wt("dead"), even=wt("even"),
    then=wt("Then"), eight=wt("eight"), crashes1=wt("crashes"), gap=wt("gap"), opens1=wt("opens"), watch=wt("Watch"), grow=wt("grow"),
    tw20=wt("Twenty"), covid=wt("Covid"), It=wt("It"), again=wt("again"),
    now=wt("Now"), weird=wt("weird"), All=wt("All"), best2=wt("best", 2), middle=wt("middle"), crashes2=wt("crashes", 2),
    Seven=wt("Seven"), within=wt("within"), weeks=wt("weeks"), worst1=wt("worst"), days5=wt("days", 5),
    dodge1=wt("Dodge"), panic=wt("panic"), miss2=wt("miss"), rescue=wt("rescue"),
    final=wt("Final"), score=wt("score"), Never=wt("Never"), sold=wt("sold"), seventy=wt("seventy"),
    skipped=wt("Skipped"), t31=wt("thirty-one"), more=wt("More"), half=wt("half"), gone=wt("gone"),
    dodge2=wt("Dodge", 2), worst2=wt("worst", 2), too=wt("too"), just2=wt("Just"), hair=wt("hair"), ahead=wt("ahead"),
    verdict=wt("Verdict"), best3=wt("best", 3), hide2=wt("hide", 2), inside=wt("inside"), worst3=wt("worst", 3),
    stay=wt("Stay"), seated=wt("seated"),
)
T["rev1"] = T["seventy"] + 0.12      # first final number tears off here (>= 75% of runtime)
T["follow"] = END + 0.35
SCENES = [
    (0.0, "hook"), (T["A"] - 0.15, "guess"), (T["And"] - 0.1, "case"), (T["two1"] - 0.1, "start"), (T["one"] - 0.1, "rules"),
    (T["two2"] - 0.1, "even"), (T["then"] - 0.1, "crash08"), (T["tw20"] - 0.1, "covid"), (T["now"] - 0.1, "weird"),
    (T["Seven"] - 0.1, "worst"), (T["dodge1"] - 0.1, "rescue"), (T["final"] - 0.1, "score"), (T["more"] - 0.1, "half"),
    (T["dodge2"] - 0.1, "both"), (T["verdict"] - 0.1, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 250 + math.sin(tl * 1.6) * 30; y = 1345
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["ten1"], 60) + hop(tl, T["cost"], 50)
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
        k = prog(u, 0, 0.6); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["scratch"], 70) + hop(t, T["disaster"], 90, 0.55)
    elif name == "case":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["hide1"], 60) + hop(t, T["nobody"], 80)
    elif name == "start":
        flip = True; x = 620; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["ten3"], 110) + hop(t, T["each"], 160, 0.55)
    elif name == "rules":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["never"], 100) + hop(t, T["skips"], 120) + hop(t, T["spy"], 80)
    elif name == "even":
        k = prog(u, 0, 0.7); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["dead"], 70)
    elif name == "crash08":
        x = 40 + (math.sin(u * 1.5 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.5 - 1.57) < 0
        lift += hop(t, T["gap"], 60) + hop(t, T["grow"], 60)
    elif name == "covid":
        k = prog(u, 0, 0.6); x = lerp(-450, 30, ease(k)); moving = k < 1
        lift += hop(t, T["again"], 60)
    elif name == "weird":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["weird"], 120) + hop(t, T["crashes2"], 70)
    elif name == "worst":
        x = 40 + (math.sin(u * 1.7) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.7) < 0
        lift += hop(t, T["Seven"], 110) + hop(t, T["worst1"], 90)
    elif name == "rescue":
        # walks in from the right, then runs off left to the EXIT on "panic"
        k = prog(u, 0, 0.45); x = lerp(1150, 560, ease(k)); flip = True; moving = 0 < k < 1
        r = prog(t, T["panic"] - 0.1, 1.1)
        if r > 0:
            x = lerp(560, 90, ease_io(r)); moving = r < 1; flip = True
        lift += hop(t, T["rescue"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["seventy"], 140) + hop(t, T["t31"], 120)
    elif name == "half":
        flip = True; x = 620; y = lerp(1950, 1350, back(prog(u, 0, 0.45)))
        lift += hop(t, T["gone"], 90)
    elif name == "both":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["too"], 90) + hop(t, T["hair"], 130)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["best3"], 110) + hop(t, T["stay"], 150, 0.55)
    return x, y, px, flip, moving, lift
