AUDIO = "final_mix_22.wav"
_R = json.load(open("results22.json"))
_c = pd.read_csv("sim22.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["R"].values          # PROFIT TAKER (sell next open after a +2.5% week, buy back 21 trading days later)
BV = _c["B"].values          # BUY & HOLD same dates (from 2005-01-18)
INN = _c["IN"].fillna(1).values
OP = _c["O"].values
S0 = int(np.argmax(~np.isnan(RV)))
RULE_V = _R["final"]; HOLD_V = _R["bh"]
# spoken numbers -> asserted against the backtest before TTS
assert round(RULE_V, -2) == 58500 and round(HOLD_V, -2) == 72300
assert _R["scan_hold"]["5"] > HOLD_V
_lead = RV - BV
assert 5000 < np.nanmax(_lead) < 5600 and str(DATES[int(np.nanargmax(_lead))].date()).startswith("2020-03")
assert _R["miss_list"][_R["sell_dates"].index("2020-03-30")] == 14.0
NEWS_PREV, NEWS_NOW = 7376.86, 7561.67   # S&P 500 close Nov 6 2026 vs Nov 13 2026 (AP / Yahoo Finance)
assert round(100 * (NEWS_NOW / NEWS_PREV - 1), 1) == 2.5


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
ZONES = []
_i = S0
while _i < N:
    if INN[_i] == 0:
        _j = _i
        while _j + 1 < N and INN[_j + 1] == 0:
            _j += 1
        ZONES.append((_i, _j)); _i = _j + 1
    else:
        _i += 1
SALE = di("2020-03-30"); SALE_BACK = SALE + 21
LEAD_I = int(np.nanargmax(_lead)); LEAD_V = float(np.nanmax(_lead))
SELLS = [di(d) for d in _R["sell_dates"]]
