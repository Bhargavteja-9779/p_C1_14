# Submission report: manuscript v22 for iMeta (Letter / Short Communication)

**Title:** Gut-microbiome disease classifiers set for a 10% false-positive rate miss it in most healthy populations

## 1. What the paper shows
1. **Atlas.** 28 classifiers (LASSO and random forest, 14 diseases), each with a cut-off set for a 10% false-positive
   rate (FPR), scored in 36 groups of healthy adults (6,525 people, 20 countries). In 70% of classifier–population
   pairs the FPR fell outside 5–15%, against about 15% expected by chance; heterogeneity exceeded sampling noise for
   every classifier (I² median 0.94). A higher AUROC did not mean a smaller spread.
2. **Robustness to how the cut-off is applied (new in v21–v22).** Scoring with the cross-validation models behind the
   cut-off keeps the heterogeneity (28/28 classifiers; 65% outside 5–15%) but shrinks the most extreme LASSO values.
3. **Audits of two released indices.** GMWI2 and GMHI labelled a median of 64% and 67% of healthy people in their own
   East Asian training studies as non-healthy (12% and 21% elsewhere). They share most training data, so the second is
   a replication in a second model. Retraining GMWI2 linked the effect to the geographic make-up of the training data.
4. **Site fix.** A known order-statistic burn-in on 100 unlabelled local people cut the within-site FPR error by 62%
   (retrospective), failed across sites and costs sensitivity. Released as `fprcal` (19 tests pass).

## 2. Review history (blind reviewers, 10-point scale; scorecard total /100, benchmark P75 total 69.25)

| Round (version) | Statistics | Novelty | Editor | Totals /100 | Status |
|---|---|---|---|---|---|
| r12 (v14) | 8 | 8 | 7.5 | 76 | minor |
| r16 (v17) | — | — | ready after minor changes | 77 | clarity below P75 |
| r17 (v18) | — | — | send to review | 73 | clarity, reproducibility below P75 |
| r18 (v19) | — | — | minor | 76 | clarity below P75 |
| r19 (v20) | 7 minor | 8 minor | 7 minor | 72 / 77 / 73 | fold-model issue found |
| **r20 (v21)** | **7.5 minor** | **8 minor (no MAJOR)** | **7 minor** | **75 / 78 / 74** | second clean panel in a row |
| r21 (v22 draft) | — | — | minor (clarity check) | 75 | 4 required wording items, all done in final v22 |

v22 answers the r20 and r21 items (see `reviews/round_20_triage.md` and `reviews/round_21_triage.md`).

## 3. Against the benchmark (P75 of 12 published iMeta papers on the same 10 dimensions)
In r20, all three reviewers put 9 of 10 dimensions at or above P75. **Clarity** was scored 7, 8 and 6 against a P75 of
7.25: one reviewer above, two at or below. A blind clarity check of the v22 draft (r21) again gave 7; its four required items
(highlight wording, a "Here we" opening with both headline numbers, percent notation, fewer numbers in the burn-in
section) are done in the final v22 and have not been re-scored. Reproducibility is held back mainly by the private repository.

## 4. Acceptance assessment
Reviewers' estimates: about 45% (range 35–55%) if the repository is public and the developers have had a right of
reply; about 30% otherwise. For: clear practical message, field-wide data, released-index audit (novelty reviewers
found no prior report), honest reporting of failed hypotheses and post hoc checks, a tested tool. Against: the
spectrum effect and the recalibration rule are known; the two indices share training data; all site results are
retrospective; the Letter is statistically dense. These are model-based estimates from simulated reviews, not a
guarantee.

## 5. Author actions before submission
See README.md. In addition, the AI-use statement must describe the simulated editor/reviewer checks that plans v6 and v7
name as their motivation (SI S5).
