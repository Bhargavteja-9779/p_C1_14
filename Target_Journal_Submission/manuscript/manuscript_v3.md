# The false-positive rate of a gut-microbiome test belongs to the population, not to the test

**Article type:** Short Communication (Letter), iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary (about 100 words).** Gut-metagenome disease classifiers are sold with one specificity, set
on training controls. We applied colorectal cancer (CRC), inflammatory bowel disease (IBD) and type 2 diabetes (T2D)
classifiers to 8,329 healthy adults from 60 public cohorts in 28 countries that the classifiers had never seen. A cut-off
meant to flag 10% of healthy people flagged 0% to 87%, depending on the cohort. Cohort identity explained 20–42% of the
variance in healthy people's scores. Age, sex, BMI, sequencing depth and diversity explained none of it. A large external
reference did not fix the cut-off. Self-calibrating on about 100 unlabelled people tested locally did, with an exact,
verifiable guarantee.

---

To the Editor,

Stool metagenomes can flag colorectal cancer (CRC), inflammatory bowel disease (IBD) and type 2 diabetes (T2D), and
pooled studies show that microbial signatures carry over between countries [1–4]. These studies judge classifiers mainly
by the area under the ROC curve (AUROC) in held-out cohorts [1, 2, 5]. A test in use needs one cut-off, and the cut-off is
usually fixed to cap the false-positive rate (FPR), because each false positive in CRC screening leads to a colonoscopy
[6]. Wirbel et al. set the cut-off at 10% FPR on training controls and found an FPR of 0.097 when held-out controls were
pooled [1]. Moved naively between studies, such models showed on average more than twice the intended false positives,
and adding external healthy controls to training ("control augmentation") was proposed as the fix [7]. A commercial
dysbiosis index was checked in healthy people from six countries and judged transferable [8]. Pooled or few-population
checks can hide large differences between populations. Clinical laboratories know this problem from reference intervals,
which must be checked on local healthy people before use [9]. To our knowledge, no study has measured the FPR of
fixed-specificity disease classifiers population by population across dozens of healthy cohorts, asked what the
variation is attributable to, or tested whether control augmentation removes it.

We measured it. We trained standard classifiers on public case–control cohorts and applied them to every eligible healthy
adult in curatedMetagenomicData [10] that they had not seen. We then asked why the FPR moves, and what restores it. We
wrote down hypotheses, falsification criteria and a cohort split before each analysis; we report the hypotheses that
failed as well as those that held (Supporting Information).

## ONE CUT-OFF, 60 POPULATIONS, FALSE-POSITIVE RATES FROM 0% TO 87%

We trained LASSO logistic regression and random-forest (RF) classifiers with fixed settings on 10 CRC, 4 IBD and 4 T2D
case–control cohorts (MetaPhlAn3 species profiles [11]). We removed one CRC cohort whose 80 samples duplicate another
cohort. The cut-off was the 90th percentile of leave-one-cohort-out scores of training controls, which targets an FPR of
0.10, following [1]. We then scored 8,329 healthy adults from 60 cohorts in 28 countries, 12 of them non-westernised
populations. Every cohort that contributed to training was excluded from that classifier's test set. Each classifier
was tested on 46–55 populations of at least 15 people (7,437–8,211 people).

Pooled over people, the FPR looked acceptable: 0.05 (CRC), 0.12 (IBD) and 0.14 (T2D) for LASSO (Figure 1). Population by
population, it did not. The CRC cut-off flagged 0% to 56% of healthy people with LASSO and 0% to 87% with RF. For the IBD
and T2D classifiers the range was 0% to 84%. In 61–69% of populations, the FPR fell outside 0.05–0.15, the band within half
the target. The spread was far beyond sampling noise (chi-square test of equal proportions, P < 10⁻¹¹⁰ for every
classifier). Errors ran in both directions. The CRC classifier was too strict in 25 of 46 populations (FPR < 0.05), which
means lost sensitivity there. It was far too loose in a few populations (0.21–0.56), which means extra colonoscopies. The
IBD and T2D classifiers over-flagged in 11–17 populations each (FPR > 0.20).

We expected two patterns that did not appear. First, we expected some populations to be over-flagged by every test.
The cohort FPRs of the three tests were only weakly correlated (Spearman ρ = 0.16–0.38; one of six correlations had
P < 0.05). Second, we expected the CRC classifier to over-flag non-westernised populations. It did not (median FPR 0.08 vs
0.04; one-sided Mann–Whitney P = 0.32 for LASSO, 0.89 for RF). In a post hoc comparison, the T2D LASSO classifier did
over-flag non-westernised populations (median FPR 0.22 vs 0.11, P = 0.005). So the error belongs to the pairing of a test
with a population, and no single list of "risky populations" can correct it.

## THE ERROR LIVES AT THE COHORT LEVEL, AND NO OUTSIDE REFERENCE PREDICTS IT

