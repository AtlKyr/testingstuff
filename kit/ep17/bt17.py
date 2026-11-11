# Autopsy #17 - "Is 2007 happening again?" Two investors put $10,000 into SPY at the 2007 top: bought at the OPEN the day after the
# record close of 2007-10-09. HOLDER keeps it. PANIC SELLER sells at the next open after a close >=40% below his buy price (adj),
# buys back at the next open after SPY closes at a new nominal record (above the 2007-10-09 close). 0.05%/side, cash 0%.
import pandas as pd, numpy as np, json
df=pd.read_csv("../spy.csv",parse_dates=["Date"]).set_index("Date").sort_index()
f=df["Adj Close"]/df["Close"]; O=(df["Open"]*f).values; C=df["Adj Close"].values; P=df["Close"].values; PO=df["Open"].values; idx=df.index; N=len(C)
FEE=0.0005; pk=idx.get_loc(pd.Timestamp("2007-10-09")); b=pk+1
assert P[pk]==P[:pk+1].max()
out={"peak_close":round(float(P[pk]),2),"buy_date":str(idx[b].date()),"buy_open_nominal":round(float(PO[b]),2)}
hold=np.full(N,np.nan); sh=10000*(1-FEE)/O[b]; hold[b:]=sh*C[b:]
out["holder"]=round(float(hold[-1]))
# break-even (holder value >= 10000 at close) total return, and price-only
lo0=b+int(np.nanargmin(hold[b:])); be=lo0+int(np.argmax(hold[lo0:]>=10000)); out["be_total"]=str(idx[be].date())
pv=10000*(1-FEE)/PO[b]*P; lp=b+int(np.argmin(pv[b:])); bp=lp+int(np.argmax(pv[lp:]>=10000)); out["be_price"]=str(idx[bp].date())
out["be_total_months"]=round((idx[be]-idx[b]).days/30.44,1); out["be_price_months"]=round((idx[bp]-idx[b]).days/30.44,1)
lo=b+int(np.argmin(hold[b:])); out["low"]=(str(idx[lo].date()),round(float(hold[lo])),round(100*(hold[lo]/10000-1),1))
def panic(thr=0.40,fee=FEE):
    cash=0.0; s=10000*(1-fee)/O[b]; eq=np.full(N,np.nan); st=0; log=[]
    for i in range(b,N):
        if i>b:
            if st==0 and s>0 and C[i-1]<=O[b]*(1-thr): cash=s*O[i]*(1-fee); s=0.0; st=1; log.append(("sell",str(idx[i].date()),round(cash)))
            elif st==1 and P[i-1]>P[pk]: s=cash*(1-fee)/O[i]; cash=0.0; st=2; log.append(("buy",str(idx[i].date()),round(s*O[i])))
        eq[i]=cash+s*C[i]
    return eq,log
eq,log=panic(); out["panic"]=round(float(eq[-1])); out["panic_log"]=log
out["panic_thr"]={t:round(float(panic(thr=t)[0][-1])) for t in (0.2,0.3,0.4,0.5)}
out["panic_fee0"]=round(float(panic(fee=0)[0][-1]))
i_s=idx.get_loc(pd.Timestamp(log[0][1])); i_b=idx.get_loc(pd.Timestamp(log[1][1]))
out["missed_gain_pct"]=round(100*(O[i_b]/O[i_s]-1),1); out["months_out"]=round((idx[i_b]-idx[i_s]).days/30.44,1)
# what the 2009 low -> rebuy did
out["holder_at_rebuy"]=round(float(hold[i_b])); out["holder_at_sell"]=round(float(hold[i_s]))
out["drawdown_pct_of_buy_at_sell"]=round(100*(O[i_s]/O[b]-1),1)
# buy & hold full period for reference
bh=10000*(1-FEE)/O[0]*C; out["bh_2005"]=round(float(bh[-1]))
ye=pd.DataFrame({"H":pd.Series(hold,idx).resample("YE").last(),"P":pd.Series(eq,idx).resample("YE").last()}).round(0)
out["year_end"]={str(k.year):{c:(None if np.isnan(v[c]) else int(v[c])) for c in ye.columns} for k,v in ye.iterrows()}
# check: holder independently
out["check_holder"]=round(10000*(1-FEE)*C[-1]/O[b])
json.dump(out,open("results17.json","w"),indent=1,default=float)
pd.DataFrame({"H":hold,"P":eq,"C":C},index=idx).to_csv("sim17.csv")
print(json.dumps({k:v for k,v in out.items() if k!="year_end"},default=float)); print(ye.T.to_string())
