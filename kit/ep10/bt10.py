# Autopsy #10 - Buy after 3 down days in a row, SPY 2005-2024.
# Rule: when SPY closes DOWN (adj close < previous adj close) 3 days in a row and we are flat -> BUY at next open.
# Exit: first UP close -> SELL at next open. Long only, 0.05% per side, cash 0%, $10,000. No indicator warm-up needed
# (needs 3 prior closes); signals start at bar 4. Buy & hold over the same dates: first open -> last adj close.
import pandas as pd, numpy as np, json, sys
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
yrs=(idx[-1]-idx[0]).days/365.25
def run(k=3, fee=0.0005, exit_mode="upclose", hold=None):
    cash=10000.0; sh=0.0; pos=False; eq=np.zeros(N); inm=np.zeros(N,bool); trades=[]; ent=None; pend=None; held=0
    for i in range(N):
        # execute pending order at today's open
        if pend=="buy":
            sh=cash*(1-fee)/O[i]; ent=(i,cash); cash=0; pos=True; held=0
        elif pend=="sell":
            cash=sh*O[i]*(1-fee); trades.append(dict(entry=str(idx[ent[0]].date()),exit=str(idx[i].date()),ret=cash/ent[1]-1,days=i-ent[0])); sh=0; pos=False
        pend=None
        eq[i]=cash+sh*C[i]; inm[i]=pos
        if i<k: continue
        down=all(C[i-j]<C[i-j-1] for j in range(k))
        if not pos and down: pend="buy"
        elif pos:
            held+=1
            if exit_mode=="upclose" and C[i]>C[i-1]: pend="sell"
            if exit_mode=="hold" and held>=hold: pend="sell"
    return eq,inm,trades
def stats(eq,inm,tr):
    s=pd.Series(eq,idx); w=[t["ret"] for t in tr]
    return dict(v=round(eq[-1]),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1),
        tim=round(100*inm.mean(),1),trades=len(tr),win=round(100*np.mean([x>0 for x in w]),1) if w else 0,
        avg=round(100*np.mean(w),3) if w else 0,hold=round(np.mean([t["days"] for t in tr]),1) if tr else 0)
bh=10000*(1-0.0005)*C/O[0]; B=pd.Series(bh,idx)
out=dict(start=str(idx[0].date()),end=str(idx[-1].date()),bh=dict(v=round(bh[-1]),cagr=round(100*((bh[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(B/B.cummax()-1).min(),1)))
eq,inm,tr=run(); out["main"]=stats(eq,inm,tr)
out["fee_stress"]={str(fe):round(run(fee=fe)[0][-1]) for fe in (0.0,0.0005,0.001,0.002)}
for k in (2,4,5): out[f"k{k}"]=stats(*run(k=k))
for h in (1,3,5,10): out[f"hold{h}"]=stats(*run(exit_mode="hold",hold=h))
# per-trade/time facts
S=pd.Series(eq,idx)
out["dd_main"]=out["main"]["dd"]
# return of SPY on days strategy is in vs out (open-to-open contribution approx by close->close of days held)
r=pd.Series(C,idx).pct_change().fillna(0)
ye=pd.DataFrame({"B":B.resample("YE").last(),"S":S.resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
# 2008 & 2020 behaviour
def seg(a,b):
    sa,sb=S[a:b],B[a:b]; return dict(strat=round(100*(sa.iloc[-1]/sa.iloc[0]-1),1),bh=round(100*(sb.iloc[-1]/sb.iloc[0]-1),1),
       strat_dd=round(100*(sa/sa.cummax()-1).min(),1),bh_dd=round(100*(sb/sb.cummax()-1).min(),1))
out["y2008"]=seg("2007-10-09","2009-03-09"); out["covid"]=seg("2020-02-19","2020-03-23")
out["y2008_full"]=seg("2008-01-01","2008-12-31"); out["y2020_full"]=seg("2020-01-01","2020-12-31")
# triggers count, % of 3-down streaks followed by up day next
dn=(pd.Series(C).diff()<0).values
trig=[i for i in range(3,N-1) if dn[i] and dn[i-1] and dn[i-2]]
out["n_streak_days"]=len(trig)
out["next_day_up_after_3down_pct"]=round(100*np.mean([C[i+1]>C[i] for i in trig]),1)
out["base_up_day_pct"]=round(100*np.mean(np.diff(C)>0),1)
# best/worst trade
w=sorted(tr,key=lambda t:t["ret"]); out["worst_trades"]=[dict(t,ret=round(100*t["ret"],1)) for t in w[:5]]; out["best_trades"]=[dict(t,ret=round(100*t["ret"],1)) for t in w[-5:]]
out["trades_per_year"]=round(len(tr)/yrs,1)
out["fees_paid_share"]=None
json.dump(out,open("results10.json","w"),indent=1,default=float)
pd.DataFrame({"B":B,"S":S,"IN":inm.astype(int)}).to_csv("sim10.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},indent=1,default=float)); print(ye.T.to_string())
