# Gut-microbiome disease tests miss their stated false-positive rate in many healthy populations and should be recalibrated at the site of use

**Article type:** Short Communication (Letter), iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary (about 100 words).** We applied colorectal cancer (CRC), inflammatory bowel disease (IBD)
and type 2 diabetes (T2D) classifiers to 6,525 healthy adults from 36 cohorts in 20 countries that the classifiers had
never seen. A cut-off meant to flag 10% of healthy people flagged 0% to 62% (LASSO), depending on the cohort; between
cohorts, I² was 70–95%. The scores of over-flagged populations were shifted by a few taxa, often "health markers"
learned from Western training cohorts. Cut-offs borrowed from other cohorts, including cohorts from the same country,
did not restore the target. Recalibrating on about 100 unlabelled people from the same site brought the average FPR
close to target, but did not remove the risk of a high FPR at an individual site, and it cost sensitivity.

**Highlights.**
- Across 32–35 healthy populations per test, a LASSO cut-off set for a 10% false-positive rate (FPR) had a 95%
  prediction interval of 1–22% (CRC) to 1–63% (IBD).
- In LASSO decompositions, a few taxa carried each population's score shift; the five populations most over-flagged
  by the IBD test were Asian, and non-westernised populations were over-flagged by the T2D LASSO test.
- Cut-offs from other cohorts, including same-country cohorts, did not restore the FPR. Control augmentation gave
  no overall gain; it helped the IBD tests, most when the same population was in the pool.
- A label-free burn-in of 100 people from the same site halved the average FPR error when burn-in and later people
  differed in age, BMI, sex or sampling order (post hoc grouping), but not the risk of an FPR above 0.15. It failed
  across sites, and it roughly halved sensitivity.

---

To the Editor,

Stool metagenomes can flag colorectal cancer (CRC), inflammatory bowel disease (IBD) and type 2 diabetes (T2D), and
pooled studies show that microbial signatures carry over between countries [1–4]. Most studies judge classifiers by the
area under the ROC curve (AUROC) in held-out cohorts [1, 2, 5]. A test in use, however, needs one cut-off, usually fixed
to cap the false-positive rate (FPR): in CRC screening, each false positive leads to a colonoscopy [6]. With a cut-off set at
10% FPR on training controls, pooled held-out controls gave an FPR of 0.097 (Source Data for Fig. 3c of [1]), but
controls of other studies gave more than twice the intended false positives; adding external controls to training
("control augmentation") removed most of the excess [7]. More recent work reports that CRC classifiers lose calibration and conformal coverage across countries [8], and
that disease predictors trained on industrialised populations lose accuracy in less industrialised ones [9]. A
commercial dysbiosis index was judged transferable across six countries [10], and gut-health indices apply one
cut-off across many cohorts [11, 12]. That test performance varies between
settings is long known for conventional diagnostics [13]. Clinical laboratories therefore verify reference intervals on
local healthy people [14], and prediction-model research recommends updating models in each new setting [15, 16].
Label-free ways to re-set operating points have also been proposed for medical imaging [17] and for Neyman–Pearson
classifiers [18].

What has not been shown for microbiome tests is how far the FPR at a fixed cut-off moves between general healthy
populations, cohort by cohort and with proper heterogeneity statistics. Nor has it been shown which taxa move it, or
whether corrections built from other cohorts work as well as calibration on the site's own people. We measured all
three in every eligible healthy adult cohort in curatedMetagenomicData [19]. We wrote analysis plans with falsification
criteria before each analysis. These are internal, time-stamped plans in the code repository, not external
pre-registrations. We report the hypotheses that failed as well as those that held (revision history: Supporting Information S3).

## DATA AND DESIGN

We trained LASSO logistic regression and random-forest (RF) classifiers with fixed settings on 10 CRC, 4 IBD and 4 T2D
case–control cohorts (MetaPhlAn3 species profiles [20]). The cut-off was the 90th percentile of leave-one-cohort-out
scores of training controls, which targets an FPR of 0.10 [1]. We then scored healthy adults, one sample per person,
from every cohort not used to train that classifier. A profile-level search (Pearson r > 0.99 between log profiles)
found 119 samples duplicated across cohorts. We removed them, keeping the copy in the case–control study (Table S7).
A post hoc check at r > 0.95 removed 8 more samples and changed no result reported here (Table S13).

