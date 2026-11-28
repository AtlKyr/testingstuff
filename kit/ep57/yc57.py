import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d); RO=d.Open.values
y=pd.read_csv('t10y2y.csv',parse_dates=[0],index_col=0).iloc[:,0]; y=pd.to_numeric(y,errors='coerce').dropna()
# value known at the close of day i = FRED value of the previous business day (1-day publication lag)
sp=y.shift(1).reindex(idx.union(y.index)).ffill().reindex(idx).values
def run(confirm=1,cost=0.0005):
    cash=1e4;sh=0;inp=False;eq=np.zeros(N);IN=np.zeros(N,bool);pend=None;tr=[]
    neg=0;pos=0
    for i in range(N):
        if pend=='S' and inp: cash=sh*O[i]*(1-cost);sh=0;inp=False;tr.append(['S',i])
        elif pend=='B' and not inp: sh=cash*(1-cost)/O[i];cash=0;inp=True;tr.append(['B',i])
        pend=None
        if i==0: sh=cash*(1-cost)/O[0];cash=0;inp=True
        eq[i]=sh*C[i] if inp else cash; IN[i]=inp
        neg=neg+1 if sp[i]<0 else 0; pos=pos+1 if sp[i]>0 else 0
        if inp and neg>=confirm: pend='S'
        elif (not inp) and pos>=confirm: pend='B'
    return eq,IN,tr
bh=1e4*(1-0.0005)/O[0]*C
for cf in (1,5,10,21,63):
    eq,IN,tr=run(cf); print(cf, round(eq[-1]), len([t for t in tr if t[0]=='S']), 'tim',round(IN.mean()*100), 'mdd', round(((eq/np.maximum.accumulate(eq))-1).min()*100,1))
eq,IN,tr=run(1)
for t in tr: print(t[0], idx[t[1]].date(), round(RO[t[1]],2))
