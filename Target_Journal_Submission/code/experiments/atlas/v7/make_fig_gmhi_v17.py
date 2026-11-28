"""Figure S2 (v17): audit of a second published index, GMHI (plan v7). A: developers' own healthy data by study;
B: per-population flag rates of GMHI vs GMWI2 in cMD strict populations; C: within-site burn-in (H6)."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results"); O = os.path.join(H, "..", "..", "..", "..", "manuscript", "figures_v17"); os.makedirs(O, exist_ok=True)
TXT, MUT, GRID, BLUE, ORA = "#0b0b0b", "#52514e", "#c3c2b7", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": MUT, "xtick.color": MUT, "ytick.color": MUT, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6})
res = json.load(open(os.path.join(R, "gmhi_results.json"))); a0 = res["alpha_gmhi"]
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw=dict(width_ratios=[1.2, 1, 1])); plt.subplots_adjust(wspace=.5)
g = pd.read_csv(os.path.join(R, "gmhi_dev_perstudy.csv")).sort_values("fpr").reset_index(drop=True); x = np.arange(len(g))
lo = [stats.beta.ppf(.025, k, n - k + 1) if k > 0 else 0 for k, n in zip(g.k, g.n)]; hi = [stats.beta.ppf(.975, k + 1, n - k) if k < n else 1 for k, n in zip(g.k, g.n)]
a = ax[0]; a.vlines(x, lo, hi, color=GRID, lw=.7)
for m, c, lab in [(~g.ea, BLUE, "other"), (g.ea, ORA, "East Asian")]: a.scatter(x[m], g.fpr[m], s=14, color=c, zorder=3, label=lab)
a.axhline(a0, color=TXT, lw=.8, ls="--"); a.text(.02, a0 + .02, f"training FPR {a0:.2f}", transform=a.get_yaxis_transform(), fontsize=6)
a.set_xticks([]); a.set_ylim(-.02, 1); a.set_ylabel("healthy people labelled non-healthy"); a.set_xlabel(f"{len(g)} training studies (developers' profiles)")
a.set_title("A  GMHI, own training data", loc="left", color=TXT); a.legend(frameon=False, fontsize=6, loc="upper left")
J = pd.read_csv(os.path.join(R, "gmhi_vs_gmwi2_strict.csv")); EA = {"CHN", "JPN", "KOR", "HKG", "TWN"}; ea = J.country.isin(EA)
b = ax[1]; b.scatter(J.fpr_gmwi2[~ea], J.fpr_gmhi[~ea], s=12, color=BLUE, label="other"); b.scatter(J.fpr_gmwi2[ea], J.fpr_gmhi[ea], s=12, color=ORA, label="East Asian")
b.set_xlabel("GMWI2: share labelled non-healthy"); b.set_ylabel("GMHI: share labelled non-healthy"); b.set_xlim(-.02, 1); b.set_ylim(-.02, 1)
b.text(.98, .02, f"{res['H5']['n']} cMD populations", transform=b.transAxes, fontsize=6, ha="right")
b.set_title(f"B  GMHI vs GMWI2 (ρ = {res['H5']['rho']:.2f})", loc="left", color=TXT); b.legend(frameon=False, fontsize=6, loc="lower right", bbox_to_anchor=(1, .07))
u = pd.read_csv(os.path.join(R, "gmhi_h6_units.csv")).groupby("pop")[["src", "burn"]].mean()
c = ax[2]
for _, r in u.iterrows(): c.plot([0, 1], [r.src, r.burn], color=GRID, lw=.8)
c.scatter(np.zeros(len(u)), u.src, s=12, color="#c8913a", zorder=3); c.scatter(np.ones(len(u)), u.burn, s=12, color=BLUE, zorder=3)
c.set_xticks([0, 1]); c.set_xticklabels(["published\ncut-off", "local burn-in\n(100 people)"]); c.set_xlim(-.4, 1.4); c.set_ylabel(f"mean |FPR − {a0:.2f}| within site")
c.set_title("C  Burn-in at the site", loc="left", color=TXT)
for e in ("png", "pdf"): fig.savefig(os.path.join(O, f"figureS2_gmhi.{e}"), dpi=300, bbox_inches="tight")
print("ok")
