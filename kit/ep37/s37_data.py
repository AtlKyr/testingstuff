AUDIO = "final_mix_37.wav"
_R = json.load(open("results37.json"))
_c = pd.read_csv("sim37.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["one"].values          # $10,000 in SPY at the first close
SV = _c["two"].values          # simulated 2x daily fund (borrow at 3m T-bill on 1x + 0.89%/yr fee)
NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
ONE_V = _R["one"]; TWO_V = _R["two"]; HOLD_V = ONE_V; RULE_V = TWO_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


I_LOW = di(_R["two_low_date"]); I_AHEAD = di(_R["two_ahead_again"])
LOW_V = _R["two_low"]
# spoken numbers -> asserted against the backtest before TTS
assert round(LOW_V, -2) == 2500 and _R["two_low_date"].startswith("2009-03")
assert round(1 - LOW_V / 10000, 2) == 0.75
assert _R["two_ahead_again"][:4] == "2014"
assert round(ONE_V, -3) == 71000 and round(TWO_V, -3) == 148000 and 1.95 < TWO_V / ONE_V < 2.15
assert HV[di("2007-12-31")] < SV[di("2007-12-31")] and HV[di("2006-12-29")] < SV[di("2006-12-29")]
R22 = _R["ret2022"]; R08 = _R["ret2008"]
THREE_V = _R["3x"]; NOCOST_V = _R["two_nofee"]
