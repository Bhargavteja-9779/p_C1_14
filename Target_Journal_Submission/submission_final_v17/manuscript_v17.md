# Gut-microbiome disease classifiers flag 0–87% of healthy people at the same cut-off, depending on the population

**Article type:** Letter, iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary.** A gut-microbiome test is published with one cut-off and one false-positive rate (FPR). In
6,525 healthy adults from 36 populations, the same cut-offs of 28 disease classifiers flagged 0% to 87% of healthy
people in populations of at least 100. Two published gut-health indices, GMWI2 and GMHI, each labelled most healthy
people in their own East Asian training studies as non-healthy. A published gut-health index labelled 64% of healthy people in its own East Asian training studies as
non-healthy, against 12% elsewhere, a model artefact traced to the geographic make-up of its training data. Within a
site, recalibrating the cut-off on 100 unlabelled local people cut the FPR error by 62% in retrospective tests.

---

To the Editor,

Stool metagenomes carry signals of colorectal cancer (CRC), inflammatory bowel disease (IBD), type 2 diabetes (T2D) and
many other diseases, and pooled analyses show that these signals carry over between countries [1–4]. Classifiers are
therefore judged by the area under the ROC curve (AUROC) in held-out cohorts [1, 5, 6]. A test in use, however, needs one
cut-off, and that cut-off fixes how many healthy people are flagged. In CRC screening every false positive leads to a
colonoscopy [7].

Clinical epidemiology has long known that a test's specificity changes with the population it is used in, the
"spectrum effect" [8, 9]. Microbiome studies have shown this for single diseases or within one region. A CRC cut-off
set for an FPR of 0.10 on training controls gave 0.09–0.13 on other-disease cohorts [1], controls from other studies
doubled the false positives of CRC classifiers [10], healthy reference ranges and disease models did not transfer
between districts of one province [11], and predictors trained on industrialised populations were uninformative in
less-industrialised cohorts [12]; CRC models also lose calibration across countries [13]. In medical imaging,
operating-point metrics drift between sites even when AUROC holds [14]. What has not been mapped is how far the FPR
at a fixed cut-off varies across diseases and healthy populations. Cross-cohort evaluations across many diseases report
AUROC [15], best-practice guides focus on discrimination [16], and an audit in this journal found that most studies do
not deposit the metadata needed to re-test them [17]. Laboratory medicine verifies reference limits on local healthy
people before use [18]; microbiome diagnostics have no such step.

Here we measured the FPR of 28 classifiers for 14 diseases in every eligible healthy adult population in
curatedMetagenomicData [19] (36 populations, 6,525 people, 20 countries). We then audited a published, released
classifier, the Gut Microbiome Wellness Index 2 (GMWI2) [20], tested the mechanism we found by retraining, and tested a
local fix. Confirmatory analyses followed time-stamped internal plans with falsification criteria, committed to the code
repository before they were run ("pre-specified"). We report failed hypotheses and label all other analyses post hoc.

## A FIXED CUT-OFF GIVES A DIFFERENT FALSE-POSITIVE RATE IN EVERY POPULATION

We trained LASSO logistic regression and random-forest (RF) classifiers on MetaPhlAn3 relative abundances of all
clades, kingdom to species [21], from 26 case–control cohorts. Following [1], each cut-off was the 90th percentile of
out-of-fold scores of training controls, which targets an FPR of 0.10. We scored one sample per healthy adult in every population not used in training, after removing 119
duplicated samples. Our primary ("strict") set excludes hospital, pregnancy, trial and colonoscopy-referral control groups
and antibiotic users; it was chosen after seeing first results, so the full set (55 populations, 8,160 people) is
reported as a check (Supporting Information S1).

