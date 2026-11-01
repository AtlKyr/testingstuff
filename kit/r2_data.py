AUDIO = "final_mix_r2.wav"
_c = pd.read_csv("conn.csv", index_col=0, parse_dates=True).loc["2005-01-01":"2024-12-31"]
DATES = _c.index
N = len(DATES)
CONN = _c["conn"].values
BHV = _c["bh"].values
POSV = _c["pos"].values
TRADES = json.load(open("trades.json"))
WINS = [tr["r"] > 0 for tr in TRADES]
FEES = [("0.05%", 16525), ("0.10%", 14223), ("0.20%", 10533)]


def di(d):
    return int(np.searchsorted(DATES, pd.Timestamp(d)))
