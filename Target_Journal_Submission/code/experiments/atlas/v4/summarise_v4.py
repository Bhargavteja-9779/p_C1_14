"""Summaries for P4-P6, P9 with population-cluster bootstrap. Writes results/summary_v4.json and *_v4.csv tables."""
import os, json, numpy as np, pandas as pd
from scipy import stats
from common_v4 import *
A, B = 0.10, 2000; rng = np.random.default_rng(7); dev, lock = split()
o = pd.read_csv(os.path.join(OUT, "deploy_v4_healthy.csv.gz"))
unit = o.groupby(["design", "disease", "model", "unit", "pop_burn", "pop_eval", "N", "method"]).fpr.agg(
    mad=lambda x: np.mean(np.abs(x - A)), p15=lambda x: np.mean(x > .15), p10=lambda x: np.mean(x > A), fpr="mean").reset_index()
unit.to_csv(os.path.join(OUT, "deploy_v4_units.csv"), index=False)
def cboot(df, col, cluster="pop_eval"):
    """mean of unit values; 95% CI by resampling distinct populations."""
    g = df.groupby(cluster)[col].agg(["sum", "size"]); s, n = g["sum"].values, g["size"].values; k = len(g)
    bs = [s[i].sum() / n[i].sum() for i in (rng.integers(0, k, k) for _ in range(B))]
    return dict(mean=s.sum() / n.sum(), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), units=int(n.sum()), populations=int(k))
def paired(df, m1, m2, col="mad"):
    w = df.pivot_table(index=["disease", "model", "unit", "pop_eval"], columns="method", values=col).reset_index().dropna(subset=[m1, m2])
    w["diff"] = w[m1] - w[m2]; r = cboot(w, "diff"); pp = w.groupby("pop_eval")["diff"].mean()
    r.update(rel=float(w[m1].mean() / w[m2].mean() - 1), sign_pos=int((pp > 0).sum()), sign_neg=int((pp < 0).sum()),
             wilcoxon_pop_p=float(stats.wilcoxon(pp).pvalue) if len(pp) > 5 else None); return r
S = {}
rnd = unit[unit.design == "random"]
strict_pops = lambda df: df[~df.pop_eval.isin(STRICT_DROP_STUDIES)]
for name, df in [("locked_full", rnd[rnd.pop_eval.isin(lock)]), ("all_strict", strict_pops(rnd)), ("all_full", rnd)]:
    for N in [25, 50, 100, 200]:
        d = df[df.N == N]
        for meth in ["SRC", "ATLAS", "BURN", "BURN-PAC", "ALIGN"]:
            x = d[d.method == meth]
            if len(x): S[f"random/{name}/N{N}/{meth}"] = {c: cboot(x, c) for c in ["mad", "p15", "p10", "fpr"]}
        if N == 100:
            S[f"random/{name}/N100/BURN_minus_SRC_mad"] = paired(d, "BURN", "SRC")
            S[f"random/{name}/N100/BURN_minus_ALIGN_mad"] = paired(d, "BURN", "ALIGN")
            S[f"random/{name}/N100/ALIGN_minus_SRC_mad"] = paired(d, "ALIGN", "SRC")
# v3 success criterion re-evaluated (locked, full, N=100)
L = lambda k: S[f"random/locked_full/N100/{k}"]
S["v3_criterion_dedup"] = dict(BURN_p15=L("BURN")["p15"]["mean"], BURN_mad=L("BURN")["mad"]["mean"], SRC_mad=L("SRC")["mad"]["mean"],
                               reduction=1 - L("BURN")["mad"]["mean"] / L("SRC")["mad"]["mean"], PAC_p10=L("BURN-PAC")["p10"]["mean"])
# P4 stress designs
st = unit[unit.design != "random"].copy(); st["group"] = st.design.str.replace(r"covariate_.*", "covariate", regex=True)
for grp in ["covariate", "subsite", "accession", "neighbour", "NX1_pooled"]:
    d0 = st[st.group.isin(["covariate", "subsite", "accession"])] if grp == "NX1_pooled" else st[st.group == grp]
    for N in [50, 100]:
        d = d0[d0.N == N]
        if not len(d): continue
        for meth in ["SRC", "BURN", "BURN-PAC"]:
            x = d[d.method == meth]; S[f"stress/{grp}/N{N}/{meth}"] = {c: cboot(x, c) for c in ["mad", "p15", "p10", "fpr"]}
        S[f"stress/{grp}/N{N}/BURN_minus_SRC_mad"] = paired(d, "BURN", "SRC")
nx1 = S["stress/NX1_pooled/N100/BURN"]; src1 = S["stress/NX1_pooled/N100/SRC"]
S["H-NX1"] = dict(burn_mad=nx1["mad"]["mean"], src_mad=src1["mad"]["mean"], reduction=1 - nx1["mad"]["mean"] / src1["mad"]["mean"],
                  burn_p15=nx1["p15"]["mean"], supported=bool(1 - nx1["mad"]["mean"] / src1["mad"]["mean"] >= .5 and nx1["p15"]["mean"] <= .2))
nb = S.get("stress/neighbour/N100/BURN")
if nb: S["H-NX2"] = dict(burn_p15=nb["p15"]["mean"], burn_mad=nb["mad"]["mean"], supported=bool(nb["p15"]["mean"] > .2))
# contaminated pools + P9 PPV
c = pd.read_csv(os.path.join(OUT, "deploy_v4_cc.csv.gz"))
cu = c.groupby(["disease", "model", "pop", "N", "pi", "pimax", "method"]).agg(fpr=("fpr", "mean"), p15=("fpr", lambda x: np.mean(x > .15)), sens=("sens", "mean")).reset_index()
cs = cu.groupby(["N", "pi", "pimax", "method"]).agg(units=("pop", "size"), pops=("pop", "nunique"), fpr=("fpr", "mean"), p15=("p15", "mean"), sens=("sens", "mean")).reset_index()
cs.to_csv(os.path.join(OUT, "deploy_v4_cc_summary.csv"), index=False)
ppv = []
for _, r in cs[(cs.N == 100)].iterrows():
    for prev in [0.005, 0.01]:
        ppv.append(dict(pi=r.pi, pimax=r.pimax, method=r.method, prev=prev, sens=r.sens, fpr=r.fpr, ppv=r.sens * prev / (r.sens * prev + r.fpr * (1 - prev))))
pd.DataFrame(ppv).to_csv(os.path.join(OUT, "ppv_v4.csv"), index=False)
json.dump(S, open(os.path.join(OUT, "summary_v4.json"), "w"), indent=1, default=float)
for k in ["v3_criterion_dedup", "H-NX1", "H-NX2"]: print(k, json.dumps(S.get(k), default=float))
for k, v in S.items():
    if "minus" in k: print(k, {a: round(b, 4) if isinstance(b, float) else b for a, b in v.items()})
rows = [(k, v["mad"]["mean"], v["p15"]["mean"], v["fpr"]["mean"], v["mad"]["populations"], v["mad"]["units"]) for k, v in S.items() if isinstance(v, dict) and "mad" in v and isinstance(v["mad"], dict)]
t = pd.DataFrame(rows, columns=["key", "mad", "p15", "fpr", "pops", "units"]); t.to_csv(os.path.join(OUT, "summary_v4_table.csv"), index=False)
pd.set_option("display.width", 200); print(t.round(3).to_string()); print(cs.round(3).to_string())
