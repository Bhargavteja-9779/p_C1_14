# Twenty local controls keep gut-microbiome diagnostic thresholds honest at new sites

**Article type:** Short Communication (Letter) — iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary (≈100 words).** Gut-metagenome classifiers are validated by AUROC across cohorts. A deployed
test also needs a fixed decision threshold, but that step is rarely checked. Across 16 held-out cohorts covering four
diseases (19 public cohorts, 3,626 people), a threshold set for 10% false positives on training cohorts gave 0–73% false
positives at new sites. In 69% of cohort–model pairs it was off by more than half its target. Batch correction and
prevalence correction did not fix this. Setting the threshold from 20 labelled local controls kept every cohort within
0.08–0.11. For the external colorectal-cancer cohorts this meant 13–181 fewer unnecessary colonoscopies per
1,000 people screened, at a cost of up to one more missed cancer.

---

To the Editor,

Stool metagenomes can flag colorectal cancer (CRC), inflammatory bowel disease (IBD) and other conditions. Pooled
studies show that microbial signatures carry over between countries [1–4]. These studies judge a classifier by the area
under the ROC curve (AUROC) in held-out cohorts [1, 2, 5]. AUROC summarises ranking over all possible thresholds. A
screening laboratory cannot use all thresholds. It must pick one cut-off, usually to cap the false-positive rate (FPR),
because every false positive in CRC screening becomes a colonoscopy [6, 7]. The threshold is normally chosen on the
training cohorts [1]. Whether it still gives the promised FPR at a new hospital is rarely reported [8, 9]. Clinical
laboratories already face a similar problem with reference intervals. They verify each interval with a small set of
local healthy samples before use [10]. Microbiome diagnostics have no such step.

Here, we measured how far a transferred threshold drifts. We then tested which deployment step restores the target. We used
19 public cohorts from curatedMetagenomicData [11], processed with one profiling pipeline [12]: 11 CRC, 4 IBD,
4 type 2 diabetes (T2D) and 5 adenoma cohorts. We fixed the protocol, the methods and the success criterion before we
looked at any test cohort (Supporting Information). We compared nine threshold-setting methods. Some used no labelled
local data, including batch correction [13, 14] and prevalence correction [15, 16]. Others used a small number of
labelled local controls [17, 18]. The finding is simple: thresholds drift far beyond chance, and about 20 local
controls are needed to fix them.

## TRANSFERRED THRESHOLDS MISS THEIR TARGET FALSE-POSITIVE RATE AT MOST NEW SITES

We trained LASSO logistic regression and random-forest classifiers with fixed settings. For CRC, we trained on eight
development cohorts and tested on three external cohorts that were locked away during method design. For IBD, T2D and
adenoma, we held out each cohort in turn (leave-one-cohort-out). The threshold was the 90th percentile of out-of-fold
scores of training controls. This is the usual way to target 90% specificity [1]. AUROC in held-out cohorts was
0.70–0.86 for CRC, 0.66–0.85 for IBD, 0.58–0.69 for T2D and 0.54–0.65 for adenoma (Table S1).

At the new site, the realised FPR ranged from 0.05 to 0.59 with LASSO and from 0.00 to 0.73 with random forest
(Figure 1, Figure S1). In 22 of 32 cohort–model pairs (69%), the FPR fell outside 0.05–0.15, that is, more than half
the target away. This spread was much larger than sampling noise. A binomial test of over-dispersion across cohorts
was significant in all eight disease–model cells (P from 1 × 10⁻³ to 1 × 10⁻¹⁷⁷; Table S2). All three external CRC
cohorts produced more false positives than promised: 0.11–0.28 with LASSO and 0.13–0.31 with random forest.

The drift ran in both directions. In some cohorts the threshold was too strict (IBD and T2D: FPR 0.05 in Karlsson
2013 and MetaCardis). In others it was far too loose (T2D: 0.59 in Qin 2012; IBD: 0.41 in HMP2). So a single global
correction cannot fix it. A site may also look "conservative" or "sensitive" only because of where its threshold landed.

Three post-hoc checks point to the cause (Table S4). First, AUROC did not predict the error. Cohorts with high AUROC were
no more likely to keep the target FPR (Spearman ρ = −0.18, P = 0.31). Second, the two classifiers erred in the same
direction at the same site (ρ = 0.69 between LASSO and random-forest FPRs, P = 0.003). The drift is therefore a property
of the site, not a quirk of one model. Third, the error tracked how far the scores of healthy controls had moved. The shift
of the median control score between training cohorts and the new site explained most of the ranking of realised FPRs
(ρ = 0.80, P = 3 × 10⁻⁸). In other words, healthy people at a new site look different to the model. Likely reasons
include DNA extraction, sequencing depth, diet, geography and how controls were defined (for example, colonoscopy-negative
volunteers versus population samples). A strong AUROC in a new cohort is thus no evidence that its threshold is safe.

