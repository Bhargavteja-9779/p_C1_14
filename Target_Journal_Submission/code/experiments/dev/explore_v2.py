"""DEV ONLY. Round 2 of D6 log: local-control protocols vs label-free and batch-standardisation baselines."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score, train_and_score_cohortstd
from src import calibrate as C
alpha = 0.10; R = int(os.environ.get("R", 100)); rng = np.random.default_rng(2)
X, y, g, M = load("CRC", DEV_CRC); X = X.values
rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        te = g == s; tr = ~te
        s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
        _, _, st_cs, _ = train_and_score_cohortstd(X, y, g, tr, te, model)
        s_cs_src, y_cs = train_and_score_cohortstd(X, y, g, tr, te, model)[:2]
        yt = y[te]; i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        for r in range(R):
            p0 = rng.permutation(i0); cal, ev0 = p0[: len(p0) // 2], p0[len(p0) // 2:]
            ev1 = i1
            def add(meth, t, n, sc=st):
                rows.append(dict(model=model, cohort=s, rep=r, method=meth, n=n, fpr=(sc[ev0] >= t).mean(), sens=(sc[ev1] >= t).mean()))
            add("source", C.source_threshold(s_src, y_src, alpha), 0)
            add("cohortstd_source", C.source_threshold(s_cs_src, y_cs, alpha), 0, st_cs)
            u = st[np.concatenate([cal, i1])]  # natural-prevalence unlabeled pool (cases not in cal)
            add("pool_q_nat", C.local_quantile(None, None, alpha, u=u), 0)
            add("pool_q_ctrl", C.local_quantile(None, None, alpha, u=st[cal]), len(cal))
            for n in [10, 20, len(cal)]:
                c = st[cal[:n]]
                add("conformal", C.local_controls_conformal(alpha, c), n)
                add("tong95", C.tong_threshold(alpha, c, 0.05), n)
                add("anchor_loc", C.control_anchored(s_src, y_src, alpha, c), n)
                add("anchor_locscale", C.control_anchored(s_src, y_src, alpha, c, scale=True), n)
        print(model, s, flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), "explore_v2.csv"), index=False)
d["n"] = np.where(d.n > 20, "all", d.n.astype(str)); d["ae"] = (d.fpr - alpha).abs(); d["over15"] = d.fpr > 0.15
print(d.groupby(["model", "method", "n"])[["fpr", "ae", "over15", "sens"]].mean().round(3).to_string())
c = d[(d.n.isin(["0", "all"]))].groupby(["model", "method", "cohort"]).fpr.mean().unstack().round(2)
print(c.to_string())
