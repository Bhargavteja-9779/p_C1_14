# Review r20_02 — Novelty and related work (Reviewer 2)

Manuscript: "Gut-microbiome disease classifiers set for a 10% false-positive rate miss it in most healthy populations" (Letter, iMeta), submission_final_v21.

Remit: judge what is new versus cited prior work (spectrum effect; conformal/Neyman-Pearson calibration; SIAMCAT; He 2018; GMHI/GMWI2); judge whether credit is fair and novelty claims are calibrated.

## Summary of what the paper claims as new

The paper states its own novelty explicitly and modestly in four places: the intro ("We extend the SIAMCAT observation in four ways"), the cover letter ("three contributions"), the retraining section ("Others have noted such biases [10, 12, 22]; we measure their size for released indices and test them by retraining"), and the site-fix section ("The rule is not new"). The claimed contributions are:

1. A cross-disease, cohort-by-cohort atlas of the realised FPR of fixed-cut-off microbiome classifiers in healthy general populations (28 classifiers x 36 populations), with heterogeneity statistics (I2, tau), prediction intervals for a new population, and a test of whether AUROC predicts the spread.
2. An audit of two released gut-health indices (GMWI2, GMHI) showing geographic miscalibration within the developers' own training data, plus a retraining experiment attributing it to training-data case mix.
3. A label-free site-level recalibration rule (order statistic / split-conformal) and a binomial verification check, with a tested tool (fprcal).

## Assessment of novelty against the named prior art

**Spectrum effect (refs 8, 9).** Credit is fair and calibrated. The paper does not claim to have discovered population-dependent specificity; it names the clinical-epidemiology concept explicitly ("the spectrum effect") and frames its work as applying/quantifying it in microbiome classifiers. This is the correct framing and avoids the common overclaim.

**SIAMCAT (ref 10, Wirbel 2021).** This is the closest and most important prior work, and the paper is right to anchor on it. SIAMCAT set cut-offs for FPR 0.10 and showed that external-study controls roughly doubled the false positives across many case-control tasks, and proposed control augmentation. The manuscript's "we extend the SIAMCAT observation in four ways" is accurate and the four extensions are genuine and non-trivial: (a) scoring healthy general/population cohorts rather than other studies' case-control controls; (b) quantifying spread with heterogeneity statistics and prediction intervals rather than a pooled doubling; (c) testing whether AUROC predicts the spread (a negative result that is new and useful); (d) extending from case-control tasks to released deployed indices. Critically, the paper does not silently reuse SIAMCAT's own remedy as novel — it reports that control augmentation (Wirbel et al.) was tried and gave no overall gain (S4), which is the fair way to treat a competitor's method. Credit is fair; the incremental-over-SIAMCAT nature is disclosed rather than hidden.

**He 2018 (ref 11).** Fairly credited as prior evidence that reference ranges and disease models do not transfer between regions/districts. The paper positions its contribution as going beyond "reference ranges did not transfer" to a quantified, cross-disease FPR atlas with a deployed-tool fix. Calibrated.

**GMHI / GMWI2 (refs 20, 22).** The audit is the most novel empirical contribution. My web search did not find a published study that measures GMWI2's or GMHI's within-training-data geographic miscalibration or that retrains the GMWI2 recipe to attribute the gap to case mix. The GMWI2 and GMHI papers themselves report pooled balanced accuracy and, in GMWI2, uneven per-class rates and a "reject option", but not a per-study East-Asian-vs-other false-positive breakdown in the training data. Independent follow-ups I could locate (hiPCA, Q2PD, GMI, the East-Asian-distinct-microbiome eLife work) compare indices or note regional distinctness, but none audit GMHI/GMWI2's own training-data miscalibration by region and test it by retraining. So the specific finding (median 64%/67% of healthy East Asians in the developers' own data flagged non-healthy, linked by leave-one-study-out retraining to a 62%/20% case-mix imbalance) appears genuinely new. The paper also credits the GMHI authors for noting prevalence-based biases ("Others have noted such biases [10, 12, 22]") and frames its own contribution as measuring the size and testing by retraining — correctly calibrated.

**Conformal / Neyman-Pearson calibration (refs 24-27).** This is where the paper is most careful and most at risk of over- or under-claiming, and it lands on the right side. It states plainly "The rule is not new" and cites split-conformal (Lei 2018, Bates 2023), prior-shift correction (Saerens 2002), and the NP-ROC bound (Tong 2018). It also cites the medical-imaging operating-point-correction precedent (Roschewitz 2023, ref 14) and laboratory reference-limit practice (refs 18, 28). The novelty claimed here is only the application to microbiome site deployment plus the retrospective within-site evaluation and the tool — which is appropriate and honest. There is no attempt to dress up the order-statistic rule as a statistical innovation.

