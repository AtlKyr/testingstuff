import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f); C=d['Adj Close']; idx=d.index
y=pd.read_csv('dgs10.csv',parse_dates=['observation_date']).set_index('observation_date')['DGS10']
y=pd.to_numeric(y,errors='coerce').ffill()/100
y=y.reindex(idx.union(y.index)).ffill().reindex(idx)
def dur(yy):
    return (1-(1+yy/2)**-20)/yy
def conv(yy):
    h=1e-4; P=lambda r: sum(0.5*yy/ (1+r/2)**k for k in range(1,21))+1/(1+r/2)**20
    return (P(yy+h)+P(yy-h)-2*P(yy))/(P(yy)*h*h)
yp=y.shift(1); dy=y-yp
D=yp.apply(dur); Cv=yp.apply(conv)
rb=(yp/252 - D*dy + 0.5*Cv*dy**2).fillna(0)
BI=(1+rb).cumprod()   # simulated 10y Treasury total return index (close to close)
FEE=0.0005
def run(ws=0.6, rebal=True):
    # buy at first open (bond at first close level approx), then mark at closes; rebalance at the first trading day's close each year
    s=10000*ws*(1-FEE)/O.iloc[0]; b=10000*(1-ws)*(1-FEE)/BI.iloc[0]; eq=[]; yr=idx[0].year
    for i,t in enumerate(idx):
        if rebal and t.year!=yr:
            yr=t.year; tot=s*C.iloc[i]+b*BI.iloc[i]; ts=tot*ws; trade=abs(ts-s*C.iloc[i]); tot-=trade*FEE*2
            s=tot*ws/C.iloc[i]; b=tot*(1-ws)/BI.iloc[i]
        eq.append(s*C.iloc[i]+b*BI.iloc[i])
    return pd.Series(eq,idx)
if __name__=='__main__':
    bh=run(1.0,False); p=run(0.6)
    yb=BI.resample('YE').last().pct_change(); print('bond yearly', (yb*100).round(1).to_dict())
    print('BH',int(bh.iloc[-1]),'6040',int(p.iloc[-1]))
    for w in [0.5,0.6,0.7,0.8]: print(w,int(run(w).iloc[-1]))
    mdd=lambda e:(e/e.cummax()-1).min(); print('mdd',mdd(bh),mdd(p))
    df=pd.DataFrame({'bh':bh,'p':p}); print(df.resample('YE').last().astype(int).T.to_string())
    lead=p>bh; print('lead frac by yr',lead.groupby(idx.year).mean().round(2).to_dict()); print('last lead',lead[lead].index[-1])
    print('2022', (df.loc['2022-12-30']/df.loc['2021-12-31']-1).round(3).to_dict(), '2008',(df.loc['2008-12-31']/df.loc['2007-12-31']-1).round(3).to_dict())
    print('bond total', BI.iloc[-1]/BI.iloc[0])
    bi=BI; yb=bi.resample('YE').last()
    R=dict(bh=float(bh.iloc[-1]), p=float(p.iloc[-1]), s08=float(bh.loc['2008-12-31']/bh.loc['2007-12-31']-1), p08=float(p.loc['2008-12-31']/p.loc['2007-12-31']-1),
           s22=float(bh.loc['2022-12-30']/bh.loc['2021-12-31']-1), p22=float(p.loc['2022-12-30']/p.loc['2021-12-31']-1), b22=float(bi.loc['2022-12-30']/bi.loc['2021-12-31']-1),
           mdd_bh=float((bh/bh.cummax()-1).min()), mdd_p=float((p/p.cummax()-1).min()), scan={str(w):float(run(w).iloc[-1]) for w in [0.5,0.7,0.8]},
           lead2020=int((p>bh)['2020'].sum()), b08=float(bi.loc['2008-12-31']/bi.loc['2007-12-31']-1))
    json.dump(R,open('results41.json','w'),indent=1)
    pd.DataFrame({'H':bh,'P':p,'BI':BI}).to_csv('sim41.csv')
    print(R)
