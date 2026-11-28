import pandas as pd,numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d)
per=idx.to_period('W-FRI'); last=np.r_[per[1:]!=per[:-1],True]   # last trading day of week
wclose_i=np.where(last)[0]
def run(dn=-0.05,up=0.05,cost=0.0005):
    cash=10000.;sh=0;inp=False;eq=np.zeros(N);pend=None;tr=[];prevw=None
    for i in range(N):
        if pend is not None:
            if pend=='sell' and inp: cash=sh*O[i]*(1-cost);sh=0;inp=False;tr.append(['S',i,O[i]])
            if pend=='buy' and not inp: sh=cash*(1-cost)/O[i];cash=0;inp=True;tr.append(['B',i,O[i]])
            pend=None
        if i==0: sh=cash*(1-cost)/O[0];cash=0;inp=True
        eq[i]=sh*C[i] if inp else cash
        if last[i]:
            if prevw is not None:
                r=C[i]/C[prevw]-1
                if inp and r<=dn: pend='sell'
                elif (not inp) and r>=up: pend='buy'
            prevw=i
    return eq,tr
bh=10000*(1-0.0005)/O[0]*C
print('bh',round(bh[-1]))
for dn,up in [(-0.05,0.05),(-0.04,0.04),(-0.06,0.06),(-0.05,0.04),(-0.04,0.05),(-0.03,0.03),(-0.07,0.07)]:
    eq,tr=run(dn,up); print(dn,up,round(eq[-1]),len([t for t in tr if t[0]=='S']))
eq,tr=run()
ath=np.maximum.accumulate(eq)
print('mdd',round((eq/ath-1).min()*100,1),'bh mdd',round((bh/np.maximum.accumulate(bh)-1).min()*100,1))
for a,b in zip(tr[0::2],tr[1::2]):
    print(idx[a[1]].date(),round(a[2],2),'->',idx[b[1]].date(),round(b[2],2),'chg',round((b[2]/a[2]-1)*100,1), 'days',b[1]-a[1])
if len(tr)%2: print('open',tr[-1][0],idx[tr[-1][1]].date())