The FPR depended on where the classifier was used (Figure 1A, B). Of 489 LASSO classifier–population pairs, 45% had an
FPR above 0.15 and 24% below 0.05. In populations of at least 100 people, FPRs ranged from 0 to 0.87 across the 28
classifiers (maximum: heart failure, RF, out-of-fold AUROC 0.75) and from 0 to 0.77 across the LASSO tests; a single
test could span most of this range (impaired glucose tolerance, IGT, LASSO: 0.09–0.77, a near-chance classifier with
AUROC 0.54). The spread exceeded sampling noise for all 28
classifiers (I² median 0.94, range 0.64–0.97; also 28/28 in the full set). Sampling noise alone would put 15–16% of
populations outside 0.05–0.15 (half to one and a half times the target); the observed share was 50–97%. For a new
population, the upper end of the 95% prediction interval of the LASSO tests ranged from 0.22 (CRC) to 0.81 (IGT)
(Figure 1C). Pooled over populations, several classifiers were close to or below the target (CRC 0.06), so a pooled FPR
hides the problem. Here "population" includes each study's sample handling, which we cannot separate from biology.

AUROC did not predict the spread (Spearman ρ = −0.06, P = 0.76; Figure 1D), and restricting to the 16 classifiers with
AUROC ≥ 0.65 changed nothing (I² median 0.94; Supporting Information S2). A better classifier was not a more portable one. No single
factor explained the error: for LASSO the population explained 17% of the variance in logit FPR (20.2% net of
sampling noise) and the classifier–population pair about half; against our pre-stated 20% threshold this is
inconclusive for LASSO, and the threshold was clearly missed for RF (S2.1). In the three-test analysis, adjusting for age, sex, body-mass index and
sequencing depth left a population effect (S2).

## TWO PUBLISHED GUT-HEALTH INDICES LABEL HEALTHY EAST ASIAN COHORTS AS NON-HEALTHY

To test a classifier that others use, we audited GMWI2 [20], a published L1 logistic regression on the presence of 95
taxa, trained on 8,069 stool metagenomes from 54 studies (a score above 0 means healthy). Its released coefficients matched the
paper's Supplementary Data (95/95). By the developers' own scores, 20.8% of their healthy training samples fall below the
cut-off; we use this training FPR as the rate the index should deliver elsewhere.

Within its own training data, the cut-off labelled 0% to 84% of healthy people as non-healthy, depending on the study
(44 studies with ≥ 20 healthy people; I² = 0.96; Figure 2A; post hoc, developers' scores only). All eight studies above
50% were from China or Japan: median 0.64 across the 13 East Asian studies against 0.12 across the 31 others (two-sided
Mann–Whitney P = 5 × 10⁻⁷). Healthy people in rural Africa were almost never mislabelled (0–7%).

In 15 healthy populations GMWI2 never saw (strict set, 1,914 people; our scoring reproduced the published scores,
r = 0.991), the FPR ranged from 0 to 0.54. Twelve of the 15 (80%) fell outside the pre-specified band of 0.10–0.31
(half to one and a half times the training FPR), against 9% expected from sampling noise (Holm-adjusted
P = 2 × 10⁻¹²; Figure 2B); eight fell below the band and four above it. The four unseen East Asian populations had FPRs
of 0.25–0.54 (median 0.38 vs 0.06 in the 11 others; one-sided P = 0.020; post hoc; full set 0.38 vs 0.20, P = 0.065). We
had expected a lower FPR in populations seen in training; this was falsified (one-sided P = 0.72).

To test whether this was specific to GMWI2, we audited its predecessor, the Gut Microbiome Health Index (GMHI) [22],
under a second pre-specified plan (Figure S2). Our re-implementation reproduced the developers' script exactly. In the
developers' own data, GMHI labelled 3% to 90% of healthy people as non-healthy across 21 studies (I² = 0.96; 24%
overall), and the eight East Asian studies had a median of 0.67 against 0.21 in the 13 others (one-sided P = 0.0007,
Holm-adjusted). In curatedMetagenomicData, the GMHI and GMWI2 flag rates of the same populations were correlated
(Spearman ρ = 0.70, 36 populations), although the two indices use different algorithms and markers. The level of GMHI
there is not interpretable on its own: four of its seven health-prevalent species do not exist under the MetaPhlAn3
names that curatedMetagenomicData uses, and on 101 samples profiled with both versions this raised the share flagged
from 70% to 85% (post hoc). A released cut-off therefore depends on the profiling software as well as on the population.

