# A false-positive-rate atlas of gut-microbiome disease tests across 36 healthy populations

**Article type:** Letter, iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary.** A microbiome disease test is usually shipped with one cut-off and one false-positive
rate (FPR). We applied 28 classifiers for 14 diseases to 6,525 healthy adults in 36 populations from 20 countries that
the classifiers had never seen. A cut-off meant to flag 10% of healthy people flagged anywhere from 0% to 87%,
depending on the population. Heterogeneity was large for every classifier (I² 0.64–0.97). It was not predicted by AUROC,
and most of it was specific to the test–population pair. Recalibrating on 100 unlabelled people from the same site cut
the FPR error by 62%. Checking the cut-off on 100 local healthy people would catch most of the large errors. We release
the atlas and a small tool, fprcal, that does both.

---

To the Editor,

Stool metagenomes carry signals of colorectal cancer (CRC), inflammatory bowel disease (IBD), type 2 diabetes (T2D) and
many other diseases. Pooled analyses show that these signals carry over between countries [1–4]. The field therefore
judges classifiers by the area under the ROC curve (AUROC) in held-out cohorts [1, 5, 6]. A test in use, however, needs
one cut-off, and that cut-off fixes how many healthy people are flagged. In CRC screening every false positive leads to
a colonoscopy [7], and colonoscopy capacity is limited. A test with a good AUROC can still flag far more, or far fewer,
healthy people than its developers stated, if the healthy people at the new site differ from those in training.

How far this happens has not been measured. Earlier work found that controls from other studies doubled the false
positives of CRC classifiers, and that adding external controls to training removed most of the excess [8]. CRC models
lose calibration across countries [9], and predictors trained on industrialised populations lose accuracy elsewhere
[10]. Laboratory medicine has a fixed answer to this problem: verify reference limits on local healthy people before
use [11]. Microbiome diagnostics have no such step, and no map of where a published cut-off can be trusted.

Here, we built that map. We trained LASSO and random-forest (RF) classifiers for 14 diseases on 26 public case–control
cohorts and measured their FPR in every eligible healthy adult population in curatedMetagenomicData [12]: 36 populations,
6,525 people, 20 countries (Figure 1A). We then asked what a site can do about it, and we packaged the answer as a tool.
Analysis plans with falsification criteria were written before each confirmatory analysis and committed to the code
repository; they are internal, time-stamped plans, not external pre-registrations. We report the hypotheses that failed.

## A FIXED CUT-OFF GIVES A DIFFERENT FALSE-POSITIVE RATE IN EVERY POPULATION

Each classifier was trained on MetaPhlAn3 species profiles [13] with fixed settings. Its cut-off was the 90th percentile of
out-of-fold scores of training controls (leave-one-cohort-out when there were three or more cohorts, five-fold
cross-validation otherwise), which targets an FPR of 0.10. Five tests used 3–10 cohorts (CRC, adenoma, IBD, T2D, impaired
glucose tolerance [IGT]); nine used one cohort each (Table S1). We scored one sample per healthy adult in every
population not used in training. Before scoring, we removed 119 samples duplicated across cohorts (Pearson r > 0.99
between profiles). Our primary set is strict: no hospital, pregnancy, trial or colonoscopy-referral control groups, no
antibiotic users (Table S1). The full set (55 populations, 8,160 people) is a sensitivity analysis. We chose the strict
set after seeing the first results.

The FPR depended on where the test was used (Figure 1B). Across 489 test–population pairs for LASSO, 45% had an FPR
above 0.15, 26% above 0.25 and 24% below 0.05. In populations of at least 100 people, FPRs ranged from 0 to 0.77. For
every one of the 28 classifiers, the spread exceeded sampling noise (I² ≥ 0.5 in 28/28 classifiers; median 0.94, range
0.64–0.97). Sampling noise alone would put 15–16% of populations outside 0.05–0.15; the observed share was 50–97%
(median 66%). For a new population, the 95% prediction interval of the FPR reached 0.34 to 0.81 at its upper end for LASSO
(Figure 1C). Pooled over populations, several tests looked well calibrated (CRC 0.06, ACVD 0.10, CAD 0.12), so a pooled
FPR hides the problem.

A better classifier was not a more portable one. AUROC did not predict the between-population spread (Spearman ρ = −0.06,
P = 0.76; Figure 1D). The heterogeneity held in the 16 classifiers with AUROC ≥ 0.65. AUROC and the FPR at a fixed cut-off
answer different questions, and validation reports give only the first.

Three checks did not explain the effect away (Supporting Information S2; the first two were run for the CRC, IBD and T2D
tests). Scoring with the cross-validation fold models,
instead of the refitted model, changed little. Adjusting for age, sex, body-mass index and sequencing depth left a
population effect that accounted for 15–49% of score variance. Results in the full set matched
those in the strict set (I² ≥ 0.5 in 28/28; median 0.92).

## THE ERROR BELONGS TO THE TEST–POPULATION PAIR

