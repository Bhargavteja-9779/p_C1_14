"""Figure S2 (v17): audit of a second published index, GMHI (plan v7). A: developers' own healthy data by study;
B: same samples scored from developers' MetaPhlAn2 and cMD MetaPhlAn3 profiles (post hoc)."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results"); O = os.path.join(H, "..", "..", "..", "..", "manuscript", "figures_v17"); os.makedirs(O, exist_ok=True)
TXT, MUT, GRID, BLUE, ORA = "#0b0b0b", "#52514e", "#c3c2b7", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": MUT, "xtick.color": MUT, "ytick.color": MUT, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6})
res = json.load(open(os.path.join(R, "gmhi_results.json"))); a0 = res["alpha_gmhi"]
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.9), gridspec_kw=dict(width_ratios=[1.2, 1])); plt.subplots_adjust(wspace=.35)
g = pd.read_csv(os.path.join(R, "gmhi_dev_perstudy.csv")).sort_values("fpr").reset_index(drop=True); x = np.arange(len(g))
lo = [stats.beta.ppf(.025, k, n - k + 1) if k > 0 else 0 for k, n in zip(g.k, g.n)]; hi = [stats.beta.ppf(.975, k + 1, n - k) if k < n else 1 for k, n in zip(g.k, g.n)]
a = ax[0]; a.vlines(x, lo, hi, color=GRID, lw=.7)
for m, c, lab in [(~g.ea, BLUE, "other"), (g.ea, ORA, "East Asian")]: a.scatter(x[m], g.fpr[m], s=14, color=c, zorder=3, label=lab)
a.axhline(a0, color=TXT, lw=.8, ls="--"); a.text(.02, a0 + .02, f"training FPR {a0:.2f}", transform=a.get_yaxis_transform(), fontsize=6)
a.set_xticks([]); a.set_ylim(-.02, 1); a.set_ylabel("healthy people labelled non-healthy"); a.set_xlabel(f"{len(g)} training studies (developers' profiles)")
a.set_title("A  GMHI, own training data", loc="left", color=TXT); a.legend(frameon=False, fontsize=6, loc="upper left")
sh = pd.read_csv(os.path.join(R, "gmhi_profiler_shift_perstudy.csv")); EA = {"CHN", "JPN", "KOR", "HKG", "TWN"}; ea = sh.country.isin(EA)
mres = json.load(open(os.path.join(R, "posthoc_gmhi_matching.json")))
b = ax[1]; b.plot([0, 1], [0, 1], color=GRID, lw=.8, ls="--")
b.scatter(sh.flag_dev[~ea], sh.flag_cmd[~ea], s=16, color=BLUE, label="other"); b.scatter(sh.flag_dev[ea], sh.flag_cmd[ea], s=16, color=ORA, label="East Asian")
b.set_xlabel("share flagged, developers' profiles (MetaPhlAn2)"); b.set_ylabel("share flagged, cMD profiles (MetaPhlAn3)"); b.set_xlim(-.02, 1); b.set_ylim(-.02, 1)
b.text(.98, .02, f"same {mres['n_overlap']:,} samples; pooled {mres['flag_dev_profiles']:.0%} → {mres['flag_cmd_profiles']:.0%}", transform=b.transAxes, fontsize=6, ha="right")
b.set_title("B  Same samples, two profiler versions", loc="left", color=TXT); b.legend(frameon=False, fontsize=6, loc="lower right", bbox_to_anchor=(1, .07))
for e in ("png", "pdf"): fig.savefig(os.path.join(O, f"figureS2_gmhi.{e}"), dpi=300, bbox_inches="tight")
print("ok")
