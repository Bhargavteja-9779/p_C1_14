"""Derived numbers for manuscript v14 (review round 11). Writes results/numbers_v14.json."""
import os, json, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); t = pd.read_csv(os.path.join(R, "gmwi2_eastasia_taxa.csv"))
o = dict(gmwi2_gap_top5_share=float(t.contrib.head(5).sum() / t.contrib.sum()), gmwi2_gap_taxa=len(t),
         gmwi2_gap_top5=t.head(5)[["taxon", "w", "presence_ea", "presence_other", "contrib"]].round(3).values.tolist())
json.dump(o, open(os.path.join(R, "numbers_v14.json"), "w"), indent=1); print(o)
