AUDIO = "final_mix_46.wav"
_R = json.load(open("results46.json"))
_c = pd.read_csv("sim46.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["H"].values; SV = _c["S"].values; NF = HV; FE = SV
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
BMID = BLO = BUP = CL
S0 = 0
MS_V = _R["final"]; BH_V = _R["bh"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


MTR = _R["trades"]
MS_SI = [di(x["sell"]) for x in MTR]; MS_BI = [di(x["buy"]) if "buy" in x else N - 1 for x in MTR]
MS_LV = [x["lvl"] for x in MTR]
MS_HIGHER = [("bp" in x) and x["bp"] > x["sp"] for x in MTR]
INN = _c["INM"].values.astype(bool)
TB_I = MS_BI; TS_I = MS_SI; TRD = []; TWIN = []
I_M07S, I_M07B, I_TOP07, I_LOW09 = di("2007-05-04"), di("2007-08-03"), di("2007-10-09"), di("2009-03-09")
I_14S, I_14B = di("2014-08-26"), di("2014-11-24")
VAR = _R["var"]
# spoken numbers -> asserted against the backtest before TTS
assert len(MTR) == 10 and sum(MS_HIGHER) == 7 and sum("buy" in x for x in MTR) == 9
assert round(MS_V, -2) == 52700 and round(BH_V, -2) == 70200 and BH_V - MS_V > 17000
assert MTR[0]["sell"] == "2007-05-04" and MTR[0]["buy"] == "2007-08-03" and MTR[0]["bp"] < MTR[0]["sp"]
assert MTR[1]["lvl"] == 200 and MTR[1]["bp"] > MTR[1]["sp"]
assert all(MS_HIGHER[MS_LV.index(l)] for l in (250, 350, 400))
assert abs(_R["dd"] - _R["bhdd"]) < 1e-6
assert VAR["21"] > BH_V and VAR["126"] < BH_V


def wi(i):
    return WORDS[i]["start"]



for _i, _w in [(0, "Dow,"), (1, "fifty"), (3, "SPY"), (5, "ten"), (8, "Sell"), (11, "A?"), (12, "Hold,"), (13, "B?"), (14, "One"),
               (20, "eight."), (21, "Each"), (26, "headline:"), (28, "top"), (31, "So"), (33, "sells"), (38, "buys"), (40, "three"),
               (43, "SPY"), (45, "two"), (48, "sells."), (49, "Three"), (54, "more"), (59, "Two"), (61, "three"), (63, "four"),
               (65, "same"), (67, "Seven"), (74, "higher."), (75, "And"), (82, "May"), (87, "sells,"), (91, "cheaper."),
               (92, "Genius?"), (97, "August,"), (102, "top."), (103, "So"), (107, "never"), (110, "Now,"), (113, "Milestone"),
               (115, "fifty-two"), (119, "Just"), (121, "seventy"), (125, "Round"), (128, "headlines."), (129, "Selling"),
               (133, "seventeen")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Dow=wi(0), fifty=wi(1), SPY=wi(3), ten=wi(5), Sell=wi(8), A=wi(11), Hold=wi(12), B=wi(13), One=wi(14), eight=wi(20),
    Each=wi(21), headline=wi(26), top=wi(28), So=wi(31), sells=wi(33), buys=wi(38), three=wi(40), SPY2=wi(43), two=wi(45),
    sells2=wi(48), Three=wi(49), more=wi(54), Two=wi(59), threefifty=wi(61), four=wi(63), same=wi(65), Seven=wi(67),
    higher=wi(74), And=wi(75), May=wi(82), sells3=wi(87), cheaper=wi(91), Genius=wi(92), August=wi(97), top2=wi(102),
    So2=wi(103), never=wi(107), Now=wi(110), Milestone=wi(113), fiftytwo=wi(115), Just=wi(119), seventy=wi(121),
    Round=wi(125), headlines=wi(128), Selling=wi(129), seventeen=wi(133), big=wi(133),
)
T["rev1"] = T["fiftytwo"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
