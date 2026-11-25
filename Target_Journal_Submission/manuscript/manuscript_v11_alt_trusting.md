# An atlas of 14 gut-microbiome disease classifiers across 36 healthy populations reveals unstable false-positive rates

**Article type:** Letter, iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary (about 100 words).**
- **Atlas.** We trained 28 classifiers for 14 diseases on 26 public case–control cohorts and set each cut-off to flag
  10% of healthy people. We then applied them to 6,525 healthy adults from 36 cohorts in 20 countries.
- **Instability.** In 70% of the 978 classifier–population pairs, the share flagged fell outside 5–15%. Every
  classifier varied strongly between populations (I² 64–97%), and better accuracy did not mean more stable
  specificity.
- **Geography (exploratory).** Populations that were compositionally far from the training controls, and populations
  outside Europe and North America, were flagged more.
- **Local recalibration.** Recalibrating each test on 100 unlabelled local people lowered the error in all 28
  classifiers.

---

To the Editor,

Gut metagenomes carry signals of colorectal cancer, inflammatory bowel disease (IBD), type 2 diabetes,
cardiometabolic, liver and neuropsychiatric diseases. Machine-learning classifiers built on these signals transfer
between cohorts with useful accuracy [1–4]. Most studies report this accuracy as the area under the ROC curve (AUROC).
A test in use, however, needs a fixed cut-off, and that cut-off sets its false-positive rate (FPR): the share of
healthy people who are told they may be ill. Earlier work saw the warning signs:
- applied to control samples of other studies, classifiers produced more than twice their intended false positives [5];
- colorectal cancer classifiers lost calibration across countries [6];
- predictors trained on industrialised populations lost accuracy elsewhere [7].

For blood tests, laboratories handle this problem by checking reference limits on local healthy people before use
[8, 9]. For microbiome tests, nobody has measured how far the FPR moves across the world's healthy populations, for
many diseases at once.

Here, we built that measurement. We trained classifiers for 14 diseases on every usable case–control cohort in
curatedMetagenomicData [10] and set each cut-off to flag 10% of training controls. We then applied all 28 classifiers
to 6,525 healthy adults from 36 cohorts in 20 countries that they had never seen (Figure 1A). Four hypotheses were
written down before the analysis; we report which held and which failed.

## ONE CUT-OFF, MANY FALSE-POSITIVE RATES

The FPR promised by a cut-off rarely held in a new healthy population (Figure 1B):
- in 70% of the 978 classifier–population pairs, the share of healthy people flagged fell outside 5–15%;
- in 27% it was above 20%, and in 34% below 5%;
- the 70% share was the same in populations of at least 100 people, so small samples do not explain it.

Every classifier showed far more between-population variation than sampling alone allows. I² ranged from 64% to 97%
(median 94%), with P < 10⁻⁶ for every classifier (Figure 1C; Table S16). For a new population, the 95% prediction
interval of the FPR was 0.01–0.22 for the LASSO colorectal cancer test and up to 0.02–0.73 for the IBD test.

Accuracy and stability were unrelated. The liver cirrhosis classifier was the most accurate in its training cohort
(AUROC 0.94), yet its FPR in a new population could lie anywhere from 0.01 to 0.62. Across all 28 classifiers, AUROC
did not predict the between-population spread (Spearman ρ = −0.06, P = 0.76; Figure 1D). Validating a test by its
AUROC therefore says little about how many healthy people it will flag at a new site.

These patterns are not explained by data problems we could check:
- we removed 119 samples duplicated across cohorts;
- we restricted the primary set to general-population healthy adults, excluding hospital, pregnancy, antibiotic and
  colonoscopy-referral cohorts;
- in a detailed analysis of three of the tests, age, sex, BMI and sequencing depth did not remove the population
  effect (Supporting Information S1–S3).

## WHO IS FLAGGED, AND WHY

We expected some populations to be over-flagged by many tests at once. This held only partly. Population identity
explained 17% of the variation in FPR across the 14 LASSO tests, between the 10% and 20% thresholds we had set, and
8% across the random forests. Test identity mattered more.

The populations that were over-flagged across tests, however, were not random (exploratory; Figure 2A):
- Cameroon, Madagascar, Peru, India and Japan had the highest cross-test false-alarm index;
- cohorts from the UK, Germany and Sweden had the lowest;
- populations outside Europe and North America scored higher than those inside (median index +0.35 versus −0.26,
  P = 0.001).

Most training cohorts came from Europe, North America and China.

A simple quantity tracked this. A population's compositional distance from a test's training controls was positively
rank-correlated with its FPR in 12 of 14 LASSO tests (median ρ = 0.38; Figure 2B). We then tested this, as a
pre-specified replication, in 19 further cohorts that had played no part in the discovery. The direction held in 10 of
14 tests (median ρ = 0.17), but the sign test did not reach significance (one-sided P = 0.09). The geographic contrast
did not replicate: only four replication cohorts came from outside Europe and North America (P = 0.30).

The taxa behind the false alarms differed from test to test. We decomposed each LASSO test's score shift in its most
over-flagged population. No taxon was among the top ten drivers in four or more tests, and only two appeared in three
(Figure 2C). This refutes our expectation of shared "false-alarm taxa". Each classifier reads a different part of the
microbiome, so each needs its own local check.

