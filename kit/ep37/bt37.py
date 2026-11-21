# #37 2x S&P: simulated daily-reset 2x SPY fund (like SSO): daily return = 2*r_SPY(adj close-to-close) - borrow(3m T-bill on 1x notional)/252
# - expense 0.89%/yr /252. $10,000 bought at the first close 2005-01-03 (0.05% cost), held to 2024-12-31. vs 1x SPY bought same close.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date'); C=d['Adj Close']
tb=pd.read_csv('dtb3.csv',parse_dates=['observation_date']).set_index('observation_date')['DTB3']
tb=pd.to_numeric(tb,errors='coerce').reindex(d.index.union(tb.index)).ffill().reindex(d.index)/100
r=C.pct_change().fillna(0)
def lev(L=2,er=0.0089,borrow=True):
    dr=L*r-((L-1)*tb*borrow+er)/252; dr.iloc[0]=0
    return 10000*(1-0.0005)*(1+dr).cumprod()
one=10000*(1-0.0005)*C/C.iloc[0]
two=lev(); two_nofee=lev(er=0,borrow=False)
R=dict(one=float(one.iloc[-1]),two=float(two.iloc[-1]),two_nofee=float(two_nofee.iloc[-1]))
def mdd(s): return float((s/s.cummax()-1).min())
R.update(mdd_one=mdd(one),mdd_two=mdd(two))
R['two_low']=float(two.min()); R['two_low_date']=str(two.idxmin().date()); R['one_low']=float(one.min())
# when did 2x first get back above $10,000 after 2008 and above 1x?
lo=two.idxmin(); R['two_back10k']=str(two[lo:][two[lo:]>=10000].index[0].date())
ahead=(two>one); R['two_ahead_again']=str(ahead[lo:][ahead[lo:]].index[0].date())
R['years_behind']=None
# multiple of SPY total return vs 2x multiple
R['spy_mult']=float(C.iloc[-1]/C.iloc[0]); R['two_mult']=float(two.iloc[-1]/10000)
# 2008 year returns
for y in [2008,2009,2020,2022]:
    a=C[str(y)].iloc[-1]/C[:str(y-1)].iloc[-1]-1 if y>2005 else 0
    b=two[str(y)].iloc[-1]/two[:str(y-1)].iloc[-1]-1
    R[f'ret{y}']=(float(a),float(b))
# worst days
R['worst_day_1x']=float(r.min()); R['worst_day_2x']=float((2*r).min()); R['worst_day_date']=str(r.idxmin().date())
# full-period: days where 2x would need to double
R['3x']=float(lev(3).iloc[-1])
R['scan_start']={str(y):(round(float((lev()[str(y):]/lev()[str(y):].iloc[0]).iloc[-1]*1e4)),round(float((C[str(y):]/C[str(y):].iloc[0]).iloc[-1]*1e4))) for y in range(2005,2021,3)}
for y in range(2005,2025): R[f'y{y}']=(round(one[str(y)].iloc[-1]),round(two[str(y)].iloc[-1]))
json.dump(R,open('results37.json','w'),indent=1,default=str)
pd.DataFrame({'one':one,'two':two}).to_csv('sim37.csv')
for k,v in R.items(): print(k,v)
