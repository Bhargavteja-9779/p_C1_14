"""Counts used in the text (populations, people, countries) -> results/counts_v4.json; PPV table print."""
import os, json, numpy as np, pandas as pd
from common_v4 import *
r = pd.read_csv(os.path.join(OUT, "atlas_rows_v4.csv.gz")); H = r[~r.study.str.startswith("TRAIN")]
ctry = META.groupby("study_name").country.agg(lambda x: x.mode().iloc[0]); nw = META.groupby("study_name").non_westernized.agg(lambda x: (x == "yes").mean() > .5)
out = {}
for strict in [True, False]:
    h = H if not strict else H[(H.strict_person == True) & ~H.study.isin(STRICT_DROP_STUDIES)]
    if strict: h = h[h.groupby(["disease", "model", "study"]).study.transform("size") >= MIN_N]
    u = h.drop_duplicates("sample_id"); st = sorted(u.study.unique())
    out["strict" if strict else "full"] = dict(people_any=int(len(u)), populations_any=len(st), countries=int(ctry[st].nunique()),
        non_westernised=int(nw[st].sum()), per_classifier={f"{d}_{m}": dict(people=int(len(g)), pops=int(g.study.nunique())) for (d, m), g in h.groupby(["disease", "model"])})
out["dedup"] = dict(excluded_samples=len(excluded()), dropped=sorted(dropped_studies()))
json.dump(out, open(os.path.join(OUT, "counts_v4.json"), "w"), indent=1); print(json.dumps(out, indent=1))
print(pd.read_csv(os.path.join(OUT, "ppv_v4.csv")).query("pi == pimax").round(4).to_string())
