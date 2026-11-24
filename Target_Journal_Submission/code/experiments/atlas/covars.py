"""Per-sample covariates for atlas samples (metadata + diversity from profiles)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, "../.."); from src.data import CACHE
r = pd.read_csv("results/atlas_rows.csv.gz"); ids = set(r.sample_id)
M = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
out = []
for f in sorted(os.listdir(os.path.join(CACHE, "ra"))):
    a = pd.read_csv(os.path.join(CACHE, "ra", f), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
    a = a.groupby(level=0).sum().T; a = a.loc[a.index.intersection(list(ids))]
    if not len(a): continue
    P = a.values / np.maximum(a.values.sum(1, keepdims=True), 1e-12)
    sh = -(np.where(P > 0, P * np.log(P), 0)).sum(1)
    out.append(pd.DataFrame(dict(shannon=sh, richness=(P > 0).sum(1)), index=a.index))
D = pd.concat(out); D = D[~D.index.duplicated()]
cols = ["study_name", "age", "gender", "BMI", "number_reads", "country", "non_westernized", "age_category"]
D = D.join(M[cols]); D.index.name = "sample_id"; D.to_csv("results/atlas_covars.csv.gz")
print(D.describe(include="all").T[["count"]])
