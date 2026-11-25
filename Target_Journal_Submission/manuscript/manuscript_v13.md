# Gut-microbiome classifiers flag healthy people at population-specific rates, and pooled training can turn a region's normal microbiome into a disease signal

**Article type:** Letter, iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary.** A gut-microbiome classifier is published with one cut-off and one false-positive rate
(FPR). We measured the FPR of 28 disease classifiers in 6,525 healthy adults from 36 populations they had never seen: the
same cut-off flagged 0% to 77% of healthy people, depending on the population. A published gut-health index did the same
in its own training data: it labelled 64% of healthy people in East Asian studies as non-healthy, against 12% elsewhere.
Taxa common in healthy East Asian guts, such as *Bacteroides plebeius*, carry "disease" weights, consistent with East
Asian samples making up most of the non-healthy training data. In a retraining experiment, balancing training data by
country removed 88% of this gap. Recalibrating on 100 unlabelled people from the same site cut the FPR error by 62% across
the 28 classifiers and by 79% for the index, at a cost in sensitivity when patients are among those 100 people.

---

To the Editor,

Stool metagenomes carry signals of colorectal cancer (CRC), inflammatory bowel disease (IBD), type 2 diabetes (T2D) and
many other diseases, and pooled analyses show that these signals carry over between countries [1–4]. The field therefore
judges classifiers by the area under the ROC curve (AUROC) in held-out cohorts [1, 5, 6]. A test in use, however, needs
one cut-off, and that cut-off fixes how many healthy people are flagged. In CRC screening every false positive leads to a
colonoscopy [7]. A classifier with a good AUROC can still flag far more, or far fewer, healthy people than its developers
stated if the healthy people at a new site differ from those in training.

How far this happens, and why, has not been measured. Controls from other studies doubled the false positives of CRC
classifiers [8], CRC models lose calibration across countries [9], and predictors trained on industrialised populations
lose accuracy elsewhere [10]. Laboratory medicine handles the problem by verifying reference limits on local healthy
people before use [11]. Microbiome diagnostics have no such step.

Here we measured the FPR of 28 classifiers for 14 diseases in every eligible healthy adult population in
curatedMetagenomicData [12] (36 populations, 6,525 people, 20 countries), then audited a published, publicly released
classifier, the Gut Microbiome Wellness Index 2 (GMWI2) [13], in its own training data and in populations it never saw.
This audit led to a mechanism, which we tested by retraining. We also tested two fixes. Confirmatory analyses followed
time-stamped internal analysis plans with falsification criteria, committed to the code repository before they were run
("pre-specified"); one later plan was committed only together with its results, and we treat that analysis as post hoc.
We report the hypotheses that failed and label every other analysis as post hoc.

## A FIXED CUT-OFF GIVES A DIFFERENT FALSE-POSITIVE RATE IN EVERY POPULATION

We trained LASSO logistic regression (C = 0.1) and random-forest (RF; 500 trees) classifiers on MetaPhlAn3 species
profiles [14] from 26 case–control cohorts. Each cut-off was the 90th percentile of out-of-fold scores of training
controls, which targets an FPR of 0.10 (Table S1). We scored one sample per healthy adult in every population not used in
training, after removing 119 samples duplicated across cohorts (Pearson r > 0.99). Our primary set excludes hospital,
pregnancy, trial and colonoscopy-referral control groups and antibiotic users. We chose this strict set after seeing the
first results, so the full set (55 populations, 8,160 people) is reported throughout as a check.

The FPR depended on where the classifier was used (Figure 1B). Of 489 LASSO classifier–population pairs, 45% had an FPR
above 0.15, 26% above 0.25 and 24% below 0.05. In populations of at least 100 people, LASSO FPRs ranged from 0 to 0.77.
The spread exceeded sampling noise for all 28 classifiers (I² ≥ 0.5; median 0.94, range 0.64–0.97; Cochran's Q and
prediction intervals per classifier in Table S2; full set: 28/28, median 0.92). Sampling noise alone would put 15–16% of populations outside 0.05–0.15; the observed share was 50–97%. For a
new population, the upper end of the 95% prediction interval of the FPR ranged from 0.22 (CRC) to 0.81 (impaired glucose
tolerance) for LASSO (Figure 1C). Pooled over populations, several classifiers looked well calibrated (CRC 0.06,
atherosclerotic cardiovascular disease 0.10), so a pooled FPR hides the problem.

