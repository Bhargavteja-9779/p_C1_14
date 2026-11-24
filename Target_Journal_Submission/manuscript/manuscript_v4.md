# Gut-microbiome disease tests miss their stated false-positive rate in most healthy populations and must be recalibrated at each site

**Article type:** Short Communication (Letter), iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary (about 100 words).** We applied colorectal cancer (CRC), inflammatory bowel disease (IBD)
and type 2 diabetes (T2D) classifiers to 6,525 healthy adults from 36 general-population cohorts in 20 countries that
the classifiers had never seen. A cut-off meant to flag 10% of healthy people flagged anywhere from 0% to 76%,
depending on the cohort and the classifier (I² 0.70–0.95). Rarer "health-marker" taxa from the training populations explained most of
this. Corrections borrowed from other cohorts, including a cohort from the same country, did not fix the cut-off.
Recalibrating on about 100 unlabelled people tested at the same site did. This held when the case mix shifted,
but not when the people came from another site.

---

To the Editor,

Stool metagenomes can flag colorectal cancer (CRC), inflammatory bowel disease (IBD) and type 2 diabetes (T2D), and
pooled studies show that microbial signatures carry over between countries [1–4]. These studies judge classifiers mainly
by the area under the ROC curve (AUROC) in held-out cohorts [1, 2, 5]. A test in use needs one cut-off. The cut-off is
usually fixed to cap the false-positive rate (FPR), because in CRC screening each false positive leads to a colonoscopy [6].
Wirbel et al. set the cut-off at 10% FPR on training controls and found an FPR of 0.097 when held-out controls were
pooled [1]. Moved naively between studies, such models produced on average more than twice the intended false positives.
Adding external healthy controls to training ("control augmentation") was proposed as the fix [7]. A commercial
dysbiosis index was checked in healthy people from six countries and judged transferable [8]. Clinical laboratories
know the underlying problem from reference intervals, which must be checked on local healthy people before use [9].
To our knowledge, no study has measured the FPR of fixed-specificity microbiome classifiers population by population
across dozens of healthy cohorts. None has asked what drives the variation, or which corrections remove it.

Here, we measured the FPR of six standard classifiers in every eligible healthy adult cohort in curatedMetagenomicData
[10]. We then asked why it moves and what restores it. Three numbers summarise the answer:

- Between populations, the FPR varies far more than sampling noise allows: a new population's 95% prediction interval
  spans 0.01–0.22 for the CRC LASSO test and 0.01–0.63 for the IBD LASSO test.
- Corrections that use other cohorts leave it there: a same-country reference put only 22–58% of cohorts in the
  0.05–0.15 band.
- A burn-in on 100 people at the site of use halves the error, but only if those people come from the same site.

We wrote analysis plans with falsification criteria and a cohort split before each analysis. These are internal,
time-stamped plans in the code repository, not external pre-registrations. We report the hypotheses that failed as
well as those that held.

## WHAT WE MEASURED, AND WHAT A FIRST REVIEW CHANGED

We trained LASSO logistic regression and random-forest (RF) classifiers with fixed settings on 10 CRC, 4 IBD and 4 T2D
case–control cohorts (MetaPhlAn3 species profiles [11]). The cut-off was the 90th percentile of leave-one-cohort-out
scores of training controls, which targets an FPR of 0.10 [1]. We then scored healthy adults (one sample per person) from
every cohort not used to train that classifier.

Our first version of this analysis (Supporting Information, S5) over-stated two things, and an internal statistical
review found both. First, some people appeared in two public cohorts. A profile-level search (Pearson r > 0.99 between
log profiles) found 119 duplicated samples: one healthy cohort was a copy of a CRC cohort, and two other healthy cohorts
shared 29–35% of their people with training cohorts. We removed every duplicate, keeping the copy in the case–control
study, and dropped the copied cohort. Second, many "healthy controls" were not general-population adults. They included
hospital in-patients, pregnant women and new mothers, people in an antibiotic trial, people referred for colonoscopy,
and metabolic-disease-enriched cohorts. The most extreme FPRs in our first version (up to 0.87) came from one hospital
cohort. Our primary analysis therefore uses a strict set: general-population cohorts, healthy adults, not pregnant or
on antibiotics. This gives 6,525 people in 36 cohorts from 20 countries, nine of them non-westernised. Each classifier
was tested on 32–35 of these populations (6,157–6,466 people). The full de-duplicated set (8,160 people, 55 cohorts,
27 countries) is a sensitivity analysis. We chose the strict set after seeing the first results, and we say so.

## THE FALSE-POSITIVE RATE BELONGS TO THE TEST–POPULATION PAIR

