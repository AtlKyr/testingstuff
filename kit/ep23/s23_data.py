AUDIO = "final_mix_23.wav"
_R = json.load(open("results23.json"))
_c = pd.read_csv("sim23.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["R"].values          # 10% STOP-LOSS (sell next open after a close 10% below the high since entry; rebuy next open after +10% off the low)
BV = _c["B"].values          # BUY & HOLD same dates (from 2005-01-03)
INN = _c["IN"].values
OP = _c["O"].values; CL = _c["C"].values
S0 = 0
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert round(RULE_V, -2) == 65100 and round(HOLD_V, -2) == 70200
assert _R["trades"] == 15 and _R["rebuy_higher"] == 9 and len(_R["pairs"]) == 15
assert sum(p[0].startswith("2022") for p in _R["pairs"]) == 3
PAIRS = _R["pairs"]
assert PAIRS[9][0].startswith("2018-02") and PAIRS[9][2] > 0          # 2018: sold, then bought back higher
assert PAIRS[11][0] == "2020-02-28" and PAIRS[11][2] < 0                # 2020: out before the worst, back near the bottom
SC_ = _R["scan"]


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
ZONES = []
_i = 0
while _i < N:
    if INN[_i] == 0:
        _j = _i
        while _j + 1 < N and INN[_j + 1] == 0:
            _j += 1
        ZONES.append((_i, _j)); _i = _j + 1
    else:
        _i += 1
SELLI = [di(p[0]) for p in PAIRS]; BUYI = [di(p[1]) for p in PAIRS]
