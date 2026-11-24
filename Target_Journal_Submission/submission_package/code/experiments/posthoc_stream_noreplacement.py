"""POST HOC P3: prospective-style evaluation WITHOUT resampling. At each locked site with >= 100 controls, controls are
streamed once in random order (batches of 50/month); cases are inserted at prevalence pi (drawn without replacement
while available). After each month the cut-off is applied to the controls NOT YET SEEN (true future controls).
Also reports burn-in cost. Scores from the frozen final run (results/scores.npz)."""
import sys, os, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src import calibrate as C
items = list(np.load(os.path.join(H, "final", "results", "scores.npz"), allow_pickle=True)["items"])
rng = np.random.default_rng(7); rows = []; B = 50; R = 300
for disease, site, model, s_src, y_src, st, yt in items:
    P0, P1 = st[yt == 0], st[yt == 1]
    if len(P0) < 100: continue
    for pi in [0.01, 0.05]:
        for r in range(R):
            c_order = rng.permutation(P0); case_pool = list(rng.permutation(P1))
            t_src = C.source_threshold(s_src, y_src, 0.10)
            rec = C.SequentialRecalibrator(s_src, y_src, 0.10, max(0.05, pi)); U = []
            rec_hc = C.SequentialRecalibrator(s_src, y_src, 0.10, max(0.05, pi), delta=0.10)
            n_months = (len(P0) - 40) // B          # keep >= 40 unseen controls for evaluation
            for month in range(1, n_months + 1):
                seen = month * B; future = c_order[seen:]
                ctrl_batch = c_order[seen - B: seen]
                n1 = rng.binomial(B, pi); cases = np.array([case_pool.pop() for _ in range(min(n1, len(case_pool)))])
                u = np.concatenate([ctrl_batch, cases]); lab = np.r_[np.zeros(len(ctrl_batch)), np.ones(len(cases))]
                th = dict(source=t_src, vp=rec.t, vp_hc=rec_hc.t, local_q=np.quantile(np.concatenate(U), 0.9) if U else t_src,
                          contam=C.contam_quantile(np.concatenate(U), 0.10, max(0.05, pi)) if U else t_src)
                for k, t in th.items():
                    rows.append(dict(disease=disease, site=site, model=model, pi=pi, rep=r, month=month, method=k,
                                     fpr_future=(future >= t).mean(), n_future=len(future)))
                rec.update(u, lab); rec_hc.update(u, lab); U.append(u)
d = pd.DataFrame(rows); d.to_csv(os.path.join(H, "addendum_results", "posthoc_stream_noreplacement.csv.gz"), index=False)
d["over"] = d.fpr_future > 0.12
late = d[d.month >= 3]
print("sites:", d.groupby(["disease", "site"]).n_future.max().to_dict())
print(late.groupby(["pi", "method"]).agg(fpr=("fpr_future", "mean"), p_over=("over", "mean")).round(3).unstack("method").to_string())
print(late.groupby(["site", "method"]).fpr_future.mean().round(3).unstack().to_string())
d["sens_proxy_t"] = 0
print("month 1:", d[d.month == 1].groupby("method").fpr_future.mean().round(3).to_dict())
