"""Main figures (vector PDF + PNG) from the locked run (results/cohort_level_summary.csv, final_*.csv.gz) and the
post-hoc experiments (experiments/posthoc/E*_*.csv). Palette: validated default
categorical order (blue, orange, aqua, yellow, magenta, green); text in neutral inks; one y-axis per panel."""
import os, sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src import calibrate as C
H = os.path.dirname(__file__); R = os.path.join(H, "..", "..", "results"); FIG = os.path.join(H, "..", "..", "figures"); os.makedirs(FIG, exist_ok=True)
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
S = dict(source="#2a78d6", em="#eb6834", featstd="#1baf7a", shift2="#eda100", ctrl10="#e87ba4", rpoolmean="#008300", local_q="#7b61c9", rpool="#52514e", gauss2="#b04e17", mlls="#9c6b00")
LAB = dict(source="Training threshold", em="Label-shift EM", featstd="Per-site standardisation",
           shift2="Unlabelled mixture fit", ctrl10="10 labelled local controls", rpoolmean="Local rank rule, expected FPR", local_q="Local pool quantile", rpool="Local rank rule, P(FPR > target) ≤ 0.1", gauss2="Two-Gaussian calibration", mlls="MLLS-BCTS")
SHORT = dict(source="Training", em="Label-shift EM", featstd="Per-site std.", shift2="Mixture fit", ctrl10="10 local controls", rpoolmean="Rank rule", local_q="Pool quantile", rpool="Strict rank rule", gauss2="Two-Gaussian", mlls="MLLS")
MK = dict(source="o", em="s", featstd="^", shift2="D", ctrl10="v", rpoolmean="P", local_q="X", rpool="*", gauss2="<", mlls=">")
plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "font.family": "DejaVu Sans", "figure.facecolor": "white"})
cm = pd.read_csv(os.path.join(R, "cohort_level_summary.csv"))
def save(fig, name):
    for ext in ("pdf", "png"): fig.savefig(os.path.join(FIG, f"{name}.{ext}"), dpi=300, bbox_inches="tight")

FIN = os.path.join(H, "..", "experiments", "final"); PH = os.path.join(H, "..", "experiments", "posthoc")
def ph(e): return pd.concat([pd.read_csv(os.path.join(PH, f"{e}_{m}.csv")) for m in ("lasso", "rf")])
rmse = lambda e: np.sqrt(np.mean(np.square(e)))

# ---------- Figure 1: the problem (locked run) ----------
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw=dict(width_ratios=[1.45, 0.9, 1]))
src = cm[(cm.method == "source") & (cm.alpha == 0.10) & (cm.pi == 0.0)].copy()
src["label"] = src.disease + " · " + src.cohort.str.replace("_", " ")
order = src.groupby("label").fpr.mean().sort_values().index; yy = {l: i for i, l in enumerate(order)}
a = ax[0]; a.axvline(0.10, color=INK2, lw=1, ls="--"); a.text(0.115, -0.75, "target 10%", color=INK2, fontsize=6.5, va="center")
for mdl, mk, col in [("lasso", "o", S["source"]), ("rf", "D", "#eb6834")]:
    x = src[src.model == mdl]; a.scatter(x.fpr, [yy[l] for l in x.label], s=16, marker=mk, color=col, edgecolor=SURF,
                                         linewidth=0.8, label="LASSO" if mdl == "lasso" else "Random forest", zorder=3)
a.set_yticks(range(len(order))); a.set_yticklabels(order, fontsize=6); a.set_xlabel("Realised false-positive rate")
a.set_title("A  Training cut-off, new cohorts", loc="left", fontsize=8, color=INK); a.grid(axis="x", color=GRID, lw=0.6)
a.set_ylim(-1.4, len(order) - 0.5); a.legend(frameon=False, fontsize=6.5, loc="lower right", bbox_to_anchor=(1.0, 0.12), markerscale=1.3, handletextpad=0.2)
b = ax[1]
for mdl, mk, c in [("lasso", "o", S["source"]), ("rf", "D", "#eb6834")]:
    x = src[src.model == mdl]; b.scatter(x.auc, x.fpr, s=16, marker=mk, color=c, edgecolor=SURF, linewidth=0.8, zorder=3)
b.axhline(0.10, color=INK2, lw=1, ls="--"); b.set_xlabel("AUROC at the new cohort"); b.set_ylabel("Realised false-positive rate")
b.set_title("B  AUROC hides it", loc="left", fontsize=8, color=INK); b.grid(color=GRID, lw=0.6)
c = ax[2]; P = [0.0, 0.01, 0.05, 0.2]
for m in ["em", "mlls", "gauss2", "featstd", "source", "shift2"]:
    x = cm[(cm.method == m) & (cm.alpha == 0.10)].groupby("pi").err.apply(rmse).reindex(P)
    c.plot(range(len(P)), x.values, color=S[m], lw=1.8, marker=MK[m], ms=4.5, mec=SURF, label=SHORT[m])