## WHY: THE GEOGRAPHIC MAKE-UP OF THE TRAINING DATA

Five taxa explained 39% of the East Asian–other gap in mean score (Figure 2C; post hoc). Four carry "non-healthy"
weights and are common in healthy East Asian guts, among them *Bacteroides plebeius* (72% vs 17%), a marker of diet and
geography whose Japanese strains acquired seaweed-degrading enzymes from marine bacteria [23]. The fifth, *Clostridium*
sp. CAG_167, weighted as "healthy", is nearly absent in East Asian samples (2% vs 28%). The list also contains the
pathobiont *Klebsiella* (59% vs 22%), so the gap is not only a story of harmless commensals.

The training data explain the weights. East Asian samples made up 62% of GMWI2's non-healthy training samples (1,574 of
2,522) but only 20% of the healthy ones (1,097 of 5,547; odds ratio 6.7). A classifier that separates healthy from
non-healthy across pooled studies can then learn region-typical taxa as disease markers. Disease predictors trained on
industrialised populations were reported to fail in other populations [12], the developers of an earlier health index
noted that such biases are hard to remove [22], and country confounding was shown with SIAMCAT [10]; we add its size
for a released index and a test by retraining. These are properties of the model and its training
data, not evidence that East Asian microbiomes are less healthy. Country also travels with laboratory, DNA extraction and
sequencing, which this analysis cannot separate from biology.

We retrained the GMWI2 recipe on 10,986 people in 61 studies, leaving one study out at a time (pre-specified). Pooled
training reproduced the effect: median FPR 0.71 in East Asian studies against 0.19 elsewhere (gap 0.52; Figure 2D).
Giving every country × label group the same total weight cut the gap to 0.06. The point estimate (88%) met our criterion
of a 50% reduction, but the study-clustered 95% CI of the relative reduction (41–149%) includes values below it. The
spread between studies fell on the logit scale (the pre-stated criterion) but not on the FPR scale, and the East Asian
median (0.29) stayed above the training FPR. This weighting also shrinks the countries that dominate the data;
balancing labels within countries alone removed 37% of the gap (post hoc; 95% CI of the absolute reduction −0.04 to
0.31), so within-country case mix may also contribute. Reweighting cost some discrimination (point estimate beyond our
pre-stated margin; that hypothesis failed), and it is a check of training data, not a deployment fix (S6).

## A SITE CAN VERIFY AND RECALIBRATE ITS OWN CUT-OFF

The classifier–population error of Figure 1 needs local data. Cut-offs set on other cohorts failed: a pooled reference of
about 4,000 healthy people, the most similar populations, and other cohorts from the same country; adding external
controls to training [10] did not help (S4).

A site that tests mostly healthy people can recalibrate without labels. It scores its first N tests and takes the k-th
smallest score as the cut-off, k = ⌈(N + 1)(1 − α(1 − π_max))⌉, with α the target FPR and π_max the highest share of
patients expected among those tested. If later healthy people are exchangeable with this burn-in group, the expected
FPR is at most α by a split-conformal argument [24, 25], with π_max acting as a conservative allowance for patients in
the burn-in group (cf. prior-shift corrections [26]). The realised FPR then has an exact, known (Beta) distribution
(N = 100: P(FPR > 0.15) = 0.055; Figure S1A), and a stricter rank bounds P(FPR > α) [27]. The rule is not new: medical
imaging corrects operating points from unlabelled site data [14], and laboratories set reference limits from routine
results [28]. We tested whether it survives a non-random split within a site.

