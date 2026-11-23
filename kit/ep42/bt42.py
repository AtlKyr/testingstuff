import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; Cs=d['Adj Close']; C=Cs.values; idx=d.index
s50=Cs.rolling(50).mean(); s200=Cs.rolling(200).mean()
above=(s50>s200).astype(float); above[s200.isna()]=np.nan
FEE=0.0005
W0=200
def run(hold=252, fee=FEE, rebuy='time'):
    sh=10000*(1-fee)/O[W0]; cash=0; out=False; back=None; tr=[]; eq=[]
    for i in range(W0,len(C)):
        if out and ((rebuy=='time' and i==back) or (rebuy=='golden' and i==back)):
            sh=cash*(1-fee)/O[i]; cash=0; out=False; tr[-1]+= [str(idx[i].date()), O[i]]
        if (not out) and i>W0 and above.iloc[i-1]==1 and above.iloc[i]==0 and i+1<len(C):
            # death cross at close i -> sell next open
            j=i+1; cash=sh*O[j]*(1-fee); sh=0; out=True; tr.append([str(idx[i].date()), str(idx[j].date()), O[j]])
            if rebuy=='time': back=j+hold
            else:
                k=j
                while k<len(C) and not (above.iloc[k-1]==0 and above.iloc[k]==1): k+=1
                back=k+1
            eq.append(sh*C[i]+cash); continue
        eq.append(sh*C[i]+cash)
    return pd.Series(eq,idx[W0:]), tr
bh=pd.Series(10000*(1-FEE)/O[W0]*C[W0:], idx[W0:])
if __name__=='__main__':
    print('start',idx[W0].date(),'BH',int(bh.iloc[-1]))
    for h in [21,63,126,252,504]: print(h,int(run(h)[0].iloc[-1]))
    print('golden',int(run(rebuy='golden')[0].iloc[-1]))
    eq,tr=run(252); print(int(eq.iloc[-1])); 
    for t in tr: print(t)
    df=pd.DataFrame({'s':eq,'b':bh}); print(df.resample('YE').last().astype(int).T.to_string())
    lead=eq>bh; print(lead.groupby(lead.index.year).mean().round(2).to_dict())
    R=dict(final=float(eq.iloc[-1]), bh=float(bh.iloc[-1]), trades=tr, n=len(tr), higher=sum(1 for x in tr if x[4]>x[2]),
           r07=float(tr[1][4]/tr[1][2]-1), r20=float([x for x in tr if x[0]=='2020-03-31'][0][4]/[x for x in tr if x[0]=='2020-03-31'][0][2]-1),
           scan={str(h):int(run(h)[0].iloc[-1]) for h in [21,63,126,504]}, golden=int(run(rebuy='golden')[0].iloc[-1]),
           fee10=float(run(252,0.001)[0].iloc[-1]), mdd=float((eq/eq.cummax()-1).min()), mdd_bh=float((bh/bh.cummax()-1).min()),
           crosses=[str(t.date()) for t in idx[W0:] if False])
    json.dump(R,open('results42.json','w'),indent=1,default=float)
    pd.DataFrame({'S':eq,'H':bh,'S50':s50[W0:],'S200':s200[W0:]}).to_csv('sim42.csv')
    print({k:v for k,v in R.items() if k!='trades'})
