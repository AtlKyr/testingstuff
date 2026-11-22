def wi(i):
    return WORDS[i]["start"]


assert WORDS[6]["text"] == "Pocket" and WORDS[11]["text"] == "B?" and WORDS[20]["text"] == "Two" and WORDS[31]["text"] == "Every"
assert WORDS[37]["text"] == "He" and WORDS[49]["text"] == "Two" and WORDS[55]["text"] == "Then" and WORDS[71]["text"] == "Now,"
assert WORDS[98]["text"] == "Every" and WORDS[107]["text"] == "His" and WORDS[115]["text"] == "Final" and WORDS[123]["text"] == "The"
T = dict(
    Eighty=wi(0), checks=wi(2), twenty=wi(4), Pocket=wi(6), A=wi(8), reinvest=wi(10), B=wi(11), Watch=wi(12), tiny=wi(14),
    eight=wi(19), Two=wi(20), ten=wi(22), five=wi(30), Every=wi(31), three=wi(32), pays=wi(35), He=wi(37), cash=wi(42),
    She=wi(43), more=wi(45), hers=wi(48), Two2=wi(49), seven=wi(51), neck=wi(52), Then=wi(55), crash=wi(57), And=wi(58),
    pile=wi(62), lead=wi(67), So=wi(68), wins=wi(70), Now=wi(71), tiny2=wi(73), December=wi(75), eight2=wi(78),
    fiftynine=wi(79), She2=wi(81), bought=wi(82), bottom=wi(88), By=wi(89), worth=wi(94), five2=wi(95), thirty=wi(97),
    Every2=wi(98), quietly=wi(103), years2=wi(106), His=wi(107), sixtyeight=wi(112), Final=wi(115), fiftyfive=wi(118),
    Reinvested=wi(120), seventy=wi(121), The=wi(123), small=wi(126), What=wi(127), grew=wi(129), wasnt=wi(131),
)
T["rev1"] = T["fiftyfive"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Pocket"] - 0.12, "guess"), (T["Two"] - 0.12, "setup"), (T["He"] - 0.12, "split"),
    (T["Two2"] - 0.12, "y2007"), (T["Then"] - 0.12, "crash"), (T["Now"] - 0.1, "remember"), (T["She2"] - 0.12, "bottom"),
    (T["Every2"] - 0.12, "every"), (T["His"] - 0.12, "jar"), (T["Final"] - 0.15, "score"), (T["The"] - 0.12, "verdict"),
    (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["twenty"], 80) if tl < 3 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["tiny"], 50)
    elif name == "setup":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["ten"], 45) + hop(t, T["three"], 40) + hop(t, T["pays"], 40)
    elif name == "split":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["cash"], 45) + hop(t, T["more"], 45)
    elif name == "y2007":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["lead"], 50) + hop(t, T["wins"], 40)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["fiftynine"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["fiftynine"], 40)
    elif name == "bottom":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["bottom"], 40) + hop(t, T["thirty"], 60)
    elif name == "every":
        x = 40 + (math.sin(u * 1.8) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.8) < 0; y = 1410; lift = 0
    elif name == "jar":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["sixtyeight"], 45)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["small"], 80) + hop(t, T["grew"], 100, 0.55)
    return x, y, px, flip, moving, lift