Why does the FPR move? We fitted linear mixed models to healthy people's scores, with a random intercept for cohort. Cohort
identity explained 20–42% of score variance (intraclass correlation, ICC; Figure 2A). Age, sex, BMI, log sequencing depth,
Shannon diversity and richness were each associated with the score, as host variables are in case–control studies [12]. Adding all of them changed the between-cohort
variance by −24% to +39%, and the adjusted ICC stayed between 0.21 and 0.35. The cut-off therefore moves with something
shared by everyone in a cohort, such as sample handling, DNA extraction, sequencing batch or the local population. It does
not move with measurable traits of the person. Kit metadata were missing or inconsistent for many cohorts, so we could not
separate these causes.

This has a practical consequence. Three corrections that use data from outside the target population all failed on
development cohorts. These were: a person-level adjustment for the main axes of healthy microbiome variation; a cut-off
taken from a pooled reference of about 4,000 healthy people; and a cut-off taken from the one to five populations most
similar in composition. The person-level adjustment narrowed the spread of cohort FPR only slightly and cut CRC AUROC
from 0.76 to 0.61–0.68. The pooled reference was no better than the training cut-off. The composition-matched references
were no better than randomly chosen ones (Table S3). On the 31 populations we had locked away, the pooled reference again
did no better than the status quo (Figure 2B). After our literature check we added control augmentation [7] as a post hoc
comparator. We retrained every classifier with all development-split healthy cohorts added as controls and tested it on
the locked populations. It did not narrow the error: across the 50 population–classifier pairs with at least 70 people,
the mean absolute deviation from 0.10 was 0.070 without augmentation and 0.066 with it (Wilcoxon P = 0.69). Each version had
42% of pairs within 0.05–0.15. Augmentation helped the IBD classifiers but harmed the CRC classifiers. On the external CRC
cohort YachidaS_2019, the augmented LASSO cut-off flagged 26% of controls. In earlier case–control analyses, AUROC also
failed to predict the error, and controls borrowed from a neighbouring site did not fix it (Supporting Information S5).
If outside data cannot predict a population's FPR, the population has to measure it.

## SELF-CALIBRATION ON THE FIRST ~100 PEOPLE TESTED, WITH AN EXACT GUARANTEE

A new screening site does not need labels to do this. In screening, almost everyone tested is healthy (CRC prevalence in
screening is below 1%). We propose a burn-in rule. Score the first N people tested and set the cut-off at the k-th
smallest score, with k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the target FPR and π_max an upper bound on disease
prevalence among those people. If later people are exchangeable with the burn-in group, the expected FPR is at most α for
any true prevalence up to π_max. This follows from split-conformal arguments [13, 14] and the fact that the flagged share
of a mixed group is at least (1 − π) times its FPR; conformal outlier detection with contaminated reference data behaves
the same way [15]. A stricter variant picks k so that P(FPR > α) ≤ 0.05, using the order-statistic tolerance bound behind
Neyman–Pearson classification [16]. Laboratory medicine uses the same idea, setting reference limits from routine,
unlabelled and partly abnormal results [17, 18]. The rule is therefore an adaptation of known tools, not a new theorem;
what is new is the evidence that, for microbiome tests, nothing short of it works. The number of people flagged in an evaluation
set then follows an exact beta-binomial law, so a site can work out N before it starts.

We fixed the rule, the comparators and a success criterion before touching the 31 locked healthy populations and the
locked case–control cohorts (two external CRC cohorts; IBD and T2D by leave-one-cohort-out). Each population was split at
random 200 times into a burn-in group of N people and an evaluation group. With N = 100, the mean absolute FPR error fell
from 0.063 (training cut-off) to 0.029 (−54%). The share of burn-ins with FPR above 0.15 was 0.085, and the stricter
variant kept the FPR above 0.10 in only 4.5% of burn-ins. All three pre-stated criteria were met (Figure 2B). The exact law
predicted the share of burn-ins with FPR above 0.15 almost perfectly: 0.119 predicted vs 0.120 observed at N = 25, 0.135
vs 0.127 at N = 50, 0.088 vs 0.085 at N = 100, and 0.050 vs 0.049 at N = 200. The fit held population by population (Figure
3A). People within a cohort therefore behave as exchangeable, which is the one assumption the guarantee needs.

The rule also held when patients were mixed into the burn-in group (Figure 3B). In the locked case–control cohorts, the
training cut-off gave a mean FPR of 0.29 instead of 0.10. With N = 100 and 1–10% patients in the burn-in group, the burn-in
rule gave a mean FPR of 0.075–0.087, below target as the bound requires. When we set π_max to 0.01 but the true prevalence
was 0.05, the mean FPR was still 0.082. Sensitivity fell from 0.46 to about 0.22. This is the price of returning the FPR to
the stated value: the training cut-off's higher sensitivity came from flagging almost three times the promised share of
healthy people.

## WHAT THIS MEANS FOR MICROBIOME DIAGNOSTICS

