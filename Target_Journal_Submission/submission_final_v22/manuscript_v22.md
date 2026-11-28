# Gut-microbiome disease classifiers set for a 10% false-positive rate miss it in most healthy populations

**Article type:** Letter, iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary.** A gut-microbiome test is published with one cut-off and one false-positive rate (FPR).
We scored 28 disease classifiers, each with a cut-off set for an FPR of 10%, in 36 groups of healthy adults. In 70% of
classifier–population pairs the FPR fell outside 5–15%, against about 15% expected from chance. Two published
gut-health indices, trained largely on the same studies, labelled a median of 64% (GMWI2) and 67% (GMHI) of healthy
people in their own East Asian training studies as non-healthy, against 12% and 21% elsewhere. Within a site,
resetting the cut-off on 100 unlabelled local people cut the FPR error by 62% in retrospective tests.

---

To the Editor,

Stool metagenomes carry signals of colorectal cancer (CRC), inflammatory bowel disease (IBD), type 2 diabetes (T2D) and
many other diseases, and these signals carry over between countries [1–4]. Classifiers are therefore judged by the area
under the ROC curve (AUROC) in held-out cohorts [1, 5, 6]. A test in use, however, needs one cut-off. That cut-off
fixes how many healthy people are flagged, and in CRC screening every false positive leads to a colonoscopy [7].

Clinical epidemiology has long known that a test's specificity depends on the population it is used in (the "spectrum
effect") [8, 9]. Microbiome studies have shown this too. Most directly, the SIAMCAT benchmark set cut-offs for an FPR
of 10% and found that controls from other studies roughly doubled the false positives across many case–control tasks
[10]. Reference ranges also did not transfer between districts of one province [11], predictors trained on
industrialised populations were uninformative elsewhere [12], although without a per-population FPR, and CRC models lost calibration across countries [13]. In medical
imaging, the operating point drifts between sites even when AUROC holds [14]. Cross-cohort benchmarks report AUROC or
transfer of discrimination [13, 15, 16], not the FPR at a fixed cut-off, and an audit in this journal found that most studies do not deposit the metadata needed to re-test them
[17]. Laboratory medicine, by contrast, verifies a reference limit on local healthy people before use [18].

We extend the SIAMCAT observation in four ways. We score healthy adult groups rather than the controls of other
case–control studies; we measure the spread across populations with heterogeneity statistics and prediction intervals;
we ask whether AUROC predicts that spread; and we audit two released gut-health indices and test the cause by
retraining. We also test a local fix. Confirmatory analyses followed time-stamped plans with falsification criteria,
committed to the code repository before they were run ("pre-specified"). Several of these hypotheses failed or were
inconclusive, and Supporting Information S5 lists them all. Analyses that were not pre-specified are marked †.

## THE SAME CUT-OFF GIVES A DIFFERENT FALSE-POSITIVE RATE IN EVERY POPULATION

We trained 28 classifiers (LASSO and random forest, RF, for 14 diseases) on MetaPhlAn3 profiles [21] from 26
case–control cohorts. As in [1], each cut-off was the 90th percentile of out-of-fold control scores, which targets an
FPR of 0.10. We then scored one sample per healthy adult in every population of the curatedMetagenomicData resource [19] not
used in training. Our main ("strict") set has 36 groups with 6,525 people from 20 countries: population cohorts and the
healthy controls of case–control studies, without hospital, pregnancy, trial or colonoscopy-referral groups. Because
this set was defined after first results, we repeated every analysis on all 55 populations (S1, data and populations).

The FPR depended on where the classifier was used (Figure 1A, B). In 70% of classifier–population pairs it fell outside
0.05–0.15 (65% among classifiers with AUROC ≥ 0.65), against about 15% expected from sampling noise if each cut-off
were exactly calibrated, and the spread exceeded sampling noise for every classifier
(I² median 0.94). In populations of at least 100 people it ranged from 0 to 0.77 for LASSO and from 0 to 0.87 for RF.
For a new population, the 95% prediction interval of some classifiers reached 0.81 (Figure 1C). Pooled over
populations, some classifiers looked well calibrated, so a pooled FPR can hide the problem.

A released model is usually refitted on all training data, while its cut-off comes from cross-validation, and this
mismatch adds to the error. When each cross-validation model flagged people at the cut-off and we averaged the flags,
65% of pairs still fell outside 0.05–0.15 and all 28 classifiers kept large heterogeneity, but the most extreme LASSO
values shrank (S2.3, fold-model check)†.

