"""POST HOC (review r17): Fisher-z 95% CI of the Spearman rho between out-of-fold AUROC and between-population tau
(28 classifiers; approximate for Spearman), and the share of classifier-population pairs (strict set, n >= 20) with an
FPR above 0.25 (2.5 times the 0.10 target). Pooled-FPR range by model."""
import os, json, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results")
s = json.load(open(os.path.join(R, "v5_summary.json")))["expl_auroc_vs_tau"]; r, n = s["spearman"], 28
z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
p = pd.read_csv(os.path.join(R, "v5_perpop_strict.csv")); h = pd.read_csv(os.path.join(R, "v5_het_strict.csv"))
out = dict(rho=r, rho_ci95_fisher=[float(np.tanh(z - 1.96 * se)), float(np.tanh(z + 1.96 * se))],
           share_pairs_fpr_gt_025={m: float((p[p.model == m].fpr > .25).mean()) for m in ["lasso", "rf"]},
           pairs={m: int((p.model == m).sum()) for m in ["lasso", "rf"]},
           pooled_range={m: [float(h[h.model == m].pooled.min()), float(h[h.model == m].pooled.max())] for m in ["lasso", "rf"]})
json.dump(out, open(os.path.join(R, "posthoc_r17_numbers.json"), "w"), indent=1); print(out)
