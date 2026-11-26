AUDIO = "final_mix_49.wav"
_R = json.load(open("results49.json"))
_c = pd.read_csv("sim49.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["bh"].values; SV = _c["strat"].values; NF = HV; FE = SV
INFL = _c["infl"].values * 100; OUTM = _c["out"].values.astype(bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
BMID = BLO = BUP = CL
S0 = 0
CL_V = _R["strat"]["final"]; MS_V = CL_V; BH_V = _R["bh"]["final"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


EV = _R["events"]
SELL_D = [e[1] for e in EV if e[0] == "SELL"]; BUY_D = [e[1] for e in EV if e[0] == "BUY"][1:]
MS_SI = [di(x) for x in SELL_D]; MS_BI = [di(x) for x in BUY_D] + [N - 1] * (len(SELL_D) - len(BUY_D))
MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
INN = ~OUTM
TRD = []; TWIN = []
Q_S07 = di("2007-12-04"); Q_B08 = di("2008-12-02"); Q_S21 = di("2021-06-02"); Q_B24 = di("2024-01-03"); Q_TOP07 = di("2007-10-09")
Q_OCT22 = di("2022-10-12"); Q_BOT09 = di("2009-03-09")
VAR = {"21": 0, "126": 0}
# spoken / shown numbers -> asserted against the backtest before TTS
assert round(CL_V, -2) == 89500 and round(BH_V, -2) == 70200
assert SELL_D[3] == "2007-12-04" and BUY_D[3] == "2008-12-02" and SELL_D[5] == "2021-06-02" and BUY_D[5] == "2024-01-03"
assert OP[Q_B08] / OP[Q_S07] - 1 < -0.40 and RAWC[Q_B08] / RAWC[Q_S07] - 1 < -0.40
assert OP[Q_B24] > OP[Q_S21] and _s["Open"].values[Q_B24] > _s["Open"].values[Q_S21]
assert _R["no2008"] < BH_V and _R["scan"]["0.025"] < BH_V
assert 50 <= (DATES[Q_S07] - DATES[Q_TOP07]).days <= 62
assert len(SELL_D) == 6


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Inflation,"), (1, "three"), (5, "Sell"), (7, "Cash"), (9, "A?"), (11, "hold,"), (12, "B?"), (13, "Keep"),
               (18, "December."), (19, "The"), (27, "sell."), (28, "When"), (30, "cools,"), (31, "buy"), (33, "Fast"), (37, "twenty-one."),
               (38, "Prices"), (42, "sells"), (44, "June."), (45, "Twenty"), (47, "stocks"), (48, "tumble,"), (51, "sitting"), (53, "cash."),
               (54, "Genius?"), (55, "Then"), (57, "rally"), (61, "It"), (62, "buys"), (66, "twenty-four,"), (68, "more"), (73, "Now,"),
               (76, "December."), (77, "December"), (80, "seven."), (81, "Inflation"), (82, "tops"), (85, "two"), (90, "peak."), (91, "It"),
               (92, "sells."), (93, "It"), (94, "sits"), (97, "worst"), (100, "crash,"), (102, "buys"), (105, "forty"), (107, "cheaper."),
               (108, "Final"), (112, "eighty-nine"), (118, "seventy"), (122, "It"), (123, "won."), (124, "But"), (125, "take"),
               (129, "December,"), (132, "loses.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Inflation=wi(0), three=wi(1), Sell=wi(5), Cash=wi(7), A=wi(9), hold=wi(11), B=wi(12), Keep=wi(13), Dec1=wi(18), rule=wi(19),
    sell=wi(27), When=wi(28), cools=wi(30), buy=wi(31), Fast=wi(33), y21=wi(37), Prices=wi(38), sells=wi(42), June=wi(44),
    Twenty22=wi(45), stocks=wi(47), tumble=wi(48), sitting=wi(51), cash=wi(53), Genius=wi(54), Then=wi(55), rally=wi(57),
    It61=wi(61), buys=wi(62), y24=wi(66), more=wi(68), Now=wi(73), Dec2=wi(76), Dec3=wi(77), seven=wi(80), Infl2=wi(81), tops=wi(82),
    two=wi(85), peak=wi(90), It91=wi(91), sold=wi(92), It93=wi(93), sits=wi(94), worst=wi(97), crash=wi(100), buys2=wi(102),
    forty=wi(105), cheaper=wi(107), Final=wi(108), eightynine=wi(112), seventy=wi(118), Verd=wi(122), won=wi(123), But=wi(124),
    take=wi(125), Dec4=wi(129), big=wi(132),
)
T["rev1"] = T["eightynine"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["seventeen"] = T["big"]; T["Round"] = T["Verd"]; T["Selling"] = T["take"]
for _k in ("Two", "threefifty", "four", "fiftyfour", "Worth", "October", "Circle", "just", "Oct2", "Oct3", "front", "last", "never",
           "dodging", "Covid", "lose", "Up", "down", "up2", "sixtytwo", "ahead", "bottom", "choppy", "sixteenth", "It2", "forty_",):
    T.setdefault(_k, 0.0)
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
