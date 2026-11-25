"""POST HOC (review round 12, editor MAJOR 2): East Asian vs other unseen populations in the STRICT set (the set the text
discusses), with the full set as a check. Writes results/posthoc_eastasia_strict_v15.json."""
import os, json, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results"); EA = {"CHN", "JPN", "KOR"}
M = pd.read_csv("/home/user/p_C1_14/data_cache/sampleMetadata.csv", low_memory=False).groupby("study_name").country.agg(lambda x: x.mode().iloc[0])
o = {}
for s in ["strict", "full"]:
    p = pd.read_csv(os.path.join(R, f"gmwi2_perpop_{s}.csv")); p = p[(~p.seen) & (p.n >= 20)].copy(); p["ea"] = p.study.map(M).isin(EA)
    a, b = p[p.ea].fpr, p[~p.ea].fpr
    o[s] = dict(unseen=len(p), ea=int(p.ea.sum()), other=int((~p.ea).sum()), ea_median=float(a.median()), other_median=float(b.median()),
                mw_p_greater=float(stats.mannwhitneyu(a, b, alternative="greater").pvalue), ea_list=p[p.ea][["study", "n", "fpr"]].values.tolist())
json.dump(o, open(os.path.join(R, "posthoc_eastasia_strict_v15.json"), "w"), indent=1); print(json.dumps({k: {a: b for a, b in v.items() if a != "ea_list"} for k, v in o.items()}, indent=1))
