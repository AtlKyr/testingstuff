import pandas as pd,numpy as np
d=pd.read_csv('../spy.csv',parse_dates=['Date']).set_index('Date')
f=d['Adj Close']/d['Close']; O=(d.Open*f).values; C=d['Adj Close'].values; H=(d.High*f).values; L=(d.Low*f).values; idx=d.index; N=len(d)
def bt(entry, exitf, warm=200, cost=0.0005, name=''):
    cash=1e4; sh=0; inp=False; eq=np.zeros(N); pend=None; trades=[]; ent=0
    for i in range(N):
        if pend=='B' and not inp: sh=cash*(1-cost)/O[i]; cash=0; inp=True; ent=O[i]; ei=i
        elif pend=='S' and inp: cash=sh*O[i]*(1-cost); sh=0; inp=False; trades.append(O[i]/ent-1)
        pend=None
        eq[i]=sh*C[i] if inp else cash
        if i>=warm:
            if not inp and entry(i): pend='B'
            elif inp and exitf(i, ei): pend='S'
    bhs=1e4*(1-cost)/O[warm]*C; tr=np.array(trades)
    print(f"{name:28s} {eq[-1]:9.0f} bh {bhs[-1]:7.0f} trades {len(tr):4d} win {np.mean(tr>0)*100 if len(tr) else 0:4.1f}% tim {np.mean([1]):.0f} mdd {((eq/np.maximum.accumulate(eq))-1).min()*100:5.1f}")
    return eq
c=pd.Series(C); 
sma200=c.rolling(200).mean().values; sma5=c.rolling(5).mean().values
# RSI2
dlt=c.diff(); up=dlt.clip(lower=0).ewm(alpha=1/2).mean(); dn=(-dlt.clip(upper=0)).ewm(alpha=1/2).mean(); rsi2=(100-100/(1+up/dn)).values
# Double RSI: RSI2<10 & close>SMA200 ; exit RSI2>70 or 5 days
bt(lambda i: rsi2[i]<10 and C[i]>sma200[i], lambda i,ei: rsi2[i]>70 or i-ei>=4, name='DoubleRSI')
# inside bar breakout: today's high<prev high & low>prev low -> buy when close > inside bar high; exit close < inside low or after 10 days
ib=np.zeros(N,bool); ib[1:]=(H[1:]<H[:-1])&(L[1:]>L[:-1])
lastib=[None]
def ent_ib(i):
    # inside bar yesterday, today close above its high
    return ib[i-1] and C[i]>H[i-1]
bt(ent_ib, lambda i,ei: i-ei>=10, name='InsideBar up-break hold10')
# Williams %R 14: buy < -90, sell > -10
hh=pd.Series(H).rolling(14).max().values; ll=pd.Series(L).rolling(14).min().values; wr=-100*(hh-C)/(hh-ll)
bt(lambda i: wr[i]<-90, lambda i,ei: wr[i]>-10, warm=60, name='Williams%R 14 -90/-10')
bt(lambda i: wr[i]<-80, lambda i,ei: wr[i]>-20, warm=60, name='Williams%R 14 -80/-20')
# ATR breakout: close > prev close + 1*ATR14 -> buy; exit close < prev close - 1*ATR
tr_=np.maximum(H[1:]-L[1:],np.maximum(abs(H[1:]-C[:-1]),abs(L[1:]-C[:-1]))); atr=np.r_[np.nan,pd.Series(tr_).rolling(14).mean().values]
bt(lambda i: C[i]>C[i-1]+atr[i], lambda i,ei: C[i]<C[i-1]-atr[i], warm=60, name='ATR breakout 1x')
# Keltner / Donchian skip; NR7: narrowest range of 7 days, buy break above, hold 5
rng=H-L; nr7=np.zeros(N,bool); nr7[7:]=[rng[i]==rng[i-6:i+1].min() for i in range(7,N)]
bt(lambda i: nr7[i-1] and C[i]>H[i-1], lambda i,ei: i-ei>=5, warm=60, name='NR7 breakout hold5')
# 3-bar / "Turtle soup" skip ; Connors "3 lower lows" ...
