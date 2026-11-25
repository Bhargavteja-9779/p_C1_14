"""Main figures (vector PDF + PNG) from results/cohort_level_summary.csv and dev round 4B. Palette: validated default
categorical order (blue, orange, aqua, yellow, magenta, green); text in neutral inks; one y-axis per panel."""
import os, sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src import calibrate as C
H = os.path.dirname(__file__); R = os.path.join(H, "..", "..", "results"); FIG = os.path.join(H, "..", "..", "figures"); os.makedirs(FIG, exist_ok=True)
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
S = dict(source="#2a78d6", em="#eb6834", featstd="#1baf7a", shift2="#eda100", ctrl10="#e87ba4", rpoolmean="#008300")
LAB = dict(source="Training threshold", em="Label-shift EM", featstd="Per-site standardisation",
           shift2="Unlabelled mixture fit", ctrl10="10 labelled local controls", rpoolmean="Rank rule on local pool (ours)")
SHORT = dict(source="Training", em="Label-shift EM", featstd="Per-site std.", shift2="Mixture fit", ctrl10="10 local controls", rpoolmean="Rank rule (ours)")
MK = dict(source="o", em="s", featstd="^", shift2="D", ctrl10="v", rpoolmean="P")
plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "font.family": "DejaVu Sans", "figure.facecolor": "white"})
cm = pd.read_csv(os.path.join(R, "cohort_level_summary.csv"))
def save(fig, name):
    for ext in ("pdf", "png"): fig.savefig(os.path.join(FIG, f"{name}.{ext}"), dpi=300, bbox_inches="tight")

# ---------- Figure 1: the problem ----------
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.5), gridspec_kw=dict(width_ratios=[1.4, 1, 1]))
src = cm[(cm.method == "source") & (cm.alpha == 0.10) & (cm.pi == 0.0)].copy()
src["label"] = src.disease + " · " + src.cohort.str.replace("_", " ")
order = src.groupby("label").fpr.mean().sort_values().index; yy = {l: i for i, l in enumerate(order)}
a = ax[0]; a.axvline(0.10, color=INK2, lw=1, ls="--"); a.text(0.11, -0.9, "target 10%", color=INK2, fontsize=6.5, va="top")
for mdl, mk in [("lasso", "o"), ("rf", "D")]:
    x = src[src.model == mdl]; a.scatter(x.fpr, [yy[l] for l in x.label], s=16, marker=mk, color=S["source"] if mdl == "lasso" else "#eb6834",
                                         edgecolor=SURF, linewidth=0.8, label="LASSO" if mdl == "lasso" else "Random forest", zorder=3)
a.set_yticks(range(len(order))); a.set_yticklabels(order, fontsize=6); a.set_xlabel("Realised false-positive rate")
a.set_title("A  Training threshold at 16 locked cohorts", loc="left", fontsize=8, color=INK); a.grid(axis="x", color=GRID, lw=0.6)
a.set_ylim(-1.4, len(order) - 0.5); a.legend(frameon=False, fontsize=6.5, loc="center right", markerscale=1.3, handletextpad=0.2)
b = ax[1]
for mdl, mk, c in [("lasso", "o", S["source"]), ("rf", "D", "#eb6834")]:
    x = src[src.model == mdl]; b.scatter(x.auc, x.fpr, s=16, marker=mk, color=c, edgecolor=SURF, linewidth=0.8, zorder=3)
b.axhline(0.10, color=INK2, lw=1, ls="--"); b.set_xlabel("AUROC at the new cohort"); b.set_ylabel("Realised false-positive rate")
b.set_title("B  AUROC does not reveal it", loc="left", fontsize=8, color=INK); b.grid(color=GRID, lw=0.6)
c = ax[2]; st = os.path.join(H, "..", "experiments", "dev", "explore_v4_lasso.csv")
if os.path.exists(st):
    v = pd.read_csv(st); v = v[(v.part == "B") & (v.pi == 0.0) & (v.method == "local_q")].drop_duplicates("cohort")
    v = v.sort_values("fpr"); c.barh(range(len(v)), v.fpr, color=S["source"], height=0.6)
    c.set_yticks(range(len(v))); c.set_yticklabels(v.cohort.str.replace("_20", " ").str.replace("->", " → "), fontsize=5.5)
    c.axvline(0.10, color=INK2, lw=1, ls="--"); c.set_xlabel("Realised false-positive rate")
