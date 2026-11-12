# Autopsy #19 - "$500 a month since 2005: when did you hit $100K?" Buy $500 of SPY at the OPEN of the first trading day of every
# month from Jan 2005, 0.05% fee, dividends reinvested (adjusted prices), cash 0. Value marked at the adjusted close.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; idx=df.index; N=len(C); FEE=0.0005; AMT=500
first=pd.Series(np.arange(N),idx).groupby(idx.to_period("M")).first().values
def run(amt=AMT,fee=FEE,start=0):
    sh=0.0; inv=0.0; val=np.zeros(N); invs=np.zeros(N); fs=set(first[first>=start])
    for i in range(start,N):
        if i in fs: sh+=amt*(1-fee)/O[i]; inv+=amt
        val[i]=sh*C[i]; invs[i]=inv
    return val,invs
val,inv=run()
out={}
def hit(v,x): j=np.argmax(v>=x); return (str(idx[j].date()),round(float(inv[j]))) if v.max()>=x else None
for x in (25000,50000,100000,200000,300000): out[f"hit_{x}"]=hit(val,x)
out["final"]=round(float(val[-1])); out["invested"]=round(float(inv[-1]))
# years from start to 100K
j=np.argmax(val>=100000); out["years_to_100k"]=round((idx[j]-idx[0]).days/365.25,2)
# the 2008 trap: max gap below invested and the date value got back above invested for good
gap=val-inv; k=int(np.argmin(gap)); out["worst_gap"]=(str(idx[k].date()),round(float(val[k])),round(float(inv[k])),round(float(gap[k])))
under=np.where(gap<0)[0]; out["last_under"]=str(idx[under[-1]].date()) if len(under) else None
# first time crossing 100K and did it fall back below after? (2020, 2022)
above=val>=100000; back=np.where((~above)&(np.arange(N)>j))[0]; out["fell_back_below_100k"]=[str(idx[back[0]].date()),str(idx[back[-1]].date())] if len(back) else None
# 2008: value at 2007-10 peak vs 2009-03 low
for d in ("2007-10-09","2009-03-09","2013-03-28","2020-02-19","2020-03-23"):
    i=idx.get_loc(pd.Timestamp(d)); out["v_"+d]=[round(float(val[i])),round(float(inv[i]))]
# when did value first exceed invested by 2x
r2=np.where((val>=2*inv)&(inv>0))[0]; out["double_first"]=str(idx[r2[0]].date()) if len(r2) else None
# without 2008-09 crash? n/a. Fee stress
out["fee0_final"]=round(float(run(fee=0)[0][-1]))
# time split: share of the final from 2005-2014 vs after
i14=idx.get_loc(idx[idx.year==2014][-1]); out["v_end2014"]=[round(float(val[i14])),round(float(inv[i14]))]
i19=idx.get_loc(idx[idx.year==2019][-1]); out["v_end2019"]=[round(float(val[i19])),round(float(inv[i19]))]
# months to go from 100K to 200K, 200K to 300K
out["months_0_100k"]=round((pd.Timestamp(out["hit_100000"][0])-idx[0]).days/30.44); 
out["months_100_200k"]=round((pd.Timestamp(out["hit_200000"][0])-pd.Timestamp(out["hit_100000"][0])).days/30.44)
out["months_200_300k"]=round((pd.Timestamp(out["hit_300000"][0])-pd.Timestamp(out["hit_200000"][0])).days/30.44) if out["hit_300000"] else None
# independent check: vectorised
fs=first; sh=(AMT*(1-FEE)/O[fs]).sum(); out["check_final"]=round(float(sh*C[-1]))
ye=pd.DataFrame({"V":pd.Series(val,idx).resample("YE").last(),"I":pd.Series(inv,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):[int(v.V),int(v.I)] for k,v in ye.iterrows()}
json.dump(out,open("results19.json","w"),indent=1,default=float)
pd.DataFrame({"V":val,"I":inv},index=idx).to_csv("sim19.csv")
print(json.dumps(out,default=float))
