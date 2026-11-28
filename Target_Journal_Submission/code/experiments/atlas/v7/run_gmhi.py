"""Plan v7 (protocol_v7_gmhi.md): audit of the published Gut Microbiome Health Index (GMHI; Gupta et al. 2020).
GMHI is re-implemented from the developers' GMHI.R (not executed). QC Q1-Q2, then H1-H6, Holm."""
import os, sys, json, zlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); IN = os.path.join(HERE, "inputs"); OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, "..", "v4"))
from common_v4 import controls, healthy_studies, dropped_studies, STRICT_DROP_STUDIES, CACHE, META, MIN_N
MH = [l.strip() for l in open(os.path.join(IN, "MH_species.txt")) if l.strip()]
MN = [l.strip() for l in open(os.path.join(IN, "MN_species.txt")) if l.strip()]
assert len(MH) == 7 and len(MN) == 43, (len(MH), len(MN))
EA_WORDS = ["china", "chinese", "japan", "japanese", "korea", "korean", "hong kong", "taiwan"]; EA_ISO = {"CHN", "JPN", "KOR", "HKG", "TWN"}

def gmhi(prof):
    """prof: DataFrame species (index, 's__' names) x samples, any scale. Exactly GMHI.R."""
    p = prof[[not (("unclassified" in i) or ("virus" in i)) for i in prof.index]].astype(float)
    p = p / p.sum(0); p = p.where(p >= 1e-5, 0.0)
    def part(sp, Rp):
        q = p.reindex(sp).fillna(0.0)
        sh = -(q.where(q > 0).apply(np.log) * q).sum(0)        # Shannon over present species
        R = (q > 0).sum(0); return (R / Rp) * sh
    return np.log10((part(MH, 7) + 1e-5) / (part(MN, 31) + 1e-5))

res = dict(source=open(os.path.join(IN, "SOURCE.txt")).read().strip())
# ---------------- Q1: developers' example ----------------
ex = pd.read_csv(os.path.join(IN, "species_relative_abundances.csv"), index_col=0)
ref = pd.read_csv(os.path.join(IN, "GMHI_output.csv"), index_col=0)["GMHI"]
mine = gmhi(ex).reindex(ref.index); res["Q1_max_abs_diff"] = float(np.nanmax(np.abs(mine.values - ref.values)))
print("Q1", res["Q1_max_abs_diff"], flush=True)
assert res["Q1_max_abs_diff"] < 1e-6, "Q1 failed: implementation does not reproduce GMHI.R"

# ---------------- developers' own data (H1, H2) ----------------
M = pd.read_csv(os.path.join(IN, "Final_metadata_4347.csv.gz"), header=None, index_col=0, low_memory=False).T.reset_index(drop=True)
sp_cols = [c for c in M.columns if str(c).startswith("s__")]
dev = gmhi(M[sp_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0).T)
M["gmhi"] = dev.values; M["study_no"] = M["Study No. (From VG sheet (V-*) from SB sheet (S-*))"]
reg = M["Geographical Region or Population"].astype(str).str.lower()
M["ea"] = reg.apply(lambda r: any(w in r for w in EA_WORDS))
Hd = M[M.Phenotype == "Healthy"].copy(); Hd["flag"] = (Hd.gmhi < 0).astype(int)
ALPHA = float(Hd.flag.mean()); res["alpha_gmhi"] = ALPHA; res["n_healthy_dev"] = int(len(Hd)); res["ties_dev"] = int((Hd.gmhi == 0).sum())
def dl(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum(); df = len(y) - 1
    t2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); ws = 1 / (v + t2); m2 = (ws * y).sum() / ws.sum(); se = ws.sum() ** -.5; t = stats.t.ppf(.975, len(y) - 2); ex_ = lambda x: 1 / (1 + np.exp(-x))
    return dict(k=len(y), pooled=ex_(m2), tau=float(np.sqrt(t2)), I2=float(max(0, (Q - df) / Q)), Q_p=float(stats.chi2.sf(Q, df)), pi_lo=float(ex_(m2 - t * np.sqrt(t2 + se ** 2))), pi_hi=float(ex_(m2 + t * np.sqrt(t2 + se ** 2))))
st = Hd.groupby("study_no").agg(n=("flag", "size"), k=("flag", "sum"), ea=("ea", "any"), region=("Geographical Region or Population", "first"),
                                author=("Author (year)", "first")).reset_index(); st["fpr"] = st.k / st.n; st = st[st.n >= 20]
st.to_csv(os.path.join(OUT, "gmhi_dev_perstudy.csv"), index=False)
res["H1"] = dl(st.k.values, st.n.values); res["H1"]["verdict"] = "supported" if res["H1"]["I2"] >= .5 else "falsified"
e, o = st[st.ea].fpr, st[~st.ea].fpr
res["H2"] = dict(n_ea=int(len(e)), n_other=int(len(o)), median_ea=float(e.median()) if len(e) else None, median_other=float(o.median()),
                 p=float(stats.mannwhitneyu(e, o, alternative="greater").pvalue) if len(e) >= 3 else None)
