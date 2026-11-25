"""POST-HOC analyses after review round 1 (exploratory; not pre-registered). Writes results/posthoc_r1_tables.md.
E4: re-analysis of the LOCKED run: per-deployment error, clustered bootstrap (by cohort-task and by control study),
    TOST equivalence of rpoolmean vs ctrl10, sensitivity analysis without the adenoma task, alpha = 0.05.
E1-E3, E5: summaries of code/experiments/posthoc/explore_r1.py outputs."""
import os, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); FIN = os.path.join(H, "..", "experiments", "final")
PH = os.path.join(H, "..", "experiments", "posthoc"); OUT = os.path.join(H, "..", "..", "results", "posthoc_r1_tables.md")
rng = np.random.default_rng(1)
d = pd.concat([pd.read_csv(os.path.join(FIN, f"final_{m}.csv.gz")) for m in ("lasso", "rf")])
L = []
def w(s=""): L.append(s)
def md(t): w(t.to_markdown()); w()
rmse = lambda e: float(np.sqrt(np.mean(np.square(e))))
M = ["source", "local_q", "em", "mlls", "gauss2", "shift2", "featstd", "ctrl10", "rpoolmean", "rpool"]

w("# Post-hoc analyses after review round 1 (EXPLORATORY, not pre-registered)\n")
w("## E4a. Locked run, per-deployment view (each of 200 splits = one simulated laboratory)\n")
for a in (0.10, 0.05):
    x = d[(d.alpha == a) & (d.pi == 0.0)]
    t = x.groupby("method").agg(cohort_rmse=("fpr", lambda v: np.nan), deploy_rmse=("fpr", lambda v: rmse(v - a)),
                                p_fpr_gt_a_plus_5=("fpr", lambda v: (v > a + 0.05).mean()),
                                p_fpr_gt_2a=("fpr", lambda v: (v > 2 * a).mean()), abstain=("abstain", "mean"))
    t["cohort_rmse"] = x.groupby(["disease", "cohort", "model", "method"]).fpr.mean().reset_index().groupby("method").fpr.apply(lambda v: rmse(v - a))
    w(f"alpha = {a}, pi = 0 (pi = 0.01 is identical in 13 of 16 cohort-task pairs because the locked design rounded the "
      "number of cases to 0; see E1)\n"); md(t.reindex(M).round(3))

w("## E4b. Paired comparisons with clustered bootstrap (alpha 0.10, pi 0.01)\n")
cm = d[(d.alpha == 0.10) & (d.pi == 0.01)].groupby(["disease", "cohort", "model", "method"]).fpr.mean().reset_index()
cm["ae"] = (cm.fpr - 0.10).abs()
wd = cm.pivot_table(index=["disease", "cohort", "model"], columns="method", values="ae").reset_index()
wd["task"] = wd.disease + ":" + wd.cohort
wd["ctrlset"] = np.where(wd.disease.isin(["CRC", "adenoma"]), wd.cohort, wd.disease + ":" + wd.cohort)  # adenoma shares CRC controls
def cboot(diff, cl, B=5000):
    u = np.unique(cl); idx = {c: np.where(cl == c)[0] for c in u}
    return np.percentile([np.concatenate([diff[idx[c]] for c in rng.choice(u, len(u))]).mean() for _ in range(B)], [2.5, 97.5])
rows = []
for sub, msk in [("all tasks", np.ones(len(wd), bool)), ("without adenoma", (wd.disease != "adenoma").values)]:
    W = wd[msk]
    for m in [c for c in M if c != "rpoolmean"]:
        diff = (W.rpoolmean - W[m]).values
        ct = W.groupby("task")[["rpoolmean", m]].mean(); dt = (ct.rpoolmean - ct[m]).values  # cohort-task level test
        rows.append(dict(subset=sub, comparison=f"rpoolmean - {m}", mean_diff=diff.mean(),
                         ci_cluster_task="%.4f to %.4f" % tuple(cboot(diff, W.task.values)),
                         ci_cluster_controls="%.4f to %.4f" % tuple(cboot(diff, W.ctrlset.values)),
                         n_tasks=len(dt), p_wilcoxon_tasks=stats.wilcoxon(dt).pvalue if np.any(dt != 0) else 1.0))
T = pd.DataFrame(rows)
for sub in T.subset.unique():
    k = T.subset == sub; p = T.loc[k, "p_wilcoxon_tasks"].values; o = np.argsort(p); h = np.empty_like(p)
    h[o] = np.maximum.accumulate(np.minimum(1, p[o] * (len(p) - np.arange(len(p))))); T.loc[k, "p_holm"] = h
