"""Figure 2 (v15): a published test (GMWI2). A: developers' own healthy training samples, FPR by study (published scores);
B: unseen cMD healthy populations (our scoring, QC r = 0.99); C: taxa behind the East Asian gap; D: case-mix balancing."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results"); O = os.path.join(H, "..", "..", "..", "..", "manuscript", "figures_v15")
TXT, MUT, GRID, BLUE, ORA = "#0b0b0b", "#52514e", "#c3c2b7", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": MUT, "xtick.color": MUT, "ytick.color": MUT, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6})
EA = {"China", "Japan", "South Korea", "CHN", "JPN", "KOR"}; alpha = json.load(open(os.path.join(R, "gmwi2_results.json")))["alpha_gmwi2"]
fig, ax = plt.subplots(2, 2, figsize=(7.2, 5.6)); ax = ax.ravel(); plt.subplots_adjust(wspace=.42, hspace=.6)
def dots(a, g, title, hollow=None):
    g = g.sort_values("fpr").reset_index(drop=True); x = np.arange(len(g)); ea = g.country.isin(EA).values
    lo = np.array([__import__("scipy.stats").stats.beta.ppf(.025, k, n - k + 1) if k > 0 else 0 for k, n in zip(g.k, g.n)])
    hi = np.array([__import__("scipy.stats").stats.beta.ppf(.975, k + 1, n - k) if k < n else 1 for k, n in zip(g.k, g.n)])
    a.vlines(x, lo, hi, color=GRID, lw=.7)
    for m, c, lab in [(~ea, BLUE, "other"), (ea, ORA, "East Asian")]:
        fc = c if hollow is None else np.where(hollow[m], "white", c)
        a.scatter(x[m], g.fpr[m], s=14, color=fc, edgecolor=c, lw=.8, zorder=3, label=lab)
    a.axhline(alpha, color=TXT, lw=.8, ls="--"); a.set_xticks([]); a.set_ylim(-.02, 1); a.set_ylabel("healthy people labelled non-healthy")
    a.set_title(title, loc="left", color=TXT); return g
g = pd.read_csv(os.path.join(R, "gmwi2_published_training_perstudy.csv"))
dots(ax[0], g, "A  Its own healthy training data"); ax[0].set_xlabel(f"{len(g)} training studies (developers' published scores)")
ax[0].text(.02, alpha + .02, f"training FPR {alpha:.2f}", transform=ax[0].get_yaxis_transform(), color=TXT, fontsize=6); ax[0].legend(frameon=False, fontsize=6, loc="upper left")
p = pd.read_csv(os.path.join(R, "gmwi2_perpop_strict.csv")); p = p[~p.seen]; M = pd.read_csv(os.path.join(H, "..", "..", "..", "..", "..", "data", "sampleMetadata.csv.gz"), low_memory=False).drop_duplicates("study_name").set_index("study_name")
p["country"] = M.loc[p.study, "country"].values; ps = p.sort_values("fpr").reset_index(drop=True)
dots(ax[1], ps, "B  Healthy populations it never saw (strict set)"); ax[1].set_xlabel(f"{len(ps)} unseen cMD populations, {int(ps.n.sum()):,} people")
t = pd.read_csv(os.path.join(R, "gmwi2_eastasia_taxa.csv")).head(8).iloc[::-1]; y = np.arange(len(t)); c = ax[2]
c.hlines(y, t.presence_other, t.presence_ea, color=GRID, lw=1.4); c.scatter(t.presence_other, y, s=16, color=BLUE, zorder=3, label="other"); c.scatter(t.presence_ea, y, s=16, color=ORA, zorder=3, label="East Asian")
c.set_yticks(y); c.set_yticklabels([f"{n.split('__')[1].replace('_', ' ')}  ({'+' if w > 0 else '−'}{abs(w):.2f})" for n, w in zip(t.taxon, t.w)], fontsize=6)
c.set_xlabel("share of healthy people carrying the taxon"); c.set_xlim(0, 1); c.legend(frameon=False, fontsize=6, loc="lower right"); c.set_title("C  Taxa behind the gap (weight)", loc="left", color=TXT)
d = ax[3]; nv = pd.read_csv(os.path.join(R, "v6b_perstudy_naive.csv")); bv = pd.read_csv(os.path.join(R, "v6b_perstudy_balanced.csv")).set_index("study_name")
for _, r in nv.iterrows():
    col = ORA if r.ea else BLUE; d.plot([0, 1], [r.fpr, bv.loc[r.study_name, "fpr"]], color=col, alpha=.55 if r.ea else .25, lw=.9)
res = json.load(open(os.path.join(R, "v6b_results.json")))
for i, m in enumerate(["naive", "balanced"]):
    d.scatter([i - .06], [res[m]["ea_median"]], s=40, color=ORA, marker="D", zorder=4, edgecolor="white"); d.scatter([i + .06], [res[m]["other_median"]], s=40, color=BLUE, marker="D", zorder=4, edgecolor="white")
d.set_xticks([0, 1]); d.set_xticklabels(["pooled training", "country × label\nreweighted"]); d.set_xlim(-.3, 1.3); d.set_ylim(-.02, 1.12); d.set_ylabel("healthy people labelled non-healthy")
d.set_title("D  Retraining with reweighted data", loc="left", color=TXT); d.axhline(alpha, color=TXT, lw=.8, ls="--")
d.text(1.08, res["balanced"]["ea_median"], f"{res['balanced']['ea_median']:.2f}", color=ORA, fontsize=6, va="center")
d.text(.5, .985, f"East Asian − other: {res['naive']['gap']:.2f} → {res['balanced']['gap']:.2f}", transform=d.transAxes, ha="center", fontsize=6, color=TXT)
for e in ["png", "pdf"]: fig.savefig(os.path.join(O, f"figure2_published_test.{e}"), dpi=300, bbox_inches="tight")
