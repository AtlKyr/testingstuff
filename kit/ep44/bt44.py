import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
C=d['Adj Close']; RAW=d['Close']
cpi=pd.read_csv('cpi.csv',parse_dates=['observation_date']).set_index('observation_date')['CPIAUCSL']
FEE=0.0005; START='2007-10-09'; INIT=1_000_000
s=C[START:]
first=set(s.groupby([s.index.year,s.index.month]).head(1).index)
c_base=cpi[pd.Timestamp('2007-09-01')]
def sim(rate=0.04, panic=None):
    sh=INIT*(1-FEE)/s.iloc[0]; cash=0.0; out=[]; totw=0; broke=None; wlist=[]; sold=None
    for t in s.index:
        if t in first or t==s.index[0]:
            cp=cpi[(t.replace(day=1)-pd.offsets.MonthBegin(1))]
            w=INIT*rate/12*cp/c_base
            if cash>0 or sold is not None:
                if cash<w and broke is None: broke=t; totw+=cash; cash=0
                elif broke is None: cash-=w; totw+=w
            else:
                need=w/(s[t]*(1-FEE))
                if need>sh: broke=t; sh=0
                else: sh-=need; totw+=w
            wlist.append((t,w))
        v=sh*s[t]+cash
        if panic is not None and sold is None and sh>0 and v<=panic*INIT:
            cash=sh*s[t]*(1-FEE); sh=0; sold=t; v=cash
        out.append(v)
    return pd.Series(out,index=s.index), totw, broke, wlist, sold
V,TW,BR,WL,_=sim()
i_low=V.idxmin()
print('final',round(V.iloc[-1]),'withdrawn',round(TW),'low',round(V.min()),i_low.date(),'broke',BR)
yr=pd.Series({t.year:w for t,w in WL}); print('first monthly',round(WL[0][1],2),'yearly 2008',round(sum(w for t,w in WL if t.year==2008)),'yearly 2024',round(sum(w for t,w in WL if t.year==2024)))
P,TWp,BRp,_,sold=sim(panic=0.5); print('panic sold',sold.date() if sold is not None else None,'broke',BRp,'final',round(P.iloc[-1]),'withdrawn',round(TWp))
for r in [0.03,0.05,0.06,0.07]:
    X,t2,b2,_,_=sim(r); print('rate',r,round(X.iloc[-1]),'broke',b2,'low',round(X.min()))
bh=INIT*(1-FEE)/s.iloc[0]*s.iloc[-1]*(1-FEE); print('never withdrew',round(bh))
# when did balance first get back above 1M
back=V[i_low:][V[i_low:]>=INIT].index[0]; print('back above 1M',back.date())
raw_dd=RAW[START:].min()/RAW[START]-1; print('raw SPY drawdown',raw_dd)
pd.DataFrame({'V':V,'P':P}).to_csv('sim44.csv')
json.dump(dict(final=float(V.iloc[-1]),withdrawn=float(TW),low=float(V.min()),low_d=str(i_low.date()),w0=WL[0][1]*12,w2024=float(sum(w for t,w in WL if t.year==2024)),
  panic_sold=str(sold.date()),panic_broke=str(BRp.date()) if BRp is not None else None,back1m=str(back.date()),bh=float(bh),
  r6=float(sim(0.06)[0].iloc[-1]),r5=float(sim(0.05)[0].iloc[-1])),open('results44.json','w'),indent=1)
