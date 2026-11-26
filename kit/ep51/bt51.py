# #51 Parabolic SAR (Wilder, AF 0.02 step / 0.20 max) on SPY daily H/L (dividend-adjusted).
# Long when SAR is below price (uptrend) at the close -> buy next open; flip to downtrend -> sell next open. 30-bar warm-up.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=(d.Open*r).values; H=(d.High*r).values; L=(d.Low*r).values; C=d['Adj Close'].values; D=d.index; n=len(C)
def psar(af0=0.02, afmax=0.2):
    sar=np.zeros(n); up=True; af=af0; ep=H[0]; sar[0]=L[0]; trend=np.zeros(n,bool)
    for i in range(1,n):
        s=sar[i-1]+af*(ep-sar[i-1])
        if up:
            s=min(s,L[i-1],L[i-2] if i>1 else L[i-1])
            if L[i]<s: up=False; s=ep; ep=L[i]; af=af0
            elif H[i]>ep: ep=H[i]; af=min(af+af0,afmax)
        else:
            s=max(s,H[i-1],H[i-2] if i>1 else H[i-1])
            if H[i]>s: up=True; s=ep; ep=H[i]; af=af0
            elif L[i]<ep: ep=L[i]; af=min(af+af0,afmax)
        sar[i]=s; trend[i]=up
    return trend, sar
WARM=30
def run(trend, fee=0.0005):
    cash=10000.; sh=0.; inpos=False; eq=np.full(n,np.nan); tr=[]; tin=0; s0=WARM+1; inm=np.zeros(n,bool)
    for i in range(s0,n):
        want=trend[i-1]
        if want and not inpos: sh=cash*(1-fee)/O[i]; cash=0; inpos=True; ent=O[i]; ei=i
        elif not want and inpos: cash=sh*O[i]*(1-fee); sh=0; inpos=False; tr.append([str(D[ei].date()), str(D[i].date()), ent, O[i]])
        eq[i]=cash+sh*C[i]; tin+=inpos; inm[i]=inpos
    if inpos: tr.append([str(D[ei].date()), None, ent, C[-1]])
    return eq, tr, tin/(n-s0), inm, s0
trend, sar = psar()
eq, tr, tin, inm, s0 = run(trend)
bh = np.full(n, np.nan); bh[s0:] = 10000*(1-0.0005)/O[s0]*C[s0:]
closed=[t for t in tr if t[1]]
wins=sum(1 for t in closed if t[3]/t[2]*(1-0.0005)**2>1)
hi=sum(1 for k in range(1,len(tr)) if tr[k][2]>tr[k-1][3])
E=pd.Series(eq,index=D); B=pd.Series(bh,index=D)
yr=lambda s,y: s[f'{y}-12-31':f'{y}-12-31'].iloc[-1] if False else s.loc[:f'{y}-12-31'].iloc[-1]
r21_s=yr(E,2021)/yr(E,2020)-1; r21_b=yr(B,2021)/yr(B,2020)-1
r08_s=yr(E,2008)/yr(E,2007)-1; r08_b=yr(B,2008)/yr(B,2007)-1
n21=sum(1 for t in tr if t[0][:4]=='2021'); n08=sum(1 for t in tr if t[0][:4]=='2008')
dd=lambda e: float(np.nanmin(e[s0:]/np.maximum.accumulate(e[s0:])-1))
res=dict(start=str(D[s0].date()), final=round(eq[-1],2), bh=round(bh[-1],2), trades=len(tr), closed=len(closed), wins=wins,
         time_in=round(tin*100,1), rebought_higher=hi, rebuys=len(tr)-1, r21=round(r21_s,4), r21_bh=round(r21_b,4), n21=n21,
         r08=round(r08_s,4), r08_bh=round(r08_b,4), n08=n08, dd=round(dd(eq),4), bhdd=round(dd(bh),4), trades_list=tr)
res['scan']={}
for a in [(0.01,0.1),(0.02,0.1),(0.02,0.2),(0.04,0.4)]:
    t2,_=psar(*a); e2=run(t2)[0]; res['scan'][f'{a[0]}/{a[1]}']=round(e2[-1])
for f in [0.0,0.001]:
    res[f'fee_{f}']=round(run(trend,f)[0][-1])
print({k:v for k,v in res.items() if k!='trades_list'})
json.dump(res,open('results51.json','w'),indent=1,default=float)
pd.DataFrame({'Date':D,'strat':eq,'bh':bh,'sar':sar,'up':trend,'inm':inm}).iloc[s0:].to_csv('sim51.csv',index=False)
