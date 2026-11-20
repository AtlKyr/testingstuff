# #35 The 1% fee: $10,000 buy & hold SPY from the first open (0.05% buy cost), vs the same portfolio charged 1%/year
# (1/12 of 1% of the value at each month's last close). Also 0.5%, 1.5%, 2%. Fees paid in $ and "lost growth".
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']
last=d.index.to_series().groupby([d.index.year,d.index.month]).last().values
islast=pd.Series(d.index.isin(last),d.index)
def run(fee=0.01):
    sh=10000*(1-0.0005)/O.iloc[0]; eq=[]; paid=0; paidl=[]; nb=0; yp={}
    for i in range(len(d)):
        v=sh*C.iloc[i]
        if islast.iloc[i] and fee>0:
            x=v*fee/12; paid+=x; sh-=x/C.iloc[i]; nb+=1; y=d.index[i].year; yp[y]=yp.get(y,0)+x
        eq.append(sh*C.iloc[i]); paidl.append(paid)
    return pd.Series(eq,d.index),pd.Series(paidl,d.index),nb,yp
bh,_,_,_=run(0); fe,paid,nb,yp=run(0.01)
R=dict(bh=float(bh.iloc[-1]),fee=float(fe.iloc[-1]),gap=float(bh.iloc[-1]-fe.iloc[-1]),paid=float(paid.iloc[-1]),nbills=nb,
 gap_pct=float(1-fe.iloc[-1]/bh.iloc[-1]),gain_bh=float(bh.iloc[-1]-10000),gain_fee=float(fe.iloc[-1]-10000))
R['share_of_gain_lost']=R['gap']/R['gain_bh']
R['scan']={str(x):round(float(run(x)[0].iloc[-1])) for x in [0.0025,0.005,0.01,0.015,0.02]}
R['yearly_paid']={y:round(v) for y,v in yp.items()}
R['paid2008']=round(yp[2008]); R['ret2008']=float(C['2008'].iloc[-1]/C['2007'].iloc[-1]-1)
for y in range(2005,2025): R[f'y{y}']=(round(bh[str(y)].iloc[-1]),round(fe[str(y)].iloc[-1]),round(paid[str(y)].iloc[-1]))
# when did the gap first exceed $10,000 (the whole starting stake)?
g=bh-fe; R['gap_gt_10k']=str(g[g>=10000].index[0].date()) if (g>=10000).any() else None
R['gap_gt_5k']=str(g[g>=5000].index[0].date())
json.dump(R,open('results35.json','w'),indent=1,default=str)
pd.DataFrame({'bh':bh,'fee':fe,'paid':paid}).to_csv('sim35.csv')
for k,v in R.items(): print(k,v)
