import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=(d['Open']*r).values; C=d['Adj Close'].values; Hh=(d['High']*r); Ll=(d['Low']*r); Cs=d['Adj Close']
dates=d.index; N=len(d); FEE=0.0005
def cloud(a=9,b=26,c=52):
    ten=(Hh.rolling(a).max()+Ll.rolling(a).min())/2; kij=(Hh.rolling(b).max()+Ll.rolling(b).min())/2
    sa=((ten+kij)/2).shift(b); sb=((Hh.rolling(c).max()+Ll.rolling(c).min())/2).shift(b)
    return np.fmax(sa.values,sb.values), np.fmin(sa.values,sb.values), sa.values, sb.values
W0=78
def run(fee=FEE, a=9,b=26,c=52, w0=W0):
    top,bot,sa,sb=cloud(a,b,c)
    cash=10000.0; sh=0; eq=np.full(N,10000.0); inm=np.zeros(N,bool); tr=[]; pend=None
    for t in range(w0,N):
        if pend=='buy' and sh==0: sh=cash*(1-fee)/O[t]; cash=0; tr.append([str(dates[t].date()),None,O[t],None])
        elif pend=='sell' and sh>0: cash=sh*O[t]*(1-fee); sh=0; tr[-1][1]=str(dates[t].date()); tr[-1][3]=O[t]
        pend=None
        if not np.isnan(top[t]):
            if sh==0 and C[t]>top[t]: pend='buy'
            if sh>0 and C[t]<bot[t]: pend='sell'
        eq[t]=sh*C[t]+cash; inm[t]=sh>0
    return eq,tr,inm,(top,bot,sa,sb)
bh=np.full(N,10000.0); bh[W0:]=10000*(1-FEE)/O[W0]*C[W0:]
if __name__=='__main__':
    eq,tr,inm,_=run()
    done=[x for x in tr if x[1]]; rets=[x[3]/x[2]*(1-FEE)**2-1 for x in done]
    print(dates[W0].date(),'final',round(eq[-1]),'bh',round(bh[-1]),'trades',len(tr),'wins',sum(x>0 for x in rets),'inm',inm[W0:].mean())
    dd=lambda e:(e/np.maximum.accumulate(e)-1)[W0:].min(); print('dd',dd(eq),dd(bh))
    for y in range(2005,2025):
        i=np.where(dates.year==y)[0][-1]; print(y, round(eq[i]), round(bh[i]), round(eq[i]/bh[i],2), round(inm[np.where(dates.year==y)[0]].mean(),2))
    print('fees', [round(run(f)[0][-1]) for f in (0.001,0.002)])
    print('params', round(run(a=7,b=22,c=44)[0][-1]), round(run(a=20,b=60,c=120)[0][-1]))
    # biggest losers / whipsaws
    srt=sorted(zip(rets,done)); print(srt[:3]); print(srt[-3:])

def save():
    eq,tr,inm,(top,bot,sa,sb)=run()
    pd.DataFrame({'H':bh,'S':eq,'INM':inm.astype(int),'TOP':top,'BOT':bot},index=dates).to_csv('sim48.csv')
    done=[x for x in tr if x[1]]; rets=[x[3]/x[2]*(1-FEE)**2-1 for x in done]
    json.dump(dict(final=float(eq[-1]),bh=float(bh[-1]),trades=[[a,b,float(c),float(e) if e else None] for a,b,c,e in tr],
       wins=int(sum(r>0 for r in rets)),closed=len(done),inm=float(inm[W0:].mean()),
       dd=float((eq/np.maximum.accumulate(eq)-1).min()),bhdd=float((bh/np.maximum.accumulate(bh)-1).min()),
       fees=[float(run(f)[0][-1]) for f in (0.001,0.002)]),open('results48.json','w'),indent=1)
if __name__=='__main__': save()