It did, in retrospective tests; no prospective test was run. In the 13 populations of the full set with at least 120
people, setting the cut-off on 100 people from a non-random part of each population (the first 100 in accession order,
or the younger or leaner half) and evaluating on the rest cut the mean absolute FPR error from 0.101 to 0.038 (−62%;
28/28 classifiers improved, meeting the pre-specified criterion; post hoc population-clustered 95% CI 51–70%, 13/13
populations; Figure 3A). For GMWI2, in the same populations, the error fell from 0.21 to 0.04 (−79%, CI 64–85%), and for
GMHI from 0.26 to 0.05 (−79%; 12 of 13 populations; Figure S2C), which also removed the shift caused by the profiling
software. Across
sites, the rule broke: a burn-in from one city or country, applied in another, was no better than the training cut-off
(S4). It must be run at the site that uses the test and repeated when sample handling or the population served changes.

Recalibration costs sensitivity. In three case–control cohorts where the training cut-off flagged 29% of controls,
reaching the 10% target cut sensitivity from 0.46 to 0.21–0.23 (100 labelled local controls: 0.25; Figure 3B). The rule
therefore suits screening, where almost everyone tested is healthy, not tests of referred patients. A site can also
check a stated FPR: an exact binomial test on 100 local healthy people flags, on average, 98% of atlas pairs whose FPR
exceeds 0.25 (Figure S1B; post hoc). We release the atlas and these procedures as fprcal, a small Python tool.

## CONCLUSION

The false-positive rate of a gut-microbiome test is a property of the test, the population and the profiling pipeline
together. Two published health indices labelled healthy East Asian cohorts as non-healthy, and for one of them
retraining linked this to the geographic make-up of pooled training data. Cross-cohort benchmarks should report the FPR at a fixed cut-off in each held-out population, with I² and a
prediction interval, next to AUROC, as STORMS-style reporting [29] could require. Developers should check the geographic
case mix of training data and state the profiler version their cut-off assumes. Sites should treat a published cut-off as provisional, verify it on local healthy people and,
for screening, recalibrate it. Processing-bias corrections such as DEBIAS-M and MMUPHin [30, 31] should be judged by the
FPR they deliver at new sites.

Our study has limits. All profiles came from one pipeline (MetaPhlAn3); our classifiers used fixed settings, and seven
had an AUROC below 0.6. "Population" includes each study's sample handling, which we cannot separate from biology. We did
not run DEBIAS-M, MMUPHin or ConQuR [32]. GMHI could be scored on curatedMetagenomicData only with four of its seven
health-prevalent species missing. The strict set and the East Asian comparisons were chosen after seeing results.
All site-level results are retrospective; a prospective deployment is needed.

## METHODS

Full methods, analysis plans and deviations, every correction we tried (including those that failed), Supporting
Figures S1–S2 and Tables S1–S26 are in the Supporting Information. In brief: MetaPhlAn3 relative abundances of all clades
(kingdom to species) present in > 5% of training samples (GMWI2: presence of its 95 taxa); one sample per person, and
samples duplicated across studies removed (119); strict set = general-population healthy adults without antibiotic use
(hospital, pregnancy, trial and colonoscopy-referral control groups excluded); LASSO (C = 0.1) and random forest (500
trees; scikit-learn 1.9.1); cut-off = 90th percentile of out-of-fold control scores; DerSimonian–Laird heterogeneity on
logit FPR; crossed random effects for the variance decomposition; study-clustered bootstrap for the case-mix analysis; GMHI re-implemented from the developers' released script (plan v7, S7).

## ACKNOWLEDGMENTS

We thank the authors of the cohorts in curatedMetagenomicData, and the authors of GMWI2, for making their data and models
public. [Further acknowledgments to be completed by the authors.]

## AUTHOR CONTRIBUTIONS

[To be completed by the authors.]

## CONFLICT OF INTEREST STATEMENT

[To be completed by the authors.]

## FUNDING

[To be completed by the authors.]

## ETHICS STATEMENT

