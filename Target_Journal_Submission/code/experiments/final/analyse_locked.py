"""Endpoints of protocol.md from locked_rows.csv.gz / locked_cohorts.csv."""
import os, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); out = []
d = pd.read_csv(os.path.join(HERE, "locked_rows.csv.gz")); info = pd.read_csv(os.path.join(HERE, "locked_cohorts.csv"))
d["key"] = d.method + np.where(d.n > 0, "_n" + d.n.astype(str), "")
cm = d.groupby(["alpha", "task", "model", "key", "cohort"]).agg(fpr=("fpr", "mean"), sens=("sens", "mean"),
        over=("fpr", lambda x: 0), reps=("fpr", "size")).reset_index()
d["over15"] = d.fpr > 1.5 * d.alpha; d["le_a"] = d.fpr <= d.alpha + 1e-12
sp = d.groupby(["alpha", "task", "model", "key"]).agg(p_over=("over15", "mean"), p_le=("le_a", "mean")).reset_index()
cm["within"] = (cm.fpr >= cm.alpha * 0.5) & (cm.fpr <= cm.alpha * 1.5)
cm["dev"] = (cm.fpr - cm.alpha).abs()
P1 = cm.groupby(["alpha", "task", "model", "key"]).agg(n_coh=("cohort", "size"), fpr_mean=("fpr", "mean"), fpr_sd=("fpr", "std"),
        max_dev=("dev", "max"), within=("within", "mean"), sens=("sens", "mean")).reset_index().merge(sp)
P1.round(3).to_csv(os.path.join(HERE, "endpoints_by_task.csv"), index=False)
pd.set_option("display.width", 250)
for a in [0.10, 0.05]:
    out.append(f"\n=== alpha={a}: per task/model (cohort-mean FPR sd, max |dev|, share within [0.5a,1.5a], P(split FPR>1.5a), sens) ===")
    t = P1[(P1.alpha == a)].pivot_table(index="key", columns=["task", "model"], values="fpr_sd").round(3)
    out.append("SD of cohort-mean FPR\n" + t.to_string())
    t = P1[(P1.alpha == a)].pivot_table(index="key", columns=["task", "model"], values="sens").round(3)
    out.append("Mean sensitivity\n" + t.to_string())
    pooled = cm[cm.alpha == a].groupby("key").agg(pairs=("within", "size"), within=("within", "mean"), max_dev=("dev", "max"), sens=("sens", "mean"))
    pooled = pooled.join(d[d.alpha == a].groupby("key").agg(p_over=("over15", "mean"), p_le=("le_a", "mean")))
    out.append("Pooled over all cohort x model pairs\n" + pooled.round(3).to_string())
# success criterion
a = 0.10; c = cm[cm.alpha == a]
w_conf = c[c.key == "conformal_n20"].within.mean(); w_src = c[c.key == "source"].within.mean()
sdc = P1[(P1.alpha == a) & (P1.key == "conformal_n20")].groupby("task").fpr_sd.mean()
sds = P1[(P1.alpha == a) & (P1.key == "source")].groupby("task").fpr_sd.mean()
out.append(f"\nSUCCESS CRITERION: conformal_n20 within-band share = {w_conf:.3f} (need >=0.90); source outside-band share = {1-w_src:.3f} (drift claim needs >=0.30)")
out.append("SD by task (mean over models): conformal_n20 " + sdc.round(3).to_dict().__repr__() + " | source " + sds.round(3).to_dict().__repr__())
# overdispersion of source
for a in [0.10, 0.05]:
    for (task, model), q in info.groupby(["task", "model"]):
        chi = (((q[f"fp_full_{a}"] - a * q.n0) ** 2) / (q.n0 * a * (1 - a))).sum()
        out.append(f"overdispersion source a={a} {task} {model}: chi2={chi:.1f} df={len(q)} p={stats.chi2.sf(chi, len(q)):.2g}")
# cohort bootstrap for SD difference conformal_n20 - source (pool all tasks, per model), alpha=0.10
rng = np.random.default_rng(1)
for model in ["lasso", "rf"]:
    x = c[(c.model == model)].pivot_table(index=["task", "cohort"], columns="key", values="fpr")[["source", "conformal_n20"]].dropna()
    dif = []
    for _ in range(2000):
        b = x.sample(len(x), replace=True, random_state=rng.integers(1e9))
        dif.append(b.conformal_n20.std() - b.source.std())
    out.append(f"bootstrap SD(conformal_n20)-SD(source) {model}: {x.conformal_n20.std()-x.source.std():.3f} 95% CI [{np.quantile(dif,.025):.3f}, {np.quantile(dif,.975):.3f}] over {len(x)} cohorts")
# harm per 1000 at prevalence p (CRC only)
for p in [0.005, 0.01]:
    h = cm[(cm.task == "CRC") & (cm.alpha == 0.10)].copy()
    h["fp_per_1000"] = 1000 * (1 - p) * h.fpr; h["missed_per_1000"] = 1000 * p * (1 - h.sens)
    out.append(f"\nCRC harm per 1,000 screened, p={p}\n" + h[h.key.isin(["source", "cohortstd", "conformal_n20", "tong95_n50"])].pivot_table(
        index=["model", "cohort"], columns="key", values=["fp_per_1000", "missed_per_1000"]).round(1).to_string())
out.append("\nAUC per cohort\n" + info[["task", "cohort", "model", "n0", "n1", "auc", "auc_cohortstd"]].round(3).to_string())
txt = "\n".join(out); open(os.path.join(HERE, "endpoints.txt"), "w").write(txt); print(txt)
