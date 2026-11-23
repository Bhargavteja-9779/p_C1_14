"""LOCKED FINAL TEST — run ONCE, only after experiments/protocol.md says STATUS: FROZEN."""
import sys, os, numpy as np, pandas as pd, warnings
from joblib import Parallel, delayed
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from src.data import load, DEV_CRC, LOCKED_CRC, DISEASES
from src.models import train_and_score
from src import calibrate as C
sys.path.insert(0, os.path.join(HERE, "dev")); from explore_v3 import KDETruth
OUT = os.path.join(HERE, "final"); os.makedirs(OUT, exist_ok=True)
PRIOR_MEAN = dict(CRC=0.01, adenoma=0.20, IBD=0.005, T2D=0.10); STRENGTH = 10
ALPHAS, KS, PIS, MODELS = (0.10, 0.05, 0.20), (5, 10, 20), (0.0, 0.01, 0.05, 0.2, "nat"), ("lasso", "rf", "hgb")
R_REAL, R_SYN, N_POOL = 50, 100, 60
assert "STATUS: FROZEN" in open(os.path.join(HERE, "protocol.md")).read(), "protocol not frozen"

def tasks():
    out = [("CRC", DEV_CRC, t) for t in LOCKED_CRC]
    for dz in ("IBD", "T2D", "adenoma"):
        st = DISEASES[dz]["studies"]; out += [(dz, [s for s in st if s != t], t) for t in st]
    return out

def get_scores(dz, src, tgt, model):
    f = os.path.join(OUT, f"scores_{dz}_{tgt}_{model}.npz")
    if not os.path.exists(f):
        X, y, g, _ = load(dz, list(src) + [tgt]); X = X.values; tr, te = np.isin(g, src), g == tgt
        s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
        np.savez(f, s_src=s_src, y_src=y_src, g_src=g[tr], st=st, yt=y[te])
    return dict(np.load(f, allow_pickle=True))

def thresholds(T, d, al, pm, cal, u, cs):
    s_src, y_src = d["s_src"], d["y_src"]; pr = (pm, STRENGTH)
    th = dict(source=C.source_threshold(s_src, y_src, al), local_q=C.local_quantile(s_src, y_src, al, u=u),
              upa=C.upa_align(s_src, y_src, al, u=u), em=C.em_label_shift(s_src, y_src, al, u=u),
              lf_sc=T.predictive(cal[al, 0], u=u, prior=pr)[0])
    for k, c in cs.items():
        th[f"conf_{k}"] = C.local_controls_conformal(al, c); th[f"ctrlq_{k}"] = C.local_controls_quantile(al, c)
        th[f"hyb_sc_{k}"] = T.predictive(cal[al, k], c=c, u=u, prior=pr)[0]; th[f"_gof_{k}"] = T.gof_pvalue(c)
    return th

def run(dz, src, tgt, model, seed):
    d = get_scores(dz, src, tgt, model); rng = np.random.default_rng(seed); pm = PRIOR_MEAN[dz]
    T = C.PredTransport(d["s_src"], d["y_src"], seed=seed); st, yt = d["st"], d["yt"]
    cal = {(al, k): C.self_calibrate(d["s_src"], d["y_src"], d["g_src"], al, k=k, prior=(pm, STRENGTH), seed=seed)
           for al in ALPHAS for k in (0,) + KS}
    rows = []; base = dict(disease=dz, target=tgt, model=model)
    K0, K1 = KDETruth(st[yt == 0]), KDETruth(st[yt == 1]); nat = (yt == 1).mean()
    for r in range(R_SYN):                                  # semi-synthetic known truth
        for pi in PIS:
            pv = nat if pi == "nat" else pi; n1 = int(round(pv * N_POOL / (1 - pv)))
            u = np.concatenate([K0.sample(N_POOL, rng), K1.sample(n1, rng)]); cs = {k: K0.sample(k, rng) for k in KS}
            for al in (ALPHAS if pi == 0.01 else ALPHAS[:1]):
                for m, t in thresholds(T, d, al, pm, cal, u, cs).items():
                    rows.append(dict(base, bench="syn", rep=r, pi=str(pi), alpha=al, method=m,
                                     fpr=t if m[0] == "_" else K0.sf(t), sens=np.nan if m[0] == "_" else K1.sf(t)))
    i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(R_REAL):                                 # real splits
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        ks = tuple(k for k in KS if len(c0) - k >= 8)
        if not ks: break
        lab = {k: st[c0[:k]] for k in ks}; pc = c0[max(ks):]
        for pi in PIS:
            n1 = min(len(c1) if pi == "nat" else int(round(pi * len(pc) / (1 - pi))), len(c1))
            u = st[np.concatenate([pc, c1[:n1]])]
            for m, t in thresholds(T, d, 0.10, pm, cal, u, lab).items():
                rows.append(dict(base, bench="real", rep=r, pi=str(pi), alpha=0.10, method=m,
                                 fpr=t if m[0] == "_" else (st[e0] >= t).mean(), sens=np.nan if m[0] == "_" else (st[e1] >= t).mean()))
    print(dz, tgt, model, "done", flush=True)
    return rows, dict(base, **{f"alpha_prime_{al}_{k}": v for (al, k), v in cal.items()})

if __name__ == "__main__":
    J = [(dz, src, tgt, m) for dz, src, tgt in tasks() for m in MODELS]
    for dz, src, tgt, m in J: get_scores(dz, src, tgt, m)    # train sequentially (RF/HGB use all cores)
    out = Parallel(n_jobs=4)(delayed(run)(*j, 1000 + i) for i, j in enumerate(J))
    pd.DataFrame([r for o in out for r in o[0]]).to_csv(os.path.join(OUT, "final_results.csv.gz"), index=False)
    pd.DataFrame([o[1] for o in out]).to_csv(os.path.join(OUT, "final_selfcal.csv"), index=False)