res["H2"]["verdict"] = "inconclusive" if len(e) < 3 else ("supported" if res["H2"]["p"] < .05 else "falsified")
print("alpha", ALPHA, "H1", res["H1"]["I2"], "H2", res["H2"], flush=True)

# ---------------- cMD healthy populations (Q2, H3-H6) ----------------
dev_ids = set(M["Sample Accession or Sample ID"].astype(str).str.strip())
dev_score = dict(zip(M["Sample Accession or Sample ID"].astype(str).str.strip(), M.gmhi))
rows = []; missing = None
for s in healthy_studies():
    p = os.path.join(CACHE, "ra", f"{s}.csv")
    if s in dropped_studies() or not os.path.exists(p): continue
    X, md = controls(s); raw = pd.read_csv(p, index_col=0)[list(X.index)]
    raw.index = [i.split("|")[-1] for i in raw.index]; raw = raw[[i.startswith("s__") for i in raw.index]].groupby(level=0).sum()
    if missing is None: missing = dict(MH=[x for x in MH if x not in raw.index], MN=[x for x in MN if x not in raw.index])
    sc = gmhi(raw).values
    acc = [str(a).split(";") if isinstance(a, str) else [] for a in md["NCBI_accession"].values]
    seen = np.array([(sid in dev_ids) or any(a in dev_ids for a in al) for sid, al in zip(md.index.astype(str), acc)])
    pub = [dev_score.get(sid, next((dev_score[a] for a in al if a in dev_score), np.nan)) for sid, al in zip(md.index.astype(str), acc)]
    rows.append(pd.DataFrame(dict(study=s, sample_id=X.index, gmhi=sc, flag=(sc < 0).astype(int), tie=(sc == 0).astype(int), in_gmhi_training=seen,
                                  strict_person=md.strict_person.values, strict_study=s not in STRICT_DROP_STUDIES, dev_gmhi=pub, country=md.country.values)))
R = pd.concat(rows); R.to_csv(os.path.join(OUT, "gmhi_rows.csv.gz"), index=False)
q = R.dropna(subset=["dev_gmhi"])
res["Q2"] = dict(n_overlap=int(len(q)), pearson=float(np.corrcoef(q.gmhi, q.dev_gmhi)[0, 1]) if len(q) > 2 else None,
                 sign_agreement=float(np.mean((q.gmhi < 0) == (q.dev_gmhi < 0))) if len(q) else None, missing_species_in_cMD=missing)
res["Q2"]["pass"] = bool(res["Q2"]["pearson"] is not None and res["Q2"]["pearson"] >= 0.80)
print("Q2", res["Q2"], flush=True)
def perpop(D):
    g = D.groupby("study").agg(n=("flag", "size"), k=("flag", "sum"), seen=("in_gmhi_training", "any"), country=("country", "first")).reset_index(); g["fpr"] = g.k / g.n; return g[g.n >= MIN_N]
for setname, D in [("strict", R[R.strict_person & R.strict_study]), ("full", R)]:
    P = perpop(D); P.to_csv(os.path.join(OUT, f"gmhi_perpop_{setname}.csv"), index=False); U = P[~P.seen]
    o = dict(unseen_pops=int(len(U)), unseen_people=int(U.n.sum()), seen_pops=int(P.seen.sum()), fpr_unseen_range=[float(U.fpr.min()), float(U.fpr.max())] if len(U) else None,
             fpr_unseen_median=float(U.fpr.median()) if len(U) else None,
             ea_unseen_median=float(U[U.country.isin(EA_ISO)].fpr.median()) if U.country.isin(EA_ISO).any() else None,
             other_unseen_median=float(U[~U.country.isin(EA_ISO)].fpr.median()) if len(U) else None, n_ea_unseen=int(U.country.isin(EA_ISO).sum()))
    if len(U) >= 5:
        o["H3"] = dl(U.k.values, U.n.values); o["H3"]["verdict"] = "supported" if o["H3"]["I2"] >= .5 else "falsified"
        lo, hi = ALPHA / 2, 1.5 * ALPHA; out = (U.fpr < lo) | (U.fpr > hi)
        p_out = np.array([stats.binom.cdf(np.ceil(lo * n) - 1, n, ALPHA) + stats.binom.sf(np.floor(hi * n), n, ALPHA) for n in U.n])
        dp = np.zeros(len(p_out) + 1); dp[0] = 1
        for pi in p_out: dp[1:] = dp[1:] * (1 - pi) + dp[:-1] * pi; dp[0] *= (1 - pi)
        o["H4"] = dict(band=[lo, hi], n_out=int(out.sum()), n=int(len(U)), out_observed=float(out.mean()), out_expected=float(p_out.mean()),
                       n_below=int((U.fpr < lo).sum()), n_above=int((U.fpr > hi).sum()), excess_pp=100 * (float(out.mean()) - float(p_out.mean())), p=float(dp[int(out.sum()):].sum()))
        o["H4"]["verdict"] = "supported" if (o["H4"]["excess_pp"] >= 20 and o["H4"]["p"] < .05) else "falsified"
    else:
        o["H3"] = o["H4"] = dict(verdict="inconclusive (< 5 unseen populations)")
    res[setname] = o