c.set_title("C  Threshold set on another\n     study's controls (dev)", loc="left", fontsize=8, color=INK)
fig.tight_layout(); save(fig, "Figure1")

# ---------- Figure 2: what works ----------
fig, ax = plt.subplots(1, 3, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1, 1, 1]))
a = ax[0]; P = [0.0, 0.01, 0.05, 0.2]
for m in S:
    x = cm[(cm.method == m) & (cm.alpha == 0.10)].groupby("pi").err.apply(lambda e: np.sqrt(np.mean(e ** 2))).reindex(P)
    a.plot(range(len(P)), x.values, color=S[m], lw=2, marker=MK[m], ms=5, mec=SURF, label=LAB[m])
a.set_xticks(range(len(P))); a.set_xticklabels(["0%", "1%", "5%", "20%"]); a.set_xlabel("Cases in the unlabelled pool")
a.set_ylabel("Cohort-RMSE of FPR (target 0.10)"); a.grid(axis="y", color=GRID, lw=0.6)
a.set_title("A  Miscalibration vs case share", loc="left", fontsize=8, color=INK)
fig.legend(*a.get_legend_handles_labels(), frameon=False, fontsize=6.5, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))
b = ax[1]; prev = 0.005
x = cm[(cm.disease == "CRC") & (cm.alpha == 0.10) & (cm.pi == 0.01) & cm.method.isin(S)].groupby("method").fpr.mean().reindex(list(S))
vals = 1000 * (1 - prev) * x.values; yb = np.arange(len(S))[::-1]; b.barh(yb, vals, color=[S[m] for m in S], height=0.6)
b.axvline(1000 * (1 - prev) * 0.10, color=INK2, lw=1, ls="--"); b.text(1000 * (1 - prev) * 0.10 + 6, -0.95, "intended", color=INK2, fontsize=6, va="center")
for i, v_ in zip(yb, vals): b.text(v_ + 6, i, f"{v_:.0f}", va="center", fontsize=6.5, color=INK)
b.set_yticks(yb); b.set_yticklabels([SHORT[m] for m in S], fontsize=6); b.set_ylim(-1.4, len(S) - 0.5); b.set_xlim(0, max(vals) * 1.18)
b.set_xlabel("False-positive referrals per 1,000"); b.set_title("B  CRC screening, prevalence 0.5%", loc="left", fontsize=8, color=INK)
c = ax[2]; pms = [0, 0.01, 0.02, 0.05, 0.1]
for dlt, col, mk in [(0.10, "#2a78d6", "o"), (0.05, "#eb6834", "s")]:
    c.plot(range(len(pms)), [C.needed_pool_size(0.10, dlt, p) for p in pms], color=col, lw=2, marker=mk, ms=5, mec=SURF,
           label=f"δ = {dlt:.2f}")
c.set_xticks(range(len(pms))); c.set_xticklabels(["0%", "1%", "2%", "5%", "10%"]); c.set_xlabel("Maximum case share in pool")
c.set_ylabel("Screened samples needed"); c.grid(axis="y", color=GRID, lw=0.6); c.set_ylim(0, 2900); c.legend(frameon=False, fontsize=6.5, loc="upper left", bbox_to_anchor=(0.03, 1.0), title="P(FPR > 10%) ≤ δ", title_fontsize=6.5, alignment="left")
c.set_title("C  How many local samples a lab needs", loc="left", fontsize=8, color=INK)
for z in ax: z.tick_params(labelsize=6.5)
fig.subplots_adjust(left=0.08, right=0.99, top=0.9, bottom=0.33, wspace=0.75); save(fig, "Figure2"); print("figures written", FIG)
