"""DEV ONLY. Round 4: verified-positive recalibration vs label-free / labelled baselines. Uses scores_dev.npz."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import DEV_CRC
from src import calibrate as C
D = os.path.dirname(__file__); Z = np.load(os.path.join(D, "scores_dev.npz"))
alpha = 0.10; R = 300; rng = np.random.default_rng(4); rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        s_src, y_src, st, yt = (Z[f"{model}|{s}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"])
        i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        for r in range(R):
            p0, p1 = rng.permutation(i0), rng.permutation(i1); h = len(p0) // 2; pool0, e0 = p0[:h], p0[h:]
            h1 = len(p1) // 2; pc, e1 = p1[:h1], p1[h1:]          # disjoint cases: pool vs evaluation
            for pi in [0.0, 0.01, 0.05, 0.10, 0.30]:
                n1 = min(rng.binomial(h, pi / (1 - pi)) if pi > 0 else 0, h1)
                idx = np.concatenate([pool0, pc[:n1]]); u = st[idx]; lab = yt[idx]
                pim = max(0.05, pi)                                   # programme's prevalence upper bound
                ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                           contam=C.contam_quantile(u, alpha, pim), oracle_pool=C.local_controls_conformal(alpha, st[pool0]))
                for name, t0 in [("vp_src", min(ths["source"], C.contam_quantile(u, 2 * alpha, pim))),
                                 ("vp_2a", C.contam_quantile(u, 2 * alpha, pim)), ("vp_3a", C.contam_quantile(u, 3 * alpha, pim))]:
                    t, nref = C.verified_positive(u, lab, alpha, pim, t0); ths[name] = t
                    rows.append(dict(model=model, cohort=s, rep=r, pi=pi, method=name + "_burn", fpr=np.nan, sens=np.nan, refer=nref / len(u)))
                for k, t in ths.items():
                    rows.append(dict(model=model, cohort=s, rep=r, pi=pi, method=k, fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean(), refer=np.nan))
d = pd.DataFrame(rows); d.to_csv(os.path.join(D, "explore_v4.csv.gz"), index=False)
d["abs_err"] = (d.fpr - alpha).abs()
agg = d.groupby(["model", "pi", "method"]).agg(fpr=("fpr", "mean"), abs_err=("abs_err", "mean"), sens=("sens", "mean"), refer=("refer", "mean"))
print(agg.round(3).to_string())
print("\nper-cohort mean FPR, pi=0.05\n", d[(d.pi == 0.05) & d.fpr.notna()].groupby(["model", "cohort", "method"]).fpr.mean().unstack().round(3).to_string())