## WHAT A SITE CAN DO

If the error belongs to the population, the fix has to use the population. A site can score its first 100 tested
people, who are almost all healthy in a screening setting, and set the cut-off at the matching rank of their scores.
This label-free "burn-in" borrows from conformal prediction and reference-interval practice [11–13]; the rule itself is
not new.

We tested it with non-random splits inside each population: burn-in from earlier samples or from one age or BMI half,
evaluation on the rest. The burn-in lowered the mean absolute FPR error in all 28 classifiers (from 0.101 to 0.038;
Wilcoxon P = 7 × 10⁻⁹; Figure 2D).

Two limits matter, both shown in the detailed analysis of three tests (Supporting Information):
- the burn-in removes the bias of the published cut-off but not the sampling risk; about one burn-in in eight still
  gives an FPR above 0.15;
- it does not travel: calibrated at another site of the same study or on a neighbouring cohort, it was no better than
  the published cut-off.

Borrowed corrections did no better there. These included cut-offs from other cohorts, a pooled healthy reference, a
ComBat-style feature alignment, control augmentation [5], and down-weighting taxa that vary between healthy
populations.

We release `fprcheck`, a small Python package. It sets the burn-in cut-off for a chosen FPR and disease-prevalence
bound, states the probability of exceeding a tolerance, and reports the atlas range of FPRs expected for each of the 14
tests.

## CONCLUSION

The specificity of a gut-microbiome disease test is not a property of the test alone. Across 14 diseases and 36 healthy
populations, the same cut-off flagged anywhere from almost nobody to most people, and accuracy did not predict this.
Benchmarks should report the FPR at a fixed cut-off for each cohort, with a prediction interval, next to AUROC [14].
Sites that adopt a published test should check its cut-off on their own people.

Our study has limits:
- one profiler and two standard classifier types;
- controls that come from different recruitment settings;
- single-cohort training for nine diseases;
- geographic findings that remain exploratory.

Methods for correcting processing bias, such as DEBIAS-M and MMUPHin [15, 16], were not run and should be judged by the
FPR they deliver at new sites.

## METHODS

Data, classifiers, cohort definitions, de-duplication, the analysis plans written before each analysis, deviations,
statistics and every attempt that failed are described in the Supporting Information.

## AUTHOR CONTRIBUTIONS

[To be completed by the authors.]

## ACKNOWLEDGMENTS

We thank the authors of the cohorts in curatedMetagenomicData for making their data public.

## CONFLICT OF INTEREST STATEMENT

[To be completed by the authors.]

## ETHICS STATEMENT

This study reanalysed public, de-identified data. The original studies obtained ethics approval and informed consent
as described in their publications. No new ethics approval was required.

## AI USE STATEMENT

[To be completed by the authors.]

## DATA AVAILABILITY STATEMENT

Profiles and metadata: curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31; MetaCardis 2022-10-19).
Code, the `fprcheck` package, analysis plans, per-person scores and all result files: [GitHub URL and Zenodo DOI to be
added].

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
6. Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
7. Poyet M, Rühlemann M, Schaan AP, et al. Industrialization drives convergent microbiome and host physiological shifts in the human metaorganism. *Cell*. 2026. https://doi.org/10.1016/j.cell.2026.10.016
8. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
9. Leeflang MMG, Rutjes AWS, Reitsma JB, Hooft L, Bossuyt PMM. Variation of a test's sensitivity and specificity with disease prevalence. *CMAJ*. 2013;185:E537–E544. https://doi.org/10.1503/cmaj.121286
10. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
11. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
12. Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. *arXiv*. 2025. arXiv:2502.04807
13. Ammer T, Schützenmeister A, Prokosch HU, Rauh M, Rank CM, Zierk J. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep*. 2021;11:16023. https://doi.org/10.1038/s41598-021-95301-2
14. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
15. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
16. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4

## FIGURE LEGENDS

**Figure 1. A cut-off that promises a 10% false-positive rate delivers anywhere from almost none to most people.**
(A) Study design.
(B) False-positive rate of the 14 LASSO classifiers (rows) in 36 healthy populations (columns, ordered by the
cross-test false-alarm index). Populations outside Europe and North America are labelled in orange; grey cells mark
cohorts used to train that test.
(C) Random-effects pooled FPR (dot) and 95% prediction interval for a new population (line) for every classifier; blue
band 0.05–0.15.
(D) Training AUROC against between-population spread (τ, logit scale) for all 28 classifiers.

**Figure 2. Who is over-flagged, why, and what a site can do.**
(A) Cross-test false-alarm index per population: mean deviation of logit FPR from each test's mean over the 14 LASSO
tests; orange, outside Europe and North America (exploratory).
(B) Spearman correlation between a population's compositional distance from the training controls and its FPR, per
test, in the discovery populations and in the pre-specified replication populations.
(C) Number of tests in which a taxon was a top-10 positive contributor to the score shift of the most over-flagged
population.
(D) Mean absolute deviation from 0.10 of the realised FPR under within-site non-random splits (accession order; age
and BMI halves). Each line is one classifier (blue, LASSO; red, random forest), with the published cut-off on the
left and a burn-in on 100 local unlabelled people on the right.
