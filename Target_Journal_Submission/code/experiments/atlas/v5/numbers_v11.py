"""Derived numbers quoted in manuscript_v11 that are not already in a result file. Writes results/numbers_v11.json."""
import os, json, numpy as np, pandas as pd
from scipy import stats
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); o = {}
p = pd.read_csv(os.path.join(R, "v5_perpop_strict.csv"))
def po(n): k = np.arange(n + 1); f = k / n; return stats.binom.pmf(k, n, .1)[(f < .05) | (f > .15)].sum()
p["exp"] = p.n.map(po); g = p.groupby(["test", "model"]).agg(exp=("exp", "mean"), obs=("fpr", lambda x: ((x < .05) | (x > .15)).mean()))
o["outside_band_expected_by_chance"] = [float(g.exp.min()), float(g.exp.max())]; o["outside_band_observed_median"] = float(g.obs.median()); o["outside_band_observed_range"] = [float(g.obs.min()), float(g.obs.max())]
L = p[p.model == "lasso"]; o["lasso_units"] = len(L); o["lasso_share_gt015"] = float((L.fpr > .15).mean()); o["lasso_share_gt025"] = float((L.fpr > .25).mean()); o["lasso_share_lt005"] = float((L.fpr < .05).mean())
B = L[L.n >= 100]; o["lasso_n100_fpr_range"] = [float(B.fpr.min()), float(B.fpr.max())]
s = json.load(open(os.path.join(R, "v5_summary.json")))
for m in ["lasso", "rf"]:
    h = s[f"H2_strict_{m}"]; o[f"H2_{m}_resid_share"] = h["var_resid"] / (h["var_test"] + h["var_pop"] + h["var_resid"])
u = pd.read_csv(os.path.join(R, "v5_h4_units.csv")); pt = u.groupby(["test", "model"])[["src", "burn"]].mean()
o["H4_exact_wilcoxon_p"] = float(stats.wilcoxon(pt.burn - pt.src, method="exact").pvalue); o["H4_reduction"] = float(1 - pt.burn.mean() / pt.src.mean())
o["H4_units"] = len(u); o["H4_populations"] = int(u["pop"].nunique()); o["H4_unit_share_better"] = float((u.burn < u.src).mean())
T = pd.read_csv(os.path.join(R, "tests_v5.csv")); o["auroc_range_lasso"] = [float(T[T.model == "lasso"].auroc.min()), float(T[T.model == "lasso"].auroc.max())]
o["auroc_range_all"] = [float(T.auroc.min()), float(T.auroc.max())]; o["single_cohort_tests"] = int((T[T.model == "lasso"].cohorts == 1).sum())
json.dump(o, open(os.path.join(R, "numbers_v11.json"), "w"), indent=1); print(json.dumps(o, indent=1))
