"""Counts quoted in manuscript v12 that were computed but not saved -> results/counts_v12.json (post hoc bookkeeping)."""
import json, pandas as pd
EA = {"China", "Japan", "South Korea", "Hong Kong", "Taiwan"}
S2 = pd.read_csv("inputs/gmwi2_SData2_training_samples.csv.gz"); hs = "Subject health status (Healthy or Non-healthy)"
S2["ea"] = S2["Geography (Country)"].isin(EA); H = S2[S2[hs] == "Healthy"]; N = S2[S2[hs] == "Non-healthy"]
L = pd.read_csv("results/v6b_loso_scores.csv.gz")
out = dict(gmwi2_training_samples=len(S2), gmwi2_training_studies=int(S2.iloc[:, 0].nunique()) if "Study" not in S2 else int(S2.Study.nunique()),
           gmwi2_healthy=len(H), gmwi2_nonhealthy=len(N), gmwi2_healthy_ea=int(H.ea.sum()), gmwi2_nonhealthy_ea=int(N.ea.sum()),
           v6b_people=len(L), v6b_columns=list(L.columns))
for c in ["study_name", "study"]:
    if c in L: out["v6b_studies"] = int(L[c].nunique())
json.dump(out, open("results/counts_v12.json", "w"), indent=1); print(out); print(S2.columns.tolist()[:8])
