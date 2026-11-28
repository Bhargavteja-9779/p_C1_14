"""POST HOC (review r20): out-of-band share (outside 0.05-0.15) among classifiers with AUROC >= 0.65 and < 0.6 (strict set,
refit scoring), and the out-of-band share expected from binomial sampling noise alone if every true FPR were 0.10."""
import os, json, numpy as np, pandas as pd
from scipy import stats
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
p = pd.read_csv(os.path.join(R, "v5_perpop_strict.csv")); T = pd.read_csv(os.path.join(R, "tests_v5.csv"))[["test", "model", "auroc"]]
p = p.merge(T, on=["test", "model"]); oob = (p.fpr < .05) | (p.fpr > .15)
exp = float(np.mean([stats.binom.cdf(np.ceil(.05 * n) - 1, n, .1) + stats.binom.sf(np.floor(.15 * n), n, .1) for n in p.n]))
out = dict(oob_all=float(oob.mean()), oob_auroc_ge_065=float(oob[p.auroc >= .65].mean()), pairs_auroc_ge_065=int((p.auroc >= .65).sum()),
           oob_auroc_lt_06=float(oob[p.auroc < .6].mean()), expected_oob_if_true_fpr_010=exp,
           meanlogit_fold_share_below_005_all=float((pd.read_csv(os.path.join(R, "posthoc_r19_foldmodel_perpop.csv")).fpr_fold < .05).mean()))
json.dump(out, open(os.path.join(R, "posthoc_r20_numbers.json"), "w"), indent=1); print(out)
