"""POST-HOC / EXPLORATORY analyses requested in review round 1 (written AFTER the locked results were seen).
Nothing here replaces the pre-registered analysis; all outputs are labelled exploratory in the manuscript.

E1  contamination with cases actually present: K ~ Binomial(n_pool, pi) cases (the locked run rounded K to 0 for small
    pools), pi in {0, .01, .02, .05, .10, .20}; ties scored both as `>= t` (locked rule) and `> t` (strict).
E2  pool size in the four large cohorts (>= 150 controls): pool of n in {25, 50, 100, 200, 300, 500} samples, rest of the
    controls / cases evaluate. Tests the sample-size rule and the strict (high-probability) version where it can act.
E3  pool from ANOTHER cohort of the same task (a different lab): pool from cohort A, evaluate in cohort B.
E5  same study, different centre: MetaCardis_2020_a (one protocol and sequencer, three centres). Pool from centre A,
    evaluate in centre B; within-centre random halves as reference. Model trained on the other T2D cohorts.
Usage: python explore_r1.py <model> <E1|E2|E3>
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC
from src.models import train_and_score
from src import calibrate as C

model, exp = sys.argv[1], sys.argv[2]
rng = np.random.default_rng({"E1": 11, "E2": 12, "E3": 13, "E5": 15}[exp])
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{exp}_{model}.csv")
ALPHAS = [0.10, 0.05]

def thresholds(s_src, y_src, alpha, u, ctrl):
    return dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                rpoolmean=C.robust_pool_mean(s_src, y_src, alpha, u=u, pi_max=0.05),
                rpool=C.robust_pool(s_src, y_src, alpha, u=u, delta=0.10, pi_max=0.05),
                ctrl10=C.local_controls_conformal(alpha, ctrl) if ctrl is not None else np.nan)

def evaluate(rows, base, s_src, y_src, u, ctrl, e0, e1):
    for alpha in ALPHAS:
        for k, t in thresholds(s_src, y_src, alpha, u, ctrl).items():
            if np.isnan(t): continue
            rows.append(dict(base, alpha=alpha, method=k, abstain=bool(np.isinf(t)), fpr=(e0 >= t).mean(),
                             fpr_strict=(e0 > t).mean(), sens=(e1 >= t).mean()))

def locked_tasks():
    X, y, g, _ = load("CRC", DEV_CRC + LOCKED_CRC)
    for s in LOCKED_CRC: yield "CRC", s, X.values, y, g, np.isin(g, DEV_CRC), g == s
    for dis in ["IBD", "T2D", "adenoma"]:
        X, y, g, _ = load(dis)
        for s in DISEASES[dis]["studies"]: yield dis, s, X.values, y, g, g != s, g == s

rows = []
if exp in ("E1", "E2"):
    for dis, s, X, y, g, tr, te in locked_tasks():
        s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
        yt = y[te]; i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
        if exp == "E1":
            for r in range(200):
                p0, p1 = rng.permutation(i0), rng.permutation(i1)
                c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
                for pi in [0.0, 0.01, 0.02, 0.05, 0.10, 0.20]:
                    # pool of fixed total size n = |c0|; K ~ Binomial(n, pi) of its members are cases
                    n = len(c0); K = min(rng.binomial(n, pi), len(c1)); pool = np.concatenate([c0[: n - K], c1[:K]])
                    evaluate(rows, dict(disease=dis, cohort=s, model=model, rep=r, pi=pi, n_pool=n, k_cases=K),
                             s_src, y_src, st[pool], st[c0[:10]] if len(c0) >= 10 else None, st[e0], st[e1])
        else:
            if len(i0) < 150: continue
            for n in [25, 50, 100, 200, 300, 500]:
                if n > len(i0) - 50: continue
                for r in range(200):
                    p0, p1 = rng.permutation(i0), rng.permutation(i1)
                    for pi in [0.0, 0.02, 0.05]:
                        K = min(rng.binomial(n, pi), len(p1) // 2)
                        pool = np.concatenate([p0[: n - K], p1[:K]]); e0 = p0[n - K:]; e1 = p1[K:]
                        evaluate(rows, dict(disease=dis, cohort=s, model=model, rep=r, pi=pi, n_pool=n, k_cases=K),
                                 s_src, y_src, st[pool], st[p0[:10]], st[e0], st[e1])
        print(exp, model, dis, s, flush=True)
        pd.DataFrame(rows).to_csv(OUT, index=False)
elif exp == "E5":
    X, y, g, M = load("T2D"); X = X.values; loc = M.location.values
    tr = g != "MetaCardis_2020_a"; te = g == "MetaCardis_2020_a"
    s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
    lt, yt = loc[te], y[te]; centres = sorted(set(lt))
    for A in centres:
        for B in centres:
            a0 = np.where((lt == A) & (yt == 0))[0]; b0 = np.where((lt == B) & (yt == 0))[0]; b1 = np.where((lt == B) & (yt == 1))[0]
            for r in range(200):
                if A == B:
                    p = rng.permutation(a0); pa, eb = p[: len(p) // 2], p[len(p) // 2:]
                else:
                    pa, eb = rng.permutation(a0)[: len(a0) // 2], b0
                evaluate(rows, dict(disease="T2D", pool_from=A, cohort=B, model=model, rep=r, pi=0.0, n_pool=len(pa), k_cases=0),
                         s_src, y_src, st[pa], None, st[eb], st[b1])
            print(exp, model, A, "->", B, flush=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
else:  # E3: pool from cohort A, evaluate in cohort B (same task); the model never saw A or B
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
                    pa = rng.permutation(a0)[: max(len(a0) // 2, 1)]
                    evaluate(rows, dict(disease=dis, pool_from=A, cohort=B, model=model, rep=r, pi=0.0, n_pool=len(pa), k_cases=0),
                             s_src, y_src, st[pa], None, st[b0], st[b1])
                print(exp, model, dis, A, "->", B, flush=True)
        pd.DataFrame(rows).to_csv(OUT, index=False)
print("FINISHED", flush=True)
