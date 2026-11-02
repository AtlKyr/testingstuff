# Autopsy #5 - Sell in May and go away. Loop backtest: signal at close (calendar), fill next open, cost per side.
import pandas as pd, numpy as np, json
df=pd.read_csv("spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; o=(df["Open"]*f).values; c=df["Adj Close"].values; idx=df.index
WIN=(11,12,1,2,3,4)
def run(cost=0.0005, start=None, months=WIN):
    ii=range(len(idx)) if start is None else [i for i in range(len(idx)) if idx[i]>=pd.Timestamp(start)]
    ii=list(ii); cash=10000.0; sh=0.0; eq=[]; pos=[]; trades=[]; entry=None
    for k,i in enumerate(ii):
        if k>0:
            want = idx[i].month in months      # decided at prior close (calendar known), filled at today's open
            if want and sh==0: sh=cash*(1-cost)/o[i]; cash=0; entry=(idx[i],o[i])
            elif not want and sh>0:
                cash=sh*o[i]*(1-cost); sh=0; trades.append(dict(a=str(entry[0].date()),b=str(idx[i].date()),r=o[i]/entry[1]-1))
        eq.append(cash+sh*c[i]); pos.append(1 if sh>0 else 0)
    eq=pd.Series(eq,index=idx[ii]); pos=pd.Series(pos,index=idx[ii])
    y=(eq.index[-1]-eq.index[0]).days/365.25
    return dict(v=round(eq.iloc[-1]),cagr=round(100*((eq.iloc[-1]/10000)**(1/y)-1),2),dd=round(100*(eq/eq.cummax()-1).min(),1),
                tim=round(100*pos.mean(),1),sells=len(trades),win=round(100*np.mean([t["r"]>0 for t in trades]),1)),eq,pos,trades
r,eq,pos,tr=run(); print("SIM",r)
bh=10000*pd.Series(c,index=idx)/c[0]; bhdd=round(100*(bh/bh.cummax()-1).min(),1)
print("BH",round(bh.iloc[-1]),bhdd)
fees={p:run(p)[0]["v"] for p in (0.0005,0.001,0.002)}; print("fees",fees)
r10,eq10,_,_=run(start="2015-01-01"); s=idx[idx>="2015-01-01"]; bh10=round(10000*c[-1]/c[idx.get_loc(s[0])]); print("10y",r10,bh10)
rs,eqs,_,_=run(months=(5,6,7,8,9,10)); print("SUMMER ONLY",rs)
summers=[]
for y in range(2005,2025):
    a=df.loc[f"{y}-05-01":].iloc[0]; b=df.loc[f"{y}-11-01":].iloc[0]
    summers.append(dict(y=y,r=round(100*((b.Open*b["Adj Close"]/b.Close)/(a.Open*a["Adj Close"]/a.Close)-1),1)))
up=sum(s_["r"]>0 for s_ in summers); print("summers up",up,[s_["r"] for s_ in summers])
oo=pd.Series(o,index=idx).pct_change().shift(-1).fillna(0); wm=pd.Series(idx.month,index=idx).isin(WIN)
wmult=round(float((1+oo[wm]).prod()),2); smult=round(float((1+oo[~wm]).prod()),2); print("mult winter",wmult,"summer",smult)
ddate=(eq/eq.cummax()-1).idxmin(); print("sim dd date",ddate.date())
# per-year: winter vs summer avg
print("trade win rate (winter holds)",r["win"])
out=dict(sim=r,bh=dict(v=round(bh.iloc[-1]),dd=bhdd),fees={str(k):v for k,v in fees.items()},ten=dict(sim=r10["v"],bh=bh10),
         summer_only=rs,summers=summers,summers_up=int(up),wmult=wmult,smult=smult,summer2008=summers[3]["r"])
json.dump(out,open("results.json","w"),indent=1)
pd.DataFrame({"sim":eq,"bh":bh,"pos":pos,"close":c},index=idx).to_csv("sim.csv")
