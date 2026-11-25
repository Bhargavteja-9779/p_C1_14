<!-- DRAFT v0.3 (2026-11-25), revised after review round 1. SOURCE FILE: edit this, then run `python build.py`
to number citations and regenerate manuscript.md. Locked (pre-registered) results and post-hoc (exploratory)
results are labelled as such throughout. Format: iMeta Letter / Short Communication, 2 figures. -->

# The decision threshold of a stool-metagenome classifier must be set at each site, on that site's own samples

**Running title:** Local cut-offs for microbiome tests

**Keywords:** gut microbiome; metagenomics; diagnostic classifier; decision threshold; false-positive rate;
external validation; colorectal cancer screening; calibration

**Highlights**
- The cut-off of a stool-metagenome classifier, set for 90% specificity in training cohorts, gave false-positive rates
  from 0% to 74% in 16 locked test cohorts, and AUROC did not predict which cohorts failed.
- Five published label-free adaptation methods did not repair the cut-off; four made it worse.
- An order-statistic cut-off computed from the site's own unlabelled samples kept the intended rate, but only when
  those samples came from the same centre as the samples later tested.

**Graphical abstract (text):** A gut-microbiome classifier moved to a new cohort keeps a similar AUROC but not its
intended false-positive rate. A cut-off set at a fixed rank among a few hundred of the site's own unlabelled samples
restores the rate; a cut-off borrowed from another cohort or centre does not.

To the Editor,

Gut-microbiome classifiers separate patients with colorectal cancer (CRC), inflammatory bowel disease (IBD) or type 2
diabetes (T2D) from healthy people across many cohorts [1-4], and
stool tests are being developed for CRC screening [5, 6]. Studies usually report the area
under the receiver operating characteristic curve (AUROC). A test in use, however, needs one fixed cut-off, and the
cut-off decides how many healthy people are sent for colonoscopy. Screening programmes tune that cut-off to the
positivity rate they can afford [7]. A laboratory that adopts a published microbiome classifier usually keeps
the cut-off chosen in the training cohorts, for example the score that gave 90% specificity there. In clinical
prediction it is well known that cut-offs and calibration need local updating [8, 9].
Microbiome meta-analyses have reported specificity at fixed cut-offs across cohorts [2], and recent
benchmarks study cross-study transfer [10]. Neyman-Pearson classifiers can be adapted to a new
site from an unlabelled sample when shift-explaining covariates are measured [11], but it is not known whether a laboratory can restore an intended
false-positive rate (FPR) without new diagnoses, nor where the samples for doing so must come from.

We used 19 public studies from curatedMetagenomicData [12] (CRC, IBD, T2D and colorectal adenoma;
3,626 unique stool metagenomes, 24 cohort-task pairs; Table S1). We trained LASSO logistic regression and random
forest on eight development CRC cohorts and set the cut-off for 90% specificity on out-of-fold training scores
[13]. Sixteen test cohorts (three external CRC cohorts and every cohort of IBD, T2D and adenoma) were locked
before any method was designed and analysed once with a pre-registered protocol (Supporting Information, Methods).
After peer review we added post-hoc experiments, which we label as exploratory.

## THE TRAINING CUT-OFF DOES NOT TRANSFER, AND AUROC HIDES THIS

At the locked cohorts, the realised FPR of the training cut-off ranged from 0.00 to 0.74 (median 0.10; Figure 1A).
The spread was far larger than binomial sampling allows (overdispersion P = 2 × 10^-52 for LASSO and 5 × 10^-88 for
random forest). The widest errors came from T2D and adenoma, where the classifiers were weak (AUROC 0.54-0.69), but
the problem was not confined to weak models: in the ten cohort-model pairs with AUROC of at least 0.70 the FPR
ranged from 0.02 to 0.39, and in the external CRC cohorts (AUROC 0.70-0.86) from 0.11 to 0.30. Cohorts with similar
AUROC had very different FPRs (Figure 1B), so AUROC-based validation cannot reveal this failure.

## LABEL-FREE FIXES FROM MACHINE LEARNING DO NOT REPAIR IT