Our primary set is strict: healthy adults, not pregnant or on antibiotics, from cohorts whose controls were not
hospital patients, mothers in pregnancy studies, trial participants, colonoscopy referrals or disease-enriched groups
(Table S1). This gives 6,525 people in 36 cohorts from 20 countries, nine of them non-westernised. Some of these cohorts
are the healthy control arms of case–control studies (Table S1). Each classifier was tested on 32–35 populations
(6,157–6,466 people). The full de-duplicated set (8,160 people, 55 cohorts, 27 countries) is a sensitivity analysis.
We chose the strict set after seeing the first results, and we say so.

## THE FALSE-POSITIVE RATE BELONGS TO THE TEST–POPULATION PAIR

Random-effects pooled FPRs in the strict set were 0.06 (CRC), 0.12 (IBD) and 0.13 (T2D) for LASSO, and 0.05, 0.09 and
0.06 for RF (Figure 1, Figure S1). Population by population, the FPR varied far more than sampling noise allows
(I² 70–95%; τ on the logit scale 0.55–1.44; Cochran's Q, P < 10⁻⁹ for every classifier). For a new population, the 95%
prediction interval of the FPR was:

| Test | LASSO | RF |
|---|---|---|
| CRC | 0.01–0.22 | 0.02–0.14 |
| IBD | 0.01–0.63 | 0.005–0.65 |
| T2D | 0.02–0.54 | 0.01–0.34 |

Even with perfect calibration, small cohorts would put 15–16% of populations outside the 0.05–0.15 band by chance; the
observed share was 59–89% (Table S2). Restricted to populations of at least 100 people, the CRC LASSO test flagged 0.4%
to 14% of healthy people, the IBD LASSO test 3% to 47% and the T2D LASSO test 1% to 61%. Errors ran in both directions.
In healthy general populations the CRC tests were, on average, too strict, which costs sensitivity. The IBD and T2D
tests over-flagged heavily in some populations.

Three checks did not explain this away.
- Scoring with the cross-validation fold models that produced the cut-off, instead of the refitted model, moved the
  pooled FPR by at most 0.04. One population moved by up to 0.14, but heterogeneity was unchanged (Table S2).
- Adjusting for age, sex, BMI and sequencing depth, as pre-specified, changed the between-population variance by −24%
  to +28%. Population identity still accounted for 15–49% of score variance (intraclass correlation; 24–27 populations
  with complete covariates). Host variables matter for individuals [21], but they did not remove the population effect.
- Adding diversity and richness, which was not pre-specified, removed 39–50% of the between-population variance for
  the IBD tests and increased it for the others (Table S5).

Two pre-specified expectations held only in part (Table S9). Populations over-flagged by the CRC LASSO test were also
over-flagged by the T2D LASSO test (Spearman ρ = 0.50, 95% CI 0.11–0.79), but the other correlations were weak
(ρ = −0.18 to 0.29). The CRC test over-flagged non-westernised populations for LASSO in the strict set (median
difference 0.05, one-sided Mann–Whitney P = 0.016), but not for RF (P = 0.71) or in the full set (P = 0.38). The T2D
LASSO test, examined post hoc, over-flagged non-westernised populations strongly (median difference 0.17, P = 0.0003; RF: no difference, P = 0.37).

## WHICH TAXA SHIFT THE SCORES

For the LASSO tests, the shift in a population's mean score relative to training controls can be split into taxon
contributions; this decomposition was pre-specified. The shift tracked the population's FPR closely (Spearman ρ = 0.76
for CRC, 0.91 for IBD and 0.90 for T2D; Figure 2A). This is partly built in; the informative part is which taxa drive
the shift.

For the IBD test, the five most over-flagged healthy populations were all Asian: India (0.62, n = 29; and 0.40), Japan
(0.47) and China (0.41 and 0.34). The training cohorts came from the USA, UK, Spain and Denmark. Scores rose because taxa that the
model had learned as markers of health were scarcer: *Gemmiger formicilis*, *Asaccharobacter celatus*, *Roseburia* sp.
CAG-182 and *Ruminococcus bromii* (Figure 2C). Lower *Ruminococcus torques* also contributed; this is a fitted weight,
not a biological claim. Oral taxa contributed less than 3% of these shifts.

