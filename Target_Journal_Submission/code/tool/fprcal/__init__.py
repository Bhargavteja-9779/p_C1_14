"""fprcal: check and set the false-positive rate of a microbiome (or any score-based) diagnostic test at the site of use.

    from fprcal import burnin_cutoff, verify_fpr, plan, atlas
"""
from .core import k_expected, k_pac, fpr_law, burnin_cutoff, verify_fpr, plan, plan_min_n
from . import atlas, models
__version__ = "0.1.0"
