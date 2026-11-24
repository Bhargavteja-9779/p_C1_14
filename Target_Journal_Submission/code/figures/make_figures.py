"""Main figures (vector PDF + PNG). Revision 2: one story - specificity does not travel; local recalibration restores it."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(H, "..", "experiments")
R = os.path.join(E, "final", "results"); DV = os.path.join(E, "dev"); AD = os.path.join(E, "addendum_results")
OUT = os.path.join(H, "out"); os.makedirs(OUT, exist_ok=True)
COL = dict(vp="#2a78d6", vp_hc="#2a78d6", source="#eb6834", local_q="#1baf7a", contam="#6250d6", oracle="#8a8985")
LAB = dict(vp="Colonoscopy-feedback cut-off", vp_hc="Colonoscopy-feedback, strict", source="Fixed cut-off (published cohorts)",
           local_q="Local quantile", contam="Prevalence-bounded local cut-off", oracle="Oracle")
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
bx(-0.4, 7.2, 4.8, 2.3, "Development\n8 CRC cohorts\n11 other-condition\n+ 2 medication cohorts", INK2)
bx(5.4, 7.2, 5.0, 2.3, "Locked test, run once\n3 CRC + 13 other sites;\nMetaCardis for\npatient groups", COL["vp"])
bx(-0.4, 3.9, 4.8, 2.5, "Fixed classifiers\nLASSO, random forest\ncut-off: 90% specificity\non source controls", INK2)
bx(5.4, 3.9, 5.0, 2.5, "Realised specificity\nper site and per\npatient group\n(conditions, drugs)", COL["source"])
bx(-0.4, 0.2, 10.8, 2.8, "Simulated deployments, 4 cut-offs:\nfixed | local quantile | prevalence-bounded |\ncolonoscopy-feedback (results of\ntest-positives)", COL["vp"], fs=5.6)
arr(4.4, 8.35, 5.4, 8.35); arr(2.0, 7.2, 2.0, 6.4); arr(4.4, 5.15, 5.4, 5.15); arr(7.9, 3.9, 7.9, 3.0)
title_ax = ax
# 1B CRC audit
ax = fig.add_subplot(gs[0, 1]); panel(ax, "B")
au = pd.read_csv(os.path.join(AD, "posthoc_crc_audit_sites.csv"))
order = au[au.model == "lasso"].sort_values("fpr").site.tolist()
SHORT = {s_: s_.replace("_20", " 20").replace("_", " ").replace("ThomasAM", "Thomas").replace("HanniganGD", "Hannigan").replace("VogtmannE", "Vogtmann")
         .replace("WirbelJ", "Wirbel").replace("ZellerG", "Zeller").replace("FengQ", "Feng").replace("GuptaA", "Gupta").replace("YachidaS", "Yachida")
         .replace("YuJ", "Yu") for s_ in order}
for j, site in enumerate(order):
    for mdl, off, mk in [("lasso", -0.17, "o"), ("rf", 0.17, "s")]:
        r = au[(au.site == site) & (au.model == mdl)].iloc[0]; locked = r.role == "locked"
        c = INK if locked else INK2
        ax.plot([r.ci_lo, r.ci_hi], [j + off] * 2, color=c, lw=0.8, alpha=0.8)
        ax.scatter(r.fpr, j + off, s=14, marker=mk, facecolor=c if mdl == "lasso" else "white", edgecolor=c, lw=0.9, zorder=3)
ax.axvline(0.10, color=INK2, lw=0.8, ls="--")
ax.set_yticks(range(len(order)), [f"{SHORT[x]}{' (locked)' if x in ['YachidaS_2019','YuJ_2015','ThomasAM_2019_c'] else ''} n={au[(au.site == x)].n_controls.iloc[0]}" for x in order], fontsize=5.8)
ax.set_xlim(-0.02, 0.62); ax.set_xlabel("False-positive rate at the new site (exact 95% CI)")
ax.scatter([], [], marker="o", facecolor=INK2, edgecolor=INK2, s=14, label="LASSO"); ax.scatter([], [], marker="s", facecolor="white", edgecolor=INK2, s=14, label="Random forest")
ax.legend(loc="lower right", fontsize=5.8); grid(ax, "x")
title(ax, "False-positive rate at 11 new CRC sites (target 10%)")
# 1C fully adjusted effects
ax = fig.add_subplot(gs[1, 0]); panel(ax, "C")
dv = pd.read_csv(os.path.join(DV, "explore_v7b_fits.csv")); dv = dv[dv.spec == "adjusted"]
ma = pd.read_csv(os.path.join(AD, "posthoc_metacardis_drugadjusted.csv")); ma = ma[(ma.model == "lasso") & (ma.spec == "sex+country+drugs")]
wc = pd.read_csv(os.path.join(AD, "posthoc_within_crc_summary.csv")); wc = wc[wc.model == "lasso"]
NAME = {"QinN_2014": "Liver cirrhosis", "JieZ_2017": "Atherosclerotic CVD", "NagySzakalD_2017": "ME/CFS", "LiJ_2017": "Hypertension",
        "LoombaR_2017": "Fatty liver", "XieH_2016": "Asthma", "ZhuF_2020": "Schizophrenia"}
rows = []
for c in ["QinN_2014", "JieZ_2017", "NagySzakalD_2017", "LiJ_2017", "LoombaR_2017", "XieH_2016", "ZhuF_2020"]:
    r = dv[dv.cohort == c].iloc[0]; rows.append((NAME[c], r.beta_dis, r.ci_lo, r.ci_hi, "dev"))
for cond, lab in [("HF", "Heart failure"), ("T2D", "Type 2 diabetes"), ("CAD", "Coronary artery disease"), ("IGT", "Prediabetes")]:
    r = ma[ma.condition == cond].iloc[0]; rows.append((lab + " (MetaCardis)", r.beta, r.lo, r.hi, "locked"))
r = wc[wc.group == "controls"].iloc[0]; rows.append(("Comorbid controls in CRC cohorts", r.beta_score, r.lo, r.hi, "crc"))
for i, (lab, b_, lo, hi, kind) in enumerate(rows[::-1]):
    c = INK if kind != "dev" else INK2; mk = {"dev": "o", "locked": "o", "crc": "D"}[kind]
    ax.plot([lo, hi], [i, i], color=c, lw=0.9)
    ax.scatter(b_, i, s=15, marker=mk, facecolor="white" if kind == "dev" else c, edgecolor=c, lw=1.0, zorder=3)
ax.axvline(0, color=INK2, lw=0.7); ax.set_yticks(range(len(rows)), [r_[0] for r_ in rows[::-1]], fontsize=6)
ax.axhline(len(rows) - 7.5, color=GRID, lw=0.8)
ax.text(0.02, len(rows) - 7.2, "development (open)", transform=ax.get_yaxis_transform(), ha="left", fontsize=5.6, color=INK2)
ax.text(0.98, 3.6, "locked / CRC cohorts (filled)", transform=ax.get_yaxis_transform(), ha="right", fontsize=5.6, color=INK)
ax.set_xlabel("CRC-test score vs same-cohort controls (logit, 95% CI)"); grid(ax, "x")
title(ax, "Which patients are over-flagged (adjusted where recorded)")
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
                              ("Other enriched taxa", "#b9b8b2")]):
    v = np.array([b[j + 1] for b in bars])
    ax.barh(yy, v, 0.6, left=np.where(v >= 0, pos, neg), color=c, edgecolor="white", lw=0.8, label=lab)
    pos += np.clip(v, 0, None); neg += np.clip(v, None, 0)
ax.axvline(0, color=INK2, lw=0.6); ax.set_yticks(yy, [b[0] for b in bars], fontsize=6)
ax.set_xlabel("Contribution to CRC-score gap (logit)"); title(ax, "Species contributions to the score gap"); grid(ax, "x")
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
sub = gs[0, 0].subgridspec(2, 1, height_ratios=[2.2, 1], hspace=0.12)
ax = fig.add_subplot(sub[0]); panel(ax, "A")
cd = pd.read_csv(os.path.join(AD, "posthoc_crc_deploy.csv.gz")); traj(ax, cd, 12, 0.36); ax.set_xlabel(""); ax.tick_params(labelbottom=False)
title(ax, "11 CRC cohorts, 1% prevalence (8 development, 3 locked)")
ax.legend(loc="upper right", bbox_to_anchor=(1, 0.95), fontsize=5.6, handlelength=2.4); ax.text(1.4, 0.335, "burn-in", fontsize=6, color=INK2)
ax2 = fig.add_subplot(sub[1], sharex=ax)
for mth in ["source", "contam", "vp", "oracle"]:
    g_ = cd[cd.method == mth].groupby("month").sens.mean()
    ax2.plot(g_.index, g_.values, color=COL[mth], ls=LS.get(mth, (0, (1, 1))), lw=1.6 if mth == "vp" else 1.1)
ax2.set_ylim(0.3, 0.75); ax2.set_ylabel("Sensitivity"); ax2.set_xlabel("Month since deployment"); grid(ax2)
ax2.text(12.3, cd[cd.method == "oracle"].sens.mean(), "oracle", fontsize=5.5, color=INK2, va="center")
ax = fig.add_subplot(gs[0, 1]); panel(ax, "B")
traj(ax, S[(S.setting == "drift") & (S.pi == 0.01)], 18, 0.5)
ax.axvspan(6.5, 18.5, color=GRID, alpha=0.35, lw=0); ax.text(7, 0.46, "all scores shift +0.5 logit", fontsize=6, color=INK2)
title(ax, "Upward drift: the restart recovers fastest")
ax = fig.add_subplot(gs[1, 0]); panel(ax, "C")
Cg = pd.read_csv(os.path.join(R, "partC_groupcal.csv.gz")); Cg = Cg[(Cg.month >= 7) & (Cg.model == "lasso")]
grp = ["control", "IGT", "CAD", "T2D", "HF"]; gl = ["No\ncondition", "Pre-\ndiabetes", "Coronary\ndisease", "Type 2\ndiabetes", "Heart\nfailure"]
x = np.arange(len(grp))
for mth, c, lab, off in [("source", COL["source"], "Fixed cut-off", -0.27), ("pooled", "#b9b8b2", "Recalibrated, everyone together", 0),
                          ("group", COL["vp"], "Recalibrated within groups", 0.27)]:
    ax.bar(x + off, [Cg[(Cg.method == mth) & (Cg.group == g)].fpr.mean() for g in grp], 0.25, color=c, edgecolor="white", lw=0.8, label=lab)
ax.axhline(0.10, color=INK2, lw=0.8, ls=(0, (1, 1))); ax.set_xticks(x, gl, fontsize=6.2); ax.set_ylabel("True false-positive rate (months 7-18)")
title(ax, "CRC test at MetaCardis, by condition"); ax.legend(fontsize=5.8, loc="upper left"); grid(ax)
ax = fig.add_subplot(gs[1, 1]); panel(ax, "D")
St = pd.read_csv(os.path.join(AD, "posthoc_stream_v2.csv.gz")); St = St[St.month >= 3]; St["over"] = St.fpr_future > 0.12
St["kind"] = St.tag.str.split("|").str[0]
mets = ["source", "local_q", "contam", "contam_hc", "vp", "vp_hc"]
names = ["Fixed", "Local\nquantile", "Prev.-\nbounded", "Prev.-b.\nstrict", "Colonoscopy\nfeedback", "Feedback\nstrict"]
xx = np.arange(len(mets)); w = 0.38
for kind, off, lab, alpha_ in [("random", -w / 2, "Random order (3 large sites)", 1.0), ("country", w / 2, "MetaCardis, country by country", 0.45)]:
    q = St[St.kind == kind]; ov = [q[q.method == m].over.mean() for m in mets]
    bb = ax.bar(xx + off, ov, w, color=[COL["vp"] if m.startswith("vp") else COL[m.replace("_hc", "")] for m in mets], alpha=alpha_, edgecolor="white", lw=0.6, label=lab)
    for i, m in enumerate(mets):
        if m.endswith("_hc"): bb[i].set_hatch("////")
ax.set_xticks(xx, names, fontsize=5.0); ax.set_ylim(0, 0.45); ax.set_ylabel("Months with false-positive rate > 12%")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc="#8a8985", label="Random order, 3 cohorts / 4 tests (left bar)"), Patch(fc="#8a8985", alpha=0.45, label="MetaCardis, country by country (right bar)")],
          fontsize=5.6, loc="upper right"); grid(ax)
title(ax, "Real samples, no resampling (post hoc)")
fig.savefig(os.path.join(OUT, "Figure2.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(OUT, "Figure2.png"), dpi=200, bbox_inches="tight")
print("ok")
