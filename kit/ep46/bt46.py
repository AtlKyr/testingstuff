import pandas as pd, numpy as np, json, sys
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
r=d['Adj Close']/d['Close']; O=(d['Open']*r).values; C=d['Adj Close'].values; NC=d['Close'].values
dates=d.index; N=len(d); FEE=0.0005
def milestones(step=50):
    ev=[]; 
    for lvl in range(100,700,step):
        idx=np.where(NC>=lvl)[0]
        if len(idx) and idx[0]>0: ev.append((lvl,idx[0]))
    return ev
def run(hold=63, step=50, fee=FEE):
    ev=milestones(step); sells={i+1:lvl for lvl,i in ev}
    cash=10000.0; sh=0.0; inm=True
    sh=cash*(1-fee)/O[0]; cash=0
    back=None; eq=np.zeros(N); trades=[]; inmk=np.ones(N,bool)
    for t in range(N):
        if inm and t in sells:
            cash=sh*O[t]*(1-fee); sh=0; inm=False; back=t+hold; trades.append(dict(lvl=sells[t],sell=str(dates[t].date()),sp=O[t]))
        elif (not inm) and t==back:
            sh=cash*(1-fee)/O[t]; cash=0; inm=True; trades[-1].update(buy=str(dates[t].date()),bp=O[t])
        # re-trigger while out: ignore
        eq[t]=sh*C[t]+cash; inmk[t]=inm
    return eq,trades,inmk
bh=10000*(1-FEE)/O[0]*C
if __name__=='__main__':
    eq,tr,inm=run()
    print('final',round(eq[-1]),'bh',round(bh[-1]),'time in mkt',inm.mean())
    for x in tr: print(x['lvl'],x['sell'],round(x['sp'],2),x.get('buy'),round(x.get('bp',0),2), 'cheaper' if x.get('bp',1e9)<x['sp'] else 'HIGHER')
    for h in [5,10,21,42,63,126,252]:
        e,_,_=run(h); print('hold',h,round(e[-1]))
    for st in [25,100]:
        e,t2,_=run(63,st); print('step',st,len(t2),round(e[-1]))
    dd=lambda e:(e/np.maximum.accumulate(e)-1).min()
    print('dd',dd(eq),dd(bh))

def save():
    eq,tr,inm=run()
    pd.DataFrame({'H':bh,'S':eq,'INM':inm.astype(int)},index=dates).to_csv('sim46.csv')
    var={h:round(run(h)[0][-1]) for h in [5,10,21,42,63,126,252]}
    fees={f:round(run(fee=f)[0][-1]) for f in [0.001,0.002]}
    dd=lambda e:float((e/np.maximum.accumulate(e)-1).min())
    json.dump(dict(final=float(eq[-1]),bh=float(bh[-1]),trades=tr,var=var,fees=fees,inm=float(inm.mean()),dd=dd(eq),bhdd=dd(bh)),open('results46.json','w'),indent=1,default=float)
if __name__=='__main__': save()
