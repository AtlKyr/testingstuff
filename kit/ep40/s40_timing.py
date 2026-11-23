def wi(i):
    return WORDS[i]["start"]


assert WORDS[0]["text"] == "Forty-eight" and WORDS[7]["text"] == "Sell" and WORDS[12]["text"] == "B?" and WORDS[13]["text"] == "Mark"
assert WORDS[17]["text"] == "Today," and WORDS[24]["text"] == "seven" and WORDS[28]["text"] == "His" and WORDS[44]["text"] == "Two"
assert WORDS[57]["text"] == "ahead." and WORDS[58]["text"] == "Then" and WORDS[68]["text"] == "Then" and WORDS[84]["text"] == "again!"
assert WORDS[85]["text"] == "Here's" and WORDS[89]["text"] == "March" and WORDS[95]["text"] == "five" and WORDS[98]["text"] == "He"
assert WORDS[105]["text"] == "eleven" and WORDS[112]["text"] == "He" and WORDS[116]["text"] == "The" and WORDS[121]["text"] == "sixty-one"
assert WORDS[124]["text"] == "seventy" and WORDS[126]["text"] == "He" and WORDS[134]["text"] == "Holding" and WORDS[137]["text"] == "more."
T = dict(
    Forty=wi(0), pops=wi(3), twenty=wi(5), Sell=wi(7), A=wi(10), Hold=wi(11), B=wi(12), Mark=wi(13), Tuesday=wi(16),
    Today=wi(17), futures=wi(18), two=wi(21), seven=wi(24), red=wi(26), His=wi(28), SPY=wi(30), up=wi(34), Sell2=wi(35),
    Buy=wi(39), week=wi(42), Two=wi(44), sells=wi(48), cheaper=wi(54), ahead=wi(57), Then=wi(58), rebound=wi(60), For=wi(64),
    trails=wi(67), Then2=wi(68), crash=wi(72), He=wi(73), cheaper2=wi(79), front=wi(83), Heres=wi(85), March=wi(89),
    twentyfourth=wi(90), SPY2=wi(93), five=wi(95), He2=wi(98), sells2=wi(99), week2=wi(101), pays=wi(104), eleven=wi(105),
    He3=wi(112), never=wi(113), The=wi(116), sixtyone=wi(121), Holding=wi(123), seventy=wi(124), He4=wi(126), cheaper3=wi(129),
    Holding2=wi(134), paid=wi(136), more=wi(137),
)
T["rev1"] = T["sixtyone"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Sell"] - 0.12, "guess"), (T["Today"] - 0.12, "news"), (T["His"] - 0.12, "rules"),
    (T["Two"] - 0.12, "y2008"), (T["Then"] - 0.12, "trails"), (T["Then2"] - 0.12, "y2020"), (T["Heres"] - 0.12, "remember"),
    (T["He2"] - 0.12, "rebuy"), (T["The"] - 0.15, "score"), (T["He4"] - 0.12, "verdict"), (T["follow"], "loop"),
]
BOUNDS = [s for s, _ in SCENES[1:-1]]
SC = {name: s for s, name in SCENES}
SC["question"] = SC["guess"]; SC["twist"] = SC["trails"]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def idle(u):
    return abs(math.sin(u * 2.4)) * 16


def hook_motion(tl):
    px = 24; x = 470 + math.sin(tl * 1.6) * 40; y = 1345
    lift = idle(tl) + (hop(tl, -0.2, 70, 0.45) + hop(tl, T["pops"], 80) if tl < 3 else 0)
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
        lift += hop(t, T["A"], 40) + hop(t, T["B"], 40) + hop(t, T["Mark"], 50)
    elif name == "news":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["two"], 50) + hop(t, T["seven"], 45)
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["up"], 45) + hop(t, T["Buy"], 40)
    elif name == "y2008":
        x = 40 + (math.sin(u * 1.6) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 1.6) < 0; y = 1410; lift = 0
    elif name == "trails":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["trails"], 30)
    elif name == "y2020":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["cheaper2"], 40) + hop(t, T["front"], 60)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
        if t > T["five"] - 0.3:
            x = 650; flip = True; moving = False; lift = idle(u) + hop(t, T["five"], 40)
    elif name == "rebuy":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["eleven"], 40) + hop(t, T["never"], 30)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); moving = 0 < k < 1; flip = True; y = 1380
        lift += hop(t, T["rev1"], 35) + hop(t, T["rev2"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = 0 < k < 1
        lift += hop(t, T["cheaper3"], 80) + hop(t, T["paid"], 100, 0.55)
    return x, y, px, flip, moving, lift
