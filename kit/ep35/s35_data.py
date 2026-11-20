AUDIO = "final_mix_35.wav"
_R = json.load(open("results35.json"))
_c = pd.read_csv("sim35.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
NF = _c["bh"].values          # NO FEE: $10,000 buy & hold SPY from the first open (0.05% buy cost)
FE = _c["fee"].values         # 1% FEE: same, minus 1/12 of 1% of the value at each month's last close
PAIDV = _c["paid"].values
RV = FE; BV = NF; AV = NF; BW = FE
INN = np.ones(N, bool)
RR = np.zeros(N)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
NF_V = _R["bh"]; FE_V = _R["fee"]; HOLD_V = NF_V; RULE_V = FE_V; A_V = NF_V; B_V = FE_V
GAP_V = NF_V - FE_V; PAID_V = _R["paid"]
# spoken numbers -> asserted against the backtest before TTS
assert _R["nbills"] == 240
assert round(_R["yearly_paid"]["2005"], -2) == 100
assert round(NF_V, -3) == 70000 and round(FE_V, -2) == 57500
assert round(PAID_V, -2) == 4400 and round(GAP_V, -2) == 12700
assert 0.20 < _R["share_of_gain_lost"] < 0.25
_last = _s.index.to_series().groupby([_s.index.year, _s.index.month]).last().values
_m = [CL[-1] / _s["Adj Close"][d] for d in _last if pd.Timestamp(d).year == 2005]
assert 6.5 < min(_m) and max(_m) < 7.5 and round(float(np.mean(_m))) == 7
YEARLY = {int(k): v for k, v in _R["yearly_paid"].items()}
SCAN = _R["scan"]


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
