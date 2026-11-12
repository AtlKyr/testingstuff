AUDIO = "final_mix_19.wav"
_R = json.load(open("results19.json"))
_c = pd.read_csv("sim19.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
VV = _c["V"].values          # $500 every month (first trading day open), dividends reinvested, 0.05% fee
IV = _c["I"].values          # money put in
FINAL_V = _R["final"]; INV_V = _R["invested"]
HIT100 = _R["hit_100000"][0]; HIT200 = _R["hit_200000"][0]; HIT300 = _R["hit_300000"][0]
GAP = _R["worst_gap"]        # date, value, invested, gap at the 2009 low
assert GAP[2] > 25000 and round(GAP[1], -3) == 14000 and HIT100.startswith("2014-08") and _R["months_100_200k"] < 60
assert _R["months_200_300k"] < 24 and round(FINAL_V, -4) == 490000 and FINAL_V < 490000 and INV_V == 120000
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
I100, I200, I300, ILOW = di(HIT100), di(HIT200), di(HIT300), di(GAP[0])
M1, M2, M3 = _R["months_0_100k"], _R["months_100_200k"], _R["months_200_300k"]
