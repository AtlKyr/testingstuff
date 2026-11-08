AUDIO = "final_mix_11.wav"
_R = json.load(open("results11.json"))
_c = pd.read_csv("sim11.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # HOLDER = buy & hold
JV = _c["P"].values          # PANIC SELLER = sell next open after a <=-4% day, buy back 21 trading days later
BH_V = _R["bh"]["v"]; P1M = _R["panic"]["1m"]["v"]; P3M = _R["panic"]["3m"]["v"]
P1W = _R["panic"]["1w"]["v"]; P6M = _R["panic"]["6m"]["v"]
NCR = _R["n_crash"]; Y1UP = _R["y1"]["up"]; Y1N = _R["y1"]["n"]
BYYEAR = {int(k): v for k, v in _R["by_year"].items()}
_df = pd.read_csv("../spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
SPYC = _df["Adj Close"].values
_r = np.r_[np.nan, SPYC[1:] / SPYC[:-1] - 1]
CRASH_I = [int(i) for i in np.where(_r <= -0.04)[0]]
Y1DOWN = set(_R["y1_down"])
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
