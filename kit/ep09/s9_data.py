AUDIO = "final_mix_09.wav"
_R = json.load(open("results9.json"))
_c = pd.read_csv("sim9.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # STAYER = buy & hold (never sells)
JV = _c["M10"].values        # JUMPER = misses the 10 best days
BH_V = _R["bh"]["v"]; J_V = _R["miss_best_10"]["v"]; BOTH_V = _R["miss_both_10"]["v"]
GAP_PCT = _R["gap_pct_final"]
BEST = [pd.Timestamp(d["d"]) for d in _R["best10"]]
WORST = [pd.Timestamp(d["d"]) for d in _R["worst10"]]
NEAR = _R["best10_within_10_tdays_of_worst10"]          # 7
_df = pd.read_csv("../spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
SPYC = _df["Adj Close"].values
RET = _df["Adj Close"].pct_change().fillna(0).values
DDV = (_df["Adj Close"] / _df["Adj Close"].cummax() - 1).values
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


def crash_zones(th=-0.20):
    z, a = [], None
    for i, v in enumerate(DDV):
        if v <= th and a is None:
            a = i
        if v > th * 0.5 and a is not None:      # zone ends when drawdown recovers above -10%
            z.append((a, i)); a = None
    if a is not None:
        z.append((a, N - 1))
    return z
ZONES = crash_zones()
