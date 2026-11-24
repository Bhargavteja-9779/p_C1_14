# Referee report (round 3): novelty and related work, manuscript_v4

**Score:** 6/10
**Decision:** Major revision. Most of the work is reframing and citing, but concern 4 may need one more comparator.

## Overall assessment

The paper's real contribution is empirical, and it is useful. No paper I found measures the realised FPR of fixed-cut-off microbiome classifiers in each of ~36 general-population healthy cohorts. None reports it with I², prediction intervals and a taxon-level account of the drift, then tests cohort-borrowing corrections against a site-local, label-free re-threshold. The authors already say the burn-in rule is "an adaptation of known tools, not a new method", which is right.

The novelty framing has problems, though:
- It understates SIAMCAT (2021), which did measure FPR on external controls.
- It leaves out the main literature on label-free and site-specific recalibration, in both clinical prediction modelling and medical AI.
- It drops two close microbiome papers: CRC-TrustBench, which was in earlier drafts, and the Global Microbiome Conservancy analysis.
- It mischaracterises DEBIAS-M.
- The title and conclusion claim more than the burn-in evidence supports. That evidence rests on 7 locked populations, and the within-site threshold was missed (48% versus the pre-stated 50%).

## Claim → closest prior work → exact difference

| # | Manuscript claim | Closest prior work (opened) | Exact difference |
|---|---|---|---|
| C1 | "No study has measured the FPR of fixed-specificity microbiome classifiers population by population across dozens of healthy cohorts." | Wirbel et al. 2021, SIAMCAT, Genome Biol, https://doi.org/10.1186/s13059-021-02306-1 (full text, PMC8008609). Cut-off at 10% FPR on CV controls; models applied to external control samples. They report "a more than twofold increase in false positives on average" and define portability as "maintenance of type I error control on external control samples". | SIAMCAT already measured external-control FPR at a fixed cut-off, study by study. It did not focus on healthy general-population cohorts or work at this scale (36 cohorts, 20 countries). It reported no heterogeneity or prediction intervals and no mechanism. The novelty claim should be narrowed to these features. |
| C1b | Same claim, CRC | Wirbel et al. 2019, Nat Med, https://doi.org/10.1038/s41591-019-0406-6 (PMC7984229): cut-off at FPR 0.1 on training controls; FPR 0.09–0.13 on other-disease cohorts. | The manuscript's pooled held-out-control figure (0.097) does not appear in the main text; it is in Source Data Fig. 3c. Cite it as such. |
| C1c | Cross-country reliability of CRC classifiers is unreported | Zhang et al. 2026, CRC-TrustBench, Front Microbiol, https://doi.org/10.3389/fmicb.2026.1971707 (full text): 15 studies and 10 countries, LOSO/LOCO, Platt calibration, conformal sets with "material undercoverage" at country level. | That paper deals with probability calibration and coverage at 0.5, not FPR at a fixed cut-off, and only for CRC. It is close and **not cited in v4**. |
| C2 | Non-westernised and Asian populations are over-flagged because the training cohorts' health-marker taxa are rarer there | Poyet et al. 2025, Global Microbiome Conservancy, bioRxiv, https://doi.org/10.1101/2025.10.20.683358 (abstract): "microbiome-based disease predictors trained on industrialized populations" lose accuracy in less industrialized cohorts. | The GMbC study shows the loss of accuracy at a general level. The manuscript adds per-cohort FPR and a taxon decomposition, mostly for Asian (industrialised) cohorts. Not cited. |
| C3 | Corrections borrowed from other cohorts (including control augmentation) do not fix the cut-off | SIAMCAT 2021 (above): augmentation "greatly improved" portability and "did not strongly depend on the set of controls used". | The manuscript finds no average gain (P = 0.58) and benefit only when the same population is in the pool. This directly contradicts SIAMCAT's robustness claim, and the text should say so. |
| C4 | Batch correction is not a substitute; MMUPHin, ConQuR and DEBIAS-M "need batch labels with cases or retraining" | Austin et al. 2025, DEBIAS-M, Nat Microbiol, https://doi.org/10.1038/s41564-025-01954-4 (PMC10888995): "we allow samples from both the training and test set to be used in the cross-batch similarity terms"; test labels are not used. Only AUROC is reported. | DEBIAS-M is label-free on the test batch by design, so it could be run on the same 100 burn-in people. The manuscript's description is inaccurate. The ComBat-style alignment is a weaker stand-in. |
| C5 | Recalibrate on the site's own ~100 unlabelled people; borrowed references fail | Roschewitz et al. 2023, UPA, Nat Commun, https://doi.org/10.1038/s41467-023-42396-y (abstract): label-free recalibration from "limited amounts of unlabelled" target data to correct operating-point drift that AUROC hides. Qiu et al. 2026, SACSIM, Biometrics, https://doi.org/10.1093/biomtc/ujag138 (abstract): adapts a Neyman–Pearson rule using "a small unlabeled sample from the target population". | The idea of a label-free, site-local re-threshold is established. The new part is a microbiome-specific test of when it breaks (cross-sub-site and cross-cohort burn-ins), with patients mixed in. Neither paper is cited. |
| C6 | The FPR "belongs to the test–population pair"; each site must recalibrate | Van Calster et al. 2023, BMC Med, https://doi.org/10.1186/s12916-023-02779-w (abstract): "we have to expect heterogeneity in model performance between locations and settings… prediction models are never truly validated". Janssen et al. 2008, J Clin Epidemiol, https://doi.org/10.1016/j.jclinepi.2007.04.018 (record): model updating in new patients. | The concept is established. The manuscript quantifies it for microbiome tests. Neither paper is cited; the authors' own novelty map lists Van Calster as "medium" closeness. |
| C7 | The burn-in order statistic controls FPR under contamination up to π_max | Bates et al. 2023 [14]; Tong et al. 2018 [16]; Bashari et al. 2025 [15] (arXiv:2502.04807, opened): a contaminated reference set gives conservative type-I control. | These are correctly cited, and the claim of no new method is appropriate. |

