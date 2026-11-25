"""POST-HOC / EXPLORATORY analyses requested in review round 2 (after locked results and round-1 post-hoc results).
F    fair per-site feature standardisation: training cohorts standardised on their CONTROLS only (the round-1 version
     used cases + controls in training but a control pool in the target). Locked tasks, pool = control half
     (pi 0) or with K ~ Binomial(n, 0.05) cases; 200 splits.
E2b  pool size with a FIXED evaluation set: in each (task, cohort) with >= 150 controls, 200 times hold out half of
     controls and cases for evaluation; draw the pool (5% binomial cases) from the other half at n in {25, 50, 75} (all
     cohorts) and {100, 150, 200, 300} where available. 'oracle' = (1 - alpha) quantile of all the cohort's controls,
     evaluated on the same half: its exceedance is the evaluation-noise floor.
E3b  pool from another cohort WITH a same-model, same-size reference pool from the target cohort itself (50 splits).
E6   time drift, HMP_2019_ibdmdb (27 control subjects, repeated samples over ~400 days): subjects split in halves;
     pool = control samples from days 0-120 of half 1; evaluate on half 2 at days 0-120 (same period) and at days
     > 180 (later period). Model trained on the other IBD cohorts. 200 subject splits.
Usage: python explore_r2.py <model> <F|E2b|E3b|E6>
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC
from src.models import train_and_score, train_and_score_featstd
from src import calibrate as C

model, exp = sys.argv[1], sys.argv[2]
rng = np.random.default_rng({"F": 21, "E2b": 22, "E3b": 23, "E6": 26}[exp])
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{exp}_{model}.csv")
ALPHAS = [0.10, 0.05]
RULES = lambda s_src, y_src, a, u: dict(source=C.source_threshold(s_src, y_src, a), local_q=C.local_quantile(s_src, y_src, a, u=u),
                                        rpoolmean=C.robust_pool_mean(s_src, y_src, a, u=u, pi_max=0.05),
                                        rpool=C.robust_pool(s_src, y_src, a, u=u, delta=0.10, pi_max=0.05))
def ev(rows, base, ths, e0, e1):
    for k, t in ths.items():
        rows.append(dict(base, method=k, abstain=bool(np.isinf(t)), fpr=(e0 >= t).mean(), sens=(e1 >= t).mean() if len(e1) else np.nan))

def locked_tasks():
    X, y, g, _ = load("CRC", DEV_CRC + LOCKED_CRC)
    for s in LOCKED_CRC: yield "CRC", s, X.values, y, g, np.isin(g, DEV_CRC), g == s
    for dis in ["IBD", "T2D", "adenoma"]:
        X, y, g, _ = load(dis)
        for s in DISEASES[dis]["studies"]: yield dis, s, X.values, y, g, g != s, g == s

rows = []
if exp == "F":
    for dis, s, X, y, g, tr, te in locked_tasks():
        out = {}
        for ref in ("all", "controls"):
            out[ref] = train_and_score_featstd(X, y, g, tr, te, model, ref=ref)
        yt = y[te]; i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        for r in range(200):
            p0, p1 = rng.permutation(i0), rng.permutation(i1)
            c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
            for pi in (0.0, 0.05):
                n = len(c0); K = min(rng.binomial(n, pi), len(c1)); pool = np.concatenate([c0[: n - K], c1[:K]])
                for a in ALPHAS:
                    for ref, (f_src, fy_src, scorer) in out.items():
                        t = C.source_threshold(f_src, fy_src, a)
                        rows.append(dict(disease=dis, cohort=s, model=model, rep=r, pi=pi, alpha=a, method=f"featstd_{ref}",
                                         fpr=(scorer(pool, e0) >= t).mean(), sens=(scorer(pool, e1) >= t).mean(), abstain=False))
        print(exp, model, dis, s, flush=True); pd.DataFrame(rows).to_csv(OUT, index=False)
elif exp == "E2b":
    for dis, s, X, y, g, tr, te in locked_tasks():
        yt = y[te]; i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        if len(i0) < 150: continue
        s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
        for r in range(200):
            p0, p1 = rng.permutation(i0), rng.permutation(i1)
            h0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; h1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
            for a in ALPHAS:
                oracle = np.quantile(st[i0], 1 - a)
                for n in (25, 50, 75, 100, 150, 200, 300):
                    if n > len(h0): continue
                    K = min(rng.binomial(n, 0.05), len(h1)); pool = np.concatenate([rng.permutation(h0)[: n - K], rng.permutation(h1)[:K]])
                    ths = RULES(s_src, y_src, a, st[pool]); ths["oracle"] = oracle
                    ths["ctrl10"] = C.local_controls_conformal(a, st[rng.permutation(h0)[:10]])
                    ev(rows, dict(disease=dis, cohort=s, model=model, rep=r, alpha=a, n_pool=n, k_cases=K, n_eval=len(e0)), ths, st[e0], st[e1])
        print(exp, model, dis, s, flush=True); pd.DataFrame(rows).to_csv(OUT, index=False)
elif exp == "E3b":
    for dis in ["CRC", "IBD", "T2D", "adenoma"]:
        studies = LOCKED_CRC if dis == "CRC" else DISEASES[dis]["studies"]
        X, y, g, _ = load(dis, DEV_CRC + LOCKED_CRC if dis == "CRC" else None); X = X.values
        for A in studies:
            for B in studies:
                if A == B: continue
                tr = np.isin(g, DEV_CRC) if dis == "CRC" else ~np.isin(g, [A, B]); te = np.isin(g, [A, B])
                s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
                gt, yt = g[te], y[te]
                a0 = np.where((gt == A) & (yt == 0))[0]; b0 = np.where((gt == B) & (yt == 0))[0]; b1 = np.where((gt == B) & (yt == 1))[0]
                for r in range(50):
                    pb = rng.permutation(b0); bpool, beval = pb[: len(pb) // 2], pb[len(pb) // 2:]
                    n = min(len(bpool), len(a0)); apool = rng.permutation(a0)[:n]; bpool = bpool[:n]
                    for a in ALPHAS:
                        for origin, pool in (("other cohort", apool), ("same cohort", bpool)):
                            ev(rows, dict(disease=dis, pool_from=A, cohort=B, model=model, rep=r, alpha=a, origin=origin, n_pool=n),
                               RULES(s_src, y_src, a, st[pool]), st[beval], st[b1])
                print(exp, model, dis, A, "->", B, flush=True)
        pd.DataFrame(rows).to_csv(OUT, index=False)
else:  # E6
    X, y, g, M = load("IBD", one_per_subject=False); X = X.values
    d = pd.to_numeric(M.days_from_first_collection, errors="coerce").fillna(0).values; subj = M.subject_id.values
    tr = g != "HMP_2019_ibdmdb"; te = g == "HMP_2019_ibdmdb"
    s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
    dt, yt, sj = d[te], y[te], subj[te]
    ctrl_subj = np.unique(sj[yt == 0]); case_subj = np.unique(sj[yt == 1])
    for r in range(200):
        ps, pc = rng.permutation(ctrl_subj), rng.permutation(case_subj)
        s1, s2 = ps[: len(ps) // 2], ps[len(ps) // 2:]; c2 = pc[len(pc) // 2:]
        pool = np.where((yt == 0) & np.isin(sj, s1) & (dt <= 120))[0]
        for a in ALPHAS:
            ths = RULES(s_src, y_src, a, st[pool])
            for period, msk in (("same period (days 0-120)", dt <= 120), ("later period (days > 180)", dt > 180)):
                e0 = st[(yt == 0) & np.isin(sj, s2) & msk]; e1 = st[(yt == 1) & np.isin(sj, c2) & msk]
                ev(rows, dict(disease="IBD", cohort="HMP_2019_ibdmdb", model=model, rep=r, alpha=a, period=period,
                              n_pool=len(pool), n_eval=len(e0)), ths, e0, e1)
    print(exp, model, "HMP", flush=True); pd.DataFrame(rows).to_csv(OUT, index=False)
print("FINISHED", flush=True)
