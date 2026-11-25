"""POST HOC (after v6b): within-study AUROC (cases vs controls of the same study; geography held constant) for NAIVE vs
BALANCED, and the between-study 'shortcut' AUROC (healthy-only studies vs disease-only... ) - study-clustered bootstrap."""
import json, numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
R = pd.read_csv("results/v6b_loso_scores.csv.gz", index_col=0)
mixed = [s for s, g in R.groupby("study_name") if g.healthy.sum() >= 10 and (g.healthy == 0).sum() >= 10]
def w(Rr):
    out = {}
    for m in ["naive", "balanced"]:
        a = [roc_auc_score(g.healthy, g[m]) for s, g in Rr.groupby("study_name") if s in mixed]; out[m] = float(np.mean(a))
    return out
o = w(R); rng = np.random.default_rng(3); d = []
for _ in range(2000):
    pick = rng.choice(mixed, len(mixed)); Rb = pd.concat([R[R.study_name == s].assign(study_name=f"{s}_{i}") for i, s in enumerate(pick)])
    mixed_b = Rb.study_name.unique(); a = {m: np.mean([roc_auc_score(g.healthy, g[m]) for s, g in Rb.groupby("study_name")]) for m in ["naive", "balanced"]}
    d.append(a["balanced"] - a["naive"])
res = dict(mixed_studies=len(mixed), within_auroc_naive=o["naive"], within_auroc_balanced=o["balanced"], diff=o["balanced"] - o["naive"],
           ci95=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
json.dump(res, open("results/v6b_within_study_auroc.json", "w"), indent=1); print(res)