The T2D test over-flagged non-westernised populations in Fiji (0.61), Cameroon (0.59) and Madagascar (0.52). These had
more Enterobacteriaceae, *Escherichia*, *Catenibacterium* and *Collinsella massiliensis*, and less *Anaerostipes hadrus*
(Figure 2D). The CRC test's most over-flagged population (Cameroon, 0.32) had more *Prevotella* sp. CAG-520 and
*Veillonella parvula* and less *Streptococcus salivarius* (Figure 2B).

These are descriptive associations, not causes. They agree with the finding that industrialisation reshapes the gut
microbiome and that predictors trained on industrialised populations transfer poorly [9]; we add the size of the
effect on the FPR of specific disease tests, population by population, and the taxa that carry it.

## WHAT DID NOT WORK: CUT-OFFS FROM OTHER COHORTS

If the error comes from the population, a correction needs information about that population. On development cohorts,
three corrections built from other data failed (Tables S3 and S4):
- a person-level adjustment for the main axes of healthy variation, which also cut CRC AUROC from 0.76 to 0.61–0.68;
- a pooled reference of about 4,000 healthy people;
- references from the most similar populations.

These ran before de-duplication and were not repeated.

The pre-specified country-matched reference also failed. We compared it on the same eight large populations, scoring
each of the 200 draws of the local reference rather than their average. A cut-off from the other cohorts of the same
country put 46% of population–test pairs in the 0.05–0.15 band; 100 labelled local controls, evaluated on random
splits of the same population as a benchmark, put 79% there (post hoc; better in all 8 populations, P = 0.0078;
Table S12).

Control augmentation [7] behaved differently here than in its original report. We added all development-split healthy
cohorts to training and tested on 29 locked populations (154 population–classifier pairs). The mean absolute deviation
from 0.10 was 0.087 without augmentation and 0.078 with it (Wilcoxon on population means, P = 0.58; Table S6).
Augmentation helped the IBD tests (0.103 to 0.064–0.067). It harmed the CRC LASSO test (0.073 to 0.081) and the T2D RF
test (0.059 to 0.101). Its largest gain came when the pool held the same population: Indian healthy adults in the pool
repaired the IBD test for another Indian cohort (FPR 0.62 to 0.03), even after we removed the people the two cohorts
shared at r > 0.99 or r > 0.95. Augmentation was evaluated on the full set of locked populations. Wirbel et al. found that the benefit did not depend strongly on which controls were added [7]. We cannot tell
from our data why the two results differ. In our data, though, the benefit depended on whether the pool contained the
same population.

## WHAT WORKED: A BURN-IN AT THE SITE OF USE

A site can measure its own FPR without labels when almost everyone tested is healthy. We used a burn-in rule:
1. score the first N people tested;
2. set the cut-off at the k-th smallest score, with k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the target FPR and
   π_max an upper bound on disease prevalence among those people.

For example, with N = 100, α = 0.10 and π_max = 0.01, k = 92: the cut-off is the 92nd-lowest of the 100 burn-in
scores.

If later people are exchangeable with the burn-in group, the expected FPR is at most α for any prevalence up to π_max.
This follows from split-conformal arguments [22, 23] and from contaminated-reference conformal testing [24]. A stricter
variant bounds P(FPR > α) at 0.05 [25]. Unlike probability recalibration across countries [8], the rule targets the FPR
at one cut-off. Laboratory medicine sets reference limits from routine, partly abnormal results
in the same way [26, 27], and label-free operating-point correction has been shown for imaging [17]. The rule is not
new. Our question is empirical: for microbiome tests, does local calibration beat borrowed references, and when does
it break?

