AUDIO = "final_mix_39.wav"
_R = json.load(open("results39.json"))
_c = pd.read_csv("sim39.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["R"].values            # reinvests every dividend (= buy & hold total return)
SV = _c["P"].values            # pockets every dividend: shares + cash jar
JAR = _c["JAR"].values
NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
S0 = 0
REIN_V = _R["reinvest"]; POCK_V = _R["spender_total"]; ONE_V = REIN_V; TWO_V = POCK_V; HOLD_V = REIN_V; RULE_V = POCK_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


CHK_D, CHK_V, CHK_G = _R["best_check"]
JAR_V = _R["checks_total"]; SHARES_V = _R["spender_shares_value"]
I_LOW = di("2009-03-09")
# spoken numbers -> asserted against the backtest before TTS
assert _R["n_div"] == 80 and round(POCK_V, -3) == 55000 and round(REIN_V, -3) == 70000
assert round(JAR_V, -2) == 6800 and CHK_D == "2008-12-19" and round(CHK_V) == 59 and round(CHK_G, -1) == 530
assert SV[I_LOW] > HV[I_LOW] and abs(SV[di("2007-12-31")] / HV[di("2007-12-31")] - 1) < 0.01
