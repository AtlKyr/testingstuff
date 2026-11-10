AUDIO = "final_mix_14.wav"
_R = json.load(open("results14.json"))
_c = pd.read_csv("sim14.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # BUY & HOLD
JV = _c["S"].values          # BOUNCE CHASER: buys the open after every +2% day, holds 21 trading days (0.05%/side)
BIG_I = [i for i in range(N) if _c["big"].values[i] == 1]
BH_V = _R["bh"]["v"]; CHV = _R["chaser"]["v"]
N_BIG = _R["n_big"]; N_DEEP = _R["big_prior_dd_le10"]
BY_YEAR = {int(k): v for k, v in _R["by_year"].items()}
ERASED, ERASED_N = _R["erased_63"][0], _R["erased_63"][1]
HOLD_WINS = _R["hold_scan_wins"]
assert BY_YEAR[2017] == 0 and HOLD_WINS == 0 and round(5 * N_DEEP / N_BIG) == 4 and round(3 * ERASED / ERASED_N) == 2
NEWS_PCT = "+2.35%"          # S&P 500, Mon 2026-11-09 close (Yahoo Finance / StockTitan / BBN Times) - best day since April
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
