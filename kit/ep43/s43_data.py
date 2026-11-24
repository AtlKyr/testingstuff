AUDIO = "final_mix_43.wav"
_R = json.load(open("results43.json"))
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _s.index
N = len(DATES)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
S0 = 0


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


ROWS = _R["rows"]
RI = [di(x["day"]) for x in ROWS]                      # monster-day index
PA = np.array([x["A"] - 10000 for x in ROWS]); PB = np.array([x["B"] - 10000 for x in ROWS])
# cumulative profit step series (step on the monster day; each round is scored one year later)
CUMA = np.zeros(N); CUMB = np.zeros(N)
for i, a_, b_ in zip(RI, PA, PB):
    CUMA[i:] += a_; CUMB[i:] += b_
HV = CUMB; SV = CUMA; NF = HV; FE = SV
INN = np.ones(N, bool)
A_V = _R["A"]; B_V = _R["B"]
HOLD_V = A_V; RULE_V = B_V; ONE_V = A_V; TWO_V = B_V; REIN_V = A_V; POCK_V = B_V
SELLS = []; BUYS = []; ZONES = []
WINB = [x["B"] > x["A"] for x in ROWS]
X0 = di("2008-01-02"); XEND = di("2023-03-01")
I_M09 = di("2009-03-10"); I_M09P = I_M09 - 1
I_M24 = di("2020-03-24"); I_A06 = di("2020-04-06")
# spoken numbers -> asserted against the backtest before TTS
assert len(ROWS) == 27 and _R["wB"] == 19 and _R["dips"] == 20
assert round(A_V, -3) == 351000 and round(B_V, -3) == 341000
assert all(x["dip"] for x in ROWS if x["day"] < "2009-03-01")
assert [x for x in ROWS if x["day"] == "2009-03-10"][0]["dip"] is False
assert CUMB[di("2009-02-27")] > CUMA[di("2009-02-27")] + 10000
assert min(CL[I_M09 + 1:I_M09 + 253]) >= CL[I_M09P]


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Up"), (5, "Buy"), (7, "Jump"), (9, "A?"), (12, "B?"), (13, "Watch"), (17, "The"), (27, "SPY"), (30, "twenty-seven"),
               (36, "Each"), (38, "twins"), (43, "A"), (48, "B"), (57, "A"), (62, "Two"), (71, "B"), (75, "B"), (77, "nineteen"),
               (81, "So"), (84, "That"), (87, "Two"), (94, "bottom."), (95, "The"), (97, "never"), (99, "B"), (102, "cash"), (105, "Twenty"),
               (109, "All"), (117, "fifty-one"), (119, "Waiting,"), (122, "forty-one"), (124, "Twenty"), (130, "The"), (132, "seven?"),
               (134, "bottom"), (137, "in.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Up=wi(0), seven=wi(3), Buy=wi(5), Jump=wi(7), A=wi(9), wait=wi(11), B=wi(12), Watch=wi(13), March=wi(15), The=wi(17), best=wi(21),
    April=wi(24), SPY=wi(27), twentyseven=wi(30), Each=wi(36), twins=wi(38), ten=wi(40), A2=wi(43), next=wi(46), B2=wi(48), drop=wi(52),
    start=wi(56), year=wi(58), compare=wi(61), Two=wi(62), dip=wi(66), every=wi(69), pulls=wi(72), ahead=wi(74), B4=wi(75),
    nineteen=wi(77), rounds=wi(80), So=wi(81), patience=wi(82), That=wi(84), March2=wi(85), Two2=wi(87), nine=wi(89), bottom=wi(94),
    The2=wi(95), never=wi(97), B5=wi(99), cash=wi(102), Twenty=wi(105), same=wi(107), All=wi(109), fiftyone=wi(117), Waiting=wi(119),
    fortyone=wi(122), Twenty2=wi(124), back2=wi(129), The3=wi(130), seven2=wi(132), bottom2=wi(134), already=wi(136), inn=wi(137),
)
T["rev1"] = T["fiftyone"] + 0.1
T["rev2"] = T["fortyone"] + 0.1
T["follow"] = END + 0.1
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