w(T.round(4).to_markdown(index=False)); w()
# equivalence rpoolmean vs ctrl10 (TOST on cohort-task means of absolute error, margin 0.02)
ct = wd.groupby("task")[["rpoolmean", "ctrl10"]].mean(); dt = (ct.rpoolmean - ct.ctrl10).values; n = len(dt)
se = dt.std(ddof=1) / np.sqrt(n); tl = (dt.mean() + 0.02) / se; tu = (dt.mean() - 0.02) / se
w(f"TOST rpoolmean vs ctrl10 (absolute FPR error, cohort-task level, margin +/-0.02): mean diff {dt.mean():.4f}, "
  f"90% CI {dt.mean() - stats.t.ppf(.95, n - 1) * se:.4f} to {dt.mean() + stats.t.ppf(.95, n - 1) * se:.4f}, "
  f"p = {max(stats.t.sf(tl, n - 1), stats.t.cdf(tu, n - 1)):.4f}\n")

w("## E4c. Locked run, alpha = 0.05 (pre-registered secondary), cohort-RMSE by case share\n")
c5 = d[d.alpha == 0.05].groupby(["disease", "cohort", "model", "pi", "method"]).agg(fpr=("fpr", "mean"), ab=("abstain", "mean")).reset_index()
md(c5.groupby(["method", "pi"]).fpr.apply(lambda v: rmse(v - 0.05)).unstack().reindex(M).round(3))
w("abstention rate at alpha = 0.05:"); md(c5.groupby(["method", "pi"]).ab.mean().unstack().reindex(M).round(3))

def agg(x, a):
    g = x.groupby(["disease", "cohort", "model", "pi", "method"]).agg(fpr=("fpr", "mean"), fs=("fpr_strict", "mean"),
         sens=("sens", "mean"), ab=("abstain", "mean"), dep=("fpr", lambda v: rmse(v - a)), K=("k_cases", "mean")).reset_index()
    return g.groupby(["pi", "method"]).apply(lambda z: pd.Series(dict(cohort_rmse=rmse(z.fpr - a), cohort_rmse_strict_ties=rmse(z.fs - a),
         deploy_rmse=rmse(z.dep), max_cohort_fpr=z.fpr.max(), sens=z.sens.mean(), abstain=z.ab.mean(), mean_cases_in_pool=z.K.mean()))).round(3)
def load(e):
    f = [os.path.join(PH, f"{e}_{m}.csv") for m in ("lasso", "rf")]
    return pd.concat([pd.read_csv(x) for x in f if os.path.exists(x)])
w("## E1. Cases actually in the pool: K ~ Binomial(n, pi) (both models, alpha 0.10)\n")
e1 = load("E1"); w(f"models: {sorted(e1.model.unique())}\n"); md(agg(e1[e1.alpha == 0.10], 0.10))
w("## E2. Pool size in large cohorts (>= 150 controls; alpha 0.10). Evaluation on the remaining controls, so the "
  "share of draws with FPR > alpha includes evaluation noise.\n")
e2 = load("E2"); x = e2[e2.alpha == 0.10]
t = x.groupby(["cohort", "pi", "n_pool", "method"]).agg(mean_fpr=("fpr", "mean"), p_fpr_gt_a=("fpr", lambda v: (v > 0.10).mean()),
     p_fpr_gt_a_plus_5=("fpr", lambda v: (v > 0.15).mean()), sens=("sens", "mean")).reset_index()
t = t[t.pi.isin([0.0, 0.05]) & t.method.isin(["source", "local_q", "rpoolmean", "rpool", "ctrl10"])]
md(t.groupby(["pi", "n_pool", "method"])[["mean_fpr", "p_fpr_gt_a", "p_fpr_gt_a_plus_5", "sens"]].mean().unstack("method").round(3))
w("Per cohort (pi = 0.05, rpool vs rpoolmean vs local_q, share of draws with FPR > 0.15):\n")
md(t[t.pi == 0.05].pivot_table(index=["cohort", "n_pool"], columns="method", values="p_fpr_gt_a_plus_5").round(3))
w("## E3. Pool from ANOTHER cohort of the same task (a different laboratory), alpha 0.10\n")
e3 = load("E3"); x = e3[e3.alpha == 0.10].groupby(["disease", "pool_from", "cohort", "model", "method"]).fpr.mean().reset_index()
md(x.groupby("method").fpr.apply(lambda v: pd.Series(dict(pair_rmse=rmse(v - 0.10), median_fpr=v.median(),
     share_pairs_fpr_gt_15=(v > 0.15).mean(), max_fpr=v.max()))).unstack().round(3))
md(x.groupby(["disease", "method"]).fpr.apply(lambda v: rmse(v - 0.10)).unstack().round(3))
w("## E5. Same study, different centre (MetaCardis_2020_a: one protocol and sequencer; Copenhagen, Leipzig, Paris), alpha 0.10\n")
e5 = load("E5"); x = e5[e5.alpha == 0.10].groupby(["model", "pool_from", "cohort", "method"]).fpr.mean().reset_index()
x["setting"] = np.where(x.pool_from == x.cohort, "same centre (random halves)", "pool from another centre")
md(x.pivot_table(index=["model", "pool_from", "cohort"], columns="method", values="fpr").round(3))
md(x.groupby(["setting", "method"]).fpr.apply(lambda v: rmse(v - 0.10)).unstack().round(3))
open(OUT, "w").write("\n".join(L)); print("\n".join(L))
