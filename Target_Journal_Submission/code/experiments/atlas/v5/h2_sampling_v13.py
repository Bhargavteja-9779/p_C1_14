"""POST HOC (review round 11, M3): split the H2 residual (test x population pair) into binomial sampling noise and true
pair-specific variance. Sampling variance of the empirical logit = 1/(k+.5) + 1/(n-k+.5), averaged over units.
Writes results/h2_sampling_v13.json."""
import os, json, numpy as np, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); s = json.load(open(os.path.join(R, "v5_summary.json")))
p = pd.read_csv(os.path.join(R, "v5_perpop_strict.csv")); o = {}
for m in ["lasso", "rf"]:
    h = s[f"H2_strict_{m}"]; d = p[p.model == m]; sv = float((1 / (d.k + .5) + 1 / (d.n - d.k + .5)).mean())
    tot = h["var_test"] + h["var_pop"] + h["var_resid"]; pair = max(0.0, h["var_resid"] - sv)
    o[m] = dict(test_share=h["var_test"] / tot, pop_share=h["var_pop"] / tot, resid_share=h["var_resid"] / tot, sampling_var=sv,
                sampling_share=min(sv, h["var_resid"]) / tot, pair_share_net=pair / tot,
                net_shares=dict(test=h["var_test"] / (tot - min(sv, h["var_resid"])), pop=h["var_pop"] / (tot - min(sv, h["var_resid"])), pair=pair / (tot - min(sv, h["var_resid"]))))
json.dump(o, open(os.path.join(R, "h2_sampling_v13.json"), "w"), indent=1); print(json.dumps(o, indent=1))
