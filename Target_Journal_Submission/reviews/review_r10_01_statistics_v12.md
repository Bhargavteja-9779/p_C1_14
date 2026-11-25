# Statistical review, round 10 — manuscript v12 (iMeta Letter)

**Score: 6/10. Decision: major revision.** The two MAJOR concerns need only reanalysis of files already in results/ and rewording. No new data are needed.

What holds up: almost every v12 number traces to a result file (gmwi2_results.json, gmwi2_published_training.json, gmwi2_eastasia.json, gmwi2_casemix.json, v6b_results.json, v6b_within_study_auroc.json, v6c_results.json). Examples: I² 0.92, PI 0.02–0.68, 80% vs 9% (P = 6e-13), G4 79% (CI 64–85%), gap 0.52 → 0.06, OR 6.7, AUROC 0.715 → 0.676. v6b has no leakage: the prevalence filter is computed inside each leave-one-study-out training fold, with one sample per subject and v4 de-duplication. Plan v6 was committed 3 minutes before the GMWI2 results (df2677c, then 28b2acd). Plan v6b was committed before the v6b results (28b2acd, then baf7218). The SI table of hypotheses reports G3, B3, C2 and C3 as falsified.

## Concerns

**1. MAJOR — v6c is labelled "pre-specified", but the repository cannot show this.** protocol_v6c.md first appears in commit 3fde340, the same commit that adds v6c_results.json and v6c_rows.csv. The commit message already reports the outcome. The main text says "pre-specified" for the C1 result. It also says each plan was "committed to the code repository before it was run". SI S6.5 says the same. For v6c, neither claim can be verified.
*What would resolve this:* label v6c as "plan written before running, but committed together with its results", or label it post hoc. Also correct the general sentence in the introduction.

**2. MAJOR — The v6c result does not support "confirming that the mechanism is not specific to GMWI2".**
(a) The balanced arm moved FPR levels far from target. Median per-population FPR rose from 0.04 to 0.33 for CRC and from 0.12 to 0.54 for T2D (my check of v6c_rows.csv). A lower τ on the logit scale is expected when FPRs move off the floor toward 0.5, because populations near 0 inflate logit spread. A τ reduction that comes with the share of populations outside the band rising from 66% to 82% is therefore not clean evidence of less heterogeneity. τ also rose for adenoma (0.84 → 0.89).
(b) The bootstrap is wrong. run_v6c.py uses `pick = set(rng.choice(pops, ...))`, which drops duplicate draws. It is therefore a roughly 63% subsample, not a cluster bootstrap. A correct resampling with replacement (/tmp/claude-0/r10_stats/boot_check.py) gives a CI of −0.22 to −0.005 for the difference, against the reported −0.23 to −0.03. It barely excludes 0.
(c) C3 failed, with a drop of 0.033 against a margin of 0.03. The main text says "cost 0.03 in AUROC" and does not say that C3 or C2 failed.
*What would resolve this:* in the main text, say "reduced τ in 4 of 5 tests, but shifted FPR levels away from target; C2 and C3 failed". Drop "confirming". Report the corrected bootstrap. Show that the τ reduction survives a level-matched comparison: for example, re-threshold each arm to a pooled FPR of 0.10 before computing τ, or use the median absolute deviation of the FPR.

**3. MINOR — The v6b study-clustered bootstrap is also wrong.** analyse_v6b.py concatenates resampled studies but keeps their names. `groupby("study_name")` then merges duplicate draws into one study with doubled n. When I relabel each draw as its own cluster, the CI for the gap reduction is 43–143%, against the reported 54–121%. The lower bound then falls below the B2 criterion of 50%. The point estimate of 88% still passes.
*What would resolve this:* correct the code, report the CI, and add "the CI includes reductions below the 50% criterion".

**4. MINOR — G3 is presented as reassurance, not as a falsified hypothesis.** The main text says the result "was not an overfitting artefact". The plan tested for in-sample optimism, and the data contradicted it (seen populations had higher FPR). Say "G3 falsified" in the main text. Holm correction over G1–G4 is stated in the plan, but the adjusted P values are not reported.

**5. MINOR — The comparison of unseen East Asian and other populations is not labelled post hoc.** The test (4 vs 11 populations, P = 0.065) is not in plan v6.

**6. MINOR — The graphical abstract makes causal claims and pools results that should be separate.**
- "Carry disease weights, because East Asian samples made up most of the non-healthy data" rests on a retraining in another dataset, so "consistent with" fits better than "because".
- "Removed 88% of this gap" refers to the curatedMetagenomicData retraining, not to GMWI2 itself.
- In "recalibrating on 100 unlabelled people … 62–79%", the burn-in groups in that analysis were all healthy. With 1–10% patients, sensitivity fell to about 0.22.
- Balancing also raised the pooled FPR (0.257 → 0.282) and the median FPR in the other studies (0.19 → 0.22). State this.

**7. MINOR — The stated GMWI2 FPR of 0.208 differs from what plan v6 defined.** It is computed on the 5,514 healthy people in the 44 studies with at least 20 healthy people, not on all 5,547 healthy training samples as plan v6 says. The difference is likely negligible, but it should be stated.

**8. MINOR — The two balancing schemes differ.** v6b weights by country × label. v6c weights by country × label and also gives each country equal weight. The text calls both "the same training-time balancing".
