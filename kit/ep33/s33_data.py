AUDIO = "final_mix_33.wav"
_R = json.load(open("results33.json"))
_c = pd.read_csv("sim33.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["eq"].values          # FEAR BUYER (VIX close >= 30 -> buy next open; sell after 252 trading days without a new VIX >= 30 close)
BV = _c["bh"].values          # JUST HOLD (buy & hold same dates, from 2005-01-03)
INN = _c["inm"].values.astype(bool)
VX = _c["vix"].values
RR = np.zeros(N)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert _R["trades"] == 5 and _R["wins"] == 5
assert round(RULE_V, -2) == 32400 and round(HOLD_V, -2) == 70200
assert _R["first_in"].startswith("2007-08")
assert _R["cash_blocks"][2][0].startswith("2012-12") and _R["cash_blocks"][2][1].startswith("2015-08") and round(_R["bh_in_cash"][2] * 100) == 40
assert all(v < HOLD_V for v in _R["scan"].values()) and len(_R["scan"]) == 12


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


TRD = _R["trades_list"]
QA0, QA1 = di(_R["cash_blocks"][2][0]), di(_R["cash_blocks"][2][1])
LEAD_V = _R["max_lead"]
