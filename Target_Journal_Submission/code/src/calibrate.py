"""Operating-point (threshold) transfer methods.
Inputs: source out-of-fold scores (s_src, y_src) on a logit scale, unlabeled target scores u, target FPR alpha.
Each method returns a threshold t (predict positive if score >= t)."""
import numpy as np
from scipy import stats, optimize

def source_threshold(s_src, y_src, alpha, **kw):
    return np.quantile(s_src[y_src == 0], 1 - alpha)

def local_quantile(s_src, y_src, alpha, u=None, **kw):
    """Assume the unlabeled target pool is all controls."""
    return np.quantile(u, 1 - alpha)

def local_controls_conformal(alpha, c):
    """Split-conformal / order-statistic threshold from n labelled local controls c: E[FPR] <= alpha."""
    c = np.sort(c); n = len(c); k = int(np.ceil((n + 1) * (1 - alpha)))
    return c[k - 1] if k <= n else np.inf

def _kde(x, bw=None):
    return stats.gaussian_kde(x, bw_method=bw)

def em_label_shift(s_src, y_src, alpha, u=None, **kw):
    """Saerens et al. (2002) EM prior adjustment: class-conditional score densities assumed equal to source;
    only prevalence changes. Threshold from implied target control CDF = source control CDF -> same as source threshold.
    Implemented as: estimate pi, then t solving (F_mix_u(t) - pi*F1_src(t))/(1-pi) = 1-alpha."""
    f0, f1 = _kde(s_src[y_src == 0]), _kde(s_src[y_src == 1])
    d0, d1 = f0(u), f1(u); pi = 0.5
    for _ in range(200):
        r = pi * d1 / (pi * d1 + (1 - pi) * d0 + 1e-300); pi_new = r.mean()
        if abs(pi_new - pi) < 1e-6: break
        pi = pi_new
    s1 = np.sort(s_src[y_src == 1]); us = np.sort(u)
    grid = np.unique(np.concatenate([us, s1]))
    Fu = np.searchsorted(us, grid, side="right") / len(us); F1 = np.searchsorted(s1, grid, side="right") / len(s1)
    F0 = np.clip((Fu - pi * F1) / max(1 - pi, 1e-6), 0, 1)
    idx = np.argmax(F0 >= 1 - alpha) if (F0 >= 1 - alpha).any() else len(grid) - 1
    return grid[idx]

def site_shift(s_src, y_src, alpha, u=None, return_params=False, **kw):
    """Site-shift mixture model (ours, v1): target score = a + b * (source-equivalent score); class-conditional shapes
    transported from source; estimate (a, log b, logit pi) by maximum likelihood on unlabeled target scores.
    Threshold = a + b * t_src."""
    f0, f1 = _kde(s_src[y_src == 0]), _kde(s_src[y_src == 1])
    t_src = np.quantile(s_src[y_src == 0], 1 - alpha)
    def nll(p):
        a, lb, lp = p; b = np.exp(lb); pi = 1 / (1 + np.exp(-lp))
        z = (u - a) / b
        return -np.sum(np.log((1 - pi) * f0(z) + pi * f1(z) + 1e-300) - lb)
    best = None
    for lp0 in (-3.0, 0.0):
        for a0 in (np.median(u) - np.median(s_src[y_src == 0]), 0.0):
            r = optimize.minimize(nll, x0=[a0, 0.0, lp0], method="Nelder-Mead", options=dict(maxiter=2000, xatol=1e-4, fatol=1e-6))
            if best is None or r.fun < best.fun: best = r
    a, lb, lp = best.x; b = np.exp(lb)
    t = a + b * t_src
    return (t, dict(a=a, b=b, pi=1 / (1 + np.exp(-lp)))) if return_params else t


# ---------------- Round 2 additions (D6 log, 2026-11-24) ----------------
def _thr_from_F0(grid, F0, alpha):
    ok = F0 >= 1 - alpha
    return grid[np.argmax(ok)] if ok.any() else grid[-1]

def mlls_bcts(s_src, y_src, alpha, u=None, **kw):
    """Alexandari et al. (2020): bias-corrected temperature scaling on source OOF scores, then MLLS (EM) prior
    estimation on target; threshold via implied control CDF (mixture deconvolution with source case CDF)."""
    def nll(p):
        T, b0, b1 = p; z = s_src / np.exp(T) + np.where(y_src == 1, 0, 0)
        lo = np.stack([np.zeros_like(z) + b0, z + b1], 1)
        lo -= lo.max(1, keepdims=True); lp = lo - np.log(np.exp(lo).sum(1, keepdims=True))
        return -lp[np.arange(len(y_src)), y_src].sum()
    T, b0, b1 = optimize.minimize(nll, [0.0, 0.0, 0.0], method="Nelder-Mead").x
    p1 = 1 / (1 + np.exp(-(u / np.exp(T) + b1 - b0)))
    ps = y_src.mean(); pi = ps
    for _ in range(500):
        w1 = pi / ps * p1; w0 = (1 - pi) / (1 - ps) * (1 - p1); r = w1 / (w1 + w0)
        if abs(r.mean() - pi) < 1e-7: break
        pi = r.mean()
    return _deconv_threshold(s_src, y_src, u, pi, alpha)

