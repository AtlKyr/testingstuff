AUDIO = "final_mix_34.wav"
_R = json.load(open("results34.json"))
_c = pd.read_csv("sim34.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
AV = _c["A"].values          # A: BUYS EVERY MONTH ($500 at the first trading day's open)
BW = _c["B"].values          # B: WAITS FOR DIPS (saves $500/month in cash, buys the whole pile at the next open after a close >= 8% below the record)
PUTV = _c["put"].values
CASHV = _c["cash"].values
RV = BW; BV = AV
INN = CASHV < 1000
RR = np.zeros(N)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
A_V = _R["A"]; B_V = _R["B"]; HOLD_V = A_V; RULE_V = B_V
GAP_V = A_V - B_V
# spoken numbers -> asserted against the backtest before TTS
assert round(7175.83 / 7818.93 - 1, 3) == -0.082 and round((7175.83 / 7818.93 - 1) * 100) == -8   # news: AP close 11/19 vs Oct record
assert round(_R["maxcash"]) == 16000 and _R["maxcash_date"].startswith("2007-08")
assert _R["buys"][0][0] == "2007-08-16" and _R["buys"][0][1] == 16000
assert round(A_V, -3) == 490000 and round(B_V, -3) == 472000 and 17000 < GAP_V < 18000
assert all(v < A_V for v in _R["scan"].values())
_o = _s["Open"] * _s["Adj Close"] / _s["Close"]
RISE = float(_o["2015-08-25"] / _o["2013-02-01"] - 1); RAW_RISE = float(_s["Open"]["2015-08-25"] / _s["Open"]["2013-02-01"] - 1)
assert round(RISE * 100) == 36 and round(RAW_RISE * 100) == 30
_wy = (pd.Timestamp("2015-08-25") - pd.Timestamp("2013-02-01")).days / 365.25
assert 2.4 < _wy < 2.7
WAITS = [("2005-07", "2005-01-03", "2007-08-16"), ("2013-15", "2013-02-01", "2015-08-25"), ("2016-18", "2016-04-01", "2018-02-09"),
         ("2019-20", "2019-03-01", "2020-02-28"), ("2020-22", "2020-12-01", "2022-01-24"), ("2023-24", "2023-12-01", "2024-08-06")]
assert all(_o[b] > _o[a] and _s["Open"][b] > _s["Open"][a] for _, a, b in WAITS)
BEST_SCAN = max(_R["scan"].values())


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


QA0, QA1 = di("2013-02-01"), di("2015-08-25")
