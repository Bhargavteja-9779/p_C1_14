"""Protocol v5 addendum A: replication of H5 (distance tracks FPR) and H6 (non-EUNA over-flagged) on the
NON-strict populations (full set minus strict-set studies). Writes results/replicate_v5.json."""
import os, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from common_v5 import *
import atlas_v5 as A5
from explore_v5 import EUNA, ctry
r = pd.read_csv(os.path.join(OUT5, "atlas_rows_v5.csv.gz"))
rep = r[r.study.isin(STRICT_DROP_STUDIES)]
per = rep.groupby(["test", "model", "study"]).agg(n=("flag", "size"), k=("flag", "sum")).reset_index(); per = per[per.n >= MIN_N]; per["fpr"] = per.k / per.n
co = pd.read_csv(os.path.join(OUT5, "coefs_v5.csv")); units = []
for t in A5.TESTS:
    c = co[co.test == t]; case, studies = A5.TESTS[t]; X, y, g, M = A5.load_cc(case, studies)
    Z = lambda Xm: (np.log10(Xm.reindex(columns=c.taxon, fill_value=0).fillna(0).values / 100 + 1e-5) - c.mu.values) / c.sd.values
    z0 = Z(X[y == 0]).mean(0)
    for s in per[per.test == t].study.unique():
        Xc, md = controls(s); units.append(dict(test=t, study=s, dist=float(np.linalg.norm(Z(Xc).mean(0) - z0) / np.sqrt(len(z0)))))
U = pd.DataFrame(units).merge(per, on=["test", "study"]); U.to_csv(os.path.join(OUT5, "replicate_v5_units.csv"), index=False); out = {}
for m in ["lasso", "rf"]:
    rho = U[U.model == m].groupby("test").apply(lambda d: stats.spearmanr(d.dist, d.fpr)[0] if len(d) >= 5 else np.nan).dropna()
    pos = int((rho > 0).sum()); out[f"H5_{m}"] = dict(tests=len(rho), positive=pos, median_rho=float(rho.median()), sign_p_one_sided=float(stats.binomtest(pos, len(rho), alternative="greater").pvalue),
                                                       populations=int(U[U.model == m].study.nunique()), per_test=rho.round(2).to_dict())
    S = pd.read_csv(os.path.join(OUT5, "v5_perpop_strict.csv")); S = S[S.model == m]; allp = pd.concat([S.assign(rep=False), per[per.model == m].assign(rep=True)])
    allp["y"] = np.log((allp.k + .5) / (allp.n - allp.k + .5)); allp["dev"] = allp.y - allp.groupby("test").y.transform("mean")
    idx = allp[allp.rep].groupby("study").dev.mean(); eu = idx.index.map(ctry).isin(EUNA)
    a, b = idx[~eu], idx[eu]
    out[f"H6_{m}"] = dict(non_euna=len(a), euna=len(b), median_non_euna=float(a.median()) if len(a) else None, median_euna=float(b.median()) if len(b) else None,
                          p_one_sided=float(stats.mannwhitneyu(a, b, alternative="greater").pvalue) if len(a) and len(b) else None, index=idx.round(2).to_dict())
json.dump(out, open(os.path.join(OUT5, "replicate_v5.json"), "w"), indent=1, default=float)
for k, v in out.items(): print(k, {x: (round(y, 3) if isinstance(y, float) else y) for x, y in v.items() if x not in ("per_test", "index")})
print(out["H6_lasso"]["index"])
