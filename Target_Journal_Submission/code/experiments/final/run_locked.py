"""LOCKED RUN — implements experiments/protocol.md exactly. Run once."""
import sys, os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load, DEV_CRC, LOCKED_CRC
from src.models import train_and_score, train_and_score_cohortstd
from src import calibrate as C
from sklearn.metrics import roc_auc_score
R = 200; R_SLOW = 20; ALPHAS = [0.10, 0.05]; rng = np.random.default_rng(20261123)
os.makedirs(os.path.join(HERE, "scores"), exist_ok=True)

def tasks():
    X, y, g, _ = load("CRC"); X = X.values
    for s in LOCKED_CRC: yield "CRC", X, y, g, s, np.isin(g, DEV_CRC)
    for d in ["IBD", "T2D", "adenoma"]:
        X, y, g, _ = load(d); X = X.values
        for s in np.unique(g): yield d, X, y, g, s, g != s

rows, info = [], []
for task, X, y, g, s, tr in tasks():
    te = g == s
    for model in ["lasso", "rf"]:
        s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
        cs_src, cy_src, cst, _ = train_and_score_cohortstd(X, y, g, tr, te, model)
        yt = y[te]; np.savez(os.path.join(HERE, "scores", f"{task}_{s}_{model}.npz"), s_src=s_src, y_src=y_src, st=st, yt=yt, cs_src=cs_src, cst=cst)
        i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        info.append(dict(task=task, cohort=s, model=model, n0=len(i0), n1=len(i1), auc=roc_auc_score(yt, st), auc_cohortstd=roc_auc_score(yt, cst)))
        for alpha in ALPHAS:
            # full-cohort status-quo counts (for overdispersion test)
            t_src = C.source_threshold(s_src, y_src, alpha)
            info[-1][f"fp_full_{alpha}"] = int((st[i0] >= t_src).sum())
            for r in range(R):
                p0 = rng.permutation(i0); cal, ev0 = p0[: len(p0) // 2], p0[len(p0) // 2:]
                u = st[np.concatenate([cal, i1])]
                def add(meth, t, n=0, sc=st):
                    rows.append(dict(task=task, cohort=s, model=model, alpha=alpha, rep=r, method=meth, n=n,
                                     fpr=float((sc[ev0] >= t).mean()), sens=float((sc[i1] >= t).mean())))
                add("source", t_src)
                add("cohortstd", C.source_threshold(cs_src, cy_src, alpha), sc=cst)
                add("pool_q", np.quantile(u, 1 - alpha))
                if r < R_SLOW:
                    add("em", C.em_label_shift(s_src, y_src, alpha, u=u))
                    add("site_shift", C.site_shift(s_src, y_src, alpha, u=u))
                for n in [10, 20, 30]:
                    if len(cal) < n: continue
                    c = st[cal[:n]]
                    add("conformal", C.local_controls_conformal(alpha, c), n)
                    add("anchor_loc", C.control_anchored(s_src, y_src, alpha, c), n)
                    add("anchor_locscale", C.control_anchored(s_src, y_src, alpha, c, scale=True), n)
                for n in [30, 50]:
                    if len(cal) >= n: add("tong95", C.tong_threshold(alpha, st[cal[:n]], 0.05), n)
        print(task, s, model, round(info[-1]["auc"], 3), flush=True)
pd.DataFrame(rows).to_csv(os.path.join(HERE, "locked_rows.csv.gz"), index=False)
pd.DataFrame(info).to_csv(os.path.join(HERE, "locked_cohorts.csv"), index=False)
