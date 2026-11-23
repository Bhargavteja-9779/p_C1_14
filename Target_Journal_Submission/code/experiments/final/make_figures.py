"""Main figures 1-3 + SI figure from locked results. Palette: validated categorical slots 1-3 (blue, orange, aqua)."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "..", "..", "manuscript", "figures")
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"; INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False, "pdf.fonttype": 42})
d = pd.read_csv(os.path.join(HERE, "locked_rows.csv.gz")); info = pd.read_csv(os.path.join(HERE, "locked_cohorts.csv"))
d["key"] = d.method + np.where(d.n > 0, "_n" + d.n.astype(str), "")
cm = d.groupby(["alpha", "task", "model", "key", "cohort"]).agg(fpr=("fpr", "mean"), sens=("sens", "mean")).reset_index()
SHORT = {"HMP_2019_ibdmdb": "HMP2 (iHMP)", "MetaCardis_2020_a": "MetaCardis", "SankaranarayananK_2015": "Sankaranarayanan 2015"}
lab = lambda s: SHORT.get(s, s.replace("_2019_c", " 2019c").replace("_2018a", " 2018a").replace("_2018b", " 2018b").replace("_", " "))
def save(fig, name):
    for ext in ("pdf", "png"): fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)

# ---------- Figure 1: realised FPR per held-out cohort, status quo vs batch correction vs 20 local controls ----------
def fig1(model, name):
    a = 0.10; c = cm[(cm.alpha == a) & (cm.model == model)]
    order = [("CRC", "Colorectal cancer (external)"), ("IBD", "IBD"), ("T2D", "Type 2 diabetes"), ("adenoma", "Adenoma")]
    rows = []
    for t, tl in order:
        for s in sorted(c[c.task == t].cohort.unique()): rows.append((t, tl, s))
    fig, ax = plt.subplots(figsize=(6.3, 5.2)); y = 0; yt, yl, heads = [], [], []
    ax.axvspan(0.05, 0.15, color=GRID, alpha=0.6, lw=0, zorder=0); ax.axvline(a, color=INK2, lw=1, ls="--", zorder=1)
    prev = None
    for t, tl, s in rows:
        if t != prev: y += 0.8; heads.append((y, tl)); y += 1; prev = t
        q = c[(c.task == t) & (c.cohort == s)].set_index("key").fpr
        xs = [q.get("source", np.nan), q.get("cohortstd", np.nan), q.get("conformal_n20", np.nan)]
        ax.plot([min(v for v in xs if v == v), max(v for v in xs if v == v)], [y, y], color=GRID, lw=1.5, zorder=1)
        ax.scatter(xs[0], y - 0.17, s=34, marker="o", color=BLUE, zorder=3, ec="white", lw=0.8)
        ax.scatter(xs[1], y + 0.17, s=34, marker="s", color=ORANGE, zorder=3, ec="white", lw=0.8)
        if xs[2] == xs[2]: ax.scatter(xs[2], y, s=46, marker="D", color=AQUA, zorder=4, ec=INK, lw=0.6)
        yt.append(y); yl.append(lab(s)); y += 1
    for hy, tl in heads: ax.text(-0.005, hy, tl, fontsize=8, fontweight="bold", color=INK, va="center", ha="left", transform=ax.get_yaxis_transform() if False else ax.transData)
    ax.set_yticks(yt, yl); ax.invert_yaxis(); ax.set_xlim(-0.01, max(0.72, c[c.key == "source"].fpr.max() + 0.03))
    ax.set_xlabel("Realised false-positive rate in held-out cohort (target 0.10; grey band 0.05–0.15)")
    ax.grid(axis="y", visible=False)
    h = [plt.Line2D([], [], marker="o", ls="", color=BLUE, label="Threshold from training cohorts (status quo)"),
         plt.Line2D([], [], marker="s", ls="", color=ORANGE, label="Cohort-wise feature standardisation, then training threshold"),
         plt.Line2D([], [], marker="D", ls="", color=AQUA, mec=INK, mew=0.6, label="Threshold from 20 local controls (conformal)")]
    ax.legend(handles=h, loc="lower right", fontsize=7)
    ax.set_title(f"{'LASSO logistic regression' if model=='lasso' else 'Random forest'}: mean over 200 calibration/evaluation splits", fontsize=8, color=INK2, loc="left", pad=14)
    save(fig, name)
fig1("lasso", "Figure1_fpr_by_cohort"); fig1("rf", "FigureS1_fpr_by_cohort_rf")

# ---------- Figure 2: methods compared (alpha=0.10) ----------
a = 0.10; c = cm[cm.alpha == a]; dd = d[d.alpha == a]
mm = pd.read_csv(os.path.join(HERE, "mismatch_rows.csv.gz")); mm = mm[mm.cal != mm.deploy]
mm_c = mm.groupby(["setting", "model", "cal", "deploy"]).fpr.mean().values
meth = [("source", "Training threshold\n(status quo)"), ("cohortstd", "Feature standardisation\n+ training threshold"),
        ("pool_q", "Unlabelled-pool quantile\n(case-control mix)"), ("site_shift", "Site-shift mixture\n(unlabelled)"),
        ("anchor_locscale_n20", "Median/IQR anchor\n(20 local controls)"), ("OTHER", "20 controls from\nanother site*"),
        ("conformal_n20", "20 controls from\nthe same site"), ("tong95_n30", "95%-confidence rule\n(29-30 same-site controls)")]
fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.6), gridspec_kw=dict(width_ratios=[1.5, 1, 1]), sharey=True)
rng = np.random.default_rng(0)
for i, (k, l) in enumerate(meth):
    if k == "OTHER": v = mm_c; pv = (mm.fpr > 1.5 * a).mean(); sv = np.nan
    else: v = c[c.key == k].fpr.values; pv = (dd[dd.key == k].fpr > 1.5 * a).mean(); sv = c[c.key == k].sens.mean()
    col = AQUA if k in ("conformal_n20", "tong95_n30") else (ORANGE if k == "OTHER" else BLUE)
    axs[0].scatter(v, i + rng.uniform(-0.18, 0.18, len(v)), s=10, color=col, alpha=0.85, lw=0)
    axs[0].plot([np.median(v)] * 2, [i - 0.3, i + 0.3], color=INK, lw=1.5)
    axs[1].barh(i, pv, color=col, height=0.6); axs[1].text(pv + 0.01, i, f"{pv:.2f}", va="center", fontsize=7, color=INK2)
    if sv == sv: axs[2].barh(i, sv, color=col, height=0.6); axs[2].text(sv + 0.01, i, f"{sv:.2f}", va="center", fontsize=7, color=INK2)
    else: axs[2].text(0.01, i, "n/a", va="center", fontsize=7, color=INK2)
axs[0].axvspan(0.05, 0.15, color=GRID, alpha=0.6, lw=0, zorder=0); axs[0].axvline(a, color=INK2, ls="--", lw=1)
axs[0].set_yticks(range(len(meth)), [l for _, l in meth]); axs[0].invert_yaxis()
axs[0].set_xlabel("Cohort-mean realised FPR\n(dot = cohort x model; bar = median)")
axs[1].set_xlabel("Share of single calibrations\nwith FPR > 0.15"); axs[2].set_xlabel("Mean sensitivity")
axs[1].set_xlim(0, 0.85); axs[2].set_xlim(0, 0.8)
for ax, t in zip(axs, "abc"): ax.set_title(t, loc="left", fontweight="bold", fontsize=9); ax.grid(axis="y", visible=False)
fig.text(0.0, -0.05, "Blue: no labelled local data. Orange: labelled controls from a different centre/cohort (*MetaCardis centres and external CRC cohorts only; dot = site pair).\nGreen: labelled controls from the deployment site. Target FPR 0.10. Same-site methods shown only for cohorts with enough controls.", fontsize=6.3, color=INK2)
fig.tight_layout(); save(fig, "Figure2_methods")

# ---------- Figure 3: CRC screening consequence with uncertainty + control budget ----------
from scipy import stats as st_
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.2))
p = 0.005; h = dd[(dd.task == "CRC") & (dd.model == "lasso")]
coh = ["ThomasAM_2019_c", "YuJ_2015", "YachidaS_2019"]; mk = [("source", "Training threshold", BLUE, "o", -0.12), ("conformal_n20", "20 same-site controls", AQUA, "D", 0.12)]
for j, s in enumerate(coh):
    for k, l, col, m, off in mk:
        q = h[(h.cohort == s) & (h.key == k)]; fp = 1000 * (1 - p) * q.fpr; mi = 1000 * p * (1 - q.sens)
        y0 = j + off
        axs[0].errorbar(fp.mean(), y0, xerr=[[fp.mean() - fp.quantile(.025)], [fp.quantile(.975) - fp.mean()]], fmt=m, color=col, ms=6, mec=INK if m == "D" else "white", mew=0.6, elinewidth=1.5, capsize=0, label=l if j == 0 else None)
        axs[0].text(410, y0, f"{mi.mean():.1f}", va="center", fontsize=6.5, color=INK2)
axs[0].text(410, -0.45, "missed\ncancers", fontsize=6.5, color=INK2, va="bottom", ha="left")
axs[0].set_yticks(range(3), [lab(s) for s in coh]); axs[0].set_xlim(0, 450); axs[0].set_ylim(2.45, -0.75)
axs[0].set_xlabel("Unnecessary colonoscopies per 1,000 screened\n(mean and 95% range over calibration/evaluation splits)")
axs[0].legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.45, -0.28), ncol=2); axs[0].grid(axis="y", visible=False)
axs[0].set_title("a  External CRC, LASSO, prevalence 0.5%", loc="left", fontsize=8, fontweight="bold")
ns = np.arange(9, 300, 10); lo, hi, md = [], [], []
for n in ns:
    k = int(np.ceil((n + 1) * 0.9)); b = st_.beta(n + 1 - k, k); lo.append(b.ppf(.025)); hi.append(b.ppf(.975)); md.append(b.mean())
axs[1].fill_between(ns, lo, hi, color=AQUA, alpha=0.25, lw=0, label="Theory: 95% range of a single site's FPR")
axs[1].plot(ns, md, color=AQUA, lw=2, label="Theory: expected FPR")
e = pd.read_csv(os.path.join(HERE, "control_budget_emp.csv"))
for n, q in e.groupby("n"):
    axs[1].errorbar(n, q.mean_FPR.mean(), yerr=[[q.mean_FPR.mean() - q.q025.mean()], [q.q975.mean() - q.mean_FPR.mean()]], fmt="o", color=BLUE, ms=5, capsize=0, label="Observed (MetaCardis, Yachida, Qin)" if n == 19 else None)
axs[1].axhspan(0.05, 0.15, color=GRID, alpha=0.6, lw=0, zorder=0); axs[1].axhline(0.10, color=INK2, ls="--", lw=1)
axs[1].set_xscale("log"); axs[1].set_xticks([9, 19, 49, 99, 199, 299], ["9", "19", "49", "99", "199", "299"])
axs[1].set_xlabel("Labelled same-site controls (n)"); axs[1].set_ylabel("Realised FPR"); axs[1].set_ylim(0, 0.32)
axs[1].legend(fontsize=6.3, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=1); axs[1].set_title("b  How many local controls?", loc="left", fontsize=8, fontweight="bold")
fig.tight_layout(); save(fig, "Figure3_consequence")
print("ok")
