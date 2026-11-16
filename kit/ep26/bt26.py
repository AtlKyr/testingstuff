# #26 Red morning: SPY opens >=1% below prior close -> sell at that open, buy back next open. vs buy & hold.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']
gap=O/C.shift(1)-1
TH=-0.01; FEE=0.0005
def run(th,fee=FEE):
    cash=0.0; sh=10000*(1-fee)/O.iloc[0]; eq=[]; out=[]; trades=[]
    idx=d.index
    for i in range(len(d)):
        if sh>0 and i>0 and gap.iloc[i]<=th and i<len(d)-1:
            cash=sh*O.iloc[i]*(1-fee); sold=O.iloc[i]; sh=0; si=i
        elif sh==0 and i>0:
            sh=cash*(1-fee)/O.iloc[i]; trades.append((idx[si],idx[i],O.iloc[i]/sold-1)); cash=0
            # if today also gap-down: we bought at open -> rule: sell at gap open; buying back at same open is a wash; treat: stay out if today gapped too
        eq.append(sh*C.iloc[i]+cash); out.append(sh==0)
    return pd.Series(eq,idx),pd.Series(out,idx),trades
def run2(th,fee=FEE):
    # clean version: out from open of gap day to open of next day where today's open isn't a gap-down
    sh=10000*(1-fee)/O.iloc[0]; cash=0; eq=[]; inm=[]; tr=[]
    for i in range(len(d)):
        g=gap.iloc[i] if i>0 else 0
        if sh>0 and g<=th and i<len(d)-1:
            cash=sh*O.iloc[i]*(1-fee); sold=O.iloc[i]; sd=d.index[i]; sh=0
        elif sh==0 and g>th:
            sh=cash*(1-fee)/O.iloc[i]; cash=0; tr.append((str(sd.date()),str(d.index[i].date()),O.iloc[i]/sold-1))
        eq.append(sh*C.iloc[i]+cash); inm.append(sh>0)
    return pd.Series(eq,d.index),pd.Series(inm,d.index),tr
eq,inm,tr=run2(TH)
bh=10000*(1-FEE)*C/O.iloc[0]
def mdd(s): return float((s/s.cummax()-1).min())
yrs=(d.index[-1]-d.index[0]).days/365.25
R=dict(final=float(eq.iloc[-1]),bh=float(bh.iloc[-1]),cagr=(eq.iloc[-1]/1e4)**(1/yrs)-1,bh_cagr=(bh.iloc[-1]/1e4)**(1/yrs)-1,
 mdd=mdd(eq),bh_mdd=mdd(bh),tim=float(inm.mean()),trades=len(tr),
 higher=sum(1 for t in tr if t[2]>0),win=sum(1 for t in tr if t[2]<0)/len(tr))
# scan
R['scan']={str(t):float(run2(t)[0].iloc[-1]) for t in [-0.005,-0.0075,-0.01,-0.015,-0.02,-0.03]}
R['fees']={str(fe):float(run2(TH,fe)[0].iloc[-1]) for fe in [0,0.001,0.002]}
tr_s=sorted(tr,key=lambda t:-t[2])
R['top']=tr_s[:5]; R['worst']=tr_s[-3:]
R['avg_next']=float(np.mean([t[2] for t in tr]))
o2o=(O.shift(-1)/O-1).dropna(); R['avg_any']=float(o2o.mean()); R['any_up']=float((o2o>0).mean())
R['bounce_sum']=float(np.prod([1+t[2] for t in tr]))
# by year count
R['per_year']=pd.Series([t[0][:4] for t in tr]).value_counts().sort_index().to_dict()
json.dump(R,open('results26.json','w'),indent=1,default=str)
pd.DataFrame({'eq':eq,'bh':bh,'inm':inm,'gap':gap}).to_csv('sim26.csv')
for k,v in R.items(): print(k,v)
