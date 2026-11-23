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


# ---------------------------------------------------------------------------------------------------------------
# Round 2 additions (2026-11-23): fast log-densities, more baselines, hybrid (few labelled controls + unlabelled pool)
# ---------------------------------------------------------------------------------------------------------------
class LogDens:
    """KDE log-density tabulated on a wide grid, linear extrapolation of log-density outside (Gaussian-like tails)."""
    def __init__(self, x, n=1024):
        k = stats.gaussian_kde(x); sd = x.std() + 1e-6
        self.g = np.linspace(x.min() - 6 * sd, x.max() + 6 * sd, n); self.v = k.logpdf(self.g)
        self.sl = (self.v[1] - self.v[0]) / (self.g[1] - self.g[0]); self.sr = (self.v[-1] - self.v[-2]) / (self.g[-1] - self.g[-2])
    def __call__(self, z):
        z = np.asarray(z, float); out = np.interp(z, self.g, self.v)
        lo, hi = z < self.g[0], z > self.g[-1]
        out[lo] = self.v[0] + self.sl * (z[lo] - self.g[0]); out[hi] = self.v[-1] + self.sr * (z[hi] - self.g[-1])
        return out

def local_controls_quantile(alpha, c):
    """Plain empirical (1-alpha) quantile of k labelled local controls (no finite-sample correction)."""
    return np.quantile(c, 1 - alpha)

def upa_align(s_src, y_src, alpha, u=None, **kw):
    """Roschewitz et al. 2023 (UPA)-style: match the quantile level of the source threshold in the pooled source score
    distribution to the same quantile of the unlabelled target pool (assumes unchanged prevalence)."""
    t = source_threshold(s_src, y_src, alpha); q = (s_src <= t).mean()
    return np.quantile(u, q)

def gmm2(s_src, y_src, alpha, u=None, **kw):
    """Free two-component Gaussian mixture on unlabelled target scores; lower-mean component = controls."""
    from sklearn.mixture import GaussianMixture
    g = GaussianMixture(2, random_state=0, n_init=3).fit(u.reshape(-1, 1)); j = np.argmin(g.means_.ravel())
    return g.means_.ravel()[j] + np.sqrt(g.covariances_.ravel()[j]) * stats.norm.ppf(1 - alpha)

def _fit_shift(l0, l1, c=None, u=None, x0s=None):
    """ML for (a, log b, logit pi) of the location-scale site-shift model. c: labelled local controls, u: unlabelled pool.
    Either may be None/empty. Returns (a, b, pi)."""
    has_u = u is not None and len(u) > 0; has_c = c is not None and len(c) > 0
    def nll(p):
        a, lb = p[0], np.clip(p[1], -3, 3); b = np.exp(lb); out = 0.0
        if has_c: out -= np.sum(l0((c - a) / b) - lb)
        if has_u:
            lp = np.clip(p[2], -12, 12); pi = 1 / (1 + np.exp(-lp)); z = (u - a) / b
            out -= np.sum(np.logaddexp(np.log1p(-pi) + l0(z), np.log(pi) + l1(z)) - lb)
        return out
    best = None
    for x0 in x0s:
        r = optimize.minimize(nll, x0=x0 if has_u else x0[:2], method="Nelder-Mead", options=dict(maxiter=3000, xatol=1e-4, fatol=1e-7))
        if best is None or r.fun < best.fun: best = r
    a, b = best.x[0], np.exp(np.clip(best.x[1], -3, 3)); pi = 1 / (1 + np.exp(-np.clip(best.x[2], -12, 12))) if has_u else np.nan
    return a, b, pi

class Transport:
    """Source score model reused across many target draws (densities built once)."""
    def __init__(self, s_src, y_src):
        self.s0, self.s1 = s_src[y_src == 0], s_src[y_src == 1]
        self.l0, self.l1 = LogDens(self.s0), LogDens(self.s1); self.m0 = np.median(self.s0)
    def tsrc(self, alpha): return np.quantile(self.s0, 1 - alpha)
    def starts(self, ref):
        d = np.median(ref) - self.m0
        return [[d, 0.0, -3.0], [d, 0.0, 0.0], [0.0, 0.0, -1.5]]
    def site_shift(self, alpha, u):          # v1 re-implemented with fast densities (label-free)
        a, b, pi = _fit_shift(self.l0, self.l1, u=u, x0s=self.starts(u)); return a + b * self.tsrc(alpha), (a, b, pi)
    def hybrid_controls_only(self, alpha, c):  # (a, b) from k labelled controls only; source shape gives the tail
        a, b, _ = _fit_shift(self.l0, self.l1, c=c, x0s=self.starts(c)); return a + b * self.tsrc(alpha), (a, b, np.nan)
    def hybrid(self, alpha, c, u):           # ours v2: controls anchor (a, b), the unlabelled pool adds information
        a, b, pi = _fit_shift(self.l0, self.l1, c=c, u=u, x0s=self.starts(c)); return a + b * self.tsrc(alpha), (a, b, pi)


# Round 2b: predictive (uncertainty-averaged) thresholds. Plug-in ML of (a, b) from few controls under-estimates the
# spread -> FPR above target. We average the tail probability over a Laplace approximation of the (a, log b) posterior.
def _num_hess(f, x, h=1e-3):
    x = np.asarray(x, float); n = len(x); H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            e_i, e_j = np.eye(n)[i] * h, np.eye(n)[j] * h
            H[i, j] = H[j, i] = (f(x + e_i + e_j) - f(x + e_i - e_j) - f(x - e_i + e_j) + f(x - e_i - e_j)) / (4 * h * h)
    return H

