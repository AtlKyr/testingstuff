import pandas as pd, numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date'); C=d['Adj Close']
tb=pd.read_csv('dtb3.csv',parse_dates=['observation_date']).set_index('observation_date')['DTB3']
tb=pd.to_numeric(tb,errors='coerce').reindex(d.index.union(tb.index)).ffill().reindex(d.index)/100
r=C.pct_change().fillna(0)
def lev(L,er):
    dr=L*r-((L-1)*tb+er)/252; dr.iloc[0]=0
    return 10000*(1-0.0005)*(1+dr).cumprod()
one=10000*(1-0.0005)*C/C.iloc[0]; two=lev(2,0.0089); three=lev(3,0.0091)
for nm,s in (('1x',one),('2x',two),('3x',three)):
    print(nm, round(s.iloc[-1]), 'low',round(s.min()),s.idxmin().date(), 'mdd',round((s/s.cummax()-1).min()*100,1))
for y in (2007,2008,2009,2010,2013,2015,2019,2020,2021,2022,2023,2024):
    print(y, round(one[str(y)].iloc[-1]),round(two[str(y)].iloc[-1]),round(three[str(y)].iloc[-1]))
# when 3x passes 2x / 1x for good
for a,b,n in ((three,one,'3>1'),(three,two,'3>2'),(two,one,'2>1')):
    lo=three.idxmin(); x=(a>b)[lo:]; print(n, x[~x].index[-1].date() if (~x).any() else None)
# flat years: index ~flat, 3x lost?
for y in range(2005,2025):
    a=C[str(y)].iloc[-1]/C[:str(y-1)].iloc[-1]-1 if y>2005 else C['2005'].iloc[-1]/C.iloc[0]-1
    b=three[str(y)].iloc[-1]/three[:str(y-1)].iloc[-1]-1 if y>2005 else three['2005'].iloc[-1]/three.iloc[0]-1
    print(y, round(a*100,1), round(b*100,1), round(3*a*100,1))
lo=three.idxmin()
x=(three>one)[lo:]; first=x[x].index[0]; print('first 3>1 after low', first.date())
y=(three<one)[first:]; print('falls behind again', y[y].index[0].date() if y.any() else None)
print('3x feb19-mar23 2020', round(three['2020-02-19']), round(three['2020-03-23']), round(three['2020-03-23']/three['2020-02-19']-1,3))
print('1x', round(one['2020-02-19']), round(one['2020-03-23']))
print('3x dec31 2007', round(three['2007-12-31']), 'mar9 2009', round(three['2009-03-09']))
print('3x peak 2007', round(three[:'2008'].max()), three[:'2008'].idxmax().date())
print('ret2011', round(C['2011'].iloc[-1]/C['2010'].iloc[-1]-1,4), round(three['2011'].iloc[-1]/three['2010'].iloc[-1]-1,4))
print('raw 2011', round(d.Close['2011'].iloc[-1]/d.Close['2010'].iloc[-1]-1,4))