**Random splits check the implementation.** Within each population we drew 200 random burn-in groups of N = 100.
The burn-in's own error under random splits depends only on N and on the size of the evaluation group, not on the data.
The comparison with the training cut-off therefore shows how miscalibrated the training cut-off is, not that the burn-in
is robust. Mean absolute FPR error was 0.063 with the training cut-off and 0.029 with the burn-in in the seven locked
populations, and 0.085 versus 0.033 in the 11 strict-set populations large enough for N = 100 (Table S4; Figure 3A shows the fixed five-population subset).

**Non-random splits test the assumption.** We drew the burn-in group from a non-random part of each population and
evaluated on the rest (Figure 3B). These designs and their success thresholds were written down before we ran them.
Within a site, the burn-in reduced the average error but not all of the risk:
- from the younger or leaner half, or from one sex, applied to the other half, the mean absolute error fell from
  0.079 to 0.033 (seven populations). The mean FPR was slightly above target (0.106, 95% CI 0.101–0.112), and the
  share of burn-ins with FPR above 0.15 was 0.135, the same as with the training cut-off;
- with the first 100 people in accession order, used here as a stand-in for time, the error fell from 0.077 to 0.034
  and the share above 0.15 from 0.167 to 0.111 (13 populations).

Across both designs, the error fell by 57% (post hoc grouping; 12 of 13 populations improved, P = 0.0007; Table S12),
and the share above 0.15 went from 0.146 to 0.126. Much of the gain in average error comes from removing the training
cut-off's bias in either direction; the burn-in does not remove the sampling risk of a high FPR at a single site.

Across sites, the burn-in broke:
- Calibrated in one city or country of a multi-site study and applied in another (MetaCardis: Leipzig, Copenhagen,
  Paris; PREDICT: UK, USA), it was worse than the training cut-off. The error rose from 0.057 to 0.078, and 37% of
  burn-ins gave an FPR above 0.15. This rests on two studies (five sub-sites).
- Calibrated on a neighbouring cohort in the same country, it was no better than the training cut-off
  (P(FPR > 0.15) 0.30 versus 0.31; P = 0.57; nine populations).

Our pre-stated hypothesis had pooled the sub-site transfers with the within-site designs and required a 50% reduction.
The pooled reduction was 48%, so that hypothesis is not supported as written.

**Other label-free corrections.** A feature alignment run on the same 100 people sat between the two (Figure 3A). It
mapped each feature's mean and SD onto the training controls, in the style of ComBat. It reduced the error relative to
the training cut-off by 35–47%, but was worse than the burn-in in all seven locked populations (difference −0.012,
95% CI −0.017 to −0.007). DEBIAS-M [28] can also learn its correction from unlabelled samples of a new batch, so it
could use the same 100 people. We could not run it in our environment; it remains an untested competitor. Against
control augmentation, the burn-in was better on average (0.029 versus 0.064; difference −0.034, 95% CI −0.076 to
−0.007), but in only four of seven populations (P = 0.22), and the two were scored on different subsets of people.

**Patients in the burn-in group.** In the locked case–control cohorts large enough for N = 100 (one CRC and two T2D
cohorts), the training cut-off gave a mean FPR of 0.29. With 1–10% patients in the burn-in group, the rule gave
0.075–0.087, below target as the bound requires (Figure 3C). With π_max set to 0.01 when the true share was 0.05, it
gave 0.082. Sensitivity fell from 0.46 to 0.21–0.23, and to 0.13–0.15 with the strict variant. This is the cost of making the stated FPR true. At 1% prevalence,
the positive predictive value, pooled over these three cohorts, rose from 1.6% to 2.6%; sensitivity from diagnosed
patients makes both figures optimistic. Neither classifier is a usable screening test on its own.

## WHERE THIS APPLIES

The burn-in needs a stream of mostly healthy people and an upper bound on prevalence. This fits population screening,
for example CRC screening, where prevalence is below 1%. It does not fit tests used on symptomatic or referred patients,
as IBD and T2D tests mostly would be. There, a site needs labelled local controls or outcome-confirmed recalibration,
in the spirit of clinical model updating [15]. The burn-in must come from the site that will use the test, and be
repeated when sample handling, sequencing or the population served changes.

## IMPLICATIONS AND LIMITATIONS

