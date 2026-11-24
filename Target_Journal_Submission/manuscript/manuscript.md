<!-- DRAFT v0.1 (2026-11-24). Numbers marked [[...]] are filled from results/main_tables.md after the locked run.
Format: iMeta Letter / Short Communication, target ~2,100 words, 2 figures, ~20 references, Methods in SI. -->

# Stool-metagenome classifiers miss their intended false-positive rate in new laboratories, and a label-free rank rule fixes it

**Short title:** Setting the decision threshold of microbiome tests at a new site

To the Editor,

Gut-microbiome classifiers can separate patients with colorectal cancer (CRC), inflammatory bowel disease (IBD) or
type 2 diabetes (T2D) from healthy people across many cohorts [1-4]. Most studies report this as the area under the
receiver operating characteristic curve (AUROC). A test that is used in practice, however, needs one fixed cut-off. The
cut-off decides how many healthy people are sent for a colonoscopy and how many cancers are found. A laboratory that
adopts a published classifier usually keeps the cut-off chosen on the training cohorts, for example the score that gave
90% specificity there. Nobody has checked whether that promise holds in a new laboratory, where DNA extraction,
sequencing and the population all differ [5, 6].

Here, we asked a simple question: when a microbiome classifier is moved to a new cohort, does it keep its intended
false-positive rate (FPR)? We used 19 public studies from curatedMetagenomicData [7] across four tasks (CRC, IBD, T2D
and colorectal adenoma; 3,626 unique stool metagenomes, 24 cohort-task pairs). We found that the training cut-off gives FPRs from [[x]] to
[[y]] at new cohorts, although the AUROC stays good. Popular label-free fixes from machine learning make this worse at
screening prevalence. A simple rule fixes it: set the cut-off at a fixed rank among the laboratory's own first,
unlabelled screening samples. The rule needs no diagnoses, comes with a finite-sample guarantee, and tells a laboratory
how many samples it must collect first (Figure 1, Figure 2).

## THE TRAINING CUT-OFF DOES NOT TRANSFER, AND AUROC HIDES THIS

We trained two standard classifiers, LASSO logistic regression and random forest, on eight development CRC cohorts.
We set the cut-off for 90% specificity on out-of-fold training scores, as is common practice [2, 8]. We then locked
16 test cohorts before any method was designed: three external CRC cohorts, and every cohort of IBD, T2D and adenoma
(Supporting Information, Table S1).

At the locked cohorts, the realised FPR of the training cut-off ranged from [[min]] to [[max]] (Figure 1A). The
spread was far larger than chance: a binomial test of overdispersion gave P = [[p]] (LASSO) and P = [[p]] (random
forest). The AUROC did not warn about this. Cohorts with similar AUROC had very different FPRs (Figure 1B). Averages
also hide the problem. For the random forest, the mean FPR over development cohorts was close to the target (0.092),
but single cohorts missed it in both directions (cohort root-mean-square error, RMSE, 0.125).

The shift is tied to the study, not only to the country. In development cohorts, a cut-off set on the controls of one
study and used in another study from the same country gave an FPR of 0.33 (two Italian studies) and 0.87 (two US
studies) instead of 0.10 (Figure 1C). Differences in sample handling and sequencing are known to move microbiome
profiles [5, 6]; our results show that they move the cut-off most of all.

## LABEL-FREE FIXES FROM MACHINE LEARNING FAIL AT SCREENING PREVALENCE

A new laboratory has many unlabelled samples but few confirmed diagnoses. We therefore tested methods that adapt a
classifier with unlabelled data. These were label-shift correction by expectation-maximisation (EM) [9] and by maximum
likelihood with bias-corrected calibration [10], unsupervised two-component calibration as used in speaker
verification [11], our own location-scale mixture fit, and per-site feature standardisation, which was recently
reported to rescue fixed cut-offs in transcriptomics [12].

None of these methods was reliable when the unlabelled pool contained few patients, which is the normal case in
screening (Figure 2A). At a 1% case share, the cohort-RMSE of the FPR was [[em]] for EM, [[featstd]] for feature
standardisation and [[shift2]] for the mixture fit, compared with [[source]] for doing nothing. The reasons are
simple. Label-shift methods assume that the scores of healthy people do not move between sites, and they do.
Mixture fits cannot tell "the healthy scores moved up" from "there are some patients", so with few patients they
invent them [11]. Standardising each site removes the site's average, but a screening pool and a case-control study
have different averages because they contain different shares of patients. These methods only worked when about half
of the pool were patients, as in the case-control studies on which they are usually tested.

## A RANK RULE ON THE LABORATORY'S OWN SAMPLES KEEPS THE PROMISE

In screening, almost every sample is from a healthy person. We used this fact directly. The laboratory collects its
first n samples, scores them, and sets the cut-off at the r-th highest score. If at most a share pi_max of the pool are
patients, a choice of r based on order statistics gives a guarantee, in the spirit of classical tolerance limits [13]
and conformal prediction [14]. One version guarantees that the expected FPR is at most the target. A stricter version
guarantees that the FPR exceeds the target with probability at most delta. Patients in the pool can only make the rule
more cautious (Supporting Information, Note S1).

At the locked cohorts, the expected-FPR rule had a cohort-RMSE of [[rpoolmean]] at a 1% case share, against
[[source]] for the training cut-off (paired difference [[d]], 95% CI [[ci]], Holm-adjusted P = [[p]]; Figure 2A). It
matched the accuracy of ten labelled local controls ([[ctrl10]]) without any diagnoses. Results were the same for both
classifiers and all four diseases (Supporting Information, Table S2).

