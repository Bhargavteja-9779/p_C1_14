"""DEV ONLY (8 development CRC cohorts). Round 3 of D6 log: fair per-site feature standardisation (pool statistics
only), location-only and location-scale anchoring with 10 local controls, prevalence grid incl. 1% (screening).
Usage: python explore_v3.py <model> [R]"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score, train_and_score_featstd
from src import calibrate as C
from sklearn.metrics import roc_auc_score
model = sys.argv[1]; R = int(sys.argv[2]) if len(sys.argv) > 2 else 50
alpha = 0.10; rng = np.random.default_rng(3)
X, y, g, M = load("CRC", DEV_CRC); X = X.values
rows = []
for s in DEV_CRC:
    te = g == s; tr = ~te
    s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
    f_src, fy_src, scorer = train_and_score_featstd(X, y, g, tr, te, model)
    yt = y[te]; auc = roc_auc_score(yt, st)
    i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(R):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        lc = st[c0[:10]]
        for pi in [0.0, 0.01, 0.05, 0.2, "nat"]:
            n1 = len(c1) if pi == "nat" else int(round(pi * len(c0) / (1 - pi)))
            pool = np.concatenate([c0, c1[:n1]]); u = st[pool]
            ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                       shift2=C.site_shift_v2(s_src, y_src, alpha, u=u), hybrid10=C.site_shift_v2(s_src, y_src, alpha, u=u, c=lc),
                       ctrl10=C.local_controls_conformal(alpha, lc), anchor10=C.anchor(s_src, y_src, alpha, lc),
                       anchorloc10=C.anchor_loc(s_src, y_src, alpha, lc))
            for k, t in ths.items():
                rows.append(dict(model=model, cohort=s, auc=auc, rep=r, pi=str(pi), method=k,
                                 fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean()))
            tf = C.source_threshold(f_src, fy_src, alpha); fe0, fe1 = scorer(pool, e0), scorer(pool, e1)
            rows.append(dict(model=model, cohort=s, auc=auc, rep=r, pi=str(pi), method="featstd",
                             fpr=(fe0 >= tf).mean(), sens=(fe1 >= tf).mean()))
    print(model, s, round(auc, 3), flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), f"explore_v3_{model}.csv"), index=False)
d["abs_err"] = (d.fpr - alpha).abs(); d["over15"] = d.fpr > 0.15
print(d.groupby(["pi", "method"])[["fpr", "abs_err", "over15", "sens"]].mean().round(3).to_string())
print(d.groupby(["pi", "method", "cohort"]).fpr.mean().groupby(["pi", "method"]).agg(lambda v: np.sqrt(np.mean((v - alpha) ** 2))).round(3).unstack("pi").to_string())
