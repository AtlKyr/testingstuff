import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d)
cost=0.0005
# January barometer: if SPY's January (last Dec close -> last Jan close, adj) is up, own Feb..Dec; else cash Feb..Dec. Always own January.
years=sorted(set(idx.year))
def run(cost=0.0005, rule='baro', TH=0.0):
    cash=10000.; sh=0.; inpos=False; eq=np.zeros(N); IN=np.zeros(N,bool); trades=0; dec=[]
    for i in range(N):
        y,m=idx[i].year,idx[i].month
        first_of_month = i==0 or idx[i-1].month!=m
        if first_of_month:
            want = True
            if m>=2:
                # January return known at last Jan close
                jan=[k for k in range(N) if idx[k].year==y and idx[k].month==1]
                prev=jan[0]-1
                jr = C[jan[-1]]/ (C[prev] if prev>=0 else O[jan[0]]) - 1
                want = jr>TH if rule=='baro' else True
            if want and not inpos:
                sh=cash*(1-cost)/O[i]; cash=0; inpos=True; trades+=1
            elif not want and inpos:
                cash=sh*O[i]*(1-cost); sh=0; inpos=False
        eq[i]= sh*C[i] if inpos else cash; IN[i]=inpos
    return eq,IN,trades
eq,IN,tr=run()
bh=10000*(1-cost)/O[0]*C
res=dict(final=float(eq[-1]),bh=float(bh[-1]),trades=tr,tim=float(IN.mean()))
yr=[]
for y in years:
    ii=[k for k in range(N) if idx[k].year==y]
    jan=[k for k in ii if idx[k].month==1]; prev=jan[0]-1
    jr=C[jan[-1]]/(C[prev] if prev>=0 else O[jan[0]])-1
    rest=C[ii[-1]]/C[jan[-1]]-1
    yr.append(dict(y=int(y),jan=round(float(jr),4),rest=round(float(rest),4),full=round(C[ii[-1]]/(C[prev] if prev>=0 else O[jan[0]])-1,4)))
res['years']=yr
res['jan_down']=[r['y'] for r in yr if r['jan']<=0]
res['jan_down_rest_up']=[r['y'] for r in yr if r['jan']<=0 and r['rest']>0]
res['agree']=sum((r['jan']>0)==(r['full']>0) for r in yr)
res['agree_rest']=sum((r['jan']>0)==(r['rest']>0) for r in yr)
def mdd(x): return float((x/np.maximum.accumulate(x)-1).min())
res['scan']={str(th):float(run(TH=th)[0][-1]) for th in (-0.02,-0.05,0.02)}
res['fee0.001']=float(run(0.001)[0][-1])
res['mdd']=mdd(eq); res['mdd_bh']=mdd(bh)
json.dump(res,open('results54.json','w'),indent=1,default=lambda o: o.item() if hasattr(o,'item') else str(o))
pd.DataFrame(dict(eq=eq,bh=bh,IN=IN),index=idx).to_csv('sim54.csv')
print({k:v for k,v in res.items() if k!='years'})
for r in yr: print(r)
