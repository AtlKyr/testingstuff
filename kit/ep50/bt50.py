# #50 Black Friday: $1,000 into SPY at the open of every Black Friday 2005-2024 (0.05% cost), held to 2024-12-31.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=d.Open*r; C=d['Adj Close']; D=d.index; RC=d.Close
bfs=[]
for y in range(2005,2025):
    nov=pd.date_range(f'{y}-11-01',f'{y}-11-30'); th=[x for x in nov if x.weekday()==3][3]; bf=th+pd.Timedelta(days=1)
    assert bf in D; bfs.append(bf)
sh=pd.Series(0.0,index=D); put=pd.Series(0.0,index=D); rows=[]
for bf in bfs:
    s=1000*(1-0.0005)/O[bf]; sh[bf:]+=s; put[bf:]+=1000
    i=D.get_loc(bf); day=C.iloc[i]/C.iloc[i-1]-1
    pk=RC[:bf].max(); dd=RC[bf]/pk-1
    rows.append(dict(bf=str(bf.date()), day=round(day,5), shares=s, worth=round(s*C.iloc[-1],2), dd=round(dd,4)))
worth=sh*C
res=dict(final=round(worth.iloc[-1],2), put=20000, mult=round(worth.iloc[-1]/20000,4), up_days=sum(r_['day']>0 for r_ in rows), rows=rows)
best=max(rows,key=lambda x:x['worth']); res['best']=best
print(res['final'],res['mult'],res['up_days'],best)
for x in rows: print(x['bf'],x['day'],x['worth'],x['dd'])
# worth vs put at key points
for dt in ['2008-11-28','2009-03-09','2011-10-03','2016-02-11','2020-02-19','2020-03-23','2022-10-12','2024-12-31']:
    i=D.searchsorted(pd.Timestamp(dt)); print(dt,round(put.iloc[i]),round(worth.iloc[i]),round(worth.iloc[i]/put.iloc[i],3))
# first date worth >= 2x put (after 2008)
m=(worth>=2*put)&(put>0); print('first 2x',D[m.values.argmax()].date(), 'put then',put[m].iloc[0])
dd20=(worth['2020-02-19':'2020-03-23'].min()/worth['2020-02-19':'2020-03-23'].max()-1); print('2020 drop',round(dd20,3))
# twin: same $1,000 every Cyber Monday / Jan
res['dd2008']=rows[3]['dd']
json.dump(res,open('results50.json','w'),indent=1,default=float)
pd.DataFrame({'Date':D,'worth':worth.values,'put':put.values}).to_csv('sim50.csv',index=False)