Seven of the 28 classifiers had an out-of-fold AUROC below 0.6 (three below 0.5); they carry little disease signal.
Restricting to the 16 classifiers with AUROC ≥ 0.65 changed nothing: I² median 0.94 (minimum 0.71), with 62% of
populations outside the band. AUROC did not predict the spread (Spearman ρ = −0.06, P = 0.76; Figure 1D). A better
classifier was not a more portable one.

The error was mostly specific to the pairing of classifier and population. In a crossed random-effects model of logit
FPR, the population accounted for 17% of the variance (LASSO), the classifier for 21% and the pair for 62%. Adjusting for
age, sex, body-mass index and sequencing depth left a population effect, and scoring with the cross-validation fold models
instead of the refitted model changed little (Supporting Information S2).

## A PUBLISHED GUT-HEALTH INDEX MISLABELS WHOLE REGIONS, EVEN IN ITS OWN TRAINING DATA

Our 28 classifiers are research models. To test a classifier that others use, we audited GMWI2 [13], a published L1
logistic regression on the presence of 95 MetaPhlAn3 taxa, trained on 8,069 stool metagenomes from 54 studies, with a
published cut-off (GMWI2 > 0 = healthy). We extracted its coefficients from the released model and checked them against
the paper's Supplementary Data (95/95 identical). The developers' own scores show that 20.8% of their healthy training
samples (5,514 people in the 44 studies with at least 20 healthy people) fall below the cut-off. We use this training FPR,
not an independent target, as the rate the index should deliver elsewhere.

Within GMWI2's own training data, the published cut-off labelled 0% to 84% of healthy people as non-healthy, depending
on the study (44 studies with ≥ 20 healthy people; I² = 0.96; Figure 2A). This result uses only the developers' published
scores. All eight studies above 50% were from China or Japan. Across the 13 East Asian studies, the median was 0.64
(range 0.25–0.84; 657 of 1,067 healthy people); across the 31 other studies it was 0.12 (range 0–0.40; Mann–Whitney
P = 5 × 10⁻⁷; post hoc). Healthy people in rural Africa were almost never mislabelled (0–7%).

In healthy populations that GMWI2 never saw, the pattern held (pre-specified). Our implementation reproduced the
published scores (r = 0.991, same call for 98.4% of 704 shared samples). In 15 unseen strict populations (1,914 people),
the FPR ranged from 0 to 0.54 (I² = 0.92; 95% prediction interval 0.02–0.68), and 80% of populations fell outside 0.10–0.31,
against 9% expected from sampling noise (exact P = 6 × 10⁻¹³, Holm-adjusted 2 × 10⁻¹²; Figure 2B). We had expected
in-sample optimism, that is, a lower FPR in populations GMWI2 had seen in training; this hypothesis was falsified (mean
0.26 seen vs 0.20 unseen; P = 0.72). The four unseen East Asian populations had FPRs of 0.25–0.54 (median 0.38 vs 0.20
elsewhere; P = 0.065; post hoc), consistent with the training-data result but too few for a separate test.

## WHY: POOLED TRAINING TURNS A REGION'S NORMAL MICROBIOME INTO A DISEASE SIGNAL

Which taxa drive the gap? We split the difference in mean GMWI2 score between East Asian and other healthy populations
into taxon contributions (post hoc). The largest came from taxa with "non-healthy" weights that are common in healthy East
Asian guts (Figure 2C): *Bacteroides plebeius* (present in 72% of East Asian healthy people vs 18% elsewhere),
*Bacteroides coprocola* (45% vs 11%), *Bacteroides stercoris* (79% vs 41%) and *Lachnoclostridium* (68% vs 45%).
*B. plebeius* is a well-known marker of diet and geography: Japanese strains acquired seaweed-degrading enzymes from
marine bacteria [15].

