# v21: open-symbol note moved into the legend, rho text moved off the dotted line (review r19). v19: Figure 1D x-axis widened (AUROC 0.44 points off the edge) and title worded as a null result (review r17).
"""Figure 1 (v15): atlas of realised FPR, 14 tests x 36 strict healthy populations. Reads v5 result files only."""
import os, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); O = os.path.join(R, "..", "..", "..", "..", "..", "manuscript", "figures_v21")
TXT, MUT, BLUE, RED, MID = "#0b0b0b", "#52514e", "#2a78d6", "#e34948", "#f0efec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": MUT, "axes.labelcolor": TXT, "xtick.color": MUT, "ytick.color": MUT,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6})
meta = pd.read_csv(os.path.join(os.path.dirname(R), "..", "..", "..", "tool", "fprcal", "data", "atlas_perpop_strict_v5.csv"))
cn = meta.drop_duplicates("study").set_index("study")[["country", "non_westernized"]]
per = pd.read_csv(os.path.join(R, "v5_perpop_strict.csv")); het = pd.read_csv(os.path.join(R, "v5_het_strict.csv"))
idx = pd.read_csv(os.path.join(R, "v5_popindex_strict_lasso.csv")).sort_values("index")
L = per[per.model == "lasso"].copy(); L["l2"] = np.log2(np.clip(L.fpr, .005, 1) / .10)
hl = het[het.model == "lasso"].sort_values("tau"); rows = hl.test.tolist(); cols = idx.study.tolist()
M = L.pivot(index="test", columns="study", values="l2").reindex(index=rows, columns=cols)
fig = plt.figure(figsize=(7.2, 10.4)); G = fig.add_gridspec(2, 1, height_ratios=[2.4, 7.6], hspace=.08)
gs = G[1].subgridspec(2, 3, height_ratios=[1.25, 1], hspace=.62, wspace=.45)
import geopandas as gpd, warnings; warnings.filterwarnings("ignore")
w = gpd.read_file("zip://" + os.path.join(os.path.dirname(R), "data", "ne_110m_admin_0_countries.zip")); w = w[w.ADM0_A3 != "ATA"]
mx = fig.add_subplot(G[0]); w.plot(ax=mx, color="#e6e5e1", edgecolor="white", lw=.3)
w["c"] = w.geometry.representative_point(); cen = {r.ADM0_A3: (r.c.x, r.c.y) for r in w.itertuples()}; cen.update({"FRA": (2.5, 46.5), "NOR": (9, 61)})
P = idx.merge(per[(per.model == "lasso")].groupby("study").n.max().rename("n").reset_index(), on="study"); P["iso"] = P.study.map(cn.country)
P["k"] = P.groupby("iso").cumcount(); P["x"] = [cen[i][0] + 2.2 * k for i, k in zip(P.iso, P.k)]; P["y"] = [cen[i][1] for i in P.iso]
cm0 = LinearSegmentedColormap.from_list("d0", [BLUE, MID, RED]); v = float(np.abs(P["index"]).max())
sc = mx.scatter(P.x, P.y, s=6 + P.n / 8, c=P["index"], cmap=cm0, vmin=-v, vmax=v, edgecolor=TXT, lw=.4, zorder=3)
mx.set_xlim(-170, 190); mx.set_ylim(-58, 84); mx.set_aspect("equal"); mx.set_axis_off()
cbm = fig.colorbar(sc, ax=mx, fraction=.02, pad=.01); cbm.set_label("false-alarm index\n(mean deviation of logit FPR)", fontsize=6); cbm.outline.set_visible(False)
for nn in [100, 500, 1000]: mx.scatter([], [], s=6 + nn / 8, color="white", edgecolor=TXT, lw=.4, label=f"n = {nn}")
mx.legend(frameon=False, loc="lower left", fontsize=6, scatterpoints=1)
mx.set_title(f"A  {len(P)} healthy populations, {P.iso.nunique()} countries: false-alarm index", loc="left", fontsize=7, color=TXT)
ax = fig.add_subplot(gs[0, :]); cmap = LinearSegmentedColormap.from_list("d", [BLUE, MID, RED])
im = ax.imshow(np.ma.masked_invalid(M.values), cmap=cmap, norm=TwoSlopeNorm(0, -3.4, 3.4), aspect="auto", interpolation="nearest")
ax.set_facecolor("white"); ax.set_yticks(range(len(rows))); ax.set_yticklabels([r.replace("_", " ") for r in rows])
lab = [f"{cn.loc[s,'country']}·{s.split('_')[0][:-1] if s.split('_')[0][-1].isupper() else s.split('_')[0]}" for s in cols]
ax.set_xticks(range(len(cols))); ax.set_xticklabels(lab, rotation=90, fontsize=6.5)
for t, s in zip(ax.get_xticklabels(), cols):
    if cn.loc[s, "non_westernized"]: t.set_fontweight("bold"); t.set_color(TXT)
