"""DEV ONLY. CRC classifier trained on 8 dev CRC cohorts. Methods judged on dev atlas cohorts (healthy FPR spread)
and on dev CRC LOSO (control FPR + case sensitivity)."""
import sys, os, numpy as np, pandas as pd; sys.path.insert(0, ".."); sys.path.insert(0, "../../..")
from common import *; from src.pipeline import Pipeline, make, logit, _log
from sklearn.model_selection import GroupKFold
A = 0.10
dev_atlas, _ = split()
X, y, g, M = load("CRC", DEV_CRC)
res = []
for model in ["lasso", "rf"]:
    p = Pipeline(model).fit(X.values, y, g)
    # fold models for OOF scores of dev CRC (needed to score with same model the residual method)
    Z = (_log(X.values, p.keep) - p.mu) / p.sd
    oof = p.oof
    H = {s: healthy(s) for s in dev_atlas}
    HZ = {s: (_log(H[s][0].reindex(columns=X.columns, fill_value=0).fillna(0).values, p.keep) - p.mu) / p.sd for s in H}
    HS = {s: logit(p.m.predict_proba(HZ[s])[:, 1]) for s in H}
    t0 = np.quantile(oof[y == 0], 1 - A)
    allH = np.concatenate(list(HS.values()))
    for k in [0, 2, 5, 10, 20, 50]:
        # leave-one-atlas-cohort-out: PCA + linear model of healthy score on PCs from other dev atlas cohorts
        fpr = {}
        for s in dev_atlas:
            if len(HS[s]) < 15: continue
            ref = [o for o in dev_atlas if o != s]
            Zr = np.vstack([HZ[o] for o in ref]); Sr = np.concatenate([HS[o] for o in ref])
            if k == 0:
                thr = np.quantile(Sr, 1 - A); fpr[s] = np.mean(HS[s] >= thr); continue
            mu = Zr.mean(0); U, S_, Vt = np.linalg.svd(Zr - mu, full_matrices=False); V = Vt[:k].T
            P = (Zr - mu) @ V; P1 = np.c_[np.ones(len(P)), P]; beta = np.linalg.lstsq(P1, Sr, rcond=None)[0]
            res_r = Sr - P1 @ beta; thr = np.quantile(res_r, 1 - A)
            Pt = np.c_[np.ones(len(HZ[s])), (HZ[s] - mu) @ V]; fpr[s] = np.mean(HS[s] - Pt @ beta >= thr)
        # CRC dev LOSO sensitivity with the same residual (reference = all dev atlas cohorts)
        Zr = np.vstack(list(HZ.values())); Sr = allH
        if k == 0: adj_oof = oof; thr = np.quantile(Sr, 1 - A)
        else:
            mu = Zr.mean(0); U, S_, Vt = np.linalg.svd(Zr - mu, full_matrices=False); V = Vt[:k].T
            P1 = np.c_[np.ones(len(Zr)), (Zr - mu) @ V]; beta = np.linalg.lstsq(P1, Sr, rcond=None)[0]
            thr = np.quantile(Sr - P1 @ beta, 1 - A); adj_oof = oof - np.c_[np.ones(len(Z)), (Z - mu) @ V] @ beta
        from sklearn.metrics import roc_auc_score
        cc = [(c, np.mean(adj_oof[(g == c) & (y == 0)] >= thr), np.mean(adj_oof[(g == c) & (y == 1)] >= thr), roc_auc_score(y[g == c], adj_oof[g == c])) for c in np.unique(g)]
        f = np.array(list(fpr.values()))
        res.append(dict(model=model, k=k, atlas_sd=f.std(), atlas_inband=np.mean((f >= .05) & (f <= .15)), atlas_mad=np.mean(abs(f - A)),
                        crc_ctrl_fpr_sd=np.std([c[1] for c in cc]), crc_ctrl_mad=np.mean([abs(c[1] - A) for c in cc]), crc_sens=np.mean([c[2] for c in cc]), crc_auc=np.mean([c[3] for c in cc])))
        print(res[-1], flush=True)
pd.DataFrame(res).to_csv("explore_r1.csv", index=False)
