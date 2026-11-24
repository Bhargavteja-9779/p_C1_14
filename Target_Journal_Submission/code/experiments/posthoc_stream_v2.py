"""POST HOC P3b (revision 3): no-resampling evaluation, improved.
(a) Random order: held-out sites with >= 100 controls, batches of 25/month, cases at 1%/5%, FPR on not-yet-seen controls.
(b) Batch-ordered (real site drift): MetaCardis streamed country by country (DNK -> FRA -> DEU and all 6 orders),
    T2D classifier from the frozen run, FPR measured on not-yet-seen controls of the CURRENT country.
Methods: source, local quantile, prevalence-bounded (+ high-confidence), verified-positive (+ high-confidence; delta = 0.10)."""
import sys, os, itertools, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src import calibrate as C
from src.data import load
items = list(np.load(os.path.join(H, "final", "results", "scores.npz"), allow_pickle=True)["items"])
rng = np.random.default_rng(8); B = 25; rows = []
def run_stream(ctrl, cases_pool, s_src, y_src, pi, tag, eval_sets):
    rec = C.SequentialRecalibrator(s_src, y_src, 0.10, max(0.05, pi)); hc = C.SequentialRecalibrator(s_src, y_src, 0.10, max(0.05, pi), delta=0.10)
    U = []; t_src = C.source_threshold(s_src, y_src, 0.10); cp = list(cases_pool)
    for month in range(1, len(ctrl) // B + 1):
        fut = eval_sets(month)
        if fut is None or len(fut) < 20: break
        cb = ctrl[(month - 1) * B: month * B]; n1 = min(rng.binomial(B, pi), len(cp)); cs = np.array([cp.pop() for _ in range(n1)])
        u = np.concatenate([cb, cs]); lab = np.r_[np.zeros(len(cb)), np.ones(len(cs))]
        pool = np.concatenate(U) if U else None; pm = max(0.05, pi)
        th = dict(source=t_src, local_q=np.quantile(pool, 0.9) if U else t_src, contam=C.contam_quantile(pool, 0.1, pm) if U else t_src,
                  contam_hc=C.contam_quantile_hc(pool, 0.1, pm) if U else t_src, vp=rec.t, vp_hc=hc.t)
        for k, t in th.items(): rows.append(dict(tag=tag, pi=pi, month=month, method=k, fpr_future=(fut >= t).mean()))
        rec.update(u, lab); hc.update(u, lab); U.append(u)
for disease, site, model, s_src, y_src, st, yt in items:
    P0, P1 = st[yt == 0], st[yt == 1]
    if len(P0) < 100: continue
    for pi in [0.01, 0.05]:
        for r in range(200):
            c = rng.permutation(P0)
            run_stream(c, rng.permutation(P1), s_src, y_src, pi, f"random|{disease}|{site}|{model}", lambda mth, c=c: c[mth * B:] if len(c) - mth * B >= 40 else None)
# (b) MetaCardis by country (T2D classifier)
X, y, g, M = load("T2D"); mc = M[g == "MetaCardis_2020_a"].country.values
for model in ["lasso", "rf"]:
    it = [i for i in items if i[0] == "T2D" and i[1] == "MetaCardis_2020_a" and i[2] == model][0]; s_src, y_src, st, yt = it[3], it[4], it[5], it[6]
    for order in itertools.permutations(["DNK", "FRA", "DEU"]):
        for r in range(50):
            seq, cty = [], []
            for c_ in order:
                cc = rng.permutation(st[(yt == 0) & (mc == c_)]); seq.append(cc); cty += [c_] * len(cc)
            ctrl = np.concatenate(seq); cty = np.array(cty)
            def ev(mth, ctrl=ctrl, cty=cty):
                i = mth * B
                if i >= len(ctrl): return None
                cur = cty[min(i, len(ctrl) - 1)]; idx = np.arange(len(ctrl)); m_ = (cty == cur) & (idx >= i)
                return ctrl[m_] if m_.sum() >= 20 else ctrl[(cty == cur)]
            run_stream(ctrl, rng.permutation(st[yt == 1]), s_src, y_src, 0.05, f"country|{'-'.join(order)}|{model}", ev)
d = pd.DataFrame(rows); d.to_csv(os.path.join(H, "addendum_results", "posthoc_stream_v2.csv.gz"), index=False)
d["over"] = d.fpr_future > 0.12; d["kind"] = d.tag.str.split("|").str[0]; d["site"] = d.tag.str.split("|").str[2]
L = d[d.month >= 3]
print("random order, per site:"); print(L[L.kind == "random"].groupby(["site", "method"]).agg(fpr=("fpr_future", "mean"), p=("over", "mean")).round(3).unstack("method").to_string())
print("months per site:", L[L.kind == "random"].groupby("site").month.max().to_dict())
print("\ncountry-ordered MetaCardis (T2D test):"); print(L[L.kind == "country"].groupby("method").agg(fpr=("fpr_future", "mean"), p=("over", "mean")).round(3).to_string())
