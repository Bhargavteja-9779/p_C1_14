"""POST HOC (review r18): (1) H4 with covariate-half units restricted to populations of n >= 150 (plan v4 P4(a)), the
accession design unchanged (n >= 120); (2) power of the exact one-sided binomial check (H0: FPR <= 0.15, level 0.05,
n = 100) at fixed true FPRs, which does not depend on observed atlas FPRs."""
import os, json, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "results")
u = pd.read_csv(os.path.join(R, "v5_h4_units.csv"))
rows = pd.read_csv(os.path.join(R, "atlas_rows_v5.csv.gz"), usecols=["test", "model", "study"])
n = rows.groupby(["test", "model", "study"]).size().rename("n").reset_index().rename(columns={"study": "pop"})
u = u.merge(n, on=["test", "model", "pop"], how="left")
keep = (u.design == "accession") | (u.n >= 150)
def h4(d):
    pt = d.groupby(["test", "model"]).agg(src=("src", "mean"), burn=("burn", "mean")).reset_index()
    return dict(units=int(len(d)), populations=int(d["pop"].nunique()), tests=int(len(pt)), tests_burn_better=int((pt.burn < pt.src).sum()),
                mean_src=float(pt.src.mean()), mean_burn=float(pt.burn.mean()), rel_reduction=float(1 - pt.burn.mean() / pt.src.mean()),
                wilcoxon_two_sided_p=float(stats.wilcoxon(pt.burn - pt.src).pvalue))
out = dict(H4_as_reported=h4(u), H4_cov_n_ge_150=h4(u[keep]), cov_units_dropped=int((~keep).sum()),
           cov_units_n_min=int(u[u.design != "accession"].n.min()))
N, p0, lv = 100, .15, .05; k = np.arange(N + 2); c = int(k[stats.binom.sf(k - 1, N, p0) < lv][0])
out["binomial_check"] = dict(n=N, h0_fpr=p0, level=lv, critical_count=c, power={str(p): float(stats.binom.sf(c - 1, N, p)) for p in [.20, .25, .30]})
json.dump(out, open(os.path.join(R, "posthoc_r18_checks.json"), "w"), indent=1); print(json.dumps(out, indent=1))
