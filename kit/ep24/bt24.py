import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=d['Open']*r; C=d['Adj Close']
v=pd.read_csv('vix.csv',parse_dates=['observation_date']).set_index('observation_date')['VIXCLS']
v=pd.to_numeric(v,errors='coerce').reindex(d.index).ffill()
FEE=0.0005
def run(hi=30,lo=20,fee=FEE):
    n=len(d); cash=10000.; sh=0.; inm=False; eq=np.zeros(n); trades=[]; IN=np.zeros(n,bool)
    # start invested at first open
    sh=cash*(1-fee)/O.iloc[0]; cash=0; inm=True; ent=O.iloc[0]
    pending=None
    for i in range(n):
        if pending=='sell' and inm:
            cash=sh*O.iloc[i]*(1-fee); trades.append(('S',d.index[i],O.iloc[i])); sh=0; inm=False
        elif pending=='buy' and not inm:
            sh=cash*(1-fee)/O.iloc[i]; cash=0; inm=True; trades.append(('B',d.index[i],O.iloc[i]))
        pending=None
        IN[i]=inm
        eq[i]=sh*C.iloc[i] if inm else cash
        x=v.iloc[i]
        if inm and x>=hi: pending='sell'
        elif (not inm) and x<lo: pending='buy'
    return pd.Series(eq,d.index),trades,IN
eq,tr,IN=run()
bh=10000*(1-FEE)/O.iloc[0]*C*(1-FEE)
def dd(s): return (s/s.cummax()-1).min()
yrs=(d.index[-1]-d.index[0]).days/365.25
print('final',round(eq.iloc[-1]),'bh',round(bh.iloc[-1]),'cagr',(eq.iloc[-1]/1e4)**(1/yrs)-1,(bh.iloc[-1]/1e4)**(1/yrs)-1)
print('dd',dd(eq),dd(bh),'inmkt',IN.mean(),'sells',sum(1 for t in tr if t[0]=='S'))
# round trips: sell then buy back -> price diff
pairs=[];s=None
for t in tr:
    if t[0]=='S': s=t
    else: pairs.append((s[1].date(),t[1].date(),s[2],t[2],t[2]/s[2]-1))
for p in pairs: print(p[0],p[1],round(p[4]*100,1))
print('higher rebuys',sum(p[4]>0 for p in pairs),'of',len(pairs))
for f in [0.001,0.002]: print('fee',f,round(run(fee=f)[0].iloc[-1]))
for hi in [25,30,35,40]:
  for lo in [15,20,25]:
    if lo<hi: print(hi,lo,round(run(hi,lo)[0].iloc[-1]))
# years
ye=eq.resample('YE').last(); yb=bh.resample('YE').last()
print(pd.DataFrame({'s':ye.round(),'b':yb.round()}))
print('vix>=30 days',(v>=30).mean())
pd.DataFrame({'eq':eq,'bh':bh,'IN':IN,'vix':v,'C':C}).to_csv('sim24.csv')
# ---- export for the render
O_=O.values
sim=pd.DataFrame({'R':eq,'B':bh,'IN':IN.astype(int),'O':O,'C':C,'V':v})
sim.to_csv('sim24.csv')
scan={f"{h}/{l}":round(run(h,l)[0].iloc[-1]) for h in [25,30,35,40] for l in [15,20,25] if l<h}
res=dict(final=float(eq.iloc[-1]),bh=float(bh.iloc[-1]),dd=float(dd(eq)),bhdd=float(dd(bh)),inmkt=float(IN.mean()),
 pairs=[(str(a),str(b),float(c)) for a,b,_,_,c in pairs],scan=scan,fee10=round(run(fee=0.001)[0].iloc[-1]),fee20=round(run(fee=0.002)[0].iloc[-1]),
 news=dict(date='2026-11-05',vix_close=28.18,vix_prev=16.61,pct=69.66))
json.dump(res,open('results24.json','w'),indent=1)
print(scan, 'all lose', all(x<bh.iloc[-1] for x in scan.values()), 'best', max(scan.values()))
