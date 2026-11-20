import pandas as pd, numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']
# use nominal close for "off the record" (index-like, no dividends) -- like the news
N=d.Close; rec=N.cummax(); dd=N/rec-1
# episodes record->new record
eps=[]; i=0; n=len(d); inep=False
cur=None
for k in range(n):
    if dd.iloc[k]==0:
        if cur: eps.append(cur); cur=None
        continue
    if cur is None: cur=dict(start=k,hit8=None,hit10=None,low=dd.iloc[k],lowk=k)
    if dd.iloc[k]<cur['low']: cur['low']=dd.iloc[k]; cur['lowk']=k
    if cur['hit8'] is None and dd.iloc[k]<=-0.08: cur['hit8']=k
    if cur['hit10'] is None and dd.iloc[k]<=-0.10: cur['hit10']=k
if cur: eps.append(cur)
for e in eps:
    if e['hit8'] is None: continue
    s=d.index[e['hit8']].date(); t=d.index[e['hit10']].date() if e['hit10'] else None
    print(s, t, round(e['low']*100,1), d.index[e['lowk']].date())
