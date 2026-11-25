SCENES = [
    (0.0, "hook"), (T["The"] - 0.12, "guess"), (T["rule"] - 0.12, "rule"), (T["In"] - 0.12, "crash"), (T["Then"] - 0.12, "chop"),
    (T["Trade"] - 0.12, "grid"), (T["Now"] - 0.12, "remember"), (T["It"] - 0.12, "never"), (T["Final"] - 0.15, "score"),
    (T["Verd"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["remember"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 430 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["fiftyfour"], 80) + hop(tl, T["Worth"], 60) if tl < 2.9 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["October"], 40)
    elif name == "rule":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["buy"], 40) + hop(t, T["sell"], 40)
    elif name == "crash":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sixtytwo"], 50) + hop(t, T["ahead"], 40)
    elif name == "chop":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Up"], 50) + hop(t, T["up2"], 50)
    elif name == "grid":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "remember":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sixteenth"], 40) + hop(t, T["front"], 40)
    elif name == "never":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["never"], 30) + hop(t, T["Covid"], 30)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Verd"], 80) + hop(t, T["big"], 100, 0.55)
    return x, y, px, flip, moving, lift
