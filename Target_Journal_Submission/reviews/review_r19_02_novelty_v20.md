# Review r19-02 (Reviewer 2: novelty and related work), manuscript v20

Manuscript: "Gut-microbiome disease classifiers flag 0 to 87% of healthy people at the same cut-off, depending on the population" (Letter, iMeta).

Materials read: manuscript_v20.md, supporting_information_v20.md, si_tables_v16.md (skimmed), highlights.md, cover_letter_v20.md, all figure PNGs, protocol_v6.md, and the v6 result file list. I checked the key prior papers myself: I read the full texts of SIAMCAT (Wirbel 2021), GMWI2 (Chang 2024) and GMHI (Gupta 2020) through Europe PMC, and the CRC-TrustBench abstract through Crossref. Crossref confirms the 2025 to 2026 references exist with the cited titles.

## 1. What is claimed as new

The Letter frames three contributions:
1. An atlas: the FPR at a fixed cut-off (90th percentile of out-of-fold control scores, target FPR 0.10) of 28 classifiers for 14 diseases across 36 healthy general-population cohorts, with heterogeneity statistics (I-squared, tau, prediction intervals), and the finding that AUROC does not predict the spread.
2. An audit of two released indices: GMWI2 and GMHI flag a median of 64% and 67% of healthy people in their own East Asian training studies, against 12% and 21% elsewhere; retraining the GMWI2 recipe links this to the geographic make-up of the training data.
3. A site-level fix: a known order-statistic (split-conformal) rule on 100 unlabelled local people cuts the FPR error by 62% within sites.

The Letter is careful and mostly well calibrated about priority. It does not claim to have discovered the spectrum effect, the conformal rule, or that cross-study transfer inflates false positives. It positions itself as the first systematic map across diseases and healthy populations. My job is to test whether that positioning survives contact with the cited prior work.

## 2. The central novelty claim stands, but it is closer to the Wirbel 2021 (SIAMCAT) result than the manuscript admits

This is the most important point of my review. The manuscript's single sentence on SIAMCAT (ref 10) is:
"controls from other studies doubled the false positives of CRC classifiers [10]".

I read SIAMCAT in full. What Wirbel et al. actually did is substantially closer to this paper's core method than that clause conveys:
- They ran a large ML meta-analysis (130 classification tasks, 50 gut metagenomic studies).
- They defined an "elevated false-positive rate (FPR)" as the central portability failure, measured at "a cutoff adjusted to maintain a FPR of 10% on the cross-validation set" — the identical cut-off rule this paper uses.
- They found "a more than twofold increase in false positives on average" on external datasets, and ">2-fold increase in FPR" across studies, with ">2.5-fold elevated FPR" for cross-disease transfer.
- They proposed "control augmentation" (adding external controls during CV) as the fix, which this paper also tested and reports as failing (S4).

So the qualitative finding — that a 10%-FPR cut-off does not hold on external controls and that the FPR roughly doubles — is already in SIAMCAT, at scale, for the same metric. This paper's genuine, defensible increments over SIAMCAT are:
(a) breadth: 14 diseases including many non-CRC/IBD/T2D conditions, and healthy general-population cohorts (not just case-control study controls) as the test set;
(b) the full per-population distribution (0 to 0.87) and formal heterogeneity (I-squared, tau, prediction interval for a new population) rather than an average fold-change;
(c) the AUROC-does-not-predict-spread result;
(d) the audit of released, deployed indices (GMWI2/GMHI) rather than research models;
(e) the geographic mechanism via retraining;
(f) the released atlas + tool.

These are real and, taken together, clear the novelty bar. But the manuscript under-credits SIAMCAT. A reader who has not read ref 10 would believe this paper first showed that a fixed-FPR microbiome cut-off breaks on external controls, when SIAMCAT showed exactly that with the same metric. The one-clause citation ("doubled the false positives") actually understates how close the prior result is, which paradoxically weakens the authors' own honesty signal. I recommend an explicit sentence in the intro or discussion acknowledging that SIAMCAT first documented the ~2-fold external FPR inflation at a 10%-FPR cut-off, and stating precisely what this paper adds (breadth across diseases and healthy populations, the distribution and its heterogeneity, the audit of released indices, the geographic mechanism). This is a calibration fix, not a fatal novelty problem.

## 3. The GMWI2/GMHI "East Asian" audit is genuinely novel and well credited

