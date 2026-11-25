# Review r9-01: Methods and statistics (Reviewer 1), manuscript v11

**Manuscript:** "A false-positive-rate atlas of gut-microbiome disease tests across 36 healthy populations" (Letter, iMeta)
**Material inspected:** manuscript_v11.md; figures_v11 (Figures 1 and 2); supporting_information_v4.md, si_tables_v4.md
(and si_tables_v11.md for the table numbering); code/experiments/atlas/v5 (atlas_v5.py, analyse_v5.py, explore_v5.py,
replicate_v5.py, verify_power_v5.py, numbers_v11.py, protocol_v5.md, all result files); v4 results quoted in the text
(deploy_v4_cc_summary.csv, holm_v6.csv, dedup095_sensitivity.json, Tables S2/S4/S5 of si_tables_v4); fprcal core.py;
git history of v5. I recomputed every quoted number I could from the result files, in memory and without writing to the
repository. Where I give numbers below that are not in the manuscript, they come from these recomputations.

**Overall score:** 6 / 10
**Recommendation for iMeta:** Major revision

## Summary assessment

The main descriptive finding is robust. A cut-off set on training controls gives very different FPRs in external healthy
populations: I² ≥ 0.5 for 28/28 classifiers, Cochran's Q P ≈ 0 for every classifier, wide prediction intervals, and the
same result in the full set. The within-site burn-in result is also robust, including at the population level (13/13
populations; see Major 5). The authors are unusually open about failed hypotheses, deviations and post hoc analyses, and
the code is clean enough to audit.

The weak point is the second section ("the error belongs to the test–population pair"). Its headline variance shares
include binomial sampling noise in the "pair" component. The verdict on pre-stated hypothesis H2 sits on its decision
boundary, and the text misstates that boundary. Several hypothesis verdicts in the text are worded differently from the
protocol. The guarantee claimed for the burn-in rule is stated more broadly than it holds, and the paper never tests it
empirically. Several supporting checks were run on v4 versions of three tests, not on the v5 classifiers shown in the
figures. The Methods are delegated entirely to a Supporting Information file that does not yet describe the v5 analysis.
All of this can be fixed without new data.

---

## MAJOR concerns

### M1. The variance decomposition puts binomial noise into the "test–population pair" share, and the H2 verdict sits on its threshold

`analyse_v5.py` fits `mixedlm("y ~ 1", vc_formula={test, pop})` to empirical logits y = log((k+.5)/(n−k+.5)). The
residual (`f.scale`) therefore contains the test×population interaction **plus the binomial sampling variance of each
empirical logit**. The authors' own Table S3 header in si_tables_v11 says so ("residual = test–population pair + binomial
noise"), yet the text says "the test–population pair for the remaining 62% (47% for RF)". The populations are small
(median n = 77; 30% have n < 50), so the noise is not negligible:

| | Mean within-unit sampling variance of y | Residual variance | Pair share as reported | Pair share after removing mean sampling variance (crude) | Population share after the same correction |
|---|---|---|---|---|---|
| LASSO | 0.25 | 1.09 | 0.62 | ≈ 0.55 | **≈ 0.20** |
| RF | 0.57 | 1.22 | 0.47 | ≈ 0.32 | ≈ 0.10 |

Protocol H2 asks whether the population component is "≥ 20% of the total **between-unit** variance", and sampling noise
is arguably not between-unit variance. After a crude correction, the LASSO population share reaches the 20% threshold.
Restricting to populations with n ≥ 50 gives 0.22 even without the correction. So "inconclusive for LASSO" is not
robust; it depends on how noise is handled.

The RF result ("falsified", test share 46%) is driven by classifiers that are below chance or degenerate (see M6).
IGT-RF has FPR = 0 in 32/35 populations, and 19.6% of RF units have k = 0, where the 0.5-corrected logit depends only on
n. Excluding classifiers with AUROC < 0.6 lowers the RF test share from 0.46 to 0.21 and raises the pair share to 0.68.

There are also no uncertainty intervals on any component. The test component is estimated from 14 levels and will be
very imprecise.