A higher AUROC did not mean a smaller spread (Spearman ρ = −0.06, 95% CI −0.42 to 0.32; Figure 1D). With fold-model
scoring the correlation was even positive (ρ = 0.41)†, so better classifiers were, if anything, less portable. No single factor explained the error
either: the population explained less of the variance than our pre-stated 20% (S2.1, variance decomposition). Here "population" includes each study's sample handling, which
we cannot separate from biology.

## TWO RELEASED GUT-HEALTH INDICES MISLABEL HEALTHY EAST ASIAN COHORTS IN THEIR OWN TRAINING DATA

To test classifiers that others use, we audited the Gut Microbiome Wellness Index 2 (GMWI2) [20], an L1 logistic
regression on 95 taxa trained on 8,069 stool metagenomes. For an index, the FPR is the share of healthy people it
labels non-healthy; by the developers' own scores this is 21% in their healthy training samples.

Within its own training data, GMWI2 labelled 0% to 84% of healthy people as non-healthy, depending on the study
(Figure 2A)†. All eight studies above 50% were from China or Japan. The median was 0.64 across the 13 East Asian
studies and 0.12 across the 31 others (P = 5 × 10⁻⁷).

In 15 healthy populations GMWI2 never saw, 12 fell outside the pre-specified band of 0.10–0.31, against 9% expected by
chance (P = 2 × 10⁻¹²; Figure 2B); eight were below the band and four above it. The four unseen East Asian populations were among the more over-flagged, which is
suggestive only (S2.2, unseen populations)†.

We then audited its predecessor, the Gut Microbiome Health Index (GMHI) [22], under a second pre-specified plan. In the
developers' own data the pattern recurred: a median of 0.67 in eight East Asian studies against 0.21 in 13 others
(P = 0.0007; Figure S2A). GMHI uses a different algorithm and markers, but 83% of its healthy samples are also in
GMWI2's training data, so this is a replication in a second model, not in independent data.

GMHI also shows that a cut-off can depend on the profiling pipeline. Four of its seven health-prevalent species do not
exist under MetaPhlAn3 names, and on the same samples the share flagged rose from 23% to 43% between profiler versions
(Figure S2B)†. For the same reason, the plan's second part (GMHI on newer profiles) failed its reproducibility gate and is not
interpreted; S7 gives the history of that decision, which was taken after seeing results.

## A LIKELY CAUSE: THE GEOGRAPHIC MAKE-UP OF THE TRAINING DATA

Five taxa explained 39% of the net East Asian–other gap in GMWI2 score (Figure 2C)†. Four carry "non-healthy" weights and
are common in healthy East Asian guts. One is *Bacteroides plebeius*, whose Japanese strains acquired
seaweed-degrading enzymes from marine bacteria [23]. The fifth, weighted as "healthy", is nearly absent in East Asian
samples. The pathobiont *Klebsiella* is also among the eight taxa shown, so the gap is not only a story of harmless
commensals.

The training data explain these weights. East Asian samples made up 62% of GMWI2's non-healthy training samples but
only 20% of the healthy ones. A classifier that separates healthy from non-healthy across pooled studies can then
learn region-typical taxa as disease markers. Others have noted such biases [10, 12, 22]; we measure their size for
released indices and test them by retraining. These are properties of the models and their training data, not
evidence that East Asian microbiomes are less healthy. Country also travels with laboratory and sequencing.

We retrained the GMWI2 recipe on 10,986 people in 61 studies, leaving one study out at a time (pre-specified). Pooled
training reproduced the effect (Figure 2D). Giving every country × label group the same total weight cut the East
Asian–other gap from 0.52 to 0.06. This met our pre-stated 50% reduction on the point estimate but not on its confidence interval. The weighting also
shrinks the largest countries, and balancing labels within countries removed less of the gap†, so case mix and country
size cannot be fully separated. Reweighting also cost discrimination; it is a check of the training data, not a
deployment fix (S6, retraining).

## A SITE CAN CHECK AND RESET ITS OWN CUT-OFF

The error in Figure 1 is specific to each classifier–population pair, so it needs local data. Cut-offs borrowed from
other cohorts failed, whether from a large pooled reference, the most similar populations or the same country, and
adding external controls to training did not help (S4, corrections that failed).

A site that tests mostly healthy people can reset the cut-off without labels. It scores its first N tests and takes
the k-th smallest score as the cut-off, k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the target FPR and π_max the
highest expected share of patients among those tested. For example, with N = 100, α = 0.10 and no patients, the cut-off
is the 91st smallest score.

