T = dict(
    Fear=wt("Fear"), hits=wt("hits"), thirty1=wt("thirty"), buy1=wt("buy"), Buy=wt("Buy"), panic=wt("panic"), A=wt("A"),
    hold=wt("hold"), B=wt("B"), One=wt("One"), quiet1=wt("quiet"), decides=wt("decides"), rule=wt("rule"), gauge=wt("gauge"),
    buy2=wt("buy", 2), calm=wt("calm"), year=wt("year"), At=wt("At"), cash1=wt("cash"), August=wt("August"), seven=wt("seven"),
    spikes=wt("spikes"), jumps=wt("jumps"), crash=wt("crash"), Ouch=wt("Ouch"), It=wt("It"), holds=wt("holds"), scare=wt("scare"),
    Five=wt("Five"), Five2=wt("Five", 2), winners=wt("winners"), So=wt("So"), wins=wt("wins"), Remember=wt("Remember"),
    From=wt("From"), twelve=wt("twelve"), fifteen=wt("fifteen"), never=wt("never"), Almost=wt("Almost"), cash2=wt("cash", 2),
    forty=wt("forty"), percent=wt("percent"), Now=wt("Now"), scoreboard=wt("scoreboard"), Fear2=wt("Fear", 2),
    thirtytwo=wt("thirty-two"), Just=wt("Just"), seventy=wt("seventy"), Being=wt("Being"), greedy=wt("greedy"),
    worked=wt("worked"), Waiting=wt("Waiting"), didnt=wt("didn't"),
)
T["rev1"] = T["thirtytwo"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Buy"] - 0.12, "guess"), (T["One"] - 0.12, "clue"), (T["rule"] - 0.3, "rules"),
    (T["At"] - 0.1, "wait"), (T["August"] - 0.1, "spike"), (T["It"] - 0.1, "trades"), (T["Remember"] - 0.1, "remember"),
    (T["Now"] - 0.15, "score"), (T["Being"] - 0.15, "verdict"), (T["follow"], "loop"),
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
    px = 24; x = 600 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["thirty1"], 80) + hop(tl, T["buy1"], 60) if tl < 3 else 0)
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
        lift += hop(t, T["buy2"], 45) + hop(t, T["year"], 45)
    elif name == "wait":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1; lift = 0 if k >= 1 else lift
    elif name == "spike":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["jumps"], 60) + hop(t, T["Ouch"], 40)
    elif name == "trades":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.4) < 0; y = 1410; lift = 0
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["forty"] - 0.3:
            x = 40; moving = False; lift = idle(u) + hop(t, T["forty"], 50)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["thirtytwo"], 35) + hop(t, T["seventy"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["worked"], 80) + hop(t, T["didnt"], 100, 0.55)
    return x, y, px, flip, moving, lift
