# Autopsy #18 - "The simple trend rule": hold SPY while the close is above its 200-day SMA, cash (0%) when below.
# Signal at close -> fill next open, 0.05%/side. Warm-up 200 bars excluded; buy & hold over the same dates.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; P=df["Close"].values; idx=df.index; N=len(C)
FEE=0.0005; W=200
sma=pd.Series(P).rolling(W).mean().values   # rule uses the price chart people see (nominal close vs its 200-day avg)
sig=(P>sma).astype(float); sig[:W-1]=np.nan
S=W  # first tradable day (signal of day W-1 fills at open of day W)
def run(fee=FEE,sig=sig,start=S):
    cash=10000.0; sh=0.0; eq=np.full(N,np.nan); trades=[]; ent=None; inmk=0
    for i in range(start,N):
        want=sig[i-1]
        if want==1 and sh==0: sh=cash*(1-fee)/O[i]; ent=(i,cash); cash=0.0
        elif want==0 and sh>0: cash=sh*O[i]*(1-fee); trades.append((str(idx[ent[0]].date()),str(idx[i].date()),cash/ent[1]-1)); sh=0.0
        eq[i]=cash+sh*C[i]; inmk+= sh>0
    return eq,trades,inmk/(N-start)
eq,tr,tim=run()
bh=np.full(N,np.nan); bh[S:]=10000*(1-FEE)/O[S]*C[S:]
def dd(x): x=x[~np.isnan(x)]; return float((x/np.maximum.accumulate(x)-1).min())
yrs=(idx[-1]-idx[S]).days/365.25
out=dict(start=str(idx[S].date()),final=round(float(eq[-1])),bh=round(float(bh[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),
 bh_cagr=round(100*((bh[-1]/1e4)**(1/yrs)-1),2),mdd=round(100*dd(eq),1),bh_mdd=round(100*dd(bh),1),time_in=round(100*tim,1),
 trades=len(tr),winrate=round(100*np.mean([t[2]>0 for t in tr]),1),
 fee10=round(float(run(0.001)[0][-1])),fee20=round(float(run(0.002)[0][-1])),fee0=round(float(run(0)[0][-1])))
# monthly check variant (Faber-ish: month-end close vs 200d SMA, fill next open)
me=pd.Series(1,index=idx).groupby(idx.to_period("M")).tail(1).index
msig=np.full(N,np.nan); last=np.nan
for i in range(W-1,N):
    if idx[i] in me: last=sig[i]
    msig[i]=last
eqm,trm,timm=run(sig=msig); out["monthly_final"]=round(float(eqm[-1])); out["monthly_trades"]=len(trm); out["monthly_mdd"]=round(100*dd(eqm),1)
# 2008: where was the rule at the 2009 low, and when did it buy back
for y in range(2006,2025):
    pass
ye=pd.DataFrame({"R":pd.Series(eq,idx).resample("YE").last(),"B":pd.Series(bh,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):[int(v.R),int(v.B)] for k,v in ye.iterrows() if not np.isnan(v.R)}
# whipsaw: trades lasting <= 10 trading days
lens=[(idx.get_loc(pd.Timestamp(b))-idx.get_loc(pd.Timestamp(a))) for a,b,_ in tr]
out["short_trades"]=sum(l<=10 for l in lens); out["losing_trades"]=sum(t[2]<=0 for t in tr)
# leader timeline: first date rule ahead of B&H, last date ahead
ahead=(eq>bh)&~np.isnan(eq)
out["ahead_pct"]=round(100*ahead[S:].mean(),1)
lastahead=np.where(ahead)[0]; out["last_ahead"]=str(idx[lastahead[-1]].date()) if len(lastahead) else None
fa=np.where(ahead)[0]; out["first_ahead"]=str(idx[fa[0]].date()) if len(fa) else None
# best/worst years vs
for y in ("2008","2009","2020","2022"):
    sl=(idx.year==int(y)); a=eq[sl]; b=bh[sl]; out["y"+y]=[round(100*(a[-1]/a[0]-1),1),round(100*(b[-1]/b[0]-1),1)]
# 2020 detail: sell date, rebuy date, price change between
t20=[t for t in tr if t[0]>="2019-06" and t[0]<"2021"]; out["trades2020"]=t20
t08=[t for t in tr if t[0]>="2007-06" and t[0]<"2010"]; out["trades0809"]=[(a,b,round(100*c,1)) for a,b,c in t08]
json.dump(out,open("results18.json","w"),indent=1,default=float)
pd.DataFrame({"R":eq,"B":bh,"P":P,"SMA":sma,"IN":sig},index=idx).to_csv("sim18.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},default=float)); print(out["year_end"])
# independent check of B&H
print("check bh", 10000*(1-FEE)*C[-1]/O[S])
