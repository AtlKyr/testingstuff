AUDIO = "final_mix_24.wav"
_R = json.load(open("results24.json"))
_c = pd.read_csv("sim24.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["R"].values          # FEAR SELLER (VIX close >= 30 -> sell next open; VIX close < 20 -> buy back next open)
BV = _c["B"].values          # SIT TIGHT = buy & hold same dates (from 2005-01-03)
INN = _c["IN"].values
OP = _c["O"].values; CL = _c["C"].values; VX = _c["V"].values
S0 = 0
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert round(RULE_V, -2) == 22300 and round(HOLD_V, -2) == 70200
assert round(_R["news"]["pct"]) == 70
PAIRS = _R["pairs"]
assert PAIRS[3][0] == "2008-09-16" and PAIRS[3][1] == "2009-12-23" and abs(PAIRS[3][2]) < 0.01
assert PAIRS[9][0] == "2020-02-28" and PAIRS[9][1] == "2021-02-16" and round(PAIRS[9][2] * 100) == 39
SC_ = _R["scan"]
assert all(v < HOLD_V for v in SC_.values()) and len(SC_) == 11


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


_a, _b = di("2020-02-24"), di("2021-02-11")
assert VX[_a:_b + 1].min() >= 20
assert RV[di("2009-03-09")] > BV[di("2009-03-09")]
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
