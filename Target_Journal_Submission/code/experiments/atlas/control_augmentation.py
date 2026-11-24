"""POST HOC comparator (added after prior-art check, 2026-11-24): control augmentation (Wirbel et al. 2021 Genome Biol).
Train each classifier on its case-control cohorts PLUS all DEV-split healthy atlas cohorts (as controls, one group each);
cut-off = 90th pct of leave-one-cohort-out OOF control scores. Evaluate realised FPR on LOCKED healthy populations, and for
CRC the sensitivity/FPR on locked external YachidaS_2019 / YuJ_2015 (training = 8 dev CRC cohorts + dev atlas)."""
import sys, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "."); sys.path.insert(0, "../..")
from common import *; from src.pipeline import Pipeline
from multiprocessing import Pool
from sklearn.metrics import roc_auc_score
A = 0.10; dev, lock = split()
def build(disease, studies=None):
    X, y, g, M = load(disease, studies); train = set(DISEASES[disease]["studies"]) | {"ThomasAM_2019_c"}
    Xs, ys, gs = [X], [y], [g]
    for s in dev:
        if s in train: continue
        Xc, md = healthy(s); Xs.append(Xc); ys.append(np.zeros(len(Xc), int)); gs.append(np.array([s] * len(Xc)))
    XA = pd.concat(Xs).fillna(0.0); return XA, np.concatenate(ys), np.concatenate(gs), train
def job(a):
    disease, model = a; rows = []
    XA, yA, gA, train = build(disease)
    for aug in [False, True]:
        keep = np.ones(len(yA), bool) if aug else np.isin(gA, list(train))
        p = Pipeline(model).fit(XA.values[keep], yA[keep], gA[keep]); t = np.quantile(p.oof[p.y == 0], 1 - A)
        for s in lock:
            if s in train: continue
            Xc, md = healthy(s); sc = p.score(Xc.reindex(columns=XA.columns, fill_value=0).fillna(0).values)
            rows.append(dict(disease=disease, model=model, aug=aug, kind="healthy", pop=s, n=len(sc), fpr=np.mean(sc >= t)))
    if disease == "CRC":
        XA2, yA2, gA2, _ = build("CRC", DEV_CRC + LOCKED_CRC)
        for aug in [False, True]:
            tr = np.isin(gA2, DEV_CRC) | (aug & ~np.isin(gA2, DEV_CRC + LOCKED_CRC))
            p = Pipeline(model).fit(XA2.values[tr], yA2[tr], gA2[tr]); t = np.quantile(p.oof[p.y == 0], 1 - A)
            for c in LOCKED_CRC:
                i = gA2 == c; sc = p.score(XA2.values[i]); yy = yA2[i]
                rows.append(dict(disease=disease, model=model, aug=aug, kind="casecontrol", pop=c, n=i.sum(), fpr=np.mean(sc[yy == 0] >= t),
                                 sens=np.mean(sc[yy == 1] >= t), auc=roc_auc_score(yy, sc)))
    print(disease, model, flush=True); return rows
if __name__ == "__main__":
    with Pool(3) as P: res = P.map(job, [(d, m) for d in ["CRC", "IBD", "T2D"] for m in ["lasso", "rf"]])
    o = pd.DataFrame([r for x in res for r in x]); o.to_csv("results/control_augmentation.csv", index=False)
    h = o[(o.kind == "healthy") & (o.n >= 15)]
    print(h.groupby(["disease", "model", "aug"]).fpr.agg(n="size", mad=lambda x: np.mean(abs(x - A)), inband=lambda x: np.mean((x >= .05) & (x <= .15)),
                                                         sd="std", lo="min", hi="max").round(3).to_string())
    print(o[o.kind == "casecontrol"].round(3).to_string())
