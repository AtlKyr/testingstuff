# #28 After a -2% day: sell next open, stay out until N calm trading days (no new <=-2% close), buy back next open.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']
r=C.pct_change()
FEE=0.0005; TH=-0.02; CALM=10
def run(th=TH,calm=CALM,fee=FEE):
    sh=10000*(1-fee)/O.iloc[0]; cash=0; eq=[]; inm=[]; tr=[]; pend_sell=False; pend_buy=False; quiet=0
    for i in range(len(d)):
        if pend_sell and sh>0:
            cash=sh*O.iloc[i]*(1-fee); sold=O.iloc[i]; sd=d.index[i]; sh=0; pend_sell=False; quiet=0
        elif pend_buy and sh==0:
            sh=cash*(1-fee)/O.iloc[i]; cash=0; tr.append((str(sd.date()),str(d.index[i].date()),O.iloc[i]/sold-1)); pend_buy=False
        eq.append(sh*C.iloc[i]+cash); inm.append(sh>0)
        if i==0 or i==len(d)-1: continue
        big = r.iloc[i]<=th
        if sh>0 and big: pend_sell=True
        elif sh==0:
            quiet = 0 if big else quiet+1
            if quiet>=calm: pend_buy=True
    return pd.Series(eq,d.index),pd.Series(inm,d.index),tr
eq,inm,tr=run()
bh=10000*(1-FEE)*C/O.iloc[0]
def mdd(s): return float((s/s.cummax()-1).min())
yrs=(d.index[-1]-d.index[0]).days/365.25
bigdays=r[r<=TH]
R=dict(final=float(eq.iloc[-1]),bh=float(bh.iloc[-1]),cagr=(eq.iloc[-1]/1e4)**(1/yrs)-1,bh_cagr=(bh.iloc[-1]/1e4)**(1/yrs)-1,
 mdd=mdd(eq),bh_mdd=mdd(bh),tim=float(inm.mean()),trades=len(tr),higher=sum(1 for t in tr if t[2]>0),
 n_big=int(len(bigdays)))
# cluster stat: after a -2% day, another -2% within next 10 trading days?
idx=np.where(r.values<=TH)[0]
nxt=[ (r.iloc[i+1:i+11]<=TH).any() for i in idx if i+11<len(r)]
R['cluster10']=float(np.mean(nxt)); 
base=[(r.iloc[i+1:i+11]<=TH).any() for i in range(1,len(r)-11)]; R['base10']=float(np.mean(base))
# best days: how many of the +2% days fell while out
up=r[r>=0.02]; R['n_up2']=int(len(up)); R['up2_out']=int((~inm.reindex(up.index)).sum())
best10=r.nlargest(10); R['best10_out']=int((~inm.reindex(best10.index)).sum())
worst10=r.nsmallest(10); R['worst10_out']=int((~inm.reindex(worst10.index)).sum())
R['scan']={f"{t}/{c}":round(float(run(t,c)[0].iloc[-1])) for t in [-0.015,-0.02,-0.03] for c in [5,10,21,42]}
R['fees']={str(fe):round(float(run(TH,CALM,fe)[0].iloc[-1])) for fe in [0,0.001,0.002]}
R['per_year']=pd.Series([t[0][:4] for t in tr]).value_counts().sort_index().to_dict()
R['bigs_per_year']=pd.Series(bigdays.index.year).value_counts().sort_index().to_dict()
# lead over time
lead=(eq-bh); R['max_lead']=float(lead.max()); R['max_lead_date']=str(lead.idxmax().date())
R['lead_flip']=str(lead[lead>0].index[-1].date()) if (lead>0).any() else None
for y in [2008,2009,2010,2011,2012,2015,2018,2020,2022]:
    s=eq[str(y)].iloc[-1]; b=bh[str(y)].iloc[-1]; R[f'y{y}']=(round(s),round(b))
R['trades_list']=tr
json.dump(R,open('results28.json','w'),indent=1,default=str)
pd.DataFrame({'eq':eq,'bh':bh,'inm':inm,'r':r}).to_csv('sim28.csv')
for k,v in R.items():
    if k!='trades_list': print(k,v)
