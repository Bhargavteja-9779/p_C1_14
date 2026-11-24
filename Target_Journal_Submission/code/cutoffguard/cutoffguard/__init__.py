"""cutoffguard: keep the false-positive rate of a deployed diagnostic test on target using only the verified
outcomes of test-positive people (e.g. colonoscopy results), overall or within patient groups."""
from .core import verified_positive_threshold, Recalibrator, GroupRecalibrator, audit_sites
__all__ = ["verified_positive_threshold", "Recalibrator", "GroupRecalibrator", "audit_sites"]
__version__ = "0.1.0"