The training data explain the weights. In GMWI2's training set, East Asian samples made up 62% of the non-healthy samples
(1,574 of 2,522) but only 20% of the healthy ones (1,097 of 5,547; odds ratio 6.7). A model asked to separate healthy from
non-healthy across pooled studies can therefore learn region-typical commensals as disease markers. That country
confounding can inflate microbiome classifier performance was shown with SIAMCAT [8]; what we add is its consequence for
the false-positive rate of a published, deployed index, its size (odds ratio 6.7; 64% vs 12%) and a test by retraining.

We tested this mechanism by retraining (pre-specified). We trained a classifier with the GMWI2 recipe from scratch on
10,986 people in 61 curatedMetagenomicData studies, holding out one study at a time. Trained on pooled data, it reproduced
the effect: healthy people in East Asian studies were labelled non-healthy at a median of 0.71, against 0.19 elsewhere
(gap 0.52; 9 vs 43 studies; Figure 2D). Weighting training samples so that, within each country, healthy and non-healthy
people carried equal weight cut the gap to 0.06, an 88% reduction (study-clustered bootstrap 95% CI 41–149%; the
interval includes reductions below our pre-stated criterion of 50%), and lowered between-study heterogeneity (τ 1.16 to
0.81). It cost discrimination: pooled AUROC fell from 0.715 to 0.676 (−0.040; CI
−0.12 to 0.02), beyond our pre-stated margin of 0.03, so that hypothesis failed. Part of the pooled AUROC came from the
geographic shortcut itself. Within studies, where cases and controls share a geography, AUROC fell only from 0.669 to
0.649 (−0.020; CI −0.052 to 0.013; post hoc).

Balancing did not carry over cleanly to the five multi-cohort disease classifiers (post hoc; a related but not identical
weighting that also gave each country equal weight; Supporting Information S6). On the logit scale, between-population
heterogeneity fell in four of five classifiers (mean τ 0.92 to 0.78; population-clustered 95% CI of the difference −0.22 to
−0.01). On the FPR scale it did not: the median absolute deviation of the FPR fell in only two of five, and balancing moved
FPR levels away from target (median CRC FPR 0.04 to 0.33; T2D 0.12 to 0.54). The share of populations outside 0.05–0.15
rose from 66% to 82%, and AUROC fell by 0.033, beyond the 0.03 margin. Both stated criteria failed. Balancing is a
training-time fix for one known confounder, not a deployment fix, so for deployment we turn to the site.

## A SITE CAN VERIFY AND RECALIBRATE ITS OWN CUT-OFF

Balancing addresses one cause at training time; it does not remove the classifier–population error of Figure 1. For that,
the site needs its own data. In a first-stage analysis of the CRC, IBD and T2D classifiers (Supporting Information S4),
cut-offs set on other cohorts failed: a pooled reference of about 4,000 healthy people, references from the most similar
populations, and other cohorts from the same country. Adding external controls to training [8] did not reduce the mean
FPR error (0.087 to 0.078; P = 0.58).

A site that tests mostly healthy people can recalibrate without labels. It scores its first N tests and takes the k-th
smallest score as the cut-off, with k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the target FPR and π_max an upper bound on
disease prevalence. If later healthy people are exchangeable with this burn-in group, the expected FPR is at most α (a
split-conformal argument [16, 17]), and the realised FPR follows an exact Beta law: with N = 100 and α = 0.10, the
probability that the FPR exceeds 0.15 is 0.055 (Figure 3A). A stricter rank bounds P(FPR > α) at 0.05 [18]. The rule is
not new; laboratory medicine sets reference limits from routine results in a similar way [19]. What we tested is whether
it survives a non-random split within a site and whether it fails across sites.

