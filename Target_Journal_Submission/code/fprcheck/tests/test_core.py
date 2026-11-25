import numpy as np
from fprcheck import burnin_k, burnin_cutoff, pac_k, prob_fpr_above, expected_fpr_range
def test_k_formula():
    assert burnin_k(100, 0.10, 0.01) == 92 and burnin_k(100, 0.10, 0.0) == 91 and burnin_k(50, 0.10, 0.01) == 46
def test_expected_fpr_exchangeable():
    rng = np.random.default_rng(0); f = []
    for _ in range(4000):
        x = rng.normal(size=1100); t = burnin_cutoff(x[:100], 0.10); f.append(np.mean(x[100:] >= t))
    assert np.mean(f) <= 0.10 + 0.005
def test_pac_bound():
    rng = np.random.default_rng(1); f = []
    for _ in range(3000):
        x = rng.normal(size=5100); t = burnin_cutoff(x[:100], 0.10, pac=True); f.append(np.mean(x[100:] >= t))
    assert np.mean(np.array(f) > 0.10) <= 0.05 + 0.015
def test_contaminated_bound():
    rng = np.random.default_rng(2); f = []
    for _ in range(3000):
        h = rng.normal(size=1000); c = rng.normal(2, 1, size=5); t = burnin_cutoff(np.r_[h[:95], c], 0.10, pi_max=0.05); f.append(np.mean(h[95:] >= t))
    assert np.mean(f) <= 0.10 + 0.005
def test_infeasible():
    assert burnin_cutoff([0.1, 0.2], 0.10) == float("inf")
def test_prob_law():
    assert abs(prob_fpr_above(0.15, 100, 91) - 0.08) < 0.05
def test_atlas_lookup():
    r = expected_fpr_range("CRC", "lasso"); assert 0 < r["pi_lo"] < r["pooled"] < r["pi_hi"] < 1
