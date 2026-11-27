AUDIO = "final_mix_54.wav"
_R = json.load(open("results54.json"))
_c = pd.read_csv("sim54.csv", index_col=0, parse_dates=True)
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


YR = {r["y"]: r for r in _R["years"]}
REC = np.maximum.accumulate(RAWC)
RW = [dict(a_end=0, b_end=0)] * 4; RA = RB = RL = RS = [0, 0, 0, 0]
E_I = np.array([], int); E_PX = []; E_BI = []; E_BPX = []; E_HI = np.array([], bool)
PTR = []; P_B = []; P_S = []; P_HI = []
MS_SI = []; MS_BI = []; MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
TRD = []; TWIN = []
VAR = {"21": 0, "126": 0}
I_LEAD = di("2008-11-20"); I_S918 = di("2008-09-18"); I_B919 = di("2008-09-19"); RAW_JUMP = 0.0
I_F20 = di("2020-02-03"); I_E20 = di("2020-12-31")
RAW20 = RAWC[I_E20] / RAWC[di("2020-01-31")] - 1
# spoken / shown numbers asserted against the backtest before TTS
assert round(CL_V, -2) == 29900 and round(BH_V, -2) == 70200
assert len(_R["jan_down"]) == 10 and len(_R["jan_down_rest_up"]) == 8
assert round(YR[2020]["jan"] * 10000) == -4 and YR[2020]["rest"] > 0.15 and RAW20 > 0.15 and YR[2009]["jan"] < 0 and YR[2008]["jan"] < 0
assert (SV / HV)[I_LEAD] > 1.5 and YR[2009]["rest"] > 0.3



def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, 'Red'), (1, 'January.'), (2, 'Skip'), (5, 'eleven'), (7, 'Skip,'), (8, 'A?'), (10, 'stay,'), (11, 'B?'), (12, 'Wall'), (16, 'as'), (19, 'so'), (23, 'Keep'), (28, 'quiet'), (30, 'The'), (32, 'red'), (34, 'sell'), (37, 'sit'), (41, 'next'), (43, 'Ten'), (46, 'twenty'), (48, 'January'), (52, 'red.'), (55, 'sells'), (57, 'dodges'), (60, 'By'), (62, 'November,'), (64, 'way'), (66, 'Two'), (69, 'red'), (73, 'sits'), (78, 'rockets'), (81, 'In'), (82, 'ten'), (90, 'rose'), (91, 'eight'), (93, 'Now,'), (95, 'quiet'), (97, 'Twenty'), (99, 'January'), (102, 'four'), (107, 'The'), (109, 'sells.'), (110, 'The'), (115, 'climbs'), (117, 'fifteen'), (119, 'Twenty'), (124, 'twenty-nine'), (128, 'Just'), (130, 'seventy'), (134, 'January'), (136, 'predicted')]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(Red=wi(0), Jan=wi(1), Skip=wi(2), eleven=wi(5), Skip2=wi(7), A=wi(8), stay=wi(10), B=wi(11), Wall=wi(12), As=wi(16), so=wi(19), Keep=wi(23), quiet=wi(28), Rule=wi(30), red1=wi(32), sell=wi(34), sit=wi(37), next=wi(41), Ten=wi(43), twenty=wi(46), Jan08=wi(48), red08=wi(52), sells08=wi(55), dodges=wi(57), By=wi(60), November=wi(62), way=wi(64), Two9=wi(66), red09=wi(69), sits=wi(73), rockets=wi(78), In=wi(81), ten=wi(82), rose=wi(90), eight=wi(91), Now=wi(93), quiet2=wi(95), Tw20=wi(97), Jan20=wi(99), four=wi(102), The107=wi(107), sells20=wi(109), The110=wi(110), climbs=wi(115), fifteen=wi(117), Twenty=wi(119), twentynine=wi(124), Just=wi(128), seventy=wi(130), Verd=wi(134), predicted=wi(136))
T["rev1"] = T["twentynine"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["big"] = T["predicted"]; T["safe"] = T["Verd"]; T["lost"] = T["Verd"]; T["Final"] = T["Twenty"]
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
