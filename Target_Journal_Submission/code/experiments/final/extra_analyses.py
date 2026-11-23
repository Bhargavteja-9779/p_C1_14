"""Post-hoc (not pre-registered) descriptive analyses of the status-quo threshold, alpha=0.10. Output: extra_analyses.txt"""
import os, glob, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); out = []
d = pd.read_csv(os.path.join(HERE, "locked_rows.csv.gz")); i = pd.read_csv(os.path.join(HERE, "locked_cohorts.csv"))
c = d[(d.alpha == 0.1) & (d.method == "source")].groupby(["task", "cohort", "model"]).fpr.mean().reset_index().merge(i)
c["dev"] = (c.fpr - 0.1).abs()
r = stats.spearmanr(c.auc, c.dev); out.append(f"AUROC vs |FPR-0.10| (32 cohort x model): Spearman rho={r.statistic:.2f}, P={r.pvalue:.2g}")
p = c.pivot_table(index=["task", "cohort"], columns="model", values="fpr")
r = stats.spearmanr(p.lasso, p.rf); out.append(f"LASSO vs RF realised FPR across 16 held-out cohorts: rho={r.statistic:.2f}, P={r.pvalue:.2g}")
rows = []
for task, coh, model in c[["task", "cohort", "model"]].itertuples(index=False):
    z = np.load(os.path.join(HERE, "scores", f"{task}_{coh}_{model}.npz"))
    rows.append(np.median(z["st"][z["yt"] == 0]) - np.median(z["s_src"][z["y_src"] == 0]))
c["ctrl_shift"] = rows
r = stats.spearmanr(c.ctrl_shift, c.fpr); out.append(f"Shift of median control score (target - training, logit) vs realised FPR: rho={r.statistic:.2f}, P={r.pvalue:.2g}")
txt = "\n".join(out); open(os.path.join(HERE, "extra_analyses.txt"), "w").write(txt); print(txt)
