import numpy as np
from scipy import stats

def verified_positive_threshold(scores, verified, labels, alpha=0.10, pi_max=0.05, delta=None):
    """Smallest cut-off t whose bounded false-positive rate is <= alpha (finite-sample, see Proposition S1).

    scores   : test scores of all m tested people in the window (higher = more likely diseased)
    verified : bool array, True if the person's true status is known (referred, attended, result available)
    labels   : 1 = disease confirmed, 0 = no disease; ignored where verified is False
    pi_max   : known upper bound on disease prevalence among tested people
    delta    : None -> expected FPR <= alpha; a number (e.g. 0.1) -> P(FPR > alpha) <= delta (high-confidence option)
    Unverified people above t are counted as possible false positives, so the bound holds whatever thresholds,
    attendance or delays produced the verification pattern. Returns +inf if no cut-off satisfies the bound."""
    s = np.asarray(scores, float); v = np.asarray(verified, bool); lab = np.asarray(labels)
    m = len(s); c1 = int(np.sum(v & (lab == 1)))
    m0_lo = m - max(c1, int(np.floor(pi_max * m)))
    k = int(np.floor(alpha * (m0_lo + 1) - 1))
    if delta is not None:
        ks = np.arange(0, max(m0_lo, 0) + 1); ok = ks[stats.binom.cdf(ks, m0_lo, alpha) <= delta]
        k = int(ok.max()) if len(ok) else -1
    if k < 0: return np.inf
    bad = np.sort(s[~(v & (lab == 1))])
    if k >= len(bad): return -np.inf
    return float(np.nextafter(bad[len(bad) - k - 1], np.inf))

class Recalibrator:
    """Sequential recalibration with a liberal burn-in cut-off and a drift alarm.

    >>> r = Recalibrator(initial_cutoff=0.0, alpha=0.10, pi_max=0.05)
    >>> refer = scores >= r.cutoff                       # month k: refer these people
    >>> r.update(scores, attended_and_resulted, labels)  # after outcomes arrive -> new r.cutoff"""
    def __init__(self, initial_cutoff, alpha=0.10, pi_max=0.05, alarm_p=0.01, delta=None):
        self.cutoff, self.alpha, self.pi_max, self.alarm_p, self.delta = float(initial_cutoff), alpha, pi_max, alarm_p, delta
        self._s, self._v, self._l, self.start, self.alarms = [], [], [], 0, 0
    def update(self, scores, verified_and_referred, labels):
        """scores: this batch; verified_and_referred: True where the person was referred under the cut-off in force
        AND their outcome is known; labels: outcomes (ignored where not verified)."""
        s = np.asarray(scores, float); v = np.asarray(verified_and_referred, bool) & (s >= self.cutoff)
        self._s.append(s); self._v.append(v); self._l.append(np.asarray(labels))
        j = len(self._s) - 1
        if j > self.start:
            fp = int(np.sum(v & (self._l[j] == 0))); n = len(s); m0 = n - int(np.floor(self.pi_max * n))
            if stats.binom.sf(fp - 1, m0, self.alpha) < self.alarm_p: self.start = j; self.alarms += 1
        cat = lambda L: np.concatenate(L[self.start:])
        self.cutoff = verified_positive_threshold(cat(self._s), cat(self._v), cat(self._l), self.alpha, self.pi_max, self.delta)
        return self.cutoff

class GroupRecalibrator:
    """One Recalibrator per patient group (e.g. recorded comorbidity), giving a per-group false-positive bound."""
    def __init__(self, groups, initial_cutoff, **kw):
        self.r = {g: Recalibrator(initial_cutoff, **kw) for g in groups}
    def cutoff(self, group): return self.r[group].cutoff
    def update(self, scores, verified, labels, groups):
        s, v, l, g = map(np.asarray, (scores, verified, labels, groups))
        for k, rec in self.r.items():
            sel = g == k
            if sel.any(): rec.update(s[sel], v[sel], l[sel])
        return {k: rec.cutoff for k, rec in self.r.items()}

def prevalence_bounded_threshold(scores, alpha=0.10, pi_max=0.05, delta=None):
    """Label-free cut-off from unlabelled scores of tested people, valid for any disease-score distribution when
    prevalence <= pi_max. delta=None: expected FPR <= alpha; delta: P(FPR > alpha) <= delta (binomial bound)."""
    u = np.sort(np.asarray(scores, float)); m = len(u); q = (1 - alpha) * (1 - pi_max) + pi_max
    if delta is None:
        k = int(np.ceil((m + 1) * q)); return float(u[k - 1]) if k <= m else np.inf
    rs = np.arange(1, m + 1); ok = rs[stats.binom.sf(rs - 1, m, q) <= delta]
    return float(u[ok.min() - 1]) if len(ok) else np.inf

def audit_sites(scores, labels, sites, cutoff, alpha=0.10):
    """Realised false-positive rate of a fixed cut-off at each site with an exact binomial test against alpha."""
    s, y, g = map(np.asarray, (scores, labels, sites)); out = []
    for site in np.unique(g):
        c = s[(g == site) & (y == 0)]; fp = int(np.sum(c >= cutoff))
        out.append(dict(site=site, n_controls=len(c), fpr=fp / max(len(c), 1),
                        p_exceeds=stats.binomtest(fp, len(c), alpha, alternative="greater").pvalue if len(c) else np.nan))
    return out