**Resolution:**
1. Refit as a binomial GLMM with an observation-level (test:population) random effect, e.g.
   `glmer(cbind(k, n−k) ~ 1 + (1|test) + (1|pop) + (1|test:pop), family = binomial)`, or as a multivariate meta-analysis
   with known sampling variances (`metafor::rma.mv` with V = 1/(k+.5) + 1/(n−k+.5)). This separates the pair variance
   from binomial noise.
2. Report profile-likelihood or parametric-bootstrap 95% CIs for all three shares.
3. Add sensitivity analyses excluding classifiers with AUROC < 0.6 and populations with n < 50.
4. Restate the H2 verdict under the pre-specified definition, and say plainly if the LASSO verdict sits on the threshold.
5. Change "the test–population pair for the remaining 62%" to "the residual (pair plus sampling noise)", or report the
   GLMM pair share.

### M2. Hypothesis verdicts and thresholds in the text do not match protocol_v5

- **H2.** The text says "Our pre-stated hypothesis that the population would explain at least a quarter". protocol_v5
  says "≥ 20% … WRONG if < 10%". The verdicts (LASSO 17% inconclusive, RF 7.5% falsified) match the 20%/10% rule, not
  "a quarter". Correct the threshold, and see M1 for the LASSO verdict.
- **H3.** The text says "This falsified our expectation of a shared set of drivers". protocol_v5 defines WRONG as "no
  taxon recurs in ≥ 3 tests". Two taxa recur in exactly three tests (`v5_summary.json`: `taxa_in_ge3_tests = 2`), so by
  the pre-stated rule H3 is **not supported / inconclusive, not falsified**. The commit message (e59cd78) itself says "H3
  not supported". The text also says "We split each over-flagged population's score shift", but the code decomposes only
  the single most over-flagged population per test. Two of the twelve most frequent "taxa" are not taxa at all
  (`k__Bacteria`, `o__Proteobacteria_unclassified`).
- **"Pre-registered."** The introduction rightly says the plans are internal and time-stamped, not external
  pre-registrations. The geography paragraph then says "we pre-registered a replication". Use "pre-specified (internal
  analysis plan, Addendum A)".
- **Replication not blind.** The replication populations' FPRs had already been computed, committed and partly
  summarised before Addendum A was written. `v5_perpop_full.csv` and the full-set H1/H2 summaries were committed at
  19:10:51 in e59cd78; Addendum A was committed at 19:11:37 in 920b99c. The replication is therefore not blind to the
  outcome data. State this.
- **RF replication result omitted.** The secondary RF replication of H5 met the stated criterion (11/14, one-sided sign
  P = 0.029, "SUPPORTED" in `replication_v5.json`) and is not mentioned. It is secondary, but it bears on the conclusion
  "did not replicate at the stated level", so report it.

**Resolution:** Add a one-row-per-hypothesis table (Supporting Information or main text) giving: H1–H6; the pre-stated
criterion verbatim; the observed statistic; and the verdict under the protocol's own three-way rule
(supported / inconclusive / wrong). Make the text use those verdicts.

### M3. The burn-in guarantee is stated more broadly than it holds, and the paper never tests it empirically

1. **Prevalence bound.** With π_max > 0, the bound E[FPR] ≤ α holds only if the *realised* number of patients in the
   burn-in group is at most π_max·N. If π_max is a bound on prevalence, the patient count is random (binomial), and
   because the bound is convex in that count, the expectation can slightly exceed α. The `_beta_eff` docstring in fprcal
   also names the wrong worst case: the adversarial case for healthy FPR is patients scoring *below* the healthy people,
   not above the cut-off. The formula covers that case, but the reasoning as written does not. State the guarantee as
   conditional on the realised patient fraction, or give the unconditional bound.
2. **"Exact Beta law" assumes continuous, untied scores.** The fatty-liver LASSO model has 3 non-zero coefficients. Up
   to 79% of scores in a population are tied (HanniganGD_2017: 0.79; IjazUZ_2017: 0.56; FengQ_2015: 0.33), and ties
   also occur for hypertension (12 taxa). Because the rule flags score ≥ threshold, ties raise the FPR above the Beta
   law. fprcal should randomise ties or warn, and the text should state the assumption.
