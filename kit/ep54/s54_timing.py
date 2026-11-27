SCENES = [
    (0.0, "hook"), (T["Skip2"] - 0.12, "guess"), (T["Rule"] - 0.12, "rule"), (T["Ten"] - 0.12, "race"), (T["Jan08"] - 0.12, "y2008"),
    (T["Two9"] - 0.12, "y2009"), (T["In"] - 0.12, "grid"), (T["Now"] - 0.12, "remember"), (T["The107"] - 0.12, "payoff"),
    (T["Twenty"] - 0.15, "score"), (T["Verd"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["remember"]; SC["bleed"] = SC["y2009"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 330 + math.sin(tl * 1.6) * 40; y = 1380
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["Jan"], 70) + hop(tl, T["eleven"], 80) if tl < 2.9 else 0)
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
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["so"], 40) + hop(t, T["quiet"], 40)
    elif name == "rule":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sell"], 40) + hop(t, T["next"], 40)
    elif name == "race":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "y2008":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["dodges"], 40) + hop(t, T["way"], 40)
    elif name == "y2009":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["rockets"], 30)
    elif name == "grid":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "remember":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Tw20"], 40) + hop(t, T["four"], 40)
    elif name == "payoff":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sells20"], 40) + hop(t, T["fifteen"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift += hop(t, T["Verd"], 80) + hop(t, T["big"], 100, 0.55)
    return x, y, px, flip, moving, lift
