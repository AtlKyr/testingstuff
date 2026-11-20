# #34 "Dry powder": A = $500 every month at the first trading day's open. B = saves $500/month in cash (0%) and invests the WHOLE pile
# at the next open after any close >= TH below the S&P's (SPY nominal close) record. Fee 0.05% per buy. Leftover cash counted at face value.
import pandas as pd, numpy as np, json, sys
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']; N=d.Close
dd=N/N.cummax()-1
first=d.index.to_series().groupby([d.index.year,d.index.month]).first().values
isfirst=pd.Series(d.index.isin(first),d.index)
FEE=0.0005; AMT=500
def run(th=0.08,fee=FEE):
    shA=shB=0.0; cashB=0.0; put=0.0; eqA=[];eqB=[];putl=[];cashl=[];buys=[];pend=False
    for i in range(len(d)):
        if isfirst.iloc[i]:
            put+=AMT; shA+=AMT*(1-fee)/O.iloc[i]; cashB+=AMT
            if i>0 and dd.iloc[i-1]<=-th: pend=True
        if pend and cashB>0:
            shB+=cashB*(1-fee)/O.iloc[i]; buys.append((str(d.index[i].date()),round(cashB),float(dd.iloc[i-1]))); cashB=0
        pend=False
        eqA.append(shA*C.iloc[i]); eqB.append(shB*C.iloc[i]+cashB); putl.append(put); cashl.append(cashB)
        if dd.iloc[i]<=-th and cashB>0: pend=True
    return pd.Series(eqA,d.index),pd.Series(eqB,d.index),pd.Series(putl,d.index),pd.Series(cashl,d.index),buys
A,B,P,K,buys=run()
R=dict(A=float(A.iloc[-1]),B=float(B.iloc[-1]),put=float(P.iloc[-1]),cash_end=float(K.iloc[-1]),nbuys=len(buys))
R['scan']={str(t):round(float(run(t)[1].iloc[-1])) for t in [0.03,0.05,0.08,0.10,0.15,0.20]}
R['fee0']=[round(float(x.iloc[-1])) for x in run(0.08,0)[:2]]
R['maxcash']=float(K.max()); R['maxcash_date']=str(K.idxmax().date())
lead=B-A; R['B_lead_max']=float(lead.max()); R['B_lead_max_date']=str(lead.idxmax().date()); R['A_lead_max']=float(-lead.min()); R['A_lead_max_date']=str(lead.idxmin().date())
for y in range(2005,2025): R[f'y{y}']=(round(A[str(y)].iloc[-1]),round(B[str(y)].iloc[-1]),round(K[str(y)].iloc[-1]))
# cash streaks for B (days with cash > 0 continuously)
has=K>0; blk=(has!=has.shift()).cumsum(); R['waits']=sorted([(str(g.index[0].date()),str(g.index[-1].date()),len(g),round(float(g.max()))) for _,g in K[has].groupby(blk[has])],key=lambda x:-x[2])[:6]
R['buys']=buys
R['days_off8']=int((dd<=-0.08).sum()); R['pct_days_off8']=float((dd<=-0.08).mean())
json.dump(R,open('results34.json','w'),indent=1,default=str)
pd.DataFrame({'A':A,'B':B,'put':P,'cash':K,'dd':dd}).to_csv('sim34.csv')
for k,v in R.items():
    if k!='buys': print(k,v)
print(len(buys)); print(buys[:5], buys[-8:])
