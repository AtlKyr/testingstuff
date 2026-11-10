# Autopsy #14 - "Big green day": after SPY closes up >= +2.0% (adj close-to-close), is the worst over?
# Bounce chaser: signal at close -> buy NEXT OPEN, hold HOLD trading days (sell at the open of the HOLD-th trading day after
# entry); a new signal while holding restarts the clock. 0.05% per side, cash 0%, $10,000. Buy & hold: first open -> last close.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
yrs=(idx[-1]-idx[0]).days/365.25; FEE=0.0005
r=np.r_[np.nan,C[1:]/C[:-1]-1]
def chase(H=21,thr=0.02,fee=FEE):
    cash=10000.0; sh=0.0; exit_i=-1; trades=[]; inm=np.zeros(N,bool); eq=np.zeros(N); entry=0; log=[]
    for i in range(N):
        sig = i>0 and r[i-1]>=thr          # yesterday's close was a big green day -> act at today's open
        if sig:
            if sh==0: sh=cash*(1-fee)/O[i]; entry=cash; cash=0.0; ei=i
            exit_i=i+H
        elif sh>0 and i==exit_i:
            cash=sh*O[i]*(1-fee); trades.append(cash/entry-1); log.append((str(idx[ei].date()),str(idx[i].date()),round(100*(cash/entry-1),2))); sh=0.0
        inm[i]=sh>0; eq[i]=cash+sh*C[i]
    return eq,trades,inm,log
def stats(eq,tr=None,inm=None):
    s=pd.Series(eq,idx); d=dict(v=round(float(eq[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1))
    if tr is not None: d.update(trades=len(tr),win=round(100*np.mean(np.array(tr)>0),1),avg=round(100*np.mean(tr),2))
    if inm is not None: d["tim"]=round(100*inm.mean(),1)
    return d
out={}
bh=10000*(1-FEE)/O[0]*C; out["bh"]=stats(bh)
eq,tr,inm,log=chase(); out["chaser"]=stats(eq,tr,inm); out["open_at_end"]=bool(inm[-1])
out["fee_010"]=stats(chase(fee=0.001)[0])["v"]; out["fee_020"]=stats(chase(fee=0.002)[0])["v"]; out["fee_0"]=stats(chase(fee=0)[0])["v"]
out["hold_variants"]={h:stats(chase(H=h)[0])["v"] for h in (1,5,10,21,42,63,126,252)}
out["hold_scan_wins"]=int(sum(chase(H=h)[0][-1]>bh[-1] for h in range(1,253)))
out["thr_variants"]={str(t):stats(chase(thr=t)[0])["v"] for t in (0.015,0.02,0.025,0.03)}
big=np.where(r>=0.02)[0]; out["n_big"]=int(len(big)); out["n_days"]=int(N-1)
out["by_year"]={int(y):int((idx[big].year==y).sum()) for y in range(2005,2025)}
peak=np.maximum.accumulate(C); dd=C/peak-1
out["big_prior_dd_le10"]=int((dd[big-1]<=-0.10).sum()); out["big_prior_dd_le20"]=int((dd[big-1]<=-0.20).sum())
out["share_days_dd_le10"]=round(100*(dd<=-0.10).mean(),1)
sma=pd.Series(C).rolling(200).mean().values
v=big[big>200]; out["big_below_sma200"]=[int((C[v-1]<sma[v-1]).sum()),int(len(v))]
# "erased": within the next K trading days the market CLOSED below the close of the day BEFORE the jump
for K in (21,63,126):
    ok=[i for i in big if i+K<N]; e=sum(C[i+1:i+K+1].min()<C[i-1] for i in ok); out[f"erased_{K}"]=[int(e),len(ok),round(100*e/len(ok),1)]
# same test for all days (baseline): close below the prior-day close within K days
ok=[i for i in range(1,N-63)]; e=sum(C[i+1:i+64].min()<C[i-1] for i in ok); out["erased_63_anyday"]=round(100*e/len(ok),1)
# lower low than the close of the jump day itself within 63d
ok=[i for i in big if i+63<N]; out["below_jumpclose_63"]=[int(sum(C[i+1:i+64].min()<C[i] for i in ok)),len(ok)]
# forward returns (next open -> close h days later)
fw={}
for h in (1,21,63,252):
    a=np.array([C[i+h]/O[i+1]-1 for i in big if i+h<N]); b=np.array([C[i+h]/O[i+1]-1 for i in range(1,N-h)])
    fw[h]=dict(n=len(a),mean=round(100*a.mean(),2),up=round(100*(a>0).mean(),1),any_mean=round(100*b.mean(),2),any_up=round(100*(b>0).mean(),1))
out["fwd"]=fw
nx=r[big[big+1<N]+1]; out["next_day"]=dict(mean=round(100*nx.mean(),3),up=round(100*(nx>0).mean(),1),any_mean=round(100*np.nanmean(r),3),any_up=round(100*np.nanmean(r[1:]>0),1))
out["top5"]=[(str(idx[i].date()),round(100*r[i],2)) for i in big[np.argsort(r[big])[-5:]]]
ye=pd.DataFrame({"B":pd.Series(bh,idx).resample("YE").last(),"S":pd.Series(eq,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
yi=pd.Series(inm,idx).groupby(idx.year).mean(); out["tim_by_year"]={int(k):round(100*v,0) for k,v in yi.items()}
# longest stretch in cash
best=(0,None,None); st=None
for i in range(N):
    if not inm[i]:
        if st is None: st=i
        if i-st+1>best[0]: best=(i-st+1,str(idx[st].date()),str(idx[i].date()))
    else: st=None
out["longest_cash"]=best
# independent vectorised check of the chaser (position array -> returns)
pos=np.zeros(N,bool); last=-10**9
for i in range(N):
    if i>0 and r[i-1]>=0.02: last=i
    pos[i]= (i-last)<21 and last>0      # holds from open of day `last` up to the open of day last+21
v=10000.0; held=False
for i in range(N):
    if pos[i] and not held: v*=(1-FEE); v*=C[i]/O[i]; held=True
    elif pos[i] and held: v*=C[i]/C[i-1]
    elif (not pos[i]) and held: v*=O[i]/C[i-1]*(1-FEE); held=False
out["check_v"]=round(v)
json.dump(out,open("results14.json","w"),indent=1,default=float)
pd.DataFrame({"B":bh,"S":eq,"inm":inm.astype(int),"big":(r>=0.02).astype(int),"C":C},index=idx).to_csv("sim14.csv")
print(json.dumps({k:v for k,v in out.items() if k not in("year_end",)},indent=0,default=float)); print(ye.T.to_string()); print(log[:6], len(log))