class PredTransport(Transport):
    def __init__(self, s_src, y_src, n_draw=400, seed=0):
        super().__init__(s_src, y_src)
        h = 1.06 * self.s0.std() * len(self.s0) ** -0.2; g = np.linspace(self.s0.min() - 8 * h - 5, self.s0.max() + 8 * h + 5, 2048)
        self.gs, self.sf = g, stats.norm.sf((g[:, None] - self.s0[None, :]) / h).mean(1)   # smoothed source control survival
        self.rng = np.random.default_rng(seed); self.n_draw = n_draw
    def S0(self, z): return np.interp(z, self.gs, self.sf, left=1.0, right=0.0)
    def _nll(self, c, u, pi_fixed=None, prior=None):
        """prior=(m, n): Beta prior on pi with mean m and strength n (pseudo-samples), e.g. deployment prevalence."""
        l0, l1 = self.l0, self.l1
        def f(p):
            a, lb = p[0], np.clip(p[1], -3, 3); b = np.exp(lb); out = 0.0
            if c is not None and len(c): out -= np.sum(l0((c - a) / b) - lb)
            if u is not None and len(u):
                if pi_fixed is None: pi = 1 / (1 + np.exp(-np.clip(p[2], -12, 12)))
                else: pi = pi_fixed
                z = (u - a) / b
                out -= np.sum(np.logaddexp(np.log1p(-pi) + l0(z), np.log(max(pi, 1e-12)) + l1(z)) - lb)
                if prior is not None and pi_fixed is None:
                    m, n = prior; out -= (m * n) * np.log(pi) + ((1 - m) * n) * np.log1p(-pi)
            return out
        return f
    def predictive(self, alpha, c=None, u=None, pi_fixed=None, prior=None):
        free_pi = u is not None and len(u) and pi_fixed is None
        f = self._nll(c, u, pi_fixed, prior); ref = c if c is not None and len(c) else u
        best = None
        for x0 in self.starts(ref):
            x0 = x0 if free_pi else x0[:2]
            r = optimize.minimize(f, x0=x0, method="Nelder-Mead", options=dict(maxiter=3000, xatol=1e-5, fatol=1e-8))
            if best is None or r.fun < best.fun: best = r
        x = best.x; H = _num_hess(f, x)
        try:
            cov = np.linalg.inv(H + 1e-6 * np.eye(len(x)))
            if not np.all(np.linalg.eigvalsh(cov) > 0): raise np.linalg.LinAlgError
            D = self.rng.multivariate_normal(x, cov, self.n_draw)
        except np.linalg.LinAlgError:
            D = np.tile(x, (self.n_draw, 1))
        a, b = D[:, 0], np.exp(np.clip(D[:, 1], -3, 3))
        fpr = lambda t: self.S0((t - a) / b).mean()
        lo, hi = x[0] + np.exp(x[1]) * self.s0.min() - 20, x[0] + np.exp(x[1]) * self.s0.max() + 20
        al = np.atleast_1d(alpha); t = np.array([optimize.brentq(lambda t: fpr(t) - aa, lo, hi) for aa in al])
        pi = (1 / (1 + np.exp(-x[2])) if free_pi else pi_fixed)
        self.last_fit = (x[0], np.exp(x[1]), pi)
        return (t if np.ndim(alpha) else t[0]), (x[0], np.exp(x[1]), pi)
    def gof_pvalue(self, c):
        """KS p-value of labelled local controls against the transported source control CDF at the last fit."""
        a, b, _ = self.last_fit
        return stats.kstest(c, lambda t: 1 - self.S0((np.asarray(t) - a) / b)).pvalue


# Round 3: source-side self-calibration. The training cohorts are themselves "sites": rehearse deployment of the
# hybrid from the other training cohorts to each training cohort j (out-of-fold source scores, no target data),
# record realised FPR for a grid of nominal levels, and pick the nominal level whose mean realised FPR equals alpha.
def self_calibrate(s_src, y_src, g_src, alpha, k=5, prior=(0.01, 10), use_pool=True, R=10, seed=0,
                   grid=np.array([0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12])):
    rng = np.random.default_rng(seed); real = []
    for j in np.unique(g_src):
        src, tgt = g_src != j, g_src == j
        if len(np.unique(y_src[src])) < 2: continue
        c_all = s_src[tgt & (y_src == 0)]
        if len(c_all) < k + 8: continue
        T = PredTransport(s_src[src], y_src[src], n_draw=200, seed=seed)
        for _ in range(R):
            p = rng.permutation(len(c_all)); lab = c_all[p[:k]]; rest = c_all[p[k:]]
            h = len(rest) // 2; pool, ev = rest[:h], rest[h:]
            t, _ = T.predictive(grid, c=lab if k else None, u=pool if use_pool else None, prior=prior)
            real.append([(ev >= tt).mean() for tt in t])
    m = np.mean(real, 0)                       # mean realised FPR per nominal level (increasing in level)
    if m[0] > alpha: return grid[0]
    if m[-1] < alpha: return grid[-1]
    return float(np.interp(alpha, m, grid))
