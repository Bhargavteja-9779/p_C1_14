"""Graphical abstract v6 (manuscript/figures_v5/graphical_abstract.png). Panel 2 uses ONE set of population-test pairs
(strict, n >= 120, with a same-country reference): share with FPR in 0.05-0.15. Writes results/ga_inband.json."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from common_v4 import *
FIG = os.path.join(HERE, "..", "..", "..", "..", "manuscript", "figures_v7")
per = pd.read_csv(os.path.join(OUT, "atlas_perpop_v4.csv")); a5 = pd.read_csv(os.path.join(OUT, "r3_a5_fair.csv")).dropna()
src = a5.merge(per[per.strict][["disease", "model", "study", "fpr"]], left_on=["disease", "model", "pop"], right_on=["disease", "model", "study"])
v = dict(units=len(src), populations=int(src["pop"].nunique()), training_cutoff=float(src.fpr.between(.05, .15).mean()),
         country_reference=float(src.country_inband.mean()), local_100=float(src.local_perdraw_inband.mean()))
json.dump(v, open(os.path.join(OUT, "ga_inband.json"), "w"), indent=1); print(v)
fig, ax = plt.subplots(1, 2, figsize=(8, 3.1), gridspec_kw=dict(width_ratios=[1.3, 1]))
for i, d in enumerate(["CRC", "IBD", "T2D"]):
    c = per[(per.disease == d) & (per.model == "lasso") & per.strict]
    ax[0].scatter(np.random.default_rng(i).uniform(-.15, .15, len(c)) + i, c.fpr, s=10, c=["#1b9e77", "#d95f02", "#7570b3"][i])
ax[0].axhspan(.05, .15, color="#cfe3f3", zorder=0); ax[0].axhline(.1, ls="--", c="k", lw=.8)
ax[0].set_xticks([0, 1, 2]); ax[0].set_xticklabels(["CRC test", "IBD test", "T2D test"]); ax[0].set_ylabel("share of healthy people flagged")
ax[0].set_title("1. One LASSO cut-off (target 10%)\nin 32–35 healthy populations per test", fontsize=9)
P = json.load(open(os.path.join(OUT, "r3_posthoc.json")))["within_site_N100"]; S = json.load(open(os.path.join(OUT, "summary_v4.json")))
nb = [S["stress/neighbour/N100/SRC"]["mad"]["mean"], S["stress/neighbour/N100/BURN"]["mad"]["mean"]]
x = np.arange(2); ax[1].bar(x - .18, [P["src_mad"], nb[0]], .34, color="#8c8c8c", label="training cut-off")
ax[1].bar(x + .18, [P["burn_mad"], nb[1]], .34, color="#2166ac", label="burn-in, 100 unlabelled people")
ax[1].set_xticks(x); ax[1].set_xticklabels([f"same site\n({P['pops']} populations)", f"other cohort,\nsame country ({S['stress/neighbour/N100/BURN']['mad']['populations']} populations)"])
ax[1].set_ylabel("mean |FPR − 0.10|"); ax[1].set_ylim(0, .12); ax[1].legend(fontsize=7, frameon=False, loc="upper left")
ax[1].set_title("2. Calibrate on the site's own people\n(average error; sensitivity falls)", fontsize=9)
for a in ax: a.spines[["top", "right"]].set_visible(False); a.tick_params(labelsize=7)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "graphical_abstract.png"), dpi=300); fig.savefig(os.path.join(FIG, "graphical_abstract.pdf"))