A new laboratory has many unlabelled samples but few confirmed diagnoses. We therefore tested published methods that
adapt a classifier with unlabelled data: label-shift correction by expectation-maximisation (EM) [14] and by
maximum likelihood with bias-corrected calibration (MLLS) [15], unsupervised two-component score
calibration from speaker verification [16], a location-scale mixture fit, and per-site feature
standardisation, which was recently reported to rescue fixed cut-offs in transcriptomics [17]. With no cases
in the unlabelled pool, the cohort root-mean-square error (RMSE) of the FPR was 0.41 for EM, 0.34 for MLLS, 0.32 for
two-component calibration, 0.20 for feature standardisation and 0.15 for the mixture fit, against 0.19 for the
unchanged cut-off (Figure 1C). Only the mixture fit did better than doing nothing, and it still missed the target
widely (0.10 even when a fifth of the pool were patients). The reasons are simple. Label-shift methods assume that the scores of healthy
people do not move between sites, and they do. Mixture fits cannot tell "healthy scores moved up" from "some patients
are present". Standardising each site removes its average, but a screening pool and a case-control study have
different averages because they hold different shares of patients. Feature-level batch correction to labelled local
controls [18] or across studies [19] is a separate route that we did not test.

## A RANK RULE ON THE SITE'S OWN SAMPLES KEEPS THE INTENDED RATE

In screening, almost every sample is from a healthy person. The simplest use of this fact is to collect the site's
first n samples, score them and set the cut-off at the r-th highest score. This is a one-sided tolerance limit
[20] and the order-statistic step of Neyman-Pearson classification [21]; versions that tolerate some
mislabelled or contaminating samples exist in statistics [22, 23], and laboratory medicine derives
reference limits from unlabelled routine samples in the same spirit [24]. We do not claim the rule as new.
We chose r so that the expected FPR stays at or below the target if at most 5% of the pool are patients (a stricter
version bounds the probability that the FPR exceeds the target; Supporting Information, Note S1). The bound needs one
assumption: the healthy samples in the pool must be exchangeable with the healthy samples tested later.

At the locked cohorts, pools were random halves of each cohort, so that assumption held by design; the test therefore
measures how close the rule comes to its target with real, small pools (6-30 controls in 12 of 16 cohorts). The rule
had a cohort-RMSE of 0.031 against 0.185 for the training cut-off (paired difference in absolute error -0.108; 95% CI
clustered by cohort -0.182 to -0.056; Holm-adjusted P = 0.0004 over 16 cohort-task pairs; Figure 2A). It was also
closer to the target than the plain local quantile of the pool (difference -0.017, 95% CI -0.028 to -0.008), and
equivalent to ten labelled local controls within ±0.02 (difference 0.006, 90% CI -0.000 to 0.011; equivalence
P = 0.0002). Per simulated deployment, the FPR exceeded 15% in 14% of deployments with the rank rule, against 20% with
ten labelled controls, 33% with the plain pool quantile and 39% with the training cut-off. Results held for both
classifiers and without the adenoma task, whose controls overlap the development cohorts (Table S3). In the smallest
cohort (six pool controls) the rule abstained, as designed; the strict version abstained in half of the
cohort-model pairs, because its guarantee needs larger pools.

Post-hoc, we checked the two weaknesses that reviewers raised. First, the pre-registered "1% cases" setting rounded
the number of cases in small pools to zero. When we drew the number of cases at random (binomial), the rank rule kept
a cohort-RMSE of 0.030-0.052 with up to 20% cases in the pool, four times the share it was designed for (Table S4).
Second, the locked pools were small. In the three cohorts with at least 150 controls, pools of 100-200 samples with 5%
cases gave an FPR above 15% in 4% of deployments with the rank rule, 7-10% with the plain pool quantile, 19% with ten
labelled controls and under 1% with the strict version (Figure 2C). Scoring ties either way changed no result at the
third decimal.

## THE SAMPLES MUST COME FROM THE SAME SITE

The guarantee rests on exchangeability, so we tested what happens when it fails (post hoc). In MetaCardis, one study
with one protocol and sequencer but three recruiting centres, a pool from the same centre gave an FPR within 0.01 of
the target (RMSE 0.009). A pool from another centre of the same study gave an RMSE of 0.067, with FPRs up to 0.24
(Copenhagen pool applied in Leipzig). A pool from another cohort of the same disease gave an RMSE of 0.158, and a
third of cohort pairs exceeded 15% (Figure 2B), no better than the training cut-off (0.173). The cut-off therefore
belongs to the site, meaning the population and the laboratory process together [25, 26], not to
the study or the country.