This study reanalysed public, de-identified, openly licensed data (curatedMetagenomicData; GMWI2 public release). The
original studies obtained ethics approval and informed consent as described in their publications. No new ethics
approval was required, and no attempt at re-identification was made. Country and region labels come from study metadata,
not from self-reported ethnicity.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31; MetaCardis 2022-10-19). The
GMWI2 model is from its public release (bioconda gmwi2 1.6, MIT licence) and the published Supplementary Data [20]. The
exact metadata file, code, analysis plans, per-person scores, the duplicate list, the per-population FPR atlas and the
fprcal tool (including the 14 LASSO atlas classifiers as coefficient tables, usable through `fprcal score`) are in the code repository: [GitHub repository URL and Zenodo DOI to be added]. Supplementary materials are
online at the journal.

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Geng M, Li M, Li Y, et al. A universal oral microbiome-based signature for periodontitis. *iMeta*. 2024;3:e212. https://doi.org/10.1002/imt2.212
7. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
8. Leeflang MMG, Rutjes AWS, Reitsma JB, Hooft L, Bossuyt PMM. Variation of a test's sensitivity and specificity with disease prevalence. *CMAJ*. 2013;185:E537–E544. https://doi.org/10.1503/cmaj.121286
9. Mulherin SA, Miller WC. Spectrum bias or spectrum effect? Subgroup variation in diagnostic test evaluation. *Ann Intern Med*. 2002;137:598–602. https://doi.org/10.7326/0003-4819-137-7-200210010-00011
10. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
11. He Y, Wu W, Zheng HM, et al. Regional variation limits applications of healthy gut microbiome reference ranges and disease models. *Nat Med*. 2018;24:1532–1535. https://doi.org/10.1038/s41591-018-0164-x
12. Poyet M, Rühlemann M, Schaan AP, et al. Industrialization drives convergent microbiome and host physiological shifts in the human metaorganism. *Cell*. 2026. https://doi.org/10.1016/j.cell.2026.10.016
13. Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707 (Correction: https://doi.org/10.3389/fmicb.2026.2021752)
14. Roschewitz M, Khara G, Yearsley J, et al. Automatic correction of performance drift under acquisition shift in medical image classification. *Nat Commun*. 2023;14:6608. https://doi.org/10.1038/s41467-023-42396-y
15. Li M, Liu J, Zhu J, et al. Performance of gut microbiome as an independent diagnostic tool for 20 diseases: cross-cohort validation of machine-learning classifiers. *Gut Microbes*. 2023;15:2205386. https://doi.org/10.1080/19490976.2023.2205386
16. Li P, Li M, Chen WH. Best practices for developing microbiome-based disease diagnostic classifiers through machine learning. *Gut Microbes*. 2025;17:2489074. https://doi.org/10.1080/19490976.2025.2489074
17. Degregori S, Huang I, Fetcinko LH, et al. A decade-scale audit of microbiome AI-readiness. *iMeta*. 2026:e70192. https://doi.org/10.1002/imt2.70192
18. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
19. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
20. Chang D, Gupta VK, Hur B, et al. Gut Microbiome Wellness Index 2 enhances health status prediction from gut microbiome taxonomic profiles. *Nat Commun*. 2024;15:7447. https://doi.org/10.1038/s41467-024-51651-9
21. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
22. Gupta VK, Kim M, Bakshi U, et al. A predictive index for health status using species-level gut microbiome profiling. *Nat Commun*. 2020;11:4635. https://doi.org/10.1038/s41467-020-18476-8
23. Hehemann JH, Correc G, Barbeyron T, Helbert W, Czjzek M, Michel G. Transfer of carbohydrate-active enzymes from marine bacteria to Japanese gut microbiota. *Nature*. 2010;464:908–912. https://doi.org/10.1038/nature08937
24. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
25. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
26. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. *Neural Comput*. 2002;14:21–41. https://doi.org/10.1162/089976602753284446
27. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
28. Ammer T, Schützenmeister A, Prokosch HU, Rauh M, Rank CM, Zierk J. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep*. 2021;11:16023. https://doi.org/10.1038/s41598-021-95301-2
29. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
30. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
31. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4
32. Ling W, Lu J, Zhao N, et al. Batch effects removal for microbiome data via conditional quantile regression. *Nat Commun*. 2022;13:5418. https://doi.org/10.1038/s41467-022-33071-9

## FIGURE LEGENDS

**Figure 1. The false-positive rate of 14 gut-microbiome disease tests in 36 healthy populations.** (A) The 36 strict
healthy adult populations (20 countries); circle area, number of people; colour, false-alarm index (mean deviation of
logit FPR from the test mean across the 14 LASSO tests). (B) Realised FPR of each LASSO test (rows, ordered by
between-population τ) in each population (columns, country·first author). The cut-off targets FPR 0.10 (white); blue
below, red above, log scale. Blank cells: training cohort or fewer than 20 people. Bold labels: populations recorded as
"non-westernised" in the curatedMetagenomicData metadata. (C) Random-effects pooled FPR (dot) and 95% prediction interval
for a new population (line), LASSO (blue) and RF (violet); grey band 0.05–0.15; arrow, interval below 0.001. (D)
Out-of-fold AUROC against between-population τ, 28 classifiers; open symbols, AUROC < 0.6.

**Figure 2. A published gut-health index (GMWI2) and why it mislabels healthy East Asian cohorts.** (A) Share of healthy
training samples labelled non-healthy by the published cut-off, per study, from the developers' own scores (44 studies
with ≥ 20 healthy people); orange, East Asian studies; dashed line, training FPR 0.21; bars, exact 95% intervals. (B) The
same for the 15 strict healthy populations GMWI2 never saw (our scoring; QC against published scores r = 0.99); shaded,
the pre-specified band 0.10–0.31. (C) The
eight taxa contributing most to the East Asian–other score gap (the five largest explain 39%); fitted weight in
parentheses (negative = "non-healthy"); dots, share of healthy people carrying the taxon, by region. (D) A GMWI2-recipe
classifier retrained on curatedMetagenomicData, leave-one-study-out: FPR per healthy study under pooled training and with
every country × label group given equal total weight; lines, studies (orange, East Asian); diamonds, regional medians,
offset sideways for legibility (other regions 0.19 → 0.22, so part of the gap closes because their FPR rises);
dashed line, training FPR 0.21.

