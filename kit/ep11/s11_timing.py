T = dict(
    Nasdaq=wt("Nasdaq"), crashed=wt("crashed"), five=wt("five"), percent1=wt("percent"), Should=wt("Should"), run=wt("run"),
    SP=wt("S&P"), dropped=wt("dropped"), four=wt("four"), too=wt("too"), In=wt("In"), years=wt("years"),
    t39=wt("thirty-nine"), times=wt("times"),
    A1=wt("A"), later1=wt("later"), how=wt("how"), higher1=wt("higher"), A2=wt("A", 2), under=wt("under"),
    B=wt("B"), almost=wt("almost"), Guess=wt("Guess"),
    One1=wt("One"), trader=wt("trader"), panicked=wt("panicked"), every=wt("every"),
    Rule=wt("Rule"), crash1=wt("crash"), day=wt("day"), sell=wt("sell"), morning=wt("morning"), wait1=wt("wait"), month=wt("month"),
    buy=wt("buy"), back=wt("back"),
    Two=wt("Two"), eight=wt("eight"), Crash=wt("Crash"), crash2=wt("crash", 2), panic1=wt("panic"), dodges1=wt("dodges"),
    takes=wt("takes"), lead1=wt("lead"), Tw11=wt("Twenty"), eleven=wt("eleven"), still=wt("still"), ahead=wt("ahead"),
    Covid=wt("Covid"), dodges2=wt("dodges", 2), crash3=wt("crash", 3), panics=wt("panics"), bottom=wt("bottom"),
    lead2=wt("lead", 2), vanishes=wt("vanishes"), Tw22=wt("Twenty", 2), t22=wt("twenty-two"), decides=wt("decides"),
    Heres=wt("Here's"), twist=wt("twist"), Change=wt("Change"), wait2=wt("wait", 2), winner=wt("winner"), changes=wt("changes"),
    One2=wt("One", 2), week=wt("week"), Three=wt("Three"), Six=wt("Six"), Different=wt("Different"), endings=wt("endings"),
    Final=wt("Final"), score=wt("score"), Holding=wt("Holding"), seventy=wt("seventy"),
    OneMonth=wt("One-month"), eighty=wt("eighty"), ThreeMonth=wt("Three-month"), fifty8=wt("fifty-eight"),
    Your=wt("Your"), guess=wt("guess"), t36=wt("Thirty-six"), t39b=wt("thirty-nine", 2), higher2=wt("higher", 2), later2=wt("later", 2),
    Verdict=wt("Verdict"), panic4=wt("panic", 4), lucky=wt("lucky"), timing=wt("timing"), crash4=wt("crash", 4),
    mostly=wt("mostly"), noise=wt("noise"),
)
T["rev1"] = T["seventy"] + 0.12      # first final number tears off here (>= 75% of runtime)
T["rev2"] = T["eighty"] + 0.1
T["rev3"] = T["fifty8"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["SP"] - 0.12, "count"), (T["A1"] - 0.12, "guess"), (T["One1"] - 0.1, "rules"), (T["Two"] - 0.1, "crash08"),
    (T["Covid"] - 0.1, "covid"), (T["Tw22"] - 0.1, "decide"), (T["Heres"] - 0.1, "twist"), (T["One2"] - 0.12, "waits"),
    (T["Final"] - 0.1, "score"), (T["Your"] - 0.1, "answer"), (T["Verdict"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["five"], 60) + hop(tl, T["run"], 55)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "count":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["four"], 70) + hop(t, T["t39"], 90)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A2"], 70) + hop(t, T["B"], 80) + hop(t, T["Guess"], 70)
    elif name == "rules":
        flip = True; x = 640; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["panicked"], 80) + hop(t, T["sell"], 70) + hop(t, T["buy"], 70)
    elif name == "crash08":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift += hop(t, T["Crash"], 60) + hop(t, T["lead1"], 70) + hop(t, T["ahead"], 60)
    elif name == "covid":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["dodges2"], 60) + hop(t, T["vanishes"], 60)
    elif name == "decide":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["decides"], 70)
    elif name == "twist":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["twist"], 110) + hop(t, T["changes"], 80)
    elif name == "waits":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["week"], 60) + hop(t, T["Three"], 60) + hop(t, T["Six"], 60) + hop(t, T["Different"], 80)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["seventy"], 80) + hop(t, T["eighty"], 90) + hop(t, T["fifty8"], 70)
    elif name == "answer":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["t36"], 120) + hop(t, T["higher2"], 80)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["lucky"], 100) + hop(t, T["mostly"], 130, 0.55)
    return x, y, px, flip, moving, lift
