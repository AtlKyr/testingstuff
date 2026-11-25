AUDIO = "final_mix_47.wav"
_R = json.load(open("results47.json"))
_c = pd.read_csv("sim47.csv", index_col=0, parse_dates=True)
_a = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
_s = _a.loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["H"].values; SV = _c["S"].values; NF = HV; FE = SV
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
BMID = BLO = BUP = CL
S0 = 0
SO_V = _R["final"]; MS_V = SO_V; BH_V = _R["bh"]; BB_V = MS_V
HOLD_V = BH_V; RULE_V = MS_V; ONE_V = BH_V; TWO_V = MS_V; REIN_V = BH_V; POCK_V = MS_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


YR = {int(k): v for k, v in _R["yret"].items()}
OUTY = _R["out"]
YFIRST = {y: int(np.where(DATES.year == y)[0][0]) for y in range(2005, 2025)}
MS_SI = [YFIRST[y] for y in OUTY]; MS_BI = [YFIRST[y + 1] if y + 1 in YFIRST else N - 1 for y in OUTY]
MS_LV = OUTY; MTR = []; MS_HIGHER = []
INN = _c["INM"].values.astype(bool)
TB_I = MS_BI; TS_I = MS_SI; TRD = []; TWIN = []
I_TOP07 = di("2007-10-09"); I_14S = I_14B = 0
THS = _R["ths"]
VAR = {"21": 0, "126": 0}
# spoken numbers -> asserted against the backtest before TTS
assert OUTY == [2010, 2014, 2018, 2020, 2022, 2024] and sum(YR[y] > 0 for y in OUTY) == 4
assert round(YR[2024] * 100) == 25 and YR[2023] >= 0.2 and YR[2009] >= 0.2 and YR[2010] > 0 and YR[2022] < 0
assert round(SO_V, -2) == 46600 and round(BH_V, -2) == 70200
assert all(v < BH_V for v in THS.values())


def wi(i):
    return WORDS[i]["start"]


for _i, _w in [(0, "Up"), (1, "twenty"), (3, "Sit"), (7, "Cash"), (9, "A?"), (11, "stay"), (13, "B?"), (14, "Watch"), (17, "last"),
               (19, "Everyone"), (22, "what"), (24, "up"), (25, "must"), (27, "down."), (28, "So"), (31, "twenty"), (37, "cash"),
               (43, "Twenty"), (44, "ten:"), (46, "skips"), (50, "climbs"), (52, "Twenty"), (53, "fourteen,"), (55, "eighteen,"),
               (57, "twenty:"), (60, "Four"), (69, "up."), (70, "Then"), (72, "twenty-two."), (78, "bear"), (80, "Finally,"),
               (84, "smart."), (85, "So"), (90, "warn"), (92, "And"), (95, "last"), (97, "After"), (99, "huge"), (101, "twenty-three,"),
               (103, "skips"), (105, "twenty-four."), (107, "soars"), (108, "twenty-five"), (110, "Without"), (112, "The"),
               (116, "forty-six"), (122, "seventy"), (126, "Big"), (129, "warnings."), (132, "big")]:
    assert WORDS[_i]["text"] == _w, (_i, WORDS[_i]["text"], _w)
T = dict(
    Up=wi(0), twenty=wi(1), Sit=wi(3), Cash=wi(7), A=wi(9), stay=wi(11), B=wi(13), Watch=wi(14), last=wi(17), Everyone=wi(19),
    what=wi(22), up=wi(24), must=wi(25), down=wi(27), So=wi(28), twentyp=wi(31), cash=wi(37), Twenty10=wi(43), ten=wi(44),
    skips=wi(46), climbs=wi(50), Twenty14=wi(52), fourteen=wi(53), eighteen=wi(55), twenty20=wi(57), Four=wi(60), up2=wi(69),
    Then=wi(70), tt22=wi(72), bear=wi(78), Finally=wi(80), smart=wi(84), So2=wi(85), warn=wi(90), And=wi(92), last2=wi(95),
    After=wi(97), huge=wi(99), tt23=wi(101), skips2=wi(103), tt24=wi(105), soars=wi(107), tf=wi(108), Without=wi(110),
    The=wi(112), fortysix=wi(116), seventy=wi(122), Big=wi(126), warnings=wi(129), big=wi(132),
)
T["rev1"] = T["fortysix"] + 0.1
T["rev2"] = T["seventy"] + 0.1
T["follow"] = END + 0.1
T["seventeen"] = T["big"]; T["Round"] = T["Big"]; T["Selling"] = T["warnings"] + 0.4
for _k in ("Two", "threefifty", "four"):
    T.setdefault(_k, 0.0)
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
M50 = CL; M200 = CL
TR = []; SELL_I = []; BUY_I = []; CROSS_I = []
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07 = R20 = 0
ROWS = json.load(open("../ep43/results43.json"))["rows"]; RI = []; WINB = []
CUMA = np.zeros(N); CUMB = np.zeros(N); X0 = 0; XEND = N - 1; I_M09 = I_M09P = I_M24 = I_A06 = 1; A_V = B_V = 0
