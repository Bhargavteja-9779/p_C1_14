"""POST HOC (requested in review r16, recommended items): (1) study-clustered bootstrap 95% CI for the corrected Q2
Pearson r (GMHI on developers' MetaPhlAn2 vs cMD MetaPhlAn3 profiles, same samples); (2) sensitivity of the East Asian
contrast to counting Mongolia as East Asian, for GMWI2 (developers' training scores) and GMHI (developers' own data).
Uses only committed files; no cMD cache needed. Seed fixed at 100 (first SEEDS_CONFIRM value)."""
import os, json, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "results")
src = open(os.path.join(HERE, "posthoc_gmhi_matching.py")).read()
ns = {"__file__": os.path.join(HERE, "posthoc_gmhi_matching.py")}
exec(compile(src.split("res = dict(")[0], "matching_head", "exec"), ns); q = ns["q"]
res = {"Q2_point_r": float(np.corrcoef(q.gmhi, q.dev_g)[0, 1]), "Q2_n": int(len(q)), "Q2_studies": int(q.study.nunique())}
rng = np.random.default_rng(100); studies = q.study.unique(); groups = {s: q[q.study == s] for s in studies}; B = 2000; rs = []
for _ in range(B):
    d = pd.concat([groups[s] for s in rng.choice(studies, len(studies), replace=True)])
    rs.append(np.corrcoef(d.gmhi, d.dev_g)[0, 1])
res["Q2_cluster_boot"] = dict(B=B, seed=100, ci95=[float(np.percentile(rs, 2.5)), float(np.percentile(rs, 97.5))],
                              share_at_or_above_0p80=float(np.mean(np.array(rs) >= 0.80)))
# Mongolia sensitivity
EA = {"China", "Japan", "South Korea", "Hong Kong", "Taiwan"}
g = pd.read_csv(os.path.join(HERE, "..", "v6", "results", "gmwi2_published_training_perstudy.csv"))
h = pd.read_csv(os.path.join(OUT, "gmhi_dev_perstudy.csv"))
def contrast(fpr, ea, alt):
    return dict(n_ea=int(ea.sum()), n_other=int((~ea).sum()), median_ea=float(fpr[ea].median()), median_other=float(fpr[~ea].median()),
                p=float(stats.mannwhitneyu(fpr[ea], fpr[~ea], alternative=alt).pvalue))
for name, df, ea0, mong, alt in [("GMWI2_training", g, g.country.isin(EA), g.country.eq("Mongolia"), "two-sided"),
                                 ("GMHI_developers", h, h.ea.astype(bool), h.region.str.contains("Mongol"), "greater")]:
    res[name] = dict(as_reported=contrast(df.fpr, ea0, alt), mongolia_as_east_asian=contrast(df.fpr, ea0 | mong, alt),
                     mongolia_studies=int(mong.sum()), mongolia_fpr=[float(x) for x in df.fpr[mong]], test=alt)
json.dump(res, open(os.path.join(OUT, "posthoc_r16_sensitivity.json"), "w"), indent=1); print(json.dumps(res, indent=1))
