"""EXPLORATORY (cycle 5, not in protocol_v5): (1) population false-alarm index by lifestyle/region; (2) does a
population's compositional distance from a test's training controls track its FPR (all 28 tests)?
Distance = Euclidean distance between centroids of z-scored log-abundance (model taxa, training-control scaling).
Writes results/explore_v5.json, explore_v5_units.csv."""
import os, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from common_v5 import *
import atlas_v5 as A5
per = pd.read_csv(os.path.join(OUT5, "v5_perpop_strict.csv")); out = {}
nw = META.groupby("study_name").non_westernized.agg(lambda x: (x == "yes").mean() > .5); ctry = META.groupby("study_name").country.agg(lambda x: x.mode().iloc[0])
EUNA = {"GBR", "USA", "NLD", "DNK", "DEU", "SWE", "FRA", "ITA", "ESP", "AUT", "IRL", "FIN", "CAN", "ISR", "LUX", "NOR", "EST", "SVK", "KAZ"}
for m in ["lasso", "rf"]:
    p = pd.read_csv(os.path.join(OUT5, f"v5_popindex_strict_{m}.csv")); p["nw"] = p.study.map(nw); p["euna"] = p.study.map(ctry).isin(EUNA)
    out[f"index_{m}"] = dict(nonwest_median=float(p[p.nw]["index"].median()), west_median=float(p[~p.nw]["index"].median()), p_nw=float(stats.mannwhitneyu(p[p.nw]["index"], p[~p.nw]["index"]).pvalue),
                             euna_median=float(p[p.euna]["index"].median()), other_median=float(p[~p.euna]["index"].median()), p_euna=float(stats.mannwhitneyu(p[p.euna]["index"], p[~p.euna]["index"]).pvalue),
                             n_nw=int(p.nw.sum()), n_euna=int(p.euna.sum()), n=len(p))
co = pd.read_csv(os.path.join(OUT5, "coefs_v5.csv")); units = []
for t in A5.TESTS:
    c = co[co.test == t]; case, studies = A5.TESTS[t]; X, y, g, M = A5.load_cc(case, studies)
    Z = lambda Xm: (np.log10(Xm.reindex(columns=c.taxon, fill_value=0).fillna(0).values / 100 + 1e-5) - c.mu.values) / c.sd.values
    z0 = Z(X[y == 0]).mean(0)
    for s in per[per.test == t].study.unique():
        Xc, md = controls(s); zc = Z(Xc[md.strict_person.values]).mean(0)
        units.append(dict(test=t, study=s, dist=float(np.linalg.norm(zc - z0) / np.sqrt(len(z0)))))
U = pd.DataFrame(units).merge(per, on=["test", "study"]); U["err"] = (U.fpr - A).abs(); U["lfpr"] = np.log((U.k + .5) / (U.n - U.k + .5))
U.to_csv(os.path.join(OUT5, "explore_v5_units.csv"), index=False)
for m in ["lasso", "rf"]:
    rho = U[U.model == m].groupby("test").apply(lambda d: pd.Series(dict(rho_fpr=stats.spearmanr(d.dist, d.fpr)[0], rho_err=stats.spearmanr(d.dist, d.err)[0])))
    out[f"dist_{m}"] = dict(tests=len(rho), median_rho_fpr=float(rho.rho_fpr.median()), pos_fpr=int((rho.rho_fpr > 0).sum()), sign_p_fpr=float(stats.binomtest(int((rho.rho_fpr > 0).sum()), len(rho)).pvalue),
                            median_rho_err=float(rho.rho_err.median()), pos_err=int((rho.rho_err > 0).sum()), sign_p_err=float(stats.binomtest(int((rho.rho_err > 0).sum()), len(rho)).pvalue),
                            per_test=rho.round(2).to_dict("index"))
json.dump(out, open(os.path.join(OUT5, "explore_v5.json"), "w"), indent=1, default=float)
for k, v in out.items(): print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items() if a != "per_test"})
