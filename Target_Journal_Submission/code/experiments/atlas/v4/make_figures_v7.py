"""Figures v4 (manuscript/figures_v4/). Reads v4 result files only."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
from common_v4 import *
FIG = os.path.join(HERE, "..", "..", "..", "..", "manuscript", "figures_v7"); os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
A = 0.10; dev, lock = split()
per = pd.read_csv(os.path.join(OUT, "atlas_perpop_v4.csv")); het = pd.read_csv(os.path.join(OUT, "heterogeneity_v4.csv"))
nw = META.groupby("study_name").non_westernized.agg(lambda x: (x == "yes").mean() > .5)
PLACE = {"LokmerA_2019": "Cameroon", "GuptaA_2019": "India", "BritoIL_2016": "Fiji"}
LAB = {"SRC": "training cut-off", "ATLAS": "pooled reference", "ALIGN": "feature alignment", "BURN": "burn-in", "BURN-PAC": "strict burn-in"}
C = {"SRC": "#8c8c8c", "ATLAS": "#e6a700", "ALIGN": "#b35806", "AUG": "#7b3294", "BURN": "#2166ac", "BURN-PAC": "#1b7837"}
def fig1(model, name):
    fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    for a, d in zip(ax, ["CRC", "IBD", "T2D"]):
        c = per[(per.disease == d) & (per.model == model) & per.strict].sort_values("fpr").reset_index(drop=True)
        lo = stats.beta.ppf(.025, c.k, c.n - c.k + 1); hi = stats.beta.ppf(.975, c.k + 1, c.n - c.k)
        h = het[(het.disease == d) & (het.model == model) & het.strict].iloc[0]
        a.axhspan(h.pi_lo, h.pi_hi, color="#e5e5e5", zorder=0, label="95% prediction interval")
        a.axhspan(.05, .15, color="#cfe3f3", zorder=0, label="0.05–0.15 band"); a.axhline(A, ls="--", c="k", lw=.7)
        isnw = c.study.map(nw).values
        a.errorbar(c.index, c.fpr, yerr=[c.fpr - lo, hi - c.fpr], fmt="none", ecolor="#999", lw=.6)
        a.scatter(c.index[~isnw], c.fpr[~isnw], s=10, c="#2166ac", zorder=3, label="westernised")
        a.scatter(c.index[isnw], c.fpr[isnw], s=14, marker="D", c="#d95f02", zorder=3, label="non-westernised")
        a.set_title(f"{d}: pooled {h.pooled:.2f}, I² {100*h.I2:.0f}%\n{len(c)} populations, {int(h.people):,} people", fontsize=8)
        a.set_xticks([]); a.set_xlabel("healthy populations (sorted)")
    ax[0].set_ylabel("share of healthy people flagged (FPR)"); ax[0].legend(fontsize=6, loc="upper left", frameon=False)
    fig.tight_layout(); [fig.savefig(os.path.join(FIG, f"{name}.{e}"), dpi=300) for e in ["pdf", "png"]]
fig1("lasso", "Figure1_atlas_lasso_strict"); fig1("rf", "FigureS1_atlas_rf_strict")
# Figure 2: mechanism
ts = pd.read_csv(os.path.join(OUT, "taxa_shift_v4.csv")); tt = pd.read_csv(os.path.join(OUT, "taxa_top_v4.csv"))
fig, ax = plt.subplots(1, 4, figsize=(9.0, 3.0), gridspec_kw=dict(width_ratios=[1.1, 1, 1, 1]))
for d, col in zip(["CRC", "IBD", "T2D"], ["#1b9e77", "#d95f02", "#7570b3"]):
    g = ts[ts.disease == d]; ax[0].scatter(g["shift"], g.fpr, s=10, c=col, label=f"{d} (ρ = {stats.spearmanr(g['shift'], g.fpr)[0]:.2f})")
ax[0].axhline(A, ls="--", c="k", lw=.7); ax[0].set_xlabel("population score shift (logit)"); ax[0].set_ylabel("FPR (LASSO, strict set)")
ax[0].legend(fontsize=6, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 1.0), handletextpad=0.2); ax[0].set_title("A", loc="left", fontweight="bold")
for a, d, lab in zip(ax[1:], ["CRC", "IBD", "T2D"], "BCD"):
    s = ts[ts.disease == d].sort_values("fpr", ascending=False).study.iloc[0]; g = tt[(tt.disease == d) & (tt.study == s)].iloc[::-1]
    raw = g.taxon.str.replace(r"^([a-z])__", r"\1:", regex=True)
    def fmt(t):
        r_, n = t.split(":", 1); n = n.replace("_", " ").replace("complex", "complex").replace("[", "").replace("]", "")
        import re as _re; n = _re.sub(r" sp CAG (\d+)", r" sp. CAG-\1", n)
        tail = ""
        if " CAG-" in n: n, tail = n.split(" CAG-"); tail = " CAG-" + tail
        return (f"$\\it{{{n.replace(' ', '\\ ')}}}$" + tail) if r_ in "sg" and not n.startswith(("Firmicutes bacterium", "[")) else n + tail
    names = raw.map(fmt)
    a.barh(names, g.contrib, color=np.where(g.w > 0, "#b2182b", "#2166ac")); a.set_title(f"{lab}  {d}: {PLACE.get(s, s)} (FPR {ts[(ts.disease == d) & (ts.study == s)].fpr.iloc[0]:.2f})", loc="left", fontsize=7)
    a.tick_params(axis="y", labelsize=5.5); a.set_xlabel("contribution to shift")
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color="#b2182b", label="higher than training controls, raises score"), Patch(color="#2166ac", label="lower than training controls, raises score")], fontsize=6, frameon=False, loc="lower center", ncol=2)
fig.tight_layout(rect=(0, 0.06, 1, 1)); [fig.savefig(os.path.join(FIG, f"Figure2_mechanism.{e}"), dpi=300) for e in ["pdf", "png"]]
# Figure 3: fixes on a fixed population set + stress tests + contaminated pools
u = pd.read_csv(os.path.join(OUT, "deploy_v4_units.csv")); S = json.load(open(os.path.join(OUT, "summary_v4.json")))
r = u[(u.design == "random") & u.pop_eval.isin(lock)]
fixed = set(r[(r.N == 200)].pop_eval); rf = r[r.pop_eval.isin(fixed)]
fig, ax = plt.subplots(1, 3, figsize=(8.6, 3.3))
for meth in ["SRC", "ATLAS", "BURN", "BURN-PAC"]:
    g = rf[rf.method == meth].groupby("N")["mad"].mean(); ax[0].plot(g.index, g.values, "o-", c=C[meth], label=LAB[meth], ms=3)
g = rf[(rf.method == "ALIGN")]; ax[0].plot([100], [g["mad"].mean()], "s", c=C["ALIGN"], label="feature alignment (N=100)")
f = os.path.join(OUT, "control_augmentation_v4.csv")
if os.path.exists(f):
    ca = pd.read_csv(f); ca = ca[ca.aug & ca["pop"].isin(fixed)]; ax[0].axhline((ca.fpr - A).abs().mean(), c=C["AUG"], ls=":", label="control augmentation")
ax[0].set_xscale("log"); ax[0].minorticks_off(); ax[0].set_xticks([25, 50, 100, 200]); ax[0].set_xticklabels([25, 50, 100, 200]); ax[0].set_xlabel("burn-in size N")
ax[0].set_ylabel("mean |FPR − 0.10|"); ax[0].set_title(f"A  locked, fixed set ({len(fixed)} populations)", loc="left", fontsize=7); ax[0].set_ylim(0.015, 0.155); ax[0].set_yticks([0.02, 0.04, 0.06, 0.08, 0.10]); ax[0].legend(fontsize=5.5, frameon=False, loc="upper right", ncol=2, bbox_to_anchor=(1.02, 1.0), columnspacing=0.8)
designs = [("random\nsplit", "random/all_strict/N100"), ("age/BMI/\nsex halves", "stress/covariate/N100"), ("accession\norder", "stress/accession/N100"),
           ("other\nsub-site", "stress/subsite/N100"), ("other\ncohort", "stress/neighbour/N100")]
for i, (lab, k) in enumerate(designs):
    for j, meth in enumerate(["SRC", "BURN"]):
        v = S[f"{k}/{meth}"]["p15"]; ax[1].bar(i + (j - .5) * .38, v["mean"], .36, color=C[meth], yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]], error_kw=dict(lw=.6), label=LAB[meth] if i == 0 else None)
    ax[1].text(i, -0.06, f"{S[f'{k}/BURN']['p15']['populations']} " + ("studies" if "subsite" in k else "pop."), ha="center", fontsize=5)
ax[1].set_xticks(range(len(designs))); ax[1].set_xticklabels([d[0] for d in designs], fontsize=5.5); ax[1].set_ylabel("share of burn-ins with FPR > 0.15"); ax[1].set_ylim(-0.08, None)
ax[1].set_title("B  where the burn-in comes from", loc="left", fontsize=7); ax[1].legend(fontsize=6, frameon=False, loc="upper left")
cs = pd.read_csv(os.path.join(OUT, "deploy_v4_cc_summary.csv")); cs = cs[(cs.N == 100) & (cs.pi == cs.pimax) & (cs.pi > 0)]
for meth in ["SRC", "BURN", "BURN-PAC"]:
    g = cs[cs.method == meth].sort_values("pi"); ax[2].plot(g.pi, g.fpr, "o-", c=C[meth], ms=3, label=f"{LAB[meth]}: FPR"); ax[2].plot(g.pi, g.sens, "o--", c=C[meth], ms=3, alpha=.6, label=f"{LAB[meth]}: sensitivity")
ax[2].axhline(A, ls="--", c="k", lw=.7); ax[2].set_xlabel("share of patients in burn-in group"); ax[2].set_ylabel("rate in locked case–control cohorts")
ax[2].set_ylim(0, 0.52); ax[2].set_xticks([0.01, 0.05, 0.10]); ax[2].set_title("C  contaminated burn-in, N = 100", loc="left", fontsize=7); ax[2].legend(fontsize=5, frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.2), columnspacing=0.6)
fig.tight_layout(); [fig.savefig(os.path.join(FIG, f"Figure3_fixes_stress.{e}"), dpi=300) for e in ["pdf", "png"]]
print("figures written", sorted(os.listdir(FIG)), "fixed set:", sorted(fixed))
