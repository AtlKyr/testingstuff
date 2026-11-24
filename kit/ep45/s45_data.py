AUDIO = "final_mix_45.wav"
_R = json.load(open("results45.json"))
_c = pd.read_csv("sim45.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["H"].values; SV = _c["S"].values; NF = HV; FE = SV
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
_ma = _a["Adj Close"].rolling(20).mean(); _sd = _a["Adj Close"].rolling(20).std()
BMID = _ma.loc[_c.index[0]:].values; BLO = (_ma - 2 * _sd).loc[_c.index[0]:].values; BUP = (_ma + 2 * _sd).loc[_c.index[0]:].values
S0 = 0
BB_V = _R["final"]; BH_V = _R["bh"]
HOLD_V = BH_V; RULE_V = BB_V; ONE_V = BH_V; TWO_V = BB_V; REIN_V = BH_V; POCK_V = BB_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


TRD = _R["trades"]
TB_I = [di(x[0]) for x in TRD]; TS_I = [di(x[1]) for x in TRD]; TWIN = [x[4] > 0 for x in TRD]
INN = np.zeros(N, bool)
for a_, b_ in zip(TB_I, TS_I):
    INN[a_:b_] = True
I_SEPB = di("2008-09-05"); I_OCTS = di("2008-10-31"); I_LEH = di("2008-09-15")
SEP_R = [x for x in TRD if x[0] == "2008-09-05"][0][4]
# spoken numbers -> asserted against the backtest before TTS
assert _R["wins"] == 65 and _R["n"] - _R["wins"] == 20 and round(BB_V, -3) == 20000 and round(BH_V, -3) == 72000
assert -0.23 < SEP_R < -0.22 and TRD[[x[0] for x in TRD].index("2008-09-05")][1] == "2008-10-31"
assert SV[di("2009-03-09")] > 1.3 * HV[di("2009-03-09")]
assert INN[di("2010-01-04"):].mean() < 0.2 + 0.01


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Sixty-five"), (2, "Only"), (5, "Bollinger,"), (6, "A?"), (10, "B?"), (11, "Watch"), (13, "September"), (15, "Two"),
               (20, "The"), (28, "Buy"), (32, "Back"), (37, "Sell."), (38, "Ten"), (47, "Small"), (51, "Then"), (56, "market"),
               (58, "The"), (62, "half"), (65, "By"), (72, "ahead"), (77, "So"), (81, "That"), (85, "bought"), (88, "fifth,"),
               (92, "Then"), (93, "Lehman"), (95, "Sold"), (101, "twenty-two"), (103, "One"), (108, "eight"), (111, "After"),
               (113, "Cash"), (119, "Final"), (124, "twenty"), (129, "seventy-two"), (131, "Winning"), (135, "big.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    sixtyfive=wi(0), Only=wi(2), twenty=wi(3), Bollinger=wi(5), A=wi(6), B=wi(10), Watch=wi(11), September=wi(13), Two=wi(15),
    rule=wi(21), Buy=wi(28), Back=wi(32), Sell=wi(37), Ten=wi(38), SPY=wi(42), Small=wi(47), wins2=wi(50), Then=wi(51),
    crashes=wi(57), half=wi(62), By=wi(65), ahead=wi(72), So=wi(77), work=wi(80), That=wi(81), bought=wi(85), fifth=wi(88),
    Then2=wi(92), Lehman=wi(93), Sold=wi(95), October=wi(98), twentytwo=wi(101), One=wi(103), eight=wi(108), After=wi(111),
    Cash=wi(113), five=wi(118), Final=wi(119), twentyk=wi(124), seventytwo=wi(129), Winning=wi(131), big=wi(135),
)
T["rev1"] = T["twentyk"] + 0.1
T["rev2"] = T["seventytwo"] + 0.1
T["follow"] = END + 0.1
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
