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

def _kde(x, bw=None, n_grid=2048):
    """Gaussian KDE tabulated on a wide grid; returns a fast vectorised density (linear interpolation, 0 outside)."""
    k = stats.gaussian_kde(x, bw_method=bw); h = np.sqrt(k.covariance[0, 0])
    grid = np.linspace(x.min() - 8 * h - 10, x.max() + 8 * h + 10, n_grid); dens = k(grid)
    return lambda z: np.interp(z, grid, dens, left=0.0, right=0.0)

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

# ---------- Round 2: control-anchored transport (few labelled local controls) ----------
def ctrl_moment_transport(s_src, y_src, alpha, c, **kw):
    """Location-scale map of the source control score distribution onto n local controls (mean/sd matching).
    t = a + b * t_src with b = sd(c)/sd(src0), a = mean(c) - b*mean(src0)."""
    s0 = s_src[y_src == 0]; t_src = np.quantile(s0, 1 - alpha)
    b = np.std(c, ddof=1) / np.std(s0, ddof=1) if len(c) > 2 else 1.0
    return np.mean(c) + b * (t_src - np.mean(s0))

def ctrl_shift_transport(s_src, y_src, alpha, c, **kw):
    """Location-only map (b = 1): t = t_src + mean(c) - mean(src0)."""
    s0 = s_src[y_src == 0]; return np.quantile(s0, 1 - alpha) + np.mean(c) - np.mean(s0)

def ctrl_robust_transport(s_src, y_src, alpha, c, **kw):
    """Median / MAD location-scale map."""
    s0 = s_src[y_src == 0]; t_src = np.quantile(s0, 1 - alpha)
    mad = lambda x: np.median(np.abs(x - np.median(x)))
    b = mad(c) / mad(s0) if len(c) > 3 and mad(c) > 0 else 1.0
    return np.median(c) + b * (t_src - np.median(s0))

def ctrl_normal(alpha, c, **kw):
    """Source-free parametric baseline: mean + z_{1-alpha} * sd of local controls."""
    return np.mean(c) + stats.norm.ppf(1 - alpha) * np.std(c, ddof=1)

# ---------- Round 3: per-deployment guarantees ----------
def pac_controls(c, beta=0.15, delta=0.10):
    """Training-conditional (PAC) threshold from n labelled local controls: smallest order statistic c_(k) with
    P(FPR > beta) <= delta. FPR(c_(k)) = 1 - F0(c_(k)), F0(c_(k)) ~ Beta(k, n-k+1); need P(Bin(n, 1-beta) >= k) <= delta."""
    c = np.sort(c); n = len(c)
    for k in range(1, n + 1):
        if stats.binom.sf(k - 1, n, 1 - beta) <= delta: return c[k - 1]
    return np.inf

def contam_quantile(u, alpha, pi_max):
    """Label-free threshold from an unlabeled pool that may contain cases at prevalence <= pi_max.
    F_u = (1-pi)F0 + pi F1 >= (1-pi_max)F0 ... => F0(t) >= (F_u(t) - pi_max)/(1 - pi_max). Choose t with
    (F_u(t) - pi_max)/(1 - pi_max) >= 1 - alpha, using the conformal (m+1) order-statistic rank.
    Holds for ANY case score distribution (no transport assumption)."""
    u = np.sort(u); m = len(u); q = (1 - alpha) * (1 - pi_max) + pi_max
    k = int(np.ceil((m + 1) * q)); return u[k - 1] if k <= m else np.inf

# ---------- Round 4: verified-positive recalibration (one-sided feedback from routine follow-up) ----------
def verified_positive(u, lab, alpha, pi_max, t0):
    """Deployment pool u (m unlabeled scores). Samples with u >= t0 were referred (colonoscopy) so their labels `lab`
    are observed; labels below t0 are never used. Count false positives exactly above t0; bound the number of
    controls from below: m0 >= m - C1 - max(0, floor(pi_max*m) - C1)  (C1 = verified cases).
    Return smallest candidate t >= t0 with (FP(t) + 1) / (m0_lo + 1) <= alpha; FP(t) = #verified controls >= t.
    Returns (t, n_referred_burn_in)."""
    u = np.asarray(u); m = len(u); ref = u >= t0
    c1 = int(lab[ref].sum()); fn_bound = max(0, int(np.floor(pi_max * m)) - c1)
    m0_lo = m - c1 - fn_bound
    ctrl_sc = np.sort(u[ref & (lab == 0)])                      # verified control scores (ascending)
    cands = np.concatenate([[t0], np.sort(u[ref]) + 1e-9])
    for t in np.sort(cands):
        fp = len(ctrl_sc) - np.searchsorted(ctrl_sc, t, side="left")
        if (fp + 1) / (m0_lo + 1) <= alpha: return t, int(ref.sum())
    return np.inf, int(ref.sum())

