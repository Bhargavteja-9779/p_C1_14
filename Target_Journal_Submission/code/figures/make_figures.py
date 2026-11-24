"""Main figures (vector PDF + PNG). Revision 2: one story - specificity does not travel; local recalibration restores it."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(H, "..", "experiments")
R = os.path.join(E, "final", "results"); DV = os.path.join(E, "dev"); AD = os.path.join(E, "addendum_results")
OUT = os.path.join(H, "out"); os.makedirs(OUT, exist_ok=True)
COL = dict(vp="#2a78d6", vp_hc="#2a78d6", source="#eb6834", local_q="#1baf7a", contam="#6250d6", oracle="#8a8985")
LAB = dict(vp="Verified-positive (ours)", vp_hc="Verified-positive, high-confidence", source="Source cut-off (status quo)",
           local_q="Local quantile", contam="Prevalence-bounded quantile", oracle="Oracle")
MK = dict(vp="o", vp_hc="o", source="s", local_q="^", contam="D")
LS = dict(vp="-", vp_hc="--", source="--", local_q=":", contam="-.")
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e4e3df", "#f4f3ef"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.2, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.6, "legend.frameon": False, "pdf.fonttype": 42})
def panel(ax, s, x=-0.12): ax.text(x, 1.05, s, transform=ax.transAxes, fontsize=10, fontweight="bold", color=INK, va="bottom")
def grid(ax, axis="y"): ax.grid(axis=axis, color=GRID, lw=0.5); ax.set_axisbelow(True)
def title(ax, t): ax.set_title(t, loc="left", fontsize=7.8, color=INK)
DIS = {"CRC": "Colorectal cancer", "IBD": "IBD", "T2D": "Type 2 diabetes", "adenoma": "Adenoma*"}
S = pd.read_csv(os.path.join(R, "sequential.csv.gz")); P = S[S.setting == "primary"]

# =============== Figure 1 ===============
fig = plt.figure(figsize=(7.4, 7.6)); gs = fig.add_gridspec(2, 2, hspace=0.5, wspace=0.75, height_ratios=[1, 1.1])
ax = fig.add_subplot(gs[0, 0]); panel(ax, "A", -0.05); ax.axis("off"); ax.set_xlim(-0.6, 10.6); ax.set_ylim(0, 10.2)
def bx(x, y, w, h, txt, ec, fs=5.7):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.25", fc=BG, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color=INK)
def arr(x0, y0, x1, y1): ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=8, color=INK2, lw=0.9))
bx(-0.4, 7.2, 4.8, 2.3, "Development\n8 CRC cohorts\n13 other-condition\ncohorts", INK2)
bx(5.4, 7.2, 5.0, 2.3, "Locked test, run once\n16 held-out sites\n11 cohorts, 4 diseases", COL["vp"])
bx(-0.4, 3.9, 4.8, 2.5, "Fixed classifiers\nLASSO, random forest\ncut-off: 90% specificity\non source controls", INK2)
bx(5.4, 3.9, 5.0, 2.5, "Realised specificity\nper site and per\npatient group\n(conditions, drugs)", COL["source"])
bx(-0.4, 0.2, 10.8, 2.8, "Simulated deployments, 4 cut-off rules:\nsource | local quantile | prevalence-bounded |\nverified-positive (colonoscopy results\nof test-positives)", COL["vp"], fs=5.6)
arr(4.4, 8.35, 5.4, 8.35); arr(2.0, 7.2, 2.0, 6.4); arr(4.4, 5.15, 5.4, 5.15); arr(7.9, 3.9, 7.9, 3.0)
ax.text(5.0, 9.9, "Protocol frozen before locked analysis; medication addendum frozen before its analysis", ha="center", fontsize=5.6, color=INK2)
title_ax = ax
# 1B
ax = fig.add_subplot(gs[0, 1]); panel(ax, "B")
src = P[(P.method == "source") & (P.month == 1)].groupby(["disease", "site", "model"]).fpr.first().reset_index()
rng = np.random.default_rng(3)
for i, d in enumerate(["CRC", "IBD", "T2D", "adenoma"]):
    q = src[src.disease == d]
    for mdl, mk, off in [("lasso", "o", -0.15), ("rf", "s", 0.15)]:
        v = q[q.model == mdl].fpr.values; jit = rng.uniform(-0.07, 0.07, len(v))
        ax.scatter(v, np.full(len(v), i) + off + jit, s=15, marker=mk, facecolor=COL["source"] if mdl == "lasso" else "white",
                   edgecolor=COL["source"], lw=0.9, zorder=3, label={"lasso": "LASSO", "rf": "Random forest"}[mdl] if i == 0 else None)
ax.axvline(0.10, color=INK2, lw=0.8, ls="--"); ax.text(0.11, -0.6, "target 10%", color=INK2, fontsize=6)
ax.set_yticks(range(4), [f"{DIS[d]}\n({src[src.disease == d].site.nunique()} sites)" for d in ["CRC", "IBD", "T2D", "adenoma"]])
ax.set_ylim(3.6, -0.8); ax.set_xlim(-0.02, 0.8); ax.set_xlabel("Realised false-positive rate at the held-out site")
title(ax, "Specificity does not travel across sites"); grid(ax, "x"); ax.legend(loc="center right", fontsize=6)
ax.text(0.79, 3.5, "*controls partly shared\nwith development", ha="right", fontsize=5.5, color=INK2)
# 1C
ax = fig.add_subplot(gs[1, 0]); panel(ax, "C")
dv = pd.read_csv(os.path.join(DV, "explore_v7b_fits.csv")); dv = dv[dv.spec == "adjusted"]
ma = pd.read_csv(os.path.join(AD, "posthoc_metacardis_drugadjusted.csv")); ma = ma[ma.model == "lasso"]
wc = pd.read_csv(os.path.join(AD, "posthoc_within_crc_summary.csv")); wc = wc[wc.model == "lasso"]
NAME = {"QinN_2014": "Liver cirrhosis", "JieZ_2017": "Atherosclerotic CVD", "LiJ_2017": "Hypertension", "LoombaR_2017": "Fatty liver"}
rows = []
for c in ["QinN_2014", "JieZ_2017", "LiJ_2017", "LoombaR_2017"]:
    r = dv[dv.cohort == c].iloc[0]; rows.append((f"{NAME[c]} (development)", r.beta_dis, r.ci_lo, r.ci_hi, "dev"))
for cond, lab in [("HF", "Heart failure"), ("T2D", "Type 2 diabetes")]:
    for spec, sl in [("sex", "sex"), ("sex+country", "+ country"), ("sex+country+drugs", "+ country + drugs")]:
        r = ma[(ma.condition == cond) & (ma.spec == spec)].iloc[0]; rows.append((f"{lab} (locked): {sl}", r.beta, r.lo, r.hi, "locked"))
r = wc[wc.group == "controls"].iloc[0]; rows.append(("Comorbid vs healthy controls,\n3 CRC cohorts", r.beta_score, r.lo, r.hi, "crc"))
cols = dict(dev=INK2, locked=COL["vp"], crc=COL["source"])
for i, (lab, b, lo, hi, kind) in enumerate(rows[::-1]):
    ax.plot([lo, hi], [i, i], color=cols[kind], lw=1.0)
    ax.scatter(b, i, s=16, facecolor=cols[kind] if kind != "dev" else "white", edgecolor=cols[kind], lw=1.0, zorder=3)
ax.axvline(0, color=INK2, lw=0.7); ax.set_yticks(range(len(rows)), [r[0] for r in rows[::-1]], fontsize=5.9)
ax.set_xlabel("CRC-test score vs same-cohort controls\n(logit, LASSO, 95% CI)")
title(ax, "Who is over-flagged: severe disease, drugs"); grid(ax, "x")
# 1D
ax = fig.add_subplot(gs[1, 1]); panel(ax, "D")
A = pd.read_csv(os.path.join(DV, "explore_v9b_axes.csv"), index_col=0)
L = pd.read_csv(os.path.join(AD, "posthoc_metacardis_decomposition.csv")).set_index("condition")
mk_ = "metformin users vs non-users (T2D)"
bars = [("Liver cirrhosis (dev)", A.loc["oral", "QinN_2014"], A.loc["commensal_depletion", "QinN_2014"], A.loc["other_enriched", "QinN_2014"]),
        ("Atherosclerotic CVD (dev)", A.loc["oral", "JieZ_2017"], A.loc["commensal_depletion", "JieZ_2017"], A.loc["other_enriched", "JieZ_2017"]),
        ("Heart failure (locked)", L.loc["HF", "oral"], L.loc["HF", "depletion"], L.loc["HF", "other"]),
        ("Type 2 diabetes (locked)", L.loc["T2D", "oral"], L.loc["T2D", "depletion"], L.loc["T2D", "other"]),
        ("Metformin vs none in T2D\n(locked, exploratory)", L.loc[mk_, "oral"], L.loc[mk_, "depletion"], L.loc[mk_, "other"])][::-1]
yy = np.arange(len(bars)); pos = np.zeros(len(bars)); neg = np.zeros(len(bars))
for j, (lab, c) in enumerate([("Oral-origin taxa enriched", COL["source"]), ("Commensal fermenters depleted", COL["vp"]),
                              ("Other taxa (e.g. Enterobacterales)", "#b9b8b2")]):
    v = np.array([b[j + 1] for b in bars])
    ax.barh(yy, v, 0.6, left=np.where(v >= 0, pos, neg), color=c, edgecolor="white", lw=0.8, label=lab)
    pos += np.clip(v, 0, None); neg += np.clip(v, None, 0)
ax.axvline(0, color=INK2, lw=0.6); ax.set_yticks(yy, [b[0] for b in bars], fontsize=6)
ax.set_xlabel("Contribution to CRC-score gap (logit)"); title(ax, "Two routes: oral taxa vs drug-linked shifts"); grid(ax, "x")
ax.legend(loc="upper center", bbox_to_anchor=(0.35, -0.2), fontsize=5.8, ncol=1, handlelength=1.1)
fig.savefig(os.path.join(OUT, "Figure1.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(OUT, "Figure1.png"), dpi=200, bbox_inches="tight")

# =============== Figure 2 ===============
fig = plt.figure(figsize=(7.4, 6.4)); gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.42)
def traj(ax, q, months, ymax, methods=("source", "local_q", "contam", "vp")):
    for mth in methods:
        g = q[q.method == mth].groupby("month").fpr; mu = g.mean()
        if mth == "vp": ax.fill_between(mu.index, g.quantile(0.1), g.quantile(0.9), color=COL[mth], alpha=0.14, lw=0)
        ax.plot(mu.index, mu.values, color=COL[mth], ls=LS[mth], lw=1.9 if mth == "vp" else 1.3, marker=MK[mth], ms=3.5, markevery=3, label=LAB[mth])
    ax.axhline(0.10, color=INK2, lw=0.8, ls=(0, (1, 1))); ax.set_xlim(0.5, months + 0.5); ax.set_ylim(0, ymax)
    ax.set_xlabel("Month since deployment"); ax.set_ylabel("True false-positive rate"); grid(ax)
ax = fig.add_subplot(gs[0, 0]); panel(ax, "A")
q = P[P.pi == 0.01]; traj(ax, q, 12, 0.36)
title(ax, f"Stable sites ({q.site.nunique()} CRC/IBD/T2D sites, 1% prevalence)")
ax.legend(loc="upper right", bbox_to_anchor=(1, 0.93), fontsize=5.8, handlelength=2.4); ax.text(1.4, 0.335, "burn-in", fontsize=6, color=INK2)
ax = fig.add_subplot(gs[0, 1]); panel(ax, "B")
traj(ax, S[(S.setting == "drift") & (S.pi == 0.01)], 18, 0.5)
ax.axvspan(6.5, 18.5, color=GRID, alpha=0.35, lw=0); ax.text(7, 0.46, "all scores shift +0.5 logit", fontsize=6, color=INK2)
title(ax, "Upward drift: only the drift alarm recovers")
ax = fig.add_subplot(gs[1, 0]); panel(ax, "C")
Cg = pd.read_csv(os.path.join(R, "partC_groupcal.csv.gz")); Cg = Cg[(Cg.month >= 7) & (Cg.model == "lasso")]
grp = ["control", "IGT", "CAD", "T2D", "HF"]; gl = ["No\ncondition", "Pre-\ndiabetes", "Coronary\ndisease", "Type 2\ndiabetes", "Heart\nfailure"]
x = np.arange(len(grp))
for mth, c, lab, off in [("source", COL["source"], "Source cut-off", -0.27), ("pooled", "#b9b8b2", "Recalibrated, pooled", 0),
                          ("group", COL["vp"], "Recalibrated per group", 0.27)]:
    ax.bar(x + off, [Cg[(Cg.method == mth) & (Cg.group == g)].fpr.mean() for g in grp], 0.25, color=c, edgecolor="white", lw=0.8, label=lab)
ax.axhline(0.10, color=INK2, lw=0.8, ls=(0, (1, 1))); ax.set_xticks(x, gl, fontsize=6.2); ax.set_ylabel("True false-positive rate (months 7-18)")
title(ax, "Per-group recalibration at one locked site"); ax.legend(fontsize=5.8, loc="upper left"); grid(ax)
ax = fig.add_subplot(gs[1, 1]); panel(ax, "D")
St = pd.read_csv(os.path.join(AD, "posthoc_stream_noreplacement.csv.gz")); St = St[St.month >= 3]; St["over"] = St.fpr_future > 0.12
mets = ["source", "local_q", "contam", "vp", "vp_hc"]; names = ["Source", "Local\nquantile", "Prevalence-\nbounded", "Verified-\npositive", "Verified-pos.\nhigh-conf."]
fpr = [St[St.method == m].fpr_future.mean() for m in mets]; ov = [St[St.method == m].over.mean() for m in mets]
xx = np.arange(len(mets))
bb = ax.bar(xx, ov, 0.6, color=[COL[m] for m in mets], edgecolor="white", lw=0.8)
bb[-1].set_facecolor("white"); bb[-1].set_edgecolor(COL["vp_hc"]); bb[-1].set_hatch("////"); bb[-1].set_linewidth(1.0)
for xi, o, f in zip(xx, ov, fpr): ax.text(xi, o + 0.008, f"{o:.0%}\nFPR {f:.3f}", ha="center", fontsize=5.8, color=INK)
ax.set_xticks(xx, names, fontsize=5.9); ax.set_ylim(0, 0.33); ax.set_ylabel("Share of months with FPR > 12%\n(on not-yet-seen controls)")
title(ax, "Real samples, no resampling (2 large locked sites)"); grid(ax)
fig.savefig(os.path.join(OUT, "Figure2.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(OUT, "Figure2.png"), dpi=200, bbox_inches="tight")
print("ok")