def _deconv_threshold(s_src, y_src, u, pi, alpha):
    s1 = np.sort(s_src[y_src == 1]); us = np.sort(u); grid = np.unique(np.concatenate([us, s1]))
    Fu = np.searchsorted(us, grid, side="right") / len(us); F1 = np.searchsorted(s1, grid, side="right") / len(s1)
    F0 = np.maximum.accumulate(np.clip((Fu - pi * F1) / max(1 - pi, 1e-6), 0, 1))
    return _thr_from_F0(grid, F0, alpha)

def dys(s_src, y_src, alpha, u=None, bins=20, **kw):
    """DyS quantification (Maletzke et al. 2019): pi minimising topsoe distance between target score histogram and
    mixture of source class histograms; threshold by deconvolution."""
    e = np.quantile(np.concatenate([s_src, u]), np.linspace(0, 1, bins + 1)); e[0] -= 1e-9; e[-1] += 1e-9
    h = lambda x: np.histogram(x, e)[0] / len(x) + 1e-6
    h0, h1, hu = h(s_src[y_src == 0]), h(s_src[y_src == 1]), h(u)
    def tops(pi):
        m = (1 - pi) * h0 + pi * h1
        return np.sum(m * np.log(2 * m / (m + hu)) + hu * np.log(2 * hu / (m + hu)))
    pi = optimize.minimize_scalar(tops, bounds=(0, 1), method="bounded").x
    return _deconv_threshold(s_src, y_src, u, pi, alpha)

def gauss2(s_src, y_src, alpha, u=None, **kw):
    """Unsupervised 2-Gaussian calibration (Brummer & Garcia-Romero 2014 style): fit a 2-component Gaussian mixture to
    target scores (EM, init from source class moments); threshold = control component quantile."""
    m = [s_src[y_src == 0].mean(), s_src[y_src == 1].mean()]; v = [s_src[y_src == 0].var(), s_src[y_src == 1].var()]
    pi = 0.3
    for _ in range(300):
        d0 = (1 - pi) * stats.norm.pdf(u, m[0], np.sqrt(v[0])); d1 = pi * stats.norm.pdf(u, m[1], np.sqrt(v[1]))
        r = d1 / (d0 + d1 + 1e-300); pi = np.clip(r.mean(), 1e-3, 0.999)
        w0, w1 = 1 - r, r
        m = [np.sum(w0 * u) / w0.sum(), np.sum(w1 * u) / max(w1.sum(), 1e-9)]
        v = [max(np.sum(w0 * (u - m[0]) ** 2) / w0.sum(), 1e-3), max(np.sum(w1 * (u - m[1]) ** 2) / max(w1.sum(), 1e-9), 1e-3)]
        if m[1] < m[0]: m, v, pi = m[::-1], v[::-1], 1 - pi
    return stats.norm.ppf(1 - alpha, m[0], np.sqrt(v[0]))

class _FastKDE:
    """Gaussian KDE tabulated on a fine grid + linear interpolation (zero outside a padded range). ~100x faster."""
    def __init__(self, x, n=2048):
        k = stats.gaussian_kde(x); sd = np.sqrt(k.covariance[0, 0])
        self.g = np.linspace(x.min() - 6 * sd, x.max() + 6 * sd, n); self.d = k(self.g)
    def __call__(self, z): return np.interp(z, self.g, self.d, left=0.0, right=0.0)

def site_shift_v2(s_src, y_src, alpha, u=None, c=None, return_params=False, lb_bound=1.0, **kw):
    """Site-shift mixture with (i) bounded log-scale |log b|<=lb_bound (fixes overflow / degenerate fits),
    (ii) optional labelled local controls c entering the likelihood as known class-0 points (hybrid)."""
    f0, f1 = _FastKDE(s_src[y_src == 0]), _FastKDE(s_src[y_src == 1])
    t_src = np.quantile(s_src[y_src == 0], 1 - alpha)
    c = np.asarray([] if c is None else c, float)
    def nll(p):
        a, lb, lp = p; lb = lb_bound * np.tanh(lb / lb_bound); b = np.exp(lb); pi = 1 / (1 + np.exp(-np.clip(lp, -30, 30)))
        z = (u - a) / b; out = -np.sum(np.log((1 - pi) * f0(z) + pi * f1(z) + 1e-300) - lb)
        if len(c): out -= np.sum(np.log(f0((c - a) / b) + 1e-300) - lb)
        return out
    best = None
    for lp0 in (-3.0, 0.0):
        for a0 in (np.median(u) - np.median(s_src[y_src == 0]), 0.0):
            r = optimize.minimize(nll, x0=[a0, 0.0, lp0], method="Nelder-Mead", options=dict(maxiter=1500, xatol=1e-4, fatol=1e-6))
            if best is None or r.fun < best.fun: best = r
    a, lb, lp = best.x; b = np.exp(lb_bound * np.tanh(lb / lb_bound))
    t = a + b * t_src
    return (t, dict(a=a, b=b, pi=1 / (1 + np.exp(-lp)))) if return_params else t

def bootstrap_check(method, s_src, y_src, alpha, u, B=30, seed=0, **kw):
    """Self-check: bootstrap the unlabeled pool; return threshold and the bootstrap spread of implied source-equivalent
    FPR (abstain if spread is large)."""
    rng = np.random.default_rng(seed); s0 = np.sort(s_src[y_src == 0])
    t = method(s_src, y_src, alpha, u=u, **kw); tb = [method(s_src, y_src, alpha, u=rng.choice(u, len(u)), **kw) for _ in range(B)]
    return t, float(np.std(tb))