3. **The empirical test (H4) does not test the guarantee.** H4 compares mean |FPR − 0.10| under deliberately
   non-exchangeable splits. That is a useful robustness check, but it says nothing about whether E[FPR] ≤ α or
   P(FPR > 0.15) ≈ 0.055 when exchangeability holds. In v5, `v5_h4_units.csv` stores only absolute errors, so even the
   direction of the error is unknown. In the accession-order units, 23% of burn-in evaluations have |FPR − 0.10| > 0.05.
   The Beta law alone predicts about 8%; part of the gap is evaluation noise, because hold-out sets can be as small as
   20 people. Nobody has made this comparison.

**Resolution:** For the H4 units, store the **signed** realised FPR. Report its mean, and the share above 0.15, next to
the value the Beta law predicts after convolving with binomial evaluation noise for each hold-out size. Add a
random-split (exchangeable) evaluation for the v5 classifiers, as v4 had for three tests, as the direct empirical check
of the guarantee. Then say how far the non-random splits depart from it. Rephrase "the expected FPR is at most α" to
include the realised-fraction condition and the no-ties condition.

### M4. Several checks in the text were run on the v4 versions of three tests, not on the v5 classifiers shown in the figures

The fold-model check, the covariate adjustment ("15–49%"), the IBD taxon explanation (Gemmiger, R. bromii), the
cross-site burn-in, control augmentation and the contamination experiment all come from v4 (CRC, IBD and T2D). The v5
IBD model is **not the same classifier**. In v4 (si_tables_v4 Table S2, strict) IBD-LASSO has a pooled FPR of 0.122
and a maximum FPR of 0.467 among n ≥ 100 populations. In v5 it has a pooled FPR of 0.187, and YachidaS_2019 alone has
0.565. The Figure 1B values (0.45–0.76) and the S3 taxon explanation therefore come from different models.

The fold-model check also does not support "changed little" for calibration in the large. In v4, the pooled FPR of the
T2D LASSO is 0.134 with the refitted model versus 0.097 with the fold models, and 0.076 versus 0.052 for RF. These are
25–30% relative shifts. Refit-versus-OOF mismatch can create exactly the test-level shifts that enter the "test"
variance component; compare IGT LASSO (pooled 0.42) with IGT RF (pooled 0.008), although both have a training FPR of
0.101. Nine v5 tests use 5-fold OOF cut-offs from as few as 36–50 controls (fatty liver 36, hypertension 41, ME/CFS 50).
Their cut-offs have sampling SDs around ±0.04–0.05 in FPR, which also loads onto the test component and the test means.

**Resolution:**
1. Re-run the fold-model scoring for all 28 v5 classifiers and report pooled FPR and τ with each.
2. Either redo the IBD decomposition with the v5 model or say explicitly that S3 refers to the v4 IBD model.
3. Label every v4-derived statement in the text "(v4 models, CRC/IBD/T2D)".
4. Report the bootstrap uncertainty of each training cut-off.

### M5. The H4 inference and description

1. **Pseudoreplication.** The exact Wilcoxon P = 7 × 10⁻⁹ treats the 28 classifiers as independent pairs. All 28 are
   evaluated on the same 13 populations and the same people. P = 7.45 × 10⁻⁹ is simply 2⁻²⁷, the smallest attainable
   value. Analysed by population, burn-in is better in **13/13 populations (exact Wilcoxon P = 2.4 × 10⁻⁴)**. A crossed
   mixed model on unit differences gives a mean difference of −0.066 (SE 0.015). The conclusion stands, but report the
   population-level analysis as primary inference, and the 28/28 count as the pre-stated criterion.
2. **Design mismatch.** The text says the burn-in used "the younger, leaner or **one-sex** half". `analyse_v5.py` uses
   only accession order, age and BMI (346 + 136 + 164 = 646 units); there is no sex design in v5 (sex was a v4 P4
   design). Correct the text.
