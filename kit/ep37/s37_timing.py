T = dict(
    Twice=wt("Twice"), P1=wt("P"), Twice2=wt("Twice", 2), money=wt("money"), Rich=wt("Rich"), A=wt("A"), wrecked=wt("wrecked"),
    B=wt("B"), Keep=wt("Keep"), March=wt("March"), Two=wt("Two"), investors=wt("investors"), ten=wt("ten"), five=wt("five"),
    One=wt("One"), other=wt("other"), twice=wt("twice"), every=wt("every"), day=wt("day"), Two2=wt("Two", 2), six=wt("six"),
    seven=wt("seven"), ahead=wt("ahead"), Then=wt("Then"), eight=wt("eight"), Every=wt("Every"), drop=wt("drop"), two3=wt("two", 3),
    him=wt("him"), Remember=wt("Remember"), March2=wt("March", 2), Two3=wt("Two", 3), nine=wt("nine"), His=wt("His"),
    shrunk=wt("shrunk"), hundred=wt("hundred"), He=wt("He"), pass_=wt("pass"), fourteen=wt("fourteen"), Then2=wt("Then", 2),
    bull=wt("bull"), doubled=wt("doubled"), Twenty=wt("Twenty"), brutal=wt("brutal"), And=wt("And"), costs=wt("costs"),
    cut=wt("cut"), day2=wt("day", 2), Final=wt("Final"), seventyone=wt("seventy-one"), Double=wt("Double"),
    fortyeight=wt("forty-eight"), Twice3=wt("Twice", 3), money2=wt("money", 2), But=wt("But"), quarters=wt("quarters"),
    vanished=wt("vanished"),
)
T["rev1"] = T["seventyone"] + 0.1
T["rev2"] = T["fortyeight"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Rich"] - 0.12, "guess"), (T["Two"] - 0.12, "setup"),
    (T["Two2"] - 0.12, "ahead"), (T["Then"] - 0.12, "crash"), (T["Remember"] - 0.1, "remember"), (T["He"] - 0.12, "behind"),
    (T["Then2"] - 0.12, "bull"), (T["Twenty"] - 0.12, "y2022"), (T["And"] - 0.12, "costs"), (T["Final"] - 0.15, "score"),
    (T["Twice3"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["Twice2"], 80) if tl < 3 else 0)
    return x, y, px, False, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["March"], 50)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "setup":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["One"], 45) + hop(t, T["twice"], 60) + hop(t, T["every"], 40)
    elif name == "ahead":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["two3"], 50)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["shrunk"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["hundred"], 40)
    elif name == "behind":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["fourteen"], 50)
    elif name == "bull":
        x = 40 + (math.sin(u * 1.8) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.8) < 0; y = 1410; lift = 0
    elif name == "y2022":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["brutal"], 40)
    elif name == "costs":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["cut"], 45)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["money2"], 80) + hop(t, T["vanished"], 100, 0.55)
    return x, y, px, flip, moving, lift
