"""DEV exploration (cycle 5): does geography-stable feature penalisation (GSP) reduce FPR spread across held-out DEV
healthy populations without losing AUROC? Cross-fitted: ICC from DEV half A, evaluate on DEV half B, and swap.
LOCKED healthy populations are not touched. Writes results/dev_gsp.csv."""
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from multiprocessing import Pool
from sklearn.metrics import roc_auc_score
from common_v5 import *
from src.pipeline import _log
dev, lock = split(); rng = np.random.default_rng(5)
def job(a):
    d, m = a; X, y, g, M = load(d); pops = [p for p in populations(d, strict=False) if p in dev]
    H = {}
    for p in pops:
        Xc, md = controls(p); H[p] = Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0).values
    perm = list(rng.permutation(pops)); halves = [perm[::2], perm[1::2]]; rows = []
    keep_all = np.ones(X.shape[1], bool)
    for h in range(2):
        A_, B_ = halves[h], halves[1 - h]
        icc = feature_icc([_log(H[p], keep_all) for p in A_])
        for gamma, dq in [(0, None), (1, None), (2, None), (4, None), (8, None), (0, .9), (0, .75), (0, .5)]:
            if m == "rf" and gamma > 0: continue
            mdl = GSP(m, icc, gamma, dq).fit(X.values, y, g); auc = roc_auc_score(y, mdl.oof)
            fpr = {p: float(np.mean(mdl.score(H[p]) >= mdl.t)) for p in B_}
            for p, f in fpr.items(): rows.append(dict(disease=d, model=m, half=h, gamma=gamma, drop_q=dq, auc_loco=auc, pop=p, n=len(H[p]), fpr=f))
    print(d, m, flush=True); return rows
if __name__ == "__main__":
    with Pool(4) as P: res = P.map(job, [(d, m) for d in ["CRC", "IBD", "T2D"] for m in ["lasso", "rf"]])
    o = pd.DataFrame([r for x in res for r in x]); o.to_csv(os.path.join(OUT5, "dev_gsp.csv"), index=False)
    o["err"] = (o.fpr - A).abs(); o["out"] = (o.fpr < .05) | (o.fpr > .15)
    s = o.groupby(["disease", "model", "gamma", "drop_q"], dropna=False).agg(auc=("auc_loco", "mean"), mad=("err", "mean"), sd=("fpr", "std"), oob=("out", "mean"), mx=("fpr", "max")).reset_index()
    pd.set_option("display.width", 200); print(s.round(3).to_string())
