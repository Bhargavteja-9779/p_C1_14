"""P6: control augmentation (Wirbel et al. 2021) head-to-head on de-duplicated data. Same design as ../control_augmentation.py
(train on case-control cohorts + all DEV healthy populations as extra controls), evaluated on LOCKED healthy populations."""
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from multiprocessing import Pool
from common_v4 import *
from src.pipeline import Pipeline
A = 0.10; dev, lock = split()
def job(a):
    d, m = a; X, y, g, M = load(d); train = set(DISEASES[d]["studies"])
    Xs, ys, gs = [X], [y], [g]
    for s in dev:
        if s in train or s in dropped_studies() or not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
        Xc, md = controls(s); Xs.append(Xc); ys.append(np.zeros(len(Xc), int)); gs.append(np.array([s] * len(Xc)))
    XA = pd.concat(Xs).fillna(0.0); yA, gA = np.concatenate(ys), np.concatenate(gs); rows = []
    for aug in [False, True]:
        k = np.ones(len(yA), bool) if aug else np.isin(gA, list(train))
        p = Pipeline(m).fit(XA.values[k], yA[k], gA[k]); t = np.quantile(p.oof[p.y == 0], 1 - A)
        for s in populations(d, strict=False):
            if s not in lock: continue
            Xc, md = controls(s); sc = p.score(Xc.reindex(columns=XA.columns, fill_value=0).fillna(0).values); f = sc >= t
            rows.append(dict(disease=d, model=m, aug=aug, pop=s, n=len(sc), fpr=f.mean(),
                             strict=s not in STRICT_DROP_STUDIES, n_strict=int(md.strict_person.sum()), fpr_strict=f[md.strict_person.values].mean()))
    print(d, m, flush=True); return rows
if __name__ == "__main__":
    f = os.path.join(OUT, "control_augmentation_v4.csv"); assert not os.path.exists(f), "already run"
    with Pool(2) as P: res = P.map(job, [(d, m) for d in ["CRC", "IBD", "T2D"] for m in ["lasso", "rf"]])
    pd.DataFrame([r for x in res for r in x]).to_csv(f, index=False)
