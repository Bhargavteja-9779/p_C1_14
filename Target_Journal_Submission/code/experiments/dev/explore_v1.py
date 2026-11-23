"""DEV ONLY (8 development CRC cohorts). Compare threshold-transfer methods. Round 1 of D6 log."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score
from src import calibrate as C
from sklearn.metrics import roc_auc_score
alpha = 0.10; R = 100; rng = np.random.default_rng(1)
X, y, g, M = load("CRC", DEV_CRC); X = X.values
rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        te = g == s; tr = ~te
        s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
        yt = y[te]; auc = roc_auc_score(yt, st)
        i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        for r in range(R):
            p0, p1 = rng.permutation(i0), rng.permutation(i1)
            c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
            for pi in [0.0, 0.05, 0.2, "nat"]:
                n1 = len(c1) if pi == "nat" else int(round(pi * len(c0) / (1 - pi)))
                u = st[np.concatenate([c0, c1[:n1]])]
                ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                           em=C.em_label_shift(s_src, y_src, alpha, u=u), shift=C.site_shift(s_src, y_src, alpha, u=u),
                           ctrl10=C.local_controls_conformal(alpha, st[c0[:10]]))
                for k, t in ths.items():
                    rows.append(dict(model=model, cohort=s, auc=auc, rep=r, pi=str(pi), method=k,
                                     fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean()))
        print(model, s, round(auc, 3), flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), "explore_v1.csv"), index=False)
d["abs_err"] = (d.fpr - alpha).abs()
print(d.groupby(["model", "pi", "method"])[["fpr", "abs_err", "sens"]].mean().round(3).unstack("method").to_string())
