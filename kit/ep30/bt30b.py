import pandas as pd, numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; idx=d.index
FEE=0.0005; AMT=1000
def run(N, mode):
    n=len(C); up=np.r_[False, C[1:]>C[:-1]]; dn=np.r_[False, C[1:]<C[:-1]]
    streak=0; shK=shW=0; wait=None; ref=None; pend=[]; ev=0; hi=0; kopen=None; ups=0; delays=[]
    for i in range(n):
        for (j,who) in list(pend):
            if j==i:
                if who=='K': shK+=AMT*(1-FEE)/O[i]; kopen=O[i]; ki=i
                else: shW+=AMT*(1-FEE)/O[i]; hi+= O[i]>kp; delays.append(i-ki)
                pend.remove((j,who))
        if dn[i]: streak+=1
        elif up[i]: streak=0
        if dn[i] and streak==N and i+1<n and wait is None:
            pend.append((i+1,'K')); wait=i; ref=C[i-N]; ups=0; ev+=1
        elif wait is not None and i>wait and i+1<n:
            if up[i]: ups+=1
            ok = (mode=='green' and up[i]) or (mode=='2green' and ups>=2) or (mode=='recover' and C[i]>=ref)
            if ok: kp=kopen; pend.append((i+1,'W')); wait=None
    return ev, round(shK*C[-1]), round(shW*C[-1]), hi, np.mean(delays), max(delays)
for mode in ['green','2green','recover']:
    for N in [3,4,5]:
        print(mode,N,run(N,mode))
