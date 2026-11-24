"""DEV ONLY (8 development CRC cohorts). Round 2 of D6 log: adds MLLS-BCTS, DyS, 2-Gaussian, bounded site-shift (v2),
hybrid (v2 + 10 labelled local controls), conformal with 10/20 controls, per-site feature standardisation.
Usage: python explore_v2.py <model> [R]"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score, train_and_score_featstd
from src import calibrate as C
from sklearn.metrics import roc_auc_score
model = sys.argv[1]; R = int(sys.argv[2]) if len(sys.argv) > 2 else 50
alpha = 0.10; rng = np.random.default_rng(2)
X, y, g, M = load("CRC", DEV_CRC); X = X.values
rows = []
for s in DEV_CRC:
    te = g == s; tr = ~te
    s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
    f_src, fy_src, ft, _ = train_and_score_featstd(X, y, g, tr, te, model)
    yt = y[te]; auc = roc_auc_score(yt, st); auc_f = roc_auc_score(yt, ft)
    i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(R):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        lc = p0[len(p0) // 2:][:0]  # placeholder
        for pi in [0.0, 0.05, 0.2, "nat"]:
            n1 = len(c1) if pi == "nat" else int(round(pi * len(c0) / (1 - pi)))
            u = st[np.concatenate([c0, c1[:n1]])]
            # labelled local controls drawn from the calibration controls (subset of the pool, as in practice)
            ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                       em=C.em_label_shift(s_src, y_src, alpha, u=u), mlls=C.mlls_bcts(s_src, y_src, alpha, u=u),
                       dys=C.dys(s_src, y_src, alpha, u=u), gauss2=C.gauss2(s_src, y_src, alpha, u=u),
                       shift2=C.site_shift_v2(s_src, y_src, alpha, u=u),
                       hybrid10=C.site_shift_v2(s_src, y_src, alpha, u=u, c=st[c0[:10]]),
                       ctrl10=C.local_controls_conformal(alpha, st[c0[:10]]),
                       ctrl20=C.local_controls_conformal(alpha, st[c0[:20]]))
            for k, t in ths.items():
                rows.append(dict(model=model, cohort=s, auc=auc, rep=r, pi=str(pi), method=k,
                                 fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean()))
            tf = C.source_threshold(f_src, fy_src, alpha)
            rows.append(dict(model=model, cohort=s, auc=auc_f, rep=r, pi=str(pi), method="featstd",
                             fpr=(ft[e0] >= tf).mean(), sens=(ft[e1] >= tf).mean()))
    print(model, s, round(auc, 3), "featstd auc", round(auc_f, 3), flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), f"explore_v2_{model}.csv"), index=False)
d["abs_err"] = (d.fpr - alpha).abs()
print(d.groupby(["pi", "method"])[["fpr", "abs_err", "sens"]].mean().round(3).to_string())
print(d.groupby(["pi", "method", "cohort"]).fpr.mean().groupby(["pi", "method"]).agg(lambda v: np.sqrt(np.mean((v - alpha) ** 2))).round(3).unstack("pi").to_string())
