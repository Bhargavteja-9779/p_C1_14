"""Pre-registered analysis of the locked final test (experiments/protocol.md). Writes tables to results/."""
import os, sys, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(__file__); OUT = os.path.join(H, "..", "..", "results"); os.makedirs(OUT, exist_ok=True)
F = [os.path.join(H, "..", "experiments", "final", f"final_{m}.csv") for m in ("lasso", "rf")]
d = pd.concat([pd.read_csv(f) for f in F if os.path.exists(f)])
PRIMARY = "rpoolmean"; rng = np.random.default_rng(0)
cm = d.groupby(["disease", "cohort", "model", "alpha", "pi", "method"]).agg(
    fpr=("fpr", "mean"), sens=("sens", "mean"), abstain=("abstain", "mean"), auc=("auc", "first"), n_pool=("n_pool", "first"),
    p_over=("fpr", lambda v: np.nan)).reset_index()
over = d.assign(o=d.fpr > d.alpha + 0.05).groupby(["disease", "cohort", "model", "alpha", "pi", "method"]).o.mean().values
cm["p_over"] = over; cm["err"] = cm.fpr - cm.alpha
cm.to_csv(os.path.join(OUT, "cohort_level_summary.csv"), index=False)
# Table 1: cohort-RMSE and mean metrics per method (primary: pi = 0.01, alpha = 0.10)
def table(a, p):
    x = cm[(cm.alpha == a) & (cm.pi == p)]
    return x.groupby("method").agg(cohort_rmse=("err", lambda e: np.sqrt(np.mean(e ** 2))), mean_fpr=("fpr", "mean"),
                                   max_abs_err=("err", lambda e: np.abs(e).max()), sens=("sens", "mean"),
                                   p_fpr_over_a_plus_5=("p_over", "mean"), abstain=("abstain", "mean"), units=("fpr", "size")).round(3)
with open(os.path.join(OUT, "main_tables.md"), "w") as f:
    for a in (0.10, 0.05):
        for p in (0.0, 0.01, 0.05, 0.2):
            t = table(a, p).sort_values("cohort_rmse"); f.write(f"\n## alpha = {a}, case share in pool = {p}\n\n{t.to_markdown()}\n")
            if a == 0.10 and p == 0.01: print(t.to_string())
    # per disease, primary setting
    x = cm[(cm.alpha == 0.10) & (cm.pi == 0.01)]
    t = x.groupby(["disease", "method"]).err.apply(lambda e: np.sqrt(np.mean(e ** 2))).unstack("disease").round(3)
    f.write(f"\n## cohort-RMSE by disease (alpha 0.10, pi 0.01)\n\n{t.to_markdown()}\n"); print(t.to_string())
    # paired tests: rpoolmean vs each method on |cohort mean FPR - alpha|, units = cohort x model
    rows = []
    for a in (0.10,):
        x = cm[(cm.alpha == a) & (cm.pi == 0.01)].assign(ae=lambda z: z.err.abs())
        w = x.pivot_table(index=["disease", "cohort", "model"], columns="method", values="ae")
        for m in w.columns:
            if m == PRIMARY: continue
            diff = (w[PRIMARY] - w[m]).dropna().values
            bs = [rng.choice(diff, len(diff)).mean() for _ in range(5000)]
            p = stats.wilcoxon(diff).pvalue if np.any(diff != 0) else 1.0
            rows.append(dict(comparison=f"{PRIMARY} - {m}", n_units=len(diff), mean_diff_abs_err=diff.mean(),
                             ci_low=np.percentile(bs, 2.5), ci_high=np.percentile(bs, 97.5), p_wilcoxon=p))
    T = pd.DataFrame(rows).sort_values("p_wilcoxon"); k = len(T)
    T["p_holm"] = np.minimum.accumulate(np.minimum(1, T.p_wilcoxon.values * (k - np.arange(k)))[::-1])[::-1]
    T["p_holm"] = np.maximum.accumulate(np.minimum(1, T.p_wilcoxon.values * (k - np.arange(k))))
    T = T.round(4); f.write(f"\n## Paired comparisons (alpha 0.10, pi 0.01; negative = {PRIMARY} closer to target)\n\n{T.to_markdown(index=False)}\n")
    print(T.to_string(index=False))
    # Clinical translation, CRC external cohorts: per 1,000 screened at prevalence 0.5%
    x = cm[(cm.disease == "CRC") & (cm.alpha == 0.10) & (cm.pi == 0.01)].groupby(["method"])[["fpr", "sens"]].mean()
    prev = 0.005
    x["colonoscopies_per_1000"] = 1000 * ((1 - prev) * x.fpr + prev * x.sens)
    x["extra_vs_intended"] = 1000 * (1 - prev) * (x.fpr - 0.10)
    x["cancers_detected_per_1000"] = 1000 * prev * x.sens
    f.write(f"\n## CRC external cohorts: consequences per 1,000 screened (prevalence 0.5%, target FPR 10%)\n\n{x.round(2).to_markdown()}\n")
    print(x.round(2).to_string())
    # Motivating analysis: overdispersion of source-threshold FPR across cohorts (binomial on evaluation halves)
    s = cm[(cm.method == "source") & (cm.alpha == 0.10) & (cm.pi == 0.0)]
    f.write("\n## Overdispersion of source-threshold FPR across test cohorts (alpha 0.10)\n\n")
    for mdl, g in s.groupby("model"):
        n0 = d[(d.method == "source") & (d.model == mdl) & (d.alpha == 0.1) & (d.pi == 0.0) & (d.rep == 0)].groupby("cohort").n_pool.first()
        chi = sum((r.fpr - 0.1) ** 2 / (0.1 * 0.9 / max(n0[r.cohort], 1)) for r in g.itertuples())  # eval half ~ pool size
        f.write(f"- {mdl}: chi2 = {chi:.1f}, df = {len(g)}, p = {stats.chi2.sf(chi, len(g)):.2e}; FPR range {g.fpr.min():.3f}-{g.fpr.max():.3f}\n")
print("written", OUT)
