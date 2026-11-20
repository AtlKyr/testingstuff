import pandas as pd, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']
s=pd.read_csv('sim34.csv',parse_dates=['Date']).set_index('Date'); K=s.cash
has=K>0; blk=(has!=has.shift()).cumsum()
out=[]
for _,g in K[has].groupby(blk[has]):
    a=g.index[0]; b=g.index[-1]; i=d.index.get_loc(b)+1
    if i>=len(d): out.append((str(a.date()),'END',len(g),float(g.max()),None)); continue
    fill=d.index[i]; out.append((str(a.date()),str(fill.date()),len(g),float(g.max()),float(O.loc[fill]/O.loc[a]-1)))
big=[o for o in out if o[3]>=3000]
for o in big: print(o)
print('all waits',len(out),'higher',sum(1 for o in out if o[4] and o[4]>0),'of',sum(1 for o in out if o[4] is not None))
print('big higher',sum(1 for o in big if o[4] and o[4]>0),len(big))
