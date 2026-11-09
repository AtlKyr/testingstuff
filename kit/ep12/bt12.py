# Autopsy #12 - "Wait for a pullback" vs buy & hold. SPY 2005-2024.
# Record = highest NOMINAL SPY close so far, seeded with the 2000 peak (S&P 1527.46 on 2000-03-24 ~ SPY 152.7).
# Pullback waiter: if close <= record*(1-X) -> buy next open; if close makes a new record (> previous record) -> sell next open.
# 0.05% per side, cash 0%, $10,000. Buy & hold = first open -> last close (adj).
import pandas as pd, numpy as np, json, sys
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; P=df["Close"].values; idx=df.index; N=len(C)
FEE=0.0005; yrs=(idx[-1]-idx[0]).days/365.25
def records(seed):
    rec=np.zeros(N); newrec=np.zeros(N,bool); m=seed
    for i in range(N):
        if P[i]>m: newrec[i]=True; m=P[i]
        rec[i]=m
    return rec,newrec
def stats(eq,inm=None):
    s=pd.Series(eq,idx); d=dict(v=round(float(eq[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1))
    if inm is not None: d["tim"]=round(100*inm.mean(),1)
    return d
def waiter(X=0.05,seed=152.7,fee=FEE):
    rec,newrec=records(seed)
    cash=10000.0; sh=0.0; pend=None; eq=np.zeros(N); inm=np.zeros(N,bool); trades=[]; ent=None; buys=[]; sells=[]
    for i in range(N):
        if pend=="buy": sh=cash*(1-fee)/O[i]; cash=0.0; ent=O[i]; buys.append(i)
        elif pend=="sell": cash=sh*O[i]*(1-fee); sh=0.0; trades.append(O[i]/ent-1); sells.append(i)
        pend=None
        eq[i]=cash+sh*C[i]; inm[i]=sh>0
        if i+1<N:
            if sh==0 and P[i]<=rec[i]*(1-X): pend="buy"
            elif sh>0 and newrec[i]: pend="sell"
    return eq,inm,trades,buys,sells
bh=10000*(1-FEE)*C/O[0]
out={"bh":stats(bh)}
rec,newrec=records(152.7)
out["n_records"]=int(newrec.sum()); out["records_by_year"]={str(k):int(v) for k,v in pd.Series(newrec,idx).groupby(idx.year).sum().items()}
out["first_record"]=str(idx[np.argmax(newrec)].date())
dd=P/rec-1; out["pct_time_within5"]=round(100*(dd>-0.05).mean(),1)
def fw(i,n): return C[i+n]/C[i]-1
R=[i for i in range(N-252) if newrec[i]]; A=list(range(N-252))
out["fwd1y_after_record"]=dict(n=len(R),up=round(100*np.mean([fw(i,252)>0 for i in R]),1),avg=round(100*np.mean([fw(i,252) for i in R]),1))
out["fwd1y_all"]=dict(up=round(100*np.mean([fw(i,252)>0 for i in A]),1),avg=round(100*np.mean([fw(i,252) for i in A]),1))
D=[i for i in A if dd[i]<=-0.05]
out["fwd1y_5pct_below"]=dict(n=len(D),up=round(100*np.mean([fw(i,252)>0 for i in D]),1),avg=round(100*np.mean([fw(i,252) for i in D]),1))
eq,inm,tr,buys,sells=waiter()
d=stats(eq,inm); d["trades"]=len(tr); d["win"]=round(100*np.mean([t>0 for t in tr]),1); out["waiter5"]=d
out["buys"]=[str(idx[i].date()) for i in buys]; out["sells"]=[str(idx[i].date()) for i in sells]
for X in (0.03,0.10,0.20): e=waiter(X)[0]; out[f"waiter{int(X*100)}"]=round(float(e[-1]))
out["seed_sens"]={str(s):round(float(waiter(seed=s)[0][-1])) for s in (150,152.7,155)}
out["fee_stress"]={str(fe):round(float(waiter(fee=fe)[0][-1])) for fe in (0.0005,0.001,0.002)}
# longest stretch in cash
gaps=[]; 
for s in sells:
    nb=[b for b in buys if b>s]; e=nb[0] if nb else N-1
    gaps.append((e-s, str(idx[s].date()), str(idx[e].date()), round(100*(P[e]/P[s]-1),1)))
gaps.sort(reverse=True); out["longest_waits"]=gaps[:5]
# never-came-back: sells where the next buy price was HIGHER than sell price
out["rebuy_higher"]=sum(1 for s in sells for nb in [[b for b in buys if b>s]] if nb and O[nb[0]]>O[s]); out["n_sells"]=len(sells)
ye=pd.DataFrame({"B":pd.Series(bh,idx).resample("YE").last(),"W":pd.Series(eq,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
json.dump(out,open("results12.json","w"),indent=1,default=float)
pd.DataFrame({"B":bh,"W":eq,"inm":inm.astype(int),"rec":rec,"P":P},index=idx).to_csv("sim12.csv")
o={k:v for k,v in out.items() if k not in ("year_end","buys","sells")}; print(json.dumps(o,indent=1,default=float)); print(ye.T.to_string())
