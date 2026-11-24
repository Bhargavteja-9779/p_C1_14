"""Figure 2 (v11): what a site can do. A: exact law of the burn-in FPR vs N (fprcal); B: within-site burn-in vs training
cut-off, 28 classifiers (v5_h4_units.csv, H4); C: power of local verification (verify_power_v5.csv, post hoc)."""
import os, sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.ticker
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results"); O = os.path.join(H, "..", "..", "..", "..", "manuscript", "figures_v11")
sys.path.insert(0, os.path.join(H, "..", "..", "..", "tool")); from fprcal import fpr_law, k_expected, k_pac
TXT, MUT, BLUE, ORA, AQUA = "#0b0b0b", "#52514e", "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": MUT, "xtick.color": MUT, "ytick.color": MUT, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6})
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.5)); plt.subplots_adjust(wspace=.45)
Ns = np.arange(20, 801, 5); a = ax[0]
for rule, c, lab in [("expected", BLUE, "E[FPR] ≤ 0.10 rule"), ("pac", ORA, "PAC rule (δ = 0.05)")]:
    q = [fpr_law(N, k_expected(N, .1) if rule == "expected" else k_pac(N, .1)) for N in Ns]
    ok = [x["feasible"] for x in q]; a.plot(Ns[ok], [x["P(FPR>0.15)"] for x, o in zip(q, ok) if o], color=c, lw=1.1, label=lab)
a.axvline(100, color=MUT, lw=.8, ls="--"); a.set_xscale("log"); a.set_xticks([25, 50, 100, 200, 400, 800]); a.set_xticklabels(["25", "50", "100", "200", "400", "800"])
a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); a.set_xlabel("burn-in size N (people)"); a.set_ylabel("P(realised FPR > 0.15)"); a.legend(frameon=False, fontsize=6); a.set_title("A  Exact risk of a high FPR", loc="left", color=TXT)
b = ax[1]; u = pd.read_csv(os.path.join(R, "v5_h4_units.csv")); pt = u.groupby(["test", "model"])[["src", "burn"]].mean().reset_index().sort_values("src")
y = np.arange(len(pt)); b.hlines(y, pt.burn, pt.src, color="#c3c2b7", lw=1)
b.scatter(pt.src, y, s=12, color=ORA, label="training cut-off", zorder=3, edgecolor="white", lw=.6); b.scatter(pt.burn, y, s=12, color=BLUE, label="burn-in, N = 100", zorder=3, edgecolor="white", lw=.6)
b.set_yticks([]); b.set_ylabel(f"{len(pt)} classifiers (14 tests × LASSO/RF)"); b.set_xlabel("mean |FPR − 0.10| within site"); b.legend(frameon=False, fontsize=6, loc="lower right")
b.set_title(f"B  Burn-in better in {(pt.burn < pt.src).sum()}/{len(pt)}", loc="left", color=TXT)
c = ax[2]; v = pd.read_csv(os.path.join(R, "verify_power_v5.csv")); v = v[v.model == "lasso"]
c.plot(v.n, v.mean_power_over025, color=BLUE, lw=2, marker="o", ms=4, label="true FPR > 0.25"); c.plot(v.n, v.mean_power_over015, color=AQUA, lw=2, marker="o", ms=4, label="true FPR > 0.15")
c.plot(v.n, v.max_false_alarm_le015, color=MUT, lw=1.2, ls="--", label="false alarm (FPR ≤ 0.15), max")
c.set_xscale("log"); c.set_xticks([25, 50, 100, 200]); c.set_xticklabels(["25", "50", "100", "200"]); c.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); c.set_ylim(0, 1.02)
c.set_xlabel("local healthy people checked (n)"); c.set_ylabel("probability the check flags it"); c.legend(frameon=False, fontsize=6, loc="lower right", bbox_to_anchor=(1, .1))
c.set_title("C  Verifying a stated FPR (LASSO atlas)", loc="left", color=TXT)
for e in ["pdf", "png"]: fig.savefig(os.path.join(O, f"figure2_site.{e}"), dpi=300, bbox_inches="tight", facecolor="white")
print(pt.round(3).to_string())
