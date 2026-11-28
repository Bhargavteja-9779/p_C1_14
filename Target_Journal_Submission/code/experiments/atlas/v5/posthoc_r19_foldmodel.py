"""POST HOC (review r19, statistics M1): the atlas cut-off is the 90th percentile of OUT-OF-FOLD control scores, but
healthy populations were scored with the model REFITTED on all training data. This script (1) refits each of the 28
classifiers exactly as atlas_v5.py did and checks that its scores reproduce atlas_rows_v5 (same cut-off); (2) scores the
same people with the mean logit of the inner leave-one-cohort-out fold models (the models behind the cut-off), as in
plan v4 P7; (3) reports the refitted model's in-sample FPR on its own training controls; (4) recomputes the headline
atlas summaries (strict set) under fold-model scoring. Writes results/posthoc_r19_foldmodel{.json,_perpop.csv}."""
import os, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from multiprocessing import Pool
from scipy import stats
from sklearn.model_selection import GroupKFold, StratifiedKFold
from common_v5 import *
from src.pipeline import make, logit, _log
import atlas_v5 as A5
OUTJ = os.path.join(OUT5, "posthoc_r19_foldmodel.json"); OUTC = os.path.join(OUT5, "posthoc_r19_foldmodel_perpop.csv")
def job(a):
    name, model = a; case, studies = A5.TESTS[name]; X, y, g, M = A5.load_cc(case, studies); Xv = X.values
    keep = (Xv > 0).mean(0) > 0.05; L = _log(Xv, keep); mu, sd = L.mean(0), L.std(0) + 1e-6; Z = (L - mu) / sd
    ug = np.unique(g); folds = list(GroupKFold(len(ug)).split(Z, y, g) if len(ug) >= 3 else StratifiedKFold(5, shuffle=True, random_state=0).split(Z, y))
    oof = np.zeros(len(y)); fm = []
    for a_, b_ in folds:
        m = make(model, 0).fit(Z[a_], y[a_]); oof[b_] = m.predict_proba(Z[b_])[:, 1]; fm.append(m)
    full = make(model, 0).fit(Z, y); oof = logit(oof); t = float(np.quantile(oof[y == 0], 1 - A))
    insample_fpr = float(np.mean(logit(full.predict_proba(Z[y == 0])[:, 1]) >= t))
    rows = []
    for s in healthy_studies():
        if s in studies or s in dropped_studies() or not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
        Xc, md = controls(s)
        if len(Xc) < MIN_N: continue
        Zc = (_log(Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0).values, keep) - mu) / sd
        sr = logit(full.predict_proba(Zc)[:, 1]); sf = np.mean([logit(m.predict_proba(Zc)[:, 1]) for m in fm], axis=0)
        rows.append(pd.DataFrame(dict(test=name, model=model, study=s, sample_id=md.index, strict_person=md.strict_person.values, score_refit=sr, score_fold=sf, thr=t)))
    print(name, model, flush=True)
    return pd.concat(rows), dict(test=name, model=model, thr=t, folds=len(folds), insample_fpr_refit=insample_fpr)
def dl(k, n):
    yv = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * yv).sum() / w.sum(); Q = (w * (yv - mu) ** 2).sum(); df = len(yv) - 1
    t2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); ws = 1 / (v + t2); m2 = (ws * yv).sum() / ws.sum(); se = ws.sum() ** -.5; tq = stats.t.ppf(.975, len(yv) - 2); ex = lambda x: 1 / (1 + np.exp(-x))
    return dict(pooled=ex(m2), tau=np.sqrt(t2), I2=max(0, (Q - df) / Q), pi_hi=ex(m2 + tq * np.sqrt(t2 + se ** 2)))
if __name__ == "__main__":
    with Pool(4) as P: res = P.map(job, [(n, m) for n in A5.TESTS for m in ["lasso", "rf"]])
    R = pd.concat([r[0] for r in res]); info = pd.DataFrame([r[1] for r in res])
    ref = pd.read_csv(os.path.join(OUT5, "atlas_rows_v5.csv.gz"))
    chk = R.merge(ref[["test", "model", "study", "sample_id", "score", "thr"]], on=["test", "model", "study", "sample_id"], suffixes=("", "_atlas"))
    out = dict(reproduction=dict(rows=int(len(R)), matched=int(len(chk)), max_abs_score_diff=float((chk.score_refit - chk.score).abs().max()),
                                 max_abs_thr_diff=float((chk.thr - chk.thr_atlas).abs().max())))
    R["flag_refit"] = (R.score_refit >= R.thr).astype(int); R["flag_fold"] = (R.score_fold >= R.thr).astype(int)
    S = R[(R.strict_person == True) & ~R.study.isin(STRICT_DROP_STUDIES)]; S = S[S.groupby(["test", "model", "study"]).study.transform("size") >= MIN_N]
    per = S.groupby(["test", "model", "study"]).agg(n=("flag_fold", "size"), k_refit=("flag_refit", "sum"), k_fold=("flag_fold", "sum")).reset_index()
    per["fpr_refit"] = per.k_refit / per.n; per["fpr_fold"] = per.k_fold / per.n; per.to_csv(OUTC, index=False)
    T = pd.read_csv(os.path.join(OUT5, "tests_v5.csv"))
    for col in ["refit", "fold"]:
        het = pd.DataFrame([dict(test=t, model=m, **dl(g[f"k_{col}"].values, g.n.values)) for (t, m), g in per.groupby(["test", "model"])]).merge(T[["test", "model", "auroc"]], on=["test", "model"])
        big = per[per.n >= 100]
        out[col] = dict(I2_median=float(het.I2.median()), I2_ge_050=int((het.I2 >= .5).sum()), share_pairs_gt025={m: float((per[per.model == m][f"fpr_{col}"] > .25).mean()) for m in ["lasso", "rf"]},
                        share_pairs_gt025_all=float((per[f"fpr_{col}"] > .25).mean()),
                        range_n100=[float(big[f"fpr_{col}"].min()), float(big[f"fpr_{col}"].max())], range_n100_lasso_max=float(big[big.model == "lasso"][f"fpr_{col}"].max()),
                        pooled={f"{t}|{m}": float(p) for t, m, p in het[["test", "model", "pooled"]].values},
                        pooled_range={m: [float(het[het.model == m].pooled.min()), float(het[het.model == m].pooled.max())] for m in ["lasso", "rf"]},
                        pi_hi_lasso_range=[float(het[het.model == "lasso"].pi_hi.min()), float(het[het.model == "lasso"].pi_hi.max())],
                        spearman_auroc_tau=[float(x) for x in stats.spearmanr(het.auroc, het.tau)])
    out["pair_spearman_refit_vs_fold"] = float(stats.spearmanr(per.fpr_refit, per.fpr_fold)[0])
    out["pair_median_abs_diff"] = float((per.fpr_refit - per.fpr_fold).abs().median())
    out["insample_fpr_refit"] = {f"{a}|{b}": float(c) for a, b, c in info[["test", "model", "insample_fpr_refit"]].values}
    json.dump(out, open(OUTJ, "w"), indent=1); print(json.dumps({k: v for k, v in out.items() if k not in ("insample_fpr_refit",)}, indent=1, default=str)[:4000])
