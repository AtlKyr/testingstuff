AUDIO = "final_mix_28.wav"
_R = json.load(open("results28.json"))
_c = pd.read_csv("sim28.csv", index_col=0, parse_dates=True)
_s = pd.read_csv("../spy.csv", index_col=0, parse_dates=True)
DATES = _c.index
N = len(DATES)
RV = _c["eq"].values          # 2% DROP SELLER (close <= -2% -> sell next open; back after 10 calm trading days, next open)
BV = _c["bh"].values          # JUST HOLD (buy & hold same dates, from 2005-01-03)
INN = _c["inm"].values.astype(bool)
RR = np.nan_to_num(_c["r"].values, nan=0.0)
_f = (_s["Adj Close"] / _s["Close"]).values
OP = _s["Open"].values * _f; CL = _s["Adj Close"].values
S0 = 0
RULE_V = _R["final"]; HOLD_V = _R["bh"]
from decimal import Decimal, ROUND_HALF_UP
_hu = lambda x: int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
# spoken numbers -> asserted against the backtest before TTS
assert _hu(_R["cluster10"] * 100) == 65
assert _R["worst10_out"] == 10 and _R["best10_out"] == 10
assert round(_R["max_lead"], -3) == 5000 and _R["max_lead"] > 5000 and _R["max_lead_date"] == "2009-03-09"
assert round(HOLD_V, -3) == 70000 and round(RULE_V, -3) == 40000 and round(HOLD_V - RULE_V, -3) == 30000
assert _R["lead_flip"] == "2020-03-23"


def di(d):
    return int(min(N - 1, np.searchsorted(DATES, pd.Timestamp(d))))


SELLI = [i for i in range(1, N) if INN[i - 1] and not INN[i]]
assert len(SELLI) in (_R["trades"], _R["trades"] + 1)
BEST = sorted(np.argsort(RR)[-10:][::-1].tolist(), key=lambda i: -RR[i])
WORST = sorted(np.argsort(RR)[:10].tolist(), key=lambda i: RR[i])
assert all(not INN[i] for i in BEST) and all(not INN[i] and not INN[i - 1] for i in WORST)
assert sum(1 for i in BEST if not INN[i - 1]) == 9
LEAD_V = _R["max_lead"]
T = dict(
    Sixty=wt("Sixty-five"), percent1=wt("percent"), drops=wt("drops"), strike=wt("strike"), within=wt("within"), weeks1=wt("weeks"),
    Monday=wt("Monday's"), close=wt("close"), Sell=wt("Sell"), A=wt("A"), hold=wt("hold"), B=wt("B"),
    Ten=wt("Ten"), hiding=wt("hiding"), panic=wt("panic"), decide=wt("decide"), rule=wt("rule"), drop=wt("drop"),
    sell2=wt("sell"), buy=wt("buy"), calm1=wt("calm"), weeks2=wt("weeks", 2), Two=wt("Two"), eight=wt("eight"),
    seller1=wt("seller"), again2=wt("again", 3), He=wt("He"), dodges=wt("dodges"), ten1=wt("ten"), worst=wt("worst"),
    nine=wt("nine"), bottom1=wt("bottom"), leads=wt("leads"), five=wt("five"), So=wt("So"), wins=wt("wins"),
    Twenty=wt("Twenty"), lead=wt("lead"), bottom2=wt("bottom", 2), Then=wt("Then"), waits=wt("waits"), calm2=wt("calm", 2),
    leaves=wt("leaves"), Those=wt("Those"), hidden=wt("hidden"), ten3=wt("ten", 3), best=wt("best"), missed=wt("missed"),
    nine2=wt("nine", 2), sold=wt("sold"), tenth=wt("tenth"), bill=wt("bill"), Holding=wt("Holding"), seventy=wt("seventy"),
    seller2=wt("seller", 2), forty=wt("forty"), fear2=wt("fear", 2), right2=wt("right", 2), Acting=wt("Acting"), cost=wt("cost"),
    thirty=wt("thirty"),
)
T["rev1"] = T["seventy"] + 0.1
T["rev2"] = T["forty"] + 0.1
T["rev3"] = T["rev2"] + 0.9
T["follow"] = END + 0.1