**DEBIAS-M / MMUPHin / ConQuR (refs 32-34).** Fairly cited as batch/processing-bias correctors not evaluated here, with an explicit limitation that they were not run and a recommendation that such methods be judged by delivered FPR. Calibrated.

## Where the novelty is strongest and where it is thin

Strongest: (1) the AUROC-does-not-predict-spread negative result (rho = -0.06, CI -0.42 to 0.32) is a clean, new, field-relevant finding that directly challenges the standard benchmarking practice; (2) the released-index audit with a retraining mechanism; (3) the breadth (14 diseases x 36 healthy populations) goes well beyond SIAMCAT's case-control scope.

Thinnest: the site-fix is explicitly "not new" as a method, and its within-site demonstration is retrospective and in healthy-only groups. The authors say this clearly, so it is not an overclaim, but reviewers weighing novelty should note that contribution 3 is an application/packaging contribution, not a methodological one.

## Fairness of credit — concerns

The citation hygiene is unusually good for this kind of Letter. I did not find instances of a known method or prior finding being presented as original. The one area that merits a closer look is the framing of the atlas relative to the recent cross-cohort benchmark literature.

## MAJOR concerns

None. There is no novelty overclaim, no uncredited prior method, and no mis-attribution of a competitor's result. The core empirical findings (released-index geographic audit + retraining; AUROC does not predict FPR spread) appear to be new to the literature as far as I can verify.

## MINOR concerns

1. Relation to the newest cross-cohort CRC/benchmark work is under-developed. Refs 13 (CRC-TrustBench), 15 and 16 (Li et al. cross-cohort diagnostic best-practice papers) are cited only in a single sentence ("Cross-cohort benchmarks still report AUROC"). Given that this literature is the paper's foil, one or two sentences distinguishing the atlas from these benchmarks (they report AUROC/transfer; the atlas reports realised FPR at a fixed cut-off in healthy populations) would sharpen the novelty claim and pre-empt a "this is just more cross-cohort benchmarking" reaction. The distinction is real but currently left implicit.

2. The industrialization paper (ref 12, Poyet/Rühlemann, Cell 2026) reports that "microbiome-based disease predictors trained on industrialized populations are uninformative in less industrialized cohorts." This is close in spirit to the atlas finding and is cited only in passing ("predictors trained on industrialised populations failed elsewhere [12]"). Because it is concurrent and overlapping, a sentence stating what this paper adds beyond it (a per-population FPR atlas with calibration statistics and a fix, versus a loss-of-information observation) would protect the novelty claim.

3. The "known order-statistic rule" (contribution 3) is honestly flagged as not new, but the manuscript cites the medical-imaging precedent (ref 14) twice as support for the whole idea of correcting operating points from unlabelled site data. A reader could ask why the microbiome application is a contribution if imaging already does this. The answer (microbiome deployment has no such practice, and the paper supplies the per-population evidence that it is needed plus a packaged tool) is implicit; making it explicit in one clause would help.

4. Minor: the abstract/highlights lead with the 70%/64%/67%/62% numbers, which is fine, but the genuinely novel conceptual result — AUROC does not predict the spread — is buried in the fourth paragraph of the intro and panel 1D. For a novelty reviewer this is the single most surprising and citable finding; consider elevating it.

## Scorecard dimension scores (1-10; P75 in parentheses)

Only dimension 3 is within my remit to judge closely; I give the others as context, weighted toward novelty/related-work considerations.

1. Biological / clinical significance — 8 (P75 8)
2. Scale and breadth of data — 8 (P75 8)
3. Novelty vs prior art — 8 (P75 7)
4. Methodological rigor and statistics — 8 (P75 7.25)
5. External validation / cross-cohort generalisation — 8 (P75 7)
6. Resource / tool value for readers — 7 (P75 5.75)
7. Figure quality and visual story — 7 (P75 7)
8. Clarity, framing and writing — 8 (P75 7.25)
9. Reproducibility and openness — 8 (P75 7.25)
10. Actionable insight / mechanism — 8 (P75 7)

Novelty rationale (dim 3 = 8): the paper asks a question the field has largely not asked at a fixed operating point (realised FPR of deployed microbiome tests across healthy populations), delivers a negative result that undercuts the standard AUROC-only benchmarking practice, and adds a released-index geographic audit with a retraining mechanism that I could not find in the prior literature. It falls short of 9 because two of its three headline contributions build directly on SIAMCAT and on a known calibration rule, and it is explicit and correct about that. Above P75 (7).

## Overall

Score: 8/10
Decision: minor revision

The novelty is real and, unusually, is neither overclaimed nor undersold; credit to SIAMCAT, the spectrum-effect literature, He 2018, the conformal/NP work and the GMHI/GMWI2 developers is fair and calibrated. The minor concerns are all about sharpening the paper's position relative to concurrent cross-cohort benchmark work (refs 12, 13, 15, 16) and elevating its most original finding, not about any misattribution.

Decision: minor
