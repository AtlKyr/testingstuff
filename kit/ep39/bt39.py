# #39 Dividends: pocket the checks (spend/keep as cash, 0%) vs reinvest. SPY 2005-2024, $10,000 at the first open.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
C=d['Close']; A=d['Adj Close']; Or=d['Open']; f=A/C; idx=d.index; COST=0.0005
ratio=f/f.shift(1)
ex0=ratio[ratio>1+1e-6].index
DD=pd.Series({t: C.shift(1)[t]*(1-f.shift(1)[t]/f[t]) for t in ex0}); ex=DD[DD>0.05].index
D=pd.Series({t: C.shift(1)[t]*(1-f.shift(1)[t]/f[t]) for t in ex})
N=10000*(1-COST)/Or.iloc[0]
# Spender: N shares forever, checks in a jar
checks=N*D
jar=checks.reindex(idx).fillna(0).cumsum()
P=N*C+jar
# Reinvestor: reinvest each check at that day's close with 0.05% cost
sh=N; R=[]
for t in idx:
    if t in D.index: sh+=sh*D[t]*(1-COST)/C[t]
    R.append(sh*C[t])
R=pd.Series(R,idx)
res=dict(n_div=len(D), first_ex=str(ex[0].date()), last_ex=str(ex[-1].date()), D_first=float(D.iloc[0]), D_last=float(D.iloc[-1]),
 spender_total=float(P.iloc[-1]), spender_shares_value=float(N*C.iloc[-1]), checks_total=float(checks.sum()),
 reinvest=float(R.iloc[-1]), bh_adj=float(10000*(1-COST)*A.iloc[-1]/(Or.iloc[0]*f.iloc[0])),
 shares_start=float(N), shares_end_reinvest=float(sh))
res['gap']=res['reinvest']-res['spender_total']
# checks by year
yr=checks.groupby(checks.index.year).sum(); res['checks_by_year']={int(k):round(float(v),2) for k,v in yr.items()}
# what the 2008-2009 checks became if reinvested: value at end of reinvested shares bought with 2008-09 checks
sh2=0; extra={}
for t in D.index:
    pass
# value at the end of each check reinvested (simple: check * C_end/C_t * later-div growth via adj): check*(A_end/A_t)
grow=pd.Series({t: float(checks[t]*(A.iloc[-1]/A[t])) for t in D.index})
res['grown_by_year']={int(k):round(float(v),1) for k,v in grow.groupby(grow.index.year).sum().items()}
res['grow_0809']=float(grow[(grow.index>='2008-09-01')&(grow.index<='2009-12-31')].sum())
res['checks_0809']=float(checks[(checks.index>='2008-09-01')&(checks.index<='2009-12-31')].sum())
m=grow.idxmax(); res['best_check']=(str(m.date()),float(checks[m]),float(grow[m]))
# race checkpoints: who's ahead, gap
for dt in ['2007-12-31','2009-03-09','2012-12-31','2016-12-30','2020-12-31','2024-12-31']:
    res['cp_'+dt]=(float(P[:dt].iloc[-1]),float(R[:dt].iloc[-1]))
def mdd(s): return float((s/s.cummax()-1).min())
res['mdd_spender']=mdd(P); res['mdd_reinvest']=mdd(R)
# jar share of spender wealth at end
res['jar_pct']=float(jar.iloc[-1]/P.iloc[-1])
# yield-on-cost: last year's checks vs first year
res['checks_2005']=float(yr.loc[2005]); res['checks_2024']=float(yr.loc[2024])
# reinvestor's 2024 dividend income
inc=[]; sh=N
for t in idx:
    if t in D.index:
        c=sh*D[t]; inc.append((t,c)); sh+=c*(1-COST)/C[t]
inc=pd.Series(dict(inc)); res['reinv_checks_2024']=float(inc[inc.index.year==2024].sum())
pd.DataFrame({'P':P,'R':R,'JAR':jar}).to_csv('sim39.csv')
json.dump(res,open('results39.json','w'),indent=1,default=float)
for k,v in res.items(): print(k,v)
