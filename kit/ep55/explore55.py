import pandas as pd,numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d)
# weekly closes: last trading day of each W-FRI week
wk=pd.Series(np.arange(N),index=idx).groupby(idx.to_period('W-FRI')).last()
wi=wk.values; wr=C[wi[1:]]/C[wi[:-1]]-1
print('weeks',len(wr))
for th in (0.04,0.05,0.06):
    up=[(idx[wi[k+1]].date(),round(wr[k]*100,2)) for k in range(len(wr)) if wr[k]>=th]
    dn=[(idx[wi[k+1]].date(),round(wr[k]*100,2)) for k in range(len(wr)) if wr[k]<=-th]
    print(th,len(up),len(dn))
up=[k for k in range(len(wr)) if wr[k]>=0.05]
ath=np.maximum.accumulate(C)
for k in up:
    i=wi[k+1]
    nxt=min(i+63,N-1); lowlater=C[i+1:i+64].min() if i+1<N else np.nan
    prelow=C[max(0,i-63):i+1].min()
    print(idx[i].date(), round(wr[k]*100,1),'dd',round((C[i]/ath[i]-1)*100,1),'3m', round((C[nxt]/O[min(i+1,N-1)]-1)*100,1),'1y',round((C[min(i+252,N-1)]/O[min(i+1,N-1)]-1)*100,1),'lowerlow',lowlater<prelow)