Within a site, it worked, in a retrospective within-cohort test; no prospective test was run. We set the cut-off on 100 people from a non-random part of each large population (the first 100
in accession order, or the younger, leaner or one-sex half) and evaluated it on the rest. Across 13 populations and 28
classifiers, the mean absolute FPR error fell from 0.101 to 0.038, a 62% reduction (population-clustered 95% CI 51–70%;
better in 13/13 populations and 28/28 classifiers; Figure 3B; pre-specified). For GMWI2, with its stated FPR as target, the
error fell from 0.21 to 0.04 (a 79% reduction; CI 64–85%; 11/13 populations). This was a pre-specified
hypothesis in the GMWI2 plan.

Across sites, it broke. In the first-stage analysis, a burn-in from one city or country of a multi-site study, applied in
another, was no better than the training cut-off (Supporting Information S4). The rule must be run at the site that will
use the test, and repeated when sample handling, sequencing or the population served changes.

Recalibration has a price. When 1–10% of the burn-in group were patients, the rule held the FPR near target but
sensitivity fell from 0.46 to 0.21–0.23 (Supporting Information S4); a cut-off set on 100 labelled local controls gave a
sensitivity of 0.245. The burn-in fits population screening, where almost everyone tested is healthy, better than tests
for symptomatic patients. A site can also check a stated FPR directly: an exact one-sided binomial test on 100 local
healthy people (H₀: FPR ≤ 0.15) detects a classifier–population pair whose observed FPR exceeds 0.25 with probability
0.98, and one above 0.15 with probability 0.72 (n = 100; Figure 3C; post hoc). We release the atlas and these
procedures as fprcal, a small Python tool with Monte-Carlo unit tests.

## CONCLUSION

The false-positive rate of a gut-microbiome disease test is a property of the test and the population together, and pooled
training across geographically unbalanced studies is one reason why: it can encode a region's normal microbiome as a
disease signal. We suggest four changes. Cross-cohort benchmarks should report the FPR at a fixed cut-off in each held-out
population, with I² and a prediction interval, next to AUROC; STORMS-style reporting [20] could ask for this. Developers
should check the geographic case mix of pooled training data and report performance within studies, not only pooled. Sites should treat a
published cut-off as provisional, verify it on local healthy people and, for screening, recalibrate it locally. Methods
that correct processing bias or augment training controls, such as DEBIAS-M and MMUPHin [8, 21, 22], should be judged by
the FPR they deliver at new sites.

Our study has limits. All profiles came from one pipeline (MetaPhlAn3); our 28 classifiers used fixed settings, nine rest
on one training cohort, and seven had an AUROC below 0.6. "Population" includes each study's sample handling, which we
cannot fully separate from biology, although the GMWI2 case-mix result points to a cause that is not purely technical. We
did not run DEBIAS-M, MMUPHin or ConQuR [23]. The strict set and the East Asian comparison were chosen after seeing
results and are labelled post hoc; the geography and distance findings for the 14-disease atlas did not replicate at the
stated level. All site-level results are retrospective. Larger, geographically balanced healthy cohorts, processed
together, and a prospective deployment are needed to separate biology from batch and to confirm the site-level fix.

## METHODS

Full methods, the analysis plans and deviations, every correction we tried, including those that failed, and Tables
S1–S20 are in the Supporting Information. In brief: MetaPhlAn3 species (or, for GMWI2, all-rank) relative abundances;
LASSO (C = 0.1) and random forest (500 trees); cut-off = 90th percentile of out-of-fold control scores; heterogeneity by
DerSimonian–Laird on logit FPR; crossed random effects for the variance decomposition; study-clustered bootstrap for the
case-mix analysis.

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

