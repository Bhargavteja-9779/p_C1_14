"""Core functions: label-free burn-in cut-off, the exact law of the realised false-positive rate (FPR), local
verification of a stated FPR, and sample-size planning.

Notation. A site scores N people (the burn-in group), almost all healthy. The cut-off is the k-th smallest burn-in
score; a person is flagged if score >= cut-off. If later healthy people are exchangeable with the burn-in group and
scores are continuous, the realised FPR of that cut-off follows Beta(N + 1 - k, k) exactly (order-statistic law).
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
import numpy as np
from scipy import stats

__all__ = ["k_expected", "k_pac", "fpr_law", "burnin_cutoff", "verify_fpr", "plan", "BurnIn", "Verification"]


def _check(alpha, pi_max=0.0, delta=None):
    if not 0 < alpha < 1: raise ValueError("alpha must be in (0, 1)")
    if not 0 <= pi_max < 1: raise ValueError("pi_max must be in [0, 1)")
    if delta is not None and not 0 < delta < 1: raise ValueError("delta must be in (0, 1)")


def _beta_eff(alpha, pi_max):
    """Target FPR among all burn-in people so that the FPR among healthy people stays <= alpha when up to a share
    pi_max of the burn-in group has the disease (worst case: all diseased scores above the cut-off)."""
    return alpha * (1 - pi_max)


def k_expected(N: int, alpha: float, pi_max: float = 0.0) -> int:
    """Rank k = ceil((N + 1)(1 - alpha(1 - pi_max))): expected FPR <= alpha (split-conformal argument).
    Returns N + 1 if N is too small (no finite cut-off achieves the target)."""
    _check(alpha, pi_max)
    return int(math.ceil((N + 1) * (1 - _beta_eff(alpha, pi_max))))


def k_pac(N: int, alpha: float, pi_max: float = 0.0, delta: float = 0.05) -> int:
    """Smallest rank k with P(realised FPR > alpha) <= delta (probably-approximately-correct variant).
    Returns N + 1 if no rank achieves it (N too small)."""
    _check(alpha, pi_max, delta)
    b = _beta_eff(alpha, pi_max)
    for k in range(1, N + 1):
        if stats.beta.sf(b, N + 1 - k, k) <= delta: return k
    return N + 1


def fpr_law(N: int, k: int, thresholds=(0.10, 0.15, 0.20)) -> dict:
    """Exact distribution of the realised FPR of the k-th smallest of N exchangeable healthy scores."""
    if not 1 <= k <= N: return dict(N=N, k=k, feasible=False)
    d = stats.beta(N + 1 - k, k)
    out = dict(N=N, k=k, feasible=True, mean=float(d.mean()), sd=float(d.std()),
               q05=float(d.ppf(.05)), q50=float(d.ppf(.5)), q95=float(d.ppf(.95)))
    for t in thresholds: out[f"P(FPR>{t:g})"] = float(d.sf(t))
    return out


@dataclass
class BurnIn:
    cutoff: float
    k: int
    N: int
    alpha: float
    pi_max: float
    rule: str
    delta: float | None
    law: dict

    def to_dict(self): return asdict(self)

    def __str__(self):
        g = (f"P(FPR > {self.alpha:g}) <= {self.delta:g}" if self.rule == "pac" else f"E[FPR] <= {self.alpha:g}")
        L = self.law
        return (f"cut-off = {self.cutoff:.6g} (rank {self.k} of {self.N}); guarantee {g} if later healthy people are "
                f"exchangeable with the burn-in group and disease prevalence in it is <= {self.pi_max:g}.\n"
                f"Realised FPR (healthy, no disease in burn-in): mean {L['mean']:.3f}, 90% range {L['q05']:.3f}-{L['q95']:.3f}, "
                f"P(FPR>0.15) = {L['P(FPR>0.15)']:.3f}")


def burnin_cutoff(scores, alpha: float = 0.10, pi_max: float = 0.0, rule: str = "expected", delta: float = 0.05) -> BurnIn:
    """Label-free cut-off from the scores of the first N people tested at a site.

    rule='expected': E[FPR] <= alpha.  rule='pac': P(FPR > alpha) <= delta (needs larger N, costs sensitivity)."""
    s = np.asarray(scores, float).ravel(); s = s[np.isfinite(s)]; N = len(s)
    if N == 0: raise ValueError("no finite scores")
    if rule == "expected": k, dl = k_expected(N, alpha, pi_max), None
    elif rule == "pac": k, dl = k_pac(N, alpha, pi_max, delta), delta
    else: raise ValueError("rule must be 'expected' or 'pac'")
    if k > N:
        need = plan_min_n(alpha, pi_max, rule, delta)
        raise ValueError(f"N = {N} is too small for this rule; at least {need} burn-in people are needed")
    return BurnIn(float(np.sort(s)[k - 1]), k, N, alpha, pi_max, rule, dl, fpr_law(N, k))


def plan_min_n(alpha=0.10, pi_max=0.0, rule="expected", delta=0.05, n_max=100000) -> int:
    for N in range(1, n_max + 1):
        k = k_expected(N, alpha, pi_max) if rule == "expected" else k_pac(N, alpha, pi_max, delta)
        if k <= N: return N
    return -1


@dataclass
class Verification:
    n: int
    flagged: int
    fpr: float
    ci_low: float
    ci_high: float
    alpha: float
    tolerance: float
    p_exceeds: float
    verdict: str

    def to_dict(self): return asdict(self)

    def __str__(self):
        return (f"{self.flagged}/{self.n} healthy people flagged: FPR {self.fpr:.3f} (95% CI {self.ci_low:.3f}-{self.ci_high:.3f}). "
                f"One-sided test of FPR > {self.alpha + self.tolerance:g}: P = {self.p_exceeds:.3g}. Verdict: {self.verdict}")


def verify_fpr(scores_healthy, cutoff: float, alpha: float = 0.10, tolerance: float = 0.05, level: float = 0.05) -> Verification:
    """Verify a stated FPR on local people known (or assumed) to be healthy, as laboratories verify reference intervals.
    verdict: 'EXCEEDS' if the exact one-sided binomial test rejects FPR <= alpha + tolerance at `level`;
    'CONSISTENT' if the 95% CI lies inside [alpha - tolerance, alpha + tolerance]; otherwise 'INCONCLUSIVE (collect more)'."""
    s = np.asarray(scores_healthy, float).ravel(); s = s[np.isfinite(s)]; n = len(s)
    if n == 0: raise ValueError("no finite scores")
    k = int((s >= cutoff).sum()); ci = stats.binomtest(k, n).proportion_ci(0.95, method="exact")
    p = float(stats.binomtest(k, n, alpha + tolerance, alternative="greater").pvalue)
    if p < level: v = "EXCEEDS"
    elif ci.low >= alpha - tolerance and ci.high <= alpha + tolerance: v = "CONSISTENT"
    else: v = "INCONCLUSIVE (collect more)"
    return Verification(n, k, k / n, float(ci.low), float(ci.high), alpha, tolerance, p, v)


def plan(alpha=0.10, pi_max=0.0, delta=0.05, Ns=(25, 50, 100, 200, 400, 800)) -> list[dict]:
    """Planning table: for each burn-in size N, realised-FPR law of the expected-FPR rule and of the PAC rule."""
    rows = []
    for N in Ns:
        r = dict(N=N)
        for name, k in [("expected", k_expected(N, alpha, pi_max)), ("pac", k_pac(N, alpha, pi_max, delta))]:
            L = fpr_law(N, k)
            r[f"{name}_k"] = k
            r[f"{name}_mean_fpr"] = L.get("mean", float("nan"))
            r[f"{name}_q95_fpr"] = L.get("q95", float("nan"))
            r[f"{name}_P(FPR>0.15)"] = L.get("P(FPR>0.15)", float("nan"))
        rows.append(r)
    return rows
