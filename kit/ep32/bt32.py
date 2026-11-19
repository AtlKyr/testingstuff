# #32 After the 5th straight red close (adj close < prior adj close), sell at next open, stay out 21 trading days, buy back at next open.
import pandas as pd, numpy as np, json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=d.Open*f; C=d['Adj Close']; r=C.pct_change()
red=(r<0).astype(int); st=red.groupby((red==0).cumsum()).cumsum()
FEE=0.0005; N=5; K=21
def run(N=N,K=K,fee=FEE):
    sh=10000*(1-fee)/O.iloc[0]; cash=0; eq=[];inm=[];tr=[];ps=False;pb=False;cnt=0
    for i in range(len(d)):
        if ps and sh>0: cash=sh*O.iloc[i]*(1-fee); sold=O.iloc[i]; sd=d.index[i]; sh=0; ps=False; cnt=0
        elif pb and sh==0: sh=cash*(1-fee)/O.iloc[i]; cash=0; tr.append((str(sd.date()),str(d.index[i].date()),O.iloc[i]/sold-1)); pb=False
        eq.append(sh*C.iloc[i]+cash); inm.append(sh>0)
        if i==len(d)-1: continue
        if sh>0 and st.iloc[i]==N: ps=True
        elif sh==0 and not ps:
            cnt+=1
            if cnt>=K: pb=True
    return pd.Series(eq,d.index),pd.Series(inm,d.index),tr
eq,inm,tr=run()
bh=10000*(1-FEE)*C/O.iloc[0]
def mdd(s): return float((s/s.cummax()-1).min())
yrs=(d.index[-1]-d.index[0]).days/365.25
ev=st[st==N].index; I=[d.index.get_loc(x) for x in ev]
day6=[r.iloc[k+1] for k in I if k+1<len(d)]            # close-to-close day six
day6o=[O.iloc[k+2]/O.iloc[k+1]-1 for k in I if k+2<len(d)]  # open-to-open
m1=[O.iloc[k+22]/O.iloc[k+1]-1 for k in I if k+22<len(d)]
R=dict(final=float(eq.iloc[-1]),bh=float(bh.iloc[-1]),cagr=(eq.iloc[-1]/1e4)**(1/yrs)-1,bh_cagr=(bh.iloc[-1]/1e4)**(1/yrs)-1,
 mdd=mdd(eq),bh_mdd=mdd(bh),tim=float(inm.mean()),trades=len(tr),higher=sum(1 for t in tr if t[2]>0),
 n_streaks=len(ev),day6_red=int(sum(x<0 for x in day6)),day6_n=len(day6),day6o_red=int(sum(x<0 for x in day6o)),
 m1_up=int(sum(x>0 for x in m1)),m1_n=len(m1),m1_avg=float(np.mean(m1)),
 base_m1_avg=float((O.shift(-21)/O-1).mean()),base_red=float((r<0).mean()))
R['day6_list']=[float(x) for x in day6]
R['scan']={str(k):round(float(run(N,k)[0].iloc[-1])) for k in [5,10,21,42,63]}
R['scanN']={str(n):round(float(run(n,K)[0].iloc[-1])) for n in [4,5,6]}
R['fees']={str(fe):round(float(run(N,K,fe)[0].iloc[-1])) for fe in [0,0.001,0.002]}
R['per_year']=pd.Series([t[0][:4] for t in tr]).value_counts().sort_index().to_dict()
lead=(eq-bh); R['max_lead']=float(lead.max()); R['max_lead_date']=str(lead.idxmax().date())
R['last_ahead']=str(lead[lead>0].index[-1].date()) if (lead>0).any() else None
for y in range(2005,2025): R[f'y{y}']=(round(eq[str(y)].iloc[-1]),round(bh[str(y)].iloc[-1]))
R['trades_list']=tr; R['events']=[str(x.date()) for x in ev]
json.dump(R,open('results32.json','w'),indent=1,default=str)
pd.DataFrame({'eq':eq,'bh':bh,'inm':inm,'r':r,'st':st}).to_csv('sim32.csv')
for k,v in R.items():
    if k not in('trades_list','events','day6_list'): print(k,v)
