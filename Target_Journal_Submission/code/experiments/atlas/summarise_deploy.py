import sys, numpy as np, pandas as pd
from scipy import stats
w = sys.argv[1]; o = pd.read_csv(f"results/deploy_{w}.csv.gz"); A = 0.10
def k_conf(N, beta): return int(np.ceil((N + 1) * (1 - beta)))
per = o.groupby(["kind", "disease", "model", "pop", "N", "pi", "pimax", "method"]).agg(
    mad=("fpr", lambda x: np.mean(abs(x - A))), p15=("fpr", lambda x: np.mean(x > .15)), p10=("fpr", lambda x: np.mean(x > A)),
    fpr=("fpr", "mean"), sens=("sens", "mean")).reset_index()
per.to_csv(f"results/deploy_{w}_perpop.csv", index=False)
s = per.groupby(["kind", "N", "pi", "pimax", "method"]).agg(pops=("pop", "size"), mad=("mad", "mean"), p15=("p15", "mean"), p10=("p10", "mean"),
                                                           fpr=("fpr", "mean"), sens=("sens", "mean")).reset_index()
# exact law of the evaluated FPR for BURN at pi=0: count above threshold among M eval ~ BetaBinomial(M, N+1-k, k)
cnt = o[(o.kind == "healthy")].groupby(["disease", "model", "pop"]).rep.size()
def pred(row):
    if row.method != "BURN" or row.pimax != 0 or row.kind != "healthy": return np.nan
    k = k_conf(row.N, A); M = row.M
    return stats.betabinom.sf(np.floor(0.15 * M), M, row.N + 1 - k, k)
sizes = o[o.kind == "healthy"].groupby(["disease", "model", "pop"]).size()
per["M"] = np.nan
H = pd.read_csv("results/atlas_rows.csv.gz").groupby(["disease", "model", "study"]).size()
per.loc[per.kind == "healthy", "M"] = [H[(d, m, p)] - N for d, m, p, N in per.loc[per.kind == "healthy", ["disease", "model", "pop", "N"]].values]
per["pred_p15"] = per.apply(pred, axis=1)
s = s.merge(per.groupby(["kind", "N", "pi", "pimax", "method"]).pred_p15.mean().reset_index(), on=["kind", "N", "pi", "pimax", "method"])
per.to_csv(f"results/deploy_{w}_perpop.csv", index=False)
pd.set_option("display.width", 200); print(s.round(3).to_string()); s.to_csv(f"results/deploy_{w}_summary.csv", index=False)
