# Autopsy #6 - MACD 12/26/9 crossover. Loop backtest: signal at close, fill next open, cost per side, cash 0%.
import pandas as pd, numpy as np, json, sys
df=pd.read_csv("spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; o=(df["Open"]*f).values; c=df["Adj Close"].values; idx=df.index
cl=df["Adj Close"]
macd=cl.ewm(span=12,adjust=False).mean()-cl.ewm(span=26,adjust=False).mean()
sig=macd.ewm(span=9,adjust=False).mean()
above=(macd>sig).values
WARM=78   # 3 x 26 bars warm-up excluded
def run(cost=0.0005, start=WARM, end=None):
    end=len(idx) if end is None else end
    cash=10000.0; sh=0.0; eq=[]; pos=[]; trades=[]; entry=None; fees=0.0
    for i in range(start,end):
        if i>start:
            j=i-1  # signal at prior close
            up = above[j] and not above[j-1]
            dn = (not above[j]) and above[j-1]
            if up and sh==0:
                fees+=cash*cost; sh=cash*(1-cost)/o[i]; cash=0; entry=(i,o[i])
            elif dn and sh>0:
                v=sh*o[i]; fees+=v*cost; cash=v*(1-cost); sh=0
                trades.append(dict(a=str(idx[entry[0]].date()),b=str(idx[i].date()),r=o[i]/entry[1]-1,d=i-entry[0]))
        eq.append(cash+sh*c[i]); pos.append(1 if sh>0 else 0)
    ii=idx[start:end]; eq=pd.Series(eq,index=ii); pos=pd.Series(pos,index=ii)
    y=(ii[-1]-ii[0]).days/365.25
    R=[t["r"] for t in trades]
    return dict(v=round(eq.iloc[-1]),cagr=round(100*((eq.iloc[-1]/10000)**(1/y)-1),2),dd=round(100*(eq/eq.cummax()-1).min(),1),
                tim=round(100*pos.mean(),1),trades=len(trades),win=round(100*np.mean([r>0 for r in R]),1),
                avg=round(100*np.mean(R),2),hold=round(np.mean([t["d"] for t in trades]),1),fees=round(fees)),eq,pos,trades
r,eq,pos,tr=run(); print("MACD",r, "open at end:",pos.iloc[-1])
s=WARM; bh=pd.Series(c[s:],index=idx[s:]); bh=10000*bh/o[s]*(1-0.0005)
bhr=dict(v=round(bh.iloc[-1]),dd=round(100*(bh/bh.cummax()-1).min(),1),cagr=round(100*((bh.iloc[-1]/10000)**(1/((idx[-1]-idx[s]).days/365.25))-1),2))
print("BH same dates from",idx[s].date(),bhr)
fees={p:run(p)[0]["v"] for p in (0.0005,0.001,0.002,0.0)}; print("fees",fees)
R=np.array([t["r"] for t in tr]); D=np.array([t["d"] for t in tr])
print("trades",len(R),"wins",(R>0).sum(),"losses",(R<=0).sum())
print("median hold",np.median(D),"<=5 days",(D<=5).sum(), "<=10 days",(D<=10).sum())
print("best trade",R.max(),"worst",R.min())
print("sum gain of winners vs losers",R[R>0].mean(),R[R<=0].mean())
# days in vs out: what did the market do while MACD was out?
oo=pd.Series(o,index=idx).pct_change().shift(-1).fillna(0).iloc[s:]
p=pos.reindex(oo.index)
print("mult in",(1+oo[p>0]).prod(),"mult out",(1+oo[p==0]).prod())
# top trades share
srt=np.sort(R)[::-1]; print("top5",srt[:5]); 
print("product all trades",np.prod(1+R*1), "without top 5",np.prod(1+srt[5:]))
# 2008 / 2020
for a,b in (("2007-10-09","2009-03-09"),("2020-02-19","2020-03-23"),("2022-01-03","2022-10-12")):
    print(a,b,"macd",round(100*(eq[b]/eq[a]-1),1),"bh",round(100*(bh[b]/bh[a]-1),1))
# yearly
ye=eq.resample("YE").last(); yb=bh.resample("YE").last()
yr=pd.DataFrame({"m":ye.pct_change(),"b":yb.pct_change()}); yr.iloc[0]=[ye.iloc[0]/10000-1,yb.iloc[0]/10000-1]
print((yr*100).round(1).to_string()); print("years macd beat bh",(yr.m>yr.b).sum(),"of",len(yr))
ddate=(eq/eq.cummax()-1).idxmin(); print("macd dd date",ddate.date(), "bh dd date",(bh/bh.cummax()-1).idxmin().date())
out=dict(start=str(idx[s].date()),sim=r,bh=bhr,fees={str(k):v for k,v in fees.items()},trades=len(R),wins=int((R>0).sum()),
         losses=int((R<=0).sum()),le5=int((D<=5).sum()),le10=int((D<=10).sum()),median_hold=float(np.median(D)),
         mult_in=round(float((1+oo[p>0]).prod()),2),mult_out=round(float((1+oo[p==0]).prod()),2),
         years=[dict(y=int(k.year),m=round(100*v.m,1),b=round(100*v.b,1)) for k,v in yr.iterrows()],
         trades_list=[dict(a=t["a"],b=t["b"],r=round(100*t["r"],2),d=t["d"]) for t in tr])
cr={}
for nm,(a,b) in dict(gfc=("2007-10-09","2009-03-09"),covid=("2020-02-19","2020-03-23"),y2022=("2022-01-03","2022-10-12")).items():
    cr[nm]=dict(m=round(100*(eq[b]/eq[a]-1),1),b=round(100*(bh[b]/bh[a]-1),1))
out["crashes"]=cr; out["cash_pct"]=round(100-r["tim"],1); out["beat_years"]=int((yr.m>yr.b).sum())
out["fee_profit_020"]=fees[0.002]-10000
json.dump(out,open("results6.json","w"),indent=1)
pd.DataFrame({"sim":eq,"bh":bh,"pos":pos,"close":c[s:],"macd":macd.values[s:],"sig":sig.values[s:]},index=idx[s:]).to_csv("sim6.csv")
