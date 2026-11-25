SCENES = [
    (0.0, "hook"), (T["Sell"] - 0.12, "guess"), (T["Each"] - 0.12, "headline"), (T["So"] - 0.12, "rule"),
    (T["SPY2"] - 0.12, "s200"), (T["Two"] - 0.12, "ladder"), (T["And"] - 0.12, "remember"), (T["Genius"] - 0.12, "genius"),
    (T["Now"] - 0.15, "score"), (T["Round"] - 0.12, "verdict"), (T["follow"], "loop"),
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
    px = 24; x = 560 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["fifty"], 80) + hop(tl, T["ten"], 60) if tl < 3.8 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["eight"], 40)
    elif name == "headline":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["headline"], 50) + hop(t, T["top"], 60)
    elif name == "rule":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sells"], 40) + hop(t, T["buys"], 40)
    elif name == "s200":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["two"], 40) + hop(t, T["more"], 50)
    elif name == "ladder":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "remember":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["May"], 40) + hop(t, T["cheaper"], 50)
    elif name == "genius":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Genius"] + 0.1, 40) + hop(t, T["never"], 30)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["Round"], 80) + hop(t, T["seventeen"], 100, 0.55)
    return x, y, px, flip, moving, lift
