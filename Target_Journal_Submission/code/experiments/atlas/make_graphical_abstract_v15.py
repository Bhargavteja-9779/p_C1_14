"""Graphical abstract (v15): study design + three findings, from result files (no new numbers)."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, "..", "..", "..", "manuscript", "graphical_abstract")
TXT, MUT, BLUE, ORA, TRN, GRID, BG = "#0b0b0b", "#52514e", "#2a78d6", "#eb6834", "#c98500", "#c3c2b7", "#f6f5f2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
per = pd.read_csv(os.path.join(H, "v5", "results", "v5_perpop_strict.csv")); L = per[(per.model == "lasso") & (per.n >= 100)]
gm = pd.read_csv(os.path.join(H, "v6", "results", "gmwi2_published_training_perstudy.csv"))
u = pd.read_csv(os.path.join(H, "v5", "results", "v5_h4_units.csv"))
fig = plt.figure(figsize=(9, 3.4)); fig.patch.set_facecolor("white")
def box(x, title, sub):
    ax = fig.add_axes([x, .08, .30, .78]); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    fig.text(x + .005, .92, title, fontsize=9.5, fontweight="bold", color=TXT); fig.text(x + .005, .875, sub, fontsize=7, color=MUT); return ax
# 1 atlas: FPR strip per test
a = box(.02, "1  Same cut-off, different populations", "14 LASSO tests; dots = healthy populations with ≥ 100 people")
tests = L.groupby("test").fpr.median().sort_values().index
for i, t in enumerate(tests):
    x = L[L.test == t].fpr.values; a.scatter(x, np.full(len(x), i) + np.random.default_rng(i).uniform(-.18, .18, len(x)), s=7, color=BLUE, alpha=.6, lw=0)
a.axvline(.10, color=TXT, ls="--", lw=.8); a.text(.105, -.9, "target 0.10", fontsize=6.5, color=TXT)
a.set_yticks(range(len(tests))); a.set_yticklabels([t.replace("_", " ") for t in tests], fontsize=6); a.set_xlim(-.02, .85); a.set_xlabel("false-positive rate in a healthy population", fontsize=7)
a.tick_params(labelsize=6, length=0)
# 2 GMWI2
b = box(.355, "2  A released index, its own data", "GMWI2: healthy people labelled non-healthy")
EA = {"CHN", "JPN", "KOR", "China", "Japan", "South Korea"}; ea = gm.country.isin(EA)
for j, (m, c, lab) in enumerate([(~ea, BLUE, "other studies"), (ea, ORA, "East Asian studies")]):
    x = gm.fpr[m].values; b.scatter(np.full(len(x), j) + np.random.default_rng(j).uniform(-.15, .15, len(x)), x, s=14, color=c, alpha=.8, lw=0)
    b.hlines(np.median(x), j - .3, j + .3, color=TXT, lw=1.5); b.text(j, np.median(x) + .04, f"median {np.median(x):.2f}", ha="center", fontsize=7, color=TXT)
b.set_xticks([0, 1]); b.set_xticklabels(["31 other\nstudies", "13 East Asian\nstudies"], fontsize=7); b.set_ylim(-.03, 1); b.set_ylabel("share labelled non-healthy", fontsize=7)
b.text(.5, .93, "cause: geographic make-up\nof the training data", ha="center", fontsize=7, color=MUT, transform=b.transAxes, va="top"); b.tick_params(labelsize=6, length=0)
# 3 site fix
c = box(.69, "3  Recalibrate at the site", "cut-off from the first 100 local people (no labels)")
pt = u.groupby(["test", "model"])[["src", "burn"]].mean()
for k, (col, c_, lab) in enumerate([("src", TRN, "training\ncut-off"), ("burn", BLUE, "local\nburn-in")]):
    x = pt[col].values; c.scatter(np.full(len(x), k) + np.random.default_rng(k + 5).uniform(-.15, .15, len(x)), x, s=12, color=c_, alpha=.8, lw=0)
    c.hlines(x.mean(), k - .3, k + .3, color=TXT, lw=1.5)
c.set_xticks([0, 1]); c.set_xticklabels(["training\ncut-off", "local\nburn-in"], fontsize=7); c.set_ylabel("mean |FPR − 0.10| within site", fontsize=7)
c.text(.5, .93, f"error −62% (28/28 classifiers)\nretrospective; costs sensitivity", ha="center", va="top", fontsize=7, color=MUT, transform=c.transAxes); c.set_ylim(0, .38); c.tick_params(labelsize=6, length=0)
for e in ("png", "pdf"): fig.savefig(os.path.join(O, f"graphical_abstract_v15.{e}"), dpi=300, bbox_inches="tight", facecolor="white")
print(pt.mean().round(3).to_dict(), gm.groupby(gm.country.isin(EA)).fpr.median().round(2).to_dict())
