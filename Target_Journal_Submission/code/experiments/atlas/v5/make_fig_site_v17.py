"""v17: classifier labels on Fig 3A rows. Figure 3 (v15, two panels) and Supporting Figure S1 (v15). Same data and code as make_fig_deploy_v11.py, re-laid out:
Fig 3A = within-site burn-in vs training cut-off (v5_h4_units.csv, H4); Fig 3B = sensitivity price (deploy_v4_cc_summary.csv).
Fig S1A = exact law of the burn-in FPR vs N (fprcal); Fig S1B = power of local verification (verify_power_v5.csv, post hoc)."""
import os, sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.ticker
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results"); O = os.path.join(H, "..", "..", "..", "..", "manuscript", "figures_v17")
sys.path.insert(0, os.path.join(H, "..", "..", "..", "tool")); from fprcal import fpr_law, k_expected, k_pac
TXT, MUT, BLUE, TRN, AQUA, VIO, GRID = "#0b0b0b", "#52514e", "#2a78d6", "#c98500", "#1baf7a", "#6250d6", "#c3c2b7"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.edgecolor": MUT, "xtick.color": MUT, "ytick.color": MUT, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .6})
# ---- Figure 3
fig, (b, d) = plt.subplots(1, 2, figsize=(7.2, 2.9)); plt.subplots_adjust(wspace=.38)
u = pd.read_csv(os.path.join(R, "v5_h4_units.csv")); pt = u.groupby(["test", "model"])[["src", "burn"]].mean().reset_index().sort_values("src")
y = np.arange(len(pt)); b.hlines(y, pt.burn, pt.src, color=GRID, lw=1)
b.scatter(pt.src, y, s=12, color=TRN, label="training cut-off", zorder=3, edgecolor="white", lw=.6); b.scatter(pt.burn, y, s=12, color=BLUE, label="burn-in on 100 local people", zorder=3, edgecolor="white", lw=.6)
b.set_yticks(y); b.set_yticklabels([f"{t.replace('_', ' ')} {m.upper() if m == 'rf' else 'LASSO'}" for t, m in zip(pt.test, pt.model)], fontsize=4.6); b.tick_params(axis="y", length=0); b.set_ylim(-.8, len(pt) - .2); b.set_xlabel("mean |FPR − 0.10| within site"); b.legend(frameon=False, fontsize=6, loc="lower right")
b.set_title(f"A  Burn-in closer to target in {(pt.burn < pt.src).sum()}/{len(pt)}", loc="left", color=TXT)
cc = pd.read_csv(os.path.join(H, "..", "v4", "results", "deploy_v4_cc_summary.csv")); cc = cc[(cc.N == 100) & (cc.pi == cc.pimax) & (cc.pi > 0)]
src = cc[cc.method == "SRC"].groupby("method")[["fpr", "sens"]].mean()  # training cut-off does not depend on the burn-in: one point
d.scatter(src.fpr, src.sens, s=26, color=TRN, edgecolor="white", lw=.6, label="training cut-off", zorder=3)
for meth, c, mk, lab in [("BURN", BLUE, "o", "burn-in, expected-FPR rule"), ("LAB", MUT, "D", "100 labelled local controls")]:
    x = cc[cc.method == meth].sort_values("pi")
    if meth == "LAB": x = x.groupby("method")[["fpr", "sens"]].mean()  # labelled controls do not depend on the burn-in case share
    d.scatter(x.fpr, x.sens, s=16, color=c, marker=mk, edgecolor="white", lw=.6, label=lab, zorder=3)
    if meth == "BURN":
        for (_, r), dy in zip(x.iterrows(), (14, -4, -22)): d.annotate(f"{r.pi:.0%} cases in burn-in", (r.fpr, r.sens), xytext=(32, dy), textcoords="offset points", fontsize=5, color=MUT, ha="left", va="center", arrowprops=dict(arrowstyle="-", color=GRID, lw=.5))
d.axvline(.10, color=MUT, lw=.8, ls="--"); d.set_xlabel("FPR (mean of 3 case–control cohorts)"); d.set_ylabel("sensitivity"); d.set_xlim(0, .32); d.set_ylim(0, .5)
d.legend(frameon=False, fontsize=5.5, loc="lower right"); d.set_title("B  The price: sensitivity", loc="left", color=TXT)
for e in ["pdf", "png"]: fig.savefig(os.path.join(O, f"figure3_site.{e}"), dpi=300, bbox_inches="tight", facecolor="white")
# ---- Supporting Figure S1
fig, (a, c) = plt.subplots(1, 2, figsize=(7.2, 2.9)); plt.subplots_adjust(wspace=.38)
Ns = np.arange(20, 801, 5)
for rule, col, lab in [("expected", BLUE, "E[FPR] ≤ 0.10 rule"), ("pac", VIO, "PAC rule (δ = 0.05)")]:
    q = [fpr_law(N, k_expected(N, .1) if rule == "expected" else k_pac(N, .1)) for N in Ns]
    ok = [x["feasible"] for x in q]; a.plot(Ns[ok], [x["P(FPR>0.15)"] for x, o in zip(q, ok) if o], color=col, lw=1.1, label=lab)
a.axvline(100, color=MUT, lw=.8, ls="--"); a.set_xscale("log"); a.set_xticks([25, 50, 100, 200, 400, 800]); a.set_xticklabels(["25", "50", "100", "200", "400", "800"])
a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); a.set_xlabel("burn-in size N (people)"); a.set_ylabel("P(realised FPR > 0.15)"); a.legend(frameon=False, fontsize=6); a.set_title("A  Exact risk of a high FPR", loc="left", color=TXT)
v = pd.read_csv(os.path.join(R, "verify_power_v5.csv")); v = v[v.model == "lasso"]
c.plot(v.n, v.mean_power_over025, color=BLUE, lw=2, marker="o", ms=4, label="observed FPR > 0.25"); c.plot(v.n, v.mean_power_over015, color=AQUA, lw=2, marker="o", ms=4, label="observed FPR > 0.15")
c.plot(v.n, v.max_false_alarm_le015, color=MUT, lw=1.2, ls="--", label="false alarm (FPR ≤ 0.15), max")
c.set_xscale("log"); c.set_xticks([25, 50, 100, 200]); c.set_xticklabels(["25", "50", "100", "200"]); c.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); c.set_ylim(0, 1.02)
c.set_xlabel("local healthy people checked (n)"); c.set_ylabel("probability the check flags it"); c.legend(frameon=False, fontsize=6, loc="lower right", bbox_to_anchor=(1, .1))
c.set_title("B  Verifying a stated FPR (LASSO atlas)", loc="left", color=TXT)
for e in ["pdf", "png"]: fig.savefig(os.path.join(O, f"figureS1_site_methods.{e}"), dpi=300, bbox_inches="tight", facecolor="white")
print(cc[cc.method.isin(["SRC", "BURN", "LAB"])][["method", "pi", "fpr", "sens"]].round(3).to_string(index=False))
