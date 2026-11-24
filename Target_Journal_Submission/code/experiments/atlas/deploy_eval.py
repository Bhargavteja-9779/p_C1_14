"""Protocol v3b evaluation. usage: python deploy_eval.py dev|locked"""
import sys, numpy as np, pandas as pd, zlib, warnings; warnings.filterwarnings("ignore")
from scipy import stats
sys.path.insert(0, "."); sys.path.insert(0, "../..")
from common import *
from src.pipeline import Pipeline
A, R, DELTA = 0.10, 200, 0.05
which = sys.argv[1]; dev, lock = split(); POPS = dev if which == "dev" else lock

def k_conf(N, beta): return int(np.ceil((N + 1) * (1 - beta)))
def k_pac(N, beta, delta=DELTA):
    for k in range(1, N + 1):
        if stats.beta.sf(beta, N + 1 - k, k) <= delta: return k
    return N + 1
def thr(sorted_b, k): return sorted_b[k - 1] if k <= len(sorted_b) else np.inf

rows = []
# (a) healthy populations
r = pd.read_csv("results/atlas_rows.csv.gz"); r = r[r.study.isin(dev + lock)]
for (d, m), g in r.groupby(["disease", "model"]):
    S = {s: x.score.values for s, x in g.groupby("study")}; t0 = g.thr.iloc[0]
    for s in [p for p in POPS if p in S]:
        x = S[s]; t_atlas = np.quantile(np.concatenate([S[o] for o in S if o in POPS and o != s]), 1 - A)
        rng = np.random.default_rng(zlib.crc32(f"{d}{m}{s}".encode()))
        for N in [25, 50, 100, 200]:
            if len(x) < N + 20: continue
            for rep in range(R):
                perm = rng.permutation(len(x)); b, e = np.sort(x[perm[:N]]), x[perm[N:]]
                for meth, t in [("SRC", t0), ("ATLAS", t_atlas), ("BURN", thr(b, k_conf(N, A))), ("BURN-PAC", thr(b, k_pac(N, A)))]:
                    rows.append((which, "healthy", d, m, s, N, 0.0, 0.0, meth, rep, np.mean(e >= t), np.nan))
print("healthy done", flush=True)
# (b) contaminated pools in case-control cohorts
cc = []
if which == "locked":
    X, y, g, M = load("CRC"); dv = np.isin(g, DEV_CRC)
    p = Pipeline("lasso").fit(X.values[dv], y[dv], g[dv]); prf = Pipeline("rf").fit(X.values[dv], y[dv], g[dv])
    for c in LOCKED_CRC:
        i = g == c
        for m, pp in [("lasso", p), ("rf", prf)]:
            cc.append(("CRC", m, c, np.quantile(pp.oof[pp.y == 0], 1 - A), pp.score(X.values[i]), y[i]))
    for d in ["IBD", "T2D"]:
        X, y, g, M = load(d)
        for c in np.unique(g):
            for m in ["lasso", "rf"]:
                pp = Pipeline(m).fit(X.values[g != c], y[g != c], g[g != c])
                cc.append((d, m, c, np.quantile(pp.oof[pp.y == 0], 1 - A), pp.score(X.values[g == c]), y[g == c]))
else:
    X, y, g, M = load("CRC", DEV_CRC)
    for c in DEV_CRC[:3]:
        pp = Pipeline("lasso").fit(X.values[g != c], y[g != c], g[g != c])
        cc.append(("CRC", "lasso", c, np.quantile(pp.oof[pp.y == 0], 1 - A), pp.score(X.values[g == c]), y[g == c]))
for d, m, c, t0, sc, yy in cc:
    s0, s1 = sc[yy == 0], sc[yy == 1]; rng = np.random.default_rng(zlib.crc32(f"cc{d}{m}{c}".encode()))
    for N in [25, 50, 100, 200]:
        for pi, pimax in [(0.01, 0.01), (0.05, 0.05), (0.10, 0.10), (0.05, 0.01), (0.0, 0.0)]:
            n1 = int(round(N * pi)); n0 = N - n1
            if n0 + 15 > len(s0) or n1 + 5 > len(s1): continue
            for rep in range(R):
                p0, p1 = rng.permutation(len(s0)), rng.permutation(len(s1))
                b = np.sort(np.r_[s0[p0[:n0]], s1[p1[:n1]]]); e0, e1 = s0[p0[n0:]], s1[p1[n1:]]
                beta = A * (1 - pimax)
                for meth, t in [("SRC", t0), ("BURN", thr(b, k_conf(N, beta))), ("BURN-PAC", thr(b, k_pac(N, beta))),
                                ("LAB", thr(np.sort(s0[p0[:N]]), k_conf(N, A)) if N + 15 <= len(s0) else np.nan)]:
                    if np.isnan(t): continue
                    rows.append((which, "casecontrol", d, m, c, N, pi, pimax, meth, rep, np.mean(e0 >= t), np.mean(e1 >= t)))
print("cc done", flush=True)
o = pd.DataFrame(rows, columns=["set", "kind", "disease", "model", "pop", "N", "pi", "pimax", "method", "rep", "fpr", "sens"])
o.to_csv(f"results/deploy_{which}.csv.gz", index=False)
