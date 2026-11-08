import pandas as pd, numpy as np, json
d=pd.read_csv('spy.csv',parse_dates=['Date']).set_index('Date').loc['2005-01-01':'2024-12-31']
r=d['Adj Close']/d['Close']; O=(d.Open*r).values; C=d['Adj Close'].values; D=d.index
ret=np.r_[np.nan, C[1:]/C[:-1]-1]
TH=-0.04; FEE=0.0005
crash=[i for i in range(1,len(C)) if ret[i]<=TH]
def fwd(i,n): j=min(i+n,len(C)-1); return C[j]/C[i]-1
rows=[dict(date=str(D[i].date()),drop=ret[i],d1=fwd(i,1),m1=fwd(i,21),y1=fwd(i,252)) for i in crash]
df=pd.DataFrame(rows)
base={n:float(np.mean([(C[i+n]/C[i]-1)>0 for i in range(len(C)-n)])) for n in (1,21,252)}
bh=10000*(1-FEE)/O[0]*C[-1]
BHc=10000*(1-FEE)/O[0]*C
def panic(hold):
    sh=10000*(1-FEE)/O[0]; cash=0.0; out_until=-1; eq=np.zeros(len(C)); n=0
    for i in range(len(C)):
        if sh==0 and i>=out_until and out_until>0:
            sh=cash*(1-FEE)/O[i]; cash=0.0
        eq[i]=sh*C[i] if sh>0 else cash
        if sh>0 and ret[i]<=TH and i+1<len(C):
            cash=sh*O[i+1]*(1-FEE); sh=0.0; out_until=i+1+hold; n+=1
    return eq, n
res={}
for h in (5,10,15,21,30,42,63,126):
    eq,n=panic(h); res[h]=(round(float(eq[-1])),n)
print('B&H',round(bh)); print('panic',res)
eq21,_=panic(21); np.save('eq_panic21.npy',eq21); np.save('eq_bh.npy',BHc)
best=np.argsort(ret[1:])[-10:][::-1]+1
near=[(str(D[b].date()),round(ret[b]*100,1), min(abs((D[b]-D[c]).days) for c in crash)) for b in best]
yrs=pd.Series([D[i].year for i in crash]).value_counts().sort_index().to_dict()
out=dict(n=len(crash),years=yrs,rows=rows,base=base,
 pos=dict(d1=float((df.d1>0).mean()),m1=float((df.m1>0).mean()),y1=float((df.y1>0).mean())),
 med=dict(d1=float(df.d1.median()),m1=float(df.m1.median()),y1=float(df.y1.median())),
 y1_neg=df[df.y1<=0].date.tolist(), worst=(str(D[int(np.nanargmin(ret))].date()), float(np.nanmin(ret))),
 best10=near, bh=round(bh), panic=res, crash_idx=crash)
json.dump(out,open('l2.json','w'),indent=1,default=str)
print({k:out[k] for k in ('n','years','base','pos','med','y1_neg','worst')}); print(near)