## Concerns

1. **MAJOR: SIAMCAT is under-described.** The introduction says only that Wirbel 2021 proposed augmentation. It does not say that they measured external-control FPR at a 10% cut-off across many studies and found a more than twofold increase. With that left out, the "to our knowledge, no study…" sentence reads as broader than it is.
   *Resolve:* State what SIAMCAT measured. Restate the novelty as: general-population healthy cohorts, scale, heterogeneity quantification (I² and prediction interval), taxon-level mechanism, and a head-to-head test of corrections. Discuss why the augmentation results differ from SIAMCAT's.

2. **MAJOR: Label-free and site-specific recalibration work is missing.** The clinical-prediction updating literature is absent (Janssen 2008; Van Calster 2023; Sperrin 2022 on targeted validation, which is in the authors' own map). So is the medical-AI literature on label-free operating-point correction (Roschewitz 2023 UPA; SACSIM 2026). Without it, a reader may think "recalibrate at each site" is a new prescription.
   *Resolve:* Add a short paragraph that cites these and positions the contribution as empirical evidence for microbiome tests, including where it fails (another sub-site or cohort).

3. **MAJOR: Close microbiome prior work has been dropped.** CRC-TrustBench (2026) was cited in earlier drafts, and the authors' citation audit recommended keeping it, but it is gone from v4. The GMbC analysis (Poyet et al. 2025) already reports that disease predictors trained on industrialised populations transfer poorly.
   *Resolve:* Cite both, and say what this study adds: FPR per cohort, the decomposition, and a wider set of diseases.

4. **MAJOR: DEBIAS-M is mischaracterised.** Its default mode is transductive and uses no test labels. It can therefore be fitted with the training data plus the site's 100 unlabelled people, which is exactly the burn-in setting. MMUPHin and ConQuR do need covariates or labels, so that part of the description is fair.
   *Resolve:* Either run DEBIAS-M with the burn-in group as the test batch and report the FPR, or correct the text and list it as an untested competitor in the setting the paper itself uses.

5. **MINOR: The title and conclusion overreach.** "Must be recalibrated at each site" and "a short… burn-in restores it" sit awkwardly with the evidence:
   - The locked comparisons rest on 7 populations, with Holm-adjusted P = 0.19 versus the training cut-off.
   - The pre-stated 50% threshold was missed.
   - The burn-in failed across sub-sites.
   - "Borrowed references do not" ignores the same-population augmentation success (India, FPR 0.62 to 0.03).

   *Resolve:* Soften the title, for example to "…should be checked and recalibrated locally". Make the conclusion conditional on the burn-in coming from the same site.

6. **MINOR: Reference hygiene.**
   - Reference 12 (Vujkovic-Cvijin 2020) is listed but never cited. Cite it in the covariate paragraph or remove it.
   - Reference 15: the arXiv page lists no venue. Confirm "Proc ICML 2025" with the proceedings (PMLR volume and pages) or cite it as arXiv.
   - Reference 1: the 0.097 figure is from Source Data Fig. 3c, not the main text. Point to it.
   - Reference 8 (Hiseni 2026) exists. "Six countries" is consistent with a Scandinavian reference plus five validation countries.
   - All 20 DOIs resolve on Crossref, and titles, journals and volumes match.

7. **MINOR: The heterogeneity claim should be set against diagnostic-accuracy precedent.** The finding that specificity varies between settings is long known for conventional tests (for example Leeflang 2013 in CMAJ, in the authors' own map). A single sentence would keep readers from taking the general phenomenon as new.

## Papers opened (by me)

- Full text: SIAMCAT 2021 (Europe PMC PMC8008609); Wirbel 2019 (PMC7984229); DEBIAS-M (PMC10888995); CRC-TrustBench (frontiersin.org).
- Abstract or record:
  - Bashari 2025 (arXiv abstract page)
  - SACSIM (EDRN page plus Crossref abstract)
  - Roschewitz 2023 UPA (Crossref abstract)
  - Van Calster 2023 (Crossref abstract)
  - Poyet 2025 GMbC (Crossref/bioRxiv abstract)
  - Janssen 2008 (Crossref record)
- Crossref metadata for all 21 manuscript references, including author lists for refs 7, 8, 17 and 18 and abstracts for refs 7, 17 and 18.
- Search phrasings used (12): FPR and specificity transfer across cohorts; site threshold recalibration; healthy reference / reference ranges; SIAMCAT control augmentation; MMUPHin, ConQuR, DEBIAS-M and PLSDA-batch prediction; NP calibration with contaminated or unlabelled data; clinical model updating (Janssen, Vergouwe, Steyerberg); non-westernised and Asian generalisation; GMbC disease predictors; label-free threshold adjustment in medical AI; GMWI2 per-cohort specificity; country-dependent specificity of CRC classifiers.
