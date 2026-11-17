# #29 Turnaround Tuesday: hold SPY only from Monday's close to Tuesday's close.
# A = Tuesdays after a RED Monday (Mon close < prior close); B = Tuesdays after a GREEN Monday. Fills at closes, 0.05%/side.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
C=d['Adj Close']; r=C.pct_change(); FEE=0.0005
dow=d.index.dayofweek
rows=[]
for i in range(2,len(d)):
    if dow[i]==1 and dow[i-1]==0:   # Tuesday right after a Monday trading day
        rows.append((d.index[i], r.iloc[i-1], r.iloc[i]))
T=pd.DataFrame(rows,columns=['date','mon','tue']).set_index('date')
red=T[T.mon<0]; green=T[T.mon>=0]
def grow(s): return 10000*np.prod((1+s.values)*(1-FEE)**2)
def path(s):
    eq=10000*np.cumprod((1+s.values)*(1-FEE)**2); return pd.Series(eq,s.index)
R=dict(n_tue=len(T),n_red=len(red),n_green=len(green),
 red_up=float((red.tue>0).mean()),green_up=float((green.tue>0).mean()),all_up=float((T.tue>0).mean()),
 red_avg=float(red.tue.mean()),green_avg=float(green.tue.mean()),
 red_final=grow(red.tue),green_final=grow(green.tue),red_final_nofee=10000*np.prod(1+red.tue.values),green_final_nofee=10000*np.prod(1+green.tue.values))
# big red Mondays <= -1%
big=T[T.mon<=-0.01]; R['n_big']=len(big); R['big_up']=float((big.tue>0).mean()); R['big_final']=grow(big.tue); R['big_avg']=float(big.tue.mean())
# dominance: top days in red set
top=red.tue.nlargest(5); R['red_top']={str(k.date()):round(v,4) for k,v in top.items()}
R['red_wo_top1']=grow(red.tue.drop(top.index[:1])); R['red_wo_top3']=grow(red.tue.drop(top.index[:3]))
gt=green.tue.nlargest(3); R['green_top']={str(k.date()):round(v,4) for k,v in gt.items()}
R['green_wo_top1']=grow(green.tue.drop(gt.index[:1]))
worst_red=red.tue.nsmallest(3); R['red_worst']={str(k.date()):round(v,4) for k,v in worst_red.items()}
# by year lead
pr,pg=path(red.tue),path(green.tue)
for y in [2007,2008,2009,2010,2012,2015,2018,2020,2022,2024]:
    R[f'y{y}']=(round(float(pr[:str(y)].iloc[-1])),round(float(pg[:str(y)].iloc[-1])))
# 2008 red tuesdays
r08=red.tue['2008']; R['r08_n']=len(r08); R['r08_growth']=float(np.prod(1+r08)-1)
bh=10000*C.iloc[-1]/C.iloc[0]; R['bh']=float(bh)
json.dump(R,open('results29.json','w'),indent=1,default=str)
pd.DataFrame({'red':pr}).join(pd.DataFrame({'green':pg}),how='outer').ffill().fillna(10000).to_csv('sim29.csv')
for k,v in R.items(): print(k,v)
