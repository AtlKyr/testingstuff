# Autopsy #15 - Lump sum vs dollar-cost averaging. SPY 2005-2024 (adj). $10,000 arrives on the first trading day of a month.
# ALL-IN: buys everything at that day's OPEN. DRIPPER: buys 1/12 ($833.33) at the OPEN of the first trading day of each of the
# next 12 months (month 0..11); un-invested cash earns 0%. 0.05% cost on every purchase. Compared (a) 12 months after the start
# (open of the first trading day of month 12 -> both fully invested from then on, so the ratio never changes afterwards) and
# (b) for the January-2005 start, at the last close of 2024. Start months: 2005-01 .. 2023-12 (228), so every drip completes.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C); FEE=0.0005
ym=idx.year*12+idx.month-1; first=np.r_[True,ym[1:]!=ym[:-1]]; fi=np.where(first)[0]      # first trading day index of each month
M=len(fi); out={}
def run(m,fee=FEE,months=12):
    """returns (lump_shares, drip_shares) per $10,000 for start month index m"""
    ls=10000*(1-fee)/O[fi[m]]
    ds=sum((10000/months)*(1-fee)/O[fi[m+k]] for k in range(months))
    return ls,ds
rows=[]
for m in range(M-12):
    ls,ds=run(m); p12=O[fi[m+12]]
    # worst paper value during the first 12 months (daily closes)
    a,b=fi[m],fi[m+12]
    lump_path=ls*C[a:b]
    k=np.searchsorted(fi[m:m+12],np.arange(a,b),side="right")          # number of slices bought by each day
    cum=np.cumsum([(10000/12)*(1-FEE)/O[fi[m+j]] for j in range(12)])
    drip_path=cum[k-1]*C[a:b]+10000*(1-k/12)
    rows.append(dict(start=str(idx[fi[m]].date())[:7],lump12=ls*p12,drip12=ds*p12,adv=100*(ls/ds-1),lump_min=lump_path.min(),drip_min=drip_path.min()))
R=pd.DataFrame(rows); n=len(R); R["win"]=R.lump12>R.drip12
out["n_starts"]=n; out["lump_wins"]=int(R.win.sum()); out["lump_win_pct"]=round(100*R.win.mean(),1)
out["avg_lump12"]=round(R.lump12.mean()); out["avg_drip12"]=round(R.drip12.mean()); out["avg_gap"]=round(R.lump12.mean()-R.drip12.mean())
out["median_adv_pct"]=round(R.adv.median(),2); out["mean_adv_pct"]=round(R.adv.mean(),2)
w=R.loc[R.adv.idxmin()]; b=R.loc[R.adv.idxmax()]
out["worst_for_lump"]=dict(start=w.start,lump12=round(w.lump12),drip12=round(w.drip12),adv=round(w.adv,1))
out["best_for_lump"]=dict(start=b.start,lump12=round(b.lump12),drip12=round(b.drip12),adv=round(b.adv,1))
out["wins_by_year"]={int(y):[int(g.win.sum()),len(g)] for y,g in R.groupby(R.start.str[:4].astype(int))}
out["avg_worst_dip"]=dict(lump=round(R.lump_min.mean()),drip=round(R.drip_min.mean()))
out["worst_dip"]=dict(lump=round(R.lump_min.min()),lump_start=R.loc[R.lump_min.idxmin()].start,drip=round(R.drip_min.min()),drip_start=R.loc[R.drip_min.idxmin()].start)
out["below_9000"]=dict(lump=int((R.lump_min<9000).sum()),drip=int((R.drip_min<9000).sum()))
# cumulative scoreboard by start month (for the race visual)
R["cum_l"]=R.win.cumsum(); R["cum_d"]=(~R.win).cumsum()
# the house example: $10,000 in January 2005, valued at the last close of 2024
ls,ds=run(0); out["jan2005"]=dict(lump=round(ls*C[-1]),drip=round(ds*C[-1]))
# longest dripper streak / lump streak
def streak(x):
    best=cur=0; end=None
    for i,v in enumerate(x):
        cur=cur+1 if v else 0
        if cur>best: best=cur; end=i
    return best,R.start[end-best+1],R.start[end]
out["longest_drip_streak"]=streak(~R.win.values); out["longest_lump_streak"]=streak(R.win.values)
# stress: fees 0.20%, drip over 6 / 24 months
for fee in (0.002,):
    w_=sum(run(m,fee)[0]>run(m,fee)[1] for m in range(M-12)); out["wins_fee020"]=int(w_)
for mo in (3,6,24):
    ms=range(M-mo); w_=sum(run(m,FEE,mo)[0]>run(m,FEE,mo)[1] for m in ms); out[f"wins_drip{mo}m"]=[int(w_),len(ms)]
# independent check: simulate one start with a day loop
m=R.adv.idxmin(); cash=10000.0; sh=0.0; nb=0
for i in range(fi[m],fi[m+12]+1):
    if nb<12 and i==fi[m+nb]: sh+=(10000/12)*(1-FEE)/O[i]; cash-=10000/12; nb+=1
    if i==fi[m+12]: chk=sh*O[i]+cash
out["check_worst_drip12"]=round(chk)
# daily paper value of both investors during the worst round (for the on-screen chart); last point = the 12-month comparison value
a,b=fi[m],fi[m+12]; ls=10000*(1-FEE)/O[a]
k=np.searchsorted(fi[m:m+12],np.arange(a,b),side="right"); cum=np.cumsum([(10000/12)*(1-FEE)/O[fi[m+j]] for j in range(12)])
out["worst_paths"]=dict(lump=[round(float(v)) for v in ls*C[a:b]]+[round(float(ls*O[b]))],drip=[round(float(v)) for v in cum[k-1]*C[a:b]+10000*(1-k/12)]+[round(float(cum[-1]*O[b]))])
json.dump(out,open("results15.json","w"),indent=1,default=float); R.to_csv("sim15.csv",index=False)
print(json.dumps({k:v for k,v in out.items() if k!="worst_paths"},indent=0,default=float)[:300]); print(out["worst_paths"]["lump"][-1],out["worst_paths"]["drip"][-1],min(out["worst_paths"]["lump"]),len(out["worst_paths"]["lump"])); print(R[R.start.between("2007-06","2009-06")][["start","lump12","drip12","adv","win"]].round(0).to_string())
