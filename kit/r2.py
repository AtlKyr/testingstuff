import pandas as pd, numpy as np, json
df=pd.read_csv("spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; px=pd.DataFrame({"open":df["Open"]*f,"close":df["Adj Close"]})
oo=px.open.pct_change().shift(-1).fillna(0)
yrs=(px.index[-1]-px.index[0]).days/365.25
def rsi(c,n):
    d=c.diff(); up=d.clip(lower=0).ewm(alpha=1/n,adjust=False).mean(); dn=(-d.clip(upper=0)).ewm(alpha=1/n,adjust=False).mean()
    return 100-100/(1+up/dn)
r2=rsi(px.close,2); s200=px.close.rolling(200).mean(); s5=px.close.rolling(5).mean()
def run(sig,cost=0.0005,idx=None):
    pos=sig.ffill().fillna(0).shift(1).fillna(0)
    tr=pos.diff().abs().fillna(0)
    ret=pos*oo-tr*cost
    if idx is not None: ret=ret.loc[idx]; pos=pos.loc[idx]; tr=tr.loc[idx]
    eq=(1+ret).cumprod()
    y=(eq.index[-1]-eq.index[0]).days/365.25
    return dict(v=round(10000*eq.iloc[-1]),cagr=round(100*(eq.iloc[-1]**(1/y)-1),2),dd=round(100*(eq/eq.cummax()-1).min(),1),tim=round(100*pos.mean(),1),rt=int(tr.sum()//2)),eq,pos
bh=px.close/px.close.iloc[0]
print("BH",round(10000*bh.iloc[-1]), round(100*(bh/bh.cummax()-1).min(),1))
# plain RSI2 30/70
s=pd.Series(np.nan,index=px.index); s[r2<30]=1; s[r2>70]=0; s.iloc[:60]=np.nan
print("RSI2 30/70",run(s)[0])
# Connors: close>SMA200 & RSI2<10 -> buy; exit close>SMA5
c=pd.Series(np.nan,index=px.index); c[(px.close>s200)&(r2<10)]=1; c[px.close>s5]=0; c[s200.isna()]=np.nan
# need: entry dominates? set exit only when in position: use loop
pos=np.zeros(len(px)); inpos=0
for i in range(len(px)):
    if np.isnan(s200.iloc[i]): pos[i]=0; continue
    if not inpos and px.close.iloc[i]>s200.iloc[i] and r2.iloc[i]<10: inpos=1
    elif inpos and px.close.iloc[i]>s5.iloc[i]: inpos=0
    pos[i]=inpos
cs=pd.Series(pos,index=px.index)
res,eqc,posc=run(cs); print("Connors",res)
for cost in (0.001,0.002): print(" cost",cost,run(cs,cost)[0])
# return per day in market
for nm,sig in (("rsi2",s),("conn",cs)):
    r,eq,p=run(sig); daily=(eq.pct_change().fillna(0)); inm=p>0
    print(nm,"avg daily ret when in mkt %",round(100*((1+oo[p.shift(0)>0]).prod()**(1/inm.sum())-1),4))
print("bh avg daily %",round(100*((bh.iloc[-1])**(1/len(bh))-1),4))
# trades stats connors
d=cs.diff().fillna(0); entries=list(px.index[d>0]); exits=list(px.index[d<0])
print("trades",len(entries))
# win rate
w=0;rets=[]
for e in entries:
    xs=[x for x in exits if x>e]
    if not xs: continue
    x=xs[0]; i0=px.index.get_loc(e)+1; i1=px.index.get_loc(x)+1
    if i1>=len(px): continue
    rr=px.open.iloc[i1]/px.open.iloc[i0]-1; rets.append(rr)
rets=np.array(rets); print("win rate",round((rets>0).mean()*100,1),"avg trade %",round(rets.mean()*100,2),"avg days", None)
pd.DataFrame({"conn":eqc*10000,"bh":bh*10000,"pos":posc,"close":px.close,"r2":r2,"s200":s200,"s5":s5}).to_csv("conn.csv")