If later healthy people resemble this burn-in group, the expected FPR is at most α by a split-conformal argument
[24, 25]; π_max is a conservative allowance for patients (cf. prior-shift corrections [26]). The realised FPR has an
exact Beta distribution (N = 100, no patients: P(FPR > 0.15) = 0.055; Figure S1A), and a stricter rank bounds
P(FPR > α) [27]. The rule is not new: medical imaging corrects operating points from unlabelled site data [14], and
laboratories set reference limits from routine results [28].

We asked whether it survives a non-random split within a site. In 13 healthy populations of at least 120 people, we set
the cut-off on 100 people from a non-random part of each population (the first 100 in accession order, or the younger
or leaner half) and evaluated it on the rest. The mean absolute FPR error (distance from the 0.10 target) fell from 0.101 to 0.038 (−62%; population-clustered
95% CI 51–70%†). All 28 classifiers and 75% of the individual population splits improved, meeting the pre-specified
criterion (Figure 3A); GMWI2 improved similarly (S2.2). A split within one study keeps the laboratory and protocol fixed, so it is close to the conditions the rule
assumes. Across sites the rule failed: a burn-in from one city or country did no better than the training cut-off
elsewhere (S4). It must therefore be run where the test is used, and repeated when sample handling or the population
served changes.

Resetting the cut-off costs sensitivity, because the test moves along its ROC curve. In three case–control cohorts
where the training cut-off flagged 29% of controls, bringing the FPR to or below the target cut sensitivity from 0.46 to
about 0.25, and a little more when patients are in the burn-in group (Figure 3B; three cohorts, no interval). The rule therefore suits screening, where almost everyone tested is healthy, not tests of
referred patients. Lower sensitivity also means more missed cases, a trade-off each programme must weigh against fewer
needless follow-ups. A site can also check a stated FPR with an exact binomial test on 100 local healthy people
(Figure S1B)†. We release the atlas and these procedures as fprcal, a tested Python tool for research use; it is not a
diagnostic device.

## CONCLUSION

The FPR of a gut-microbiome test is a property of the test, the population and the profiling pipeline together, and in
our data a higher AUROC did not mean a more stable FPR. We suggest three changes. Benchmarks should report the FPR at a fixed
cut-off in each held-out population, with I² and a prediction interval, next to AUROC, as is standard for clinical
prediction models [29, 30] and as STORMS-style reporting [31] could require. Developers should check the geographic
case mix of their training data, score their cut-off with the model they release, and state the profiler version it
assumes. Sites should treat a published cut-off as provisional, verify it on local healthy people and, for screening,
reset it. Processing-bias corrections such as DEBIAS-M and MMUPHin [32, 33] should be judged by the FPR they deliver
at new sites.

Our study has limits. All profiles came from one pipeline (MetaPhlAn3), our classifiers used fixed settings, and seven
had an AUROC below 0.6. We did not run DEBIAS-M, MMUPHin or ConQuR [34], or audit other released indices. The GMHI
audit rests on the developers' own, largely shared data. The strict set and the East Asian comparisons were chosen after
seeing results. All site-level results are retrospective, and the within-site tests used healthy-only groups; a
prospective deployment is needed.

## METHODS

Full methods, analysis plans and deviations, every correction we tried (including those that failed), Supporting
Figures S1–S2 and Tables S1–S27 are in the Supporting Information.

- **Data.** MetaPhlAn3 relative abundances of all clades (kingdom to species) from curatedMetagenomicData, release
  2021-03-31 (MetaCardis 2022-10-19). One sample per person. Samples duplicated across studies were removed (119).
- **Features.** Clades present in more than 5% of training samples. For GMWI2, the presence of its 95 taxa.
- **Classifiers.** LASSO logistic regression (C = 0.1) and random forest (500 trees), scikit-learn 1.9.1, cross-validated
  leave-one-cohort-out (5-fold for single-cohort classifiers). Cut-off: 90th percentile of out-of-fold control scores.
- **Statistics.** DerSimonian–Laird heterogeneity on logit FPR; crossed random effects for the variance decomposition;
  study-clustered bootstrap for the case-mix analysis; Holm correction within each plan. Test sidedness is stated in S2.
- **GMHI.** Re-implemented from the developers' released script (plan v7; S7).

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
29. Riley RD, Ensor J, Snell KIE, et al. External validation of clinical prediction models using big datasets from e-health records or IPD meta-analysis: opportunities and challenges. *BMJ*. 2016;353:i3140. https://doi.org/10.1136/bmj.i3140
30. Debray TPA, Damen JAAG, Snell KIE, et al. A guide to systematic review and meta-analysis of prediction model performance. *BMJ*. 2017;356:i6460. https://doi.org/10.1136/bmj.i6460
31. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
32. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
33. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4
34. Ling W, Lu J, Zhao N, et al. Batch effects removal for microbiome data via conditional quantile regression. *Nat Commun*. 2022;13:5418. https://doi.org/10.1038/s41467-022-33071-9