c.set_xticks(range(len(P))); c.set_xticklabels(["0%", "1%", "5%", "20%"]); c.set_xlabel("Cases in the unlabelled pool")
c.set_ylabel("Cohort-RMSE of FPR"); c.grid(axis="y", color=GRID, lw=0.6); c.set_ylim(0, 0.47)
c.set_title("C  Label-free fixes", loc="left", fontsize=8, color=INK)
c.legend(frameon=False, fontsize=5.8, loc="upper left", bbox_to_anchor=(1.0, 1.0), handlelength=1.5)
for z in ax: z.tick_params(labelsize=6.5)
fig.subplots_adjust(left=0.2, right=0.86, top=0.88, bottom=0.17, wspace=0.55); save(fig, "Figure1")

# ---------- Figure 2: local recalibration, and where it fails ----------
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw=dict(width_ratios=[1.1, 1.1, 1]))
d = pd.concat([pd.read_csv(os.path.join(FIN, f"final_{m}.csv.gz")) for m in ("lasso", "rf")])
d = d[(d.alpha == 0.10) & (d.pi == 0.0)]
a = ax[0]; MM = ["source", "local_q", "ctrl10", "rpoolmean", "rpool"]; yb = np.arange(len(MM))[::-1]
for yv, m in zip(yb, MM):
    v = d[d.method == m].fpr.values  # abstention counts as FPR 0, as in the tables
    q = np.percentile(v, [5, 25, 50, 75, 95])
    a.plot([q[0], q[4]], [yv, yv], color=S[m], lw=1); a.plot([q[1], q[3]], [yv, yv], color=S[m], lw=5, solid_capstyle="butt")
    a.plot(q[2], yv, "o", color=SURF, mec=S[m], ms=4)
    a.text(0.83, yv, f"{(v > 0.15).mean() * 100:.0f}%", va="center", fontsize=6.5, color=INK, clip_on=False)
a.text(0.83, len(MM) - 0.45, "FPR > 15%", fontsize=6, color=INK2, clip_on=False); a.axvline(0.10, color=INK2, lw=1, ls="--")
a.set_yticks(yb); a.set_yticklabels([SHORT[m] for m in MM], fontsize=6.5); a.set_xlim(0, 0.8); a.set_ylim(-0.6, len(MM) - 0.1)
a.set_xlabel("FPR per simulated deployment"); a.grid(axis="x", color=GRID, lw=0.6)
a.set_title("A  Same-site pool (locked)", loc="left", fontsize=8, color=INK)
b = ax[1]; e3, e5 = ph("E3"), ph("E5")
e3 = e3[e3.alpha == 0.10].groupby(["model", "pool_from", "cohort", "method"]).fpr.mean().reset_index().assign(setting="Other cohort")
e5 = e5[e5.alpha == 0.10].groupby(["model", "pool_from", "cohort", "method"]).fpr.mean().reset_index()
e5["setting"] = np.where(e5.pool_from == e5.cohort, "Same centre", "Other centre")
ee = pd.concat([e5, e3]); SET = ["Same centre", "Other centre", "Other cohort"]; MB = ["source", "local_q", "rpoolmean"]
r_ = np.random.default_rng(0)
for j, st in enumerate(SET):
    for k, m in enumerate(MB):
        v = ee[(ee.setting == st) & (ee.method == m)].fpr.values; yv = (len(SET) - 1 - j) + (k - 1) * 0.25
        b.scatter(v, yv + r_.uniform(-0.07, 0.07, len(v)), s=7, color=S[m], alpha=0.75, lw=0, label=SHORT[m] if j == 0 else None)
        b.plot(np.median(v), yv, "|", color=INK, ms=7, mew=1.4)
b.axvline(0.10, color=INK2, lw=1, ls="--"); b.set_yticks(range(len(SET))[::-1]); b.set_yticklabels(SET, fontsize=6.5)
b.set_xlabel("Realised FPR (mean over splits)"); b.grid(axis="x", color=GRID, lw=0.6)
b.set_title("B  Where the pool comes from", loc="left", fontsize=8, color=INK)
b.legend(frameon=False, fontsize=6, loc="upper right", markerscale=1.8, handletextpad=0.1)
c = ax[2]; e2 = ph("E2"); e2 = e2[(e2.alpha == 0.10) & (e2.pi == 0.05)]
t = e2.groupby(["cohort", "n_pool", "method"]).fpr.apply(lambda v: (v > 0.15).mean()).reset_index()
t = t[t.n_pool <= 200].groupby(["n_pool", "method"]).fpr.mean().unstack()
for m in ["ctrl10", "local_q", "rpoolmean", "rpool"]:
    c.plot(t.index, 100 * t[m], color=S[m], lw=1.8, marker=MK[m], ms=4.5, mec=SURF, label=SHORT[m])
c.set_xlabel("Unlabelled pool size (5% cases)"); c.set_ylabel("Deployments with FPR > 15% (%)"); c.grid(axis="y", color=GRID, lw=0.6)
c.set_xscale("log"); c.set_xticks([25, 50, 100, 200]); c.set_xticklabels(["25", "50", "100", "200"]); c.minorticks_off()
c.set_ylim(0, 42); c.set_title("C  How large a pool", loc="left", fontsize=8, color=INK); c.legend(frameon=False, fontsize=5.8, loc="upper right", handlelength=1.6)
for z in ax: z.tick_params(labelsize=6.5)
fig.subplots_adjust(left=0.1, right=0.99, top=0.88, bottom=0.17, wspace=0.85); save(fig, "Figure2"); print("figures written", FIG)
