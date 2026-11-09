AUDIO = "final_mix_12.wav"
_R = json.load(open("results12.json"))
_c = pd.read_csv("sim12.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # BUY & HOLD (buys at records too)
JV = _c["W"].values          # WAITER: buy after a 5% drop from the record, sell at each new record
INM = _c["inm"].values
REC = _c["rec"].values; PX = _c["P"].values
BH_V = _R["bh"]["v"]; WV = _R["waiter5"]["v"]; NTR = _R["waiter5"]["trades"]
BUYS = _R["buys"]; SELLS = _R["sells"]
NEWREC_I = [i for i in range(1, N) if PX[i] > REC[i - 1]]
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
_sp = pd.read_csv("../spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
REBUY_PCT = int(round(100 * (_sp.loc[_R["buys"][7], "Open"] / _sp.loc[_R["sells"][6], "Open"] - 1)))
MONTHS_CASH = int(round((pd.Timestamp(_R["buys"][7]) - pd.Timestamp(_R["sells"][6])).days / 30.44))
