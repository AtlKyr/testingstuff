SCENES = [
    (0.0, "hook"), (T["Real"] - 0.12, "guess"), (T["Nine"] - 0.12, "clue"), (T["test"] - 0.25, "rules"), (T["His"] - 0.1, "twin"),
    (T["Two"] - 0.1, "y2008"), (T["So"] - 0.1, "legend"), (T["Those"] - 0.1, "quiet"), (T["Then"] - 0.1, "y2020"),
    (T["Final"] - 0.25, "score"), (T["legend2"] - 0.3, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 600 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["Buy"], 80) if tl < 3.2 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0
        lift = 0
    elif name == "rules":
        x = 650; flip = True; y = lerp(1950, 1350, back(prog(u, 0, 0.5)))
        lift += hop(t, T["red1"], 45)
    elif name == "twin":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["green"], 45)
    elif name == "y2008":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["twentysix"], 40) + hop(t, T["sinks"], 30)
    elif name == "legend":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["Hold"], 60)
    elif name == "quiet":
        x = 40 + (math.sin(u * 1.2 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.2 - 1.57) < 0
        lift = 0
    elif name == "y2020":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["jump"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; y = 1380
        lift += hop(t, T["fiftyfive"], 30) + hop(t, T["seventeen"], 35) + hop(t, T["seventyone"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["real"], 80) + hop(t, T["crashes"], 100, 0.55)
    return x, y, px, flip, moving, lift
