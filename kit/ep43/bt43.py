import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
k=d['Adj Close']/d['Close']; O=(d['Open']*k).values; C=d['Adj Close'].values; D=d.index
r=np.r_[np.nan, C[1:]/C[:-1]-1]
FEE=0.0005; H=252
idx=[i for i in range(1,len(C)) if r[i]>=0.04]
def run(maxw):
    rows=[]
    for i in idx:
        pre=C[i-1]; end=i+H
        va=10000/(O[i+1]*(1+FEE))*C[end]*(1-FEE)
        j=None
        for t in range(i+1,i+1+maxw):
            if t>=end: break
            if C[t]<pre: j=t; break
        if j is not None and j+1<=end:
            vb=10000/(O[j+1]*(1+FEE))*C[end]*(1-FEE); bd=str(D[j+1].date()); paid=float(O[j+1]/O[i+1]-1)
        else: vb=10000.0; bd=None; paid=None
        rows.append(dict(day=str(D[i].date()),ret=float(round(r[i]*100,2)),A=float(round(va,2)),B=float(round(vb,2)),dip=bool(j is not None),bbuy=bd,paid=paid,end=str(D[end].date())))
    return rows
R=run(H)
A=sum(x['A'] for x in R); B=sum(x['B'] for x in R)
wB=sum(x['B']>x['A'] for x in R); wA=sum(x['A']>x['B'] for x in R); dips=sum(x['dip'] for x in R)
print('N',len(R),'A',round(A),'B',round(B),'Bwins',wB,'Awins',wA,'dips',dips)
cum=0; race=[]
for x in R:
    cum+=x['B']-x['A']; race.append((x["day"],int(round(cum)))); print(x['day'],x['ret'],round(x['A']),round(x['B']),x['dip'],x['bbuy'],'cumB-A',round(cum))
# variants
var={}
for mw in [21,63,126]:
    V=run(mw)
    # if no dip within mw days -> buy anyway at open after day i+mw (re-run variant)
    tot=0
    for i,x in zip(idx,V):
        if x['dip']: tot+=x['B']
        else:
            jb=i+1+mw; tot+=10000/(O[jb]*(1+FEE))*C[i+H]*(1-FEE)
    var[mw]=round(tot); print('wait max',mw,'then buy anyway ->',round(tot))
# no-cost check
# same with close fills check (independent)
first_dip_2008=[x for x in R if x['day']<'2009-03-01']
print('2008 rounds',len(first_dip_2008), all(x['dip'] for x in first_dip_2008))
m=[x for x in R if x['day']=='2009-03-10'][0]; print('mar2009',m)
json.dump(dict(rows=R,A=A,B=B,wB=int(wB),wA=int(wA),dips=int(dips),var=var,race=race),open('results43.json','w'),indent=1)
