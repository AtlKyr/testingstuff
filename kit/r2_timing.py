T = dict(
    three=wt("three", 1), four=wt("four"), still=wt("still"), sixteen=wt("sixteen", 1), half=wt("half", 1), this2=wt("This", 2),
    table=wt("table"), rsi1=wt("RSI", 1), rules=wt("rules"), only=wt("Only"), above=wt("above", 1), buy1=wt("Buy", 1), below=wt("below"),
    sell=wt("Sell"), closes=wt("closes"), twenty1=wt("Twenty", 1), fees=wt("Fees"), A=wt("A"), fifty=wt("fifty"), s73=wt("Seventy-three"),
    average=wt("Average"), three2=wt("three", 2), money=wt("money", 1), printer=wt("printer"), problem=wt("problem"), ten3=wt("ten", 3),
    ninety=wt("ninety"), cash=wt("cash"), nothing=wt("nothing"), final=wt("Final"), sixteen2=wt("sixteen", 2), buy2=wt("Buy", 2),
    s71=wt("seventy-one"), And=wt("And"), more=wt("more"), broker=wt("broker"), twenty2=wt("Twenty", 2), five=wt("five"), verdict=wt("Verdict"),
    win=wt("win"), profit=wt("profit"), follow=wt("Follow"), three_s=wt("three-strategy"), channel=wt("channel"),
)
SCENES = [
    (0.0, "hook"), (T["this2"] - 0.12, "title"), (wt("The", 1) - 0.1, "rules"), (T["twenty1"] - 0.1, "test"), (T["A"] - 0.1, "trades"),
    (wt("The", 2) - 0.1, "problem"), (T["final"] - 0.1, "score"), (T["And"] - 0.1, "fees"), (T["verdict"] - 0.08, "verdict"),
    (T["follow"] - 0.12, "outro"),
]
BOUNDS = [s for s, _ in SCENES[1:]]


def hop(t, tt, h=130, d=0.5):
    hp = prog(t, tt, d)
    return math.sin(math.pi * hp) * h if 0 < hp < 1 else 0.0


def motion(t):
    name, s0, s1 = scene_at(t)
    u = t - s0
    px, y, flip, moving, lift, x = 19, 1310, False, False, 0.0, 40
    if name == "hook":
        k = prog(u, 0, 0.4); x = lerp(-180, 40, ease(k)); moving = k < 1
        lift += hop(t, T["four"], 110) + hop(t, T["sixteen"], 90, 0.4)
    elif name == "title":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
        lift += hop(t, T["rsi1"], 120)
    elif name == "rules":
        k = prog(u, 0, 0.7); x = lerp(-450, 40, ease(k)); moving = k < 1
        lift += hop(t, T["buy1"], 110) + hop(t, T["sell"], 110)
    elif name == "test":
        flip = True; x = 620; y = lerp(1950, 1310, back(prog(u, 0, 0.5))); lift = abs(math.sin(u * 2.4)) * 16
    elif name == "trades":
        x = 40 + (math.sin(u * 1.4) * 0.5 + 0.5) * 520; moving = True; flip = math.cos(u * 1.4) < 0
        lift += hop(t, T["printer"], 150)
    elif name == "problem":
        x = 40
    elif name == "score":
        x = 40; lift += hop(t, T["sixteen2"], 120) + hop(t, T["s71"], 120)
    elif name == "fees":
        k = prog(u, 0, 0.8); x = lerp(1150, 620, ease(k)); flip = True; moving = 0 < k < 1
    elif name == "verdict":
        x = 40; lift += hop(t, T["profit"], 170, 0.6)
    elif name == "outro":
        px = 24; x = 20; y = lerp(1950, 1290, back(prog(u, 0, 0.6))); lift = abs(math.sin(u * 3.0)) * 40 if u > 0.8 else 0
    return x, y, px, flip, moving, lift
