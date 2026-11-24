"""Main figures (vector PDF + PNG preview). Run after the locked analysis."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(H, "..", "experiments")
R = os.path.join(E, "final", "results"); DV = os.path.join(E, "dev"); OUT = os.path.join(H, "out"); os.makedirs(OUT, exist_ok=True)
# palette (validated: blue, orange, aqua, violet; neutral grey for reference lines)
COL = dict(vp="#2a78d6", source="#eb6834", local_q="#1baf7a", contam="#6250d6", oracle="#8a8985")
LAB = dict(vp="Verified-positive recalibration (ours)", source="Source cut-off (status quo)", local_q="Local quantile",
           contam="Prevalence-bounded quantile", oracle="Oracle")
MK = dict(vp="o", source="s", local_q="^", contam="D", oracle="")
LS = dict(vp="-", source="--", local_q=":", contam="-.", oracle=(0, (1, 1)))
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "legend.frameon": False,
                     "pdf.fonttype": 42, "svg.fonttype": "none"})
def panel(ax, s): ax.text(-0.14, 1.06, s, transform=ax.transAxes, fontsize=10, fontweight="bold", color=INK, va="bottom")
def grid(ax, axis="y"): ax.grid(axis=axis, color=GRID, lw=0.5); ax.set_axisbelow(True)
DIS = {"CRC": "Colorectal cancer", "IBD": "IBD", "T2D": "Type 2 diabetes", "adenoma": "Adenoma"}

S = pd.read_csv(os.path.join(R, "sequential.csv.gz"))
P = S[S.setting == "primary"]

# ---------------- Figure 1: the problem and its biology ----------------
fig = plt.figure(figsize=(7.4, 7.0)); gs = fig.add_gridspec(2, 2, hspace=0.62, wspace=0.95, height_ratios=[1, 1.0])
# 1A realised FPR of the source cut-off per site
ax = fig.add_subplot(gs[0, 0]); panel(ax, "A")
src = P[(P.method == "source") & (P.month == 1)].groupby(["disease", "site", "model"]).fpr.first().reset_index()
order = ["CRC", "IBD", "T2D", "adenoma"]; ypos = 0; yt, yl = [], []
for d in order:
    q = src[src.disease == d]
    for mdl, mk in [("lasso", "o"), ("rf", "s")]:
        v = q[q.model == mdl].fpr.values
        ax.scatter(v, np.full(len(v), ypos) + (0.12 if mdl == "rf" else -0.12), s=16, marker=mk, facecolor=COL["source"] if mdl == "lasso" else "white",
                   edgecolor=COL["source"], lw=0.9, zorder=3, label={"lasso": "LASSO", "rf": "Random forest"}[mdl] if d == "CRC" else None)
    yt.append(ypos); yl.append(f"{DIS[d]}\n({q.site.nunique()} sites)"); ypos += 1
ax.axvline(0.10, color=INK2, lw=0.8, ls="--"); ax.text(0.108, 3.45, "intended 10%", color=INK2, fontsize=6.5)
ax.set_yticks(yt, yl); ax.invert_yaxis(); ax.set_xlabel("Realised false-positive rate at the new site"); ax.set_xlim(-0.02, 0.62)
ax.set_title("Cut-offs set on source cohorts miss their target", loc="left", fontsize=8, color=INK); grid(ax, "x")
ax.legend(loc="lower right", fontsize=6.5, handletextpad=0.2)
# 1B forest plot of adjusted score difference (condition vs own controls)
ax = fig.add_subplot(gs[0, 1]); panel(ax, "B")
dev = pd.read_csv(os.path.join(DV, "explore_v7b_fits.csv")); dev = dev[dev.spec == "adjusted"].assign(set="Development")
lk = pd.read_csv(os.path.join(R, "partB_adjusted_holm.csv")); lk = lk[lk.model == "lasso"].rename(columns={"beta": "beta_dis", "lo": "ci_lo", "hi": "ci_hi"}).assign(set="Locked")
NAME = {"JieZ_2017": "Atherosclerotic CVD", "QinN_2014": "Liver cirrhosis", "LiJ_2017": "Hypertension", "LoombaR_2017": "Fatty liver",
        "NagySzakalD_2017": "ME/CFS", "XieH_2016": "Asthma", "ZhuF_2020": "Schizophrenia"}
dev["label"] = dev.cohort.map(NAME)
lk["label"] = lk.condition.map({"HF": "Heart failure", "T2D": "Type 2 diabetes", "CAD": "Coronary artery disease", "IGT": "Prediabetes (IGT)",
                                "IBD": "IBD"}) + " · " + lk.cohort.map({"MetaCardis_2020_a": "MetaCardis", "QinJ_2012": "Qin 2012", "KarlssonFH_2013": "Karlsson 2013",
                         "NielsenHB_2014": "Nielsen 2014", "HallAB_2017": "Hall 2017", "IjazUZ_2017": "Ijaz 2017", "HMP_2019_ibdmdb": "HMP2 IBDMDB"})
F = pd.concat([dev.sort_values("beta_dis"), lk.sort_values("beta_dis")])
for i, (_, r) in enumerate(F.iterrows()):
    filled = r["set"] == "Locked"; c = COL["vp"] if filled else INK2
    ax.plot([r.ci_lo, r.ci_hi], [i, i], color=c, lw=1.0)
    ax.scatter(r.beta_dis, i, s=18, marker="o", facecolor=c if filled else "white", edgecolor=c, lw=1.0, zorder=3)
ax.axvline(0, color=INK2, lw=0.7); ax.set_yticks(range(len(F)), F.label, fontsize=6.2)
ax.axhline(len(dev) - 0.5, color=GRID, lw=0.8)
ax.text(1.02, (len(dev) - 1) / 2, "Development", rotation=270, transform=ax.get_yaxis_transform(), va="center", fontsize=6.5, color=INK2)
ax.text(1.02, len(dev) + (len(lk) - 1) / 2, "Locked test", rotation=270, transform=ax.get_yaxis_transform(), va="center", fontsize=6.5, color=COL["vp"])
ax.set_xlabel("CRC-test score, condition − own controls\n(logit; adjusted for age, BMI, sex where recorded; 95% CI)")
ax.set_title("Chronic disease raises the cancer score", loc="left", fontsize=8, color=INK); grid(ax, "x")
# 1C mechanism: two routes
ax = fig.add_subplot(gs[1, 0]); panel(ax, "C")
A = pd.read_csv(os.path.join(DV, "explore_v9b_axes.csv"), index_col=0)
cond = ["QinN_2014", "JieZ_2017", "LoombaR_2017", "LiJ_2017", "NagySzakalD_2017", "XieH_2016", "ZhuF_2020"]
cats = [("oral", "Oral-origin taxa enriched", COL["source"]), ("commensal_depletion", "Commensal fermenters depleted", COL["vp"]),
        ("other_enriched", "Other taxa", "#b9b8b2")]
cond = cond[::-1]; yy = np.arange(len(cond)); h = 0.62
pos_base = np.zeros(len(cond)); neg_base = np.zeros(len(cond))
for k, lab, c in cats:
    v = A.loc[k, cond].values; b0 = np.where(v >= 0, pos_base, neg_base)
    ax.barh(yy, v, h, left=b0, color=c, edgecolor="white", linewidth=1.0, label=lab)
    pos_base += np.clip(v, 0, None); neg_base += np.clip(v, None, 0)
ax.scatter(A.loc["total", cond].values, yy, marker="|", s=120, color=INK, lw=1.6, zorder=4, label="Net score gap")
ax.axvline(0, color=INK2, lw=0.6); ax.set_yticks(yy, [NAME[c] for c in cond], fontsize=6.5)
ax.set_xlabel("Contribution to CRC-score gap vs own controls (logit)")
ax.set_title("Two routes to a false alarm (development)", loc="left", fontsize=8, color=INK)
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.2), fontsize=6, ncol=2, handlelength=1.2, columnspacing=0.8); grid(ax, "x")
# 1D medications (addendum A1, MetaCardis; exploratory metformin within T2D)
ax = fig.add_subplot(gs[1, 1]); panel(ax, "D")
AD = os.path.join(E, "addendum_results")
rg = pd.read_csv(os.path.join(AD, "confirm_regression.csv")); mt = pd.read_csv(os.path.join(AD, "metformin_within_T2D.csv"))
items = []
def g_(model, outcome, term):
    r = rg[(rg.model == model) & (rg.outcome == outcome) & (rg.term == term)].iloc[0]; return r.beta, r.lo, r.hi
items.append(("PPI → total score (LASSO) H5", *g_("lasso", "score", "ppi"), "pre"))
items.append(("PPI → total score (RF)", *g_("rf", "score", "ppi"), "pre"))
items.append(("PPI → oral-taxa component H6", *g_("lasso", "oral", "ppi"), "pre"))
items.append(("Metformin → total score (LASSO)", *g_("lasso", "score", "metformin"), "expl"))
for c, lab in [("MetaCardis_2020_a", "MetaCardis"), ("LiJ_2014", "Li 2014"), ("QinJ_2012", "Qin 2012"), ("KarlssonFH_2013", "Karlsson 2013")]:
    r = mt[(mt.model == "lasso") & (mt.cohort == c)]
    if len(r): r = r.iloc[0]; items.append((f"Metformin in T2D · {lab} (n={r.n_met}/{r.n_no})", r.beta, r.lo, r.hi, "expl"))
for i, (lab, b, lo, hi, kind) in enumerate(items[::-1]):
    c = COL["vp"] if kind == "pre" else COL["contam"]
    ax.plot([lo, hi], [i, i], color=c, lw=1.0)
    ax.scatter(b, i, s=18, marker="o" if kind == "pre" else "D", facecolor=c if kind == "pre" else "white", edgecolor=c, lw=1.0, zorder=3)
ax.axvline(0, color=INK2, lw=0.7); ax.set_yticks(range(len(items)), [it[0] for it in items[::-1]], fontsize=6)
ax.set_xlabel("Adjusted effect on CRC-test score (logit, 95% CI)")
ax.set_title("Medications (filled: pre-specified; open: exploratory)", loc="left", fontsize=8, color=INK); grid(ax, "x")
fig.savefig(os.path.join(OUT, "Figure1.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(OUT, "Figure1.png"), dpi=200, bbox_inches="tight")

# ---------------- Figure 2: the fix ----------------
fig = plt.figure(figsize=(7.2, 6.2)); gs = fig.add_gridspec(2, 2, hspace=0.5, wspace=0.32)
def traj(ax, q, months, title, ymax):
    for mth in ["source", "local_q", "contam", "vp"]:
        g = q[q.method == mth].groupby("month").fpr
        mu, lo, hi = g.mean(), g.quantile(0.1), g.quantile(0.9)
        if mth == "vp": ax.fill_between(mu.index, lo, hi, color=COL[mth], alpha=0.15, lw=0)
        ax.plot(mu.index, mu.values, color=COL[mth], ls=LS[mth], lw=2 if mth == "vp" else 1.4, marker=MK[mth], ms=4,
                markevery=3, label=LAB[mth])
    ax.axhline(0.10, color=INK2, lw=0.8, ls=(0, (1, 1))); ax.axhline(0.12, color=GRID, lw=0.8)
    ax.text(months + 0.3, 0.10, "target", va="center", fontsize=6.5, color=INK2)
    ax.set_xlim(0.5, months + 0.5); ax.set_ylim(0, ymax); ax.set_xlabel("Month since deployment")
    ax.set_ylabel("True false-positive rate"); ax.set_title(title, loc="left", fontsize=8, color=INK); grid(ax)
ax = fig.add_subplot(gs[0, 0]); panel(ax, "A")
traj(ax, P[P.pi == 0.01], 12, "Locked sites, 1% prevalence (16 sites × 2 models)", 0.36)
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.9), fontsize=6.2, handlelength=2.6)
ax.annotate("burn-in month", xy=(1.1, P[(P.pi == 0.01) & (P.method == "vp") & (P.month == 1)].fpr.mean()), xytext=(1.6, 0.345),
            fontsize=6.5, color=INK2, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
ax = fig.add_subplot(gs[0, 1]); panel(ax, "B")
Dd = S[(S.setting == "drift") & (S.pi == 0.01)]
traj(ax, Dd, 18, "Score drift of +0.5 logit at month 7 (drift alarm)", 0.5)
ax.axvspan(6.5, 18.5, color=GRID, alpha=0.35, lw=0); ax.text(7, 0.46, "after drift", fontsize=6.5, color=INK2)
# 2C group-conditional at MetaCardis
ax = fig.add_subplot(gs[1, 0]); panel(ax, "C")
C = pd.read_csv(os.path.join(R, "partC_groupcal.csv.gz")); C = C[(C.month >= 7) & (C.model == "lasso")]
grp = ["control", "IGT", "CAD", "T2D", "HF"]; gl = ["None", "Pre-\ndiabetes", "Coronary\nart. dis.", "Type 2\ndiabetes", "Heart\nfailure"]
x = np.arange(len(grp))
for j, (mth, c, lab, off) in enumerate([("source", COL["source"], "Source cut-off", -0.27), ("pooled", "#b9b8b2", "Recalibrated, pooled", 0),
                                         ("group", COL["vp"], "Recalibrated per group (ours)", 0.27)]):
    v = [C[(C.method == mth) & (C.group == g)].fpr.mean() for g in grp]
    ax.bar(x + off, v, 0.25, color=c, edgecolor="white", linewidth=1.0, label=lab)
ax.axhline(0.10, color=INK2, lw=0.8, ls=(0, (1, 1)))
ax.set_xticks(x, gl, fontsize=6.5); ax.set_ylabel("True false-positive rate (months 7–18)")
ax.set_title("One site, many patients: MetaCardis (locked)", loc="left", fontsize=8, color=INK); ax.legend(fontsize=6.2, loc="upper left"); grid(ax)
# 2D harms per 1,000
ax = fig.add_subplot(gs[1, 1]); panel(ax, "D")
Q = P[P.pi == 0.01].copy(); Q["fp"] = 1000 * (1 - Q.pi) * Q.fpr; Q["miss"] = 1000 * Q.pi * (1 - Q.sens)
hz = Q.groupby(["disease", "method"])[["fp", "miss"]].mean()
dd = ["CRC", "IBD", "T2D"]; x = np.arange(len(dd))
for mth, off in [("source", -0.18), ("vp", 0.18)]:
    v = [hz.loc[(d, mth), "fp"] for d in dd]
    ax.bar(x + off, v, 0.34, color=COL[mth], edgecolor="white", linewidth=1.0, label=LAB[mth])
    for xi, vi, d in zip(x + off, v, dd):
        ax.text(xi, vi + 4, f"{vi:.0f}", ha="center", fontsize=6.5, color=INK)
ax.set_xticks(x, [DIS[d] for d in dd]); ax.set_ylim(0, 330)
ax.set_ylabel("False positives per 1,000 screened\n(12 months, 1% prevalence)"); ax.legend(fontsize=6.2, loc="upper left", bbox_to_anchor=(0, 1.02))
ax.set_xticks(x, [f"{DIS[d]}\nmissed/1,000: {hz.loc[(d, 'source'), 'miss']:.1f} vs {hz.loc[(d, 'vp'), 'miss']:.1f}" for d in dd], fontsize=6.5)
ax.set_title("Fewer unnecessary referrals", loc="left", fontsize=8, color=INK); grid(ax)
fig.savefig(os.path.join(OUT, "Figure2.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(OUT, "Figure2.png"), dpi=200, bbox_inches="tight")
print("ok")
