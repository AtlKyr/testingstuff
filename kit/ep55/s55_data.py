AUDIO = "final_mix_55.wav"
_R = json.load(open("results55.json"))
_c = pd.read_csv("sim55.csv", index_col=0, parse_dates=True)
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
# ---- #55: sell after a -5% week, buy back after a +5% week
Q_RT = _R["rt"]
Q_SELL = [di(r["sell"]) for r in Q_RT]; Q_BUY = [di(r["buy"]) for r in Q_RT]
Q_S07, Q_B08, Q_S15, Q_B20 = di("2007-07-30"), di("2008-10-20"), di("2015-08-24"), di("2020-03-30")
Q_RAW07 = RAWO[Q_B08] / RAWO[Q_S07] - 1; Q_ADJ07 = OP[Q_B08] / OP[Q_S07] - 1
Q_RAW15 = RAWO[Q_B20] / RAWO[Q_S15] - 1; Q_ADJ15 = OP[Q_B20] / OP[Q_S15] - 1
Q_YRS = (DATES[Q_B20] - DATES[Q_S15]).days / 365.25
Q_LEAD08 = (SV / HV)[di("2008-12-31")]
Q_SCAN = _R["scan"]
# spoken / shown numbers asserted against the backtest before TTS
assert round(CL_V, -2) == 51300 and round(BH_V, -2) == 70200
assert -0.36 < Q_RAW07 < -0.31 and -0.36 < Q_ADJ07 < -0.31          # "a third cheaper" (raw AND adjusted)
assert Q_RAW15 > 1 / 3 and Q_ADJ15 > 1 / 3                           # "over a third higher" (raw AND adjusted)
assert 4.5 <= Q_YRS < 4.75 and Q_RT[7]["sell"] == "2015-08-24"     # "four and a half years"
assert len([r for r in Q_RT if "2008-10" <= r["sell"] <= "2011-10"]) == 6   # six round trips in three years
assert Q_LEAD08 > 1.2 and abs(7297.49 / 6910.39 - 1.056) < 0.001


def wi(i):
    return WORDS[i]["start"]


_A = [(0, 'Up'), (1, 'five'), (4, 'percent.'), (5, 'Time'), (8, 'back?'), (9, 'Sell'), (12, 'A?'), (15, 'hold,'), (16, 'B?'), (17, 'One'),
      (19, 'wait'), (22, 'Down'), (27, 'week:'), (28, 'sell.'), (29, 'Up'), (31, 'buy'), (33, 'It'), (34, 'sold'), (37, 'It'), (38, 'buys'),
      (40, 'this'), (42, 'Twenty'), (44, 'ten'), (47, 'Two'), (49, 'eight:'), (51, 'sells'), (54, 'buys'), (57, 'third'), (59, 'Holding'),
      (61, 'foolish.'), (62, 'Then'), (64, 'whiplash.'), (65, 'Out,'), (66, 'in,'), (67, 'out,'), (68, 'in,'), (69, 'six'), (73, 'three'),
      (75, 'Now,'), (78, 'long'), (80, 'August'), (82, 'fifteen:'), (87, 'down.'), (89, 'sells.'), (90, 'The'), (91, 'next'), (98, 'four'),
      (101, 'half'), (103, 'It'), (108, 'Covid'), (110, 'then'), (111, 'buys'), (115, 'third'), (116, 'higher.'), (117, 'Twenty'),
      (120, 'seller,'), (121, 'fifty-one'), (125, 'Holder,'), (126, 'seventy'), (130, 'The'), (131, 'crash'), (135, 'The'), (136, 'waiting'), (137, 'did.')]
for _i, _w in _A:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(Up=wi(0), five0=wi(1), pct0=wi(4), Time=wi(5), back0=wi(8), Sell=wi(9), A=wi(12), hold=wi(15), B=wi(16), One=wi(17), wait0=wi(19),
         Down=wi(22), week1=wi(27), sell=wi(28), Up2=wi(29), buyb=wi(31), It33=wi(33), sold=wi(34), It37=wi(37), buys37=wi(38), this=wi(40),
         Twenty=wi(42), ten=wi(44), Two=wi(47), eight=wi(49), sells08=wi(51), buys08=wi(54), third=wi(57), Holding=wi(59), foolish=wi(61),
         Then=wi(62), whiplash=wi(64), o1=wi(65), i1=wi(66), o2=wi(67), i2=wi(68), six=wi(69), three=wi(73), Now=wi(75), long2=wi(78),
         August=wi(80), fifteen=wi(82), down=wi(87), sells15=wi(89), The90=wi(90), next=wi(91), four=wi(98), half=wi(101), It103=wi(103),
         Covid=wi(108), then=wi(110), buys111=wi(111), third2=wi(115), higher=wi(116), Tw117=wi(117), seller=wi(120), fiftyone=wi(121),
         Holder=wi(125), seventy=wi(126), Verd=wi(130), crashV=wi(131), The135=wi(135), waiting=wi(136), did=wi(137))
T["rev1"] = T["fiftyone"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["big"] = T["The135"]; T["safe"] = T["Verd"]; T["lost"] = T["Verd"]; T["Final"] = T["Tw117"]
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