A gut-microbiome classifier's specificity is not a fixed property that can be printed on a label. It belongs to the
population tested, it varies more than ten-fold between populations, and pooled validation hides this. We suggest three
changes. First, cross-cohort benchmarks should report the realised FPR cohort by cohort at a fixed cut-off, next to AUROC,
and STORMS-style reporting [19] could ask for it. Second, a site that adopts a published classifier should treat its cut-off
as provisional and self-calibrate on its first ~100 unlabelled tests, using the exact law to choose N and α. A site that
needs a high-confidence guarantee should use the stricter variant. Third, methods that correct processing bias or
augment training controls, such as DEBIAS-M, MMUPHin and control augmentation [7, 20, 21], should be judged by the FPR they deliver at new sites, not only by AUROC.

Our study has limits. All profiles come from one pipeline (MetaPhlAn3); other profilers may shift scores differently. The
healthy cohorts were recruited for many purposes, and some "controls" are hospital patients (for example, the most
over-flagged CRC population). We used two standard classifiers with fixed settings, not the best possible models. The
burn-in guarantee assumes that the first people tested resemble later ones; a site whose population changes over time
needs to recalibrate. In real screening, positive results are confirmed later, which allows the cut-off to be refined
with labels. We did not test these extensions.

## METHODS

Full methods, the pre-registered protocols (atlas, cohort split, burn-in evaluation), every hypothesis tried (including
those that failed) and the supplementary tables are in the Supporting Information.

## AUTHOR CONTRIBUTIONS

[To be completed by the authors.]

## CONFLICT OF INTEREST STATEMENT

[To be completed by the authors.]

## FUNDING

[To be completed by the authors.]

## ETHICS STATEMENT

This study reanalysed public, de-identified data. No new ethics approval was required.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles and metadata are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31; MetaCardis
2022-10-19). Code, protocols, per-person scores and all results: [GitHub repository URL and Zenodo DOI to be added].

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
7. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
8. Hiseni P, Furu K, Wang Pedersen V, et al. Towards standardized gut microbiota diagnostics: normobiosis beyond geographical borders. *Gut Microbes*. 2026;18:2701485. https://doi.org/10.1080/19490976.2026.2701485
9. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
10. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
11. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
12. Vujkovic-Cvijin I, Sklar J, Jiang L, Natarajan L, Knight R, Belkaid Y. Host variables confound gut microbiota studies of human disease. *Nature*. 2020;587:448–454. https://doi.org/10.1038/s41586-020-2881-9
13. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
14. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
15. Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. *Proc ICML*. 2025. arXiv:2502.04807
16. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
17. Zierk J, Arzideh F, Kapsner LA, Prokosch HU, Metzler M, Rauh M. Reference interval estimation from mixed distributions using truncation points and the Kolmogorov–Smirnov distance (kosmic). *Sci Rep*. 2020;10:1704. https://doi.org/10.1038/s41598-020-58749-2
18. Ammer T, Schützenmeister A, Prokosch HU, Rauh M, Rank CM, Zierk J. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep*. 2021;11:16023. https://doi.org/10.1038/s41598-021-95301-2
19. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
20. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
21. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4

## FIGURE LEGENDS

**Figure 1. One cut-off gives very different false-positive rates in healthy populations.** Each dot is one healthy adult
population (at least 15 people) not used to train the classifier. The y-axis is the share flagged by a LASSO classifier
whose cut-off targets an FPR of 0.10 (dashed line; blue band 0.05–0.15). Orange diamonds: non-westernised populations.
Bars: exact 95% binomial confidence intervals. Panel titles give the FPR pooled over people and the share of populations
outside the band. Random forest: Figure S1.

**Figure 2. The error sits at the cohort level, and only local self-calibration removes it.** (A) Share of healthy
people's score variance that lies between cohorts (intraclass correlation from linear mixed models), without (blue) and
with (orange) adjustment for age, sex, BMI, log sequencing depth, Shannon diversity and richness. (B) Mean absolute
deviation of the realised FPR from 0.10 in locked healthy populations, by burn-in size N (populations with at least N + 20
people; 200 random burn-in/evaluation splits each). Grey: training cut-off. Yellow: cut-off from the pooled healthy
reference. Blue: burn-in rule for expected FPR ≤ 0.10. Green: stricter burn-in rule for P(FPR > 0.10) ≤ 0.05, which aims
below 0.10 by design and so has a larger absolute deviation.

**Figure 3. The exact law predicts each population, and the rule tolerates patients in the burn-in group.** (A) Observed
vs predicted share of burn-ins with evaluated FPR above 0.15 (burn-in rule; one dot per locked population × classifier ×
N). Dashed line: identity. (B) Mean realised FPR in locked case–control cohorts (N = 100) when a share π of the burn-in
group are patients; π_max is the assumed upper bound (equal to π unless stated). Dashed line: target 0.10.