What does this mean in practice? For CRC at 0.5% prevalence and a 10% target FPR, the training cut-off sent 199
healthy people per 1,000 screened to colonoscopy instead of the intended 100; the rank rule sent 87. The price is
sensitivity: in the CRC cohorts it was 0.48 with the rank rule and 0.65 with the training cut-off, which bought its
extra detections with twice the intended FPR. With the strict version, a site needs about 360 unlabelled samples if
at most 1% are patients, 610 if at most 5% and 1,500 if at most 10% (Note S1). Programmes that work at a 5% target,
closer to current stool-test positivity [7], need correspondingly larger pools; with our small locked pools
the rank rule abstained in 31% of cohort-model pairs at that target.

## CONCLUSION

The cut-off of a microbiome test belongs to the site that runs it. AUROC-based validation hides threshold failure,
and label-free adaptation methods from machine learning do not repair it at screening prevalence. A classical
order-statistic rule applied to a few hundred of the site's own unlabelled samples restores the intended FPR, but a
pool borrowed from another cohort, or even from another centre of the same study, does not. We suggest that
microbiome diagnostic studies report the realised FPR at each external cohort, and that deployment protocols include
a local calibration run that is repeated when the population or laboratory process changes. Our study has limits.
All cohorts were case-control studies; cases were mostly diagnosed, often symptomatic cancers, so sensitivity in true
screening will be lower, and advanced adenomas may exceed the assumed 5% case share. Within-cohort pools are
exchangeable with later samples by design, which a prospective screening pool may not be. We did not test
feature-level batch correction or newer label-shift estimators. Code and result tables: [[GitHub URL]].

## FIGURE LEGENDS

**Figure 1. The training cut-off does not transfer, and label-free fixes do not repair it (locked test).**
(A) Realised false-positive rate (FPR) of the cut-off set for 90% specificity on training cohorts, at 16 locked test
cohorts, for LASSO (circles) and random forest (diamonds); each point is the mean over 200 random evaluation halves.
Dashed line, intended FPR (10%). (B) The same FPRs plotted against the AUROC at each cohort. (C) Cohort root-mean-square
error of the FPR (32 cohort-model units) for the training cut-off and five label-free adaptation methods, by the share
of patients in the unlabelled pool. EM, expectation-maximisation label-shift correction; MLLS, maximum likelihood with
bias-corrected calibration.

**Figure 2. A rank rule on the site's own unlabelled samples keeps the intended FPR, if the samples come from the
same site.** (A) Locked test: FPR per simulated deployment (200 splits x 32 cohort-model units, no cases in the pool;
abstention counted as FPR 0). Box, interquartile range; line, 5th-95th percentile; dot, median; right, share of
deployments with FPR above 15%. Rank rule: expected-FPR version; strict rank rule: P(FPR > 10%) ≤ 0.1. (B) Post hoc:
mean FPR when the pool comes from the same MetaCardis centre, another MetaCardis centre, or another cohort of the same
disease; each point is one pool-target pair and model; bars, medians. (C) Post hoc: share of deployments with FPR above
15% by pool size in the three cohorts with at least 150 controls (5% cases in the pool, binomial).

## AUTHOR CONTRIBUTIONS
[[to be completed by the authors (CRediT)]]

## ACKNOWLEDGMENTS
We thank the authors of the original studies and the curatedMetagenomicData team for making the data public.

## FUNDING
[[to be completed by the authors]]

## CONFLICT OF INTEREST STATEMENT
The authors declare no conflicts of interest.

## ETHICS STATEMENT
This study re-analysed published, de-identified data. No new samples were collected.

## DATA AVAILABILITY STATEMENT
All data are public in curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31, and MetaCardis
2022-10-19). Code, the frozen protocol, raw per-split results and result tables: [[GitHub URL and archived DOI]].
Supplementary materials (methods, Note S1, Tables S1-S4) are available online.