# H5: shared population effect with GMWI2 (strict, n >= 20, all populations scored by both)
G = pd.read_csv(os.path.join(HERE, "..", "v6", "results", "gmwi2_perpop_strict.csv"))
Ps = pd.read_csv(os.path.join(OUT, "gmhi_perpop_strict.csv")); J = Ps.merge(G, on="study", suffixes=("_gmhi", "_gmwi2"))
rho, p2 = stats.spearmanr(J.fpr_gmhi, J.fpr_gmwi2); res["H5"] = dict(n=int(len(J)), rho=float(rho), p_one_sided=float(p2 / 2 if rho > 0 else 1 - p2 / 2))
res["H5"]["verdict"] = "supported" if (rho > 0 and res["H5"]["p_one_sided"] < .05) else "falsified"
J.to_csv(os.path.join(OUT, "gmhi_vs_gmwi2_strict.csv"), index=False)
# H6: within-site burn-in (full set, n >= 120), target ALPHA; flag if -gmhi > t (status quo t = 0)
def kth(N, a): return int(np.ceil((N + 1) * (1 - a)))
units = []
for s, x in R.groupby("study"):
    if len(x) < 120: continue
    md = META.loc[x.sample_id]; neg = -x.gmhi.values
    order = np.argsort(md.NCBI_accession.astype(str).values + "|" + md.index.values.astype(str), kind="stable"); xs = neg[order]
    tb = np.sort(xs[:100])[kth(100, ALPHA) - 1]
    units.append(dict(pop=s, design="accession", src=abs(np.mean(xs[100:] > 0) - ALPHA), burn=abs(np.mean(xs[100:] >= tb) - ALPHA)))
    for cov in ["age", "BMI"]:
        v = pd.to_numeric(md[cov], errors="coerce").values
        if np.isfinite(v).mean() < .8: continue
        ok = np.isfinite(v); lo_, hi_ = ok & (v <= np.median(v[ok])), ok & (v > np.median(v[ok]))
        if lo_.sum() < 100 or hi_.sum() < 40: continue
        rng = np.random.default_rng(zlib.crc32(f"gmhi{s}{cov}".encode()))
        b = rng.choice(np.where(lo_)[0], 100, replace=False); ev = np.where(hi_)[0]
        tb = np.sort(neg[b])[kth(100, ALPHA) - 1]
        units.append(dict(pop=s, design=cov, src=abs(np.mean(neg[ev] > 0) - ALPHA), burn=abs(np.mean(neg[ev] >= tb) - ALPHA)))
Uh = pd.DataFrame(units); Uh.to_csv(os.path.join(OUT, "gmhi_h6_units.csv"), index=False)
d = (Uh.groupby("pop").burn.mean() - Uh.groupby("pop").src.mean()); rng = np.random.default_rng(7)
bs = np.array([d.sample(len(d), replace=True, random_state=int(rng.integers(1e9))).mean() for _ in range(5000)])
res["H6"] = dict(pops=int(len(d)), units=int(len(Uh)), src_mean=float(Uh.src.mean()), burn_mean=float(Uh.burn.mean()), rel_change=float(Uh.burn.mean() / Uh.src.mean() - 1),
                 diff=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], p=float(min(1, 2 * min((bs >= 0).mean(), (bs <= 0).mean()))),
                 pops_improved=int((d < 0).sum()))
res["H6"]["verdict"] = "supported" if res["H6"]["ci"][1] < 0 else "falsified"
# Holm over H2, H4 (strict), H5, H6
ps = {k: v for k, v in dict(H2=res["H2"].get("p"), H4=res["strict"].get("H4", {}).get("p"), H5=res["H5"]["p_one_sided"], H6=res["H6"]["p"]).items() if v is not None}
ks = sorted(ps, key=ps.get); m = len(ks); adj = {}; run = 0
for i, k in enumerate(ks): run = max(run, min(1, ps[k] * (m - i))); adj[k] = run
res["holm"] = adj
if not res["Q2"]["pass"]: res["note"] = "Q2 failed: H3-H6 not interpretable (implementation mismatch)"
json.dump(res, open(os.path.join(OUT, "gmhi_results.json"), "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)[:4000])
