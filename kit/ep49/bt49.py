# #49 Hot inflation: sell stocks when PCE inflation (YoY) > 3%, back in when <= 3%.
# PCE for month M is published ~end of M+1 -> usable from the first trading day of M+2 (no look-ahead).
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=(d.Open*r).values; C=d['Adj Close'].values; D=d.index; n=len(C)
p=pd.read_csv('pcepi.csv',parse_dates=['observation_date']).set_index('observation_date').PCEPI
yoy=(p/p.shift(12)-1)
av=yoy.copy(); av.index=av.index+pd.offsets.MonthBegin(2)
S=av.reindex(D,method='ffill').values
FEE=0.0005
def run(th, skip=None, fee=FEE):
    out=S>th
    if skip is not None: out=out & ~skip
    cash=10000.; sh=0.; inpos=False; eq=np.zeros(n); tin=0; ev=[]
    for i in range(n):
        want = (not out[i-1]) if i>0 else (not out[0])
        if want and not inpos:
            sh=cash*(1-fee)/O[i]; cash=0; inpos=True; ev.append(('BUY',str(D[i].date()),O[i]))
        elif (not want) and inpos:
            cash=sh*O[i]*(1-fee); sh=0; inpos=False; ev.append(('SELL',str(D[i].date()),O[i]))
        eq[i]=cash+sh*C[i]; tin+=inpos
    return eq, ev, tin/n
bh=10000*(1-FEE)/O[0]*C
def stats(eq):
    yrs=(D[-1]-D[0]).days/365.25
    return dict(final=round(eq[-1],2), cagr=round(((eq[-1]/10000)**(1/yrs)-1)*100,2), maxdd=round((eq/np.maximum.accumulate(eq)-1).min()*100,1))
TH=0.03
eq,ev,tin=run(TH)
res=dict(rule='PCE YoY > 3% -> cash (next open), <= 3% -> back in', strat=stats(eq), bh=stats(bh), time_in=round(tin*100,1), events=ev)
print(res['strat'],res['bh'],res['time_in']); [print(e) for e in ev]
res['sells']=sum(1 for e in ev if e[0]=='SELL')
# scan thresholds
res['scan']={}
for th in [0.025,0.0275,0.03,0.0325,0.035,0.0375,0.04,0.045]:
    e2,_,t2=run(th); res['scan'][str(th)]=round(e2[-1]); 
print('scan',res['scan'])
for f in [0.001,0.002]:
    e2,_,_=run(TH,fee=f); print('fee',f,round(e2[-1])); res['fee_%s'%f]=round(e2[-1])
# counterfactual: no 2008 exit (stay in during 2008)
sk=(D>=pd.Timestamp('2008-01-01'))&(D<=pd.Timestamp('2009-06-30'))
e3,ev3,_=run(TH,skip=sk); print('no 2008 exit',round(e3[-1]),stats(e3)); res['no2008']=round(e3[-1])
sk2=(D>=pd.Timestamp('2021-01-01'))
e4,_,_=run(TH,skip=sk2); print('no 2021+ exit',round(e4[-1])); res['no2021']=round(e4[-1])
# key inflation values
for m in ['2008-07-01','2022-06-01','2021-05-01','2005-09-01']:
    print(m, round(yoy[m]*100,2))
res['peak2008']=round(yoy['2008-07-01']*100,2); res['peak2022']=round(yoy['2022-06-01']*100,2)
# value at various dates
def at(s,dt): i=D.searchsorted(pd.Timestamp(dt)); return round(s[i])
for dt in ['2008-08-01','2008-12-31','2009-03-09','2009-03-10','2021-06-01','2022-10-12','2023-08-01','2024-01-02']:
    print(dt,'strat',at(eq,dt),'bh',at(bh,dt))
# lead: dates where strat > bh
lead=eq>bh; print('first day ahead', D[np.argmax(lead)].date(), 'pct days ahead', round(lead.mean()*100,1))
json.dump(res,open('results49.json','w'),indent=1,default=str)
pd.DataFrame({'Date':D,'strat':eq,'bh':bh,'infl':S,'out':S>TH}).to_csv('sim49.csv',index=False)
