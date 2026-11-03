AUDIO = "final_mix_06.wav"
_R = json.load(open("results6.json"))
_c = pd.read_csv("sim6.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SIMV = _c["sim"].values
BHV = _c["bh"].values
POSV = _c["pos"].values
CLOSE = _c["close"].values
MACDV = _c["macd"].values
SIGV = _c["sig"].values
SIM_DD = (_c["sim"] / _c["sim"].cummax() - 1).values * 100
BH_DD = (_c["bh"] / _c["bh"].cummax() - 1).values * 100
SIM_V = _R["sim"]["v"]; BH_V = _R["bh"]["v"]
SIM_DDV = _R["sim"]["dd"]; BH_DDV = _R["bh"]["dd"]
NTR = _R["trades"]; WINS = _R["wins"]; LOSSES = _R["losses"]; WINR = _R["sim"]["win"]
MIN_ = _R["mult_in"]; MOUT = _R["mult_out"]; CASHP = _R["cash_pct"]; TIM = _R["sim"]["tim"]
COV_M = _R["crashes"]["covid"]["m"]; COV_B = _R["crashes"]["covid"]["b"]
YEARS = _R["years"]; BEATY = _R["beat_years"]
FEES = [("0.05%", _R["fees"]["0.0005"]), ("0.10%", _R["fees"]["0.001"]), ("0.20%", _R["fees"]["0.002"])]
FEE_PROFIT = _R["fee_profit_020"]
TRADES = _R["trades_list"]


def di(d):
    return int(np.searchsorted(DATES, pd.Timestamp(d)))
