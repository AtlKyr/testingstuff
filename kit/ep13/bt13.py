# Autopsy #13 - The Monday effect. SPY 2005-2024, adj close-to-close daily returns by weekday.
# "Monday return" = previous trading day's close -> Monday close (includes the weekend).
# Mondays-only trader: buys at the close before each Monday (usually Friday), sells at Monday's close.
# Never-Monday trader: sells at the close before each Monday, buys back at Monday's close (owns every other day).
# Fills at the close (the topic is about which day you own), 0.05% per side, cash 0%, $10,000.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
C=df["Adj Close"].values; idx=df.index; N=len(C); FEE=0.0005; yrs=(idx[-1]-idx[0]).days/365.25
r=np.r_[np.nan,C[1:]/C[:-1]-1]; wd=idx.dayofweek.values
names=["Mon","Tue","Wed","Thu","Fri"]
out={"by_day":{}}
for d in range(5):
    m=(wd==d)&~np.isnan(r); v=r[m]
    out["by_day"][names[d]]=dict(n=int(m.sum()),avg_bp=round(1e4*v.mean(),2),up=round(100*(v>0).mean(),1),
        growth=round(float(np.prod(1+v)),3),worst=round(100*v.min(),1),best=round(100*v.max(),1))
mon=(wd==0)&~np.isnan(r)
# first-trading-day-of-week variant (Tuesday after a Monday holiday)
wk=pd.Series(idx).dt.isocalendar().week.values; yr=pd.Series(idx).dt.isocalendar().year.values
first=np.r_[True,(wk[1:]!=wk[:-1])|(yr[1:]!=yr[:-1])]; first[0]=False
def run(mask,fee=FEE):
    eq=np.zeros(N); v=10000.0; trades=0; inm=np.zeros(N,bool)
    for i in range(N):
        if i>0 and mask[i]:
            v=v*(1-fee)*(1+r[i])*(1-fee); trades+=1; inm[i]=True
        eq[i]=v
    return eq,trades,inm
def stats(eq,inm=None,tr=None):
    s=pd.Series(eq,idx); d=dict(v=round(float(eq[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1))
    if inm is not None: d["tim"]=round(100*inm.mean(),1)
    if tr is not None: d["trades"]=tr
    return d
bh=10000*C/C[0]*(1-FEE)**2; out["bh"]=stats(bh)
eqM,tM,iM=run(mon); out["mon_only"]=stats(eqM,iM,tM)
# never-monday: owns every day except Mondays; one round trip per week that contains a Monday
notmon=(~mon)&~np.isnan(r)
eqN=np.zeros(N); v=10000*(1-FEE); tN=0
for i in range(1,N):
    if mon[i]:
        v=v*(1-FEE)*(1-FEE); tN+=1   # sell at close before Monday, buy back at Monday close
    else: v=v*(1+r[i])
    eqN[i]=v
eqN[0]=10000*(1-FEE); out["never_mon"]=stats(eqN,None,tN)
out["mon_only_nofee"]=round(float(run(mon,0)[0][-1])); 
v=10000.0
for i in range(1,N):
    if not mon[i]: v*=1+r[i]
out["never_mon_nofee"]=round(v)
for d in range(1,5):
    m=(wd==d)&~np.isnan(r); out[f"{names[d]}_only_nofee"]=round(float(run(m,0)[0][-1])); out[f"{names[d]}_only"]=round(float(run(m)[0][-1]))
out["first_day_only_nofee"]=round(float(run(first,0)[0][-1]))
# by period: Monday avg return by 5y block
out["mon_by_block"]={f"{a}-{a+4}":round(1e4*np.nanmean(r[mon&(idx.year>=a)&(idx.year<=a+4)]),1) for a in (2005,2010,2015,2020)}
out["mon_by_year_growth"]={int(y):round(float(np.prod(1+r[mon&(idx.year==y)])-1)*100,1) for y in range(2005,2025)}
out["mon_worst_dates"]=[(str(idx[i].date()),round(100*r[i],1)) for i in np.argsort(np.where(mon,r,9))[:5]]
out["mon_best_dates"]=[(str(idx[i].date()),round(100*r[i],1)) for i in np.argsort(np.where(mon,r,-9))[-5:]]
ye=pd.DataFrame({"B":pd.Series(bh,idx).resample("YE").last(),"M":pd.Series(eqM,idx).resample("YE").last(),"N":pd.Series(eqN,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
json.dump(out,open("results13.json","w"),indent=1,default=float)
pd.DataFrame({"B":bh,"M":eqM,"N":eqN},index=idx).to_csv("sim13.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},indent=1,default=float)); print(ye.T.to_string())
