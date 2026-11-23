"""DEV ONLY. Round 3: PAC local-control threshold; label-free contamination-bounded quantile. Uses scores_dev.npz."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import DEV_CRC
from src import calibrate as C
D = os.path.dirname(__file__); Z = np.load(os.path.join(D, "scores_dev.npz"))
alpha = 0.10; R = 300; rng = np.random.default_rng(3); rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        s_src, y_src, st, yt = (Z[f"{model}|{s}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"])
        i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        for r in range(R):
            p0 = rng.permutation(i0); h = len(p0) // 2; pool0, e0 = p0[:h], p0[h:]
            res = {}
            for n in [10, 20]:
                if n <= h:
                    res[f"conf_n{n}"] = C.local_controls_conformal(alpha, st[pool0[:n]])
                    res[f"pac_n{n}"] = C.pac_controls(st[pool0[:n]])
            res["pac_all"] = C.pac_controls(st[pool0]); res["conf_all"] = C.local_controls_conformal(alpha, st[pool0])
            for k, t in res.items():
                rows.append(dict(model=model, cohort=s, rep=r, pi="ctrl", method=k, fpr=(st[e0] >= t).mean(), sens=(st[i1] >= t).mean(), m=h))
            for pi in [0.0, 0.01, 0.05, 0.10]:
                n1 = rng.binomial(h, pi) if pi > 0 else 0
                u = st[np.concatenate([pool0, rng.choice(i1, n1, replace=False)])]
                ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                           contam02=C.contam_quantile(u, alpha, 0.02), contam05=C.contam_quantile(u, alpha, 0.05),
                           contam10=C.contam_quantile(u, alpha, 0.10))
                for k, t in ths.items():
                    rows.append(dict(model=model, cohort=s, rep=r, pi=str(pi), method=k, fpr=(st[e0] >= t).mean(), sens=(st[i1] >= t).mean(), m=len(u)))
d = pd.DataFrame(rows); d.to_csv(os.path.join(D, "explore_v3.csv.gz"), index=False)
d["abs_err"] = (d.fpr - alpha).abs(); d["over15"] = d.fpr > 0.15; d["inf"] = ~np.isfinite(d.fpr) | (d.sens == 0)
print("pool size per cohort (controls in pool half):", d[d.pi == "ctrl"].groupby("cohort").m.first().to_dict())
agg = d.groupby(["model", "pi", "method"]).agg(fpr=("fpr", "mean"), abs_err=("abs_err", "mean"), p_over15=("over15", "mean"), sens=("sens", "mean"))
print(agg.round(3).to_string())
c = d[(d.pi == "0.05")].groupby(["model", "cohort", "method"]).over15.mean().unstack().round(2)
print("\nP(FPR>0.15) per cohort, true pi=0.05\n", c.to_string())
