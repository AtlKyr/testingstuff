AUDIO = "final_mix_51.wav"
_R = json.load(open("results51.json"))
_c = pd.read_csv("sim51.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["bh"].values; SV = _c["strat"].values; NF = HV; FE = SV
SARV = _c["sar"].values; UPV = _c["up"].values.astype(bool); INN = _c["inm"].values.astype(bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
HI = _s["High"].values * _f; LO = _s["Low"].values * _f
BMID = BLO = BUP = CL
S0 = 0
CL_V = _R["final"]; MS_V = CL_V; BH_V = _R["bh"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


PTR = _R["trades_list"]
P_B = [di(x[0]) for x in PTR]; P_S = [di(x[1]) for x in PTR if x[1]]
P_HI = [PTR[k][2] > PTR[k - 1][3] for k in range(1, len(PTR))]
MS_SI = []; MS_BI = []; MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
TRD = []; TWIN = []
VAR = {"21": 0, "126": 0}
# spoken / shown numbers asserted against the backtest before TTS
assert _R["closed"] == 250 and round(_R["rebought_higher"] / _R["rebuys"] * 4) == 3
assert round(_R["r21_bh"] * 100) == 29 and round(_R["r21"] * 100) == 2 and _R["n21"] == 16
assert _R["r08"] <= _R["r08_bh"] + 0.02 and _R["r08"] < -0.35
assert round(CL_V, -2) == 12600 and round(BH_V, -2) == 70600 and CL_V > 10000


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Two"), (2, "fifty"), (3, "trades."), (4, "One"), (5, "famous"), (7, "Follow"), (10, "A?"), (12, "just"), (14, "B?"),
               (15, "Watch"), (17, "smoothest"), (19, "Parabolic"), (23, "dots"), (29, "in."), (30, "When"), (32, "flip"), (35, "out."),
               (36, "Two"), (38, "eight:"), (41, "flip,"), (43, "flip,"), (45, "flip."), (46, "It"), (48, "falls"), (51, "hard."),
               (52, "Every"), (56, "cost."), (58, "sells"), (61, "drop,"), (63, "buys"), (67, "bounce."), (68, "Three"), (76, "higher"),
               (80, "Now,"), (82, "smooth"), (84, "Twenty"), (85, "twenty-one."), (88, "climbs"), (89, "twenty-nine"), (92, "straight"),
               (94, "The"), (97, "sixteen"), (99, "anyway."), (100, "It"), (102, "two"), (104, "The"), (105, "bill."), (108, "twelve"),
               (114, "seventy"), (118, "Twenty"), (121, "flipping,"), (124, "barely"), (126, "cash.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Two0=wi(0), fifty=wi(2), trades=wi(3), One=wi(4), famous=wi(5), Follow=wi(7), A=wi(10), just=wi(12), B=wi(14), Watch=wi(15),
    smoothest=wi(17), Parabolic=wi(19), dots=wi(23), inn=wi(29), When=wi(30), flip=wi(32), out=wi(35), Two8=wi(36), eight=wi(38),
    f1=wi(41), f2=wi(43), f3=wi(45), It46=wi(46), falls=wi(48), hard=wi(51), Every=wi(52), cost=wi(56), sells=wi(58), drop=wi(61),
    buys=wi(63), bounce=wi(67), Three=wi(68), higher=wi(76), Now=wi(80), smooth=wi(82), Tw21=wi(84), y21=wi(85), climbs=wi(88),
    twentynine=wi(89), straight=wi(92), The94=wi(94), sixteen=wi(97), anyway=wi(99), It100=wi(100), two=wi(102), Final=wi(104),
    bill=wi(105), twelve=wi(108), seventy=wi(114), Verd=wi(118), flipping=wi(121), barely=wi(124), big=wi(126),
)
T["rev1"] = T["twelve"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["seventeen"] = T["big"]; T["Round"] = T["Verd"]; T["Selling"] = T["barely"]
for _k in ("Two", "threefifty", "four", "fiftyfour", "Worth", "October", "Circle", "Oct2", "Oct3", "front", "last", "never",
           "dodging", "Covid", "lose", "Up", "down", "up2", "sixtytwo", "ahead", "bottom", "choppy", "sixteenth", "It2", "forty",
           "buy", "sell", "rule", "In", "Trade", "It"):
    T.setdefault(_k, 0.0)
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
