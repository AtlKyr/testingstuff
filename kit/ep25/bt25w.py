import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
A=d['Adj Close']; Cn=d['Close']; FEE=0.0005; AMT=1000
res={}
rows=[]
for y,g in d.groupby(d.index.year):
    hi=g['Close'].idxmax(); lo=g['Close'].idxmin(); fi=g.index[0]
    rows.append((y,hi.date(),lo.date(),fi.date()))
def strat(pick):
    sh=0; hist=[]
    for y,g in d.groupby(d.index.year):
        day=pick(g); sh+=AMT*(1-FEE)/A.loc[day]
    return sh*A.iloc[-1]
worst=strat(lambda g:g['Close'].idxmax()); best=strat(lambda g:g['Close'].idxmin()); first=strat(lambda g:g.index[0])
print('worst',round(worst),'best',round(best),'jan1',round(first),'put in',AMT*20)
# equity paths for race
def path(pick):
    days={pick(g) for y,g in d.groupby(d.index.year)}
    sh=0;inv=0;eq=[];pi=[]
    for t in d.index:
        if t in days: sh+=AMT*(1-FEE)/A.loc[t]; inv+=AMT
        eq.append(sh*A.loc[t]); pi.append(inv)
    return pd.Series(eq,d.index),pd.Series(pi,d.index)
w,pi=path(lambda g:g['Close'].idxmax()); b,_=path(lambda g:g['Close'].idxmin()); f,_=path(lambda g:g.index[0])
pd.DataFrame({'worst':w,'best':b,'first':f,'putin':pi,'C':A}).to_csv('sim25w.csv')
print('gap best-worst',best-worst,(best/worst-1))
for r in rows: print(r)
# worst timer worst purchases
print(w.resample('YE').last().round(), pi.resample('YE').last())
# cash alternative: never invest
print('worst/putin',worst/20000)
# worst single purchase: 2007-10-09 high -> value
print('worst entry underwater min', (w/pi-1).min(), (w/pi-1).idxmin())
