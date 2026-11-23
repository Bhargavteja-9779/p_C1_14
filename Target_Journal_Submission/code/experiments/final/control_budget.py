"""POST-HOC (review round 1). How many labelled local controls? Under exchangeability, the conformal threshold
(k = ceil((n+1)(1-alpha))-th smallest of n controls) gives realised FPR ~ Beta(n+1-k, k). Theory vs empirical check on
the cohorts with >= 200 calibration-pool controls is not possible for n=200, so the check uses the large cohorts
(MetaCardis 642, Yachida 251, QinJ 174 controls): calibration n drawn from one half, FPR on the other half."""
import os, glob, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); alpha = 0.10; out = []; rng = np.random.default_rng(3)
rows = []
for n in [9, 19, 29, 49, 99, 199, 299]:
    k = int(np.ceil((n + 1) * (1 - alpha))); b = stats.beta(n + 1 - k, k)
    rows.append(dict(n=n, mean_FPR=b.mean(), q025=b.ppf(.025), q975=b.ppf(.975), P_gt_015=b.sf(0.15), P_in_005_015=b.cdf(0.15) - b.cdf(0.05)))
T = pd.DataFrame(rows); out += ["Theory (alpha=0.10, exchangeable local controls):", T.round(3).to_string(index=False)]
emp = []
for f in glob.glob(os.path.join(HERE, "scores", "T2D_MetaCardis*.npz")) + glob.glob(os.path.join(HERE, "scores", "CRC_YachidaS*.npz")) + glob.glob(os.path.join(HERE, "scores", "T2D_QinJ*.npz")):
    z = np.load(f); st, yt = z["st"], z["yt"]; i0 = np.where(yt == 0)[0]
    for n in [19, 49, 79]:
        if n > len(i0) // 2: continue
        k = int(np.ceil((n + 1) * (1 - alpha))); fp = []
        for r in range(500):
            p = rng.permutation(i0); c = np.sort(st[p[:n]]); fp.append(np.mean(st[p[len(p) // 2:]] >= c[k - 1]))
        fp = np.array(fp); emp.append(dict(file=os.path.basename(f)[:-4], n=n, mean_FPR=fp.mean(), q025=np.quantile(fp, .025), q975=np.quantile(fp, .975), P_gt_015=(fp > 0.15).mean()))
pd.DataFrame(emp).to_csv(os.path.join(HERE, "control_budget_emp.csv"), index=False)
out += ["\nEmpirical (large cohorts; includes evaluation-half sampling noise):", pd.DataFrame(emp).round(3).to_string(index=False)]
txt = "\n".join(out); open(os.path.join(HERE, "control_budget.txt"), "w").write(txt); print(txt)
