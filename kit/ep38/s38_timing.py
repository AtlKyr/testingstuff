def wi(i):
    return WORDS[i]["start"]


assert WORDS[7]["text"] == "Sit" and WORDS[13]["text"] == "B?" and WORDS[20]["text"] == "Twenty" and WORDS[28]["text"] == "Every"
assert WORDS[45]["text"] == "Two" and WORDS[53]["text"] == "Two" and WORDS[61]["text"] == "And" and WORDS[68]["text"] == "Stocks"
assert WORDS[82]["text"] == "He" and WORDS[88]["text"] == "Twenty" and WORDS[101]["text"] == "But" and WORDS[114]["text"] == "The"
assert WORDS[118]["text"] == "sixty-three" and WORDS[121]["text"] == "seventy" and WORDS[123]["text"] == "Twenty" and WORDS[130]["text"] == "Skip"
T = dict(
    Down=wi(0), six=wi(3), Skip=wi(5), Thanks=wi(6), Sit=wi(7), A=wi(10), B=wi(13), Keep=wi(14), crash=wi(16), Thanks2=wi(17),
    Twenty=wi(20), SPY=wi(23), ten=wi(24), each=wi(27), Every=wi(28), sells=wi(32), Monday=wi(34), buys=wi(37), next=wi(40),
    She=wi(42), holds=wi(44), Two=wi(45), five=wi(47), costs=wi(49), little=wi(52), Two2=wi(53), seven=wi(55), dodges=wi(57),
    red=wi(59), And=wi(61), crash2=wi(63), Two3=wi(65), eight=wi(67), Stocks=wi(68), fall=wi(71), then=wi(73), single=wi(75),
    best=wi(76), twenty=wi(80), He=wi(82), sat=wi(83), most=wi(85), Twenty2=wi(88), eleven=wi(89), eighteen=wi(91), shaky=wi(92),
    red2=wi(94), He2=wi(96), right=wi(98), But=wi(101), dodged=wi(106), small=wi(108), The=wi(109), missed=wi(112),
    wasnt=wi(113), The2=wi(114), sat2=wi(116), sixtythree=wi(118), Held=wi(120), seventy=wi(121), Twenty3=wi(123),
    short=wi(124), cost=wi(126), seventyfive=wi(128), Skip2=wi(130), turkey=wi(132), market=wi(135),
)
T["rev1"] = T["sixtythree"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Sit"] - 0.12, "guess"), (T["Twenty"] - 0.12, "setup"), (T["Every"] - 0.12, "rule"),
    (T["Two"] - 0.12, "y2005"), (T["Two2"] - 0.12, "y2007"), (T["And"] - 0.1, "remember"), (T["Stocks"] - 0.12, "best"),
    (T["Twenty2"] - 0.12, "red"), (T["But"] - 0.12, "small"), (T["The2"] - 0.15, "score"),
    (T["Twenty3"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]
SC["crash"] = SC["remember"]; SC["twist"] = SC["red"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["Skip"], 80) if tl < 3 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["crash"], 50)
    elif name == "setup":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ten"], 45) + hop(t, T["each"], 40)
    elif name == "rule":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sells"], 45) + hop(t, T["buys"], 45) + hop(t, T["holds"], 40)
    elif name == "y2005":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "y2007":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["dodges"], 45)
    elif name == "remember":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["eight"], 50)
    elif name == "best":
        x = 40 + (math.sin(u * 1.5 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.5 - 1.57) < 0; lift = 0
        if t > T["best"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["best"], 40) + hop(t, T["most"], 35)
    elif name == "red":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["eleven"], 40) + hop(t, T["eighteen"], 40) + hop(t, T["right"], 50)
    elif name == "small":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["small"], 40) + hop(t, T["missed"], 45)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["seventyfive"], 80) + hop(t, T["turkey"], 100, 0.55)
    return x, y, px, flip, moving, lift
