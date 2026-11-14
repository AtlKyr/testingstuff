# Autopsy #23 - "The 10% stop-loss": hold SPY; if the close falls >=10% below the highest close since you bought -> sell next open.
# Buy back when the close rises >=10% above the lowest close since you sold -> buy next open. Adj Close signals.
# 0.05%/side, cash 0%, $10K, start 2005-01-03 open (no warm-up needed). B&H same dates.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
FEE=0.0005
def run(stop=0.10,back=0.10,fee=FEE):
    sh=10000*(1-fee)/O[0]; cash=0.0; eq=np.full(N,np.nan); INA=np.zeros(N); hi=C[0]; lo=None; pend=None; tr=[]; ent=(0,10000.0); inm=0; ev=[]
    for i in range(N):
        if pend=="sell": cash=sh*O[i]*(1-fee); tr.append((ent[0],i,cash/ent[1]-1)); sh=0.0; lo=C[i]; ev.append(("S",i)); pend=None
        elif pend=="buy": sh=cash*(1-fee)/O[i]; ent=(i,cash); cash=0.0; hi=C[i]; ev.append(("B",i)); pend=None
        if sh>0:
            hi=max(hi,C[i])
            if C[i]<=hi*(1-stop): pend="sell"
        else:
            lo=min(lo,C[i])
            if C[i]>=lo*(1+back): pend="buy"
        eq[i]=cash+sh*C[i]; inm+=sh>0; INA[i]=1.0 if sh>0 else 0.0
    global LASTIN; LASTIN=INA
    return eq,tr,inm/N,ev
eq,tr,tim,ev=run(); INV=LASTIN.copy()
bh=10000*(1-FEE)/O[0]*C
def dd(x): return float((x/np.maximum.accumulate(x)-1).min())
yrs=(idx[-1]-idx[0]).days/365.25
out=dict(final=round(float(eq[-1])),bh=round(float(bh[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),bh_cagr=round(100*((bh[-1]/1e4)**(1/yrs)-1),2),
 mdd=round(100*dd(eq),1),bh_mdd=round(100*dd(bh),1),time_in=round(100*tim,1),trades=len(tr),winrate=round(100*np.mean([t[2]>0 for t in tr]),1),
 fee0=round(float(run(fee=0)[0][-1])),fee10=round(float(run(fee=0.001)[0][-1])),fee20=round(float(run(fee=0.002)[0][-1])))
out["scan"]={f"{s}/{b}":round(float(run(s,b)[0][-1])) for s in (0.05,0.10,0.15,0.20) for b in (0.05,0.10,0.15)}
# each sell/buy pair: sold price vs bought back price
pairs=[]
evs=ev
for k in range(0,len(evs)-1):
    if evs[k][0]=="S" and evs[k+1][0]=="B":
        s=evs[k][1]; b=evs[k+1][1]; pairs.append((str(idx[s].date()),str(idx[b].date()),round(100*(O[b]/O[s]-1),1)))
out["pairs"]=pairs; out["rebuy_higher"]=sum(p[2]>0 for p in pairs)
ye=pd.DataFrame({"R":pd.Series(eq,idx).resample("YE").last(),"B":pd.Series(bh,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):[int(v.R),int(v.B)] for k,v in ye.iterrows()}
for yy in ("2008","2009","2018","2020","2022"):
    sl=(idx.year==int(yy)); a=eq[sl]; b=bh[sl]; out["y"+yy]=[round(100*(a[-1]/a[0]-1),1),round(100*(b[-1]/b[0]-1),1)]
json.dump(out,open("results23.json","w"),indent=1,default=float)
pd.DataFrame({"R":eq,"B":bh,"IN":INV,"O":O,"C":C},index=idx).to_csv("sim23.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},default=float)); print(out["year_end"])
