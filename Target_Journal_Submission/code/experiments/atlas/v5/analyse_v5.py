"""v5 confirmatory analyses H1-H4 (protocol_v5.md) + exploratory. Writes results/v5_*.csv|json."""
import os, json, zlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
import statsmodels.formula.api as smf
from common_v5 import *
from src.pipeline import _log
r = pd.read_csv(os.path.join(OUT5, "atlas_rows_v5.csv.gz")); T = pd.read_csv(os.path.join(OUT5, "tests_v5.csv"))
def strict(h):
    h = h[(h.strict_person == True) & ~h.study.isin(STRICT_DROP_STUDIES)]; return h[h.groupby(["test", "model", "study"]).study.transform("size") >= MIN_N]
def dl(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum(); df = len(y) - 1
    t2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); ws = 1 / (v + t2); m2 = (ws * y).sum() / ws.sum(); se = ws.sum() ** -.5; t = stats.t.ppf(.975, len(y) - 2); ex = lambda x: 1 / (1 + np.exp(-x))
    return dict(pooled=ex(m2), tau=np.sqrt(t2), I2=max(0, (Q - df) / Q), Q_p=stats.chi2.sf(Q, df), pi_lo=ex(m2 - t * np.sqrt(t2 + se ** 2)), pi_hi=ex(m2 + t * np.sqrt(t2 + se ** 2)))
out = {}
for setname, H in [("strict", strict(r)), ("full", r)]:
    per = H.groupby(["test", "model", "study"]).agg(n=("flag", "size"), k=("flag", "sum")).reset_index(); per["fpr"] = per.k / per.n
    het = pd.DataFrame([dict(test=t, model=m, populations=len(g), people=int(g.n.sum()), **dl(g.k.values, g.n.values),
                             oob=float(((g.fpr < .05) | (g.fpr > .15)).mean()), fpr_min=g.fpr.min(), fpr_max=g.fpr.max()) for (t, m), g in per.groupby(["test", "model"])])
    het = het.merge(T[["test", "model", "auroc"]], on=["test", "model"]); het.to_csv(os.path.join(OUT5, f"v5_het_{setname}.csv"), index=False); per.to_csv(os.path.join(OUT5, f"v5_perpop_{setname}.csv"), index=False)
    out[f"H1_{setname}"] = dict(tests=len(het), I2_ge_050=int((het.I2 >= .5).sum()), I2_median=float(het.I2.median()), I2_range=[float(het.I2.min()), float(het.I2.max())],
                                auroc65_tests=int((het.auroc >= .65).sum()), auroc65_I2_ge_050=int(((het.auroc >= .65) & (het.I2 >= .5)).sum()))
    # H2 crossed random effects on empirical logit FPR
    for m in ["lasso", "rf"]:
        d = per[per.model == m].copy(); d["y"] = np.log((d.k + .5) / (d.n - d.k + .5)); d["one"] = 1
        f = smf.mixedlm("y ~ 1", d, groups="one", vc_formula={"test": "0 + C(test)", "pop": "0 + C(study)"}).fit(reml=True)
        vc = dict(zip(f.model.exog_vc.names, f.vcomp)); tot = vc["test"] + vc["pop"] + f.scale
        out[f"H2_{setname}_{m}"] = dict(var_test=vc["test"], var_pop=vc["pop"], var_resid=f.scale, pop_share=vc["pop"] / tot, test_share=vc["test"] / tot, units=len(d), populations=d.study.nunique())
        # population false-alarm index (BLUP-like: mean deviation from test means)
        d["dev"] = d.y - d.groupby("test").y.transform("mean")
        d.groupby("study").agg(index=("dev", "mean"), tests=("dev", "size")).reset_index().assign(model=m).to_csv(os.path.join(OUT5, f"v5_popindex_{setname}_{m}.csv"), index=False)
