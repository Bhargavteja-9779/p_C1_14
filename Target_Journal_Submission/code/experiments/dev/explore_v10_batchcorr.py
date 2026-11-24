"""DEV ONLY (post hoc): does label-free per-site standardisation (a simple batch correction) remove cut-off drift?
Variant A (as main analysis): pooled z-scoring with training statistics. Variant B: every cohort (training cohorts and
the held-out site) z-scored with its own mean/sd (site-wise centring, no labels). Variant C: site-wise rank (quantile)
normalisation within cohort. Cut-off = 90%-specificity quantile of LOCO out-of-fold source controls. LOCO over 8 DEV cohorts."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import make, logit
from sklearn.metrics import roc_auc_score
from scipy.stats import rankdata
X, y, g, M = load("CRC", DEV_CRC); X = X.values
L = np.log10(X / 100 + 1e-5)
def sitewise(Lm, groups, mode):
    Z = np.zeros_like(Lm)
    for s in np.unique(groups):
        i = groups == s; A = Lm[i]
        if mode == "z": Z[i] = (A - A.mean(0)) / (A.std(0) + 1e-6)
        else: Z[i] = (np.apply_along_axis(rankdata, 0, A) - 0.5) / len(A) - 0.5
    return Z
rows = []
for model in ["lasso", "rf"]:
    for variant in ["pooled", "site_z", "site_rank"]:
        for s in DEV_CRC:
            te = g == s; tr = ~te
            keep = (X[tr] > 0).mean(0) > 0.05
            if variant == "pooled":
                mu, sd = L[tr][:, keep].mean(0), L[tr][:, keep].std(0) + 1e-6; Z = (L[:, keep] - mu) / sd
            else:
                Z = sitewise(L[:, keep], g, "z" if variant == "site_z" else "rank")
            oof = np.zeros(tr.sum()); gtr = g[tr]; Ztr, ytr = Z[tr], y[tr]
            for s2 in np.unique(gtr):
                b = gtr == s2; m = make(model).fit(Ztr[~b], ytr[~b]); oof[b] = logit(m.predict_proba(Ztr[b])[:, 1])
            t = np.quantile(oof[ytr == 0], 0.9); m = make(model).fit(Ztr, ytr); st = logit(m.predict_proba(Z[te])[:, 1])
            rows.append(dict(model=model, variant=variant, site=s, auc=roc_auc_score(y[te], st), fpr=(st[y[te] == 0] >= t).mean(),
                             sens=(st[y[te] == 1] >= t).mean()))
        print(model, variant, flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), "explore_v10_batchcorr.csv"), index=False)
d["absdev"] = (d.fpr - 0.1).abs(); d["over"] = d.fpr > 0.12
print(d.groupby(["model", "variant"]).agg(auc=("auc", "mean"), fpr_mean=("fpr", "mean"), fpr_min=("fpr", "min"), fpr_max=("fpr", "max"),
      absdev=("absdev", "mean"), share_over=("over", "mean"), sens=("sens", "mean")).round(3).to_string())
