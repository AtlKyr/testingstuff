import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; RC=d.Close.values; RO=d.Open.values
idx=d.index; N=len(d); cost=0.0005
rec=np.maximum.accumulate(RC); dd=RC/rec-1
def episodes(th=0.20):
    inbear=False; eps=[]
    for k in range(N):
        if RC[k]>=rec[k]: inbear=False
        if not inbear and dd[k]<=-th: inbear=True; eps.append(k)
    return eps
def run(th=0.20, up=0.20, horizon=None):
    rows=[]; A=np.zeros(N); B=np.zeros(N)
    for k in episodes(th):
        m=RC[k]; j=None; lo=k
        for q in range(k,N):
            if RC[q]<m: m=RC[q]; lo=q
            if RC[q]>=(1+up)*m: j=q;break
        ia, ib = k+1, j+1
        sa=1e4*(1-cost)/O[ia]; sb=1e4*(1-cost)/O[ib]
        A[ia:]+=sa*C[ia:]; B[ib:]+=sb*C[ib:]
        B[ia:ib]+=1e4   # waiter keeps his $10K in cash meanwhile
        rows.append(dict(sig=str(idx[k].date()),a_buy=str(idx[ia].date()),b_buy=str(idx[ib].date()),low=str(idx[lo].date()),
            a_px=float(O[ia]),b_px=float(O[ib]),a_raw=float(RO[ia]),b_raw=float(RO[ib]),b_vs_a=float(O[ib]/O[ia]-1),b_vs_a_raw=float(RO[ib]/RO[ia]-1),
            a_end=float(sa*C[-1]),b_end=float(sb*C[-1]),days_wait=int(ib-ia),low_dd=float(RC[lo]/rec[k]-1)))
    return A,B,rows
A,B,rows=run()
res=dict(rows=rows,A=float(A[-1]),B=float(B[-1]),a_wins=sum(r['a_end']>r['b_end'] for r in rows),n=len(rows))
res['scan_up']={str(u):[round(float(run(0.2,u)[0][-1])),round(float(run(0.2,u)[1][-1]))] for u in (0.10,0.15,0.20,0.25,0.30)}
res['scan_th']={str(t):[round(float(run(t,0.2)[0][-1])),round(float(run(t,0.2)[1][-1])),len(episodes(t))] for t in (0.15,0.20,0.25)}
# 1-year horizon per round
oneyr=[]
for r in rows:
    ia=idx.get_loc(pd.Timestamp(r['a_buy'])); ib=idx.get_loc(pd.Timestamp(r['b_buy']))
    oneyr.append((r['sig'], round(C[min(N-1,ia+252)]/O[ia]-1,3), round(C[min(N-1,ib+252)]/O[ib]-1,3)))
res['oneyr']=oneyr
lead=np.sign(A-B); res['lead_changes']=[str(idx[i].date()) for i in range(1,N) if lead[i]!=lead[i-1] and A[i]>0]
json.dump(res,open('results53.json','w'),indent=1)
pd.DataFrame(dict(A=A,B=B),index=idx).to_csv('sim53.csv')
print(json.dumps({k:v for k,v in res.items()},indent=1))
