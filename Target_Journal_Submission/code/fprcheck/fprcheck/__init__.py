"""fprcheck: set and check the false-positive-rate (FPR) cut-off of a microbiome disease classifier at a new site.

Typical use at a site adopting a published classifier:
    from fprcheck import burnin_cutoff, expected_fpr_range
    t = burnin_cutoff(scores_of_first_100_people, alpha=0.10, pi_max=0.01)
    expected_fpr_range("CRC", "lasso")   # what the published cut-off did in 32-36 healthy populations

Guarantee (burn-in rule): if later people are exchangeable with the burn-in people, the expected FPR is <= alpha for
any disease prevalence up to pi_max. It is NOT a per-site guarantee (see `pac=True`) and it does not transfer between
sites. See the accompanying paper for when it holds and fails.
"""
from .core import burnin_k, burnin_cutoff, pac_k, prob_fpr_above, expected_fpr_range, atlas_table
__all__ = ["burnin_k", "burnin_cutoff", "pac_k", "prob_fpr_above", "expected_fpr_range", "atlas_table"]
__version__ = "0.1.0"
