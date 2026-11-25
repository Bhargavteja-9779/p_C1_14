"""POST-HOC analyses after review round 2 (exploratory). Writes results/posthoc_r2_tables.md.
T1  locked run: rank-rule error predicted by order-statistic theory (r / (n0 + 1)) vs observed; contribution of abstention.
T2  locked run: label-free methods per model (which made the cut-off worse for each classifier).
F   fair feature standardisation (training cohorts standardised on controls only).
E2b pool size with fixed evaluation sets and an oracle noise floor, per task.
E3b other-cohort vs same-cohort pool with the same model and pool size; bootstrap clustered by target cohort.
E6  time drift in HMP_2019_ibdmdb (subject-disjoint pool and evaluation; same vs later period)."""
import os, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); FIN = os.path.join(H, "..", "experiments", "final")
PH = os.path.join(H, "..", "experiments", "posthoc"); OUT = os.path.join(H, "..", "..", "results", "posthoc_r2_tables.md")
rng = np.random.default_rng(2); rmse = lambda e: float(np.sqrt(np.mean(np.square(e))))
L = []
def w(s=""): L.append(s)
def md(t): w(t.to_markdown()); w()
def load(e): return pd.concat([pd.read_csv(os.path.join(PH, f"{e}_{m}.csv")) for m in ("lasso", "rf") if os.path.exists(os.path.join(PH, f"{e}_{m}.csv"))])
w("# Post-hoc analyses after review round 2 (EXPLORATORY, not pre-registered)\n")

d = pd.concat([pd.read_csv(os.path.join(FIN, f"final_{m}.csv.gz")) for m in ("lasso", "rf")])
x = d[(d.alpha == 0.10) & (d.pi == 0.0) & (d.method == "rpoolmean")]
u = x.groupby(["disease", "cohort", "model"]).agg(fpr=("fpr", "mean"), n=("n_pool", "first"), ab=("abstain", "mean")).reset_index()
n0 = u.n - np.floor(0.05 * u.n); r = np.floor((n0 + 1) * 0.10); u["theory"] = np.where(r > 0, r / (n0 + 1), 0.0)
w("## T1. Locked run: rank-rule FPR predicted by order-statistic theory (alpha 0.10, no cases)\n")
w(f"cohort-RMSE observed {rmse(u.fpr - 0.1):.3f}; predicted from r/(n0+1) alone {rmse(u.theory - 0.1):.3f}; "
  f"without the abstaining cohort (HallAB_2017): observed {rmse(u[u.ab == 0].fpr - 0.1):.3f}, predicted {rmse(u[u.ab == 0].theory - 0.1):.3f}.\n")
md(u.assign(pool_n=u.n).drop(columns="n").round(3).sort_values("pool_n"))

w("## T2. Locked run: cohort-RMSE per classifier (alpha 0.10)\n")
c = d[d.alpha == 0.10].groupby(["disease", "cohort", "model", "pi", "method"]).fpr.mean().reset_index()
md(c[c.pi.isin([0.0, 0.2])].groupby(["model", "pi", "method"]).fpr.apply(lambda v: rmse(v - 0.1)).unstack("method").round(3))

w("## F. Feature standardisation, training cohorts standardised on all samples vs on controls only (alpha 0.10)\n")
f = load("F"); f = f[f.alpha == 0.10].groupby(["disease", "cohort", "model", "pi", "method"]).fpr.mean().reset_index()
md(f.groupby(["model", "pi", "method"]).fpr.apply(lambda v: rmse(v - 0.1)).unstack("method").round(3))

w("## E2b. Pool size with fixed evaluation sets (5% binomial cases in the pool, alpha 0.10)\n")
w("Share of deployments with FPR > 0.15. 'oracle' = cut-off at the true (1 - alpha) quantile of all the cohort's "
  "controls: its exceedance is the evaluation-noise floor.\n")
e = load("E2b"); e = e[e.alpha == 0.10]; e["task"] = e.disease + ":" + e.cohort
t = e.groupby(["task", "model", "n_pool", "method"]).fpr.apply(lambda v: (v > 0.15).mean()).reset_index()
md(t.pivot_table(index=["task", "n_pool"], columns="method", values="fpr").round(3))
w("Mean over the four tasks and both models, at pool sizes available in all tasks:\n")
md(t[t.n_pool <= 75].pivot_table(index="n_pool", columns="method", values="fpr").round(3))
w("Mean FPR:\n")
md(e[e.n_pool <= 75].pivot_table(index="n_pool", columns="method", values="fpr").round(3))

w("## E3b. Pool from another cohort vs from the target cohort itself (same model, same pool size; alpha 0.10)\n")
b = load("E3b"); b = b[b.alpha == 0.10]
p = b.groupby(["disease", "pool_from", "cohort", "model", "origin", "method"]).fpr.mean().reset_index()
md(p.groupby(["origin", "method"]).fpr.apply(lambda v: pd.Series(dict(rmse=rmse(v - 0.1), share_gt_15=(v > 0.15).mean()))).unstack().round(3))
q = p[p.method == "rpoolmean"].pivot_table(index=["disease", "pool_from", "cohort", "model"], columns="origin", values="fpr").reset_index()
q["dae"] = (q["other cohort"] - 0.1).abs() - (q["same cohort"] - 0.1).abs(); q["cl"] = q.disease + ":" + q.cohort
cl = q.cl.unique(); idx = {k: np.where(q.cl.values == k)[0] for k in cl}
bs = [np.concatenate([q.dae.values[idx[k]] for k in rng.choice(cl, len(cl))]).mean() for _ in range(5000)]
w(f"Rank rule, |FPR - 0.10| other cohort minus same cohort: mean {q.dae.mean():.3f}, 95% CI clustered by target cohort "
  f"{np.percentile(bs, 2.5):.3f} to {np.percentile(bs, 97.5):.3f} ({len(q)} pair-model units, {len(cl)} target cohorts).\n")

w("## E6. Time drift, HMP_2019_ibdmdb (pool: controls days 0-120 of half the subjects; evaluation: the other subjects)\n")
h = load("E6"); h = h[h.alpha == 0.10]
md(h.groupby(["model", "period", "method"]).agg(mean_fpr=("fpr", "mean"), p90_fpr=("fpr", lambda v: v.quantile(.9)),
     share_gt_15=("fpr", lambda v: (v > 0.15).mean()), sens=("sens", "mean"), n_pool=("n_pool", "mean"), n_eval=("n_eval", "mean")).round(3))
open(OUT, "w").write("\n".join(L)); print("\n".join(L))
