# #56 3x S&P: simulated daily-reset 3x SPY fund (like UPRO): daily return = 3*r_SPY(adj close-to-close) - 2x T-bill borrowing/252
# - expense 0.91%/yr /252. $10,000 at the first close 2005-01-03 (0.05% cost), held to 2024-12-31, vs 1x SPY (same close). 2x for the footnote.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date'); C=d['Adj Close']; RC=d['Close']
tb=pd.read_csv('dtb3.csv',parse_dates=['observation_date']).set_index('observation_date')['DTB3']
tb=pd.to_numeric(tb,errors='coerce').reindex(d.index.union(tb.index)).ffill().reindex(d.index)/100
r=C.pct_change().fillna(0)
def lev(L,er):
    dr=L*r-((L-1)*tb+er)/252; dr.iloc[0]=0
    return 10000*(1-0.0005)*(1+dr).cumprod()
one=10000*(1-0.0005)*C/C.iloc[0]; two=lev(2,0.0089); three=lev(3,0.0091)
def yret(s,y): return float(s[str(y)].iloc[-1]/s[:str(y-1)].iloc[-1]-1)
R=dict(one=float(one.iloc[-1]),two=float(two.iloc[-1]),three=float(three.iloc[-1]),
       low3=float(three.min()),low3_date=str(three.idxmin().date()),low1=float(one.min()),
       mdd3=float((three/three.cummax()-1).min()),mdd1=float((one/one.cummax()-1).min()),
       r2008_3=yret(three,2008),r2008_1=yret(one,2008),r2011_3=yret(three,2011),r2011_1=yret(one,2011),
       r2011_raw=float(RC['2011'].iloc[-1]/RC['2010'].iloc[-1]-1),
       y2007_3=float(three['2007'].iloc[-1]),y2007_1=float(one['2007'].iloc[-1]),
       c20_3=float(three['2020-03-23']/three['2020-02-19']-1),c20_1=float(one['2020-03-23']/one['2020-02-19']-1))
lo=three.idxmin(); x=(three>one)[lo:]; first=x[x].index[0]; R['catch']=str(first.date()); R['catch_years']=(first-lo).days/365.25
R['three_nofee']=float((10000*(1-0.0005)*(1+3*r).cumprod()).iloc[-1])
# 3x vs 1x: every start year (honesty scan)
R['by_start']={str(y):(round(float(three[str(y):].iloc[-1]/three[:str(y-1)].iloc[-1]*1e4)) if y>2005 else round(R['three']),
                       round(float(one[str(y):].iloc[-1]/one[:str(y-1)].iloc[-1]*1e4)) if y>2005 else round(R['one'])) for y in range(2005,2021)}
R['start_wins']=sum(a>b for a,b in R['by_start'].values())
json.dump(R,open('results56.json','w'),indent=1)
pd.DataFrame({'eq':three,'bh':one,'two':two,'IN':1}).to_csv('sim56.csv')
for k,v in R.items(): print(k,v)
