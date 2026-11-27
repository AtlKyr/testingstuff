AUDIO = "final_mix_53.wav"
_R = json.load(open("results53.json"))
_c = pd.read_csv("sim53.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["B"].values; SV = _c["A"].values; NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values; RAWO = _s["Open"].values
HI = _s["High"].values * _f; LO = _s["Low"].values * _f
BMID = BLO = BUP = CL
S0 = 0
CL_V = _R["A"]; MS_V = CL_V; BH_V = _R["B"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []
SARV = CL; UPV = np.ones(N, bool)


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


RW = _R["rows"]
RA = [di(r["a_buy"]) for r in RW]; RB = [di(r["b_buy"]) for r in RW]; RL = [di(r["low"]) for r in RW]; RS = [di(r["sig"]) for r in RW]
REC = np.maximum.accumulate(RAWC)
E_I = np.array([], int); E_PX = []; E_BI = []; E_BPX = []; E_HI = np.array([], bool)
PTR = []; P_B = []; P_S = []; P_HI = []
MS_SI = []; MS_BI = []; MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
TRD = []; TWIN = []
VAR = {"21": 0, "126": 0}
I_LEAD = di("2008-12-01"); I_S918 = di("2008-09-18"); I_B919 = di("2008-09-19"); RAW_JUMP = 0.0
# spoken / shown numbers asserted against the backtest before TTS
assert round(CL_V, -2) == 131500 and round(BH_V, -2) == 147600 and _R["a_wins"] == 3 and _R["n"] == 4
assert RW[0]["b_vs_a"] < -0.25 and RW[0]["b_vs_a_raw"] < -0.25 and RW[0]["low_dd"] < -0.5 and RW[0]["b_buy"].startswith("2008-12")
assert RW[3]["days_wait"] > 230 and RW[1]["b_vs_a"] > 0 and RW[3]["b_vs_a_raw"] > 0 and RW[2]["a_end"] > RW[2]["b_end"]
assert RW[1]["a_buy"] == "2018-12-26" and RW[0]["a_buy"].startswith("2008-07")




def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, 'Down'), (1, 'twenty'), (3, 'Buy'), (5, 'bear?'), (6, 'Buy'), (8, 'A?'), (10, 'wait,'), (11, 'B?'), (12, 'Since'), (16, 'four'), (19, 'One'), (22, 'settles'), (24, 'Twin'), (29, 'ten'), (32, 'SPY'), (38, 'record.'), (39, 'Twin'), (41, 'waits'), (45, 'bull:'), (46, 'twenty'), (50, 'lowest'), (51, 'close.'), (52, 'Christmas,'), (55, 'A'), (59, 'bottom.'), (60, 'B'), (62, 'more.'), (63, 'Twenty'), (65, 'A'), (67, 'again.'), (68, 'Twenty'), (70, 'B'), (72, 'almost'), (77, 'more.'), (78, 'Three'), (81, 'A.'), (82, 'Now,'), (84, 'bear'), (88, 'July,'), (92, 'A'), (93, 'buys.'), (94, 'Then'), (96, 'sinks'), (98, 'half'), (101, 'B'), (104, 'December:'), (105, 'over'), (107, 'quarter'), (109, 'Final'), (115, 'one'), (123, 'one'), (129, 'Three'), (131, 'lost'), (134, 'patient')]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(Down=wi(0), twenty=wi(1), Buy=wi(3), bear=wi(5), Buy2=wi(6), A=wi(8), wait=wi(10), B=wi(11), Since=wi(12), four=wi(16), One=wi(19), settles=wi(22), TwinA=wi(24), ten=wi(29), SPY=wi(32), record=wi(38), TwinB=wi(39), waits=wi(41), bull=wi(45), twenty2=wi(46), lowest=wi(50), close=wi(51), Xmas=wi(52), A18=wi(55), bottom=wi(59), B18=wi(60), more18=wi(62), Tw20=wi(63), A20=wi(65), again=wi(67), Tw22=wi(68), B22=wi(70), almost=wi(72), more22=wi(77), Three=wi(78), Around=wi(81), Now=wi(82), bear2=wi(84), July=wi(88), A08=wi(92), buys08=wi(93), Then=wi(94), sinks=wi(96), half=wi(98), B08=wi(101), December=wi(104), over=wi(105), quarter=wi(107), Final=wi(109), one1=wi(115), one2=wi(123), Verd=wi(129), lost=wi(131), patient=wi(134))
T["rev1"] = T["one1"] + 0.1
T["rev2"] = T["one2"] + 0.1
T["follow"] = END + 0.1
T["big"] = T["patient"]; T["safe"] = T["lost"]; T["Twenty"] = T["Final"]
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
