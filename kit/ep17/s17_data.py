AUDIO = "final_mix_17.wav"
_R = json.load(open("results17.json"))
_c = pd.read_csv("sim17.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
HV = _c["H"].values          # TOP BUYER WHO HOLDS (bought the open of 2007-10-10, day after the record close)
PV = _c["P"].values          # PANIC SELLER: sells next open after a close >= 40% below his buy price, back after a new record close
_s = pd.read_csv("../spy.csv", parse_dates=["Date"]).set_index("Date").sort_index()
B0 = int(np.searchsorted(DATES, pd.Timestamp(_R["buy_date"])))
PRICE_V = 10000 * (1 - 0.0005) / _s["Open"].values[B0] * _s["Close"].values      # same buy, dividends NOT counted
HOLD_V = _R["holder"]; PAN_V = _R["panic"]
SELL_D, BUY_D = _R["panic_log"][0][1], _R["panic_log"][1][1]
BE_T, BE_P = _R["be_total"], _R["be_price"]
MISSED = _R["missed_gain_pct"]
THR = {k: v for k, v in _R["panic_thr"].items()}
assert round(PAN_V, -3) == 26000 and round(HOLD_V, -3) == 52000 and round(_R["be_total_months"] / 12 * 2) / 2 == 4.5
assert _R["be_price_months"] > 60 and 95 < MISSED < 100 and all(v < HOLD_V for v in THR.values())
import rocco as _rk


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))
I_SELL, I_BUY, I_BET, I_BEP = di(SELL_D), di(BUY_D), di(BE_T), di(BE_P)
