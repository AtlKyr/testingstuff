# Autopsy #16 - "Sell when the Fed hikes?" Hike avoider: after every FOMC rate HIKE (fed funds target raised; decision announced
# ~2:15pm ET, so signal at that day's close) -> sell at NEXT OPEN; buy back at the open once 126 trading days (~6 months) have
# passed since the most recent hike with no new hike. 0.05%/side, cash 0%, $10,000. Buy & hold: first open -> last adj close.
import pandas as pd, numpy as np, json
HIKES="""2005-02-02 2005-03-22 2005-05-03 2005-06-30 2005-08-09 2005-09-20 2005-11-01 2005-12-13 2006-01-31 2006-03-28 2006-05-10 2006-06-29
2015-12-16 2016-12-14 2017-03-15 2017-06-14 2017-12-13 2018-03-21 2018-06-13 2018-09-26 2018-12-19
2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14 2023-02-01 2023-03-22 2023-05-03 2023-07-26""".split()
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
yrs=(idx[-1]-idx[0]).days/365.25; FEE=0.0005
hi=[idx.get_loc(pd.Timestamp(d)) for d in HIKES]; assert len(hi)==32
hset=set(hi)
def avoid(W=126,fee=FEE):
    cash=0.0; sh=10000*(1-fee)/O[0]; last=-10**9; inm=np.zeros(N,bool); eq=np.zeros(N); log=[]; out_i=None
    for i in range(N):
        if i>0 and (i-1) in hset:
            last=i-1
            if sh>0: cash=sh*O[i]*(1-fee); sh=0.0; out_i=i
        elif sh==0 and last>=0 and i-last>W:
            sh=cash*(1-fee)/O[i]; log.append((str(idx[out_i].date()),str(idx[i].date()),round(100*(O[i]/O[out_i]-1),1))); cash=0.0
        inm[i]=sh>0; eq[i]=cash+sh*C[i]
    return eq,inm,log
def stats(eq,inm=None):
    s=pd.Series(eq,idx); d=dict(v=round(float(eq[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),dd=round(100*(s/s.cummax()-1).min(),1))
    if inm is not None: d["tim"]=round(100*inm.mean(),1)
    return d
out={}
bh=10000*(1-FEE)/O[0]*C; out["bh"]=stats(bh)
eq,inm,log=avoid(); out["avoider"]=stats(eq,inm); out["periods_out"]=log; out["in_at_end"]=bool(inm[-1])
out["fee_0"]=stats(avoid(fee=0)[0])["v"]; out["fee_020"]=stats(avoid(fee=0.002)[0])["v"]
out["wait_variants"]={w:stats(avoid(W=w)[0])["v"] for w in (21,63,126,252)}
out["wait_scan_wins"]=[int(sum(avoid(W=w)[0][-1]>bh[-1] for w in range(5,253,5))),len(range(5,253,5))]
# forward returns after each hike: next open -> close 252 days later
fw=[(HIKES[k],round(100*(C[i+252]/O[i+1]-1),1)) for k,i in enumerate(hi) if i+252<N]
out["fwd252"]=fw; out["fwd252_up"]=[sum(v>0 for _,v in fw),len(fw)]
out["fwd252_mean"]=round(np.mean([v for _,v in fw]),1)
a=np.array([C[i+252]/O[i+1]-1 for i in range(0,N-253)]); out["any_252_mean"]=round(100*a.mean(),1); out["any_252_up"]=round(100*(a>0).mean(),1)
# each hiking cycle: close of first-hike day -> close of last-hike day
cyc=[(HIKES[0],HIKES[11]),(HIKES[12],HIKES[20]),(HIKES[21],HIKES[31])]
out["cycles"]=[(a_,b_,round(100*(C[idx.get_loc(pd.Timestamp(b_))]/C[idx.get_loc(pd.Timestamp(a_))]-1),1)) for a_,b_ in cyc]
# 2022 cycle low inside
i0,i1=idx.get_loc(pd.Timestamp(HIKES[21])),idx.get_loc(pd.Timestamp(HIKES[31]))
lo=i0+int(np.argmin(C[i0:i1+1])); out["c22_low"]=(str(idx[lo].date()),round(100*(C[lo]/C[i0]-1),1))
ye=pd.DataFrame({"B":pd.Series(bh,idx).resample("YE").last(),"S":pd.Series(eq,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
# independent check: position array (in market unless within the out windows), returns-based
pos=np.ones(N,bool)
for a_,b_,_ in log: pos[idx.get_loc(pd.Timestamp(a_)):idx.get_loc(pd.Timestamp(b_))]=False
v=10000*(1-FEE); held=True; v*=C[0]/O[0]
for i in range(1,N):
    if pos[i] and held: v*=C[i]/C[i-1]
    elif (not pos[i]) and held: v*=O[i]/C[i-1]*(1-FEE); held=False
    elif pos[i] and not held: v*=(1-FEE)*C[i]/O[i]; held=True
out["check_v"]=round(v)
json.dump(out,open("results16.json","w"),indent=1,default=float)
pd.DataFrame({"B":bh,"S":eq,"inm":inm.astype(int),"C":C},index=idx).to_csv("sim16.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},default=float,indent=0)); print(ye.T.to_string())
