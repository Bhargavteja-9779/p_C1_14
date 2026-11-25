"""Figures for manuscript v11 (iMeta Letter format: 2 multi-panel figures). Reads v5 result files only."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import FancyBboxPatch
from scipy import stats
from common_v5 import *
EUNA = {"GBR", "USA", "NLD", "DNK", "DEU", "SWE", "FRA", "ITA", "ESP", "AUT", "IRL", "FIN", "CAN", "ISR", "LUX", "NOR", "EST", "SVK", "KAZ"}
ctry = META.groupby("study_name").country.agg(lambda x: x.mode().iloc[0])
FIG = os.path.join(HERE5, "..", "..", "..", "..", "manuscript", "figures_v11"); os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 7, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
R = lambda f: os.path.join(OUT5, f)
het = pd.read_csv(R("v5_het_strict.csv")); per = pd.read_csv(R("v5_perpop_strict.csv")); T = pd.read_csv(R("tests_v5.csv"))
idx = pd.read_csv(R("v5_popindex_strict_lasso.csv")).set_index("study")["index"]
NAME = {"CRC": "Colorectal cancer", "adenoma": "Adenoma", "IBD": "IBD", "T2D": "Type 2 diabetes", "IGT": "Impaired glucose tol.", "CAD": "Coronary artery disease",
        "HF": "Heart failure", "ACVD": "Atherosclerotic CVD", "cirrhosis": "Liver cirrhosis", "hypertension": "Hypertension", "schizophrenia": "Schizophrenia",
        "ME/CFS": "ME/CFS", "migraine": "Migraine", "fatty_liver": "Fatty liver"}
def popname(s): return f"{ctry[s]} ({s.split('_')[0]})"
# ---------------- Figure 1 ----------------
fig = plt.figure(figsize=(7.2, 8.4)); gs = fig.add_gridspec(4, 2, height_ratios=[0.32, 1.55, 0.42, 1.0], width_ratios=[1.35, 1], hspace=0.25, wspace=0.35)
ax = fig.add_subplot(gs[0, :]); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 1.2)
NPAIR = len(per); NTR = json.load(open(R("training_cohorts_v5.json")))["training_cohorts"]
boxes = [(0.1, f"{NTR} case–control cohorts\n14 diseases, 28 classifiers\n(LASSO, random forest)"), (2.6, "Cut-off at the 90th percentile\nof training-control scores\n(promised FPR = 10%)"),
         (5.1, "6,525 healthy adults\n36 cohorts · 20 countries\nnever seen in training"), (7.6, f"Share flagged = realised FPR\nper test × population\n({NPAIR} classifier–population pairs)")]
for x, t in boxes:
    ax.add_patch(FancyBboxPatch((x, 0.15), 2.2, 0.9, boxstyle="round,pad=0.03", fc="#eef3f8", ec="#2166ac", lw=0.8)); ax.text(x + 1.1, 0.6, t, ha="center", va="center", fontsize=6)
for x in [2.35, 4.85, 7.35]: ax.annotate("", (x + 0.22, 0.6), (x, 0.6), arrowprops=dict(arrowstyle="->", lw=1))
ax.set_title("A  Study design", loc="left", fontsize=8, fontweight="bold")
# B heatmap (LASSO)
ax = fig.add_subplot(gs[1, :]); L = per[per.model == "lasso"].pivot(index="test", columns="study", values="fpr")
cols = idx.sort_values().index.intersection(L.columns); rows = het[het.model == "lasso"].sort_values("I2").test; M = L.loc[rows, cols]
im = ax.imshow(M.values, aspect="auto", cmap="RdBu_r", norm=TwoSlopeNorm(vcenter=0.10, vmin=0, vmax=0.6), interpolation="nearest")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([NAME[t] for t in rows]); ax.set_xticks(range(len(cols)))
ax.set_xticklabels([popname(s) for s in cols], rotation=90, fontsize=5)
for i, s in enumerate(cols):
    if ctry[s] not in EUNA: ax.get_xticklabels()[i].set_color("#b35806")
cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label("FPR (promised 0.10)"); cb.set_ticks([0, .05, .1, .2, .4, .6])
ax.set_title("B  False-positive rate of each LASSO test in each healthy population (grey = cohort used in training)", loc="left", fontsize=8, fontweight="bold")
ax.set_facecolor("#d9d9d9")
# C prediction intervals
ax = fig.add_subplot(gs[3, 0]); h = het.sort_values(["model", "pi_hi"]); y = 0; yt, yl = [], []
for t in het[het.model == "lasso"].sort_values("pi_hi").test:
    for m, c, dy in [("lasso", "#2166ac", 0.18), ("rf", "#b2182b", -0.18)]:
        r_ = het[(het.test == t) & (het.model == m)].iloc[0]; ax.plot([r_.pi_lo, r_.pi_hi], [y + dy] * 2, c=c, lw=1.6); ax.plot(r_.pooled, y + dy, "o", c=c, ms=2.5)
    yt.append(y); yl.append(NAME[t]); y += 1
ax.axvspan(.05, .15, color="#cfe3f3", zorder=0); ax.axvline(.1, ls="--", c="k", lw=.6); ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6)
ax.set_xlabel("FPR in a new healthy population (pooled, 95% prediction interval)"); ax.plot([], [], c="#2166ac", label="LASSO"); ax.plot([], [], c="#b2182b", label="random forest")
ax.legend(frameon=False, fontsize=6, loc="lower right"); ax.set_title(f"C  I² {100*het.I2.min():.0f}–{100*het.I2.max():.0f}% in all 28 classifiers", loc="left", fontsize=8, fontweight="bold")
# D AUROC vs tau
ax = fig.add_subplot(gs[3, 1]); s = json.load(open(R("v5_summary.json")))["expl_auroc_vs_tau"]
for m, c in [("lasso", "#2166ac"), ("rf", "#b2182b")]:
    d = het[het.model == m]; ax.scatter(d.auroc, d.tau, s=12, c=c, label=m.upper() if m == "lasso" else "RF")
ax.set_xlabel("AUROC in training cohorts (out-of-fold)"); ax.set_ylabel("between-population spread of FPR (τ, logit)")
ax.set_title(f"D  Better tests are not more portable\n(Spearman ρ = {s['spearman']:.2f}, P = {s['p']:.2f})", loc="left", fontsize=8, fontweight="bold"); ax.legend(frameon=False, fontsize=6)
fig.savefig(os.path.join(FIG, "Figure1_atlas.pdf")); fig.savefig(os.path.join(FIG, "Figure1_atlas.png"), dpi=300, bbox_inches="tight")
# ---------------- Figure 2 ----------------
fig, axs = plt.subplots(2, 2, figsize=(7.2, 7.0)); plt.subplots_adjust(hspace=0.85, wspace=0.4)
ax = axs[0, 0]; d = idx.sort_values(); colr = ["#b35806" if ctry[s] not in EUNA else "#4d4d4d" for s in d.index]
ax.barh(range(len(d)), d.values, color=colr); ax.set_yticks(range(len(d))); ax.set_yticklabels([popname(s) for s in d.index], fontsize=4.5); ax.axvline(0, c="k", lw=.6)
e = json.load(open(R("explore_v5.json")))["index_lasso"]
ax.set_xlabel("false-alarm index (mean logit-FPR deviation over 14 tests)"); ax.set_title(f"A  Populations outside Europe/N. America are over-\nflagged across tests (P = {e['p_euna']:.3f}; exploratory)", loc="left", fontsize=7.5, fontweight="bold")
ax = axs[0, 1]; U = pd.read_csv(R("explore_v5_units.csv")); Ur = pd.read_csv(R("replicate_v5_units.csv"))
rd = json.load(open(R("explore_v5.json")))["dist_lasso"]["per_test"]; rr = json.load(open(R("replicate_v5.json")))["H5_lasso"]["per_test"]
t_ = sorted(rd, key=lambda k: rd[k]["rho_fpr"]); x = np.arange(len(t_))
ax.scatter(x - .12, [rd[k]["rho_fpr"] for k in t_], s=14, c="#2166ac", label="discovery (36 healthy populations)")
ax.scatter(x + .12, [rr.get(k, np.nan) for k in t_], s=14, c="#e08214", marker="D", label="replication (19 other populations)")
ax.axhline(0, c="k", lw=.6); ax.set_xticks(x); ax.set_xticklabels([NAME[k] for k in t_], rotation=70, ha="right", fontsize=5.5); ax.set_ylabel("Spearman ρ: distance from training\ncontrols vs FPR (LASSO)")
rj = json.load(open(R("replicate_v5.json")))["H5_lasso"]
ax.set_title(f"B  Populations far from the training controls are flagged\nmore (12/14 tests; replication {rj['positive']}/14)", loc="left", fontsize=7.5, fontweight="bold"); ax.legend(frameon=False, fontsize=5.5, loc="lower right")
ax = axs[1, 0]; rec = pd.read_csv(R("v5_recurrent_taxa.csv")).set_index("taxon")["test"]; cnt = rec.value_counts().sort_index()
ax.bar(cnt.index, cnt.values, color="#7570b3"); ax.set_xlabel("tests in which the taxon is a top-10 driver\n(most over-flagged population of each test)"); ax.set_ylabel("taxa")
ax.set_xticks(cnt.index); ax.set_title(f"C  The taxa that drive false alarms differ\nbetween tests (none in ≥ 4 of 14)", loc="left", fontsize=7.5, fontweight="bold")
ax = axs[1, 1]; u = pd.read_csv(R("v5_h4_units.csv")); pt = u.groupby(["test", "model"]).agg(src=("src", "mean"), burn=("burn", "mean")).reset_index()
for _, r_ in pt.iterrows(): ax.plot([0, 1], [r_.src, r_.burn], c="#2166ac" if r_.model == "lasso" else "#b2182b", alpha=.5, lw=.8, marker="o", ms=2)
ax.set_xticks([0, 1]); ax.set_xticklabels(["training cut-off", "burn-in on 100 local\nunlabelled people"]); ax.set_ylabel("mean |FPR − 0.10| (within-site\nnon-random splits)"); ax.set_xlim(-.3, 1.3)
h4 = json.load(open(R("v5_summary.json")))["H4"]
ax.set_title(f"D  Local recalibration lowers the error in\n{h4['tests_burn_better']}/{h4['tests']} classifiers (P = {h4['wilcoxon_tests_p']:.0e})", loc="left", fontsize=7.5, fontweight="bold")
fig.savefig(os.path.join(FIG, "Figure2_why_and_fix.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(FIG, "Figure2_why_and_fix.png"), dpi=300, bbox_inches="tight")
print("ok", sorted(os.listdir(FIG)))
