"""POST HOC: geographic case-mix of GMWI2 training data (SData2) - share East Asian among healthy vs non-healthy, and
presence of B. plebeius etc. by health status WITHIN vs ACROSS regions (on cMD profiles of GMWI2-training samples)."""
import json, numpy as np, pandas as pd
from scipy import stats
EA = {"China", "Japan", "South Korea", "Hong Kong", "Taiwan"}
S2 = pd.read_csv("inputs/gmwi2_SData2_training_samples.csv.gz"); hs = "Subject health status (Healthy or Non-healthy)"
S2["ea"] = S2["Geography (Country)"].isin(EA)
tab = pd.crosstab(S2[hs], S2.ea); orr = stats.fisher_exact(tab.values)
out = dict(table={str(k): {str(c): int(v) for c, v in r.items()} for k, r in tab.to_dict("index").items()},
           ea_share_healthy=float(S2[S2[hs] == "Healthy"].ea.mean()), ea_share_nonhealthy=float(S2[S2[hs] == "Non-healthy"].ea.mean()),
           fisher_or=float(orr[0]), fisher_p=float(orr[1]))
# within-region health association of a taxon vs pooled association (Simpson check) on GMWI2's own published scores is not
# possible (no profiles); use region-stratified health-status odds from SData2 phenotype x region counts only.
out["nonhealthy_by_region_and_phenotype_top"] = S2[S2[hs] == "Non-healthy"].groupby(["ea", "Phenotype"]).size().sort_values(ascending=False).head(12).reset_index().values.tolist()
json.dump(out, open("results/gmwi2_casemix.json", "w"), indent=1); print(json.dumps(out, indent=1))