3. **Undisclosed population set.** H4 runs on the **full** set with all persons, not the strict primary set. Two of its
   13 populations (MetaCardis_2020_a, ShaoY_2019) are not strict populations. Say so.
4. **Different averaging.** The quoted 0.101 → 0.038 averages over classifiers, not over the 646 evaluations (unit-level
   means 0.1013 and 0.0382; same to 3 dp, but say which). The burn-in arm averages |error| over 200 random draws per
   covariate unit, while the training-cut-off arm is a single evaluation. State this.

### M6. Sub-chance and degenerate classifiers are pooled into every summary

Three RF classifiers have out-of-fold AUROC below 0.5: adenoma 0.444, IGT 0.447, fatty liver 0.449. Several LASSO
classifiers are near chance (IGT 0.537, fatty liver 0.540, migraine 0.555). Fatty-liver LASSO has 3 non-zero taxa,
yet it supplies the maximum I² (0.967). These classifiers enter H1, H2, the AUROC–τ correlation, the outside-band
shares and fprcal's atlas. A sub-chance model's FPR heterogeneity says little about deployable tests. Its near-zero FPRs
(IGT-RF pooled 0.008) dominate the RF test variance (M1).

**Resolution:** Pre-specify a minimum AUROC (e.g. ≥ 0.6, or a 95% CI excluding 0.5) for the main summaries, or report
every summary both with and without such classifiers. The text already does this for H1 at 0.65; extend it to H2, the
Spearman analysis and the outside-band figure. Flag these classifiers in fprcal output.

### M7. The Methods are delegated to a Supporting Information file that does not describe this analysis

The Letter's Methods are one sentence pointing to "Tables S1–S15" and to SI sections S2–S4. The text SI provided
(supporting_information_v4.md) describes the three-test v4 analysis, and its section numbering does not match the
citations:

- In the v4 SI, S2 = analysis plans, S3 = revision history and S4 = failed fixes.
- The text uses S2 = the three robustness checks, S3 = the IBD taxa and S4 = the cut-offs from other cohorts.

The tables file si_tables_v11.md has S1–S23, not S1–S15. There is no SI text describing:

- the 14-test selection rule;
- the DL estimator with 0.5 continuity correction and t_{k−2} prediction interval;
- the mixed-model specification;
- the H3 decomposition;
- the H4 designs;
- Addendum A;
- the verification-power method.

A reader cannot reproduce the paper from the manuscript and SI as submitted.

**Resolution:** Write a v11 SI methods section covering all of these, with deviations, and fix all S-section and
S-table citations. iMeta Letters allow a short Methods paragraph in the main text. At minimum, the main text should name
the heterogeneity estimator, the mixed model, and the population set used for H4.

---

## MINOR concerns

1. **Prediction-interval range is wrong.** "the 95% prediction interval … reached 0.34 to 0.81 at its upper end for
   LASSO". From `v5_het_strict.csv`, the LASSO pi_hi values range from **0.22 (CRC)** to 0.81 (IGT); 0.34 is
   hypertension. Correct to 0.22–0.81, or name the exclusion.
2. **The "sampling noise alone" comparison conflates calibration in the large with heterogeneity.** The expected
   15–16% outside 0.05–0.15 assumes the true FPR is 0.10 in every population. For tests whose pooled FPR is far from
   0.10, most populations fall outside the band even with τ = 0; IGT-LASSO's pooled FPR is 0.42, for example. Add the
   expected share under homogeneity around each test's pooled FPR. Also cite Cochran's Q (P < 10⁻¹⁰ for all 28) as
   the test of "spread exceeded sampling noise". I² measures magnitude, not significance, and is inflated by large n.
3. **Heterogeneity estimator.** DL with empirical logits and a 0.5 correction is biased with rare events, and 4% of
   LASSO units and 20% of RF units have k = 0. Add a sensitivity analysis with a binomial-normal random-effects model
   (`metafor::rma.glmm`, or `glmer` per test), Q-profile CIs for τ, and HKSJ-adjusted prediction intervals.
