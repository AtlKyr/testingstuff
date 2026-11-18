# #30 "Catch the falling knife or wait for green?" After the S&P (SPY) closes down N days in a row:
# KNIFE adds $1,000 at the next open; WAITER waits for the first UP close after the streak and adds $1,000 at the next open.
# New signal only when a NEW streak reaches N (streak counter resets on an up close). Both hold forever. Fee 0.05%.
import pandas as pd, numpy as np, json, sys
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index
FEE=0.0005; AMT=1000
def run(N, save=False):
    n=len(C); up=np.r_[False, C[1:]>C[:-1]]; dn=np.r_[False, C[1:]<C[:-1]]
    streak=0; shK=shW=0; putK=putW=0; waiting=False; eqK=[];eqW=[];pk=[];pw=[]; events=[]
    pendK=None; pendW=None
    for i in range(n):
        # fills at today's open
        if pendK==i: shK+=AMT*(1-FEE)/O[i]; putK+=AMT; events[-1]['k_open']=O[i]; events[-1]['k_date']=str(idx[i].date())
        if pendW==i: shW+=AMT*(1-FEE)/O[i]; putW+=AMT; ev=[e for e in events if e.get('w_date') is None][0]; ev['w_open']=O[i]; ev['w_date']=str(idx[i].date())
        # close signals
        if dn[i]: streak+=1
        elif up[i]: streak=0
        if dn[i] and streak==N and i+1<n:
            pendK=i+1; waiting=True; events.append(dict(sig=str(idx[i].date()),sig_close=C[i]))
        if up[i] and waiting and i+1<n:
            pendW=i+1; waiting=False
        eqK.append(shK*C[i]); eqW.append(shW*C[i]); pk.append(putK); pw.append(putW)
    K=pd.Series(eqK,idx); W=pd.Series(eqW,idx)
    ev=[e for e in events if 'w_open' in e and 'k_open' in e]
    higher=sum(e['w_open']>e['k_open'] for e in ev)
    return K,W,putK,putW,events,higher,pd.Series(pk,idx),pd.Series(pw,idx)
N=int(sys.argv[1]) if len(sys.argv)>1 else 4
K,W,pK,pW,ev,hi,pk,pw=run(N)
print('N',N,'events',len(ev),'putK',pK,'putW',pW,'K',round(K.iloc[-1]),'W',round(W.iloc[-1]),'waiter paid more',hi)
for M in [2,3,4,5,6]:
    k,w,a,b,e,h,_,_=run(M); print(M,len(e),a,b,round(k.iloc[-1]),round(w.iloc[-1]),'paid more',h, round((w.iloc[-1]/b)/(k.iloc[-1]/a)-1,4))

# ---- details for N=4 (the news streak)
K,W,pK,pW,ev,hi,pk,pw=run(4)
ev=[e for e in ev if 'w_open' in e]
for e in ev: e['cost']=e['w_open']/e['k_open']-1
import collections
yrs=collections.Counter(e['sig'][:4] for e in ev); print('per year',dict(sorted(yrs.items())))
for e in ev:
    if e['sig'][:4] in ('2008','2020','2022'): print(e['sig'],e['k_date'],e['w_date'],round(100*e['cost'],2))
cs=sorted(ev,key=lambda e:e['cost']); print('best wait',cs[0]['sig'],round(100*cs[0]['cost'],2),'worst wait',cs[-1]['sig'],cs[-1]['k_date'],cs[-1]['w_date'],round(100*cs[-1]['cost'],2))
diff=(K-W); 
ye=pd.DataFrame({'K':K,'W':W,'d':diff}).resample('YE').last().round(0); print(ye)
print('days K ahead %', round(100*(diff[diff.index>=ev[0]['k_date']]>0).mean(),1))
print('mean cost %', round(100*np.mean([e['cost'] for e in ev]),3))
R=dict(N=4,events=len(ev),put=pK,K=float(K.iloc[-1]),W=float(W.iloc[-1]),paid_more=int(hi),
  scan={str(M):[float(run(M)[0].iloc[-1]),float(run(M)[1].iloc[-1]),run(M)[2]] for M in [3,5]},
  worst=dict(sig=cs[-1]['sig'],k=cs[-1]['k_date'],w=cs[-1]['w_date'],cost=cs[-1]['cost']))
json.dump(R,open('results30.json','w'),indent=1,default=float)
pd.DataFrame({'K':K,'W':W,'PUT':pk}).to_csv('sim30.csv')
json.dump(ev,open('events30.json','w'),indent=0,default=float)