## REFERENCES
1. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. PLoS Comput Biol. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
2. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. Nat Med. 2019;25:679-689. https://doi.org/10.1038/s41591-019-0406-6
3. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. Nat Med. 2019;25:667-678. https://doi.org/10.1038/s41591-019-0405-7
4. Duvallet C, Gibbons SM, Gurry T, Irizarry RA, Alm EJ. Meta-analysis of gut microbiome studies identifies disease-specific and shared responses. Nat Commun. 2017;8:1784. https://doi.org/10.1038/s41467-017-01973-8
5. Baxter NT, Ruffin MT, Rogers MAM, Schloss PD. Microbiota-based model improves the sensitivity of fecal immunochemical test for detecting colonic lesions. Genome Med. 2016;8:37. https://doi.org/10.1186/s13073-016-0290-3
6. Imperiale TF, Ransohoff DF, Itzkowitz SH, et al. Multitarget stool DNA testing for colorectal-cancer screening. N Engl J Med. 2014;370:1287-1297. https://doi.org/10.1056/NEJMoa1311194
7. Toes-Zoutendijk E, van Leerdam ME, Dekker E, et al. Real-time monitoring of results during first year of Dutch colorectal cancer screening program and optimization by altering fecal immunochemical test cut-off levels. Gastroenterology. 2017;152:767-775.e2. https://doi.org/10.1053/j.gastro.2016.11.022
8. Van Calster B, McLernon DJ, van Smeden M, Wynants L, Steyerberg EW. Calibration: the Achilles heel of predictive analytics. BMC Med. 2019;17:230. https://doi.org/10.1186/s12916-019-1466-7
9. Steyerberg EW, Borsboom GJJM, van Houwelingen HC, Eijkemans MJC, Habbema JDF. Validation and updating of predictive logistic regression models: a study on sample size and shrinkage. Stat Med. 2004;23:2567-2586. https://doi.org/10.1002/sim.1844
10. Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. Front Microbiol. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
11. Qiu J, Zhao YQ, Zheng Y. Shift-adjusted Neyman-Pearson classifiers via single index modeling (SACSIM). Biometrics. 2026;82:ujag138. https://doi.org/10.1093/biomtc/ujag138
12. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. Nat Methods. 2017;14:1023-1024. https://doi.org/10.1038/nmeth.4468
13. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. Genome Biol. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
14. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. Neural Comput. 2002;14:21-41. https://doi.org/10.1162/089976602753284446
15. Alexandari A, Kundaje A, Shrikumar A. Maximum likelihood with bias-corrected calibration is hard-to-beat at label shift adaptation. Proc Mach Learn Res. 2020;119:222-232 (ICML 2020). https://doi.org/10.48550/arxiv.1901.06852
16. Brümmer N, Garcia-Romero D. Generative modelling for unsupervised score calibration. In: Proc IEEE ICASSP 2014. p. 1680-1684. https://doi.org/10.1109/icassp.2014.6853884
17. Zheng H, Chen W. High AUROC can mask decision failure in sepsis transcriptomic classifiers: preprocessing stability outweighs post hoc calibration across cohorts. PLoS One. 2026;21:e0357585. https://doi.org/10.1371/journal.pone.0357585
18. Gibbons SM, Duvallet C, Alm EJ. Correcting for batch effects in case-control microbiome studies. PLoS Comput Biol. 2018;14:e1006102. https://doi.org/10.1371/journal.pcbi.1006102
19. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. Nat Microbiol. 2025;10:897-911. https://doi.org/10.1038/s41564-025-01954-4
20. Wilks SS. Determination of sample sizes for setting tolerance limits. Ann Math Stat. 1941;12:91-96. https://doi.org/10.1214/aoms/1177731788
21. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. Sci Adv. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
22. Yao S, Rava B, Tong X, James G. Asymmetric error control under imperfect supervision: a label-noise-adjusted Neyman-Pearson umbrella algorithm. J Am Stat Assoc. 2023;118:1824-1836. https://doi.org/10.1080/01621459.2021.2016423
23. Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. In: Proc ICML 2025. https://doi.org/10.48550/arxiv.2502.04807
24. Jones GRD, Haeckel R, Loh TP, et al. Indirect methods for reference interval determination - review and recommendations. Clin Chem Lab Med. 2018;57:20-29. https://doi.org/10.1515/cclm-2018-0073
25. Nearing JT, Comeau AM, Langille MGI. Identifying biases and their potential solutions in human microbiome studies. Microbiome. 2021;9:113. https://doi.org/10.1186/s40168-021-01059-0
26. Wang Y, Lê Cao KA. Managing batch effects in microbiome data. Brief Bioinform. 2020;21:1954-1970. https://doi.org/10.1093/bib/bbz105
27. Angelopoulos AN, Bates S. Conformal prediction: a gentle introduction. Found Trends Mach Learn. 2023;16:494-591. https://doi.org/10.1561/2200000101