I searched for any published critique showing that GMWI/GMWI2/GMHI mislabels healthy East Asian (Chinese/Japanese) cohorts. I did not find one. The GMWI2 and GMHI papers themselves acknowledge only a generic prevalence-method bias and under-representation of some geographies; neither quantifies an East Asian false-positive excess, and I found no third-party paper that does. The quantitative audit here — median 64% flagged in East Asian training studies vs 12% elsewhere (GMWI2), replicated in GMHI (67% vs 21%), with the in-training-data demonstration in Figure 2A and S2A — appears to be new. This is the strongest novelty element of the Letter: it turns a vague acknowledged limitation into a measured effect in the developers' own published scores, which is hard to dismiss.

Credit here is fair. The manuscript states plainly that "others have noted such biases [10, 12, 22]", and refs 10/12/22 are appropriate (SIAMCAT, Poyet industrialization, and the GMHI paper itself). It is explicit that these are properties of the models and training data, not claims about East Asian microbiomes, and that country is confounded with laboratory/sequencing. The retraining experiment (Figure 2D) that links the effect to case-mix is, as far as I can find, a new contribution. The honest reporting that the balancing intervention's CI (41 to 149%) does not exclude smaller reductions, and that it fails on the FPR scale and costs discrimination, is appropriately calibrated and if anything over-modest.

One caveat on novelty framing: GMHI shares 83% of its healthy training samples with GMWI2, which the manuscript discloses ("a replication in a second model, not in independent data"). Good. But the highlights and graphical abstract present "two released gut-health indices" as if they were two independent lines of evidence. The main text qualifies it; the highlights ("the two share most training studies") just barely does. Keep the qualifier visible wherever the "two indices" headline appears, so the replication is not oversold.

## 4. The conformal/NP calibration contribution is correctly presented as "not new"

The manuscript is scrupulous here: "The rule is not new" (refs 24, 25 Lei/Bates split-conformal; 27 Tong NP classification; 26 Saerens prior-shift; 14 imaging drift; 28 laboratory reference intervals). The site-level fix is framed as an application, not a method contribution, and the honesty is appropriate. No novelty inflation. The contribution that is new — that this specific label-free rule, run within a site on 100 people, recovers the FPR for microbiome classifiers in retrospective non-random splits (and fails across sites) — is modest but correctly scoped. The conformal citations are apt and I have no priority concern here.

## 5. Related-work coverage: adequate, with gaps

Prior work is cited competently. The spectrum-effect literature (8, 9), He 2018 regional reference ranges (11), Poyet industrialization (12), CRC-TrustBench (13), imaging drift (14), the 20-disease benchmark (15), the best-practices guide (16), the AI-readiness audit (17), and laboratory reference-interval verification (18, 28) together place the work well. CRC-TrustBench (13) is correctly characterised: its abstract confirms it is a leakage-aware CRC benchmark that evaluates LOSO/LOCO AUROC and probability calibration (Platt, conformal-style, Brier) but does not map fixed-cut-off FPR across healthy populations or diseases — so it is adjacent, not pre-emptive. Good.

Gaps I would want addressed:
- SIAMCAT credit (Section 2) is the main one.
- The "What is missing is a map..." sentence overstates the void given SIAMCAT and the 20-disease benchmark (15). Soften to "a cross-disease map across healthy general populations".
- hiPCA / other health indices: I could not find a published head-to-head, but there are additional released health indices (e.g. PCA-based health indices, 2023 Microbiome) that the Letter could mention in one clause to show the audit generalises beyond GMWI2/GMHI, or to scope the claim ("two released indices we could obtain and verify").

## 6. Minor novelty/credit points
- "AUROC does not warn when it is off" / "AUROC does not predict the spread" (rho = -0.06). This is a clean, apparently new observation for this setting, well supported by Figure 1D. Fairly claimed.
- The profiler-version sensitivity of GMHI's cut-off (23% to 43%, MetaPhlAn2 vs 3; Figure S2B) is a nice, apparently novel point. Correctly labelled post hoc and the authors wisely decline to over-interpret the cMD transfer (Q2 gate failed).
- The three recommendations (report FPR per held-out population next to AUROC; check training case mix; verify/reset local cut-off) are sensible and framed as proposals, not discoveries. Good.

## 7. Assessment against scorecard dimension 3 (Novelty vs prior art)

Benchmark P75 for dimension 3 is 7.0 (max 8, top example imt2.70192). The question a novelty reviewer must answer: does this paper "ask a question the field has not asked, or overturn a widely held assumption, with evidence" (anchor 9), or is it "a new angle or new combination of known methods; result partly anticipated" (anchor 6)?

