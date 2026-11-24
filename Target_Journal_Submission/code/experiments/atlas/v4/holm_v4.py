"""Holm correction over every P value reported in manuscript v4 main text (one family). Writes results/holm_v4.csv."""
import os, json, pandas as pd
from common_v4 import OUT
S = json.load(open(os.path.join(OUT, "summary_v4.json"))); H2 = json.load(open(os.path.join(OUT, "h2h_v4.json")))
h = pd.read_csv(os.path.join(OUT, "hypotheses_v4.csv")).set_index(["strict", "model", "test"]).p
fam = {
 "BURN-SRC locked N100 (pop Wilcoxon)": S["random/locked_full/N100/BURN_minus_SRC_mad"]["wilcoxon_pop_p"],
 "BURN-SRC strict N100": S["random/all_strict/N100/BURN_minus_SRC_mad"]["wilcoxon_pop_p"],
 "BURN-ALIGN locked N100": S["random/locked_full/N100/BURN_minus_ALIGN_mad"]["wilcoxon_pop_p"],
 "BURN-SRC neighbour N100": S["stress/neighbour/N100/BURN_minus_SRC_mad"]["wilcoxon_pop_p"],
 "BURN-SRC NX1 pooled N100": S["stress/NX1_pooled/N100/BURN_minus_SRC_mad"]["wilcoxon_pop_p"],
 "augmentation vs none": H2["aug_vs_noaug_all_locked"]["wilcoxon_pop_p"],
 "BURN vs augmentation N100": H2["burn_vs_aug_N100"]["wilcoxon_pop_p"],
 "A3 CRC LASSO strict": h[(True, "lasso", "A3_CRC_nonwest_minus_west")], "A3 CRC RF strict": h[(True, "rf", "A3_CRC_nonwest_minus_west")],
 "A3 CRC LASSO full": h[(False, "lasso", "A3_CRC_nonwest_minus_west")], "T2D LASSO non-west strict (post hoc)": h[(True, "lasso", "A3_T2D_nonwest_minus_west_posthoc")],
}
d = pd.DataFrame(dict(test=list(fam), p=list(fam.values()))).sort_values("p").reset_index(drop=True); m = len(d)
d["holm"] = (d.p * (m - d.index)).cummax().clip(upper=1); d.to_csv(os.path.join(OUT, "holm_v4.csv"), index=False); print(d.round(4).to_string())
