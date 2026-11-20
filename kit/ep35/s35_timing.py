T = dict(
    One=wt("One"), fee1=wt("fee"), forty=wt("forty"), bills1=wt("bills"), Costs=wt("Costs"), A=wt("A"), lot=wt("lot"), B=wt("B"),
    The=wt("The"), worst=wt("worst"), never=wt("never"), Two2=wt("Two", 2), investors=wt("investors"), ten=wt("ten"), Same=wt("Same"),
    pays=wt("pays"), fee2=wt("fee", 2), Year=wt("Year"), hundred2=wt("hundred", 2), Who=wt("Who"), notice=wt("notice"),
    Two3=wt("Two", 3), eight=wt("eight"), crashes=wt("crashes"), still=wt("still"), arrives=wt("arrives"), Then=wt("Then"),
    bull=wt("bull"), bills2=wt("bills", 2), grow=wt("grow"), Remember=wt("Remember"), Each=wt("Each"), dollar=wt("dollar"),
    stopped=wt("stopped"), Left=wt("Left"), seven=wt("seven"), Final=wt("Final"), seventy=wt("seventy"), fiftyseven=wt("fifty-seven"),
    Bills=wt("Bills"), four1=wt("four"), Real=wt("Real"), twelve=wt("twelve"), One3=wt("One", 3), ate=wt("ate"), fifth=wt("fifth"),
    gains=wt("gains"),
)
T["rev1"] = T["seventy"] + 0.1
T["rev2"] = T["fiftyseven"] + 0.1
T["rev3"] = T["four1"] + 0.05
T["rev4"] = T["twelve"] + 0.05
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Costs"] - 0.12, "guess"), (T["The"] - 0.12, "clue"), (T["Two2"] - 0.15, "rules"),
    (T["Year"] - 0.12, "year1"), (T["Two3"] - 0.12, "crash"), (T["Then"] - 0.12, "bull"), (T["Remember"] - 0.1, "remember"),
    (T["Final"] - 0.15, "score"), (T["One3"] - 0.15, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["fee1"], 60) + hop(tl, T["forty"], 80) if tl < 3 else 0)
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
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ten"], 45) + hop(t, T["fee2"], 45)
    elif name == "year1":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; lift = (0 if k < 1 else idle(u)) + hop(t, T["hundred2"], 50)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["still"], 40)
    elif name == "bull":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["Left"] - 0.3:
            x = 40; moving = False; lift = idle(u) + hop(t, T["seven"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["ate"], 80) + hop(t, T["fifth"], 100, 0.55)
    return x, y, px, flip, moving, lift
