"""P4 (non-exchangeable burn-in), P5 (ALIGN comparator), P6 (random-split re-run, contaminated pools). One run.
Writes results/deploy_v4_healthy.csv.gz, results/deploy_v4_cc.csv.gz."""
import os, zlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from multiprocessing import Pool
from scipy import stats
from common_v4 import *
from src.pipeline import Pipeline, _log, logit
A, R, DELTA = 0.10, 200, 0.05
def k_conf(N, beta): return int(np.ceil((N + 1) * (1 - beta)))
def k_pac(N, beta, delta=DELTA):
    for k in range(1, N + 1):
        if stats.beta.sf(beta, N + 1 - k, k) <= delta: return k
    return N + 1
def thr(b, k): return np.sort(b)[k - 1] if k <= len(b) else np.inf
dev, lock = split()
def country(md): return md.country.mode().iloc[0]
def job(a):
    d, m = a; rows = []
    X, y, g, M = load(d); p = Pipeline(m).fit(X.values, y, g); t0 = float(np.quantile(p.oof[y == 0], 1 - A))
    L0 = _log(X.values[y == 0], p.keep); mu0, sd0 = L0.mean(0), L0.std(0) + 1e-6
    pops = populations(d, strict=False); P = {}
    for s in pops:
        Xc, md = controls(s); Xa = Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0).values
        P[s] = dict(L=_log(Xa, p.keep), sc=p.score(Xa), md=md)
    def align_score(Lb, Le):
        La = (Le - Lb.mean(0)) / (Lb.std(0) + 1e-6) * sd0 + mu0
        return logit(p.m.predict_proba((La - p.mu) / p.sd)[:, 1])
    add = lambda design, unit, sb, se, N, meth, rep, f: rows.append((design, d, m, unit, sb, se, N, meth, rep, f))
    # P6 random splits (+P5 ALIGN at N=100)
    for s in pops:
        x = P[s]["sc"]; split_set = dev if s in dev else lock
        t_atlas = np.quantile(np.concatenate([P[o]["sc"] for o in pops if o in split_set and o != s]), 1 - A)
        rng = np.random.default_rng(zlib.crc32(f"{d}{m}{s}".encode()))
        for N in [25, 50, 100, 200]:
            if len(x) < N + 20: continue
            for rep in range(R):
                perm = rng.permutation(len(x)); b, e = x[perm[:N]], x[perm[N:]]
                for meth, t in [("SRC", t0), ("ATLAS", t_atlas), ("BURN", thr(b, k_conf(N, A))), ("BURN-PAC", thr(b, k_pac(N, A)))]:
                    add("random", s, s, s, N, meth, rep, np.mean(e >= t))
                if N == 100:
                    add("random", s, s, s, N, "ALIGN", rep, np.mean(align_score(P[s]["L"][perm[:N]], P[s]["L"][perm[N:]]) >= t0))
    # P4 non-exchangeable designs
    def stress(design, unit, sb, xb, se, xe):
        rng = np.random.default_rng(zlib.crc32(f"{design}{unit}{d}{m}".encode()))
        for N in [50, 100]:
            if len(xb) < N or len(xe) < 40: continue
            add(design, unit, sb, se, N, "SRC", 0, np.mean(xe >= t0))
            for rep in range(R):
                b = xb[rng.permutation(len(xb))[:N]]
                add(design, unit, sb, se, N, "BURN", rep, np.mean(xe >= thr(b, k_conf(N, A))))
                add(design, unit, sb, se, N, "BURN-PAC", rep, np.mean(xe >= thr(b, k_pac(N, A))))
    for s in pops:
        x, md = P[s]["sc"], P[s]["md"]
        if len(x) >= 150:
            for cov in ["age", "BMI"]:
                v = pd.to_numeric(md[cov], errors="coerce").values
                if np.isfinite(v).mean() < .8: continue
                ok = np.isfinite(v); med = np.median(v[ok]); lo, hi = ok & (v <= med), ok & (v > med)
                stress(f"covariate_{cov}", f"{s}:{cov}", s, x[lo], s, x[hi])
            sex = md.gender.values
            if (sex == "female").sum() >= 60 and (sex == "male").sum() >= 60:
                stress("covariate_sex", f"{s}:F>M", s, x[sex == "female"], s, x[sex == "male"])
                stress("covariate_sex", f"{s}:M>F", s, x[sex == "male"], s, x[sex == "female"])
        acc = md.assign(_a=md.NCBI_accession.astype(str), _i=md.index).sort_values(["_a", "_i"]).index
        order = pd.Index(md.index).get_indexer(acc)
        for N in [50, 100]:
            if len(x) >= N + 20:
                xs = x[order]; add("accession", f"{s}:acc", s, s, N, "SRC", 0, np.mean(xs[N:] >= t0))
                add("accession", f"{s}:acc", s, s, N, "BURN", 0, np.mean(xs[N:] >= thr(xs[:N], k_conf(N, A))))
                add("accession", f"{s}:acc", s, s, N, "BURN-PAC", 0, np.mean(xs[N:] >= thr(xs[:N], k_pac(N, A))))
    subs = [("MetaCardis_2020_a", "location", ["Leipzig", "Copenhagen", "Paris"]), ("AsnicarF_2021", "country", ["GBR", "USA"]),
            ("BritoIL_2016", "location", ["village_1", "village_5"]), ("LiuW_2016", "non_westernized", ["yes", "no"])]
    for s, col, lv in subs:
        if s not in P: continue
        x, md = P[s]["sc"], P[s]["md"]
        for a_ in lv:
            for b_ in lv:
                if a_ != b_: stress("subsite", f"{s}:{a_}>{b_}", s, x[(md[col] == a_).values], s, x[(md[col] == b_).values])
    sp = {s: (P[s]["sc"][P[s]["md"].strict_person.values], country(P[s]["md"])) for s in populations(d, strict=True) if s in P}
    for a_ in sp:
        for b_ in sp:
            if a_ != b_ and sp[a_][1] == sp[b_][1] and len(sp[a_][0]) >= 60 and len(sp[b_][0]) >= 60:
                stress("neighbour", f"{a_}>{b_}", a_, sp[a_][0], b_, sp[b_][0])
    print(d, m, "done", len(rows), flush=True)
    return rows
