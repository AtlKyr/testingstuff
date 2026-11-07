AUDIO = "final_mix_10.wav"
_R = json.load(open("results10.json"))
_c = pd.read_csv("sim10.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # HOLDER = buy & hold
JV = _c["S"].values          # PANIC BUYER = buy after 3 red closes, sell after first green close
INM = _c["IN"].values
BH_V = _R["bh"]["v"]; S_V = _R["main"]["v"]
FEE = _R["fee_stress"]; F05 = FEE["0.0005"]; F10 = FEE["0.001"]; F20 = FEE["0.002"]; F00 = FEE["0.0"]
TIM = _R["main"]["tim"]                      # % of days invested
UP3 = _R["next_day_up_after_3down_pct"]; UPB = _R["base_up_day_pct"]
FEE_EAT = (F00 - F05) / (F00 - 10000)        # share of gross profit eaten by fees (~0.50)
_df = pd.read_csv("../spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
SPYC = _df["Adj Close"].values
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
