import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
k=d['Adj Close']/d['Close']; O=(d['Open']*k); C=d['Adj Close']; D=d.index
FEE=0.0005; WARM=60
def run(n=20, m=2.0, exit_mid=True, start=WARM):
    ma=C.rolling(n).mean(); sd=C.rolling(n).std(); lo=ma-m*sd; up=ma+m*sd
    pos=0; cash=10000.0; sh=0; eq=[]; trades=[]; inn=[]; entry=None
    for i in range(start, len(C)):
        # execute pending at open i
        if i>start:
            sig_buy = pos==0 and C.iloc[i-1] < lo.iloc[i-1]
            sig_sell = pos==1 and (C.iloc[i-1] > (ma.iloc[i-1] if exit_mid else up.iloc[i-1]))
            if sig_buy:
                sh=cash*(1-FEE)/O.iloc[i]; entry=(D[i],O.iloc[i],cash); cash=0; pos=1
            elif sig_sell:
                cash=sh*O.iloc[i]*(1-FEE); trades.append((str(entry[0].date()),str(D[i].date()),float(entry[1]),float(O.iloc[i]),cash/entry[2]-1)); sh=0; pos=0
        eq.append(cash+sh*C.iloc[i]); inn.append(pos)
    eq=pd.Series(eq,index=D[start:]); 
    return eq, trades, np.mean(inn), lo, ma
eq,tr,tim,lo,ma=run()
bh=10000*(1-FEE)/O.iloc[WARM]*C.iloc[-1]*(1-FEE)
bhs=10000/O.iloc[WARM]*C.iloc[WARM:]
wins=sum(1 for t in tr if t[4]>0)
dd=(eq/eq.cummax()-1).min(); bdd=(bhs/bhs.cummax()-1).min()
yrs=(D[-1]-D[WARM]).days/365.25
print('start',D[WARM].date(),'final',round(eq.iloc[-1]),'bh',round(bh),'trades',len(tr),'wins',wins,round(wins/len(tr)*100,1),'time',round(tim*100,1))
print('cagr',round(((eq.iloc[-1]/1e4)**(1/yrs)-1)*100,2),'bh cagr',round(((bh/1e4)**(1/yrs)-1)*100,2),'dd',round(dd*100,1),'bhdd',round(bdd*100,1))
rets=[t[4] for t in tr]; print('avg trade',round(np.mean(rets)*100,2),'best',max(rets),'worst',min(rets))
worst=sorted(tr,key=lambda t:t[4])[:5]; print('worst',worst)
best=sorted(tr,key=lambda t:-t[4])[:3]; print('best',best)
# year-by-year
ys=eq.resample('YE').last(); yb=bhs.resample('YE').last(); 
for y in [2008,2009,2013,2017,2020,2022,2024]: print(y, round(ys[str(y)].iloc[0]), round(yb[str(y)].iloc[0]))
# lead periods
lead=(eq>bhs*(bh/bhs.iloc[-1]) )
r=eq/ (bhs); print('max ratio',round(r.max(),3), r.idxmax().date(), 'last date ahead', r[r>1].index.max())
for fee in [0.001,0.002]:
    FEE=fee
    e2,t2,_,_,_=run(); print('fee',fee,round(e2.iloc[-1]))
FEE=0.0005
for n,m,em in [(20,2,False),(20,2.5,True),(20,1.5,True),(10,2,True),(50,2,True)]:
    e2,t2,ti2,_,_=run(n,m,em); print('var',n,m,em,round(e2.iloc[-1]),len(t2),round(ti2*100))
json.dump(dict(final=float(eq.iloc[-1]),bh=float(bh),trades=tr,n=len(tr),wins=wins,tim=float(tim),dd=float(dd),bdd=float(bdd),start=str(D[WARM].date())),open('results45.json','w'),indent=1)
pd.DataFrame({'S':eq,'H':bhs*(1-FEE)**2}).to_csv('sim45.csv')
