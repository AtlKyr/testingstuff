AUDIO = "final_mix_08.wav"
_R = json.load(open("results8.json"))
_c = pd.read_csv("sim8.csv", index_col=0, parse_dates=True)
_c[["N0", "D0", "N", "D"]] = _c[["N0", "D0", "N", "D"]].fillna(10000.0)
DATES = _c.index
N = len(DATES)
NG = _c["N0"].values; DG = _c["D0"].values          # gross (before fees) race
NF = _c["N"].values; DF = _c["D"].values            # with 0.05%/side fees
BHV = _c["B"].values
BH_V = _R["bh"]["v"]; NF_V = _R["night_fee"]["v"]; DF_V = _R["day_fee"]["v"]
NG_V = _R["night_nofee"]["v"]; DG_V = _R["day_nofee"]["v"]
NDAYS = _R["night_fee"]["trades"]
CR = _R["crashes_gross"]
import rocco as _rk
_rk.COSTUME["straw"] = [(-3, 5, "KKKKKKKK"), (-2, 4, "KyyyyyyyyK"), (-1, 4, "KRRRRRRRRK"), (0, 4, "KyyyyyyyyK"),
                        (1, -1, "KKyyyyyyyyyyyyyyyyKK"), (2, 0, ".KKKKKKKKKKKKKKKK.")]


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