4. **AUROC vs τ.** The 28 points come in 14 LASSO/RF pairs on the same diseases, so they are not independent. With
   n = 28 the 95% CI for ρ = −0.06 runs from about −0.42 to +0.32. "A better classifier was not a more portable one"
   overstates a null result. Report the CI, analyse per model or with disease as a random effect, exclude sub-chance
   classifiers (M6), and rephrase as "we found no evidence that AUROC predicted …".
5. **Verification power wording.**
   - The 0.98 and 0.72 values are **mean** powers over atlas pairs, not the probability for a given pair above the
     threshold. A pair whose true FPR is exactly 0.25 is detected with probability 0.79 at n = 100 and 0.49 at n = 50;
     one just above 0.15 is detected with probability ≈ 0.04.
   - "Raising a false alarm in at most 3.3% of pairs" is the largest per-pair false-alarm probability, not a share of
     pairs. The size of the test at FPR = 0.15 is 0.039.
   - Rephrase both. Also report the RF values (0.97 and 0.68).
   - I checked whether treating observed FPRs as true inflates power by refitting with empirical-Bayes shrunken FPRs
     (per-test DL τ). The effect is small: 0.97 / 0.69 at n = 100 and 0.89 at n = 50. Adding this sensitivity line
     would answer the obvious objection.
   - Justify the tolerance of 0.15 for a stated FPR of 0.10.
6. **Exploratory geography P value.**
   - P = 0.0008 is the smallest of at least four comparisons in `explore_v5.json`: EUNA vs non-westernised grouping,
     LASSO and RF. The grouping shown in bold in Figure 1B (non-westernised) gives P = 0.0035. Report all four, or
     adjust for them.
   - The "Europe and North America" list includes Israel and Kazakhstan. Kazakhstan matters for the replication
     (CosteaPI_2017, index −0.03); counting it as outside EUNA would give 5 vs 14 populations, not 4 vs 15. Say
     "Europe, North America, Israel and Kazakhstan", or justify the list.
7. **Multiplicity.** The Letter reports about 10 P values with no adjustment and no statement of family. The v4 analyses
   it draws on were Holm-adjusted over a 34-test family (`holm_v6.csv`); for example, "control augmentation P = 0.58" is
   from that family. Add a supplementary table listing every P value with its status (confirmatory / replication /
   exploratory / post hoc), its family, and its Holm-adjusted value where applicable. Mark P values in the text
   accordingly.
8. **Small evidence base for the cross-site claim.** "Across sites, it broke … 0.057 to 0.078" rests on 2 populations
   and 30 units at N = 100 (si_tables_v4 Table S4, stress/subsite). The neighbour design is similarly small. Give the
   number of populations and a CI, and soften "broke" to "did not transfer in the two multi-site cohorts we could test".
9. **Recalibration price.** The training cut-off's sensitivity of 0.46 comes at an FPR of 0.29 in these cohorts
   (`deploy_v4_cc_summary.csv`, SRC). Even with π = 0, the burn-in gives a sensitivity of 0.246. Most of the "fall" is
   therefore the move from FPR 0.29 to 0.10, not patient contamination. The text half-says this through the labelled
   comparison (0.245); state it directly. These results come from 3 populations and 6 units.
10. **Leakage and duplicates.** The r > 0.99 threshold catches technical duplicates, not repeat sampling of the same
    person. The v4 r > 0.95 sensitivity found additional near-duplicate pairs, including LeChatelierE_2013 ~
    MetaCardis_2020_a (4 pairs) and JieZ_2017 ~ QinJ_2012 (2 pairs). MetaCardis is the training cohort for CAD, HF and
    IGT, and JieZ is the training cohort for ACVD, while LeChatelier and QinJ are test populations. Either check subject
    overlap from metadata, or re-run the r > 0.95 sensitivity for the v5 tests. The effect is probably small, but it
    should be shown.
11. **Analysis code frozen with the results, not before.** analyse_v5.py was committed together with the results
    (e59cd78), three minutes after the plan. Implementation choices made in that code were therefore not fixed in
    advance: the 0.5 correction, DL, t_{k−2}, the ≥ 120 population size for H4, and the covariate-half rules. Say so in
    the deviations section.
