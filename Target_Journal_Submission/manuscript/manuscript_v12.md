# Gut-microbiome classifiers flag healthy people at population-specific rates, and pooled training can turn a region's normal microbiome into a disease signal

**Article type:** Letter, iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary.** A gut-microbiome classifier is published with one cut-off and one false-positive rate
(FPR). We measured the FPR of 28 disease classifiers in 6,525 healthy adults from 36 populations they had never seen: the
same cut-off flagged 0% to 77% of healthy people, depending on the population. A published gut-health index did the same
in its own training data: it labelled 64% of healthy people in East Asian studies as non-healthy, against 12% elsewhere.
Taxa common in healthy East Asian guts, such as *Bacteroides plebeius*, carry "disease" weights, because East Asian
samples made up most of the non-healthy training data. Balancing training data by country removed 88% of this gap, and
recalibrating on 100 unlabelled people at the site cut the FPR error by 62–79%.

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
classifier, the Gut Microbiome Wellness Index 2 (GMWI2) [22], in its own training data and in populations it never saw.
This audit led to a mechanism, which we tested by retraining. We also tested two fixes. Each confirmatory analysis
followed a time-stamped internal analysis plan with falsification criteria, committed to the code repository before it
was run ("pre-specified"). We report the hypotheses that failed and label every other analysis as post hoc.

## A FIXED CUT-OFF GIVES A DIFFERENT FALSE-POSITIVE RATE IN EVERY POPULATION

We trained LASSO logistic regression (C = 0.1) and random-forest (RF; 500 trees) classifiers on MetaPhlAn3 species
profiles [13] from 26 case–control cohorts. Each cut-off was the 90th percentile of out-of-fold scores of training
controls, which targets an FPR of 0.10 (Table S1). We scored one sample per healthy adult in every population not used in
training, after removing 119 samples duplicated across cohorts (Pearson r > 0.99). Our primary set excludes hospital,
pregnancy, trial and colonoscopy-referral control groups and antibiotic users. We chose this strict set after seeing the
first results, so the full set (55 populations, 8,160 people) is reported throughout as a check.

The FPR depended on where the classifier was used (Figure 1B). Of 489 LASSO classifier–population pairs, 45% had an FPR
above 0.15, 26% above 0.25 and 24% below 0.05. In populations of at least 100 people, LASSO FPRs ranged from 0 to 0.77.
The spread exceeded sampling noise for all 28 classifiers (I² ≥ 0.5; median 0.94, range 0.64–0.97; full set: 28/28,
median 0.92). Sampling noise alone would put 15–16% of populations outside 0.05–0.15; the observed share was 50–97%. For a
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

Our 28 classifiers are research models. To test a classifier that others use, we audited GMWI2 [22], a published L1
logistic regression on the presence of 95 MetaPhlAn3 taxa, trained on 8,069 stool metagenomes from 54 studies, with a
published cut-off (GMWI2 > 0 = healthy). We extracted its coefficients from the released model and checked them against
the paper's Supplementary Data (95/95 identical). The developers' own scores show that 20.8% of their healthy training
samples fall below the cut-off; we take this as the stated FPR.

Within GMWI2's own training data, the published cut-off labelled 0% to 84% of healthy people as non-healthy, depending
on the study (44 studies with ≥ 20 healthy people; I² = 0.96; Figure 2A). This result uses only the developers' published
scores. All eight studies above 50% were from China or Japan. Across the 13 East Asian studies, the median was 0.64
(range 0.25–0.84; 657 of 1,067 healthy people); across the 31 other studies it was 0.12 (range 0–0.40; Mann–Whitney
P = 5 × 10⁻⁷; post hoc). Healthy people in rural Africa were almost never mislabelled (0–7%).

In healthy populations that GMWI2 never saw, the pattern held (pre-specified). Our implementation reproduced the
published scores (r = 0.991, same call for 98.4% of 704 shared samples). In 15 unseen strict populations (1,914 people),
the FPR ranged from 0 to 0.54 (I² = 0.92; 95% prediction interval 0.02–0.68), and 80% of populations fell outside 0.10–0.31,
against 9% expected from sampling noise (exact P = 6 × 10⁻¹³; Figure 2B). Populations that had been in GMWI2's training
data were not better calibrated than unseen ones (mean 0.26 vs 0.20; P = 0.72), so this was not an overfitting artefact.
The four unseen East Asian populations had FPRs of 0.25–0.54 (median 0.38 vs 0.20 elsewhere; P = 0.065), consistent with
the training-data result but too few for a separate test.

