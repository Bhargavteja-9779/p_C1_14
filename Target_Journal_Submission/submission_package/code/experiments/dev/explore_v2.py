"""DEV ONLY. Round 2: few labelled local controls. Caches LOCO scores in scores_dev.npz."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score
from src import calibrate as C
D = os.path.dirname(__file__); cache = os.path.join(D, "scores_dev.npz")
alpha = 0.10; R = 200; rng = np.random.default_rng(2)
if not os.path.exists(cache):
    X, y, g, M = load("CRC", DEV_CRC); X = X.values; out = {}
    for model in ["lasso", "rf"]:
        for s in DEV_CRC:
            te = g == s; s_src, y_src, st, _ = train_and_score(X, y, g, ~te, te, model)
            out[f"{model}|{s}|src"] = s_src; out[f"{model}|{s}|ysrc"] = y_src
            out[f"{model}|{s}|tgt"] = st; out[f"{model}|{s}|ytgt"] = y[te]
    np.savez(cache, **out)
Z = np.load(cache); rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        s_src, y_src, st, yt = (Z[f"{model}|{s}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"])
        i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        for n in [5, 10, 20]:
            if n >= len(i0) - 5: continue
            for r in range(R):
                p0 = rng.permutation(i0); c, e0 = st[p0[:n]], st[p0[n:]]
                ths = dict(source=C.source_threshold(s_src, y_src, alpha),
                           conformal=C.local_controls_conformal(alpha, c), normal=C.ctrl_normal(alpha, c),
                           shift=C.ctrl_shift_transport(s_src, y_src, alpha, c), moment=C.ctrl_moment_transport(s_src, y_src, alpha, c),
                           robust=C.ctrl_robust_transport(s_src, y_src, alpha, c))
                for k, t in ths.items():
                    rows.append(dict(model=model, cohort=s, n=n, rep=r, method=k, fpr=(e0 >= t).mean(), sens=(st[i1] >= t).mean()))
d = pd.DataFrame(rows); d.to_csv(os.path.join(D, "explore_v2.csv.gz"), index=False)
d["abs_err"] = (d.fpr - alpha).abs(); d["over15"] = d.fpr > 0.15
agg = d.groupby(["model", "n", "method"]).agg(fpr=("fpr", "mean"), abs_err=("abs_err", "mean"), p_over15=("over15", "mean"), sens=("sens", "mean"))
print(agg.round(3).to_string())
# per-cohort bias for the shift method (does location-only suffice?)
print(d[d.n == 10].groupby(["model", "cohort", "method"]).fpr.mean().unstack().round(3).to_string())
