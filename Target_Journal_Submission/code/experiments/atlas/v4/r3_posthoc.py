"""POST HOC (review round 3, statistics): (1) within-site non-random designs only (covariate + accession), excluding
cross-site sub-site transfers; (2) A5 compared fairly: per-draw in-band share for local labelled controls vs the
country reference on the SAME populations (n >= 120). Writes results/r3_posthoc.json."""
import os, json, numpy as np, pandas as pd
from scipy import stats
from common_v4 import *
rng = np.random.default_rng(31); A = 0.10; out = {}
u = pd.read_csv(os.path.join(OUT, "deploy_v4_units.csv"))
def cb(df, col):
    g = df.groupby("pop_eval")[col].agg(["sum", "size"]); s, n = g["sum"].values, g["size"].values; k = len(g)
    bs = [s[i].sum() / n[i].sum() for i in (rng.integers(0, k, k) for _ in range(2000))]
    return dict(mean=s.sum() / n.sum(), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), pops=k, units=int(n.sum()))
w = u[u.design.isin(["covariate_age", "covariate_BMI", "covariate_sex", "accession"]) & (u.N == 100)]
p = w.pivot_table(index=["design", "disease", "model", "unit", "pop_eval"], columns="method", values=["mad", "p15"]).reset_index()
p.columns = ["_".join(c).strip("_") for c in p.columns]; p["diff"] = p.mad_BURN - p.mad_SRC
pp = p.groupby("pop_eval")["diff"].mean()
out["within_site_N100"] = dict(burn_mad=p.mad_BURN.mean(), src_mad=p.mad_SRC.mean(), reduction=1 - p.mad_BURN.mean() / p.mad_SRC.mean(),
                               burn_p15=p.p15_BURN.mean(), src_p15=p.p15_SRC.mean(), diff=cb(p, "diff"), pops_better=int((pp < 0).sum()), pops=len(pp),
                               wilcoxon_pop_p=float(stats.wilcoxon(pp).pvalue))
# A5 fair comparison
r = pd.read_csv(os.path.join(OUT, "atlas_rows_v4.csv.gz")); H = r[~r.study.str.startswith("TRAIN")]
H = H[(H.strict_person == True) & ~H.study.isin(STRICT_DROP_STUDIES)]
ctry = META.groupby("study_name").country.agg(lambda x: x.mode().iloc[0]); res = []
for (d, m), g in H.groupby(["disease", "model"]):
    S = {s: x.score.values for s, x in g.groupby("study") if len(x) >= MIN_N}
    for s, x in S.items():
        if len(x) < 120: continue
        same = [o for o in S if o != s and ctry[o] == ctry[s]]
        fp = []
        for _ in range(200):
            q = rng.permutation(len(x)); t = np.sort(x[q[:100]])[int(np.ceil(101 * .9)) - 1]; fp.append(np.mean(x[q[100:]] >= t))
        fp = np.array(fp)
        c = np.mean(x >= np.quantile(np.concatenate([S[o] for o in same]), 1 - A)) if same else np.nan
        res.append(dict(disease=d, model=m, pop=s, local_perdraw_inband=np.mean((fp >= .05) & (fp <= .15)), country_fpr=c,
                        country_inband=float(.05 <= c <= .15) if same else np.nan))
R_ = pd.DataFrame(res); R_.to_csv(os.path.join(OUT, "r3_a5_fair.csv"), index=False); both = R_.dropna()
out["A5_fair"] = dict(units=len(R_), local_perdraw_inband=R_.local_perdraw_inband.mean(), units_with_country_ref=len(both), pops_with_country_ref=both["pop"].nunique(),
                      local_perdraw_inband_same_units=both.local_perdraw_inband.mean(), country_inband_same_units=both.country_inband.mean())
het = pd.read_csv(os.path.join(OUT, "heterogeneity_v4.csv")); out["Q_p_max_strict"] = float(het[het.strict].Q_p.max())
out["fold_max_abs_change_strict"] = float(het[het.strict].max_abs_fpr_change_folds.max())
json.dump(out, open(os.path.join(OUT, "r3_posthoc.json"), "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
