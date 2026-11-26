AUDIO = "final_mix_50.wav"
_R = json.load(open("results50.json"))
_c = pd.read_csv("sim50.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["put"].values; SV = _c["worth"].values; NF = HV; FE = SV
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
BMID = BLO = BUP = CL
S0 = 0
CL_V = _R["final"]; MS_V = CL_V; BH_V = 20000.0; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


BF_ROWS = _R["rows"]; BF_I = [di(r["bf"]) for r in BF_ROWS]; BF_W = [r["worth"] for r in BF_ROWS]; BF_UP = [r["day"] > 0 for r in BF_ROWS]
MS_SI = []; MS_BI = []; MS_LV = []; MTR = []; MS_HIGHER = []
TOPC = CL; BOTC = CL; CTR = []; TB_I = []; TS_I = []; CWIN = []
INN = np.ones(N, bool); TRD = []; TWIN = []
QB08 = di("2008-11-28"); QEVEN = di("2011-10-03"); QDBL = di("2017-06-01"); QC0 = di("2020-02-19"); QC1 = di("2020-03-23")
VAR = {"21": 0, "126": 0}
# spoken / shown numbers asserted against the backtest before TTS
assert _R["up_days"] == 10 and len(BF_ROWS) == 20
assert round(CL_V, -2) == 79900 and round(80000 - CL_V) == 138
assert max(BF_W) == BF_W[3] and BF_ROWS[3]["bf"] == "2008-11-28" and 8.5 < BF_W[3] / 1000 < 9.0
assert abs(SV[QEVEN] / HV[QEVEN] - 1) < 0.01 and HV[QEVEN] == 6000
assert SV[QDBL] >= 2 * HV[QDBL] and not any((SV[:QDBL] >= 2 * HV[:QDBL]) & (HV[:QDBL] > 0))
assert 0.32 < 1 - SV[QC1] / SV[QC0] < 0.35
assert round(-BF_ROWS[3]["dd"] * 100) == 42


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Black"), (3, "up"), (5, "ten"), (8, "Doubled,"), (9, "A?"), (11, "four"), (13, "B?"), (14, "Every"), (22, "thousand"),
               (25, "SPY,"), (29, "mall."), (30, "One"), (34, "steal"), (37, "Then"), (40, "eight"), (42, "Six"), (51, "even."),
               (52, "It"), (53, "doubles"), (60, "seventeen."), (61, "Twenty"), (64, "third"), (68, "month."), (69, "Now,"), (72, "scary"),
               (74, "Black"), (78, "eight."), (79, "Stocks"), (84, "crash."), (85, "Nobody's"), (87, "That"), (91, "grows"), (93, "nine"),
               (96, "best"), (100, "twenty."), (101, "Final"), (103, "Twenty"), (106, "Seventy-nine"), (111, "Four"), (115, "thirty-eight"),
               (118, "The"), (122, "deal"), (127, "store.")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Black=wi(0), up=wi(3), ten=wi(5), Doubled=wi(8), A=wi(9), four=wi(11), B=wi(13), Every=wi(14), thousand=wi(22), SPY=wi(25),
    mall=wi(29), One=wi(30), steal=wi(34), Then=wi(37), eight=wi(40), Six=wi(42), even=wi(51), It52=wi(52), doubles=wi(53),
    seventeen_=wi(60), Twenty20=wi(61), third=wi(64), month=wi(68), Now=wi(69), scary=wi(72), BF08=wi(74), eight2=wi(78),
    Stocks=wi(79), crash=wi(84), Nobody=wi(85), That=wi(87), grows=wi(91), nine=wi(93), best=wi(96), all20=wi(100), Final=wi(101),
    Twenty=wi(103), seventynine=wi(106), Verd=wi(111), thirtyeight=wi(115), The=wi(118), deal=wi(122), big=wi(127),
)
T["rev1"] = T["Twenty"] + 0.1
T["rev2"] = T["seventynine"] + 0.1
T["follow"] = END + 0.1
T["seventeen"] = T["big"]; T["Round"] = T["Verd"]; T["Selling"] = T["The"]
for _k in ("Two", "threefifty", "fiftyfour", "Worth", "October", "Circle", "just", "Oct2", "Oct3", "front", "last", "never",
           "dodging", "Covid", "lose", "Up", "down", "up2", "sixtytwo", "ahead", "bottom", "choppy", "sixteenth", "It2", "forty",
           "buy", "sell", "rule", "In", "Trade", "It"):
    T.setdefault(_k, 0.0)
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