ax.set_xticks(np.arange(-.5, len(cols)), minor=True); ax.set_yticks(np.arange(-.5, len(rows)), minor=True)
ax.grid(which="minor", color="white", lw=.8); ax.tick_params(which="minor", length=0); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=.025, pad=.01, ticks=np.log2(np.array([.01, .025, .05, .1, .2, .4, .8]) / .1))
cb.ax.set_yticklabels(["0.01", "0.025", "0.05", "0.10", "0.20", "0.40", "0.80"]); cb.set_label("realised FPR (target 0.10)"); cb.outline.set_visible(False)
ax.set_title("B  Realised FPR of 14 LASSO tests in each population (bold: non-westernised in cMD metadata)",
             loc="left", fontsize=7, color=TXT)
# B prediction intervals
bx = fig.add_subplot(gs[1, :2]); order = het[het.model == "lasso"].sort_values("pi_hi").test.tolist()
for j, (m, c, off) in enumerate([("lasso", BLUE, -.17), ("rf", "#6250d6", .17)]):
    h = het[het.model == m].set_index("test").loc[order]; y = np.arange(len(order)) + off
    bx.hlines(y, np.clip(h.pi_lo, .001, 1), h.pi_hi, color=c, lw=2, label=f"{m.upper() if m=='rf' else 'LASSO'}: 95% prediction interval")
    bx.scatter(h.pooled, y, s=14, color=c, edgecolor="white", lw=.8, zorder=3)
    cl = h.pi_lo.values < .001
    bx.scatter(np.full(cl.sum(), .001), y[cl], marker="<", s=14, color=c, zorder=3)
bx.axvspan(.05, .15, color="#d9d8d4", alpha=.5, lw=0); bx.axvline(.10, color=MUT, lw=.8, ls="--")
bx.set_xscale("log"); bx.set_xticks([.001, .01, .05, .1, .2, .5, 1]); bx.set_xticklabels(["0.001", "0.01", "0.05", "0.10", "0.20", "0.50", "1"])
bx.set_yticks(range(len(order))); bx.set_yticklabels([o.replace("_", " ") for o in order]); bx.set_xlabel("FPR in a new healthy population (dot = pooled)")
bx.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5, -.19), ncol=2, fontsize=6); bx.set_title("C  Where a new population's FPR may land", loc="left", fontsize=7, color=TXT)
# C AUROC vs tau
cx = fig.add_subplot(gs[1, 2])
for m, c, mk in [("lasso", BLUE, "o"), ("rf", "#6250d6", "s")]:
    h = het[het.model == m]; lo = h.auroc < .6
    cx.scatter(h.auroc[~lo], h.tau[~lo], s=18, color=c, marker=mk, edgecolor="white", lw=.8, label="LASSO" if m == "lasso" else "RF")
    cx.scatter(h.auroc[lo], h.tau[lo], s=18, facecolor="white", marker=mk, edgecolor=c, lw=1)
cx.axvline(.6, color=MUT, lw=.6, ls=":")
from scipy import stats; r, p = stats.spearmanr(het.auroc, het.tau)
cx.set_xlabel("out-of-fold AUROC"); cx.set_ylabel("between-population τ (logit FPR)")
cx.text(.98, .98, f"Spearman ρ = {r:.2f}, P = {p:.2f}", transform=cx.transAxes, ha="right", va="top", fontsize=6, color=MUT, bbox=dict(facecolor="white", edgecolor="none", pad=1))
cx.set_xlim(.36, .97); cx.set_ylim(top=1.78); from matplotlib.lines import Line2D; hh, ll = cx.get_legend_handles_labels(); hh.append(Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor=MUT)); ll.append("AUROC < 0.6"); cx.legend(hh, ll, frameon=False, loc="upper center", bbox_to_anchor=(.5, .93), ncol=3, fontsize=5.5, handletextpad=.2, columnspacing=.8); cx.set_title("D  AUROC did not predict the spread", loc="left", fontsize=7, color=TXT)
for e in ["pdf", "png"]: fig.savefig(os.path.join(O, f"figure1_atlas.{e}"), dpi=300, bbox_inches="tight", facecolor="white")
print("ok", r, p)
