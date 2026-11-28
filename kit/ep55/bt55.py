import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index; N=len(d)
RO=d.Open.values; RC=d.Close.values
per=idx.to_period('W-FRI'); last=np.r_[per[1:]!=per[:-1],True]
def run(dn=-0.05,up=0.05,cost=0.0005):
    cash=10000.;sh=0;inp=False;eq=np.zeros(N);IN=np.zeros(N,bool);pend=None;tr=[];prevw=None
    for i in range(N):
        if pend=='sell' and inp: cash=sh*O[i]*(1-cost);sh=0;inp=False;tr.append(['S',i])
        if pend=='buy' and not inp: sh=cash*(1-cost)/O[i];cash=0;inp=True;tr.append(['B',i])
        pend=None
        if i==0: sh=cash*(1-cost)/O[0];cash=0;inp=True
        eq[i]=sh*C[i] if inp else cash; IN[i]=inp
        if last[i]:
            if prevw is not None:
                r=C[i]/C[prevw]-1
                if inp and r<=dn: pend='sell'
                elif (not inp) and r>=up: pend='buy'
            prevw=i
    return eq,IN,tr
eq,IN,tr=run()
bh=10000*(1-0.0005)/O[0]*C
def mdd(x): return float((x/np.maximum.accumulate(x)-1).min())
R=dict(final=float(eq[-1]),bh=float(bh[-1]),mdd=mdd(eq),mdd_bh=mdd(bh),tim=float(IN.mean()),
       cagr=float((eq[-1]/1e4)**(252/N)-1),cagr_bh=float((bh[-1]/1e4)**(252/N)-1))
sells=[t[1] for t in tr if t[0]=='S']; buys=[t[1] for t in tr if t[0]=='B']
R['sells']=len(sells)
rt=[]
for s,b in zip(sells,buys):
    rt.append(dict(sell=str(idx[s].date()),buy=str(idx[b].date()),adj=round(O[b]/O[s]-1,4),raw=round(RO[b]/RO[s]-1,4),days=int(b-s),
                   cal_years=round((idx[b]-idx[s]).days/365.25,2)))
R['rt']=rt; R['higher']=int(sum(r['adj']>0 for r in rt))
R['weeks_up5']=int(sum(1 for i in np.where(last)[0][1:] if True))
# count all weeks
wi=np.where(last)[0]; wr=C[wi[1:]]/C[wi[:-1]]-1
R['n_up5']=int((wr>=0.05).sum()); R['n_dn5']=int((wr<=-0.05).sum())
# lead
ratio=eq/bh
for y in (2008,2009,2015,2016,2020):
    i=np.where(idx.year==y)[0][-1]; R[f'ratio_end{y}']=round(float(ratio[i]),3); R[f'eq_end{y}']=round(float(eq[i])); R[f'bh_end{y}']=round(float(bh[i]))
im=int(np.argmax(ratio)); R['maxlead']=dict(date=str(idx[im].date()),ratio=round(float(ratio[im]),3),eq=round(float(eq[im])),bh=round(float(bh[im])))
lead=np.where(ratio>1)[0]; R['last_lead']=str(idx[lead[-1]].date()) if len(lead) else None
# at the 2015 sale moment
s15=[s for s in sells if idx[s].year==2015][0]; b20=[b for b in buys if idx[b].year==2020][0]
R['at2015sale']=dict(eq=round(float(eq[s15])),bh=round(float(bh[s15])))
R['at2020buy']=dict(eq=round(float(eq[b20])),bh=round(float(bh[b20])))
R['wait_trading_days']=int(b20-s15)
R['scan']={f'{a}/{b}':round(float(run(a,b)[0][-1])) for a,b in [(-0.04,0.04),(-0.06,0.06),(-0.07,0.07),(-0.05,0.04),(-0.05,0.06),(-0.03,0.03)]}
R['fee0.10']=round(float(run(cost=0.001)[0][-1])); R['fee0']=round(float(run(cost=0)[0][-1]))
# without the 2015 trade: hold through
json.dump(R,open('results55.json','w'),indent=1,default=lambda o: o.item())
pd.DataFrame(dict(eq=eq,bh=bh,IN=IN.astype(int)),index=idx).to_csv('sim55.csv')
print(json.dumps({k:v for k,v in R.items() if k!='rt'},default=lambda o: o.item())); [print(r) for r in rt]
