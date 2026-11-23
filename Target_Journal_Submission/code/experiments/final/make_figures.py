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

# ---------- Figure 2: methods compared, pooled across tasks/models (alpha=0.10) ----------
a = 0.10; c = cm[cm.alpha == a]; dd = d[d.alpha == a]
meth = [("source", "Training threshold\n(status quo)"), ("cohortstd", "Feature\nstandardisation"), ("em", "Prevalence EM"),
        ("pool_q", "Unlabelled-pool\nquantile"), ("site_shift", "Site-shift\nmixture"), ("anchor_locscale_n20", "Median/IQR anchor\n(20 controls)"),
        ("conformal_n10", "Conformal\n(10 controls)"), ("conformal_n20", "Conformal\n(20 controls)"), ("tong95_n30", "95%-confidence\n(30 controls)")]
fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.4), gridspec_kw=dict(width_ratios=[1.5, 1, 1]), sharey=True)
rng = np.random.default_rng(0)
for i, (k, l) in enumerate(meth):
    v = c[c.key == k].fpr.values
    axs[0].scatter(v, i + rng.uniform(-0.18, 0.18, len(v)), s=10, color=AQUA if k.startswith(("conformal", "tong")) else BLUE, alpha=0.8, lw=0)
    axs[0].plot([np.median(v)] * 2, [i - 0.3, i + 0.3], color=INK, lw=1.5)
    p = (dd[dd.key == k].fpr > 1.5 * a).mean(); axs[1].barh(i, p, color=AQUA if k.startswith(("conformal", "tong")) else BLUE, height=0.6)
    axs[1].text(p + 0.01, i, f"{p:.2f}", va="center", fontsize=7, color=INK2)
    s = c[c.key == k].sens.mean(); axs[2].barh(i, s, color=AQUA if k.startswith(("conformal", "tong")) else BLUE, height=0.6)
    axs[2].text(s + 0.01, i, f"{s:.2f}", va="center", fontsize=7, color=INK2)
axs[0].axvspan(0.05, 0.15, color=GRID, alpha=0.6, lw=0, zorder=0); axs[0].axvline(a, color=INK2, ls="--", lw=1)
axs[0].set_yticks(range(len(meth)), [l for _, l in meth]); axs[0].invert_yaxis()
axs[0].set_xlabel("Cohort-mean realised FPR\n(each dot = cohort × model; bar = median)")
axs[1].set_xlabel("Share of single-site splits\nwith FPR > 0.15"); axs[2].set_xlabel("Mean sensitivity")
axs[1].set_xlim(0, 0.85); axs[2].set_xlim(0, 0.8)
for ax, t in zip(axs, "abc"): ax.set_title(t, loc="left", fontweight="bold", fontsize=9); ax.grid(axis="y", visible=False)
fig.text(0.0, -0.04, "Blue: no labelled local data. Aqua: uses n labelled local controls. Target FPR 0.10. Local-control methods only where the cohort has enough controls.", fontsize=6.5, color=INK2)
fig.tight_layout(); save(fig, "Figure2_methods")

# ---------- Figure 3: CRC screening consequence + how many local controls ----------
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.1))
p = 0.005; h = cm[(cm.task == "CRC") & (cm.alpha == 0.10) & (cm.model == "lasso")]
coh = ["ThomasAM_2019_c", "YuJ_2015", "YachidaS_2019"]; mk = [("source", "Status quo", BLUE, "o"), ("cohortstd", "Feature standardisation", ORANGE, "s"), ("conformal_n20", "20 local controls", AQUA, "D")]
for j, s in enumerate(coh):
    for k, l, col, m in mk:
        q = h[(h.cohort == s) & (h.key == k)].iloc[0]
        axs[0].scatter(1000 * (1 - p) * q.fpr, 1000 * p * (1 - q.sens), color=col, marker=m, s=40, ec=INK if m == "D" else "white", lw=0.6, zorder=3, label=l if j == 0 else None)
    xs = [1000 * (1 - p) * h[(h.cohort == s) & (h.key == k)].fpr.iloc[0] for k, *_ in mk]; ys = [1000 * p * (1 - h[(h.cohort == s) & (h.key == k)].sens.iloc[0]) for k, *_ in mk]
    axs[0].plot(xs, ys, color=GRID, lw=1, zorder=1); axs[0].annotate(lab(s), (xs[0], ys[0]), xytext=(4, 4), textcoords="offset points", fontsize=6.5, color=INK2)
axs[0].set_xlabel("Unnecessary colonoscopies per 1,000 screened"); axs[0].set_ylabel("Missed cancers per 1,000 screened")
axs[0].legend(fontsize=6.5, loc="upper right"); axs[0].set_title("a  External CRC cohorts (LASSO, prevalence 0.5%)", loc="left", fontsize=8, fontweight="bold")
# panel b: n controls vs per-split exceedance and sensitivity (pooled over feasible pairs, alpha=0.10)
ks = [("conformal_n10", 10), ("conformal_n20", 20), ("conformal_n30", 30), ("tong95_n30", 30), ("tong95_n50", 50)]
rows = []
for k, n in ks:
    q = dd[dd.key == k]; rows.append((k, n, (q.fpr > 0.15).mean(), q.fpr.mean(), q.sens.mean()))
r = pd.DataFrame(rows, columns=["k", "n", "exceed", "fpr", "sens"])
cf = r[r.k.str.startswith("conformal")]; tg = r[r.k.str.startswith("tong")]
axs[1].plot(cf.n, cf.exceed, color=AQUA, marker="D", lw=2, ms=6, mec=INK, mew=0.6, label="Conformal (mean FPR ≤ 0.10)")
axs[1].plot(tg.n, tg.exceed, color=BLUE, marker="o", lw=2, ms=6, label="95%-confidence rule")
for _, q in r.iterrows(): axs[1].annotate(f"sens {q.sens:.2f}", (q.n, q.exceed), xytext=(5, 3), textcoords="offset points", fontsize=6.5, color=INK2)
axs[1].set_xlabel("Labelled local controls (n)"); axs[1].set_ylabel("Share of splits with FPR > 0.15"); axs[1].set_ylim(0, 0.3); axs[1].set_xlim(5, 58)
axs[1].legend(fontsize=6.5, loc="upper right"); axs[1].set_title("b  Local-control budget (all feasible cohorts)", loc="left", fontsize=8, fontweight="bold")
fig.tight_layout(); save(fig, "Figure3_consequence")
print("ok")
