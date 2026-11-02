AUDIO = "final_mix_05.wav"
_R = json.load(open("results.json"))
_c = pd.read_csv("sim.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SIMV = _c["sim"].values
BHV = _c["bh"].values
POSV = _c["pos"].values
CLOSE = _c["close"].values
SIM_DD = (_c["sim"] / _c["sim"].cummax() - 1).values * 100
BH_DD = (_c["bh"] / _c["bh"].cummax() - 1).values * 100
SUMMERS = _R["summers"]                     # [{y, r}] May open -> Nov open
SUM_UP = _R["summers_up"]
SIM_V = _R["sim"]["v"]; BH_V = _R["bh"]["v"]; SUMONLY_V = _R["summer_only"]["v"]
SIM_DDV = _R["sim"]["dd"]; BH_DDV = _R["bh"]["dd"]
WMULT = _R["wmult"]; SMULT = _R["smult"]; S2008 = _R["summer2008"]
FEES = [("0.05%", _R["fees"]["0.0005"]), ("0.10%", _R["fees"]["0.001"]), ("0.20%", _R["fees"]["0.002"])]
TIM = _R["sim"]["tim"]
import rocco as _rk
_rk.COSTUME["straw"] = [(-3, 5, "KKKKKKKK"), (-2, 4, "KyyyyyyyyK"), (-1, 4, "KRRRRRRRRK"), (0, 4, "KyyyyyyyyK"),
                        (1, -1, "KKyyyyyyyyyyyyyyyyKK"), (2, 0, ".KKKKKKKKKKKKKKKK.")]


def di(d):
    return int(np.searchsorted(DATES, pd.Timestamp(d)))
