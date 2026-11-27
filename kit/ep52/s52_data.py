AUDIO = "final_mix_52.wav"
_R = json.load(open("results52.json"))
_c = pd.read_csv("sim52.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["bh"].values; SV = _c["eq"].values; NF = HV; FE = SV
INN = _c["IN"].values.astype(bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values; RAWO = _s["Open"].values
HI = _s["High"].values * _f; LO = _s["Low"].values * _f
BMID = BLO = BUP = CL
S0 = 0
CL_V = _R["final"]; MS_V = CL_V; BH_V = _R["bh"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []
SARV = CL; UPV = np.ones(N, bool)


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


_E = pd.read_csv("events52.csv")
E_I = _E["i"].values.astype(int); E_PX = _E["sell_px"].values; E_BI = _E["buy_i"].fillna(N - 1).values.astype(int)
E_BPX = _E["buy_px"].fillna(0).values
E_HI = (E_BPX > E_PX)
PTR = []; P_B = []; P_S = []; P_HI = []
MS_SI = []; MS_BI = []; MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
TRD = []; TWIN = []
VAR = {"21": 0, "126": 0}
I_LEAD = di("2008-12-01"); I_S918 = di("2008-09-18"); I_B919 = di("2008-09-19")
RAW_JUMP = RAWO[I_B919] / (RAWC[I_S918 - 1] * 0.98) - 1
ADJ_JUMP = OP[I_B919] / (CL[I_S918 - 1] * 0.98) - 1
# spoken / shown numbers asserted against the backtest before TTS
assert int(_R["closed_green"]) == 31 and _R["sells"] == 353 and abs(_R["rebought_higher"] / _R["sells"] - 0.5) < 0.01
assert round(CL_V, -2) == 37500 and round(BH_V, -2) == 70200
assert RAW_JUMP > 0.10 and ADJ_JUMP > 0.10 and I_S918 in list(E_I)
assert (SV / HV)[I_LEAD] > 1.0 and (SV / HV)[di("2009-06-01"):].max() < 1.0
assert _R["closed_below_th"] > _R["sells"] / 2


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Down"), (3, "closed"), (5, "thirty-one"), (7, "Sell"), (10, "A?"), (12, "hold,"), (13, "B?"), (14, "Wednesday,"), (16, "Dow"), (17, "erased"), (19, "eleven-hundred-point"), (21, "But"), (27, "next"), (29, "Our"), (32, "sells"), (35, "drops"), (40, "day,"), (42, "buys"), (45, "morning."), (46, "Ten"), (50, "twenty"), (54, "At"), (58, "brilliant."), (59, "Most"), (62, "below"), (65, "sold."), (66, "By"), (67, "December"), (72, "ahead."), (73, "Then"), (75, "bleeding"), (77, "Every"), (80, "fees."), (81, "Half"), (87, "higher."), (88, "Now,"), (91, "next"), (93, "September"), (99, "sells"), (101, "minus"), (103, "The"), (106, "green."), (107, "Next"), (109, "over"), (112, "higher."), (113, "Twenty"), (116, "Panic"), (118, "thirty-seven"), (122, "Holder:"), (123, "seventy"), (127, "Panic"), (129, "safe."), (131, "kept"), (133, "bills.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(Down=wi(0), closed=wi(3), thirtyone=wi(5), Sell=wi(7), A=wi(10), hold=wi(12), B=wi(13), Wed=wi(14), Dow=wi(16), erased=wi(17), eleven=wi(19), But=wi(21), next1=wi(27), Our=wi(29), sells=wi(32), drops=wi(35), day=wi(40), buys=wi(42), morning2=wi(45), Ten=wi(46), twenty=wi(50), At=wi(54), brilliant=wi(58), Most=wi(59), below=wi(62), sold=wi(65), By=wi(66), December=wi(67), ahead=wi(72), Then=wi(73), bleeding=wi(75), Every=wi(77), fees=wi(80), Half=wi(81), higher=wi(87), Now=wi(88), next3=wi(91), September=wi(93), sells2=wi(99), minus=wi(101), The103=wi(103), green2=wi(106), Next=wi(107), over=wi(109), higher2=wi(112), Twenty=wi(113), Panic=wi(116), thirtyseven=wi(118), Holder=wi(122), seventy=wi(123), Verd=wi(127), safe=wi(129), kept=wi(131), bills=wi(133))
T["rev1"] = T["thirtyseven"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["big"] = T["kept"]; T["Final"] = T["Twenty"]; T["flipping"] = T["safe"]
for _k in ("Two", "threefifty", "four", "fiftyfour", "Worth", "October", "Circle", "Oct2", "Oct3", "front", "last", "never",
           "dodging", "Covid", "lose", "Up", "down", "up2", "sixtytwo", "ahead2", "bottom", "choppy", "sixteenth", "It2", "forty",
           "buy", "sell", "rule", "In", "Trade", "It", "Two0", "fifty", "trades", "One", "famous", "Follow", "just", "Watch",
           "smoothest", "Parabolic", "dots", "inn", "When", "flip", "out", "Two8", "eight", "f1", "f2", "f3", "It46", "falls",
           "hard", "cost", "drop", "bounce", "Three", "smooth", "Tw21", "y21", "climbs", "twentynine", "straight", "The94",
           "sixteen", "anyway", "It100", "two", "bill", "twelve", "seventeen", "Round", "Selling", "seventy2"):
    T.setdefault(_k, 0.0)
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
