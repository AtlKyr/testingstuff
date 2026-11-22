# #38 Thanksgiving week: sit it out vs hold through. SPY 2005-2024.
# A ("sit out"): sell at the OPEN of the Monday of Thanksgiving week (signal = calendar), buy back at the OPEN of the Monday after.
# B: buy & hold from the first open 2005-01-03 to the last adj close. 0.05% per side.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d['Open']*f; C=d['Adj Close']; idx=d.index
COST=0.0005
def tg(y):
    nov=pd.date_range(f'{y}-11-01',f'{y}-11-30'); return [x for x in nov if x.weekday()==3][3]
weeks=[]
for y in range(2005,2025):
    th=tg(y); mon=th-pd.Timedelta(days=3); nmon=th+pd.Timedelta(days=4)
    s=idx[idx>=mon][0]; b=idx[idx>=nmon][0]; fri=idx[idx<=th+pd.Timedelta(days=1)][-1]
    prev=idx[idx<s][-1]
    weeks.append(dict(y=y,sell=str(s.date()),buy=str(b.date()),sellpx=O[s],buypx=O[b],
        wk_cc=C[fri]/C[prev]-1, wk_skip=O[b]/O[s]-1))
def run(skip_years, cost=COST):
    eq=10000*(1-cost)/O.iloc[0]  # shares
    cash=None; sh=eq; curve=[]
    sells={pd.Timestamp(w['sell']):w for w in weeks if w['y'] in skip_years}
    buys={pd.Timestamp(w['buy']):w for w in weeks if w['y'] in skip_years}
    inmk=[]
    for t in idx:
        if t in buys and cash is not None:
            sh=cash*(1-cost)/O[t]; cash=None
        if t in sells and cash is None:
            cash=sh*O[t]*(1-cost); sh=0
        v= cash if cash is not None else sh*C[t]
        curve.append(v); inmk.append(cash is None)
    return pd.Series(curve,idx), np.array(inmk)
allY=[w['y'] for w in weeks]
A,inA=run(allY); B,_=run([])
B2=10000*(1-COST)*C/O.iloc[0]
assert abs(B.iloc[-1]-B2.iloc[-1])<1
def mdd(s): return float((s/s.cummax()-1).min())
yrs=(idx[-1]-idx[0]).days/365.25
res=dict(A=float(A.iloc[-1]),B=float(B.iloc[-1]),A_cagr=(A.iloc[-1]/1e4)**(1/yrs)-1,B_cagr=(B.iloc[-1]/1e4)**(1/yrs)-1,
 A_mdd=mdd(A),B_mdd=mdd(B),time_in=float(inA.mean()),trades=len(allY),
 up_weeks_cc=int(sum(w['wk_cc']>0 for w in weeks)), up_skip=int(sum(w['wk_skip']>0 for w in weeks)),
 weeks=[{k:(round(v,5) if isinstance(v,float) else v) for k,v in w.items()} for w in weeks])
# skipping all but 2008
A_no08,_=run([y for y in allY if y!=2008]); res['A_skip_all_but_2008']=float(A_no08.iloc[-1])
A_only08,_=run([2008]); res['A_skip_only_2008']=float(A_only08.iloc[-1])
for c in (0.001,0.002):
    a,_=run(allY,c); b,_=run([],c); res[f'fee_{c}']=(float(a.iloc[-1]),float(b.iloc[-1]))
# win rate of skipping (skip "wins" a year if the week fell)
res['skip_right']=int(sum(w['wk_skip']<0 for w in weeks))
# cumulative missed gain
res['sum_skip_pct']=float(np.prod([1+w['wk_skip'] for w in weeks])-1)
w08=[w for w in weeks if w['y']==2008][0]; res['w08']=w08
# 2008 Thanksgiving week rank among all SPY weeks
wk=C.resample('W-FRI').last().pct_change().dropna()
res['w08_rank']=int((wk>wk.loc['2008-11-28']).sum()+1); res['n_weeks']=len(wk); res['w08_week']=float(wk.loc['2008-11-28'])
# race at checkpoints
for dt in ['2007-12-31','2008-11-21','2008-12-31','2011-12-30','2015-12-31','2018-12-31','2020-12-31']:
    res['cp_'+dt]=(float(A[:dt].iloc[-1]),float(B[:dt].iloc[-1]))
pd.DataFrame({'A':A,'B':B,'IN':inA.astype(int)}).to_csv('sim38.csv')
json.dump(res,open('results38.json','w'),indent=1,default=float)
for k,v in res.items():
    if k!='weeks': print(k,v)
for w in weeks: print(w['y'],w['sell'],w['buy'],round(w['wk_cc']*100,2),round(w['wk_skip']*100,2))
