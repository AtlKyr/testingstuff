# #57 Yield-curve inversion rule: FRED T10Y2Y (10y minus 2y). Value known at the close of day i = previous business day's FRED
# value (1-day publication lag). Close of day i: spread < 0 -> sell at next open; spread > 0 -> buy back at next open. 0.05%/side.
import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d); RO=d.Open.values; RC=d.Close.values
y=pd.read_csv('t10y2y.csv',parse_dates=[0],index_col=0).iloc[:,0]; y=pd.to_numeric(y,errors='coerce').dropna()
sp=y.shift(1).reindex(idx.union(y.index)).ffill().reindex(idx).values
def run(confirm=1,cost=0.0005):
    cash=1e4;sh=0;inp=False;eq=np.zeros(N);IN=np.zeros(N,bool);pend=None;tr=[];neg=pos=0
    for i in range(N):
        if pend=='S' and inp: cash=sh*O[i]*(1-cost);sh=0;inp=False;tr.append(['S',i])
        elif pend=='B' and not inp: sh=cash*(1-cost)/O[i];cash=0;inp=True;tr.append(['B',i])
        pend=None
        if i==0: sh=cash*(1-cost)/O[0];cash=0;inp=True
        eq[i]=sh*C[i] if inp else cash; IN[i]=inp
        neg=neg+1 if sp[i]<0 else 0; pos=pos+1 if sp[i]>0 else 0
        if inp and neg>=confirm: pend='S'
        elif (not inp) and pos>=confirm: pend='B'
    return eq,IN,tr
eq,IN,tr=run()
bh=1e4*(1-0.0005)/O[0]*C
def mdd(x): return float((x/np.maximum.accumulate(x)-1).min())
R=dict(final=float(eq[-1]),bh=float(bh[-1]),mdd=mdd(eq),mdd_bh=mdd(bh),tim=float(IN.mean()))
S=[t[1] for t in tr if t[0]=='S']; B=[t[1] for t in tr if t[0]=='B']
R['sells']=len(S); R['sells_0607']=len([s for s in S if idx[s].year<=2007])
R['trades']=[dict(k=t[0],d=str(idx[t[1]].date()),raw=round(float(RO[t[1]]),2)) for t in tr]
i_s22=[s for s in S if idx[s].year==2022][-1]; i_b24=[b for b in B if idx[b].year==2024][0]
R['s22']=str(idx[i_s22].date()); R['b24']=str(idx[i_b24].date()); R['raw22_24']=float(RO[i_b24]/RO[i_s22]-1); R['adj22_24']=float(O[i_b24]/O[i_s22]-1)
R['out22_years']=(idx[i_b24]-idx[i_s22]).days/365.25
i_b07=[b for b in B if idx[b].year==2007][-1]; R['b07']=str(idx[i_b07].date()); R['b07_raw']=float(RO[i_b07])
top=int(np.argmax(RC[:np.searchsorted(idx,pd.Timestamp('2008-01-01'))])); R['top07']=str(idx[top].date())
R['months_before_top']=(idx[top]-idx[i_b07]).days/30.44
# inversion streak 2022-2024 (calendar)
neg=y[y<0]; R['inv_start']=str(y['2022-07':][y['2022-07':]<0].index[0].date()); _z=y[R['inv_start']:]; R['inv_end']=str(_z[_z>0].index[0].date())
R['inv_years']=(pd.Timestamp(R['inv_end'])-pd.Timestamp(R['inv_start'])).days/365.25
R['scan']={str(c):round(float(run(c)[0][-1])) for c in (5,10,21,63)}
R['fee10']=round(float(run(cost=0.001)[0][-1]))
ratio=eq/bh
for yy in (2006,2007,2008,2009,2019,2021,2022,2023,2024): R[f'r{yy}']=round(float(ratio[np.where(idx.year==yy)[0][-1]]),3)
json.dump(R,open('results57.json','w'),indent=1)
pd.DataFrame(dict(eq=eq,bh=bh,IN=IN.astype(int),sp=sp),index=idx).to_csv('sim57.csv')
print(json.dumps({k:v for k,v in R.items() if k!='trades'},indent=0))
