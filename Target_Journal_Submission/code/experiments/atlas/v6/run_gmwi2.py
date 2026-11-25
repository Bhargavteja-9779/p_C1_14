"""Plan v6: score healthy atlas populations with the published GMWI2; QC vs published scores; G1-G4."""
import os, sys, json, zlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v4"))
from common_v4 import controls, healthy_studies, dropped_studies, STRICT_DROP_STUDIES, CACHE, META, MIN_N
OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)
J = json.load(open(os.path.join(HERE, "gmwi2_coefficients.json"))); F, W = J["features"], np.array(J["coef"])
S2 = pd.read_csv(os.path.join(HERE, "inputs/gmwi2_SData2_training_samples.csv.gz")); S5 = pd.read_csv(os.path.join(HERE, "inputs/gmwi2_SData5_published_scores.csv.gz"))
H5 = S5[S5["Subject health status"] == "Healthy"]; ALPHA = float((H5.GMWI2 < 0).mean())
train_ids = set(S2["Sample accession"].astype(str)) | set(S2["RunID"].astype(str))
pub = dict(zip(S5["Sample accession"].astype(str), S5.GMWI2))
def gmwi2(raw):
    """raw: clades x samples relative abundance (%, full MetaPhlAn3 clade strings). Presence = abundance/100 > 1e-5."""
    P = (raw.reindex(F).fillna(0.0).values / 100.0) > 1e-5
    return W @ P  # intercept 0
def in_training(md):
    acc = [str(a).split(";") if isinstance(a, str) else [] for a in md["NCBI_accession"].values]
    return np.array([(sid in train_ids) or any(a in train_ids for a in al) for sid, al in zip(md.index.astype(str), acc)])
rows = []
for s in healthy_studies():
    p = os.path.join(CACHE, "ra", f"{s}.csv")
    if s in dropped_studies() or not os.path.exists(p): continue
    X, md = controls(s)                                   # de-duplicated adult healthy, one per subject
    raw = pd.read_csv(p, index_col=0)[list(X.index)]
    sc = gmwi2(raw); tr = in_training(md)
    rows.append(pd.DataFrame(dict(study=s, sample_id=X.index, gmwi2=sc, flag=(sc < 0).astype(int), tie=(sc == 0).astype(int), in_gmwi2_training=tr,
                                  strict_person=md.strict_person.values, strict_study=s not in STRICT_DROP_STUDIES, published=[pub.get(str(i), np.nan) for i in X.index])))
R = pd.concat(rows); R.to_csv(os.path.join(OUT, "gmwi2_rows.csv.gz"), index=False)
q = R.dropna(subset=["published"]); qc = dict(n_overlap=len(q), pearson=float(np.corrcoef(q.gmwi2, q.published)[0, 1]) if len(q) > 2 else None,
                                              sign_agreement=float(np.mean((q.gmwi2 < 0) == (q.published < 0))) if len(q) else None)
print("QC", qc, "alpha_GMWI2", ALPHA, flush=True)
def dl(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum(); df = len(y) - 1
    t2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); ws = 1 / (v + t2); m2 = (ws * y).sum() / ws.sum(); se = ws.sum() ** -.5; t = stats.t.ppf(.975, len(y) - 2); ex = lambda x: 1 / (1 + np.exp(-x))
    return dict(pooled=ex(m2), tau=float(np.sqrt(t2)), I2=float(max(0, (Q - df) / Q)), Q_p=float(stats.chi2.sf(Q, df)), pi_lo=float(ex(m2 - t * np.sqrt(t2 + se ** 2))), pi_hi=float(ex(m2 + t * np.sqrt(t2 + se ** 2))))
def perpop(D):
    g = D.groupby("study").agg(n=("flag", "size"), k=("flag", "sum"), seen=("in_gmwi2_training", "any")).reset_index(); g["fpr"] = g.k / g.n; return g[g.n >= MIN_N]
