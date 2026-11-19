# #33 Be greedy when others are fearful: VIX close >=30 -> buy SPY next open, hold until 252 trading days pass with no new VIX>=30 close, sell next open. Cash 0%.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']
v=pd.read_csv('../ep24/vix.csv',parse_dates=['observation_date']).set_index('observation_date')['VIXCLS']
v=pd.to_numeric(v,errors='coerce').reindex(d.index).ffill()
FEE=0.0005; TH=30; H=252
def run(th=TH,H=H,fee=FEE):
    sh=0; cash=10000.0; eq=[];inm=[];tr=[];pb=False;ps=False;left=0
    for i in range(len(d)):
        if pb and sh==0: sh=cash*(1-fee)/O.iloc[i]; cash=0; bd=d.index[i]; bp=O.iloc[i]; pb=False; left=H
        elif ps and sh>0: cash=sh*O.iloc[i]*(1-fee); tr.append((str(bd.date()),str(d.index[i].date()),O.iloc[i]/bp-1)); sh=0; ps=False
        eq.append(sh*C.iloc[i]+cash); inm.append(sh>0)
        if i==len(d)-1: continue
        if sh>0:
            left = H if v.iloc[i]>=th else left-1
            if left<=0: ps=True
        elif v.iloc[i]>=th: pb=True
    return pd.Series(eq,d.index),pd.Series(inm,d.index),tr
eq,inm,tr=run()
bh=10000*(1-FEE)*C/O.iloc[0]
def mdd(s): return float((s/s.cummax()-1).min())
yrs=(d.index[-1]-d.index[0]).days/365.25
R=dict(final=float(eq.iloc[-1]),bh=float(bh.iloc[-1]),cagr=(eq.iloc[-1]/1e4)**(1/yrs)-1,bh_cagr=(bh.iloc[-1]/1e4)**(1/yrs)-1,
 mdd=mdd(eq),bh_mdd=mdd(bh),tim=float(inm.mean()),trades=len(tr),wins=sum(1 for t in tr if t[2]>0),
 fear_days=int((v>=30).sum()),first_fear=str(v[v>=30].index[0].date()),first_buy_open=None)
R['scan']={f"{t}/{h}":round(float(run(t,h)[0].iloc[-1])) for t in [25,30,40] for h in [63,126,252,504]}
R['fees']={str(fe):round(float(run(TH,H,fe)[0].iloc[-1])) for fe in [0,0.001,0.002]}
lead=(eq-bh); R['max_lead']=float(lead.max())
for y in range(2005,2025): R[f'y{y}']=(round(eq[str(y)].iloc[-1]),round(bh[str(y)].iloc[-1]))
# cash days from start to first buy
fb=inm[inm].index[0]; R['first_in']=str(fb.date()); R['wait_days']=int(d.index.get_loc(fb)); R['first_buy_px_vs_low']=float(O.loc[fb]/C.loc['2009-03-09']-1)
# what buy&hold did while it waited (2005-01-03 -> first buy)
R['bh_while_wait']=float(C.loc[fb]/O.iloc[0]-1)
# cash stretches
blocks=(inm!=inm.shift()).cumsum(); out=[(g.index[0].date(),g.index[-1].date(),len(g)) for _,g in inm[~inm].groupby(blocks[~inm])]
R['cash_blocks']=[(str(a),str(b),n) for a,b,n in out]
R['bh_in_cash']=[float(C.loc[str(b)]/C.loc[str(a)]-1) for a,b,n in out]
R['trades_list']=tr
json.dump(R,open('results33.json','w'),indent=1,default=str)
pd.DataFrame({'eq':eq,'bh':bh,'inm':inm,'vix':v}).to_csv('sim33.csv')
for k,v_ in R.items(): print(k,v_)
