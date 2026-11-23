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
        fp = q[f"fp_full_{a}"].values; tab = np.array([fp, q.n0.values - fp]).T
        chi, pv = stats.chi2_contingency(tab)[:2]
        rows.append(dict(alpha=a, task=task, model=model, cohorts=len(q), realised_FPR_range=f"{(fp/q.n0).min():.2f}–{(fp/q.n0).max():.2f}",
                         chi2_equal_props=round(chi, 1), df=len(q) - 1, P=f"{pv:.2g}"))
o += ["\n## Table S2. Heterogeneity of realised FPR across held-out cohorts under the transferred threshold",
      "Chi-square test of equal false-positive proportions across cohorts (all controls of each cohort). Replaces the pre-registered test against Binomial(alpha) (see Deviations); a common bias shared by all cohorts (as in external CRC) is not detected by this test.\n", md(pd.DataFrame(rows))]
cm = d.groupby(["alpha", "key", "task", "model", "cohort"]).agg(fpr=("fpr", "mean"), sens=("sens", "mean")).reset_index()
cm["within"] = (cm.fpr >= cm.alpha / 2) & (cm.fpr <= 1.5 * cm.alpha)
for a in [0.10, 0.05]:
    g = cm[cm.alpha == a].groupby("key").agg(pairs=("within", "size"), share_in_band=("within", "mean"), min_cohort_FPR=("fpr", "min"), max_cohort_FPR=("fpr", "max"), mean_sens=("sens", "mean"))
    q = d[d.alpha == a].groupby("key").agg(P_split_FPR_gt_1p5a=("fpr", lambda x: (x > 1.5 * a).mean()), P_split_FPR_le_a=("fpr", lambda x: (x <= a + 1e-12).mean()))
    g = g.join(q).reset_index().rename(columns={"key": "method"})
    if a == 0.05: g = g[~g.method.isin(["conformal_n10", "tong95_n30", "tong95_n50"])]
    o += [f"\n## Table S3{'a' if a == 0.10 else 'b'}. Pooled endpoints, target FPR = {a}", "Band = [alpha/2, 1.5 alpha]. At alpha=0.05, conformal with n=10 (needs n>=19) and the 95%-confidence rule with n<=50 (needs n>=59) are not feasible and are omitted. The 95%-confidence rule's secondary endpoint is P_split_FPR_le_a (target >= 0.95).\n", md(g)]
sd = cm[cm.alpha == 0.10].groupby(["key", "task", "model"]).fpr.std().unstack(["task", "model"]).round(3)
sd.columns = [f"{a} {b}" for a, b in sd.columns]; o += ["\n## Table S5. SD across held-out cohorts of cohort-mean FPR (alpha = 0.10)\n", md(sd.reset_index().rename(columns={"key": "method"}))]
o += ["\n## Table S4. Post-hoc descriptive analyses (not pre-registered)\n", "```", open(os.path.join(HERE, "extra_analyses.txt")).read(), "```"]

def txt_table(title, fname, note=""):
    return [f"\n## {title}\n", note, "```", open(os.path.join(HERE, fname)).read(), "```"]
o += txt_table("Table S6. Status-quo threshold with matched scoring (fold-model ensemble) vs refitted model", "ensemble_check.txt", "Post hoc.")
ch = pd.read_csv(os.path.join(HERE, "cohort_characteristics.csv"))
o += ["\n## Table S7. Cohort characteristics (controls)\n", "Post hoc. Median read depth in millions; control_disease = most frequent 'disease' labels among controls.\n", md(ch)]
pr = [l for l in open(os.path.join(HERE, "post_review1.txt")).read().splitlines() if l[:2] in ("B.", "C.", "D.", "E.")]
o += ["\n## Table S8. Read depth, MetaCardis control subgroups, percentile normalisation, adenoma positivity\n", "Post hoc. B: depth vs control-score shift; C: MetaCardis control subgroups; D: percentile normalisation against 20 local controls (external CRC, R=50); E: positivity of Yachida adenoma carriers.\n", "```", "\n".join(pr), "```"]
o += txt_table("Table S9. Twenty labelled controls from another centre or cohort", "mismatch_analysis.txt", "Post hoc. Conformal rule, n=20, alpha=0.10, R=200. same_site=True rows use the half-split design of the main analysis.")
o += txt_table("Table S10. Single-site FPR of the conformal rule by number of local controls", "control_budget.txt", "Post hoc. Theory: FPR ~ Beta(n+1-k, k).")
o += txt_table("Table S11. Label-free threshold from simulated screening pools", "screening_pool_sim.txt", "Post hoc. Pools resampled from each cohort's calibration-half controls (with replacement) plus cases at prevalence pi; effective number of distinct controls is therefore limited by cohort size.")
open(OUT, "w").write("\n".join(o)); print("ok", OUT)
