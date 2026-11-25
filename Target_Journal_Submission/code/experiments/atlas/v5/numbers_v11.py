"""Headline numbers for manuscript v11 -> results/numbers_v11.json (all derived from v5 result files)."""
import os, json, numpy as np, pandas as pd
from common_v5 import OUT5
R = lambda f: os.path.join(OUT5, f)
per = pd.read_csv(R("v5_perpop_strict.csv")); het = pd.read_csv(R("v5_het_strict.csv")); T = pd.read_csv(R("tests_v5.csv"))
o = {}
o["pairs"] = len(per); o["pairs_lasso"] = int((per.model == "lasso").sum())
o["share_out_of_band"] = float(((per.fpr < .05) | (per.fpr > .15)).mean()); o["share_above_020"] = float((per.fpr > .20).mean()); o["share_below_005"] = float((per.fpr < .05).mean())
o["share_above_030"] = float((per.fpr > .30).mean())
big = per[per.n >= 100]; o["pairs_n100"] = len(big); o["share_out_of_band_n100"] = float(((big.fpr < .05) | (big.fpr > .15)).mean())
o["I2_min"], o["I2_max"], o["I2_median"] = float(het.I2.min()), float(het.I2.max()), float(het.I2.median())
o["pi_hi_max"], o["pi_hi_min"] = float(het.pi_hi.max()), float(het.pi_hi.min())
o["pi_width_median"] = float((het.pi_hi - het.pi_lo).median())
o["auroc_min"], o["auroc_max"] = float(T.auroc.min()), float(T.auroc.max()); o["tests_auroc_ge_070"] = int((T.auroc >= .70).sum())
o["cases_total"] = int(T.drop_duplicates("test").n_cases.sum())
for t in ["CRC", "IBD", "cirrhosis", "ACVD"]:
    for m in ["lasso"]:
        h = het[(het.test == t) & (het.model == m)].iloc[0]; o[f"{t}_{m}"] = dict(pooled=float(h.pooled), pi_lo=float(h.pi_lo), pi_hi=float(h.pi_hi), auroc=float(h.auroc))
json.dump(o, open(R("numbers_v11.json"), "w"), indent=1); print(json.dumps(o, indent=1))
