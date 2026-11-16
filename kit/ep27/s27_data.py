AUDIO = "final_mix_27.wav"
_R = json.load(open("results27.json"))
_c = pd.read_csv("sim27.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
AV = _c["A"].values          # A: buys $500 at the open of the first trading day of every month
BV = _c["B"].values          # B: waits for a day that closes >= 1% down, buys at that close (cash rolls over)
CASHB = _c["cash"].values; PUT = _c["put"].values
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
RET = np.r_[0, CL[1:] / CL[:-1] - 1]
S0 = 0
A_V = _R["A"]; B_V = _R["B"]
assert round(A_V, -3) == 490000 and round(B_V, -3) == 488000 and _R["put"] == 120000


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


_y17 = slice(di("2017-01-03"), di("2017-12-29") + 1)
RED17 = [i for i in range(_y17.start, _y17.stop) if RET[i] <= -0.01]
assert len(RED17) == 4
_sep, _buy = di("2017-09-01"), di("2018-01-30")
assert RET[_buy] <= -0.01 and all(RET[i] > -0.01 for i in range(_sep + 1, _buy)) and CASHB[_buy - 1] == 2500
assert round((CL[_buy] / OP[_sep] - 1) * 100) == 15
assert BV[di("2008-12-31")] > AV[di("2008-12-31")]
GAP = A_V - B_V
