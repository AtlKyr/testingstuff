# Autopsy #22 - "Lock in profits after a big up week?" Weekly bars = last trading day of each calendar week (W-FRI).
# Rule: if the week's close is >= +TH% above the previous week's close -> sell at next open (take profits),
# sit in cash HOLD trading days, then buy back at the next open (a new big week while in cash restarts nothing - we're already out).
# 0.05%/side, cash 0%, $10K. B&H same dates (from first week's following open).
import pandas as pd, numpy as np, json, sys
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C)
FEE=0.0005
wk=pd.Series(C,idx).groupby(idx.to_period("W-FRI")).apply(lambda s:(s.index[-1],s.iloc[-1]))
wend=[w[0] for w in wk.values]; wc=np.array([w[1] for w in wk.values])
pos={d:i for i,d in enumerate(idx)}
wret=wc[1:]/wc[:-1]-1; wend_i=np.array([pos[d] for d in wend[1:]])
def signals(th):
    s=np.zeros(N,bool); s[wend_i[wret>=th]]=True; return s
S=pos[wend[1]]+1  # first day a signal could act
def run(th,hold,fee=FEE):
    big=signals(th); cash=10000.0; sh=10000*(1-fee)/O[S]; cash=0.0; eq=np.full(N,np.nan); INA=np.full(N,np.nan); out_until=-1; sells=[]; inm=0
    buyback=None
    for i in range(S,N):
        if i>S and sh>0 and big[i-1]:
            cash=sh*O[i]*(1-fee); sh=0.0; buyback=i+hold; sells.append(i)
        elif sh==0 and buyback is not None and i>=buyback:
            sh=cash*(1-fee)/O[i]; cash=0.0; buyback=None
        eq[i]=cash+sh*C[i]; inm+=sh>0; INA[i]=1.0 if sh>0 else 0.0
    global LASTIN; LASTIN=INA
    return eq,sells,inm/(N-S)
TH=0.025; HOLD=21
eq,sells,tim=run(TH,HOLD); INV=LASTIN.copy()
bh=np.full(N,np.nan); bh[S:]=10000*(1-FEE)/O[S]*C[S:]
def dd(x): x=x[~np.isnan(x)]; return float((x/np.maximum.accumulate(x)-1).min())
yrs=(idx[-1]-idx[S]).days/365.25
# what came after the big weeks: SPY next-21-day return from next open (what the seller missed)
miss=[]
for i in sells:
    j=min(i+HOLD,N-1); miss.append(O[j]/O[i]-1)
miss=np.array(miss)
# baseline: any day next-21-day open-to-open
allr=O[S+HOLD:]/O[S:-HOLD]-1
out=dict(start=str(idx[S].date()),final=round(float(eq[-1])),bh=round(float(bh[-1])),cagr=round(100*((eq[-1]/1e4)**(1/yrs)-1),2),
 bh_cagr=round(100*((bh[-1]/1e4)**(1/yrs)-1),2),mdd=round(100*dd(eq),1),bh_mdd=round(100*dd(bh),1),time_in=round(100*tim,1),
 sells=len(sells),missed_up=int((miss>0).sum()),miss_avg=round(100*miss.mean(),2),base_avg=round(100*allr.mean(),2),base_up=round(100*(allr>0).mean(),1),
 fee0=round(float(run(TH,HOLD,0)[0][-1])),fee10=round(float(run(TH,HOLD,0.001)[0][-1])),fee20=round(float(run(TH,HOLD,0.002)[0][-1])))
out["scan_hold"]={h:round(float(run(TH,h)[0][-1])) for h in (5,10,21,42,63,126)}
out["scan_th"]={str(t):round(float(run(t,HOLD)[0][-1])) for t in (0.02,0.025,0.03,0.04,0.05)}
out["n_bigweeks"]=int((wret>=TH).sum()); out["n_weeks"]=len(wret)
out["bigweeks_by_year"]=pd.Series([idx[i].year for i in wend_i[wret>=TH]]).value_counts().sort_index().to_dict()
ye=pd.DataFrame({"R":pd.Series(eq,idx).resample("YE").last(),"B":pd.Series(bh,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):[int(v.R),int(v.B)] for k,v in ye.iterrows()}
out["sell_dates"]=[str(idx[i].date()) for i in sells]
out["miss_list"]=[round(100*m,1) for m in miss]
json.dump(out,open("results22.json","w"),indent=1,default=float)
pd.DataFrame({"R":eq,"B":bh,"IN":INV,"O":O,"C":C},index=idx).to_csv("sim22.csv")
print(json.dumps({k:v for k,v in out.items() if k not in("year_end","sell_dates","miss_list")},default=float)); print(out["year_end"])