## BATCH CORRECTION AND PREVALENCE CORRECTION DO NOT RESTORE THE OPERATING POINT

A natural objection is that batch correction should remove site effects. We standardised every species within each
cohort, including the new site's own samples, before training and scoring [13, 14]. This is label-free. It narrowed the
spread but did not remove it. (Dedicated tools such as DEBIAS-M [20] remain to be tested in this setting.) Only 28% of cohort–model pairs fell within 0.05–0.15, and the worst cohort reached an FPR
of 0.32 (Figure 2A). The share of single-site splits with FPR above 0.15 dropped only from 0.38 to 0.32 (Figure 2B).

Prevalence correction made things worse. The EM procedure of Saerens et al. [15] re-estimates the share of cases at the new
site and moves the threshold. It assumes that each class's score distribution is the same at every site, and only the
case–control mix changes. Under that assumption, however, the FPR at a fixed threshold cannot change at all. So the
drift we saw means that the scores of controls themselves moved between sites. Applied anyway, EM put cohort-mean FPRs
anywhere between 0 and 1 (Figure 2A).

Two more label-free options also failed. Taking the 90th percentile of all unlabelled samples at the new site treats every
sample as a control [19]. That works only when cases are rare. In these case–control cohorts (about half cases) it
pushed the threshold so high that sensitivity fell to 0.14. A mixture model that we designed to learn a location–scale
shift from unlabelled scores reached the target band in 66% of pairs. It was still unstable when one class dominated
(Figure 2A). We report it as a negative result. Moving the training threshold by the median and spread of 20 local
controls (an "anchor") was also not enough: 40–50% of pairs fell within the band.

## TWENTY LABELLED LOCAL CONTROLS FIX THE THRESHOLD, AT A PREDICTABLE COST

The method that worked is the simplest. The site collects n people confirmed to be free of the disease (for CRC, people
with a normal colonoscopy). It runs the classifier on them and sets the threshold at a fixed rank among their scores:
the ⌈(n + 1)(1 − α)⌉-th smallest score, for target FPR α. This rule comes from split-conformal prediction [17]. It keeps the
expected FPR at or below α without any modelling assumption, as long as the local controls resemble future controls at that site.

With n = 20, every feasible cohort–model pair landed within 0.05–0.15 (20 of 20; cohort means 0.08–0.11; Figure 1,
Figure 2A). With n = 10 the result was similar (28 of 28; 0.08–0.11). The spread of cohort-mean FPR across sites fell
from 0.09 to 0.007 (CRC), 0.30 to 0.005 (T2D) and 0.075 to 0.008 (adenoma). The cohort-bootstrap difference in spread was
−0.16 (95% CI −0.23 to −0.05) for LASSO and −0.22 (−0.32 to −0.06) for random forest. Both pre-stated success criteria
were met (Supporting Information).

The rule has two honest costs. First, it controls the average FPR, not every single deployment. With 20 controls, a
single site still exceeded an FPR of 0.15 in 19% of random calibration sets (Figure 2B). A stricter version picks the rank
so that P(FPR > α) ≤ 0.05 [18]. It cut that risk to 1–2% with 30–50 controls but lowered sensitivity to 0.08–0.11
(Figure 3B). Second, a lower FPR means lower sensitivity when the transferred threshold had been over-calling.
For 1,000 people screened at a CRC prevalence of 0.5%, the three external CRC cohorts had 112–280 unnecessary colonoscopies
and 1.3–2.3 missed cancers under the transferred LASSO threshold. With 20 local controls the figures were about 99
unnecessary colonoscopies and 1.5–3.3 missed cancers (Figure 3A). The rule therefore does not make the test more
accurate. It makes the test do what its label says, so a programme can plan colonoscopy capacity.

What does this mean in practice? Consider a laboratory that buys a validated CRC model and plans to screen a new
population. Before go-live, it profiles stool from 20 people with a recent normal colonoscopy. It scores them with the
frozen model, sorts the scores and uses the 19th of the 20 sorted values (⌈21 × 0.9⌉ = 19), that is the second-highest score, as the cut-off. No retraining and
no access to the original training data is needed. The same 20 profiles can be re-used later to monitor drift: if a
growing share of new confirmed-negative samples score above the cut-off, the threshold needs renewal. This mirrors
how laboratories verify reference intervals with about 20 local samples [10], and it fits within normal validation budgets.

There is also a hard floor. A target FPR of 0.05 needs at least 19 controls for the conformal rule. The 95%-confidence
version needs at least 59. With fewer controls, no valid threshold exists. In our data, a 10-control calibration at
α = 0.05 returned no usable threshold (Table S3).

## CONCLUSION