Pooled over people, the FPR in the strict set was close to or below target: 0.06 (CRC), 0.12 (IBD) and 0.13 (T2D) for
LASSO, and 0.05, 0.09 and 0.06 for RF (random-effects estimates; Figure 1, Figure S1). Population by population, it
was not. Between-population heterogeneity was large for every classifier (I² 0.70–0.95; τ on the logit scale
0.55–1.44; P < 10⁻¹⁰). For a new population, the 95% prediction interval of the FPR was 0.01–0.22 for the CRC LASSO
test, 0.02–0.14 for CRC RF, 0.01–0.63 for IBD LASSO, 0.005–0.65 for IBD RF, 0.02–0.54 for T2D LASSO and 0.01–0.34 for
T2D RF. Even with perfect calibration, small cohorts would put 15–16% of populations outside the 0.05–0.15 band by
chance. The observed share was 59–89%, an excess of 44–73 percentage points.

Restricted to populations of at least 100 people, the CRC LASSO test flagged 0.4% to 14% of healthy people. The IBD
LASSO test flagged 3% to 47% and the T2D LASSO test 1% to 61%. Errors ran in both directions. The CRC tests were, on
average, too strict in healthy general populations, which means lost sensitivity there. The IBD and T2D tests
over-flagged heavily in some populations.

Three checks did not explain this away. Scoring with the cross-validation fold models that produced the cut-off,
instead of the refitted model, moved the pooled FPR by at most 0.04 (CRC LASSO: 0.044 versus 0.037). Adjusting for age,
sex, BMI and sequencing depth, as pre-specified, changed the between-population variance by −24% to +28%. Population
identity still accounted for 15–49% of score variance (intraclass correlation). These models could use only the 24–27
populations that recorded all four covariates (of 32–35). Adding Shannon diversity and richness, which we had not
pre-specified, removed 39–50% of between-population variance for the IBD tests but increased it for the others.
Covariates are often significant for individuals, but they do not remove the population effect.

Two pre-specified expectations were only partly met. We expected populations over-flagged by one test to be over-flagged
by the others. The correlation was moderate for CRC and T2D LASSO (Spearman ρ = 0.50, 95% CI 0.11–0.79) and absent
otherwise (ρ = −0.18 to 0.29, all CIs including 0). We expected the CRC test to over-flag non-westernised populations. It
did for LASSO in the strict set (median difference 0.05, one-sided Mann–Whitney P = 0.016), but not for RF (P = 0.71) or
in the full set (P = 0.38). The T2D LASSO test, examined post hoc, over-flagged non-westernised populations strongly
(median difference 0.17, P = 0.0003). No single list of "risky populations" fits all tests.

## WHY: HEALTH MARKERS OF THE TRAINING POPULATION ARE RARER ELSEWHERE

For the LASSO tests, a population's mean score shift relative to training controls can be split into taxon
contributions. This decomposition was pre-specified. The shift tracked the population's FPR closely (Spearman
ρ = 0.76 for CRC, 0.91 for IBD, 0.90 for T2D; Figure 2A). For the IBD test, the five most over-flagged healthy
populations were all Asian: India (0.62 and 0.40), Japan (0.47) and China (0.41 and 0.34). In each, the score rose
because taxa that the model had learned as markers of health in its Western training cohorts were scarcer. These
were *Gemmiger formicilis*, *Asaccharobacter celatus*, *Roseburia* sp. CAG-182 and *Ruminococcus bromii* (Figure 2C).
Oral taxa contributed less than 3% of these shifts. The T2D test over-flagged non-westernised populations in Fiji
(0.61), Cameroon (0.59) and Madagascar (0.52). The drivers were higher Enterobacteriaceae, *Escherichia*,
*Catenibacterium* and *Collinsella massiliensis*, and lower *Anaerostipes hadrus* (Figure 2D). The CRC test's most
over-flagged population (Cameroon, 0.32) had more *Prevotella* sp. CAG-520 and *Veillonella parvula* and less
*Streptococcus salivarius* (Figure 2B). These are descriptive associations, not causes. They suggest that much of the
"false positive" signal is ordinary population-to-population variation in gut composition, read through a model that
saw only a few populations.

## WHAT DID NOT WORK: CORRECTIONS THAT USE OTHER COHORTS

If the error comes from the population, a correction needs information about that population. We tested four
corrections that borrow it from elsewhere.

On development cohorts, three failed (Table S3):

- an adjustment of each person's score for the main axes of healthy microbiome variation (it cut CRC AUROC from 0.76
  to 0.61–0.68);
- a cut-off from a pooled reference of about 4,000 healthy people;
- cut-offs from the one to five populations most similar in composition.

