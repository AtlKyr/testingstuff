AUDIO = "final_mix_26.wav"
_R = json.load(open("results26.json"))
_c = pd.read_csv("sim26.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["eq"].values          # RED-MORNING SITTER (SPY opens <= -1% vs prior close -> sell at that open, buy back next open)
BV = _c["bh"].values          # JUST HOLD = buy & hold same dates (from 2005-01-03)
INN = _c["inm"].values.astype(bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert round(RULE_V, -3) == 51000 and round(HOLD_V, -3) == 70000
assert _R["per_year"]["2008"] == 31 and _R["higher"] / _R["trades"] > 0.5
assert _R["fees"]["0"] < HOLD_V and all(v < HOLD_V for v in _R["scan"].values())
TOPD = dict((p[0], p) for p in _R["top"])
assert round(TOPD["2008-10-10"][2] * 100) == 8 and TOPD["2008-10-10"][1] == "2008-10-13"


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


assert RV[di("2011-12-30")] > BV[di("2011-12-30")]
assert RV[di("2016-12-30")] < BV[di("2016-12-30")]
SELLI = [i for i in range(1, N) if INN[i - 1] and not INN[i]]
assert len(SELLI) == _R["trades"]
HIGHER = _R["higher"]; TRADES = _R["trades"]
