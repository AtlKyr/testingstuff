AUDIO = "final_mix_32.wav"
_R = json.load(open("results32.json"))
_c = pd.read_csv("sim32.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["eq"].values          # STREAK SELLER (5th straight red close -> sell next open; back 21 trading days later, next open)
BV = _c["bh"].values          # SIT TIGHT (buy & hold same dates, from 2005-01-03)
INN = _c["inm"].values.astype(bool)
RR = np.nan_to_num(_c["r"].values, nan=0.0)
STK = _c["st"].values
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert _R["n_streaks"] == 43 and _R["day6_n"] == 43 and _R["day6_n"] - _R["day6_red"] == 27
assert round(RULE_V, -2) == 40900 and round(HOLD_V, -2) == 70200
assert _R["last_ahead"].startswith("2010") and _R["max_lead_date"].startswith("2009")


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


SELLI = [i for i in range(1, N) if INN[i - 1] and not INN[i]]
assert len(SELLI) in (_R["trades"], _R["trades"] + 1)
EVI = [di(x) for x in _R["events"]]           # the 43 fifth-red-day closes
D6 = _R["day6_list"]                           # day-six close-to-close returns
assert len(EVI) == 43 and sum(1 for x in D6 if x > 0) == 27
LEAD_V = _R["max_lead"]
