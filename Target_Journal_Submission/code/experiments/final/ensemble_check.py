"""POST-HOC (review round 1, statistics referee issue 2). Status-quo threshold with matched scoring:
target scored by the AVERAGE of the leave-one-cohort-out fold models (the same models that produced the out-of-fold
training scores used for the threshold), instead of the model refitted on all training cohorts. alpha=0.10 and 0.05.
Also: heterogeneity of realised FPR across cohorts (chi-square test of equal proportions), for both scorings."""
import os, sys, numpy as np, pandas as pd
from scipy import stats
from sklearn.model_selection import GroupKFold
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load, DEV_CRC, LOCKED_CRC
from src.models import preprocess_fit, preprocess_apply, make, logit
rows = []
def tasks():
    X, y, g, _ = load("CRC"); X = X.values
    for s in LOCKED_CRC: yield "CRC", X, y, g, s, np.isin(g, DEV_CRC)
    for d in ["IBD", "T2D", "adenoma"]:
        X, y, g, _ = load(d); X = X.values
        for s in np.unique(g): yield d, X, y, g, s, g != s
for task, X, y, g, s, tr in tasks():
    te = g == s; p = preprocess_fit(X[tr]); Ztr, Zte = preprocess_apply(X[tr], p), preprocess_apply(X[te], p); ytr, gtr = y[tr], g[tr]; yt = y[te]
    for model in ["lasso", "rf"]:
        oof = np.zeros(len(ytr)); ens = np.zeros(te.sum()); k = 0
        for a, b in GroupKFold(len(np.unique(gtr))).split(Ztr, ytr, gtr):
            m = make(model).fit(Ztr[a], ytr[a]); oof[b] = m.predict_proba(Ztr[b])[:, 1]; ens += m.predict_proba(Zte)[:, 1]; k += 1
        ens = logit(ens / k); oof = logit(oof); full = np.load(os.path.join(HERE, "scores", f"{task}_{s}_{model}.npz"))["st"]
        for alpha in [0.10, 0.05]:
            t = np.quantile(oof[ytr == 0], 1 - alpha)
            for scoring, sc in [("refit (main)", full), ("fold-ensemble", ens)]:
                rows.append(dict(task=task, cohort=s, model=model, alpha=alpha, scoring=scoring, n0=int((yt == 0).sum()),
                                 fp=int((sc[yt == 0] >= t).sum()), fpr=float((sc[yt == 0] >= t).mean()), sens=float((sc[yt == 1] >= t).mean())))
    print(task, s, flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(HERE, "ensemble_check.csv"), index=False); out = []
d["out_band"] = (d.fpr < d.alpha / 2) | (d.fpr > 1.5 * d.alpha)
out.append(d.groupby(["alpha", "scoring"]).agg(pairs=("fpr", "size"), share_out_of_band=("out_band", "mean"), min_fpr=("fpr", "min"), max_fpr=("fpr", "max"), sd_fpr=("fpr", "std"), sens=("sens", "mean")).round(3).to_string())
for (a, sc, task, model), q in d.groupby(["alpha", "scoring", "task", "model"]):
    tab = np.array([q.fp, q.n0 - q.fp]).T
    chi, pv = stats.chi2_contingency(tab)[:2] if (tab[:, 0].sum() > 0) else (np.nan, np.nan)
    out.append(f"heterogeneity a={a} {sc:14s} {task:8s} {model}: FPR {q.fpr.min():.2f}-{q.fpr.max():.2f}, chi2={chi:.1f}, df={len(q)-1}, P={pv:.2g}")
out.append(d[d.alpha == 0.1].pivot_table(index=["task", "cohort"], columns=["model", "scoring"], values="fpr").round(3).to_string())
txt = "\n".join(out); open(os.path.join(HERE, "ensemble_check.txt"), "w").write(txt); print(txt)
