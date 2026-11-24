import numpy as np
from cutoffguard import verified_positive_threshold, Recalibrator, GroupRecalibrator

def _site(rng, m, pi, shift):
    y = (rng.random(m) < pi).astype(int)
    s = np.where(y == 1, rng.normal(1.5, 1, m), rng.normal(0, 1, m)) + shift
    return s, y

def test_fresh_controls():
    from scipy.stats import norm
    rng = np.random.default_rng(1); fpr = []
    for _ in range(4000):
        mu = rng.normal(0, 1); y = (rng.random(200) < 0.03).astype(int)
        s = np.where(y == 1, rng.normal(mu + 1.5, 1, 200), rng.normal(mu, 1, 200))
        t0 = np.quantile(s, 0.7); ver = (s >= t0) & (rng.random(200) < 0.7)
        t = verified_positive_threshold(s, ver, y, 0.10, 0.05)
        fpr.append(norm.sf(t - mu))
    assert np.mean(fpr) <= 0.10 + 0.005

def test_recalibrator_converges_and_alarm():
    from scipy.stats import norm
    rng = np.random.default_rng(2); r = Recalibrator(initial_cutoff=0.5)
    for month in range(24):
        mu = 0.0 if month < 12 else 0.8
        y = (rng.random(200) < 0.01).astype(int); s = np.where(y == 1, rng.normal(mu + 1.5, 1, 200), rng.normal(mu, 1, 200))
        r.update(s, s >= r.cutoff, y)
    assert r.alarms >= 1 and norm.sf(r.cutoff - 0.8) <= 0.13

def test_group():
    rng = np.random.default_rng(3); gr = GroupRecalibrator(["healthy", "chronic"], initial_cutoff=0.0)
    for _ in range(12):
        g = np.where(rng.random(400) < 0.3, "chronic", "healthy"); y = (rng.random(400) < 0.01).astype(int)
        s = rng.normal(0, 1, 400) + (g == "chronic") * 0.8 + y * 1.5
        refer = s >= np.array([gr.cutoff(k) for k in g]); gr.update(s, refer, y, g)
    from scipy.stats import norm
    assert abs(norm.sf(gr.cutoff("chronic") - 0.8) - norm.sf(gr.cutoff("healthy"))) < 0.04

def test_high_confidence():
    from scipy.stats import norm
    rng = np.random.default_rng(4); fpr = []
    for _ in range(3000):
        mu = rng.normal(0, 1); y = (rng.random(400) < 0.02).astype(int)
        s = np.where(y == 1, rng.normal(mu + 1.5, 1, 400), rng.normal(mu, 1, 400))
        t = verified_positive_threshold(s, s >= np.quantile(s, 0.7), y, 0.10, 0.05, delta=0.10)
        fpr.append(norm.sf(t - mu))
    assert np.mean(np.array(fpr) > 0.10) <= 0.10 + 0.02
