AUDIO = "final_mix_56.wav"
_R = json.load(open("results56.json"))
_c = pd.read_csv("sim56.csv", index_col=0, parse_dates=True)
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
CL_V = _R["three"]; MS_V = CL_V; BH_V = _R["one"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []
SARV = CL; UPV = np.ones(N, bool)


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


YR = {}
REC = np.maximum.accumulate(RAWC)
RW = [dict(a_end=0, b_end=0)] * 4; RA = RB = RL = RS = [0, 0, 0, 0]
E_I = np.array([], int); E_PX = []; E_BI = []; E_BPX = []; E_HI = np.array([], bool)
PTR = []; P_B = []; P_S = []; P_HI = []
MS_SI = []; MS_BI = []; MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
TRD = []; TWIN = []
VAR = {"21": 0, "126": 0}
I_LEAD = di("2008-11-20"); I_S918 = di("2008-09-18"); I_B919 = di("2008-09-19"); RAW_JUMP = 0.0
I_F20 = di("2020-02-03"); I_E20 = di("2020-12-31"); RAW20 = 0.0
# ---- #56: simulated 3x daily S&P fund vs plain SPY
Q_THREE_V = _R["three"]; Q_ONE_V = _R["one"]; Q_TWO_V = _R["two"]
CL_V = Q_THREE_V; BH_V = Q_ONE_V
Q_LOW = _R["low3"]; Q_ILOW = di(_R["low3_date"]); Q_ICATCH = di(_R["catch"])
Q_I07 = di("2007-12-31"); Q_I10 = di("2010-12-31"); Q_I11 = di("2011-12-30")
Q_C0, Q_C1 = di("2020-02-19"), di("2020-03-23")
# spoken / shown numbers asserted against the backtest before TTS
assert _R["r2008_3"] < -0.85 and round(Q_LOW, -2) == 800 and 7.5 <= _R["catch_years"] < 8.5 and round(-_R["c20_3"] * 100) == 76
assert round(-_R["r2011_3"] * 100) == 11 and abs(_R["r2011_1"]) < 0.02 and abs(_R["r2011_raw"]) < 0.01
assert round(Q_ONE_V, -3) == 71000 and round(Q_THREE_V, -3) == 174000 and round((1 - Q_LOW / 1e4) * 100) == 92 and _R["y2007_3"] > _R["y2007_1"]
assert abs(SV[-1] - Q_THREE_V) < 1 and abs(HV[-1] - Q_ONE_V) < 1


def wi(i):
    return WORDS[i]["start"]


_A = [(0, 'Triple'), (2, 'Down'), (4, 'eighty-five'), (8, 'year.'), (9, 'Triple'), (11, 'A?'), (13, 'plain'), (17, 'B?'), (18, 'One'),
      (19, 'strange'), (23, 'Ten'), (26, 'each,'), (31, 'The'), (34, 'moves'), (35, 'three'), (41, 'every'), (43, 'day.'), (44, 'Two'),
      (47, "triple's"), (48, 'ahead.'), (49, 'Then'), (51, 'crash.'), (52, 'By'), (53, 'March'), (61, 'eight'), (64, 'Game'), (65, 'over?'),
      (67, 'crawls'), (69, 'Eight'), (73, 'catch'), (79, 'Then'), (80, 'twenty'), (83, 'seventy-six'), (87, 'month.'), (88, 'Now,'),
      (90, 'strange'), (92, 'Twenty'), (93, 'eleven.'), (99, 'basically'), (100, 'nowhere.'), (101, 'The'), (104, 'Lost'), (105, 'eleven'),
      (107, 'Every'), (108, 'up-and-down'), (111, 'eats'), (113, 'Twenty'), (116, 'plain'), (120, 'seventy-one'), (122, 'Triple,'),
      (125, 'seventy-four'), (127, 'Triple'), (128, 'won.'), (129, 'If'), (132, 'stomach'), (134, 'ninety-two')]
for _i, _w in _A:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(Tri=wi(0), Down=wi(2), e85=wi(4), Tri2=wi(9), A=wi(11), plain=wi(13), B=wi(17), One=wi(18), strange=wi(19), Ten=wi(23),
         each=wi(26), The31=wi(31), moves=wi(34), three=wi(35), every=wi(41), Two=wi(44), triples=wi(47), ahead=wi(48), Then=wi(49),
         crash=wi(51), By=wi(52), March=wi(53), eight=wi(61), Game=wi(64), over=wi(65), crawls=wi(67), Eight=wi(69), catch=wi(73),
         Then2=wi(79), tw20=wi(80), s76=wi(83), month=wi(87), Now=wi(88), strange2=wi(90), Tw11=wi(92), eleven=wi(93), basically=wi(99),
         nowhere=wi(100), The101=wi(101), Lost=wi(104), eleven2=wi(105), Every=wi(107), updown=wi(108), eats=wi(111), Tw113=wi(113),
         plain2=wi(116), s71=wi(120), Triple3=wi(122), s74=wi(125), Verd=wi(127), won=wi(128), If=wi(129), stomach=wi(132), n92=wi(134))
T["rev1"] = T["s71"] + 0.1
T["rev2"] = T["s74"] + 0.1
T["follow"] = END + 0.1
T["big"] = T["If"]; T["safe"] = T["Verd"]; T["lost"] = T["Verd"]; T["Final"] = T["Tw113"]
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
Q_SELL = []; Q_BUY = []; Q_RT = []; Q_SCAN = {}; Q_S15 = Q_B20 = Q_S07 = Q_B08 = 1; Q_RAW07 = Q_RAW15 = Q_YRS = 0.0
