AUDIO = "final_mix_07.wav"
_R = json.load(open("results7.json"))
_c = pd.read_csv("sim7.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
SIMV = _c["sim"].values
BHV = _c["bh"].values
POSV = _c["pos"].values
CLOSE = _c["close"].values
HH = _c["hh"].values
LL = _c["ll"].values
SIM_DD = (_c["sim"] / _c["sim"].cummax() - 1).values * 100
BH_DD = (_c["bh"] / _c["bh"].cummax() - 1).values * 100
SIM_V = _R["sim"]["v"]; BH_V = _R["bh"]["v"]
SIM_DDV = _R["sim"]["dd"]; BH_DDV = _R["bh"]["dd"]
NTR = _R["trades"]; WINS = _R["wins"]; LOSSES = _R["losses"]; WINR = _R["sim"]["win"]
AVG_WIN = _R["avg_win"]; AVG_LOSS = _R["avg_loss"]; WL_RATIO = AVG_WIN / abs(AVG_LOSS)
MIN_ = _R["mult_in"]; MOUT = _R["mult_out"]; TIM = _R["sim"]["tim"]; CASHP = 100 - TIM
COV_M = _R["crashes"]["covid"]["m"]; COV_B = _R["crashes"]["covid"]["b"]
V55 = _R["r55"]["v"]
FEES = [("0.05%", _R["fees"]["0.0005"]), ("0.10%", _R["fees"]["0.001"]), ("0.20%", _R["fees"]["0.002"])]
TRADES = _R["trades_list"]


def di(d):
    return int(np.searchsorted(DATES, pd.Timestamp(d)))


# covid rebound: low close 2020-03-23 -> first Turtle buy 2020-04-13 (B&H value ratio from sim7.csv)
COV_LOW_I, COV_BUY_I = di("2020-03-23"), di("2020-04-13")
REBOUND = (BHV[COV_BUY_I] / BHV[COV_LOW_I] - 1) * 100
