AUDIO = "final_mix_44.wav"
_R = json.load(open("results44.json"))
_c = pd.read_csv("sim44.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True).loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
VV = _c["V"].values; PP = _c["P"].values
HV = VV; SV = PP; NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
CLALL = _a["Adj Close"].values; DALL = _a.index
S0 = 0
LEFT_V = _R["final"]; OUT_V = _R["withdrawn"]; LOW_V = _R["low"]
HOLD_V = LEFT_V; RULE_V = OUT_V; ONE_V = HOLD_V; TWO_V = RULE_V; REIN_V = HOLD_V; POCK_V = RULE_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


I_LOW = di(_R["low_d"]); I_SOLD = di(_R["panic_sold"]); I_BROKE = di(_R["panic_broke"]); I_BACK = di(_R["back1m"])
# spoken numbers -> asserted against the backtest before TTS
assert round(LOW_V, -3) == 411000 and round(LEFT_V, -5) == 2300000 and round(OUT_V, -3) == 822000
assert _R["panic_sold"].startswith("2008-11") and _R["panic_broke"].startswith("2019") and _R["back1m"].startswith("2014")
assert DATES[0] == pd.Timestamp("2007-10-09") and abs(_R["w0"] - 40000) < 1


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "A"), (1, "million"), (3, "retired"), (7, "Broke"), (10, "A?"), (13, "B?"), (14, "And"), (17, "twin."), (18, "October"),
               (27, "record"), (29, "He"), (33, "four"), (36, "forty"), (41, "then"), (44, "inflation."), (45, "All"), (47, "SPY."),
               (48, "His"), (51, "Then"), (56, "By"), (66, "four"), (68, "eleven"), (72, "paychecks"), (75, "Here"), (78, "split."),
               (79, "And"), (83, "sold"), (86, "November"), (91, "losing"), (93, "Safe"), (96, "In"), (100, "money"), (102, "out."),
               (103, "Our"), (105, "never"), (107, "Back"), (113, "twenty"), (115, "End"), (121, "three"), (127, "eight"),
               (131, "Worst"), (134, "Still"), (135, "richer.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    million=wi(1), retired=wi(3), Broke=wi(7), A=wi(10), B=wi(13), And=wi(14), twin=wi(17), October=wi(18), record=wi(27), He=wi(29),
    four=wi(33), forty=wi(36), then=wi(41), inflation=wi(44), All=wi(45), SPY=wi(47), His=wi(48), Then=wi(51), By=wi(56),
    four2=wi(66), eleven=wi(68), paychecks=wi(72), Here=wi(75), split=wi(78), And2=wi(79), sold=wi(83), November=wi(86),
    losing=wi(91), Safe=wi(93), In=wi(96), money=wi(100), out=wi(102), Our=wi(103), never=wi(105), Back=wi(107), fourteen=wi(113),
    End=wi(115), three=wi(121), eight=wi(127), Worst=wi(131), Still=wi(134), richer=wi(135),
)
T["rev1"] = T["three"] + 0.1
T["rev2"] = T["eight"] + 0.1
T["follow"] = END + 0.1
CHK_D = "2008-12-19"
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
