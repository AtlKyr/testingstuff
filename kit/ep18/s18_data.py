AUDIO = "final_mix_18.wav"
_R = json.load(open("results18.json"))
_c = pd.read_csv("sim18.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["R"].values          # 200-DAY LINE rule (close > SMA200 -> in at next open, else cash)
BV = _c["B"].values          # BUY & HOLD same dates (from 2005-10-18)
PX = _c["P"].values; SMA = _c["SMA"].values; INN = _c["IN"].fillna(0).values
S0 = int(np.argmax(~np.isnan(RV)))
LINE_V = _R["final"]; HOLD_V = _R["bh"]
assert round(LINE_V, -2) == 43800 and round(HOLD_V, -2) == 70900 and round(-_R["y2008"][1]) == 36 and _R["short_trades"] == 41
assert abs(_R["y2008"][0]) < 1 and _R["mdd"] / _R["bh_mdd"] < 0.5 and _R["losing_trades"] > 32
MDD_L, MDD_B = _R["mdd"], _R["bh_mdd"]
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
# fakeout trades (<=10 trading days) and whether they lost: recomputed from the sim (in-position runs)
_runs = []; _st = None
for _i in range(S0 + 1, N):
    _was = INN[_i - 2] if _i >= 2 else 0
    _now = INN[_i - 1]
    if _now == 1 and _was != 1 and _st is None:
        _st = _i
    if _now == 0 and _was == 1 and _st is not None:
        _runs.append((_st, _i)); _st = None
FAKE = [(a, b) for a, b in _runs if b - a <= 10]
FAKE_LOST = [(a, b) for a, b in FAKE if RV[b] <= RV[a - 1]]
