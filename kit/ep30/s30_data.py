AUDIO = "final_mix_30.wav"
_R = json.load(open("results30.json"))
_EV = json.load(open("events30.json"))
_c = pd.read_csv("sim30.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
AV = _c["K"].values          # A: knife catcher, $1,000 at the open after the 4th straight red close
BV = _c["W"].values          # B: waits for the first green close, $1,000 at the next open
PUT = _c["PUT"].values
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
RET = np.r_[0, CL[1:] / CL[:-1] - 1]
S0 = 0
A_V = _R["K"]; B_V = _R["W"]; GAP = A_V - B_V
assert round(A_V, -3) == 450000 and round(B_V, -3) == 448000 and _R["put"] == 107000 and A_V > B_V
assert _R["events"] == 107 and _R["paid_more"] == 70


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


_e18 = [e for e in _EV if e["sig"] == "2018-12-18"][0]
_e08 = [e for e in _EV if e["sig"] == "2008-10-07"][0]
assert round(-100 * _e18["cost"]) == 4 and round(100 * _e08["cost"]) == 7
K18, W18 = di(_e18["k_date"]), di(_e18["w_date"])
K08, W08 = di(_e08["k_date"]), di(_e08["w_date"])
ROCKET = di("2008-10-13")
assert RET[ROCKET] == RET[1:].max() and round(RET[ROCKET] * 100, 1) == 14.5
assert all(RET[i] < 0 for i in range(K08, K08 + 3))   # three more red closes after A's buy
SCAN3 = _R["scan"]["3"]; SCAN5 = _R["scan"]["5"]
