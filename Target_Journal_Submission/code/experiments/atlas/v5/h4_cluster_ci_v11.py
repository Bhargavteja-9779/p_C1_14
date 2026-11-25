"""POST HOC (review round 9): population-clustered bootstrap CI for the within-site burn-in reduction (H4 units).
Resamples the 13 populations with replacement (2,000 draws, seed fixed); statistic = 1 - mean(burn)/mean(src) over all
units of the drawn populations, and the mean difference. Also per-population summary. Writes results/h4_cluster_ci_v11.json."""
import os, json, numpy as np, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
u = pd.read_csv(os.path.join(R, "v5_h4_units.csv")); pops = u["pop"].unique(); g = {p: u[u["pop"] == p] for p in pops}
rng = np.random.default_rng(20261124); red, diff = [], []
for _ in range(2000):
    d = pd.concat([g[p] for p in rng.choice(pops, len(pops))]); red.append(1 - d.burn.mean() / d.src.mean()); diff.append(d.burn.mean() - d.src.mean())
pp = u.groupby("pop")[["src", "burn"]].mean()
o = dict(reduction=float(1 - u.burn.mean() / u.src.mean()), reduction_ci=[float(np.quantile(red, .025)), float(np.quantile(red, .975))],
         diff=float(u.burn.mean() - u.src.mean()), diff_ci=[float(np.quantile(diff, .025)), float(np.quantile(diff, .975))],
         populations=len(pops), populations_better=int((pp.burn < pp.src).sum()))
json.dump(o, open(os.path.join(R, "h4_cluster_ci_v11.json"), "w"), indent=1); print(o)