res = dict(qc=qc, alpha_gmwi2=ALPHA, alpha_source="Chang 2024 SData5: share of healthy training samples with published GMWI2<0")
if qc["pearson"] is not None and qc["pearson"] < 0.90: res["stop"] = "QC failed"
for setname, D in [("strict", R[R.strict_person & R.strict_study]), ("full", R)]:
    P = perpop(D); P.to_csv(os.path.join(OUT, f"gmwi2_perpop_{setname}.csv"), index=False); U = P[~P.seen]; Sn = P[P.seen]
    o = dict(unseen_pops=len(U), unseen_people=int(U.n.sum()), seen_pops=len(Sn), fpr_unseen_range=[float(U.fpr.min()), float(U.fpr.max())] if len(U) else None,
             fpr_unseen_median=float(U.fpr.median()) if len(U) else None)
    if len(U) >= 5:
        o["G1"] = dl(U.k.values, U.n.values)
        lo, hi = ALPHA / 2, 1.5 * ALPHA; out_obs = float(((U.fpr < lo) | (U.fpr > hi)).mean())
        p_out = np.array([stats.binom.cdf(np.ceil(lo * n) - 1, n, ALPHA) + stats.binom.sf(np.floor(hi * n), n, ALPHA) for n in U.n])
        # exact Poisson-binomial tail P(#out >= observed) by DP
        dp = np.zeros(len(p_out) + 1); dp[0] = 1
        for pi in p_out: dp[1:] = dp[1:] * (1 - pi) + dp[:-1] * pi; dp[0] *= (1 - pi)
        kobs = int(((U.fpr < lo) | (U.fpr > hi)).sum())
        o["G2"] = dict(band=[lo, hi], out_observed=out_obs, out_expected=float(p_out.mean()), excess_pp=100 * (out_obs - float(p_out.mean())), p=float(dp[kobs:].sum()))
    if len(U) >= 3 and len(Sn) >= 3:
        o["G3"] = dict(seen_mean=float(Sn.fpr.mean()), unseen_mean=float(U.fpr.mean()), p=float(stats.mannwhitneyu(Sn.fpr, U.fpr, alternative="less").pvalue))
    res[setname] = o
# G4 within-site burn-in (full set, n>=120), target ALPHA, published cut-off 0 as status quo. Flag = score < cut-off.
def kth(N, a): return int(np.ceil((N + 1) * (1 - a)))
units = []
for s, x in R.groupby("study"):
    if len(x) < 120: continue
    md = META.loc[x.sample_id]; neg = -x.gmwi2.values      # flag if neg > t  <=> gmwi2 < -t ; status quo t=0
    order = np.argsort(md.NCBI_accession.astype(str).values + "|" + md.index.values.astype(str), kind="stable"); xs = neg[order]
    tb = np.sort(xs[:100])[kth(100, ALPHA) - 1]
    units.append(dict(pop=s, design="accession", seen=bool(x.in_gmwi2_training.any()), src=abs(np.mean(xs[100:] > 0) - ALPHA), burn=abs(np.mean(xs[100:] >= tb) - ALPHA)))
    rng = np.random.default_rng(zlib.crc32(f"gmwi2{s}".encode()))
    for cov in ["age", "BMI"]:
        v = pd.to_numeric(md[cov], errors="coerce").values
        if np.isfinite(v).mean() < .8: continue
        ok = np.isfinite(v); lo, hi = ok & (v <= np.median(v[ok])), ok & (v > np.median(v[ok]))
        if lo.sum() < 100 or hi.sum() < 40: continue
        b = [abs(np.mean(neg[hi] >= np.sort(neg[lo][rng.permutation(lo.sum())[:100]])[kth(100, ALPHA) - 1]) - ALPHA) for _ in range(200)]
        units.append(dict(pop=s, design=f"cov_{cov}", seen=bool(x.in_gmwi2_training.any()), src=abs(np.mean(neg[hi] > 0) - ALPHA), burn=float(np.mean(b))))
U4 = pd.DataFrame(units); U4.to_csv(os.path.join(OUT, "gmwi2_g4_units.csv"), index=False)
pp = U4.groupby("pop")[["src", "burn"]].mean(); rng = np.random.default_rng(7)
boot = [ (lambda b: 1 - b.burn.mean() / b.src.mean())(pp.iloc[rng.integers(0, len(pp), len(pp))]) for _ in range(5000)]
res["G4"] = dict(populations=len(pp), units=len(U4), mean_src=float(pp.src.mean()), mean_burn=float(pp.burn.mean()), rel_reduction=float(1 - pp.burn.mean() / pp.src.mean()),
                 ci95=[float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))], pops_better=int((pp.burn < pp.src).sum()),
                 p_boot_le0=float(np.mean(np.array(boot) <= 0)))
json.dump(res, open(os.path.join(OUT, "gmwi2_results.json"), "w"), indent=1); print(json.dumps(res, indent=1))