## FIGURE LEGENDS

**Figure 1. The false-positive rate of 28 gut-microbiome disease classifiers (14 diseases) in 36 healthy populations.** (A) The 36 strict
healthy adult populations (20 countries); circle area, number of people; colour, false-alarm index (mean deviation of
logit FPR from the test mean across the 14 LASSO tests). (B) Realised FPR of each LASSO test (rows, ordered by
between-population τ) in each population (columns, country·first author). The cut-off targets FPR 0.10 (white); blue
below, red above, log scale; FPR = 0 is drawn at the lowest colour. Blank cells: training cohort or fewer than 20 people. Bold labels: populations recorded as
"non-westernised" in the curatedMetagenomicData metadata. (C) Random-effects pooled FPR (dot) and 95% prediction interval
for a new population (line), LASSO (blue) and RF (violet); grey band 0.05–0.15; arrow, interval below 0.001. (D)
Out-of-fold AUROC against between-population τ, 28 classifiers; open symbols, AUROC < 0.6; Spearman ρ 95% CI −0.42 to
0.32.

**Figure 2. A published gut-health index (GMWI2) and why it mislabels healthy East Asian cohorts.** (A) Share of healthy
training samples labelled non-healthy by the published cut-off, per study, from the developers' own scores (44 studies
with ≥ 20 healthy people); orange, East Asian studies; dashed line, training FPR 0.21; bars, exact 95% intervals. (B) The
same for the 15 strict healthy populations GMWI2 never saw (our scoring; QC against the developers' published scores on 704 shared samples, r = 0.99); shaded,
the pre-specified band 0.10–0.31. (C) The
eight taxa contributing most to the East Asian–other score gap (★, the five largest, explain 39%); fitted weight in
parentheses (negative = "non-healthy"); dots, share of healthy people carrying the taxon, by region. (D) A GMWI2-recipe
classifier retrained on curatedMetagenomicData, leave-one-study-out: FPR per healthy study under pooled training and with
every country × label group given equal total weight (gap 0.52 → 0.06; relative reduction 88%, study-clustered 95% CI
41–149%, so the point estimate is uncertain); lines, studies (orange, East Asian); diamonds, regional medians (the gap of 0.06 is computed before rounding),
offset sideways for legibility (other regions 0.19 → 0.22, so part of the gap closes because their FPR rises);
dashed line, training FPR 0.21.

**Figure 3. What a site can do.** (A) Mean absolute deviation of the FPR from 0.10 within a site: training cut-off
(ochre) versus burn-in on 100 people from a non-random part of the same population (blue), for each of 28 classifiers
(rows labelled by test and model).
Each classifier is evaluated in 11–13 populations of the full set with ≥ 120 people × non-random splits (accession
order, age, body-mass index); 646 evaluations in total (Table S5). (B) Sensitivity against FPR at N = 100, averaged over three case–control cohorts (one
CRC, two T2D): training cut-off (ochre; does not depend on the burn-in), expected-FPR burn-in with 1%, 5% or 10% patients
in the burn-in group (blue), and a cut-off set on 100 labelled local controls (grey); dashed line, target FPR. The
burn-in point with no patients lies under the labelled-controls marker. The three cohorts are the held-out
case–control cohorts of the earlier three-disease analysis, fixed before testing (S4), not chosen by their FPR.

**Supporting Figure S1. Statistics of the site rules.** (A) Exact probability that the realised FPR exceeds 0.15 when the cut-off is the k-th smallest
of N burn-in scores (expected-FPR rule, blue; rule bounding P(FPR > 0.10) at 0.05, violet). (B) Probability that an exact
one-sided binomial check on n local healthy people (H₀: FPR ≤ 0.15) flags a classifier–population pair with observed FPR above
0.25 (blue) or 0.15 (green); dashed, largest false-alarm probability among pairs with FPR ≤ 0.15. The curves are
saw-toothed because k and the critical count are integers. Post hoc.

**Supporting Figure S2. Audit of a second published index, GMHI (plan v7).** (A) Share of healthy people labelled
non-healthy (GMHI < 0) in the developers' own data, per study (21 studies with ≥ 20 healthy people; GMHI recomputed with
the developers' script on their profiles); orange, East Asian studies; bars, exact 95% intervals; dashed line, overall
training rate 0.24. (B) The same samples scored from two profiles (post hoc): share flagged with the developers' MetaPhlAn2 profiles
against curatedMetagenomicData MetaPhlAn3 profiles, per study (12 studies with ≥ 20 matched healthy samples).