## WHY: POOLED TRAINING TURNS A REGION'S NORMAL MICROBIOME INTO A DISEASE SIGNAL

Which taxa drive the gap? We split the difference in mean GMWI2 score between East Asian and other healthy populations
into taxon contributions (post hoc). The largest came from taxa with "non-healthy" weights that are common in healthy East
Asian guts (Figure 2C): *Bacteroides plebeius* (present in 72% of East Asian healthy people vs 18% elsewhere),
*Bacteroides coprocola* (45% vs 11%), *Bacteroides stercoris* (79% vs 41%) and *Lachnoclostridium* (68% vs 45%).
*B. plebeius* is a well-known marker of diet and geography: Japanese strains acquired seaweed-degrading enzymes from
marine bacteria [23].

The training data explain the weights. In GMWI2's training set, East Asian samples made up 62% of the non-healthy samples
(1,574 of 2,522) but only 20% of the healthy ones (1,097 of 5,547; odds ratio 6.7). A model asked to separate healthy from
non-healthy across pooled studies can therefore learn region-typical commensals as disease markers. We call this
geographic case-mix confounding.

We tested this mechanism by retraining (pre-specified). We trained a classifier with the GMWI2 recipe from scratch on
10,986 people in 61 curatedMetagenomicData studies, holding out one study at a time. Trained on pooled data, it reproduced
the effect: healthy people in East Asian studies were labelled non-healthy at a median of 0.71, against 0.19 elsewhere
(gap 0.52; 9 vs 43 studies; Figure 2D). Weighting training samples so that, within each country, healthy and non-healthy
people carried equal weight cut the gap to 0.06, an 88% reduction (study-clustered 95% CI 54–121%), and lowered
between-study heterogeneity (τ 1.16 to 0.81). It cost discrimination: pooled AUROC fell from 0.715 to 0.676 (−0.040; CI
−0.12 to 0.02), beyond our pre-stated margin of 0.03, so that hypothesis failed. Part of the pooled AUROC came from the
geographic shortcut itself. Within studies, where cases and controls share a geography, AUROC fell only from 0.669 to
0.649 (−0.020; CI −0.052 to 0.013; post hoc).

## A SITE CAN VERIFY AND RECALIBRATE ITS OWN CUT-OFF

Balancing addresses one cause at training time; it does not remove the classifier–population error of Figure 1. For that,
the site needs its own data. In a first-stage analysis of the CRC, IBD and T2D classifiers (Supporting Information S4),
cut-offs set on other cohorts failed: a pooled reference of about 4,000 healthy people, references from the most similar
populations, and other cohorts from the same country. Adding external controls to training [8] did not reduce the mean
FPR error (0.087 to 0.078; P = 0.58).

A site that tests mostly healthy people can recalibrate without labels. It scores its first N tests and takes the k-th
smallest score as the cut-off, with k = ⌈(N + 1)(1 − α(1 − π_max))⌉, where α is the target FPR and π_max an upper bound on
disease prevalence. If later healthy people are exchangeable with this burn-in group, the expected FPR is at most α (a
split-conformal argument [14, 15]), and the realised FPR follows an exact Beta law: with N = 100 and α = 0.10, the
probability that the FPR exceeds 0.15 is 0.055 (Figure 3A). A stricter rank bounds P(FPR > α) at 0.05 [16]. The rule is
not new; laboratory medicine sets reference limits from routine results in a similar way [17]. What we tested is whether
it survives a non-random split within a site and whether it fails across sites.

Within a site, it worked. We set the cut-off on 100 people from a non-random part of each large population (the first 100
in accession order, or the younger, leaner or one-sex half) and evaluated it on the rest. Across 13 populations and 28
classifiers, the mean absolute FPR error fell from 0.101 to 0.038, a 62% reduction (population-clustered 95% CI 51–70%;
better in 13/13 populations and 28/28 classifiers; Figure 3B; pre-specified). For GMWI2, with its stated FPR as target, the
error fell from 0.