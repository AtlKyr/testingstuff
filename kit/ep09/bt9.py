# Autopsy #9 - Missing the 10 best days, SPY 2005-2024.
# STAYER (buy & hold): buy at the first open (2005-01-03) with one 0.05% fee, hold to the last adjusted close (2024-12-31).
# MISSER: identical, except on each of the N best close-to-close days it is in cash: sells at the previous close and buys back
# at that day's close (fills at the CLOSE because the experiment is defined on close-to-close days), 0.05% per fill.
# Consecutive missed days share one round trip. Cash 0%. Prices: Adj Close (dividends included).
import pandas as pd, numpy as np, json, sys
df=pd.read_csv(sys.argv[1] if len(sys.argv)>1 else "../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=df["Open"]*f; C=df["Adj Close"]; idx=df.index
r=C.pct_change(); r.iloc[0]=C.iloc[0]/O.iloc[0]-1          # day 0: open -> close
FEE=0.0005; yrs=(idx[-1]-idx[0]).days/365.25
r_cc=r.iloc[1:]                                             # rankable close-to-close days (5,032)
def path(miss_idx,fee=FEE):
    m=pd.Series(False,index=idx); m[miss_idx]=True
    g=np.where(m,1.0,1+r)
    # fee: sell at close before each missed block, buy back at close at end of block
    starts=m & ~m.shift(1,fill_value=False)
    ends=m & ~m.shift(-1,fill_value=False)
    sell_fee=starts.shift(-1,fill_value=False)   # sell happens at the close of the day before the block
    g=g*np.where(sell_fee,1-fee,1)*np.where(ends,1-fee,1)
    return pd.Series(10000*(1-fee)*np.cumprod(g),index=idx), int(starts.sum())
def stats(s): return dict(v=round(s.iloc[-1]),cagr=round(100*((s.iloc[-1]/10000)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1))
best=r_cc.sort_values(ascending=False); worst=r_cc.sort_values()
B,_=path([]); out=dict(start=str(idx[0].date()),end=str(idx[-1].date()),days=len(idx),bh=stats(B))
for n in (5,10,20,30,40,50):
    s,rt=path(best.index[:n]); out[f"miss_best_{n}"]=dict(stats(s),roundtrips=rt)
for n in (10,):
    s,_=path(worst.index[:n]); out["miss_worst_10"]=stats(s)
    s,_=path(list(best.index[:n])+list(worst.index[:n])); out["miss_both_10"]=stats(s)
s0,_=path(best.index[:10],fee=0.0); out["miss_best_10_nofee"]=stats(s0)
out["best10"]=[dict(d=str(d.date()),r=round(100*v,2)) for d,v in best.iloc[:10].items()]
out["worst10"]=[dict(d=str(d.date()),r=round(100*v,2)) for d,v in worst.iloc[:10].items()]
# twist facts
W=worst.index[:10]
gap=[int(min(abs(np.searchsorted(idx,d)-np.searchsorted(idx,w)) for w in W)) for d in best.index[:10]]
out["best10_trading_days_to_nearest_worst10"]=gap
out["best10_within_10_tdays_of_worst10"]=int(sum(g<=10 for g in gap))
dd=(C/C.cummax()-1)
out["best10_market_drawdown_pct"]=[round(100*dd[d],1) for d in best.index[:10]]
out["best10_in_bear_dd_le_-20"]=int(sum(dd[d]<=-0.20 for d in best.index[:10]))
out["best10_years"]=pd.Series([d.year for d in best.index[:10]]).value_counts().to_dict()
out["share_of_days_pct"]=round(100*10/len(r_cc),2)
# where the misser's gap appears: year-end values
s10,_=path(best.index[:10]); s20,_=path(best.index[:20])
ye=pd.DataFrame({"B":B.resample("YE").last(),"M10":s10.resample("YE").last(),"M20":s20.resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
out["gap_pct_final"]=round(100*(1-s10.iloc[-1]/B.iloc[-1]),1)
out["fee_stress"]={str(fe):round(path(best.index[:10],fee=fe)[0].iloc[-1]) for fe in (0.0,0.0005,0.001,0.002)}
json.dump(out,open("results9.json","w"),indent=1,default=int)
pd.DataFrame({"B":B,"M10":s10,"M20":s20}).to_csv("sim9.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},indent=1,default=int)); print(ye.to_string())
