AUDIO = "final_mix_36.wav"
_R = json.load(open("results36.json"))
_c = pd.read_csv("sim36.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["bh"].values          # buy & hold $10,000 from the first open
SV = _c["st"].values          # correction rule
NF = HV; FE = SV
INN = _c["IN"].values.astype(bool)
DDN = _c["dd"].values         # nominal close vs its all-time closing high
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; NOM = _s["Close"].values
S0 = 0
HOLD_V = _R["bh"]; RULE_V = _R["st"]
TR = _R["trades"]


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


SELLS = [di(t["sell"]) for t in TR]; BUYS = [di(t["buy"]) for t in TR]
ZONES = list(zip(SELLS, BUYS))
I_XMAS = di("2018-12-24")
SCAN = _R["scan"]
# spoken numbers -> asserted against the backtest before TTS
assert len(_R["episodes"]) == 6 and _R["ntr"] == 6
assert round(-DDN[I_XMAS] * 100, 1) == 20.2 and str(DATES[I_XMAS].date()) == "2018-12-24"
assert round(HOLD_V, -3) == 70000 and round(RULE_V, -3) == 85000
assert [t["why"] for t in TR] == ["bear", "record", "record", "bear", "bear", "bear"]
assert TR[0]["ratio"] < 1 and TR[1]["ratio"] > 1 and TR[2]["ratio"] > 1 and TR[3]["ratio"] < 1
LINE202 = 68575   # rerun of bt36 with the buy-back line at -20.2% (printed 2026-11-21): loses to buy & hold
assert LINE202 < HOLD_V
XMAS_CHEAPER = round((1 - TR[3]["ratio"]) * 100)   # 10
assert XMAS_CHEAPER == 10
