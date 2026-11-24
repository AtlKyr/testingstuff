SCENES = [
    (0.0, "hook"), (T["Jump"] - 0.12, "guess"), (T["The"] - 0.12, "news"), (T["SPY"] - 0.12, "count"),
    (T["A2"] - 0.12, "rules"), (T["Two"] - 0.12, "y2008"), (T["B4"] - 0.12, "rounds"), (T["That"] - 0.12, "remember"),
    (T["Twenty"] - 0.12, "y2020"), (T["All"] - 0.15, "score"), (T["Twenty2"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["rounds"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["seven"], 80) + hop(tl, T["Buy"], 60) if tl < 3 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["March"], 50)
    elif name == "news":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["best"], 60) + hop(t, T["April"], 40)
    elif name == "count":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["twentyseven"], 50) + hop(t, T["ten"], 40)
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["B2"], 40) + hop(t, T["year"], 40)
    elif name == "y2008":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "rounds":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["nineteen"], 40) + hop(t, T["patience"], 50)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["bottom"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["never"], 40) + hop(t, T["cash"], 30)
    elif name == "y2020":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["same"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); moving = 0 < k < 1; flip = True; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift += hop(t, T["seven2"], 80) + hop(t, T["already"], 100, 0.55)
    return x, y, px, flip, moving, lift
