import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=(d['Open']*r).values; C=d['Adj Close'].values; Hh=(d['High']*r); Ll=(d['Low']*r)
dates=d.index; N=len(d); FEE=0.0005
def stoch(k=14, sm=3):
    hh=Hh.rolling(k).max(); ll=Ll.rolling(k).min()
    fk=100*(d['Adj Close']-ll)/(hh-ll)
    slowk=fk.rolling(sm).mean()  # slow %K
    return slowk.values.copy()
def run(lo=20, hi=80, k=14, fee=FEE, warm=60, mode='cross'):
    K=stoch(k); K[:warm]=np.nan
    cash=10000.0; sh=0; eq=np.zeros(N); inm=np.zeros(N,bool); trades=[]; pend=None
    for t in range(N):
        if pend=='buy' and sh==0:
            sh=cash*(1-fee)/O[t]; cash=0; trades.append([str(dates[t].date()),None,O[t],None])
        elif pend=='sell' and sh>0:
            cash=sh*O[t]*(1-fee); sh=0; trades[-1][1]=str(dates[t].date()); trades[-1][3]=O[t]
        pend=None
        if t>0 and not np.isnan(K[t]) and not np.isnan(K[t-1]):
            if sh==0 and K[t-1]<lo<=K[t]: pend='buy'
            if sh>0 and K[t-1]>hi>=K[t]: pend='sell'
        eq[t]=sh*C[t]+cash; inm[t]=sh>0
    return eq,trades,inm,K
w0=60
bh=10000*(1-FEE)/O[w0]*C; bh[:w0]=10000
if __name__=='__main__':
    eq,tr,inm,K=run()
    done=[x for x in tr if x[1]]
    rets=[x[3]/x[2]*(1-FEE)**2-1 for x in done]
    print('final',round(eq[-1]),'bh from w0',round(bh[-1]),'trades',len(tr),'wins',sum(r>0 for r in rets),'inm',inm[w0:].mean())
    print('avg win',np.mean([r for r in rets if r>0]),'avg loss',np.mean([r for r in rets if r<=0]),'worst',min(rets), done[int(np.argmin(rets))])
    hold=[ (pd.Timestamp(x[1])-pd.Timestamp(x[0])).days for x in done]; print('avg hold days',np.mean(hold))
    for lo,hi in [(20,80),(30,70),(10,90),(20,50)]:
        print(lo,hi,round(run(lo,hi)[0][-1]))
    for k in [5,9,21]: print('k',k,round(run(k=k)[0][-1]))
    dd=lambda e:(e/np.maximum.accumulate(e)-1)[w0:].min(); print('dd',dd(eq),dd(bh))
    # yearly lead
    for y in range(2005,2025):
        i=np.where(dates.year==y)[0][-1]; print(y, round(eq[i]), round(bh[i]), round(inm[np.where(dates.year==y)[0]].mean(),2))
    # time below 20 signals count
