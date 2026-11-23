def wi(i):
    return WORDS[i]["start"]


assert WORDS[0]["text"] == "Sixty-forty." and WORDS[5]["text"] == "All" and WORDS[10]["text"] == "B?" and WORDS[11]["text"] == "One"
assert WORDS[16]["text"] == "Two" and WORDS[31]["text"] == "She" and WORDS[44]["text"] == "Then" and WORDS[66]["text"] == "So"
assert WORDS[81]["text"] == "Twenty" and WORDS[92]["text"] == "The" and WORDS[102]["text"] == "Her" and WORDS[114]["text"] == "Final"
assert WORDS[117]["text"] == "forty-four" and WORDS[121]["text"] == "seventy" and WORDS[123]["text"] == "Her" and WORDS[134]["text"] == "bigger."
T = dict(
    Sixty=wi(0), safe=wi(3), All=wi(5), A=wi(7), B=wi(10), One=wi(11), ugly=wi(12), Two=wi(16), ten=wi(18), five=wi(24),
    He=wi(25), SPY=wi(30), She=wi(31), sixty=wi(33), forty=wi(36), rebalances=wi(41), January=wi(43), Then=wi(44),
    Stocks=wi(48), thirtyseven=wi(50), fourteen=wi(56), lead=wi(60), years=wi(65), So=wi(66), bonds=wi(67), Then2=wi(69),
    passes=wi(76), fourteen2=wi(80), Twenty=wi(81), crash=wi(83), front=wi(88), briefly=wi(91), The=wi(92), twentytwo=wi(97),
    Stocks2=wi(98), eighteen=wi(100), Her=wi(102), sixteen=wi(105), shield=wi(107), cracked=wi(108), Final=wi(114),
    fortyfour=wi(117), seventy=wi(121), Her2=wi(123), half=wi(127), His=wi(130), far=wi(133), bigger=wi(134),
)
T["rev1"] = T["fortyfour"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["All"] - 0.12, "guess"), (T["Two"] - 0.12, "setup"), (T["She"] - 0.12, "split"),
    (T["Then"] - 0.12, "crash"), (T["So"] - 0.12, "bull"), (T["Twenty"] - 0.12, "y2020"), (T["The"] - 0.12, "remember"),
    (T["Her"] - 0.12, "shieldsc"), (T["Final"] - 0.15, "score"), (T["Her2"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["crash"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["safe"], 80) if tl < 3 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["ugly"], 50)
    elif name == "setup":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["ten"], 45) + hop(t, T["SPY"], 40)
    elif name == "split":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["forty"], 45) + hop(t, T["January"], 40)
    elif name == "crash":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["fourteen"], 50) + hop(t, T["lead"], 40)
    elif name == "bull":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "y2020":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["front"], 40)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["eighteen"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["eighteen"], 40)
    elif name == "shieldsc":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sixteen"], 40) + hop(t, T["cracked"], 30)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); moving = 0 < k < 1; flip = True; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift += hop(t, T["half"], 80) + hop(t, T["far"], 100, 0.55)
    return x, y, px, flip, moving, lift
