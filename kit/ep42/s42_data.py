AUDIO = "final_mix_42.wav"
_R = json.load(open("results42.json"))
_c = pd.read_csv("sim42.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True).loc[_c.index[0]:]
DATES = _c.index
N = len(DATES)
HV = _c["H"].values            # ignores the cross (buy & hold from 2005-10-18, after the 200-day warm-up)
SV = _c["S"].values            # sells the open after every death cross, buys back 252 trading days later
M50 = _c["S50"].values; M200 = _c["S200"].values
NF = HV; FE = SV
INN = np.ones(N, bool)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values; RAWC = _s["Close"].values
S0 = 0
HOLD_V = _R["bh"]; RULE_V = _R["final"]; ONE_V = HOLD_V; TWO_V = RULE_V; REIN_V = HOLD_V; POCK_V = RULE_V
SELLS = []; BUYS = []; ZONES = []


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


TR = _R["trades"]
SELL_I = [di(x[1]) for x in TR]; BUY_I = [di(x[3]) for x in TR]
CROSS_I = [di(x[0]) for x in TR]
I_S07, I_B08 = di("2007-12-31"), di("2008-12-30"); I_S20, I_B21 = di("2020-04-01"), di("2021-04-01"); I_BOT20 = di("2020-03-23")
R07, R20 = _R["r07"], _R["r20"]
# spoken numbers -> asserted against the backtest before TTS
assert _R["n"] == 8 and _R["higher"] == 6 and round(RULE_V / 1000) == 29 and round(HOLD_V / 1000) == 71
assert abs(R07 + 0.40) < 0.015 and R20 > 0.60 and TR[6][1] == "2020-04-01"
assert SV[di("2009-12-31")] > HV[di("2009-12-31")] and SV[di("2012-12-31")] < HV[di("2012-12-31")]
CHK_D = "2008-12-19"; I_LOW = di("2009-03-09")