What does this mean for a screening programme? For CRC at 0.5% prevalence and a 10% target FPR, the training cut-off
sent [[x]] healthy people per 1,000 screened to colonoscopy instead of the intended 100. The rank rule sent [[y]]
(Figure 2B). The stricter version needs enough samples: about 360 screened samples if at most 1% are patients, 610 if
at most 5%, and 1,500 if at most 10% (Figure 2C). Smaller pools make it abstain, which is the honest answer.

## CONCLUSION

The cut-off of a microbiome test belongs to the laboratory, not to the published model. AUROC-based validation hides
this, and current label-free adaptation methods fail at screening prevalence. A rank rule on a few hundred of the
laboratory's own unlabelled samples restores the intended false-positive rate with a guarantee. We suggest that
microbiome diagnostic studies report the realised FPR at each external cohort, and that deployment protocols include
a local calibration run. Our study has limits. All data were public case-control cohorts, not prospective screening
cohorts. Within-cohort splits make the local pool and future samples exchangeable by design; a laboratory whose
methods drift over time must repeat the calibration. We fixed specificity; the same logic applies to sensitivity
targets when local cases are available. Code: [[GitHub URL]].

## METHODS

Methods are described in the Supporting Information.

## AUTHOR CONTRIBUTIONS
[[to be completed by the authors]]

## ACKNOWLEDGMENTS
We thank the authors of the original studies and the curatedMetagenomicData team for making the data public.

## CONFLICT OF INTEREST STATEMENT
The authors declare no conflicts of interest.

## ETHICS STATEMENT
This study re-analysed published, de-identified data. No new samples were collected.

## DATA AVAILABILITY STATEMENT
All data are public in curatedMetagenomicData (Bioconductor; ExperimentHub release 2021-03-31 and MetaCardis
2022-10-19). Code and result tables: [[GitHub URL]]. Supplementary materials (methods, tables, figures, graphical
abstract) are available online.

## REFERENCES
1. Pasolli E, et al. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. PLoS Comput Biol. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
2. Wirbel J, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. Nat Med. 2019;25:679-689. https://doi.org/10.1038/s41591-019-0406-6
3. Thomas AM, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. Nat Med. 2019;25:667-678. https://doi.org/10.1038/s41591-019-0405-7
4. Duvallet C, et al. Meta-analysis of gut microbiome studies identifies disease-specific and shared responses. Nat Commun. 2017;8:1784. https://doi.org/10.1038/s41467-017-01973-8
5. Nearing JT, Comeau AM, Langille MGI. Identifying biases and their potential solutions in human microbiome studies. Microbiome. 2021;9:113. https://doi.org/10.1186/s40168-021-01059-0
6. Wang Y, Le Cao KA. Managing batch effects in microbiome data. Brief Bioinform. 2020;21:1954-1970. https://doi.org/10.1093/bib/bbz105
7. Pasolli E, et al. Accessible, curated metagenomic data through ExperimentHub. Nat Methods. 2017;14:1023-1024. https://doi.org/10.1038/nmeth.4468
8. Wirbel J, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. Genome Biol. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
9. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. Neural Comput. 2002;14:21-41. https://doi.org/10.1162/089976602753284446
10. Alexandari A, Kundaje A, Shrikumar A. Maximum likelihood with bias-corrected calibration is hard-to-beat at label shift adaptation. ICML 2020. https://doi.org/10.48550/arxiv.1901.06852
11. Brummer N, Garcia-Romero D. Generative modelling for unsupervised score calibration. ICASSP 2014. https://doi.org/10.1109/icassp.2014.6853884
12. Zheng H, Chen W. High AUROC can mask decision failure in sepsis transcriptomic classifiers: preprocessing stability outweighs post hoc calibration across cohorts. PLoS One. 2026;21:e0357585. https://doi.org/10.1371/journal.pone.0357585
13. Wilks SS. Determination of sample sizes for setting tolerance limits. Ann Math Stat. 1941;12:91-96. https://doi.org/10.1214/aoms/1177731788
14. Angelopoulos AN, Bates S. Conformal prediction: a gentle introduction. Found Trends Mach Learn. 2023;16:494-591. https://doi.org/10.1561/2200000101
15. Van Calster B, et al. Calibration: the Achilles heel of predictive analytics. BMC Med. 2019;17:230. https://doi.org/10.1186/s12916-019-1466-7
16. Qiu J, Zhao YQ, Zheng Y. Shift-adjusted Neyman-Pearson classifiers via single index modeling (SACSIM). Biometrics. 2026;82:ujag138. https://doi.org/10.1093/biomtc/ujag138
17. Zhang Y, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. Front Microbiol. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
18. Sung H, et al. Global cancer statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries. CA Cancer J Clin. 2021;71:209-249. https://doi.org/10.3322/caac.21660
19. Baxter NT, et al. Microbiota-based model improves the sensitivity of fecal immunochemical test for detecting colonic lesions. Genome Med. 2016;8:37. https://doi.org/10.1186/s13073-016-0290-3
20. Steyerberg EW, et al. Validation and updating of predictive logistic regression models: a study on sample size and shrinkage. Stat Med. 2004;23:2567-2586. https://doi.org/10.1002/sim.1844
<!-- TODO citation audit: refs 15-20 must be cited in text (intro/discussion) or dropped; verify volume/pages of all. -->