def verified_positive_seq(u, tau, lab, alpha, pi_max, delta=None):
    """Sequential/general form. Sample i was referred iff u_i >= tau_i (its threshold at test time); its label is
    known only then. For candidate t: FP_ub(t) = #verified controls with u >= t + #UNverified samples with u >= t
    (unverified ones are counted as possible false positives -> valid upper bound whatever the past thresholds).
    m0_lo = m - C1 - max(0, floor(pi_max*m) - C1). Return smallest t with (FP_ub(t)+1)/(m0_lo+1) <= alpha."""
    u, tau, lab = map(np.asarray, (u, tau, lab)); m = len(u); ver = u >= tau
    c1 = int(lab[ver].sum()); m0_lo = m - c1 - max(0, int(np.floor(pi_max * m)) - c1)
    bad = np.sort(u[~(ver & (lab == 1))])                         # everything not a verified case
    k = int(np.floor(alpha * (m0_lo + 1) - 1))                    # max allowed FP_ub (marginal: E[FPR] <= alpha)
    if delta is not None:   # high-confidence version: P(FPR > alpha) <= delta (training-conditional order statistic)
        ks = np.arange(0, m0_lo + 1); ok = ks[stats.binom.cdf(ks, m0_lo, alpha) <= delta]
        k = int(ok.max()) if len(ok) else -1
    if k < 0: return np.inf
    if k >= len(bad): return -np.inf
    return bad[len(bad) - k - 1] + 1e-9                           # leaves exactly k 'bad' samples >= t

class SequentialRecalibrator:
    """Proposed method (frozen candidate): sequential verified-positive recalibration with a drift alarm.
    Month 1 uses a liberal burn-in threshold. After each month, only outcomes of referred AND attending samples are
    used. If the newest month with outcomes shows more verified false positives than Binomial(m0, alpha) allows
    (one-sided p < alarm_p), the pool is restarted from that month."""
    def __init__(self, s_src, y_src, alpha=0.10, pi_max=0.05, burn=2, alarm_p=0.01, delay=0, delta=None):
        self.alpha, self.pi_max, self.alarm_p, self.delay, self.delta = alpha, pi_max, alarm_p, delay, delta
        self.t = np.quantile(s_src[y_src == 0], 1 - min(burn * alpha, 0.9))
        self.U, self.L, self.TAU, self.start, self.alarms = [], [], [], 0, 0
    def update(self, u_new, lab_new, attended=None):
        attended = np.ones(len(u_new), bool) if attended is None else attended
        self.U.append(np.asarray(u_new)); self.L.append(np.asarray(lab_new)); self.TAU.append(np.where(attended, self.t, np.inf))
        j = len(self.U) - 1 - self.delay
        if j >= self.start + 1:
            ver = self.U[j] >= self.TAU[j]; fp = int((ver & (self.L[j] == 0)).sum()); n = len(self.U[j])
            m0 = n - int(np.floor(self.pi_max * n))
            if stats.binom.sf(fp - 1, m0, self.alpha) < self.alarm_p: self.start = j; self.alarms += 1
        lo, hi = self.start, len(self.U)
        tau = np.concatenate([self.TAU[i] if i < hi - self.delay else np.full(len(self.U[i]), np.inf) for i in range(lo, hi)])
        self.t = verified_positive_seq(np.concatenate(self.U[lo:hi]), tau, np.concatenate(self.L[lo:hi]), self.alpha, self.pi_max, self.delta)
        return self.t


def contam_quantile_hc(u, alpha, pi_max, delta=0.10):
    """High-confidence prevalence-bounded quantile (post hoc comparator): rank r chosen so that, under the prevalence
    bound, P(FPR > alpha) <= delta (binomial order-statistic bound on the pool at level q)."""
    u = np.sort(u); m = len(u); q = (1 - alpha) * (1 - pi_max) + pi_max
    rs = np.arange(1, m + 1); ok = rs[stats.binom.sf(rs - 1, m, q) <= delta]
    return u[ok.min() - 1] if len(ok) else np.inf
