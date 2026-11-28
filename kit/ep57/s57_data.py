AUDIO = "final_mix_57.wav"
_R = json.load(open("results57.json"))
_c = pd.read_csv("sim57.csv", index_col=0, parse_dates=True)
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
# ---- #57: yield-curve inversion rule (FRED T10Y2Y)
CL_V = _R["final"]; BH_V = _R["bh"]
Q_TR = _R["trades"]
Q_SELL = [di(x["d"]) for x in Q_TR if x["k"] == "S"]; Q_BUYS = [di(x["d"]) for x in Q_TR if x["k"] == "B"]
Q_S22, Q_B24, Q_B07 = di(_R["s22"]), di(_R["b24"]), di(_R["b07"]); Q_TOP = di(_R["top07"]); Q_LOW09 = di("2009-03-09")
Q_RAW22 = RAWO[Q_B24] / RAWO[Q_S22] - 1
SPREAD = _c["sp"].values
# spoken / shown numbers asserted against the backtest before TTS
assert _R["inv_years"] > 2 and _R["sells_0607"] == 10 and _R["raw22_24"] > 0.4 and _R["adj22_24"] > 0.4 and _R["out22_years"] > 2
assert _R["b07"] == "2007-06-11" and 3.5 < _R["months_before_top"] < 4.5 and round(_R["mdd"] * 100) == -55 and abs(_R["mdd"] - _R["mdd_bh"]) < 0.001
assert round(CL_V, -2) == 41600 and round(BH_V, -2) == 70200 and abs(Q_RAW22 - _R["raw22_24"]) < 1e-9


def wi(i):
    return WORDS[i]["start"]


_A = [(0, 'The'), (1, 'yield'), (3, 'upside'), (7, 'two'), (9, 'Sell'), (12, 'alarm,'), (13, 'A?'), (15, 'ignore'), (17, 'B?'), (18, 'One'),
      (19, 'all-clear'), (23, 'Short'), (26, 'long'), (28, 'sell.'), (29, 'Flip'), (31, 'buy.'), (32, 'Wall'), (37, 'recession'),
      (39, 'Twenty'), (41, 'ten'), (44, 'Two'), (46, 'six:'), (49, 'rings.'), (50, 'Sell,'), (51, 'buy,'), (52, 'sell,'), (53, 'buy.'),
      (54, 'Ten'), (62, 'And'), (64, 'recession'), (66, 'Twenty'), (69, 'sells'), (71, 'sits'), (76, 'The'), (80, 'climbs'), (82, 'forty'),
      (86, 'Now,'), (89, 'all-clear.'), (90, 'June'), (95, 'curve'), (96, 'flips'), (99, 'buys.'), (100, 'Four'), (104, 'top.'),
      (105, 'It'), (106, 'rides'), (110, 'down'), (111, 'fifty-five'), (113, 'Same'), (117, 'Twenty'), (120, 'alarm,'), (121, 'forty-one'),
      (125, 'Holder,'), (126, 'seventy'), (130, 'Right'), (133, 'recession.'), (134, 'Wrong'), (137, 'money.')]
for _i, _w in _A:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(The=wi(0), upside=wi(3), two0=wi(7), Sell=wi(9), A=wi(13), ignore=wi(15), B=wi(17), One=wi(18), allclear=wi(19), Short=wi(23),
         long0=wi(26), sell=wi(28), Flip=wi(29), buyr=wi(31), Wall=wi(32), recess0=wi(37), Twenty=wi(39), ten=wi(41), Two=wi(44), six=wi(46),
         rings=wi(49), s1=wi(50), b1=wi(51), s2=wi(52), b2=wi(53), Ten=wi(54), And=wi(62), recess1=wi(64), Tw22=wi(66), sells22=wi(69),
         sits=wi(71), The76=wi(76), climbs=wi(80), forty=wi(82), Now=wi(86), allclear2=wi(89), June=wi(90), curve=wi(95), flips=wi(96),
         buys=wi(99), Four=wi(100), top=wi(104), It105=wi(105), rides=wi(106), down=wi(110), f55=wi(111), Same=wi(113), Tw117=wi(117),
         alarm2=wi(120), f41=wi(121), Holder=wi(125), seventy=wi(126), Verd=wi(130), recess2=wi(133), Wrong=wi(134), money=wi(137))
T["rev1"] = T["f41"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["big"] = T["Wrong"]; T["safe"] = T["Verd"]; T["lost"] = T["Verd"]; T["Final"] = T["Tw117"]
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
Q_BUY = []; Q_RT = []; Q_SCAN = {}; Q_S15 = Q_B20 = Q_S07 = Q_B08 = 1; Q_RAW07 = Q_RAW15 = Q_YRS = 0.0

Q_THREE_V = CL_V; Q_ONE_V = BH_V; Q_TWO_V = BH_V; Q_LOW = 1.0; Q_ILOW = Q_ICATCH = Q_I07 = Q_I10 = Q_I11 = 1; Q_C0 = Q_C1 = 1
