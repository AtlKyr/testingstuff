AUDIO = "final_mix_16.wav"
_R = json.load(open("results16.json"))
_c = pd.read_csv("sim16.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SV = _c["B"].values          # BUY & HOLD
JV = _c["S"].values          # HIKE SELLER: sells next open after every Fed hike, buys back after 126 trading days with no new hike
INM = _c["inm"].values
HIKES = ["2005-02-02","2005-03-22","2005-05-03","2005-06-30","2005-08-09","2005-09-20","2005-11-01","2005-12-13","2006-01-31",
         "2006-03-28","2006-05-10","2006-06-29","2015-12-16","2016-12-14","2017-03-15","2017-06-14","2017-12-13","2018-03-21",
         "2018-06-13","2018-09-26","2018-12-19","2022-03-16","2022-05-04","2022-06-15","2022-07-27","2022-09-21","2022-11-02",
         "2022-12-14","2023-02-01","2023-03-22","2023-05-03","2023-07-26"]
BH_V = _R["bh"]["v"]; SEL_V = _R["avoider"]["v"]
FWD = _R["fwd252"]; UP, NH = map(int, _R["fwd252_up"])
WAIT_WINS, WAIT_N = map(int, _R["wait_scan_wins"])
CYC22 = _R["cycles"][2][2]
assert (UP, NH) == (29, 32) and round(SEL_V, -3) == 35000 and round(BH_V, -3) == 70000 and CYC22 > 0 and len(HIKES) == 32
assert [d for d, _ in FWD] == HIKES
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
HIKE_I = [di(d) for d in HIKES]
