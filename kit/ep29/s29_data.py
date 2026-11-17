AUDIO = "final_mix_29.wav"
_R = json.load(open("results29.json"))
_c = pd.read_csv("sim29.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _s.index
N = len(DATES)
_c = _c.reindex(DATES).ffill().fillna(10000.0)
RV = _c["red"].values          # TURNAROUND TRADER: owns SPY Mon close -> Tue close, only after a red Monday (0.05%/side)
BV = _c["green"].values        # THE TWIN: same, only after a green Monday
CL = _s["Adj Close"].values; OP = CL
S0 = 0
RULE_V = _R["red_final"]; TWIN_V = _R["green_final"]; HOLD_V = _R["bh"]
assert round(TWIN_V, -2) == 5500 and round(RULE_V, -2) == 17400 and round(HOLD_V, -3) == 71000


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


G08 = RV[di("2008-12-31")] / RV[di("2007-12-31")] - 1; T08 = BV[di("2008-12-31")] / BV[di("2007-12-31")] - 1
assert round(G08 * 100) == 26 and T08 < 0
Q09, Q18 = RV[di("2009-12-31")], RV[di("2018-12-31")]
assert Q18 < Q09
INN = np.ones(N, bool)
T = dict(
    Down=wt("Down"), almost=wt("almost"), Monday1=wt("Monday"), Buy=wt("Buy"), Tuesday1=wt("Tuesday"), Real=wt("Real"), A=wt("A"),
    myth=wt("myth"), B=wt("B"), Nine=wt("Nine"), answer=wt("answer"), test=wt("test"), own=wt("own"), Mondays_close=wt("Monday's"),
    Tuesdays_close=wt("Tuesday's"), red1=wt("red"), His=wt("His"), twin1=wt("twin"), green=wt("green"), Mondays=wt("Mondays"),
    Two=wt("Two"), eight=wt("eight"), Red=wt("Red"), jumps=wt("jumps"), twentysix=wt("twenty-six"), twin2=wt("twin", 2),
    sinks=wt("sinks"), So=wt("So"), true=wt("true"), Hold=wt("Hold"), Those=wt("Those"), From=wt("From"), eighteen=wt("eighteen"),
    nothing=wt("nothing"), Then=wt("Then"), Another=wt("Another"), jump=wt("jump"), Final=wt("Final"), fiftyfive=wt("fifty-five"),
    Turnaround=wt("Turnaround"), seventeen=wt("seventeen"), Someone=wt("Someone"), seventyone=wt("Seventy-one"),
    legend2=wt("legend", 2), real=wt("real"), mostly=wt("mostly"), crashes=wt("crashes"),
)
T["rev1"] = T["fiftyfive"] + 0.1
T["rev2"] = T["seventeen"] + 0.1
T["rev3"] = T["seventyone"] + 0.1
T["follow"] = END + 0.1
