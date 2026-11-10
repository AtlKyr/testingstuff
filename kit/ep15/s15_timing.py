T = dict(
    ten=wt("ten"), invest=wt("invest"), All=wt("All"), today=wt("today"), or_=wt("or"), drip1=wt("drip"), monthly=wt("monthly"),
    year1=wt("year"), A=wt("A"), in3=wt("in", 3), B=wt("B"), drip2=wt("drip", 2), One=wt("One"), starting1=wt("starting"),
    changes=wt("changes"), everything=wt("everything"), The1=wt("The"), rule=wt("rule"), every1=wt("every"), since=wt("since"),
    five1=wt("five"), one_r=wt("one"), round1=wt("round"), Two1=wt("Two"), six=wt("six"), Allin1=wt("All-in"), takes=wt("takes"),
    round2=wt("round", 2), round3=wt("round", 3), money=wt("money"), longer=wt("longer"), Then=wt("Then"), crash=wt("crash"),
    dripper1=wt("dripper"), nineteen=wt("nineteen"), row=wt("row"), buying=wt("buying"), cheaper=wt("cheaper"), After=wt("After"),
    allin2=wt("all-in"), runs=wt("runs"), again=wt("again"), Remember=wt("Remember"), month4=wt("month", 4), June=wt("June"),
    eight=wt("eight"), later=wt("later"), allin3=wt("all-in", 2), sixtynine=wt("sixty-nine"), left=wt("left"),
    dripper2=wt("dripper", 2), ninetysix=wt("ninety-six"), Final=wt("Final"), score=wt("score"), Allin4=wt("All-in", 2),
    won=wt("won"), s77=wt("seventy-seven"), dripper3=wt("dripper", 3), fiftyone=wt("fifty-one"), Average=wt("Average"),
    lead=wt("lead"), five3=wt("five", 3), thirtythree=wt("thirty-three"), Dripping=wt("Dripping"), isnt=wt("isn't"),
    better=wt("better"), ret=wt("return"), Its2=wt("It's"), insurance=wt("insurance"), pay=wt("pay"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["s77"] + 0.1
T["rev2"] = T["fiftyone"] + 0.1
T["rev3"] = T["five3"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["All"] - 0.1, "choice"), (T["A"] - 0.12, "guess"), (T["One"] - 0.1, "hidden"), (T["The1"] - 0.1, "rules"),
    (T["Two1"] - 0.1, "r0506"), (T["Then"] - 0.1, "crash"), (T["After"] - 0.1, "after"), (T["Remember"] - 0.1, "remember"),
    (T["Final"] - 0.1, "score"), (T["Dripping"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["ten"], 70) + hop(tl, T["invest"], 60)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "choice":
        x = 360 + math.sin(u * 2.2) * 300; moving = True; flip = math.cos(u * 2.2) < 0
        lift += hop(t, T["today"], 60) + hop(t, T["drip1"], 60) + hop(t, T["year1"], 60)
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 640, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["in3"], 60) + hop(t, T["B"], 60) + hop(t, T["drip2"], 70)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift += hop(t, T["changes"], 40)
    elif name == "rules":
        flip = True; x = 650; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["every1"], 50) + hop(t, T["round1"], 50)
    elif name == "r0506":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 600; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift += hop(t, T["round2"], 60) + hop(t, T["longer"], 60)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["crash"], 60) + hop(t, T["nineteen"], 60) + hop(t, T["cheaper"], 50)
    elif name == "after":
        x = lerp(-300, 700, prog(u, 0, s1 - s0)); moving = True; y = 1410
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["June"], 40) + hop(t, T["sixtynine"], 40) + hop(t, T["ninetysix"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["s77"], 35) + hop(t, T["fiftyone"], 40) + hop(t, T["thirtythree"], 30)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ret"], 100) + hop(t, T["insurance"], 120, 0.55) + hop(t, T["pay"], 80)
    return x, y, px, flip, moving, lift
