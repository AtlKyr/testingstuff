# Autopsy #20 - "Yields spike -> sell stocks?": 10-year Treasury yield (FRED DGS10, end of day).
# Rule: if the 10y yield is >= +1.00 point above its level 252 trading days earlier -> cash; else hold SPY.
# Signal at close -> fill next open, 0.05%/side, cash 0%. Warm-up: first 252 bars excluded; B&H over same dates.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
y=pd.read_csv("dgs10.csv",parse_dates=["observation_date"]).set_index("observation_date")["DGS10"]
y=pd.to_numeric(y,errors="coerce").ffill()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
Y=y.reindex(idx,method="ffill").values
FEE=0.0005; W=252
def mk(th):
    ch=np.full(N,np.nan); ch[W:]=Y[W:]-Y[:-W]
    s=np.where(ch>=th,0.0,1.0); s[:W]=np.nan; return s,ch
S=W+1
def run(sig,fee=FEE,start=S):
    cash=10000.0; sh=0.0; eq=np.full(N,np.nan); trades=[]; ent=None; inmk=0
    for i in range(start,N):
        want=sig[i-1]
        if want==1 and sh==0: sh=cash*(1-fee)/O[i]; ent=(i,cash); cash=0.0
        elif want==0 and sh>0: cash=sh*O[i]*(1-fee); trades.append((str(idx[ent[0]].date()),str(idx[i].date()),cash/ent[1]-1)); sh=0.0
        eq[i]=cash+sh*C[i]; inmk+= sh>0
    return eq,trades,inmk/(N-start)
sig,ch=mk(1.0)
eq,tr,tim=run(sig)
bh=np.full(N,np.nan); bh[S:]=10000*(1-FEE)/O[S]*C[S:]
def dd(x): x=x[~np.isnan(x)]; return float((x/np.maximum.accumulate(x)-1).min())
yrs=(idx[-1]-idx[S]).days/365.25
out=dict(start=str(idx[S].date()),final=round(float(eq[-1])),bh=round(float(bh[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),
 bh_cagr=round(100*((bh[-1]/1e4)**(1/yrs)-1),2),mdd=round(100*dd(eq),1),bh_mdd=round(100*dd(bh),1),time_in=round(100*tim,1),
 trades=len(tr),winrate=round(100*np.mean([t[2]>0 for t in tr]),1) if tr else None,
 fee10=round(float(run(sig,0.001)[0][-1])),fee20=round(float(run(sig,0.002)[0][-1])),fee0=round(float(run(sig,0)[0][-1])))
out["variants"]={str(th):round(float(run(mk(th)[0])[0][-1])) for th in (0.5,0.75,1.0,1.25,1.5,2.0)}
# cash spells
cash=(sig==0); spells=[]; i=S
while i<N:
    if cash[i]:
        j=i
        while j+1<N and cash[j+1]: j+=1
        spells.append((str(idx[i].date()),str(idx[min(j+1,N-1)].date()),j-i+1, round(100*(C[min(j+2,N-1)]/C[i+1]-1),1) if i+1<N else None)); i=j+1
    else: i+=1
out["cash_spells"]=spells
ye=pd.DataFrame({"R":pd.Series(eq,idx).resample("YE").last(),"B":pd.Series(bh,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):[int(v.R),int(v.B)] for k,v in ye.iterrows() if not np.isnan(v.R)}
ahead=(eq>bh)&~np.isnan(eq); out["ahead_pct"]=round(100*ahead[S:].mean(),1)
for yy in ("2008","2013","2018","2020","2022","2023"):
    sl=(idx.year==int(yy)); a=eq[sl]; b=bh[sl]; out["y"+yy]=[round(100*(a[-1]/a[0]-1),1),round(100*(b[-1]/b[0]-1),1)]
# yield >= 5% days in data
y5=idx[(Y>=5.0)]; out["y5_days"]=len(y5); out["y5_first"]=str(y5[0].date()) if len(y5) else None; out["y5_last"]=str(y5[-1].date()) if len(y5) else None
out["ymax"]=[float(np.nanmax(Y)),str(idx[np.nanargmax(Y)].date())]
json.dump(out,open("results20.json","w"),indent=1,default=float)
pd.DataFrame({"R":eq,"B":bh,"Y":Y,"CH":ch,"IN":sig},index=idx).to_csv("sim20.csv")
print(json.dumps({k:v for k,v in out.items() if k not in("year_end",)},default=float)); print(out["year_end"])
print("check bh",10000*(1-FEE)*C[-1]/O[S])
