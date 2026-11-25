AUDIO = "final_mix_48.wav"
_R = json.load(open("results48.json"))
_c = pd.read_csv("sim48.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["H"].values; SV = _c["S"].values; NF = HV; FE = SV
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
BMID = BLO = BUP = CL
S0 = 0
CL_V = _R["final"]; MS_V = CL_V; BH_V = _R["bh"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


TOPC = _c["TOP"].values; BOTC = _c["BOT"].values
CTR = _R["trades"]
TB_I = [di(x[0]) for x in CTR]; TS_I = [di(x[1]) if x[1] else N - 1 for x in CTR]
CWIN = [(x[3] / x[2] * (1 - 0.0005) ** 2 - 1) > 0 for x in CTR if x[1]]
# out-of-market bands: from each exit to the next entry
MS_SI = [TS_I[k] for k in range(len(CTR) - 1)]; MS_BI = [TB_I[k + 1] for k in range(len(CTR) - 1)]
MS_LV = []; MTR = []; MS_HIGHER = []
INN = _c["INM"].values.astype(bool)
TRD = []; TWIN = []
W0 = di("2005-04-26")
I_BOT09 = di("2009-03-09"); I_LEAD = di("2014-10-16"); I_TOP07 = di("2007-10-09"); I_14S = I_14B = 0
VAR = {"21": 0, "126": 0}
# spoken numbers -> asserted against the backtest before TTS
assert len(CTR) == 54 and _R["closed"] - _R["wins"] > _R["closed"] / 2
assert round((SV[I_BOT09] / HV[I_BOT09] - 1) * 100) == 62
assert SV[I_LEAD] > HV[I_LEAD] and (SV[I_LEAD + 1:] <= HV[I_LEAD + 1:]).all()
assert round(CL_V, -2) == 40900 and round(BH_V, -2) == 73300
assert INN[di("2008-01-02"):di("2008-12-31")].mean() < 0.2


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Ichimoku"), (2, "Fifty-four"), (4, "Worth"), (6, "The"), (8, "A?"), (10, "just"), (12, "B?"), (13, "Circle"),
               (17, "October."), (18, "The"), (21, "close"), (25, "buy."), (26, "Close"), (29, "sell."), (30, "In"), (35, "sits"),
               (40, "crash."), (43, "March"), (47, "bottom,"), (49, "sixty-two"), (51, "ahead."), (52, "Then"), (56, "choppy."),
               (57, "Up,"), (58, "down,"), (59, "up"), (61, "Trade"), (68, "lose."), (69, "Each"), (72, "chips"), (77, "Now,"),
               (79, "October"), (81, "October"), (82, "sixteenth,"), (87, "last"), (90, "front."), (91, "It"), (92, "never"),
               (98, "dodging"), (102, "Covid"), (104, "Final"), (108, "forty"), (114, "seventy-three"), (118, "The"),
               (120, "dodged"), (122, "It"), (126, "chop.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Ichimoku=wi(0), fiftyfour=wi(2), Worth=wi(4), The=wi(6), A=wi(8), just=wi(10), B=wi(12), Circle=wi(13), October=wi(17),
    rule=wi(18), close=wi(21), buy=wi(25), Close=wi(26), sell=wi(29), In=wi(30), sits=wi(35), crash=wi(40), March=wi(43),
    bottom=wi(47), sixtytwo=wi(49), ahead=wi(51), Then=wi(52), choppy=wi(56), Up=wi(57), down=wi(58), up2=wi(59), Trade=wi(61),
    lose=wi(68), Each=wi(69), chips=wi(72), Now=wi(77), Oct2=wi(79), Oct3=wi(81), sixteenth=wi(82), last=wi(87), front=wi(90),
    It=wi(91), never=wi(92), dodging=wi(98), Covid=wi(102), Final=wi(104), forty=wi(108), seventythree=wi(114), Verd=wi(118),
    dodged=wi(120), It2=wi(122), big=wi(126),
)
T["rev1"] = T["forty"] + 0.1
T["rev2"] = T["seventythree"] + 0.1
T["follow"] = END + 0.1
T["seventeen"] = T["big"]; T["Round"] = T["Verd"]; T["Selling"] = T["It2"]
for _k in ("Two", "threefifty", "four"):
    T.setdefault(_k, 0.0)
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