My honest read: the atlas result is partly anticipated by SIAMCAT (anchor 6 territory for that piece), but the released-index East Asian audit with the retraining mechanism is a question the field has not answered and overturns the implicit assumption that a published, globally-trained wellness index carries a stable cut-off (anchor 8 to 9 territory for that piece). The combination, with the honest failed-hypothesis reporting, lands at a 7 — at P75, not above it. It would reach 8 if Section 2 (explicit SIAMCAT delineation) were fixed, because the paper's true increment would then be legible rather than blurred.

## 8. Decision

The work is novel enough for iMeta as a Letter, the credit is mostly fair, and the novelty claims are calibrated with one real exception (SIAMCAT). The required fixes are textual, not new experiments: (i) explicitly delineate the increment over SIAMCAT; (ii) keep the GMHI-shares-training-data qualifier visible in highlights/graphical abstract; (iii) soften "what is missing is a map". These are minor-revision items from a novelty standpoint. I therefore recommend minor revision.

## MAJOR concerns
- M1 (credit calibration, SIAMCAT). The core atlas finding — that a 10%-FPR cut-off breaks on external controls, with the FPR roughly doubling — was already shown by Wirbel 2021 (SIAMCAT) using the same 10%-FPR cut-off metric at scale (130 tasks, 50 studies), and SIAMCAT also introduced control augmentation as the fix this paper re-tests. The manuscript reduces this to one clause ("doubled the false positives of CRC classifiers [10]"). The paper must add an explicit sentence stating what SIAMCAT established and precisely what this paper adds beyond it (breadth across 14 diseases and healthy general populations, the full per-population distribution and heterogeneity/prediction intervals, the AUROC-null result, the audit of released deployed indices, and the geographic retraining mechanism). As written, a reader could mistake the atlas's qualitative headline for a first discovery. This is the one place where novelty is over-implied; it is fixable in text.

## MINOR concerns
- m1. "What is missing is a map of how far the FPR at a fixed cut-off varies across diseases and healthy populations" overstates the gap given SIAMCAT and the 20-disease benchmark (15). Re-scope to "a cross-disease map across healthy general populations, with per-population distributions".
- m2. Highlights and the graphical abstract present GMWI2 and GMHI as "two released indices" without the shared-training-data caveat that the main text gives (83% overlap, "replication in a second model, not independent data"). Keep that qualifier wherever the two-index headline appears, so the replication is not read as independent confirmation.
- m3. Consider one clause acknowledging other released health indices beyond GMWI2/GMHI (e.g. PCA-based indices), to scope the audit claim and show the phenomenon is not specific to one lab's model.
- m4. The intro clause on Poyet (12), He 2018 (11) and SIAMCAT (10) lists them as single-disease/region precedents; good, but the sentence could note that these established the phenomenon qualitatively and that the present contribution is the systematic, quantitative, cross-disease map plus the released-index audit — making the novelty delta explicit in the intro rather than only implicit.
- m5. The conformal section is correctly credited as "not new"; no change needed, but ensure the Neyman-Pearson (27) and split-conformal (24, 25) attributions remain if the site-fix section is shortened in revision, since they are what keep the method claim honest.

## Scorecard dimension scores (1-10; P75 in brackets)
1. Biological / clinical significance: 8 (P75 8)
2. Scale and breadth of data: 8 (P75 8)
3. Novelty vs prior art: 7 (P75 7) — would be 8 with the SIAMCAT delineation fixed
4. Methodological rigor and statistics: 8 (P75 7.25)
5. External validation / cross-cohort generalisation: 8 (P75 7)
6. Resource / tool value for readers: 7 (P75 5.75)
7. Figure quality and visual story: 7 (P75 7)
8. Clarity, framing and writing: 8 (P75 7.25)
9. Reproducibility and openness: 8 (P75 7.25)
10. Actionable insight / mechanism: 8 (P75 7)

Total: 77/100 (benchmark P75 total 69.25).

## DECISION
Score 8/10. Decision: MINOR revision. Novel and fairly credited overall; the one required fix is an explicit delineation of the increment over SIAMCAT (Wirbel 2021), which currently blurs where the atlas's novelty begins. The GMWI2/GMHI East Asian audit with its retraining mechanism is a genuinely new, well-calibrated contribution, and the conformal/NP calibration is correctly presented as not new.
