AUDIO = "final_mix_41.wav"
_R = json.load(open("results41.json"))
_c = pd.read_csv("sim41.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["H"].values            # 100% SPY
SV = _c["P"].values            # 60/40 SPY / simulated 10-year Treasuries, rebalanced every January
BIV = _c["BI"].values
NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
S0 = 0
HOLD_V = _R["bh"]; RULE_V = _R["p"]; ONE_V = HOLD_V; TWO_V = RULE_V; REIN_V = HOLD_V; POCK_V = RULE_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


S08, P08, S22, P22, B22 = _R["s08"], _R["p08"], _R["s22"], _R["p22"], _R["b22"]
MDD_H, MDD_P = _R["mdd_bh"], _R["mdd_p"]; SC70 = _R["scan"]["0.7"]; SC80 = _R["scan"]["0.8"]
# spoken numbers -> asserted against the backtest before TTS
assert round(-S08 * 100) == 37 and round(-P08 * 100) == 14 and round(-S22 * 100) == 18 and round(-B22 * 100) == 16
assert round(RULE_V / 1000) == 44 and round(HOLD_V / 1000) == 70 and abs(MDD_P / MDD_H - 0.5) < 0.06 and _R["lead2020"] == 3
assert SV[di("2010-12-31")] > HV[di("2010-12-31")] and SV[di("2015-12-31")] < HV[di("2015-12-31")]
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09"); SELL_I = []