# H3 recurrent drivers (strict, LASSO)
co = pd.read_csv(os.path.join(OUT5, "coefs_v5.csv")); per = pd.read_csv(os.path.join(OUT5, "v5_perpop_strict.csv")); top = []
import atlas_v5 as A5
for t in co.test.unique():
    c = co[co.test == t].reset_index(drop=True)
    if (c.w != 0).sum() == 0: continue
    case, studies = A5.TESTS[t]; X, y, g, M = A5.load_cc(case, studies)
    z0 = ((np.log10(X.reindex(columns=c.taxon, fill_value=0).fillna(0).values[y == 0] / 100 + 1e-5) - c.mu.values) / c.sd.values).mean(0)
    pp = per[(per.test == t) & (per.model == "lasso")].sort_values("fpr", ascending=False)
    s = pp.study.iloc[0]; Xc, md = controls(s); Xc = Xc[md.strict_person.values]
    z = ((np.log10(Xc.reindex(columns=c.taxon, fill_value=0).fillna(0).values / 100 + 1e-5) - c.mu.values) / c.sd.values).mean(0)
    contrib = c.w.values * (z - z0)
    for i, j in enumerate(np.argsort(-contrib)[:10]):
        if contrib[j] > 0: top.append(dict(test=t, study=s, fpr=pp.fpr.iloc[0], rank=i + 1, taxon=c.taxon[j], w=c.w[j], dz=(z - z0)[j], contrib=contrib[j]))
top = pd.DataFrame(top); top.to_csv(os.path.join(OUT5, "v5_top_taxa.csv"), index=False)
rec = top.groupby("taxon").test.nunique().sort_values(ascending=False); rec.to_csv(os.path.join(OUT5, "v5_recurrent_taxa.csv"))
out["H3"] = dict(tests_decomposed=int(top.test.nunique()), taxa_in_ge4_tests=int((rec >= 4).sum()), taxa_in_ge3_tests=int((rec >= 3).sum()), top=rec.head(12).to_dict())
# H4 within-site burn-in (accession order, covariate halves), N=100, all populations (full set), as v4 P4
def k_conf(N): return int(np.ceil((N + 1) * (1 - A)))
res = []
for (t, m), g in r.groupby(["test", "model"]):
    t0 = g.thr.iloc[0]
    for s, x in g.groupby("study"):
        if len(x) < 120: continue
        md = META.loc[x.sample_id]; sc = x.score.values
        order = np.argsort(md.NCBI_accession.astype(str).values + "|" + md.index.values.astype(str), kind="stable")
        xs = sc[order]; res.append(dict(test=t, model=m, design="accession", pop=s, src=abs(np.mean(xs[100:] >= t0) - A), burn=abs(np.mean(xs[100:] >= np.sort(xs[:100])[k_conf(100) - 1]) - A)))
        rng = np.random.default_rng(zlib.crc32(f"{t}{m}{s}".encode()))
        for cov in ["age", "BMI"]:
            v = pd.to_numeric(md[cov], errors="coerce").values
            if np.isfinite(v).mean() < .8: continue
            ok = np.isfinite(v); lo, hi = ok & (v <= np.median(v[ok])), ok & (v > np.median(v[ok]))
            if lo.sum() < 100 or hi.sum() < 40: continue
            b = [abs(np.mean(sc[hi] >= np.sort(sc[lo][rng.permutation(lo.sum())[:100]])[k_conf(100) - 1]) - A) for _ in range(200)]
            res.append(dict(test=t, model=m, design=f"cov_{cov}", pop=s, src=abs(np.mean(sc[hi] >= t0) - A), burn=float(np.mean(b))))
R4 = pd.DataFrame(res); R4.to_csv(os.path.join(OUT5, "v5_h4_units.csv"), index=False)
pt = R4.groupby(["test", "model"]).agg(src=("src", "mean"), burn=("burn", "mean"), units=("pop", "size")).reset_index(); pt["better"] = pt.burn < pt.src
out["H4"] = dict(tests=len(pt), tests_burn_better=int(pt.better.sum()), share=float(pt.better.mean()), mean_src=float(pt.src.mean()), mean_burn=float(pt.burn.mean()),
                 wilcoxon_tests_p=float(stats.wilcoxon(pt.burn - pt.src).pvalue))
# exploratory: AUROC vs heterogeneity
h = pd.read_csv(os.path.join(OUT5, "v5_het_strict.csv")); out["expl_auroc_vs_tau"] = dict(spearman=float(stats.spearmanr(h.auroc, h.tau)[0]), p=float(stats.spearmanr(h.auroc, h.tau)[1]))
json.dump(out, open(os.path.join(OUT5, "v5_summary.json"), "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
print(h.sort_values("I2").round(3).to_string())
