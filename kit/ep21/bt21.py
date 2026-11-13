# Autopsy #21 - Friday the 13th. Close-to-close fills (timing topic): skipper sells at Thursday's close before every
# Friday the 13th and buys back at that Friday's close -> sits out exactly the Friday-13th session. 0.05%/side.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
C=df["Adj Close"].values; idx=df.index; N=len(C); FEE=0.0005
r=np.r_[np.nan,C[1:]/C[:-1]-1]
f13=np.array([(d.weekday()==4 and d.day==13) for d in idx]); f13[0]=False
allfri13=[d for d in pd.date_range("2005-01-03","2024-12-31") if d.weekday()==4 and d.day==13]
def run(skip,fee=FEE):
    eq=np.empty(N); v=10000.0*(1-fee); eq[0]=v
    for i in range(1,N):
        if skip[i]: v=v*(1-fee)*(1-fee)  # sell prev close, rebuy this close
        else: v*=1+r[i]
        eq[i]=v
    return eq
eq=run(f13); bh=run(np.zeros(N,bool))
eq0=run(f13,0)
days=[(str(idx[i].date()),round(100*r[i],2)) for i in np.where(f13)[0]]
rr=np.array([d[1] for d in days])
oth=r[1:][~f13[1:]]
fri=np.array([d.weekday()==4 for d in idx]); fri[0]=False
out=dict(n=len(days),n_calendar=len(allfri13),up=int((rr>0).sum()),down=int((rr<0).sum()),avg=round(float(rr.mean()),3),
 avg_all=round(100*float(np.nanmean(r[1:])),3),up_all=round(100*float((r[1:]>0).mean()),1),
 avg_fri=round(100*float(np.nanmean(r[fri])),3),up_fri=round(100*float((r[fri]>0).mean()),1),
 final=round(float(eq[-1])),bh=round(float(bh[-1])),final_nofee=round(float(eq0[-1])),
 best=max(days,key=lambda d:d[1]),worst=min(days,key=lambda d:d[1]),days=days)
# without the best Friday 13th
best_i=np.where(f13)[0][int(np.argmax(rr))]; sk2=f13.copy(); sk2[best_i]=False
out["final_if_held_best"]=round(float(run(sk2)[-1]))
out["sum_pct"]=round(float(rr.sum()),2); out["prod"]=round(float(np.prod(1+rr/100)),4)
ye={str(y):[round(float(eq[idx.year==y][-1])),round(float(bh[idx.year==y][-1]))] for y in range(2005,2025)}
out["year_end"]=ye
json.dump(out,open("results21.json","w"),indent=1,default=float)
pd.DataFrame({"R":eq,"B":bh,"F13":f13.astype(int)},index=idx).to_csv("sim21.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},default=float)); print(ye)
