import pandas as pd, numpy as np
from scipy import stats
import statsmodels.api as sm
r=pd.read_csv('results/atlas_rows.csv.gz'); r=r[~r.study.str.startswith('TRAIN')]
for (d,m),g in r.groupby(['disease','model']):
    c=g.groupby('study').agg(n=('flag','size'),x=('flag','sum')); c=c[c.n>=15]; c['p']=c.x/c.n
    pbar=c.x.sum()/c.n.sum()
    # share outside band
    out=((c.p<0.05)|(c.p>0.15)).mean()
    # expected outside band under homogeneous p=0.10 and p=pbar
    def expout(p0):
        e=[]
        for n in c.n:
            k=np.arange(n+1); pk=stats.binom.pmf(k,n,p0); f=k/n
            e.append(pk[(f<0.05)|(f>0.15)].sum())
        return np.mean(e)
    # moment tau^2 on prop scale
    vobs=np.var(c.p,ddof=1); vexp=np.mean(pbar*(1-pbar)/c.n)
    # DL on logit with 0.5 correction
    y=np.log((c.x+.5)/(c.n-c.x+.5)); v=1/(c.x+.5)+1/(c.n-c.x+.5); w=1/v
    mu=(w*y).sum()/w.sum(); Q=(w*(y-mu)**2).sum(); k=len(c)
    tau2=max(0,(Q-(k-1))/(w.sum()-(w**2).sum()/w.sum()))
    # GLMM-ish: binomial w/ random intercept via 95% predictive interval on logit
    wr=1/(v+tau2); mur=(wr*y).sum()/wr.sum()
    lo,hi=[1/(1+np.exp(-(mur+s*1.96*np.sqrt(tau2)))) for s in (-1,1)]
    # restrict to n>=100
    big=c[c.n>=100]; outbig=((big.p<0.05)|(big.p>0.15)).mean()
    print(f"{d} {m}: k={k} pooled={pbar:.3f} outside={out:.2f} exp_out(p=.10)={expout(.10):.2f} exp_out(pbar)={expout(pbar):.2f} "
          f"varobs={vobs:.4f} varbinom={vexp:.4f} tau(logit)={np.sqrt(tau2):.2f} I2={max(0,(Q-(k-1))/Q):.2f} PI95=[{lo:.3f},{hi:.3f}] "
          f"n>=100: k={len(big)} out={outbig:.2f} range=[{big.p.min():.3f},{big.p.max():.3f}]  range_all=[{c.p.min():.2f},{c.p.max():.2f}] n_at_min={list(c.n[c.p==c.p.min()])} n_at_max={list(c.n[c.p==c.p.max()])}")