The pre-specified country-matched reference did no better. A cut-off set on the other cohorts of the same country put
only 22–58% of populations in the 0.05–0.15 band. Labelled local controls (n = 100) put 100% there.

Control augmentation [7], added after our literature search, retrains the classifier with extra healthy controls. We
added all development-split healthy cohorts and tested on 29 locked populations (154 population–classifier pairs). The
mean absolute deviation from 0.10 was 0.087 without augmentation and 0.078 with it (Wilcoxon on population means,
P = 0.58). Augmentation helped the IBD tests (0.103 to 0.064–0.067). It harmed the CRC LASSO test (0.073 to 0.081) and the
T2D RF test (0.059 to 0.101). Where it helped most, the augmentation pool contained the same population. Indian healthy
adults in the pool fixed the IBD test for another Indian cohort (FPR 0.62 to 0.03), and this held after we removed
the people the two cohorts shared.

## WHAT WORKED: A BURN-IN AT THE SITE OF USE

A site that adopts a test can measure its own FPR without labels, because almost everyone tested in screening is
healthy. We used a burn-in rule. Score the first N people tested and set the cut-off at the k-th smallest score, with
k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the target FPR and π_max is an upper bound on disease prevalence among those
people. If later people are exchangeable with the burn-in group, the expected FPR is at most α for any prevalence up to
π_max. This follows from split-conformal arguments [13, 14] and from the fact that the flagged share of a mixed group is
at least (1 − π) times its FPR. Conformal outlier detection with contaminated reference data behaves the same way [15].
A stricter variant picks k so that P(FPR > α) ≤ 0.05 [16]. Laboratory medicine sets reference limits from routine,
partly abnormal results in the same way [17, 18]. The rule is an adaptation of known tools, not a new method. Our
question is empirical: does it hold for microbiome tests, and when does it break?

**Random splits check the code, not the world.** Within each locked population we drew 200 random burn-in groups of
N = 100. The mean absolute FPR error fell from 0.063 (training cut-off) to 0.029. This result rests on 38
population–classifier pairs but only seven distinct populations. Resampling whole populations, the reduction was
−0.034 (95% CI −0.065 to −0.013), with six of seven populations improved (Wilcoxon on population means, P = 0.031).
Across the 11 strict-set populations large enough for N = 100, the error fell from 0.085 to 0.033 (11 of 11 improved,
P = 0.001). Under random splits, however, the burn-in and evaluation groups are exchangeable by construction. The share
of burn-ins with FPR above 0.15 then follows a known beta-binomial law whatever the data. In our first version we
called the close fit to that law evidence; it is only a check that the code is right.

**Non-random splits test the assumption.** We therefore drew the burn-in group from a non-random part of each
population and evaluated on the rest (Figure 3B). These designs and their success thresholds were written down
before we ran them. When the burn-in came from the younger or leaner half, or from one sex, and was applied to the
other half, the error still fell by 58% (0.079 to 0.033; seven populations). When the burn-in was the first 100 people
in accession order, it fell by 56% (0.077 to 0.034; 13 populations). The burn-in broke when it came from a different
place. Calibrated in one city or country of a multi-site study and applied in another (MetaCardis: Leipzig, Copenhagen,
Paris; PREDICT: UK, USA), it was worse than doing nothing. The error rose from 0.057 to 0.078, and 37% of burn-ins gave
an FPR above 0.15. This rests on only two studies. Calibrated on a neighbouring cohort in the same country, the burn-in
was no better than the training cut-off (P(FPR > 0.15) 0.30 versus 0.31; P = 0.57, nine populations). Across all
within-site designs, the error fell by 48%. Our pre-stated threshold was 50%, so this hypothesis is not supported as
written, and we report it as such.

A label-free batch correction run on the same 100 people sat between the two. It aligned each feature's mean and SD to
the training controls, in the style of ComBat. It reduced the error relative to the training cut-off by 35–47%, but
remained worse than the burn-in in every locked population (difference −0.012, 95% CI −0.017 to −0.007). Against
control augmentation, the burn-in was better on average (0.029 versus 0.064; difference −0.034, 95% CI −0.076 to
−0.007), but in only four of seven populations (P = 0.22). Our first version reported P = 0.0004 for this comparison;
that test counted repeated populations as independent.

**Patients in the burn-in group.** In the locked case–control cohorts that were large enough for N = 100 (one CRC
cohort and two T2D cohorts), the training cut-off gave a mean FPR of 0.29. With 1–10% patients in the burn-in group, the
rule gave 0.075–0.087, below target as the bound requires (Figure 3C). Sensitivity fell from 0.46 to 0.21–0.23. This is
the price of returning the FPR to its stated value. At 1% prevalence, the positive predictive value rose from 1.6% to
2.6%. Neither test is close to a screening tool on its own; the point is that the stated FPR becomes true.

