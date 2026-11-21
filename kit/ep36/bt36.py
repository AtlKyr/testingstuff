# #36 Correction rule: SPY nominal close <= -10% below its all-time closing high (first close of that drawdown episode)
# -> sell at next open. Buy back at next open after: first close <= -20% below the record (bear market), OR a new record close
# (whichever first). Episode ends at a new record. 0.05%/side, cash 0%. vs buy & hold from first open.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; N=d.Close.values; idx=d.index
def run(sell_th=0.10, buy_th=0.20, cost=0.0005):
    cash=0; sh=10000*(1-cost)/O[0]; inm=True; rec=N[0]; armed=True; pend=None; trades=[]; eq=[]; INN=[]
    for i in range(len(d)):
        if pend is not None:
            if pend[0]=='S': cash=sh*O[i]*(1-cost); sh=0; inm=False; trades.append(dict(sell_sig=str(idx[pend[1]].date()),sell=str(idx[i].date()),sp=O[i],sn=d.Open.values[i]))
            else: sh=cash*(1-cost)/O[i]; cash=0; inm=True; trades[-1].update(buy_sig=str(idx[pend[1]].date()),buy=str(idx[i].date()),bp=O[i],bn=d.Open.values[i],why=pend[2])
            pend=None
        newrec = N[i]>rec
        if newrec: rec=N[i]
        dd=N[i]/rec-1
        if newrec: armed=True
        if inm and armed and dd<=-sell_th and i<len(d)-1: pend=('S',i); armed=False
        elif (not inm) and i<len(d)-1 and (dd<=-buy_th or newrec): pend=('B',i,'bear' if dd<=-buy_th else 'record')
        eq.append(sh*C[i]+cash); INN.append(inm)
    return pd.Series(eq,idx), trades, INN
bh,_,_=run(sell_th=9)  # never sells
st,tr,INN=run()
for t in tr:
    if 'bp' in t: t['ratio']=t['bp']/t['sp']; t['ratio_raw']=t['bn']/t['sn']
R=dict(bh=float(bh.iloc[-1]),st=float(st.iloc[-1]),ntr=len(tr),tim=float(np.mean(INN)))
def mdd(s): return float((s/s.cummax()-1).min())
R.update(mdd_bh=mdd(bh),mdd_st=mdd(st))
yrs=(idx[-1]-idx[0]).days/365.25; R['cagr_bh']=(R['bh']/1e4)**(1/yrs)-1; R['cagr_st']=(R['st']/1e4)**(1/yrs)-1
R['trades']=tr
R['wins']=sum(1 for t in tr if t.get('ratio',9)<1)
R['scan']={f"{a}/{b}":round(float(run(a,b)[0].iloc[-1])) for a in [0.08,0.10,0.12,0.15] for b in [0.15,0.20,0.25,0.30] if b>a}
R['fee_stress']={str(c):round(float(run(cost=c)[0].iloc[-1])) for c in [0.001,0.002]}
# max drawdown per record episode (nominal)
rec=pd.Series(N,idx).cummax(); ddn=pd.Series(N,idx)/rec-1
eps=[]; cur=None
for i in range(len(d)):
    if ddn.iloc[i]==0:
        if cur and cur['min']<=-0.10: eps.append(cur)
        cur={'start':str(idx[i].date()),'min':0}
    else:
        if ddn.iloc[i]<cur['min']: cur['min']=float(ddn.iloc[i]); cur['low']=str(idx[i].date())
if cur and cur['min']<=-0.10: eps.append(cur)
R['episodes']=eps
for y in range(2005,2025): R[f'y{y}']=(round(st[str(y)].iloc[-1]),round(bh[str(y)].iloc[-1]))
json.dump(R,open('results36.json','w'),indent=1,default=str)
pd.DataFrame({'bh':bh,'st':st,'IN':INN,'N':N,'dd':ddn.values}).to_csv('sim36.csv')
for k,v in R.items():
    if k=='trades':
        for t in v: print(t)
    else: print(k,v)
