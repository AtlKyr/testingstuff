# Autopsy #8 - Overnight vs intraday on SPY 2005-2024.
# NIGHT: buy at today's close (market-on-close), sell at next day's open.  DAY: buy at today's open, sell at today's close.
# Prices adjusted by Adj Close/Close (dividends included; an ex-dividend gap lands in the overnight return, which is correct).
# Costs 0.05% per side on every fill; cash 0%; $10,000 start; full compounding. Buy & hold: first open -> last adj close, one 0.05% fee.
import pandas as pd, numpy as np, json, sys
df=pd.read_csv(sys.argv[1] if len(sys.argv)>1 else "spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f); C=df["Adj Close"]; idx=df.index
night_r=(O/C.shift(1)-1).iloc[1:]          # close(t-1) -> open(t), one per day from day 2
day_r=(C/O-1)                               # open(t) -> close(t), every day
def path(r,cost):
    g=(1+r)*(1-cost)**2
    return 10000*g.cumprod()
res={}
for cost in (0.0,0.0001,0.0002,0.0005,0.001):
    n=path(night_r,cost); d=path(day_r,cost)
    res[str(cost)]=dict(night=round(n.iloc[-1]),day=round(d.iloc[-1]))
print("finals by cost per side:",res)
bh=10000*(1-0.0005)*C/O.iloc[0]
yrs=(idx[-1]-idx[0]).days/365.25
N=path(night_r,0.0005); D=path(day_r,0.0005); N0=path(night_r,0.0); D0=path(day_r,0.0)
def dd(s): return round(100*(s/s.cummax()-1).min(),1)
def cagr(v): return round(100*((v/10000)**(1/yrs)-1),2)
out=dict(start=str(idx[0].date()),end=str(idx[-1].date()),days=len(idx),
 bh=dict(v=round(bh.iloc[-1]),cagr=cagr(bh.iloc[-1]),dd=dd(bh)),
 night_fee=dict(v=round(N.iloc[-1]),cagr=cagr(N.iloc[-1]),dd=dd(N),trades=len(night_r)),
 day_fee=dict(v=round(D.iloc[-1]),cagr=cagr(D.iloc[-1]),dd=dd(D),trades=len(day_r)),
 night_nofee=dict(v=round(N0.iloc[-1]),cagr=cagr(N0.iloc[-1]),dd=dd(N0),mult=round(float((1+night_r).prod()),2)),
 day_nofee=dict(v=round(D0.iloc[-1]),cagr=cagr(D0.iloc[-1]),dd=dd(D0),mult=round(float((1+day_r).prod()),2)),
 fees_sweep=res)
# win rates (gross)
out["night_up_days"]=round(100*(night_r>0).mean(),1); out["day_up_days"]=round(100*(day_r>0).mean(),1)
# break-even cost per side where night final == $10,000
be=lambda r: (np.prod(1+r))**(1/(2*len(r)))-1
out["night_breakeven_cost_pct"]=round(100*be(night_r.values),4); out["day_breakeven_cost_pct"]=round(100*be(day_r.values),4)
# multiplicative check: night*day == bh gross?
out["check_night_x_day"]=round(float((1+night_r).prod()*(1+day_r).prod()),3); out["check_bh_gross"]=round(float(C.iloc[-1]/O.iloc[0]),3)
# yearly gross multipliers and fee-path year-end values
yr=pd.DataFrame({"n":(1+night_r).groupby(night_r.index.year).prod(),"d":(1+day_r).groupby(day_r.index.year).prod()})
out["years"]=[dict(y=int(k),n=round(100*(v.n-1),1),d=round(100*(v.d-1),1)) for k,v in yr.iterrows()]
out["years_night_beat_day"]=int((yr.n>yr.d).sum())
ye=pd.DataFrame({"N":N.resample("YE").last(),"D":D.resample("YE").last(),"N0":N0.resample("YE").last(),"D0":D0.resample("YE").last(),"B":bh.resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:int(v[c]) for c in ye.columns} for k,v in ye.iterrows()}
# crashes (gross, no fees) - where did the losses happen?
cr={}
for nm,(a,b) in dict(gfc=("2007-10-10","2009-03-09"),covid=("2020-02-20","2020-03-23"),y2022=("2022-01-04","2022-10-12")).items():
    m=(night_r.index>=a)&(night_r.index<=b); md=(day_r.index>=a)&(day_r.index<=b)
    cr[nm]=dict(night=round(100*((1+night_r[m]).prod()-1),1),day=round(100*((1+day_r[md]).prod()-1),1),bh=round(100*(C[b]/C.shift(1)[a]-1),1))
out["crashes_gross"]=cr
out["fees_paid_night"]=None
# fees paid by night trader (approx: sum of cost*equity per fill)
eqb=N.shift(1).fillna(10000); out["fees_paid_night"]=round(float((eqb*0.0005*2).sum()))
out["peak_night_fee"]=dict(v=round(N.max()),date=str(N.idxmax().date()))
out["peak_day_fee"]=dict(v=round(D.max()),date=str(D.idxmax().date()))
json.dump(out,open("results8.json","w"),indent=1)
pd.DataFrame({"N":N,"D":D,"N0":N0,"D0":D0,"B":bh}).to_csv("sim8.csv")
print(json.dumps({k:v for k,v in out.items() if k not in("years","year_end")},indent=1))
print(pd.DataFrame(out["years"]).to_string())
print(ye.to_string())