AUROC-based cross-cohort validation hides a practical failure. The decision threshold of a gut-microbiome classifier
does not travel. We recommend three steps for anyone reporting or deploying such a test:
(i) report the realised FPR and sensitivity at a pre-fixed threshold for each held-out cohort, not only the AUROC;
(ii) before go-live, set the threshold on at least 20 local confirmed controls (≥ 30 for a 95%-confidence guarantee at 90% specificity);
(iii) do not rely on batch or prevalence correction to fix the operating point.
These steps cost little. They need no new algorithm, and they turn a promise on paper ("90% specificity") into one that holds
at the site where the test is used. Journals and reporting guidelines for microbiome diagnostics could ask for step (i) as standard.
Our study has limits. The cohorts are case–control studies, not screening populations. We used two classifier families,
one profiling pipeline and one simple batch-correction baseline. T2D and adenoma classifiers were weak, so absolute sensitivities are low. Only one IBD
cohort had enough controls for the 20-control rule. Prospective checks in screening programmes are the next step. Code
and all per-cohort scores are public.

## METHODS

Full methods, the pre-registered protocol and all supplementary tables are in the Supporting Information.

## AUTHOR CONTRIBUTIONS

[To be completed by the authors.]

## ACKNOWLEDGMENTS

We thank the investigators of the original cohorts and the curatedMetagenomicData team.

## CONFLICT OF INTEREST STATEMENT

[To be completed by the authors.]

## ETHICS STATEMENT

This study re-analysed publicly available, de-identified data. No new samples were collected.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles and metadata are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31, MetaCardis
2022-10-19). Code, the frozen protocol, per-cohort scores and all results: [GitHub repository URL to be added].

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
7. Sung H, Ferlay J, Siegel RL, et al. Global cancer statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries. *CA Cancer J Clin*. 2021;71:209–249. https://doi.org/10.3322/caac.21660
8. Van Calster B, Steyerberg EW, Wynants L, van Smeden M. There is no such thing as a validated prediction model. *BMC Med*. 2023;21:70. https://doi.org/10.1186/s12916-023-02779-w
9. Zhang Y, Cidan Y, Xu J, Li B. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
10. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
11. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
12. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
13. Wang Y, Lê Cao KA. Managing batch effects in microbiome data. *Brief Bioinform*. 2020;21:1954–1970. https://doi.org/10.1093/bib/bbz105
14. Gibbons SM, Duvallet C, Alm EJ. Correcting for batch effects in case-control microbiome studies. *PLoS Comput Biol*. 2018;14:e1006102. https://doi.org/10.1371/journal.pcbi.1006102
15. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. *Neural Comput*. 2002;14:21–41. https://doi.org/10.1162/089976602753284446
16. Godau P, Kalinowski P, Christodoulou E, et al. Navigating prevalence shifts in image analysis algorithm deployment. *Med Image Anal*. 2025;102:103504. https://doi.org/10.1016/j.media.2025.103504
17. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
18. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
19. Roschewitz M, Khara G, Yearsley J, et al. Automatic correction of performance drift under acquisition shift in medical image classification. *Nat Commun*. 2023;14:6608. https://doi.org/10.1038/s41467-023-42396-y
20. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4

## FIGURE LEGENDS

**Figure 1. Transferred decision thresholds miss their target false-positive rate at new sites.** Each row is one
held-out cohort; the classifier is LASSO logistic regression (random forest: Figure S1). The x-axis is the realised
false-positive rate (FPR) among held-out controls. The target is 0.10 (dashed line); the grey band is 0.05–0.15.
Blue circles: threshold from training cohorts (status quo). Orange squares: cohort-wise feature standardisation, then the
training threshold. Green diamonds: threshold from 20 labelled local controls (conformal rule), shown only where the
cohort had at least 40 controls. Values are means over 200 random splits of each cohort's controls into calibration and
evaluation halves. CRC models were trained on eight development cohorts. Other diseases use leave-one-cohort-out.

**Figure 2. Only labelled local controls restore the operating point.** (A) Cohort-mean realised FPR for each method.
Each dot is one cohort × classifier; the black bar is the median. (B) Share of single calibration sets with FPR above
0.15, across all cohorts and splits. (C) Mean sensitivity. Blue: methods using no labelled local data. Green: methods using
n labelled local controls. Target FPR 0.10. Local-control methods are shown only for cohorts with enough controls.

**Figure 3. Consequences for screening and how many local controls are needed.** (A) Unnecessary colonoscopies and missed
cancers per 1,000 people screened at an assumed CRC prevalence of 0.5%. Three external CRC cohorts, LASSO classifier.
Lines join the three methods within a cohort. (B) Share of calibration sets with FPR above 0.15, by number of labelled
local controls, for the conformal rule (expected FPR ≤ 0.10) and the 95%-confidence rule (P(FPR > 0.10) ≤ 0.05). Labels
give mean sensitivity. Each point pools all cohorts with enough controls for that n, so the cohort set differs between points.
