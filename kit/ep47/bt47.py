import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=(d['Open']*r).values; C=d['Adj Close'].values
dates=d.index; N=len(d); FEE=0.0005
yrs=sorted(set(dates.year))
last={y:np.where(dates.year==y)[0][-1] for y in yrs}; first={y:np.where(dates.year==y)[0][0] for y in yrs}
yret={}
for y in yrs:
    prev=C[last[y-1]] if y-1 in last else O[first[y]]
    yret[y]=C[last[y]]/prev-1
def run(th=0.20, fee=FEE):
    out_years=[y+1 for y in yrs if yret[y]>=th and y+1 in first]
    sells={first[y]:y for y in out_years}; buys={first[y+1]:y for y in out_years if y+1 in first}
    sh=10000*(1-fee)/O[0]; cash=0; eq=np.zeros(N); inm=np.ones(N,bool)
    for t in range(N):
        if t in sells and sh>0: cash=sh*O[t]*(1-fee); sh=0
        if t in buys and sh==0: sh=cash*(1-fee)/O[t]; cash=0
        eq[t]=sh*C[t]+cash; inm[t]=sh>0
    return eq,out_years,inm
bh=10000*(1-FEE)/O[0]*C
if __name__=='__main__':
    for y in yrs: print(y, round(yret[y]*100,1))
    for th in [0.10,0.15,0.20,0.25,0.30]:
        e,o,_=run(th); print(th, o, round(e[-1]))
    e,o,inm=run(); print('bh',round(bh[-1]), 'final',round(e[-1]), 'inm',inm.mean())
    print('next-year returns', {y:round(yret[y]*100,1) for y in o})
    dd=lambda e:(e/np.maximum.accumulate(e)-1).min(); print(dd(e),dd(bh))
    # after big years vs other years average next-year return
    big=[yret[y+1] for y in yrs if yret[y]>=0.2 and y+1 in yret]; oth=[yret[y+1] for y in yrs if yret[y]<0.2 and y+1 in yret]
    print('avg next after big',np.mean(big),len(big),'pos',sum(x>0 for x in big),' other',np.mean(oth),len(oth))
    # lead over time
    for y in yrs: print(y, round(e[last[y]]), round(bh[last[y]]), round(e[last[y]]/bh[last[y]],3))

def save():
    e,o,inm=run()
    pd.DataFrame({'H':bh,'S':e,'INM':inm.astype(int)},index=dates).to_csv('sim47.csv')
    json.dump(dict(final=float(e[-1]),bh=float(bh[-1]),out=o,yret={str(k):float(v) for k,v in yret.items()},
      ths={str(th):float(run(th)[0][-1]) for th in [0.10,0.15,0.20,0.25,0.30]}, fees={str(f):float(run(fee=f)[0][-1]) for f in [0.001,0.002]},
      inm=float(inm.mean())),open('results47.json','w'),indent=1)
if __name__=='__main__': save()