This study reanalysed public, de-identified data. The original studies obtained ethics approval and informed consent as
described in their publications. No new ethics approval was required.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31; MetaCardis 2022-10-19). The
GMWI2 model is from its public release (bioconda gmwi2 1.6, MIT licence) and the published Supplementary Data [13]. The
exact metadata file, code, analysis plans, per-person scores, the duplicate list, the per-population FPR atlas and the
fprcal tool are in the code repository: [GitHub repository URL and Zenodo DOI to be added]. Supplementary materials are
online at the journal.

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Geng M, Li M, Li Y, et al. A universal oral microbiome-based signature for periodontitis. *iMeta*. 2024;3:e212. https://doi.org/10.1002/imt2.212
7. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
8. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
9. Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707 (Correction: https://doi.org/10.3389/fmicb.2026.2021752)
10. Poyet M, Rühlemann M, Schaan AP, et al. Industrialization drives convergent microbiome and host physiological shifts in the human metaorganism. *Cell*. 2026. https://doi.org/10.1016/j.cell.2026.10.016
11. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
12. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
13. Chang D, Gupta VK, Hur B, et al. Gut Microbiome Wellness Index 2 enhances health status prediction from gut microbiome taxonomic profiles. *Nat Commun*. 2024;15:7447. https://doi.org/10.1038/s41467-024-51651-9
14. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
15. Hehemann JH, Correc G, Barbeyron T, Helbert W, Czjzek M, Michel G. Transfer of carbohydrate-active enzymes from marine bacteria to Japanese gut microbiota. *Nature*. 2010;464:908–912. https://doi.org/10.1038/nature08937
16. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
17. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
18. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
19. Ammer T, Schützenmeister A, Prokosch HU, Rauh M, Rank CM, Zierk J. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep*. 2021;11:16023. https://doi.org/10.1038/s41598-021-95301-2
20. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
21. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
22. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4
23. Ling W, Lu J, Zhao N, et al. Batch effects removal for microbiome data via conditional quantile regression. *Nat Commun*. 2022;13:5418. https://doi.org/10.1038/s41467-022-33071-9

## FIGURE LEGENDS

**Figure 1. A false-positive-rate atlas of 14 gut-microbiome disease tests in 36 healthy populations.** (A) The 36 strict
healthy adult populations (20 countries); circle area, number of people; colour, mean deviation in logit FPR from the test
mean across the 14 LASSO tests. (B) Realised FPR of each LASSO test (rows, ordered by between-population τ) in each
population (columns). Cut-off targets FPR 0.10 (white); blue below, red above, log scale. Blank cells: training cohort or
fewer than 20 people. (C) Random-effects pooled FPR (dot) and 95% prediction interval for a new population (line), LASSO
(blue), RF (orange); grey band 0.05–0.15. (D) Classifier AUROC (out-of-fold) against between-population τ, 28 classifiers;
AUROC < 0.6 marked.

**Figure 2. A published gut-health index (GMWI2), and why it mislabels regions.** (A) Share of healthy training samples
labelled non-healthy by the published GMWI2 cut-off, per study, from the developers' own published scores (44 studies ≥ 20
healthy people); orange, East Asian studies; dashed line, stated rate 0.21; bars, exact 95% intervals. (B) The same for
healthy populations in curatedMetagenomicData, our scoring (QC against published scores r = 0.99); open symbols,
populations that were in GMWI2's training data. (C) The eight taxa contributing most to the East Asian–other score gap;
fitted GMWI2 weight in parentheses; dots, share of healthy people carrying the taxon, by region. (D) A GMWI2-recipe
classifier retrained on curatedMetagenomicData, leave-one-study-out: FPR per healthy study under pooled training versus
training with country-balanced sample weights; lines, studies (orange, East Asian); diamonds, regional medians.

**Figure 3. What a site can do.** (A) Exact probability that the realised FPR exceeds 0.15 when the cut-off is the k-th
smallest of N burn-in scores from the same population (expected-FPR rule, blue; rule bounding P(FPR > 0.10) at 0.05,
orange). (B) Mean absolute deviation of the FPR from 0.10 within site: training cut-off (orange) versus burn-in on 100
people from a non-random part of the same population (blue), for each of 28 classifiers (13 populations, 646 evaluations).
(C) Probability that an exact one-sided binomial check on n local healthy people (H₀: FPR ≤ 0.15) flags a test–population
pair with observed FPR above 0.25 (blue) or 0.15 (green); dashed, largest false-alarm probability among pairs with
FPR ≤ 0.15. Post hoc.
