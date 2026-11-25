"""CONFIRMATORY replication of protocol_v5 Addendum A (H5, H6). Run ONCE. Rules fixed before running:
- Replication populations: studies in v5_perpop_full.csv NOT in v5_perpop_strict.csv (all adult de-duplicated controls,
  n >= 20, training cohorts of each test already excluded by atlas_v5.py).
- H5 (LASSO, 14 tests): Spearman rho between distance-to-training-controls (same definition as explore_v5.py, computed on
  all controls of the population) and FPR across replication populations. A test with < 3 replication populations or an
  undefined rho counts as NOT positive (conservative). Supported if >= 9/14 positive AND one-sided sign test P < 0.05
  (over all 14 tests). WRONG if <= 7/14.
- H6 (LASSO): index = mean over the 14 tests of logit-FPR deviation from the test mean, test mean taken over replication +
  strict populations (strict populations use strict persons, as in v5_perpop_strict.csv). One-sided Mann-Whitney
  non-EUNA > EUNA among replication populations, P < 0.05. WRONG if median difference <= 0.
- RF: same computations, secondary.
Writes results/replication_v5.json, replication_v5_units.csv, replication_v5_index.csv."""
import os, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from common_v5 import *
import atlas_v5 as A5
OUTF = os.path.join(OUT5, "replication_v5.json"); assert not os.path.exists(OUTF), "already run (confirmatory, run once)"
full = pd.read_csv(os.path.join(OUT5, "v5_perpop_full.csv")); strict = pd.read_csv(os.path.join(OUT5, "v5_perpop_strict.csv"))
REP = sorted(set(full.study) - set(strict.study)); rep = full[full.study.isin(REP)].copy()
ctry = META.groupby("study_name").country.agg(lambda x: x.mode().iloc[0])
EUNA = {"GBR", "USA", "NLD", "DNK", "DEU", "SWE", "FRA", "ITA", "ESP", "AUT", "IRL", "FIN", "CAN", "ISR", "LUX", "NOR", "EST", "SVK", "KAZ"}
co = pd.read_csv(os.path.join(OUT5, "coefs_v5.csv")); units = []
for t in A5.TESTS:
    c = co[co.test == t]; case, studies = A5.TESTS[t]; X, y, g, M = A5.load_cc(case, studies)
    Z = lambda Xm: (np.log10(Xm.reindex(columns=c.taxon, fill_value=0).fillna(0).values / 100 + 1e-5) - c.mu.values) / c.sd.values
    z0 = Z(X[y == 0]).mean(0)
    for s in rep[rep.test == t].study.unique():
        Xc, md = controls(s); units.append(dict(test=t, study=s, dist=float(np.linalg.norm(Z(Xc).mean(0) - z0) / np.sqrt(len(z0)))))
U = rep.merge(pd.DataFrame(units), on=["test", "study"]); U["country"] = U.study.map(ctry); U["euna"] = U.country.isin(EUNA)
U.to_csv(os.path.join(OUT5, "replication_v5_units.csv"), index=False)
out = dict(replication_populations=REP, n_populations=len(REP), countries={s: ctry[s] for s in REP})
lg = lambda d: np.log((d.k + .5) / (d.n - d.k + .5))
IDX = []
for m in ["lasso", "rf"]:
    rows = {}
    for t in A5.TESTS:
        d = U[(U.test == t) & (U.model == m)]
        rho = stats.spearmanr(d.dist, d.fpr)[0] if len(d) >= 3 else np.nan
        rows[t] = dict(pops=len(d), rho=None if not np.isfinite(rho) else float(rho))
    pos = sum(1 for v in rows.values() if v["rho"] is not None and v["rho"] > 0)
    h5 = dict(tests=len(rows), positive=pos, sign_p_one_sided=float(stats.binomtest(pos, len(rows), alternative="greater").pvalue),
              median_rho=float(np.nanmedian([v["rho"] if v["rho"] is not None else np.nan for v in rows.values()])), per_test=rows)
    h5["verdict"] = "SUPPORTED" if (pos >= 9 and h5["sign_p_one_sided"] < .05) else ("WRONG" if pos <= 7 else "INCONCLUSIVE")
    # H6
    a = pd.concat([strict[strict.model == m].assign(set="strict"), rep[rep.model == m].assign(set="replication")])
    a["y"] = lg(a); a["dev"] = a.y - a.groupby("test").y.transform("mean")
    ix = a[a.set == "replication"].groupby("study").agg(index=("dev", "mean"), tests=("dev", "size")).reset_index()
    ix["country"] = ix.study.map(ctry); ix["euna"] = ix.country.isin(EUNA); ix["model"] = m; IDX.append(ix)
    o, e = ix[~ix.euna]["index"], ix[ix.euna]["index"]
    h6 = dict(n_other=len(o), n_euna=len(e), other_median=float(o.median()) if len(o) else None, euna_median=float(e.median()) if len(e) else None)
    if len(o) and len(e):
        h6["median_diff"] = h6["other_median"] - h6["euna_median"]; h6["mw_p_one_sided"] = float(stats.mannwhitneyu(o, e, alternative="greater").pvalue)
        h6["verdict"] = "SUPPORTED" if h6["mw_p_one_sided"] < .05 and h6["median_diff"] > 0 else ("WRONG" if h6["median_diff"] <= 0 else "INCONCLUSIVE")
    else: h6["verdict"] = "NOT TESTABLE (one group empty)"
    out[f"H5_{m}"], out[f"H6_{m}"] = h5, h6
pd.concat(IDX).to_csv(os.path.join(OUT5, "replication_v5_index.csv"), index=False)
json.dump(out, open(OUTF, "w"), indent=1, default=float)
for k in ["H5_lasso", "H6_lasso", "H5_rf", "H6_rf"]: print(k, {a: b for a, b in out[k].items() if a != "per_test"})
print(out["countries"])
