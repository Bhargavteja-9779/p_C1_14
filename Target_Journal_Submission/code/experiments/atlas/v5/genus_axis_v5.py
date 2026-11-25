"""EXPLORATORY: share of each LASSO test's positive score shift (in its most over-flagged strict population) carried by
the industrialisation axis: depleted Bacteroides/Parabacteroides/Phocaeicola (contribution > 0 with lower abundance)
and enriched Prevotella/Segatella (contribution > 0 with higher abundance). Genus lists fixed before running.
Also: which population is most over-flagged per test. Writes results/genus_axis_v5.csv, genus_axis_v5.json."""
import os, re, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from common_v5 import *
import atlas_v5 as A5
BACT = {"Bacteroides", "Parabacteroides", "Phocaeicola"}; PREV = {"Prevotella", "Segatella"}
genus = lambda t: re.sub(r"^[a-z]__\[?", "", t).split("_")[0].strip("[]")
co = pd.read_csv(os.path.join(OUT5, "coefs_v5.csv")); per = pd.read_csv(os.path.join(OUT5, "v5_perpop_strict.csv")); rows = []
for t in A5.TESTS:
    c = co[co.test == t].reset_index(drop=True); case, studies = A5.TESTS[t]; X, y, g, M = A5.load_cc(case, studies)
    Z = lambda Xm: (np.log10(Xm.reindex(columns=c.taxon, fill_value=0).fillna(0).values / 100 + 1e-5) - c.mu.values) / c.sd.values
    z0 = Z(X[y == 0]).mean(0); pp = per[(per.test == t) & (per.model == "lasso")].sort_values("fpr", ascending=False); s = pp.study.iloc[0]
    Xc, md = controls(s); dz = Z(Xc[md.strict_person.values]).mean(0) - z0; ctb = c.w.values * dz; gen = c.taxon.map(genus).values
    pos = ctb[ctb > 0].sum(); bact = ctb[(ctb > 0) & np.isin(gen, list(BACT)) & (dz < 0)].sum(); prev = ctb[(ctb > 0) & np.isin(gen, list(PREV)) & (dz > 0)].sum()
    rows.append(dict(test=t, top_population=s, fpr=pp.fpr.iloc[0], positive_shift=pos, bacteroides_depleted_share=bact / pos, prevotella_enriched_share=prev / pos, axis_share=(bact + prev) / pos))
o = pd.DataFrame(rows); o.to_csv(os.path.join(OUT5, "genus_axis_v5.csv"), index=False)
s = dict(tests=len(o), median_axis_share=float(o.axis_share.median()), tests_axis_ge_020=int((o.axis_share >= .2).sum()),
         top_population_counts=o.top_population.value_counts().to_dict())
json.dump(s, open(os.path.join(OUT5, "genus_axis_v5.json"), "w"), indent=1); print(json.dumps(s, indent=1)); print(o.round(2).to_string())
