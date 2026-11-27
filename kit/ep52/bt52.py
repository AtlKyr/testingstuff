import pandas as pd,numpy as np,json
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']
O=(d.Open*f).values;L=(d.Low*f).values;C=d['Adj Close'].values;pc=np.r_[np.nan,C[:-1]]
rawO=d.Open.values; rawpc=np.r_[np.nan,d.Close.values[:-1]]
idx=d.index; cost=0.0005; TH=0.02
def run(th,cost=0.0005):
    sh=10000*(1-cost)/O[0]; cash=0.; inpos=True; ev=[]; eq=np.zeros(len(C)); IN=np.ones(len(C),bool)
    for i in range(len(C)):
        if i>0 and not inpos:
            sh=cash*(1-cost)/O[i]; ev[-1]['buy_i']=i; ev[-1]['buy_px']=O[i]; cash=0; inpos=True
        if i>0 and inpos and L[i]<=pc[i]*(1-th):
            px=min(O[i],pc[i]*(1-th)); cash=sh*px*(1-cost); sh=0; inpos=False
            ev.append(dict(i=i,date=str(idx[i].date()),sell_px=px,gap=O[i]<=pc[i]*(1-th),close_ret=C[i]/pc[i]-1))
            IN[i]=False
        eq[i]=sh*C[i] if inpos else cash
    return eq,ev,IN
eq,ev,IN=run(TH)
bh=10000*(1-cost)/O[0]*C
res=dict(final=float(eq[-1]),bh=float(bh[-1]),sells=len(ev))
up=[e for e in ev if 'buy_px' in e and e['buy_px']>e['sell_px']]
res['rebought_higher']=len(up)
res['closed_green']=int(sum(e['close_ret']>0 for e in ev))
res['closed_below_th']=int(sum(e['close_ret']<=-TH for e in ev))
res['gap_sells']=int(sum(bool(e['gap']) for e in ev))
# avg cost per round trip: buy_px/sell_px-1
g=np.array([e['buy_px']/e['sell_px']-1 for e in ev if 'buy_px' in e])
res['avg_rt']=float(g.mean()); res['med_rt']=float(np.median(g))
def mdd(x): return float((x/np.maximum.accumulate(x)-1).min())
res['mdd']=mdd(eq); res['mdd_bh']=mdd(bh)
yrs=(idx[-1]-idx[0]).days/365.25
res['cagr']=(eq[-1]/1e4)**(1/yrs)-1; res['cagr_bh']=(bh[-1]/1e4)**(1/yrs)-1
for th in (0.015,0.02,0.025,0.03,0.04): res[f'th{th}']=float(run(th)[0][-1])
for c in (0.001,0.002): res[f'fee{c}']=float(run(TH,c)[0][-1])
# year counts
ys=pd.Series([e['date'][:4] for e in ev]).value_counts().sort_index(); res['by_year']=ys.to_dict()
# biggest missed rebound
ev2=sorted([e for e in ev if 'buy_px' in e],key=lambda e:-(e['buy_px']/e['sell_px']))
res['top_cost']=[(e['date'],round(e['buy_px']/e['sell_px']-1,4),round(e['close_ret'],4)) for e in ev2[:8]]
# raw price check for top
# race lead: when did strategy fall behind for good
json.dump(res,open('results52.json','w'),indent=1,default=str)
pd.DataFrame(dict(eq=eq,bh=bh,IN=IN),index=idx).to_csv('sim52.csv')
pd.DataFrame(ev).to_csv('events52.csv',index=False)
print(json.dumps(res,indent=1,default=str))
