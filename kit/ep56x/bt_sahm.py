import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d)
RO=d.Open.values; RC=d.Close.values
s=pd.read_csv('sahm.csv',parse_dates=[0],index_col=0).iloc[:,0]
# month M value usable from the 10th calendar day of M+1 (after the jobs report), act at the first open on/after that day
avail=pd.Series(s.values,index=[ (m+pd.offsets.MonthBegin(1))+pd.Timedelta(days=9) for m in s.index])
sig=avail.reindex(idx,method='ffill').values      # value known at that day's open
def run(th=0.5,back=None,cost=0.0005,lag_days=9):
    back=th if back is None else back
    av=pd.Series(s.values,index=[(m+pd.offsets.MonthBegin(1))+pd.Timedelta(days=lag_days) for m in s.index]).reindex(idx,method='ffill').values
    cash=10000.;sh=0;inp=False;eq=np.zeros(N);IN=np.zeros(N,bool);tr=[]
    for i in range(N):
        want = not (av[i]>=th) if not inp else not (av[i]>=th)
        if i==0: sh=cash*(1-cost)/O[0];cash=0;inp=True;tr.append(['B',i])
        else:
            if inp and av[i]>=th: cash=sh*O[i]*(1-cost);sh=0;inp=False;tr.append(['S',i])
            elif (not inp) and av[i]<back: sh=cash*(1-cost)/O[i];cash=0;inp=True;tr.append(['B',i])
        eq[i]=sh*C[i] if inp else cash; IN[i]=inp
    return eq,IN,tr
eq,IN,tr=run()
bh=10000*(1-0.0005)/O[0]*C
def mdd(x): return float((x/np.maximum.accumulate(x)-1).min())
R=dict(final=float(eq[-1]),bh=float(bh[-1]),mdd=mdd(eq),mdd_bh=mdd(bh),tim=float(IN.mean()))
rt=[]
S=[t[1] for t in tr if t[0]=='S']; B=[t[1] for t in tr if t[0]=='B'][1:]
for a,b in zip(S,B):
    rt.append(dict(sell=str(idx[a].date()),buy=str(idx[b].date()),adj=round(float(O[b]/O[a]-1),4),raw=round(float(RO[b]/RO[a]-1),4),
                   sell_raw=round(float(RO[a]),2),buy_raw=round(float(RO[b]),2)))
if len(S)>len(B): rt.append(dict(sell=str(idx[S[-1]].date()),buy=None,sell_raw=round(float(RO[S[-1]]),2),raw_to_end=round(float(RC[-1]/RO[S[-1]]-1),4)))
R['rt']=rt; R['sells']=len(S)
ratio=eq/bh
for y in range(2007,2025):
    i=np.where(idx.year==y)[0][-1]; R[f'r{y}']=round(float(ratio[i]),3)
im=int(np.argmax(ratio)); R['maxlead']=dict(date=str(idx[im].date()),ratio=round(float(ratio[im]),3))
lead=np.where(ratio>1.0)[0]; R['last_lead']=str(idx[lead[-1]].date()) if len(lead) else None
R['scan']={}
for th in (0.3,0.4,0.5,0.6,0.7,0.8,1.0):
    R['scan'][str(th)]=round(float(run(th)[0][-1]))
R['lag0']=round(float(run(lag_days=0)[0][-1])); R['fee10']=round(float(run(cost=0.001)[0][-1]))
# market moves around sell/buy
json.dump(R,open('results56.json','w'),indent=1)
pd.DataFrame(dict(eq=eq,bh=bh,IN=IN.astype(int),sahm=sig),index=idx).to_csv('sim56.csv')
print(json.dumps(R,indent=0))
