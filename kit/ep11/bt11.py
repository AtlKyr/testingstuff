# Autopsy #11 - "The Nasdaq just crashed. What happens next?" SPY 2005-2024.
# Crash day = SPY adj close-to-close return <= -4%. Forward returns measured close->close (1d/21d/252d).
# Panic seller: holds SPY; on a crash day close -> SELL at next open; stays out N trading days -> BUY back at open.
# Holder: buy at first open, hold. 0.05% per side, cash 0%, $10,000. No indicator -> no warm-up.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
FEE=0.0005; yrs=(idx[-1]-idx[0]).days/365.25
r=np.full(N,np.nan); r[1:]=C[1:]/C[:-1]-1
crash=np.where(r<=-0.04)[0]
def fw(i,n): return C[i+n]/C[i]-1 if i+n<N else np.nan
out={"n_crash":int(len(crash))}
out["by_year"]=pd.Series(idx[crash].year).value_counts().sort_index().astype(int).to_dict()
for nm,n in (("d1",1),("m1",21),("y1",252)):
    v=np.array([fw(i,n) for i in crash]); v=v[~np.isnan(v)]
    base=np.array([fw(i,n) for i in range(1,N-n)])
    out[nm]=dict(n=len(v),up=int((v>0).sum()),pct=round(100*(v>0).mean(),1),median=round(100*np.median(v),1),base_pct=round(100*(base>0).mean(),1))
out["y1_down"]=[str(idx[i].date()) for i in crash if i+252<N and fw(i,252)<=0]
out["worst"]=dict(date=str(idx[np.nanargmin(r)].date()),ret=round(100*np.nanmin(r),1))
def stats(eq,inm=None):
    s=pd.Series(eq,idx); d=dict(v=round(float(eq[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1))
    if inm is not None: d["tim"]=round(100*inm.mean(),1)
    return d
bh=10000*(1-FEE)*C/O[0]; out["bh"]=stats(bh)
def panic(hold,fee=FEE):
    sh=10000*(1-fee)/O[0]; cash=0.0; pend=None; back=None; eq=np.zeros(N); inm=np.zeros(N,bool); sells=0; tr=[]
    for i in range(N):
        if pend=="sell": cash=sh*O[i]*(1-fee); sh=0.0; back=i+hold; sells+=1; sold_px=O[i]
        elif sh==0 and back is not None and i>=back:
            sh=cash*(1-fee)/O[i]; cash=0.0; tr.append(O[i]/sold_px-1); back=None
        pend=None
        eq[i]=cash+sh*C[i]; inm[i]=sh>0
        if sh>0 and r[i]<=-0.04 and i+1<N: pend="sell"
    return eq,inm,sells,tr
P={}
for h,lab in ((5,"1w"),(10,"2w"),(21,"1m"),(63,"3m"),(126,"6m")):
    eq,inm,s,tr=panic(h); d=stats(eq,inm); d["sells"]=s; d["rebuy_higher"]=int(sum(x>0 for x in tr)); d["rebuys"]=len(tr); P[lab]=d
    if lab=="1m": eq1m=eq
out["panic"]=P
out["fee_stress_1m"]={str(fe):round(float(panic(21,fe)[0][-1])) for fe in (0.0005,0.001,0.002)}
out["hold_scan"]={h:round(float(panic(h)[0][-1])) for h in range(1,127)}
wins=[h for h,v in out["hold_scan"].items() if v>out["bh"]["v"]]; out["winning_holds"]=[min(wins),max(wins),len(wins)] if wins else []
best=np.argsort(np.nan_to_num(r,nan=0))[-10:]
out["best10_near_crash"]=int(sum(min(abs(b-c) for c in crash)<=10 for b in best))
ye=pd.DataFrame({"B":pd.Series(bh,idx).resample("YE").last(),"P":pd.Series(eq1m,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
json.dump(out,open("results11.json","w"),indent=1,default=float)
pd.DataFrame({"B":bh,"P":eq1m},index=idx).to_csv("sim11.csv")
o={k:v for k,v in out.items() if k not in ("year_end","hold_scan")}; print(json.dumps(o,indent=1,default=float)); print(ye.T.to_string())
