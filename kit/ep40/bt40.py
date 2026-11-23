import pandas as pd, numpy as np, json, sys
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index
gap=np.r_[np.nan, O[1:]/C[:-1]-1]
FEE=0.0005
def run(th=0.02, N=5, fee=FEE, rec=False):
    cash=10000.0; sh=0.0; inpos=False; buyback=None; trades=[]; eq=[]
    # start: buy at first open
    sh=cash*(1-fee)/O[0]; cash=0; inpos=True
    for i in range(len(C)):
        if inpos and i>0 and gap[i]>=th:
            cash=sh*O[i]*(1-fee); sh=0; inpos=False; buyback=i+N; trades.append([str(idx[i].date()), O[i], None, None])
        elif (not inpos) and i==buyback:
            sh=cash*(1-fee)/O[i]; cash=0; inpos=True; trades[-1][2]=str(idx[i].date()); trades[-1][3]=O[i]
        eq.append(cash+sh*C[i])
    return np.array(eq), trades
bh=np.array([10000*(1-FEE)/O[0]*c for c in C])
if __name__=='__main__':
    for th in [0.01,0.015,0.02,0.025,0.03]:
        print(th, [int(run(th,N)[0][-1]) for N in [1,2,3,5,10,21]])
    print('BH', int(bh[-1]))
    eq,tr=run(0.02,5)
    hi=sum(1 for t in tr if t[3] and t[3]>t[1]); print('trades',len(tr),'rebought higher',hi)
    print(tr[:5])

if __name__=='__main__':
    eq,tr=run(0.02,5)
    sells=[t[0] for t in tr]; buys=[t[2] for t in tr]
    pd.DataFrame({'S':eq,'H':bh},index=idx).to_csv('sim40.csv')
    i24=list(idx).index(pd.Timestamp('2020-03-24'))
    t24=[x for x in tr if x[0]=='2020-03-24'][0]
    t10=[x for x in tr if x[0]=='2020-03-10'][0]
    s=pd.Series(eq,idx); b=pd.Series(bh,idx); lead=s>b
    scan={f"{th}_{N}":int(run(th,N)[0][-1]) for th in [0.015,0.02,0.025] for N in [1,3,5,10]}
    R=dict(final=float(eq[-1]), bh=float(bh[-1]), n_gaps=int((gap>=0.02).sum()), n_sells=len(tr), cheaper=sum(1 for x in tr if x[3]<x[1]),
           gap24=float(gap[i24]), rebuy24=float(t24[3]/t24[1]-1), rebuy10=float(t10[3]/t10[1]-1), last_lead=str(lead[lead].index[-1].date()),
           sells=sells, buys=buys, fee10=float(run(0.02,5,0.001)[0][-1]), fee0=float(run(0.02,5,0)[0][-1]), scan=scan,
           cagr=float((eq[-1]/10000)**(1/20)-1), cagr_bh=float((bh[-1]/10000)**(1/20)-1),
           mdd=float((eq/np.maximum.accumulate(eq)-1).min()), mdd_bh=float((bh/np.maximum.accumulate(bh)-1).min()),
           tim=float(1-5*len(tr)/len(idx)))
    json.dump(R,open('results40.json','w'),indent=1); print({k:v for k,v in R.items() if k not in('sells','buys')})
