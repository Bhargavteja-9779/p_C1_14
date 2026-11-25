import numpy as np, pytest
from scipy import stats
from fprcal import k_expected, k_pac, fpr_law, burnin_cutoff, verify_fpr, plan, plan_min_n, atlas
from fprcal.cli import main


def test_k_values_match_paper():
    assert k_expected(100, .10, .01) == 92          # worked example in the manuscript
    assert k_expected(100, .10) == 91
    k = k_pac(100, .10); assert stats.beta.sf(.10, 101 - k, k) <= .05 and stats.beta.sf(.10, 102 - k, k - 1) > .05


@pytest.mark.parametrize("N", [20, 50, 100])
def test_expected_rule_guarantee_monte_carlo(N):
    rng = np.random.default_rng(N); fpr = []
    for _ in range(4000):
        b = rng.standard_normal(N); t = burnin_cutoff(b, .10).cutoff
        fpr.append(stats.norm.sf(t))                 # true FPR of this cut-off for a N(0,1) healthy population
    assert np.mean(fpr) <= .10 + 3 * np.std(fpr) / np.sqrt(len(fpr))
    L = fpr_law(N, k_expected(N, .10)); assert abs(np.mean(fpr) - L["mean"]) < 4 * L["sd"] / np.sqrt(len(fpr))


def test_pac_rule_guarantee_monte_carlo():
    rng = np.random.default_rng(1); ex = [stats.norm.sf(burnin_cutoff(rng.standard_normal(200), .10, rule="pac").cutoff) > .10 for _ in range(4000)]
    assert np.mean(ex) <= .05 + 3 * np.sqrt(.05 * .95 / 4000)


def test_contamination_bound():
    # 1% diseased people (scores far above) in the burn-in: FPR among healthy stays <= alpha on average with pi_max=0.01
    rng = np.random.default_rng(2); fpr = []
    for _ in range(4000):
        b = np.r_[rng.standard_normal(99), [8.0]]; fpr.append(stats.norm.sf(burnin_cutoff(b, .10, pi_max=.01).cutoff))
    assert np.mean(fpr) <= .10 + 3 * np.std(fpr) / np.sqrt(4000)


def test_small_n_raises():
    with pytest.raises(ValueError, match="too small"): burnin_cutoff(np.arange(5.), .10, rule="pac")
    assert plan_min_n(.10) == 9 and plan_min_n(.10, rule="pac") > 9


def test_verify():
    s = np.r_[np.zeros(70), np.ones(30)]
    assert verify_fpr(s, .5).verdict == "EXCEEDS"
    assert verify_fpr(np.r_[np.zeros(900), np.ones(100)], .5).verdict == "CONSISTENT"
    assert verify_fpr(np.r_[np.zeros(18), np.ones(2)], .5).verdict.startswith("INCONCLUSIVE")


def test_plan_monotone():
    p = plan(); assert [r["N"] for r in p] == sorted(r["N"] for r in p)
    # small N: rank rounding makes it non-monotone, so check from N = 50
    q = [r["expected_P(FPR>0.15)"] for r in p if r["N"] >= 50]; assert all(a >= b for a, b in zip(q, q[1:]))


def test_atlas():
    assert len(atlas.tests()) == 14
    r = atlas.lookup("CRC", "lasso"); assert r["populations"] == 32 and 0 < r["pi95"][0] < r["pi95"][1] < 1
    assert 0 <= atlas.position("IBD", "lasso", .3) <= 1


def test_cli(tmp_path, capsys):
    f = tmp_path / "s.txt"; np.savetxt(f, np.random.default_rng(0).standard_normal(100))
    main(["cutoff", str(f), "--pi-max", "0.01"]); assert "rank 92 of 100" in capsys.readouterr().out
    main(["atlas", "IBD"]); assert "prediction interval" in capsys.readouterr().out
    main(["plan", "--json"]); assert '"N": 100' in capsys.readouterr().out


def test_models_reproduce_atlas_scale():
    import pandas as pd
    from fprcal import models
    m = models.meta(); assert len(m) == 14 and m.auroc.notna().all()
    c = models._coef(); t = c[c.test == "CRC"]
    # a sample at the training mean of every model taxon scores exactly the intercept
    x = pd.DataFrame([100 * (10 ** t.mu.values - 1e-5)], columns=t.taxon.values)
    assert abs(models.score(x, "CRC").iloc[0] - m.set_index("test").loc["CRC", "intercept"]) < 1e-6
    full = x.copy(); full.columns = ["k__Bacteria|" + c for c in full.columns]       # full clade names accepted
    assert abs(models.score(full, "CRC").iloc[0] - models.score(x, "CRC").iloc[0]) < 1e-12
    assert models.score_all(x).shape == (1, 28)
