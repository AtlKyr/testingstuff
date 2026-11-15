import pandas as pd, numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
C=d['Adj Close']; ret=C.pct_change().fillna(0)
ym=d.index.to_period('M')
pos=pd.Series(0,index=d.index)  # day index within month
g=pd.Series(range(len(d)),index=d.index).groupby(ym)
first=g.rank(method='first').astype(int); last=g.rank(method='first',ascending=False).astype(int)
FEE=0.0005
def run(nlast=1,nfirst=3,fee=FEE):
    # hold returns of last nlast days of month and first nfirst days: buy at close of the day before window
    inwin=((last<=nlast)|(first<=nfirst)).values
    eq=10000.; out=[]; held=False; n=0; days=0
    for i in range(len(d)):
        if held: eq*=1+ret.iloc[i]; days+=1
        # decide at close i whether to hold day i+1
        nxt= inwin[i+1] if i+1<len(d) else False
        if nxt and not held: eq*=1-fee; held=True; n+=1
        elif (not nxt) and held: eq*=1-fee; held=False
        out.append(eq)
    return pd.Series(out,d.index),n,days/len(d)
eq,n,tim=run()
bh=10000*(1-FEE)*C/C.iloc[0]*(1-FEE)
yrs=(d.index[-1]-d.index[0]).days/365.25
print('TOM final',round(eq.iloc[-1]),'bh',round(bh.iloc[-1]),'trades',n,'time',tim)
dd=lambda s:(s/s.cummax()-1).min()
print('dd',dd(eq),dd(bh))
# other days only
inwin=((last<=1)|(first<=3))
print('sum logret window',np.log1p(ret[inwin]).sum(),'other',np.log1p(ret[~inwin]).sum())
print('avg day window',ret[inwin].mean()*100,'other',ret[~inwin].mean()*100)
oth=10000*np.exp(np.log1p(ret[~inwin]).sum()); print('other days only gross',round(oth))
for f in [0,0.001,0.002]: print('fee',f,round(run(fee=f)[0].iloc[-1]))
for a,b in [(1,3),(1,4),(2,3),(1,2),(4,4)]: print(a,b,round(run(a,b)[0].iloc[-1]))
ye=eq.resample('YE').last(); yb=bh.resample('YE').last(); print(pd.DataFrame({'s':ye.round(),'b':yb.round()}).T)
# share of years strategy annual return beats
print('worst day in window',ret[inwin].idxmin(),ret[inwin].min())
pd.DataFrame({'eq':eq,'bh':bh,'IN':inwin.astype(int),'C':C}).to_csv('sim25.csv')
