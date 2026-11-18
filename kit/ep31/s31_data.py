AUDIO = "final_mix_31.wav"
_R = json.load(open("results31.json"))
_c = pd.read_csv("sim31.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
RET = np.r_[0, CL[1:] / CL[:-1] - 1]
PR = _c["P"].values; SMA = _c["SMA"].values; IND = _c["IND"].values; INM = _c["INM"].values
S0 = int(np.argmax(~np.isnan(_c["B"].values)))
AV = _c["M"].values          # A: same 200-day rule, checked at each month-end close (fill next open)
BV = _c["B"].values          # B: never checks = buy & hold from the same day
DV = _c["D"].values          # ghost: the daily checker
PUT = np.full(N, 10000.0)
A_V = _R["monthly"]; B_V = _R["bh"]; D_V = _R["daily"]; WK_V = _R["weekly"]
assert _R["trd"] == 64 and round(A_V, -3) == 59000 and round(B_V, -3) == 71000 and A_V > D_V and B_V > A_V
assert _R["trm"] == 12


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


_t22 = [t for t in _R["trades_m"] if t[0][:4] == "2022"]
assert round(-100 * _t22[0][2]) == 9 and _t22[1][2] < 0
LOW09 = di("2009-03-09")
assert round(AV[LOW09] / BV[LOW09], 1) >= 2.0
assert AV[di("2018-12-31")] > BV[di("2018-12-31")]
_ah = np.where((AV > BV) & (np.arange(N) >= di("2008-06-01")))[0]
PASS = int(_ah[-1]) + 1          # day buy & hold passes the monthly checker for good (2022-11)
assert str(DATES[PASS].date())[:7] == "2022-11"
SELL08 = di("2008-01-02")
T22 = [(di(a), di(b)) for a, b, _ in _t22]
