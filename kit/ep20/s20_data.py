AUDIO = "final_mix_20.wav"
_R = json.load(open("results20.json"))
_c = pd.read_csv("sim20.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["R"].values          # YIELD RULE (10y up >= 1 pt vs 252 days ago -> cash at next open)
BV = _c["B"].values          # BUY & HOLD same dates (from 2006-01-04)
YLD = _c["Y"].values; INN = _c["IN"].fillna(1).values
S0 = int(np.argmax(~np.isnan(RV)))
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert round(RULE_V, -2) == 58200 and round(HOLD_V, -2) == 66100
assert round(_R["y2022"][0]) == -7 and round(_R["y2022"][1]) == -19
assert _R["y2008"][0] == _R["y2008"][1] and _R["y2013"][0] < _R["y2013"][1] / 2 and abs(_R["y2023"][0] / _R["y2023"][1] - 0.5) < 0.06
YE = _R["year_end"]; assert abs(YE["2022"][0] / YE["2022"][1] - 1) < 0.02
NEWS_NOW, NEWS_YAGO = 5.12, 4.08   # 10y yield Nov 12 2026 (AP) vs Nov 12 2025 (FRED DGS10)
VAR = _R["variants"]


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
# cash zones (rule out of the market)
ZONES = []
_i = S0
while _i < N:
    if INN[_i - 1] == 0:
        _j = _i
        while _j + 1 < N and INN[_j] == 0:
            _j += 1
        ZONES.append((_i, _j)); _i = _j + 1
    else:
        _i += 1
