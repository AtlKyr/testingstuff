# #27 "Only buy red days": $500 arrives each month (1st trading day). Normal buyer: buys at that day's open.
# Red-day buyer: waits for a red day (close <= TH vs prior close) and buys at THAT close; cash rolls over. Fee 0.05%.
import pandas as pd, numpy as np, json, sys
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']; r=C.pct_change()
FEE=0.0005; AMT=500
first=d.index.to_series().groupby([d.index.year,d.index.month]).first().values
isfirst=pd.Series(d.index.isin(first),d.index)
def run(th):
    shA=shB=0; cashB=0; put=0; eqA=[];eqB=[];cb=[]; buys=0; waits=[]; pending_since=None
    for i,dt in enumerate(d.index):
        if isfirst.iloc[i]:
            shA+=AMT*(1-FEE)/O.iloc[i]; cashB+=AMT; put+=AMT
            if pending_since is None: pending_since=i
        if cashB>0 and i>0 and r.iloc[i]<=th:
            shB+=cashB*(1-FEE)/C.iloc[i]; cashB=0; buys+=1; waits.append(i-pending_since); pending_since=None
        eqA.append(shA*C.iloc[i]); eqB.append(shB*C.iloc[i]+cashB); cb.append(cashB)
    return pd.Series(eqA,d.index),pd.Series(eqB,d.index),put,buys,waits,pd.Series(cb,d.index)
TH=float(sys.argv[1]) if len(sys.argv)>1 else -0.01
A,B,put,buys,waits,cb=run(TH)
R=dict(th=TH,put=put,A=float(A.iloc[-1]),B=float(B.iloc[-1]),buys=buys,max_wait=int(max(waits)),avg_wait=float(np.mean(waits)),max_cash=float(cb.max()),max_cash_date=str(cb.idxmax().date()))
R['scan']={str(t):(float(run(t)[1].iloc[-1])) for t in [0.0,-0.005,-0.01,-0.015,-0.02]}
print(R)
if len(sys.argv)<=1 or sys.argv[-1]=='save':
    json.dump(R,open('results27.json','w'),indent=1)
    pd.DataFrame({'A':A,'B':B,'cash':cb}).to_csv('sim27.csv')
