"""DEV ONLY: atlas-reference and composition-matched reference thresholds, leave-one-dev-cohort-out."""
import sys, numpy as np, pandas as pd; sys.path.insert(0, ".."); sys.path.insert(0, "../../..")
from common import *
A = 0.10; dev, _ = split()
r = pd.read_csv("../results/atlas_rows.csv.gz"); r = r[r.study.isin(dev)]
# composition centroids: CLR on genus-agnostic species union, PCA on dev samples
F = {}
for s in dev:
    X, md = healthy(s); F[s] = X
U = pd.concat(F.values()).fillna(0); keep = (U > 0).mean() > 0.05; U = U.loc[:, keep]
L = np.log(U.values + 1e-4); L = L - L.mean(1, keepdims=True); mu = L.mean(0); _, _, Vt = np.linalg.svd(L - mu, full_matrices=False)
P = pd.DataFrame((L - mu) @ Vt[:10].T, index=U.index)
studies = np.concatenate([[s] * len(F[s]) for s in dev]); cent = pd.DataFrame(P.values).groupby(studies).mean()
out = []
for (d, m), g in r.groupby(["disease", "model"]):
    S = {s: x.score.values for s, x in g.groupby("study")}; t0 = g.thr.iloc[0]
    st = [s for s in S if len(S[s]) >= 15]
    for s in st:
        oth = [o for o in st if o != s]
        t_atlas = np.quantile(np.concatenate([S[o] for o in oth]), 1 - A)
        dist = ((cent.loc[oth] - cent.loc[s]) ** 2).sum(1).sort_values()
        row = dict(disease=d, model=m, study=s, n=len(S[s]), fpr_src=np.mean(S[s] >= t0), fpr_atlas=np.mean(S[s] >= t_atlas))
        for k in [1, 3, 5]:
            nn = dist.index[:k]; row[f"fpr_nn{k}"] = np.mean(S[s] >= np.quantile(np.concatenate([S[o] for o in nn]), 1 - A))
        # random-k reference (control for nn)
        rng = np.random.default_rng(0); row["fpr_rand3"] = np.mean([np.mean(S[s] >= np.quantile(np.concatenate([S[o] for o in rng.choice(oth, 3, replace=False)]), 1 - A)) for _ in range(50)])
        out.append(row)
o = pd.DataFrame(out); o.to_csv("explore_r2.csv", index=False)
cols = [c for c in o if c.startswith("fpr")]
summ = o.groupby(["disease", "model"])[cols].agg(lambda x: np.mean(np.abs(x - A))).round(3)
print("mean |FPR-0.10| per dev cohort\n", summ.to_string())
print("in band\n", o.groupby(["disease", "model"])[cols].agg(lambda x: np.mean((x >= .05) & (x <= .15))).round(2).to_string())