## WHAT THIS MEANS FOR MICROBIOME DIAGNOSTICS

A gut-microbiome classifier's specificity is not a fixed property that can be printed on a label. In general healthy
populations it varies so much between cohorts that pooled validation hides it. Corrections built from other cohorts do
not reliably fix it, even when those cohorts are from the same country. What fixes it is calibration on the site's own
people. We suggest three changes. First, cross-cohort benchmarks should report the FPR cohort by cohort at a fixed
cut-off, with I² and a prediction interval, next to AUROC; STORMS-style reporting [19] could ask for this. Second, a
site that adopts a published classifier should treat its cut-off as provisional and recalibrate on its own first ~100
tests, and recalibrate again when sample handling or the population served changes. Third, methods that correct
processing bias or augment training controls, such as DEBIAS-M, MMUPHin and control augmentation [7, 20, 21], should
be judged by the FPR they deliver at new sites, not only by AUROC.

Our study has limits. All profiles come from one pipeline (MetaPhlAn3), and other profilers may shift scores
differently. We used two standard classifiers with fixed settings, not the best possible models. We did not run
MMUPHin, ConQuR or DEBIAS-M, which need batch labels with cases or retraining; our batch-correction comparator was a
simple label-free alignment. The strict subset was chosen after seeing the first results. Only two studies had
sub-sites, and only three locked case–control cohorts were large enough for the contaminated burn-in at N = 100. Our
non-random splits used accession order as a stand-in for time, because collection dates were not available. In real
screening, positive results are confirmed later, which would let a site refine its cut-off with labels; we did not
test this. Every way of fixing the cut-off that we tried, including those that failed, is listed in Table S3 and in the
repository's variant ledger.

## CONCLUSION

The false-positive rate of a gut-microbiome disease test depends on where it is used. A short, label-free burn-in at
the site of use restores it. Borrowed references do not.

## METHODS

Full methods, the analysis plans (atlas, cohort split, burn-in evaluation, revision plan v4 with deviations D1–D4),
every hypothesis tried (including those that failed) and the supplementary tables are in the Supporting Information.

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

This study reanalysed public, de-identified data. No new ethics approval was required.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles and metadata are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31; MetaCardis
2022-10-19). Code, analysis plans, per-person scores, the duplicate list and all results: [GitHub repository URL and
Zenodo DOI to be added].

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

**Figure 1. One cut-off gives very different false-positive rates in healthy general populations.** Each point is
one healthy adult population (strict set, at least 20 people) not used to train the classifier, sorted by FPR. The
y-axis is the share flagged by a LASSO classifier whose cut-off targets an FPR of 0.10 (dashed line). Blue band:
0.05–0.15. Orange band: 95% random-effects prediction interval for a new population. Orange diamonds: non-westernised
populations. Bars: exact 95% binomial confidence intervals. Panel titles give the random-effects pooled FPR, I², and
the numbers of populations and people. Random forest: Figure S1.

**Figure 2. Over-flagging follows the population's shift in "health-marker" taxa.** (A) LASSO score shift of each
population relative to training controls (sum of taxon contributions, logit scale) against its FPR; ρ is Spearman's
correlation. (B–D) The eight taxa contributing most to the shift in the most over-flagged population for each test.
Red: taxon more abundant than in training controls, with a positive model weight. Blue: taxon less abundant, with a
negative weight (a "health marker" of the training cohorts).

**Figure 3. Only calibration at the site of use restores the FPR.** (A) Mean absolute deviation of the realised FPR
from 0.10 in the five locked populations large enough for every burn-in size (fixed set), 200 random burn-in groups
each. Grey: training cut-off. Yellow: pooled healthy reference. Brown square: label-free feature alignment on the same
100 people. Purple dotted: control augmentation. Blue: burn-in rule. Green: stricter burn-in rule
(P(FPR > 0.10) ≤ 0.05); at N = 25 it is infeasible and flags nobody. (B) Share of burn-ins (N = 100) giving
FPR > 0.15, by where the burn-in people come from. "Random split": the same population, random halves. "Age/BMI/sex
halves": burn-in from one half of the population and evaluation on the other. "Accession order": the first 100 people
by accession. "Other sub-site": another city or country of the same multi-site study. "Other cohort": another cohort
from the same country. Bars: 95% CI from resampling populations. (C) Locked case–control cohorts with patients mixed
into the burn-in group at prevalence π (π_max = π): FPR (solid) and sensitivity (dashed) of the training cut-off and
the two burn-in rules.
