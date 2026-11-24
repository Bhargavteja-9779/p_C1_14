import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
OUT = "../../../manuscript/figures_v3/"; BLUE, ORANGE, AQUA, YEL = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"; INK, MUTED = "#0b0b0b", "#8a8984"
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "figure.dpi": 300})
r = pd.read_csv("results/atlas_rows.csv.gz"); C = pd.read_csv("results/atlas_covars.csv.gz").groupby("study_name").non_westernized.first()
ext = r[~r.study.str.startswith("TRAIN")]
def fig1(model, name):
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True)
    for ax, d in zip(axs, ["CRC", "IBD", "T2D"]):
        g = ext[(ext.disease == d) & (ext.model == model)].groupby("study").flag.agg(["sum", "size"]); g = g[g["size"] >= 15]
        g["p"] = g["sum"] / g["size"]; g = g.sort_values("p"); x = np.arange(len(g))
        lo = stats.beta.ppf(.025, g["sum"], g["size"] - g["sum"] + 1); hi = stats.beta.ppf(.975, g["sum"] + 1, g["size"] - g["sum"])
        ax.axhspan(.05, .15, color=BLUE, alpha=.08, lw=0); ax.axhline(.10, color=MUTED, lw=.8, ls="--")
        ax.vlines(x, np.nan_to_num(lo), hi, color=MUTED, lw=.6)
        nw = g.index.map(C) == "yes"
        ax.scatter(x[~nw], g.p[~nw], s=12, color=BLUE, zorder=3, label="westernised", edgecolor="white", lw=.4)
        ax.scatter(x[nw], g.p[nw], s=14, color=ORANGE, marker="D", zorder=3, label="non-westernised", edgecolor="white", lw=.4)
        pooled = g["sum"].sum() / g["size"].sum(); out = np.mean((g.p < .05) | (g.p > .15))
        ax.set_title(f"{d} test: {len(g)} healthy populations\npooled FPR {pooled:.2f}; {out:.0%} outside 0.05–0.15", fontsize=7.5, color=INK)
        ax.set_xticks([]); ax.set_xlabel("population (sorted)")
    axs[0].set_ylabel("realised false-positive rate\n(target 0.10, band 0.05–0.15)"); axs[0].legend(frameon=False, fontsize=6.5, loc="upper left")
    fig.tight_layout(); fig.savefig(OUT + name + ".png"); fig.savefig(OUT + name + ".pdf"); plt.close(fig)
fig1("lasso", "Figure1_atlas_lasso"); fig1("rf", "FigureS1_atlas_rf")
# Figure 2: (a) ICC raw/adjusted; (b) locked healthy mean abs error by method and N
icc = pd.read_csv("results/a4_icc.csv"); s = pd.read_csv("results/deploy_locked_summary.csv")
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8))
lab = [f"{d}\n{m.upper() if m=='rf' else 'LASSO'}" for d, m in zip(icc.disease, icc.model)]; x = np.arange(len(icc))
a.bar(x - .18, icc.icc_raw, .34, color=BLUE, label="cohort only"); a.bar(x + .18, icc.icc_adj, .34, color=ORANGE, label="+ age, sex, BMI, depth, diversity")
a.set_xticks(x); a.set_xticklabels(lab, fontsize=6.5); a.set_ylabel("share of score variance\nbetween cohorts (ICC)"); a.set_ylim(0, .55); a.legend(frameon=False, fontsize=6.5, loc="upper left", ncol=2); a.set_title("a  Cohort effect is not explained by individuals", loc="left", fontsize=8)
h = s[s.kind == "healthy"]
for meth, col, mk, lbl in [("SRC", MUTED, "o", "training threshold (status quo)"), ("ATLAS", YEL, "s", "pooled healthy atlas"), ("BURN", BLUE, "o", "burn-in, expected-FPR rule"), ("BURN-PAC", AQUA, "^", "burn-in, 95%-confidence rule")]:
    q = h[h.method == meth].sort_values("N"); b.plot(q.N, q.mad, marker=mk, color=col, lw=2, ms=5, label=lbl)
b.set_xscale("log"); b.set_xticks([25, 50, 100, 200]); b.set_xticklabels([25, 50, 100, 200]); b.set_xlabel("N people in burn-in (unlabelled)")
b.set_ylabel("mean |realised FPR − 0.10|\nlocked healthy populations"); b.set_ylim(0, None); b.minorticks_off(); b.legend(frameon=False, fontsize=6.5); b.set_title("b  Only local self-calibration fixes it", loc="left", fontsize=8)
fig.tight_layout(); fig.savefig(OUT + "Figure2_mechanism_fix.png"); fig.savefig(OUT + "Figure2_mechanism_fix.pdf"); plt.close(fig)
# Figure 3: (a) exact law vs observed per population (BURN, healthy); (b) contaminated burn-in mean FPR
per = pd.read_csv("results/deploy_locked_perpop.csv"); q = per[(per.kind == "healthy") & (per.method == "BURN")]
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8))
for N, col in zip([25, 50, 100, 200], [YEL, AQUA, ORANGE, BLUE]):
    z = q[q.N == N]; a.scatter(z.pred_p15, z.p15, s=10, color=col, label=f"N={N}", edgecolor="white", lw=.3)
a.set_xlim(0, .25); a.set_ylim(0, .25); a.plot([0, .25], [0, .25], color=MUTED, lw=.8, ls="--"); a.set_xlabel("predicted by exact beta-binomial law"); a.set_ylabel("observed P(FPR > 0.15)")
a.legend(frameon=False, fontsize=6.5); a.set_title("a  Exact law predicts each population", loc="left", fontsize=8)
c = s[(s.kind == "casecontrol") & (s.N == 100)]
conds = [(0, 0, "π=0"), (.01, .01, "π=0.01"), (.05, .05, "π=0.05"), (.05, .01, "π=0.05,\nbound 0.01"), (.10, .10, "π=0.10")]
x = np.arange(len(conds))
for j, (meth, col) in enumerate([("SRC", MUTED), ("BURN", BLUE), ("BURN-PAC", AQUA)]):
    v = [c[(c.pi == p) & (c.pimax == pm) & (c.method == meth)].fpr.mean() for p, pm, _ in conds]
    b.bar(x + (j - 1) * .26, v, .24, color=col, label={"SRC": "status quo", "BURN": "burn-in", "BURN-PAC": "burn-in 95%"}[meth])
b.axhline(.10, color=INK, lw=.8, ls="--"); b.set_xticks(x); b.set_xticklabels([t for *_, t in conds], fontsize=6.5)
b.set_ylabel("mean realised FPR (N=100)"); b.legend(frameon=False, fontsize=6.5); b.set_title("b  Burn-in with patients mixed in", loc="left", fontsize=8)
fig.tight_layout(); fig.savefig(OUT + "Figure3_law_contamination.png"); fig.savefig(OUT + "Figure3_law_contamination.pdf"); plt.close(fig)
print("ok")
