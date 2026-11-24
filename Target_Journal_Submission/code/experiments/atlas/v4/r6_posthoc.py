"""POST HOC (review round 6): (1) Holm over EVERY population-level P value computed in v4 (not only those reported);
(2) population-level test for local-vs-country reference (A5 fair). Writes results/holm_v6.csv, r6_posthoc.json."""
import os, json, numpy as np, pandas as pd
from scipy import stats
from common_v4 import OUT
S = json.load(open(os.path.join(OUT, "summary_v4.json"))); H2 = json.load(open(os.path.join(OUT, "h2h_v4.json")))
P3 = json.load(open(os.path.join(OUT, "r3_posthoc.json"))); hy = pd.read_csv(os.path.join(OUT, "hypotheses_v4.csv"))
rows = [(k, v["wilcoxon_pop_p"]) for k, v in S.items() if isinstance(v, dict) and v.get("wilcoxon_pop_p") is not None]
rows += [(f"h2h:{k}", v["wilcoxon_pop_p"]) for k, v in H2.items() if v.get("wilcoxon_pop_p") is not None]
rows += [("within-site N100 (post hoc)", P3["within_site_N100"]["wilcoxon_pop_p"])]
rows += [(f"{'strict' if r.strict else 'full'}:{r.model}:{r.test}", r.p) for r in hy.itertuples() if not pd.isna(r.p) and not r.test.startswith("A1")]
a5 = pd.read_csv(os.path.join(OUT, "r3_a5_fair.csv")).dropna(); pp = a5.assign(d=a5.local_perdraw_inband - a5.country_inband).groupby("pop").d.mean()
w = stats.wilcoxon(pp); rows.append(("A5 local vs country reference (post hoc, by population)", float(w.pvalue)))
d = pd.DataFrame(rows, columns=["test", "p"]).sort_values("p").reset_index(drop=True); m = len(d)
d["holm"] = (d.p * (m - d.index)).cummax().clip(upper=1); d.to_csv(os.path.join(OUT, "holm_v6.csv"), index=False)
out = dict(family_size=m, surviving=d[d.holm < .05].test.tolist(), A5_pop=dict(populations=len(pp), mean_diff=float(pp.mean()), pops_local_better=int((pp > 0).sum()), wilcoxon_p=float(w.pvalue)))
json.dump(out, open(os.path.join(OUT, "r6_posthoc.json"), "w"), indent=1); print(json.dumps(out, indent=1)); print(d.round(4).to_string())
