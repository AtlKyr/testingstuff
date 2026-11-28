SCENES = [
    (0.0, "hook"), (T["Sell"] - 0.12, "guess"), (T["Short"] - 0.12, "rule"), (T["Wall"] - 0.12, "alarm"), (T["Twenty"] - 0.12, "race"),
    (T["Two"] - 0.12, "y2006"), (T["Tw22"] - 0.12, "y2022"), (T["Now"] - 0.12, "remember"), (T["June"] - 0.12, "payoff"),
    (T["It105"] - 0.12, "crash"), (T["Tw117"] - 0.15, "score"), (T["Verd"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["remember"]; SC["bleed"] = SC["y2022"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 330 + math.sin(tl * 1.6) * 40; y = 1380
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["upside"], 60) + hop(tl, T["two0"], 70) if tl < 3.4 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["allclear"], 40)
    elif name == "rule":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sell"], 40) + hop(t, T["buyr"], 40)
    elif name == "alarm":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["recess0"], 50)
    elif name == "race":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "y2006":
        x = 40 + (math.sin(u * 2.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 2.4) < 0; y = 1410; lift = 0
    elif name == "y2022":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["sells22"], 40) + hop(t, T["forty"], 40)
    elif name == "remember":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["allclear2"], 40)
    elif name == "payoff":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["buys"], 40) + hop(t, T["top"], 40)
    elif name == "crash":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["f55"], 30) + hop(t, T["Same"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift += hop(t, T["Verd"], 80) + hop(t, T["big"], 100, 0.55)
    return x, y, px, flip, moving, lift
