AUDIO = "final_mix_21.wav"
_R = json.load(open("results21.json"))
_c = pd.read_csv("sim21.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["R"].values          # SKIPPER (out on every Friday the 13th, close-to-close)
BV = _c["B"].values          # HOLDER (same close fills)
F13 = np.where(_c["F13"].values == 1)[0]
S0 = 0
SKIP_V = _R["final"]; HOLD_V = _R["bh"]
DAYS = _R["days"]
assert _R["n"] == 35 and _R["up"] == 20 and len(F13) == 35
assert round(SKIP_V, -2) == 60700 and round(HOLD_V, -2) == 70900 and round(HOLD_V - SKIP_V, -3) == 10000
assert _R["best"][0] == "2020-03-13" and 8.5 < _R["best"][1] < 9.0
YE = _R["year_end"]; assert abs(YE["2009"][0] / YE["2009"][1] - 1) < 0.035


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
