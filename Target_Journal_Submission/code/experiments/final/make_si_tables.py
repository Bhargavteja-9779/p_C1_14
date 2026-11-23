"""Build supplementary tables (markdown) from locked outputs -> manuscript/si_tables.md"""
import os, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "..", "..", "manuscript", "si_tables.md")
def md(df):
    cols = list(df.columns); L = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False): L.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else (f"{v:.3f}" if isinstance(v, float) else str(v)) for v in r) + " |")
    return "\n".join(L)
d = pd.read_csv(os.path.join(HERE, "locked_rows.csv.gz")); info = pd.read_csv(os.path.join(HERE, "locked_cohorts.csv"))
d["key"] = d.method + np.where(d.n > 0, "_n" + d.n.astype(str), "")
o = ["# Supplementary tables\n"]
t = info.pivot_table(index=["task", "cohort", "n0", "n1"], columns="model", values=["auc", "auc_cohortstd"]).reset_index()
t.columns = ["task", "cohort", "controls", "cases", "AUROC LASSO", "AUROC RF", "AUROC LASSO (cohort-std)", "AUROC RF (cohort-std)"]
o += ["## Table S1. Held-out cohorts and AUROC", "CRC: trained on 8 development cohorts. Others: leave-one-cohort-out. Cohort-std = features standardised within cohort.\n", md(t)]
rows = []
for a in [0.10, 0.05]:
    for (task, model), q in info.groupby(["task", "model"]):
        chi = (((q[f"fp_full_{a}"] - a * q.n0) ** 2) / (q.n0 * a * (1 - a))).sum()
        rows.append(dict(alpha=a, task=task, model=model, cohorts=len(q), realised_FPR_range=f"{(q[f'fp_full_{a}']/q.n0).min():.2f}–{(q[f'fp_full_{a}']/q.n0).max():.2f}", chi2=round(chi, 1), P=f"{stats.chi2.sf(chi, len(q)):.2g}"))
o += ["\n## Table S2. Over-dispersion of realised FPR under the transferred threshold", "Chi-square of observed false positives (all controls of each held-out cohort) against Binomial(n_controls, alpha); df = number of cohorts.\n", md(pd.DataFrame(rows))]
cm = d.groupby(["alpha", "key", "task", "model", "cohort"]).agg(fpr=("fpr", "mean"), sens=("sens", "mean")).reset_index()
cm["within"] = (cm.fpr >= cm.alpha / 2) & (cm.fpr <= 1.5 * cm.alpha)
for a in [0.10, 0.05]:
    g = cm[cm.alpha == a].groupby("key").agg(pairs=("within", "size"), share_in_band=("within", "mean"), min_cohort_FPR=("fpr", "min"), max_cohort_FPR=("fpr", "max"), mean_sens=("sens", "mean"))
    q = d[d.alpha == a].groupby("key").agg(P_split_FPR_gt_1p5a=("fpr", lambda x: (x > 1.5 * a).mean()), P_split_FPR_le_a=("fpr", lambda x: (x <= a + 1e-12).mean()))
    g = g.join(q).reset_index().rename(columns={"key": "method"})
    o += [f"\n## Table S3{'a' if a == 0.10 else 'b'}. Pooled endpoints, target FPR = {a}", "Band = [alpha/2, 1.5 alpha]. A threshold of +inf (too few controls for the rule) gives FPR 0 and sensitivity 0.\n", md(g)]
sd = cm[cm.alpha == 0.10].groupby(["key", "task", "model"]).fpr.std().unstack(["task", "model"]).round(3)
sd.columns = [f"{a} {b}" for a, b in sd.columns]; o += ["\n## Table S5. SD across held-out cohorts of cohort-mean FPR (alpha = 0.10)\n", md(sd.reset_index().rename(columns={"key": "method"}))]
o += ["\n## Table S4. Post-hoc descriptive analyses (not pre-registered)\n", "```", open(os.path.join(HERE, "extra_analyses.txt")).read(), "```"]
open(OUT, "w").write("\n".join(o)); print("ok", OUT)
