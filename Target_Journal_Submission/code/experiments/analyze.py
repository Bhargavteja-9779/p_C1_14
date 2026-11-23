"""Summaries + statistics from deploy_sim output. usage: python analyze.py results/deploy_X.csv.gz outdir"""
import sys, os, numpy as np, pandas as pd
from scipy import stats
ALPHA = 0.10
d = pd.read_csv(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
d["ae"] = (d.fpr - ALPHA).abs(); d["viol"] = (d.fpr > ALPHA + 0.05).astype(float)
d["meth"] = np.where(d["mode"] == "pcz", "M6_pcz_restandardise", d.method)
# site-level means (unit of analysis = site; mean over seeds x splits)
site = d.groupby(["disease", "target", "model", "pi", "meth"]).agg(ae=("ae", "mean"), fpr=("fpr", "mean"), viol=("viol", "mean"),
        sens=("sens", "mean"), auc=("auc", "mean"), fpr_sd=("fpr", "std")).reset_index()
site.to_csv(f"{out}/site_level.csv", index=False)
summ = site.groupby(["model", "pi", "meth"]).agg(ae=("ae", "mean"), viol=("viol", "mean"), sens=("sens", "mean"),
        n_sites=("ae", "size")).reset_index()
summ.to_csv(f"{out}/summary.csv", index=False)
print(summ.pivot_table(index=["model", "pi"], columns="meth", values="ae").round(3).to_string())
print(summ.pivot_table(index=["model", "pi"], columns="meth", values="viol").round(3).to_string())
print(summ.pivot_table(index=["model", "pi"], columns="meth", values="sens").round(3).to_string())
# paired site-level comparisons vs M0 (Wilcoxon, Holm across all comparisons in this file) + bootstrap CI of mean diff
rows = []; rng = np.random.default_rng(0)
for (m, pi), g in site.groupby(["model", "pi"]):
    w = g.pivot_table(index=["disease", "target"], columns="meth", values="ae")
    for k in w.columns:
        if k in ("M0_source", "Oracle"): continue
        x = (w[k] - w["M0_source"]).dropna()
        if len(x) < 3: continue
        p = stats.wilcoxon(x).pvalue if (x != 0).any() else 1.0
        bs = [rng.choice(x.values, len(x)).mean() for _ in range(5000)]
        rows.append(dict(model=m, pi=pi, method=k, n_sites=len(x), mean_diff=x.mean(), ci_lo=np.quantile(bs, .025),
                         ci_hi=np.quantile(bs, .975), wins=(x < 0).sum(), p=p))
c = pd.DataFrame(rows)
if len(c):
    o = np.argsort(c.p.values); m_ = len(c); adj = np.empty(m_); run = 0
    for r, i in enumerate(o): run = max(run, min(1, (m_ - r) * c.p.values[i])); adj[i] = run
    c["p_holm"] = adj
c.to_csv(f"{out}/paired_vs_M0.csv", index=False); print(c.round(4).to_string())
