AUDIO = "final_mix_25.wav"
_R = json.load(open("results25.json"))
_c = pd.read_csv("sim25w.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["worst"].values      # WORST TIMER: $1,000 each year at the CLOSE of the year's highest close (0.05% fee)
BV = _c["best"].values       # TWIN (perfect timer): $1,000 each year at the close of the year's lowest close
PI = _c["putin"].values      # money put in
CL = _c["C"].values; OP = CL
S0 = 0
RULE_V = _R["worst"]; HOLD_V = _R["best"]
# spoken numbers -> asserted against the backtest before TTS
assert round(HOLD_V, -2) == 96400 and round(RULE_V, -3) == 73000 and round(RULE_V, -2) == 73000
assert RULE_V / _R["putin"] > 3 and _R["putin"] == 20000
assert round(_R["dd2009"], 2) == -0.50


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


_y = lambda y: _c.loc[str(y)]
assert _y(2007)["C"].idxmax().strftime("%Y-%m-%d") == "2007-10-09"
assert _y(2008)["C"].idxmax().strftime("%Y-%m-%d") == "2008-01-02"
assert _y(2009)["C"].idxmin().strftime("%Y-%m-%d") == "2009-03-09"
assert _y(2022)["C"].idxmax().strftime("%Y-%m-%d") == "2022-01-03" and _y(2022).index[0].strftime("%Y-%m-%d") == "2022-01-03"
BUYW = [int(np.searchsorted(DATES, _y(y)["C"].idxmax())) for y in range(2005, 2025)]
BUYB = [int(np.searchsorted(DATES, _y(y)["C"].idxmin())) for y in range(2005, 2025)]
ZONES = []
SELLI = []; BUYI = []
