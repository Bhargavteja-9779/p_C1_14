"""POST HOC, descriptive (cycle 5): if a site verified the stated FPR (0.10) on n local healthy people with fprcal's exact
one-sided binomial test (H0: FPR <= 0.15, level 0.05), how often would it detect the over-flagging seen in the atlas?
Each strict population's observed FPR is treated as its true FPR. Writes results/verify_power_v5.csv/json."""
import os, json, numpy as np, pandas as pd
from scipy import stats
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
p = pd.read_csv(os.path.join(OUT, "v5_perpop_strict.csv")); rows = []
def crit(n, p0=.15, lv=.05):  # smallest k with P(X>=k | p0) < lv
    k = np.arange(n + 2); return int(k[stats.binom.sf(k - 1, n, p0) < lv][0])
for n in [25, 50, 100, 200]:
    c = crit(n)
    for m in ["lasso", "rf"]:
        d = p[p.model == m]; over = d[d.fpr > .15]; very = d[d.fpr > .25]
        pw = stats.binom.sf(c - 1, n, over.fpr.values); pv = stats.binom.sf(c - 1, n, very.fpr.values)
        fa = stats.binom.sf(c - 1, n, np.clip(d[d.fpr <= .15].fpr.values, 0, 1))
        rows.append(dict(n=n, model=m, k_crit=c, units=len(d), units_over015=len(over), mean_power_over015=float(pw.mean()),
                         units_over025=len(very), mean_power_over025=float(pv.mean()), max_false_alarm_le015=float(fa.max())))
R = pd.DataFrame(rows); R.to_csv(os.path.join(OUT, "verify_power_v5.csv"), index=False)
json.dump(rows, open(os.path.join(OUT, "verify_power_v5.json"), "w"), indent=1); print(R.round(3).to_string())
