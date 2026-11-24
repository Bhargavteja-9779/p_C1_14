"""LOCKED FINAL TEST - run once with the frozen protocol (experiments/protocol.md). Usage: python run_final.py <model>"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC
from src.models import train_and_score, train_and_score_featstd
from src import calibrate as C
from sklearn.metrics import roc_auc_score
model = sys.argv[1]; R = 200; rng = np.random.default_rng(2026)
def tasks():
    X, y, g, _ = load("CRC", DEV_CRC + LOCKED_CRC)
    for s in LOCKED_CRC: yield "CRC", s, X.values, y, g, np.isin(g, DEV_CRC), g == s
    for dis in ["IBD", "T2D", "adenoma"]:
        X, y, g, _ = load(dis)
        for s in DISEASES[dis]["studies"]: yield dis, s, X.values, y, g, g != s, g == s
rows = []
for dis, s, X, y, g, tr, te in tasks():
    s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
    f_src, fy_src, scorer = train_and_score_featstd(X, y, g, tr, te, model)
    yt = y[te]; auc = roc_auc_score(yt, st); i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(R):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        for pi in [0.0, 0.01, 0.05, 0.2]:
            n1 = min(len(c1), int(round(pi * len(c0) / (1 - pi)))); pool = np.concatenate([c0, c1[:n1]]); u = st[pool]
            for alpha in [0.10, 0.05]:
                ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                           em=C.em_label_shift(s_src, y_src, alpha, u=u), mlls=C.mlls_bcts(s_src, y_src, alpha, u=u),
                           gauss2=C.gauss2(s_src, y_src, alpha, u=u), shift2=C.site_shift_v2(s_src, y_src, alpha, u=u),
                           ctrl10=C.local_controls_conformal(alpha, st[c0[:10]]),
                           rpoolmean=C.robust_pool_mean(s_src, y_src, alpha, u=u, pi_max=0.05),
                           rpool=C.robust_pool(s_src, y_src, alpha, u=u, delta=0.10, pi_max=0.05))
                for k, t in ths.items():
                    rows.append(dict(disease=dis, cohort=s, model=model, auc=auc, rep=r, pi=pi, alpha=alpha, method=k,
                                     n_pool=len(pool), fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean(), abstain=bool(np.isinf(t))))
                tf = C.source_threshold(f_src, fy_src, alpha)
                rows.append(dict(disease=dis, cohort=s, model=model, auc=auc, rep=r, pi=pi, alpha=alpha, method="featstd",
                                 n_pool=len(pool), fpr=(scorer(pool, e0) >= tf).mean(), sens=(scorer(pool, e1) >= tf).mean(), abstain=False))
    print(model, dis, s, "auc", round(auc, 3), "n0", len(i0), "n1", len(i1), flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(os.path.dirname(__file__), f"final_{model}.csv"), index=False)
print("FINISHED", flush=True)
