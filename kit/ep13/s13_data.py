AUDIO = "final_mix_13.wav"
_R = json.load(open("results13.json"))
_c = pd.read_csv("sim13.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # HOLDER (owns every day)
JV = _c["N"].values          # MONDAY SKIPPER: sells at the close before Monday, buys back at Monday's close (0.05%/side)
BH_V = _R["bh"]["v"]; SKV = _R["never_mon"]["v"]; SK0 = _R["never_mon_nofee"]
MON_08 = _R["mon_by_year_growth"]["2008"]
_df = pd.read_csv("../spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
_r = _df["Adj Close"].pct_change()
BEST_PCT = round(100 * float(_r.max()), 1); BEST_DATE = _r.idxmax()
WORST_PCT = round(100 * float(_r.min()), 1); WORST_DATE = _r.idxmin()
MON_I = [i for i in range(1, N) if DATES[i].dayofweek == 0]
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
