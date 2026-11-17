SCENES = [
    (0.0, "hook"), (T["Monday"] - 0.1, "question"), (T["Sell"] - 0.12, "guess"), (T["Ten"] - 0.15, "clue"),
    (T["rule"] - 0.2, "rules"), (T["Two"] - 0.1, "crash"), (T["He"] - 0.1, "dodge"), (T["So"] - 0.1, "y2020"),
    (T["Then"] - 0.1, "leaves"), (T["Those"] - 0.1, "remember"), (T["bill"] - 0.25, "score"),
    (T["fear2"] - 0.25, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["strike"], 80) + hop(tl, T["within"], 50) if tl < 4.5 else 0)
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
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["close"], 60)
    elif name == "guess":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["sell2"], 45) + hop(t, T["buy"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["eight"], 40) + hop(t, T["again2"], 40)
    elif name == "dodge":
        x = 40 + (math.sin(u * 1.5 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.5 - 1.57) < 0
        lift = hop(t, T["leads"], 45)
    elif name == "y2020":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["wins"], 40) + hop(t, T["lead"], 40)
    elif name == "leaves":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["leaves"], 30)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0
        lift = 0
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["seventy"], 35) + hop(t, T["forty"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["right2"], 90) + hop(t, T["thirty"], 110, 0.55)
    return x, y, px, flip, moving, lift