Is there a "bad population" that every test over-flags, or a "bad test" that fails everywhere? Neither explained most of
the variation. In a crossed random-effects model of logit FPR, the population accounted for 17% of the variance (LASSO;
7.5% for RF), the test for 21% (46% for RF), and the test–population pair for the remaining 62% (47% for RF). Our
pre-stated hypothesis that the population would explain at least a quarter was not supported (inconclusive for LASSO,
falsified for RF).

The taxa behind each error were also test-specific. We split each over-flagged population's score shift into taxon
contributions. No taxon was among the top ten drivers in four or more of the 14 LASSO tests; two (*Ruminococcus torques*
and *Bacteroides vulgatus*) appeared in three. This falsified our expectation of a shared set of drivers. For the IBD
test, the six most over-flagged populations were Indian, Japanese and Chinese, with FPRs of 0.45–0.76 (Figure 1B). Their
scores rose because taxa the model had learned as markers of health, such as *Gemmiger formicilis* and *Ruminococcus
bromii*, were scarcer than in the training controls from the USA, UK, Spain and Denmark (Supporting Information S3).
These are fitted weights, not causal effects.

Geography mattered, but we could not confirm it. In the strict set, populations outside Europe and North America had a
higher cross-test false-alarm index (LASSO medians 0.35 vs −0.26 on the logit scale; Mann–Whitney P = 0.0008; Figure 1A).
A population's compositional distance from a test's training controls was rank-correlated with its FPR in 12 of 14 LASSO
tests. Both observations were exploratory, so we pre-registered a replication on the 19 populations of the full set that
were not in the strict set. The distance effect pointed the same way in 10 of 14 tests but missed the stated threshold
(one-sided sign test P = 0.090). The geography effect pointed the same way (+0.25) but only four of the replication
populations were outside Europe and North America (P = 0.30). We therefore treat both as hypotheses for larger, more
diverse cohorts.

## A SITE CAN VERIFY AND RECALIBRATE ITS OWN CUT-OFF

If the error belongs to the test–population pair, a fix needs data from the population that will use the test. Cut-offs
built from other cohorts failed in our earlier analysis of the CRC, IBD and T2D tests (Supporting Information S4): a
pooled reference of about 4,000 healthy people, references from the most similar populations and a reference from other
cohorts of the same country. Control augmentation [8] did not reduce the mean FPR error overall (0.087 to 0.078; P =
0.58); it helped mostly when the pool contained people from the same population.

The site's own people did. A site that tests mostly healthy people can set its cut-off without labels: score the first N
people tested and take the k-th smallest score as the cut-off, with k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the
target FPR and π_max an upper bound on disease prevalence among those people. If later healthy people are exchangeable
with this burn-in group, the expected FPR is at most α (a split-conformal argument [14, 15]), and the realised FPR follows
an exact Beta law. With N = 100 and α = 0.10, the probability that the realised FPR exceeds 0.15 is 0.055; with
N = 200 it is 0.015 (Figure 2A). A stricter rank bounds the probability that the FPR exceeds α at 0.05 [16], at a
cost in sensitivity. The rule is not new; laboratory medicine estimates reference limits from routine results in a
similar way [17]. The question is whether it works on microbiome tests and when it breaks.

Within a site, it worked for every test. We set the cut-off on 100 people from a non-random part of each large
population (the first 100 in accession order, as a stand-in for time, or the younger, leaner or one-sex half) and
evaluated it on the rest. Over 646 such evaluations in 13 populations, the mean absolute FPR error fell from 0.101 with
the training cut-off to 0.038 with the burn-in (−62%). The burn-in was better for all 28 classifiers (exact Wilcoxon
P = 7 × 10⁻⁹; Figure 2B) and in 75% of individual evaluations. This was a pre-stated hypothesis.

Across sites, it broke. In our earlier analysis of the CRC, IBD and T2D tests, a burn-in from one city or country of a
multi-site study, applied in another, was worse than the training cut-off (mean error 0.057 to 0.078), and a burn-in
from a neighbouring cohort in the same country was no better (Supporting Information S4). The rule must be run at the
site that will use the test, and repeated when sample handling, sequencing or the population served changes.

A site can also check a stated FPR directly, as clinical laboratories verify reference intervals [11]. With an exact
one-sided binomial test on n local healthy people (H₀: FPR ≤ 0.15), a check on 100 people would detect a test–population
pair with a true FPR above 0.25 with probability 0.98, and one above 0.15 with probability 0.72, while raising a false
alarm in at most 3.3% of pairs within range (Figure 2C; post hoc, treating each observed FPR as true). Fifty people
would detect 91% of the pairs above 0.25.

Recalibration has a price. When we placed 1–10% patients in the burn-in group of three large case–control cohorts (one
CRC, two T2D), the rule held the FPR below target (0.075–0.087) but sensitivity fell from 0.46 to 0.21–0.23
(Supporting Information S4). Any cut-off that meets a 10% FPR at these sites pays a similar price: one set on 100
labelled local controls gave a sensitivity of 0.245. The burn-in therefore fits population screening, where almost
everyone tested is healthy, better than tests for symptomatic patients, which need labelled local controls.