A microbiome classifier's specificity is not a fixed property, and it should not be printed on a label without local
verification. We suggest three changes.
First, cross-cohort benchmarks should report the FPR at a fixed cut-off cohort by cohort, with I² and a prediction
interval, next to AUROC; STORMS-style reporting [29] could ask for this. Second, a site adopting a published classifier
should treat its cut-off as provisional and check it on its own people. Third, methods that correct processing bias or
augment training controls, such as DEBIAS-M, MMUPHin and control augmentation [7, 28, 30], should be judged by the FPR
they deliver at new sites.

Our study has limits.
- All profiles come from one pipeline (MetaPhlAn3), and we used two standard classifiers with fixed settings.
- We did not run DEBIAS-M, MMUPHin or ConQuR [31].
- The strict set was chosen after seeing the first results.
- Only two studies had sub-sites, and only three locked case–control cohorts were large enough for the contaminated
  burn-in at N = 100.
- Accession order stands in for time.
- Cohorts differ in collection and DNA extraction protocols, so "population" here includes site processing; we
  cannot separate the two.
- The strict set excludes the referred or symptomatic controls that a real IBD or T2D test would meet.
- The burn-in-versus-augmentation contrast uses seven populations, and Figure 3A shows the five large enough for
  every N (where augmentation's mean error is 0.077).
- Populations are treated as independent; related sub-studies (TettAJ_2019_a–c) are outside the strict set.

We applied Holm correction across all 34 population-level P values we computed, reported or not (Table S10). The
within-site burn-in (adjusted P = 0.022), the strict-set random-split comparison (0.026; this shows the training
cut-off's miscalibration) and the post hoc T2D non-westernised difference (0.010) survive. The seven-population locked
comparisons, the local-versus-country comparison and the CRC non-westernised difference do not.

## CONCLUSION

The false-positive rate of a gut-microbiome disease test depends on where the test is used. In the cohorts we could
test, a short, label-free burn-in from the same site brought its average close to target; references borrowed from
other cohorts did not. Neither removes the risk of a high FPR at a given site, which is why sites should monitor it.

## METHODS

Full methods, the analysis plans and deviations, the revision history and every correction we tried, including those
that failed, are in the Supporting Information (S1–S5). Tables S1–S13 are generated directly from the result files.

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

This study reanalysed public, de-identified data. The original studies obtained ethics approval and informed consent
as described in their publications. curatedMetagenomicData distributes these processed profiles for reuse. No new ethics
approval was required.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31; MetaCardis 2022-10-19). The
exact metadata file used, code, analysis plans, per-person scores, the duplicate list and all results are in the code
repository: [GitHub repository URL and Zenodo DOI to be added]. Original sequencing data are available
from the accessions given in each cohort's publication (cohorts listed in Table S1).

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
7. Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
8. Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
9. Poyet M, Rühlemann M, Schaan AP, et al. Industrialization drives convergent microbiome and host physiological shifts in the human metaorganism. *Cell*. 2026. https://doi.org/10.1016/j.cell.2026.10.016
10. Hiseni P, Furu K, Wang Pedersen V, et al. Towards standardized gut microbiota diagnostics: normobiosis beyond geographical borders. *Gut Microbes*. 2026;18:2701485. https://doi.org/10.1080/19490976.2026.2701485
11. Gupta VK, Kim M, Bakshi U, et al. A predictive index for health status using species-level gut microbiome profiling. *Nat Commun*. 2020;11:4635. https://doi.org/10.1038/s41467-020-18476-8
12. Chang D, Gupta VK, Hur B, et al. Gut Microbiome Wellness Index 2 enhances health status prediction from gut microbiome taxonomic profiles. *Nat Commun*. 2024;15:7447. https://doi.org/10.1038/s41467-024-51651-9
13. Leeflang MMG, Rutjes AWS, Reitsma JB, Hooft L, Bossuyt PMM. Variation of a test's sensitivity and specificity with disease prevalence. *CMAJ*. 2013;185:E537–E544. https://doi.org/10.1503/cmaj.121286
14. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
15. Janssen KJM, Moons KGM, Kalkman CJ, Grobbee DE, Vergouwe Y. Updating methods improved the performance of a clinical prediction model in new patients. *J Clin Epidemiol*. 2008;61:76–86. https://doi.org/10.1016/j.jclinepi.2007.04.018
16. Van Calster B, Steyerberg EW, Wynants L, van Smeden M. There is no such thing as a validated prediction model. *BMC Med*. 2023;21:70. https://doi.org/10.1186/s12916-023-02779-w
17. Roschewitz M, Khara G, Yearsley J, et al. Automatic correction of performance drift under acquisition shift in medical image classification. *Nat Commun*. 2023;14:6608. https://doi.org/10.1038/s41467-023-42396-y
18. Qiu J, Zhao Y, Zheng Y. Shift-adjusted Neyman–Pearson classifiers via single index modeling (SACSIM). *Biometrics*. 2026;82:ujag138. https://doi.org/10.1093/biomtc/ujag138
19. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
20. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
21. Vujkovic-Cvijin I, Sklar J, Jiang L, Natarajan L, Knight R, Belkaid Y. Host variables confound gut microbiota studies of human disease. *Nature*. 2020;587:448–454. https://doi.org/10.1038/s41586-020-2881-9
22. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
23. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
24. Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. *arXiv*. 2025. arXiv:2502.04807
25. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
26. Zierk J, Arzideh F, Kapsner LA, Prokosch HU, Metzler M, Rauh M. Reference interval estimation from mixed distributions using truncation points and the Kolmogorov–Smirnov distance (kosmic). *Sci Rep*. 2020;10:1704. https://doi.org/10.1038/s41598-020-58749-2
27. Ammer T, Schützenmeister A, Prokosch HU, Rauh M, Rank CM, Zierk J. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep*. 2021;11:16023. https://doi.org/10.1038/s41598-021-95301-2
28. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
29. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
30. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4
31. Ling W, Lu J, Zhao N, et al. Batch effects removal for microbiome data via conditional quantile regression. *Nat Commun*. 2022;13:5418. https://doi.org/10.1038/s41467-022-33071-9

## FIGURE LEGENDS

**Figure 1. One cut-off gives very different false-positive rates in healthy populations.** Each point is one healthy
adult population (strict set, at least 20 people) not used to train the classifier, sorted by FPR. The y-axis is the
share flagged by a LASSO classifier whose cut-off targets an FPR of 0.10 (dashed line). Blue band: 0.05–0.15. Grey
band: 95% random-effects prediction interval for a new population. Orange diamonds: non-westernised populations. Bars:
exact 95% binomial confidence intervals. Panel titles give the random-effects pooled FPR, I², and the numbers of
populations and people. Random forest: Figure S1.

**Figure 2. Over-flagging follows shifts in a few taxa.** (A) LASSO score shift of each
population relative to training controls (sum of taxon contributions, logit scale) against its FPR; ρ is Spearman's
correlation. (B–D) The eight taxa contributing most to the score shift in the most over-flagged population for each
test. All bars raise the score. The same taxon can carry opposite weights in different
models (for example *Ruminococcus torques* in B and C). Red: the taxon is more abundant than in training controls and has a positive weight.
Blue: it is less abundant and has a negative weight, that is, a "health marker" of the training cohorts.

**Figure 3. Only calibration at the site of use restores the FPR.** (A) Mean absolute deviation of the realised FPR
from 0.10 in the five locked populations large enough for every burn-in size (fixed set), 200 random burn-in groups
each. Methods: training cut-off; pooled reference of other healthy populations; feature alignment on the same 100
people; control augmentation; burn-in; strict burn-in (P(FPR > 0.10) ≤ 0.05; infeasible at N = 25, where it flags
nobody). Under random splits, the burn-in curves depend only on N. (B) Share of burn-ins (N = 100) giving FPR > 0.15,
by where the burn-in people came from:
- Random split: random halves of the same population.
- Age/BMI/sex halves: burn-in from one half of the population, evaluation on the other.
- Accession order: burn-in from the first 100 people.
- Other sub-site: another city or country of the same study.
- Other cohort: another cohort from the same country.

The number of populations is given under each pair of bars; error bars are 95% CIs from resampling populations.
(C) Locked case–control cohorts with patients mixed into the burn-in group: FPR (solid) and sensitivity (dashed) of the
training cut-off and the two burn-in rules (π_max equal to the true share).