12. **Population ≠ biology.** The "population" effect includes extraction kit, sequencing centre and depth. The text
    acknowledges this in Limitations. The "geography" and "IBD markers of health" paragraphs should carry the same
    caveat inline, because readers will take them as biological.
13. **Pooled CAD value.** CAD pooled FPR = 0.1151 for LASSO and 0.108 for RF; "CAD 0.12" is fine for LASSO, but say
    "LASSO". Figure 1C shows ≈ 0.11.
14. **Figure 2A legend.** The panel legend reads "PAC rule (δ = 0.05)"; the figure legend reads "rule bounding
    P(FPR > 0.10) at 0.05". Harmonise them, and say in the panel that the y-axis is P(FPR > 0.15) for both rules.

---

## Numbers I could not reconcile with the result files

| Text claim | Result file value | Status |
|---|---|---|
| "95% prediction interval … reached 0.34 to 0.81 at its upper end for LASSO" | `v5_het_strict.csv`: LASSO pi_hi range 0.218 (CRC) – 0.809 (IGT) | **Incorrect lower bound (0.22)** |
| "pre-stated hypothesis that the population would explain at least a quarter" | protocol_v5 H2: "≥ 20% … WRONG if < 10%" | **Threshold misquoted** |
| H3 "This falsified our expectation" | protocol WRONG = no taxon in ≥ 3 tests; observed 2 taxa in 3 tests | **Verdict mislabelled (not supported, not falsified)** |
| Burn-in on "the younger, leaner or one-sex half" | `analyse_v5.py` / `v5_h4_units.csv`: designs = accession, cov_age, cov_BMI only | **No sex design in v5** |
| "the test–population pair for the remaining 62% (47% for RF)" | Residual includes binomial noise (si_tables_v11 S3 header); ≈ 55% / 32% after crude noise removal | **Mislabelled component** |
| IBD over-flagging explained by Gemmiger / R. bromii (S3) for the populations at FPR 0.45–0.76 | Decomposition is from the v4 IBD model (v4 max n ≥ 100 FPR 0.467); the FPRs are from the v5 model | **Different models** |
| "Tables S1–S15" | si_tables_v11.md: S1a–S8 plus S9–S23 | **Numbering mismatch** |
| SI S2 / S3 / S4 cross-references | supporting_information_v4.md: S2 = plans, S3 = revision history, S4 = failed fixes | **Section mismatch** |

Verified as correct:

- **Atlas and heterogeneity:** 36 populations, 6,525 people, 20 countries; full set 55 / 8,160; 119 duplicates; 489
  LASSO pairs; 45% / 26% / 24%; range 0–0.77 in populations with n ≥ 100; I² 28/28, median 0.94, range 0.64–0.97;
  full-set median 0.92; outside band 15–16% expected vs 50–97% observed (median 66%); pooled CRC 0.06, ACVD 0.10,
  CAD 0.12.
- **AUROC:** Spearman ρ −0.06, P = 0.76; 16 classifiers with AUROC ≥ 0.65.
- **Variance shares:** 17% / 7.5%, 21% / 46%, 62% / 47% (as computed, subject to M1).
- **Taxa and IBD populations:** two taxa in three tests; IBD top-six populations (IND, JPN, CHN) at 0.45–0.76.
- **Geography and replication:** medians 0.35 vs −0.26, P = 0.0008; distance 12/14; replication 10/14, P = 0.090;
  geography +0.25, P = 0.30, four non-EUNA populations.
- **Burn-in law and H4:** P(FPR > 0.15) = 0.055 (N = 100) and 0.015 (N = 200); 646 evaluations, 13 populations,
  0.101 → 0.038, −62%, 28/28, P = 7 × 10⁻⁹, 75%.
- **Verification power:** 0.98, 0.72, 3.3%, and 91% at n = 50.
- **v4-derived numbers:** covariate population share 15–49%; augmentation 0.087 → 0.078, P = 0.58; cross-site 0.057 →
  0.078; contamination FPR 0.075–0.087, sensitivity 0.46 → 0.21–0.23, labelled-controls sensitivity 0.245; fprcal
  atlas 32–36 populations.
