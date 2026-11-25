import math, os
import numpy as np
from scipy import stats

def burnin_k(n, alpha=0.10, pi_max=0.0):
    """Rank of the burn-in order statistic used as cut-off: k = ceil((n+1)(1 - alpha(1 - pi_max)))."""
    if not (0 < alpha < 1 and 0 <= pi_max < 1 and n >= 1): raise ValueError("need 0<alpha<1, 0<=pi_max<1, n>=1")
    return int(math.ceil((n + 1) * (1 - alpha * (1 - pi_max))))

def pac_k(n, alpha=0.10, pi_max=0.0, delta=0.05):
    """Smallest k with P(FPR > alpha(1-pi_max)) <= delta under exchangeability (order-statistic tolerance bound)."""
    beta = alpha * (1 - pi_max)
    for k in range(1, n + 1):
        if stats.beta.sf(beta, n + 1 - k, k) <= delta: return k
    return n + 1

def burnin_cutoff(scores, alpha=0.10, pi_max=0.0, pac=False, delta=0.05):
    """Cut-off from unlabelled burn-in scores (higher score = more disease-like; flag if score >= cut-off).
    Returns +inf (flag nobody) when the rule is infeasible for this n."""
    s = np.sort(np.asarray(scores, float)); s = s[np.isfinite(s)]; n = len(s)
    k = pac_k(n, alpha, pi_max, delta) if pac else burnin_k(n, alpha, pi_max)
    return float(s[k - 1]) if k <= n else float("inf")

def prob_fpr_above(level, n, k, m=None):
    """P(realised FPR > level) for healthy people exchangeable with the burn-in: Beta(n+1-k, k) law of the
    population FPR; with m evaluation people, the exact beta-binomial law of the observed share."""
    if m is None: return float(stats.beta.sf(level, n + 1 - k, k))
    return float(stats.betabinom.sf(math.floor(level * m), m, n + 1 - k, k))

def atlas_table():
    import csv
    p = os.path.join(os.path.dirname(__file__), "atlas_v5.csv")
    with open(p) as f: return list(csv.DictReader(f))

def expected_fpr_range(test, model="lasso"):
    """Random-effects pooled FPR and 95% prediction interval of the published-style cut-off (target 0.10) across
    the healthy populations of the atlas (strict set)."""
    for r in atlas_table():
        if r["test"] == test and r["model"] == model:
            return {k: (float(v) if k not in ("test", "model") else v) for k, v in r.items()}
    raise KeyError(f"{test}/{model} not in atlas; available: {sorted({r['test'] for r in atlas_table()})}")