We packaged the atlas and these procedures as fprcal, a Python tool with four commands: atlas (the FPR spread of each of
the 14 tests in 32–36 populations), verify, cutoff and plan (burn-in size). Its unit tests include Monte-Carlo checks of
the two guarantees.

## CONCLUSION

The false-positive rate of a gut-microbiome disease test is a property of the test and the population together. We
suggest three changes. Cross-cohort benchmarks should report the FPR at a fixed cut-off in each held-out population,
with I² and a prediction interval, next to AUROC; STORMS-style reporting [18] could ask for this. Sites should treat a
published cut-off as provisional, verify it on local healthy people and, for screening use, recalibrate it locally.
Methods that correct processing bias or augment training controls, such as DEBIAS-M and MMUPHin [8, 19, 20], should be
judged by the FPR they deliver at new sites.

Our study has limits. All profiles came from one pipeline (MetaPhlAn3) and two standard classifiers with fixed settings;
nine tests rest on one training cohort, and several had a low AUROC. "Population" includes each study's sample
handling, which we cannot separate from biology. We did not run DEBIAS-M, MMUPHin or ConQuR [21]. The strict set was
chosen after seeing the first results, and the geography and distance findings did not replicate at the stated level.
Larger and more diverse healthy cohorts, processed together, are needed to tell how much of the error is biology.

## METHODS

Full methods, the analysis plans and deviations, every correction we tried, including those that failed, and Tables
S1–S15 are in the Supporting Information.

## ACKNOWLEDGMENTS

We thank the authors of the cohorts in curatedMetagenomicData for making their data public.
[Further acknowledgments to be completed by the authors.]

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
exact metadata file, code, analysis plans, per-person scores, the duplicate list, the per-population FPR atlas and the
fprcal tool are in the code repository: [GitHub repository URL and Zenodo DOI to be added]. Supplementary materials
(figures, tables, graphical abstract) are online in DOI or http://www.imeta.science/.

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Geng M, Li M, Li Y, et al. A universal oral microbiome-based signature for periodontitis. *iMeta*. 2024;3:e212. https://doi.org/10.1002/imt2.212
7. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
8. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
9. Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
10. Poyet M, Rühlemann M, Schaan AP, et al. Industrialization drives convergent microbiome and host physiological shifts in the human metaorganism. *Cell*. 2026. https://doi.org/10.1016/j.cell.2026.10.016
11. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
12. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
13. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
14. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
15. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
16. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
17. Ammer T, Schützenmeister A, Prokosch HU, Rauh M, Rank CM, Zierk J. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep*. 2021;11:16023. https://doi.org/10.1038/s41598-021-95301-2
18. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
19. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
20. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4
21. Ling W, Lu J, Zhao N, et al. Batch effects removal for microbiome data via conditional quantile regression. *Nat Commun*. 2022;13:5418. https://doi.org/10.1038/s41467-022-33071-9

## FIGURE LEGENDS

**Figure 1. A false-positive-rate atlas of 14 gut-microbiome disease tests in 36 healthy populations.**
(A) The 36 strict healthy adult populations (20 countries). Circle area: number of people; colour: false-alarm index,
the mean over the 14 LASSO tests of each population's deviation in logit FPR from the test mean (red: over-flagged
across tests). Populations in the same country are offset horizontally. Map: Natural Earth 1:110m (public domain).
(B) Realised FPR of each LASSO test (rows, ordered by between-population τ) in each population (columns, ordered by
false-alarm index). The cut-off targets an FPR of 0.10 (white); blue below, red above, log scale. Bold labels:
non-westernised populations. Blank cells: training cohort of that test, or fewer than 20 people.
(C) Random-effects pooled FPR (dot) and 95% prediction interval for a new population (line), LASSO (blue) and RF
(orange). Grey band: 0.05–0.15; dashed line: target.
(D) Classifier AUROC (out-of-fold on training data) against between-population τ of logit FPR, 28 classifiers.

**Figure 2. What a site can do.**
(A) Exact probability that the realised FPR exceeds 0.15 when the cut-off is the k-th smallest of N burn-in scores from
the same population (expected-FPR rule, blue; rule bounding P(FPR > 0.10) at 0.05, orange). The saw-tooth comes from
rounding of the rank k. Dashed line: N = 100.
(B) Mean absolute deviation of the FPR from 0.10 within site, training cut-off (orange) versus burn-in on 100 people
from a non-random part of the same population (blue), for each of the 28 classifiers (13 populations, 646 evaluations).
(C) Probability that an exact one-sided binomial check on n local healthy people (H₀: FPR ≤ 0.15, level 0.05) flags a
LASSO test–population pair with an observed FPR above 0.25 (blue) or 0.15 (green); dashed: largest false-alarm
probability among pairs with FPR ≤ 0.15. Post hoc; observed FPRs are treated as true.