**Figure 3. What a site can do.** (A) Mean absolute deviation of the FPR from 0.10 within a site: training cut-off
(ochre) versus burn-in on 100 people from a non-random part of the same population (blue), for each of 28 classifiers.
Each classifier is evaluated in 11–13 populations of the full set with ≥ 120 people × non-random splits (accession
order, age, body-mass index); 646 evaluations in total (Table S5). (B) Sensitivity against FPR at N = 100, averaged over three case–control cohorts (one
CRC, two T2D): training cut-off (ochre; does not depend on the burn-in), expected-FPR burn-in with 1%, 5% or 10% patients
in the burn-in group (blue), and a cut-off set on 100 labelled local controls (grey); dashed line, target FPR.

**Supporting Figure S2. Audit of a second published index, GMHI (plan v7).** (A) Share of healthy people labelled
non-healthy (GMHI < 0) in the developers' own data, per study (21 studies with ≥ 20 healthy people; GMHI recomputed with
the developers' script on their profiles); orange, East Asian studies; bars, exact 95% intervals; dashed line, overall
training rate 0.24. (B) GMHI against GMWI2 flag rates in 36 strict curatedMetagenomicData populations (n ≥ 20). (C)
Within-site burn-in (N = 100) against the published cut-off, mean absolute deviation from 0.24 per population (13
populations with ≥ 120 people).

**Supporting Figure S1.** (A) Exact probability that the realised FPR exceeds 0.15 when the cut-off is the k-th smallest
of N burn-in scores (expected-FPR rule, blue; rule bounding P(FPR > 0.10) at 0.05, violet). (B) Probability that an exact
one-sided binomial check on n local healthy people (H₀: FPR ≤ 0.15) flags a test–population pair with observed FPR above
0.25 (blue) or 0.15 (green); dashed, largest false-alarm probability among pairs with FPR ≤ 0.15. Post hoc.
