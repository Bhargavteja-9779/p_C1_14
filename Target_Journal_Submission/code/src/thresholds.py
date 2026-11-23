"""Operating-point (decision threshold) transfer methods, v2 (RECHECK).

Every method receives source out-of-fold scores (s_src, y_src) on the logit scale, a target false-positive rate alpha and,
depending on the method, an unlabeled target pool u, a prevalence pi, or n labelled target controls c.
Every method returns a threshold t: predict positive if score >= t.
"""
import numpy as np
from scipy import stats, optimize


class _Dens:
    """Gaussian KDE tabulated on a grid for fast repeated evaluation."""
    def __init__(self, x):
        k = stats.gaussian_kde(x); bw = k.factor * x.std(ddof=1)
        self.g = np.linspace(x.min() - 6 * bw, x.max() + 6 * bw, 4096); self.d = k(self.g)
    def __call__(self, z):
        return np.interp(z, self.g, self.d, left=0.0, right=0.0)


def source(s_src, y_src, alpha, **kw):
    """M0: status quo - threshold set on source (out-of-fold) controls."""
    return float(np.quantile(s_src[y_src == 0], 1 - alpha))


def local_quantile(s_src, y_src, alpha, u, **kw):
    """M1: (1-alpha) quantile of the unlabeled target pool (treats pool as all controls)."""
    return float(np.quantile(u, 1 - alpha))


def _subtract(u, s1, pi, alpha):
    """Threshold where the implied control CDF F0 = (F_u - pi F1_src)/(1-pi) reaches 1-alpha."""
    us, s1 = np.sort(u), np.sort(s1); grid = np.unique(np.concatenate([us, s1]))
    Fu = np.searchsorted(us, grid, side="right") / len(us); F1 = np.searchsorted(s1, grid, side="right") / len(s1)
    F0 = np.maximum.accumulate(np.clip((Fu - pi * F1) / max(1 - pi, 1e-6), 0, 1))
    ok = F0 >= 1 - alpha
    return float(grid[np.argmax(ok)] if ok.any() else grid[-1])


def em_prior(s_src, y_src, alpha, u, dens=None, return_pi=False, **kw):
    """M2: Saerens et al. (2002) EM estimate of target prevalence, then mixture subtraction."""
    f0, f1 = dens or (_Dens(s_src[y_src == 0]), _Dens(s_src[y_src == 1]))
    d0, d1 = f0(u), f1(u); pi = 0.5
    for _ in range(500):
        r = pi * d1 / (pi * d1 + (1 - pi) * d0 + 1e-300); new = r.mean()
        if abs(new - pi) < 1e-7: break
        pi = new
    t = _subtract(u, s_src[y_src == 1], pi, alpha)
    return (t, pi) if return_pi else t


def known_prev(s_src, y_src, alpha, u, pi, **kw):
    """M3: mixture subtraction with prevalence pi supplied (e.g. from epidemiology)."""
    return _subtract(u, s_src[y_src == 1], pi, alpha)


def site_shift(s_src, y_src, alpha, u, dens=None, return_params=False, **kw):
    """M4: site-shift mixture model. Target score = a + b * (source-equivalent score); class-conditional score shapes are
    transported from the source; (a, log b, logit pi) fitted by maximum likelihood on the unlabeled pool only.
    Threshold = a + b * t_src."""
    f0, f1 = dens or (_Dens(s_src[y_src == 0]), _Dens(s_src[y_src == 1]))
    t_src = np.quantile(s_src[y_src == 0], 1 - alpha)
    def nll(p):
        a, lb, lp = p; b = np.exp(lb); pi = 1 / (1 + np.exp(-lp)); z = (u - a) / b
        return -np.sum(np.log((1 - pi) * f0(z) + pi * f1(z) + 1e-300) - lb) + 0.5 * (lb / 1.0) ** 2  # weak prior on log b
    best = None
    for lp0 in (-3.0, 0.0):
        for a0 in (np.median(u) - np.median(s_src[y_src == 0]), 0.0):
            r = optimize.minimize(nll, x0=[a0, 0.0, lp0], method="Nelder-Mead",
                                  options=dict(maxiter=1500, xatol=1e-4, fatol=1e-6))
            if best is None or r.fun < best.fun: best = r
    a, lb, lp = best.x; b = np.exp(lb); t = float(a + b * t_src)
    return (t, dict(a=a, b=b, pi=1 / (1 + np.exp(-lp)))) if return_params else t


def conformal_controls(alpha, c, **kw):
    """M5: split-conformal threshold from n labelled local controls c. With k = ceil((n+1)(1-alpha)), the realised FPR on a
    new exchangeable control satisfies E[FPR] <= alpha; FPR ~ Beta(n+1-k, k) exactly (continuous scores).
    If k > n the method abstains from flagging anyone (t = +inf)."""
    c = np.sort(np.asarray(c)); n = len(c); k = int(np.ceil((n + 1) * (1 - alpha)))
    return float(c[k - 1]) if k <= n else np.inf


def conformal_fpr_tail(n, alpha, eps):
    """Exact P(FPR > alpha + eps) for the conformal threshold from n exchangeable controls (Beta law)."""
    k = int(np.ceil((n + 1) * (1 - alpha)))
    if k > n: return 0.0
    return float(stats.beta.sf(alpha + eps, n + 1 - k, k))


def prediction_alignment(s_src, y_src, alpha, u, **kw):
    """M7: Unsupervised Prediction Alignment (Roschewitz et al. 2023, Nat Commun, doi:10.1038/s41467-023-42396-y),
    score-level form: map target scores to source scores by matching their whole CDFs, then apply the source threshold.
    Equivalent threshold: t = Q_u(F_src(t_src)), F_src = CDF of all source (out-of-fold) scores. Assumes the class mix
    of the target pool equals the source's."""
    t_src = np.quantile(s_src[y_src == 0], 1 - alpha)
    q = np.mean(s_src < t_src)
    return float(np.quantile(u, q))


def between_site_tau2(s_src, y_src, g_src, alpha, B=200, seed=0):
    """Between-site variance of the (1-alpha) control quantile, from leave-one-cohort-out OOF scores of the training
    cohorts: var(q_c) minus the mean bootstrap sampling variance of q_c (method of moments, floored at 0)."""
    rng = np.random.default_rng(seed); q, v = [], []
    for c in np.unique(g_src):
        x = s_src[(g_src == c) & (y_src == 0)]
        if len(x) < 5: continue
        q.append(np.quantile(x, 1 - alpha))
        v.append(np.var([np.quantile(rng.choice(x, len(x)), 1 - alpha) for _ in range(B)]))
    return float(max(np.var(q, ddof=1) - np.mean(v), 0.0)) if len(q) >= 3 else 0.0


def shrink(t_src, tau2, x, alpha, B=200, seed=0, conformal=False):
    """M8: empirical-Bayes threshold. Local estimate t_loc from sample x (unlabeled pool or labelled controls),
    its sampling variance by bootstrap; posterior mean t = t_src + w (t_loc - t_src), w = tau2 / (tau2 + var_loc)."""
    rng = np.random.default_rng(seed); x = np.asarray(x)
    t_loc = conformal_controls(alpha, x) if conformal else np.quantile(x, 1 - alpha)
    if not np.isfinite(t_loc): t_loc = x.max()
    var = np.var([np.quantile(rng.choice(x, len(x)), 1 - alpha) for _ in range(B)])
    w = tau2 / (tau2 + var) if tau2 + var > 0 else 0.0
    return float(t_src + w * (t_loc - t_src))
