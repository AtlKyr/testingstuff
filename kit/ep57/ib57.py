import pandas as pd,numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; H=(d.High*f).values; L=(d.Low*f).values; idx=d.index; N=len(d)
ib=np.zeros(N,bool); ib[1:]=(H[1:]<H[:-1])&(L[1:]>L[:-1])
print('inside bars',ib.sum(), ib.mean())
def run(hold=None, stop=True, cost=0.0005, warm=20):
    cash=1e4; sh=0; inp=False; eq=np.zeros(N); pend=None; tr=[]; IN=np.zeros(N,bool)
    mh=ml=None; sl=None
    for i in range(N):
        if pend=='B' and not inp: sh=cash*(1-cost)/O[i]; cash=0; inp=True; ent=O[i]; ei=i; sl=pend_sl
        elif pend=='S' and inp: cash=sh*O[i]*(1-cost); sh=0; inp=False; tr.append((ei,i,O[i]/ent-1))
        pend=None
        eq[i]=sh*C[i] if inp else cash; IN[i]=inp
        if i<warm: continue
        # setup: bar i-1 is inside bar of mother bar i-2; signal: close i > mother high
        if not inp:
            if ib[i-1] and C[i]>H[i-2]: pend='B'; pend_sl=L[i-2]
        else:
            if (stop and C[i]<sl) or (hold and i-ei>=hold): pend='S'
    bh=1e4*(1-cost)/O[warm]*C
    t=np.array([x[2] for x in tr])
    return eq,bh,tr,IN
for hold in (5,10,20,None):
    for stop in (True,False):
        if hold is None and not stop: continue
        eq,bh,tr,IN=run(hold,stop); t=np.array([x[2] for x in tr])
        print(hold,stop,round(eq[-1]),round(bh[-1]),len(tr),round((t>0).mean()*100,1),'tim',round(IN.mean()*100),'mdd',round(((eq/np.maximum.accumulate(eq))-1).min()*100,1))
