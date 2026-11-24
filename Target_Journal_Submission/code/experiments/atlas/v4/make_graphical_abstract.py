"""Graphical abstract (manuscript/figures_v5/graphical_abstract.png) from result files."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from common_v4 import *
FIG = os.path.join(HERE, "..", "..", "..", "..", "manuscript", "figures_v5")
per = pd.read_csv(os.path.join(OUT, "atlas_perpop_v4.csv")); S = json.load(open(os.path.join(OUT, "summary_v4.json"))); P = json.load(open(os.path.join(OUT, "r3_posthoc.json")))
fig, ax = plt.subplots(1, 3, figsize=(9, 3), gridspec_kw=dict(width_ratios=[1.3, 1, 1]))
for i, d in enumerate(["CRC", "IBD", "T2D"]):
    c = per[(per.disease == d) & (per.model == "lasso") & per.strict]
    ax[0].scatter(np.random.default_rng(i).uniform(-.15, .15, len(c)) + i, c.fpr, s=10, c=["#1b9e77", "#d95f02", "#7570b3"][i])
ax[0].axhspan(.05, .15, color="#cfe3f3", zorder=0); ax[0].axhline(.1, ls="--", c="k", lw=.8)
ax[0].set_xticks([0, 1, 2]); ax[0].set_xticklabels(["CRC test", "IBD test", "T2D test"]); ax[0].set_ylabel("share of healthy people flagged")
ax[0].set_title("1. One cut-off (target 10%),\n32–35 healthy populations each", fontsize=9)
v = [S["random/all_full/N100/SRC"]["mad"]["mean"], S["random/all_full/N100/ATLAS"]["mad"]["mean"], S["stress/neighbour/N100/BURN"]["mad"]["mean"]]
ax[1].bar(["training\ncut-off", "pooled\nreference", "other cohort,\nsame country"], v, color=["#8c8c8c", "#e6a700", "#9e9ac8"])
ax[1].set_ylabel("mean |FPR − 0.10|"); ax[1].set_title("2. Borrowed cut-offs\ndo not fix it", fontsize=9); ax[1].set_ylim(0, .11)
w = P["within_site_N100"]; ax[2].bar(["training\ncut-off", "burn-in, 100 people\nsame site"], [w["src_mad"], w["burn_mad"]], color=["#8c8c8c", "#2166ac"])
ax[2].set_ylim(0, .11); ax[2].set_title("3. Calibrating on 100 unlabelled\npeople at the site does", fontsize=9)
for a in ax: a.spines[["top", "right"]].set_visible(False); a.tick_params(labelsize=7)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "graphical_abstract.png"), dpi=300); fig.savefig(os.path.join(FIG, "graphical_abstract.pdf"))
