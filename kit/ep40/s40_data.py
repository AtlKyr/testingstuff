AUDIO = "final_mix_40.wav"
_R = json.load(open("results40.json"))
_c = pd.read_csv("sim40.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["H"].values            # buy & hold
SV = _c["S"].values            # sells every +2% opening pop, back in a week
NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
S0 = 0
HOLD_V = _R["bh"]; RULE_V = _R["final"]; ONE_V = HOLD_V; TWO_V = RULE_V; REIN_V = HOLD_V; POCK_V = RULE_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


SELL_I = [di(d) for d in _R["sells"]]; BUY_I = [di(d) for d in _R["buys"]]
I_T24 = di("2020-03-24"); I_B31 = di("2020-03-31"); I_S10 = di("2020-03-10"); I_B17 = di("2020-03-17")
GAP24 = _R["gap24"]; REB24 = _R["rebuy24"]
SC3 = _R["scan"]["0.02_3"]; SC10 = _R["scan"]["0.02_10"]
# spoken numbers -> asserted against the backtest before TTS
assert _R["n_gaps"] == 48 and round(GAP24 * 100) == 5 and round(REB24 * 100) == 11
assert round(RULE_V / 1000) == 61 and round(HOLD_V / 1000) == 70 and _R["cheaper"] == 17 and _R["n_sells"] == 33
assert _R["last_lead"] == "2020-03-25" and SC3 > HOLD_V and SC10 < HOLD_V
assert SV[di("2008-12-31")] > HV[di("2008-12-31")] and SV[di("2020-03-20")] > HV[di("2020-03-20")]
# names used at module level by older chained scene files
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
