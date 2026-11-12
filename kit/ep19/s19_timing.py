T = dict(
    Five=wt("Five"), month1=wt("month"), five1=wt("five"), When=wt("When"), hit=wt("hit"), thousand2=wt("thousand", 2),
    A=wt("A"), under1=wt("under"), ten1=wt("ten"), B=wt("B"), over1=wt("over"), ten2=wt("ten", 2), But=wt("But"), shock=wt("shock"),
    second1=wt("second"), rule=wt("rule"), buy=wt("buy"), same=wt("same"), never=wt("never"), sell=wt("sell"), fees=wt("fees"),
    Then1=wt("Then"), eight=wt("eight"), hits=wt("hits"), twentyfive=wt("twenty-five"), worth1=wt("worth"), fourteen1=wt("fourteen"),
    Most=wt("Most"), quit=wt("quit"), keep=wt("keep"), cheap=wt("cheap"), single=wt("single"), August=wt("August"),
    one3=wt("one", 2), Nine=wt("Nine"), seven=wt("seven"), A2=wt("A", 2), wins=wt("wins"), Now=wt("Now"), remember=wt("remember"),
    took=wt("took"), five2=wt("five", 2), third=wt("third"), Under=wt("Under"), two2=wt("two", 3), Final=wt("Final"), score=wt("score"),
    one4=wt("one", 3), worth2=wt("worth", 2), almost=wt("almost"), four=wt("four"), ninety=wt("ninety"), first=wt("first"),
    hardest=wt("hardest"), Then2=wt("Then", 2), snowballs=wt("snowballs"),
)
for k, v in T.items():
    assert v is not None, k
T["rev1"] = T["one4"] + 0.1
T["rev2"] = T["four"] + 0.1
T["rev3"] = T["rev2"] + 0.6
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["When"] - 0.1, "question"), (T["A"] - 0.12, "guess"), (T["But"] - 0.1, "hidden"), (T["rule"] - 0.15, "rules"),
    (T["Then1"] - 0.1, "crash"), (T["Most"] - 0.1, "quit"), (T["August"] - 0.1, "hit"), (T["Now"] - 0.1, "remember"),
    (T["Final"] - 0.1, "score"), (T["first"] - 0.25, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + hop(tl, -0.05, 60, 0.45) + hop(tl, T["month1"], 70) + hop(tl, T["five1"], 60)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1350, False, False, idle(t - s0), 40
    if name == "hook":
        return hook_motion(t)
    if name == "loop":
        return hook_motion(0.03 + (t - s0) * 0.05)
    if name == "question":
        x = lerp(-300, 700, prog(u, 0, s1 - s0)); moving = True; lift = 0
    elif name == "guess":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["under1"], 50) + hop(t, T["over1"], 50)
    elif name == "hidden":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "rules":
        y = lerp(1950, 1350, back(prog(u, 0, 0.5))); x = 40
        lift += hop(t, T["same"], 45) + hop(t, T["never"], 45)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["twentyfive"], 40) + hop(t, T["fourteen1"], 50)
    elif name == "quit":
        x = 40 + (math.sin(u * 1.4 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.4 - 1.57) < 0
        lift = hop(t, T["keep"], 50) + hop(t, T["cheap"], 40)
    elif name == "hit":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["one3"], 60) + hop(t, T["Nine"], 40) + hop(t, T["wins"], 80)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["five2"], 40) + hop(t, T["two2"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["one4"], 35) + hop(t, T["four"], 45)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["hardest"], 90) + hop(t, T["snowballs"], 110, 0.55)
    return x, y, px, flip, moving, lift