def cc_job(a):
    d, m = a; rows = []; cc = []
    if d == "CRC":
        X, y, g, M = load("CRC"); dv = np.isin(g, DEV_CRC); pp = Pipeline(m).fit(X.values[dv], y[dv], g[dv])
        for c in LOCKED_CRC: cc.append((c, np.quantile(pp.oof[pp.y == 0], 1 - A), pp.score(X.values[g == c]), y[g == c]))
    else:
        X, y, g, M = load(d)
        for c in np.unique(g):
            pp = Pipeline(m).fit(X.values[g != c], y[g != c], g[g != c]); cc.append((c, np.quantile(pp.oof[pp.y == 0], 1 - A), pp.score(X.values[g == c]), y[g == c]))
    for c, t0, sc, yy in cc:
        s0, s1 = sc[yy == 0], sc[yy == 1]; rng = np.random.default_rng(zlib.crc32(f"cc{d}{m}{c}".encode()))
        for N in [25, 50, 100, 200]:
            for pi, pimax in [(0.01, 0.01), (0.05, 0.05), (0.10, 0.10), (0.05, 0.01), (0.0, 0.0)]:
                n1 = int(round(N * pi)); n0 = N - n1
                if n0 + 15 > len(s0) or n1 + 5 > len(s1): continue
                for rep in range(R):
                    p0, p1 = rng.permutation(len(s0)), rng.permutation(len(s1))
                    b = np.r_[s0[p0[:n0]], s1[p1[:n1]]]; e0, e1 = s0[p0[n0:]], s1[p1[n1:]]; beta = A * (1 - pimax)
                    for meth, t in [("SRC", t0), ("BURN", thr(b, k_conf(N, beta))), ("BURN-PAC", thr(b, k_pac(N, beta))),
                                    ("LAB", thr(s0[p0[:N]], k_conf(N, A)) if N + 15 <= len(s0) else np.nan)]:
                        if np.isnan(t): continue
                        rows.append((d, m, c, N, pi, pimax, meth, rep, np.mean(e0 >= t), np.mean(e1 >= t)))
    print("cc", d, m, "done", flush=True); return rows
if __name__ == "__main__":
    fh, fc = os.path.join(OUT, "deploy_v4_healthy.csv.gz"), os.path.join(OUT, "deploy_v4_cc.csv.gz")
    assert not os.path.exists(fh), "already run"
    jobs = [(d, m) for d in ["CRC", "IBD", "T2D"] for m in ["lasso", "rf"]]
    with Pool(4) as Pp:
        h = Pp.map_async(job, jobs); c = Pp.map_async(cc_job, jobs); h, c = h.get(), c.get()
    pd.DataFrame([r for x in h for r in x], columns=["design", "disease", "model", "unit", "pop_burn", "pop_eval", "N", "method", "rep", "fpr"]).to_csv(fh, index=False)
    pd.DataFrame([r for x in c for r in x], columns=["disease", "model", "pop", "N", "pi", "pimax", "method", "rep", "fpr", "sens"]).to_csv(fc, index=False)
