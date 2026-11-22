AUDIO = "final_mix_38.wav"
_R = json.load(open("results38.json"))
_c = pd.read_csv("sim38.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["B"].values            # holds through every Thanksgiving week (buy & hold)
SV = _c["A"].values            # sits out every Thanksgiving week (Mon open -> next Mon open)
NF = HV; FE = SV
INN = _c["IN"].values.astype(bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
HOLD_V = _R["B"]; SIT_V = _R["A"]; ONE_V = HOLD_V; TWO_V = SIT_V; RULE_V = SIT_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


WK = {w["y"]: w for w in _R["weeks"]}
ONLY08_V = _R["A_skip_only_2008"]
W08 = WK[2008]
# spoken numbers -> asserted against the backtest before TTS
assert round(SIT_V, -3) == 63000 and round(HOLD_V, -3) == 70000 and round(HOLD_V - SIT_V, -2) == 7500
assert _R["w08_rank"] == 1 and _R["trades"] == 20
assert WK[2005]["wk_skip"] > 0 and WK[2007]["wk_skip"] < 0 and WK[2011]["wk_skip"] < 0 and WK[2018]["wk_skip"] < 0
assert max(-w["wk_skip"] for w in _R["weeks"]) < W08["wk_skip"]
NEWS_PCT = -8.6   # S&P 500 week to Fri 2026-11-20 (AP / CBS / NBC, verified 2026-11-21)
