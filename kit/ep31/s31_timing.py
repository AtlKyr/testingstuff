T = dict(
    sixtyfour=wt("sixty-four"), Check=wt("Check"), monthly1=wt("monthly"), A1=wt("A"), never1=wt("never"), B1=wt("B"),
    One2=wt("One", 2), choppy1=wt("choppy"), rule2=wt("rule", 2), own=wt("own"), twohundred=wt("two-hundred-day"), cash=wt("cash"),
    Checked1=wt("Checked"), faked=wt("faked"), Checked2=wt("Checked", 2), month=wt("month"), calms=wt("calms"),
    Two1=wt("Two"), sells=wt("sells"), January=wt("January"), crash=wt("crash"), bottom=wt("bottom"), twice=wt("twice"),
    Ten=wt("Ten"), ahead=wt("ahead"), So=wt("So"), wins=wt("wins"), Remember=wt("Remember"), Twenty=wt("Twenty"),
    He2=wt("He"), buys=wt("buys"), nine=wt("nine"), sells2=wt("sells", 2), Buys=wt("Buys"), loses2=wt("loses", 2),
    holder2=wt("holder", 2), catches=wt("catches"), Final=wt("Final"), fiftynine=wt("fifty-nine"), seventyone=wt("seventy-one"),
    Monthly=wt("Monthly"), daily=wt("daily"), Never2=wt("Never", 2), both=wt("both"),
)
T["rev1"] = T["fiftynine"] + 0.1
T["rev2"] = T["seventyone"] + 0.1
T["rev3"] = T["rev2"] + 0.8
T["follow"] = END + 0.1
SCENES = [
    (0.0, "hook"), (T["Check"] - 0.12, "guess"), (T["One2"] - 0.12, "clue"), (T["rule2"] - 0.15, "rules"),
    (T["Checked1"] - 0.1, "daily"), (T["Two1"] - 0.1, "y2008"), (T["Ten"] - 0.1, "decade"), (T["Remember"] - 0.1, "remember"),
    (T["He2"] - 0.1, "y2022"), (T["Final"] - 0.1, "score"), (T["Monthly"] - 0.1, "verdict"), (T["follow"], "loop"),
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
    lift = idle(tl) + (hop(tl, -0.05, 60, 0.45) + hop(tl, T["sixtyfour"], 80) if tl < 4 else 0)
    return x, y, px, math.cos(tl * 1.6) < 0, False, lift


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
        lift += hop(t, T["A1"], 40) + hop(t, T["B1"], 40)
    elif name == "clue":
        x = 40 + (math.sin(u * 1.9 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.9 - 1.57) < 0; lift = 0
    elif name == "rules":
        k = prog(u, 0, 0.5); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["own"], 45) + hop(t, T["cash"], 45)
    elif name == "daily":
        x = 40 + (math.sin(u * 2.2) * 0.5 + 0.5) * 560; moving = True; flip = math.cos(u * 2.2) < 0; y = 1410; lift = 0
    elif name == "y2008":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["sells"], 40) + hop(t, T["twice"], 60)
    elif name == "decade":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["ahead"], 50) + hop(t, T["wins"], 40)
    elif name == "remember":
        x = 40 + (math.sin(u * 1.6 - 1.57) * 0.5 + 0.5) * 580; moving = True; flip = math.cos(u * 1.6 - 1.57) < 0; lift = 0
    elif name == "y2022":
        k = prog(u, 0, 0.6); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["nine"], 50) + hop(t, T["loses2"], 40)
    elif name == "score":
        k = prog(u, 0, 0.6); x = lerp(1150, 650, ease(k)); flip = True; moving = 0 < k < 1; y = 1380
        lift += hop(t, T["fiftynine"], 35) + hop(t, T["seventyone"], 35)
    elif name == "verdict":
        k = prog(u, 0, 0.5); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["daily"], 80) + hop(t, T["both"], 100, 0.55)
    return x, y, px, flip, moving, lift
