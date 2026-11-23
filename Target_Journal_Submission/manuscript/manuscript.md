# Gut-microbiome diagnostic thresholds do not transfer between sites, and AUROC does not warn

**Article type:** Short Communication (Letter) — iMeta

**Authors:** [to be completed by the authors]

**Graphical-abstract summary (≈100 words).** Gut-metagenome classifiers are validated by AUROC across cohorts, but a
deployed test needs one fixed decision threshold. We tested whether thresholds transfer, using 16 held-out cohorts from
four diseases (19 public cohorts, 3,626 people). A threshold set for 10% false positives on training cohorts gave 0–73%
false positives at new sites, and AUROC did not predict the error. Batch correction, prevalence correction and controls
borrowed from a neighbouring site did not fix it. Calibrating on controls from the deployment site itself did, on
average. But a single site needs about 100 local controls, not 20, for a dependable threshold.

---

To the Editor,

Stool metagenomes can flag colorectal cancer (CRC), inflammatory bowel disease (IBD) and other conditions, and pooled
studies show that microbial signatures carry over between countries [1–4]. These studies judge a classifier mainly by the
area under the ROC curve (AUROC) in held-out cohorts [1, 2, 5]. AUROC summarises ranking over all possible thresholds.
A laboratory cannot use all thresholds. It must fix one cut-off, usually to cap the false-positive rate (FPR), because in
CRC screening a positive result leads to colonoscopy and the cut-off sets the colonoscopy workload [6]. In medical imaging,
performance at a fixed threshold can drift between sites while AUROC stays intact [7], and prediction models in general
need checking in each new setting [8]. Wirbel et al. set a cut-off at 10% FPR on training controls and reported the FPR
pooled over held-out studies [1]. Recent benchmarks use a fixed probability cut-off of 0.5 [9]. To our knowledge, the
realised FPR of a transferred threshold is rarely reported cohort by cohort, and reporting guidance for microbiome
studies does not ask for it [10]. Clinical laboratories handle a related problem by verifying transferred reference
intervals on a small set of local healthy samples [11].

Here, we asked three questions. Does a transferred threshold keep its promised FPR at a new site? Does anything short of
local data fix it? And how much local data is enough? We used 19 cohorts from curatedMetagenomicData [12], all profiled
with MetaPhlAn3 [13]: 11 CRC, 4 IBD, 4 type 2 diabetes (T2D) and 5 adenoma cohorts. We fixed the protocol, methods and
success criteria before looking at any test cohort, and we label every later analysis as post hoc (Supporting Information).

## A THRESHOLD SET ON TRAINING COHORTS MISSES ITS TARGET AT MOST NEW SITES

We trained LASSO logistic regression and random-forest classifiers with fixed settings. For CRC, we trained on eight
development cohorts and tested on three external cohorts that were locked away during method design. For IBD, T2D and
adenoma, we held out each cohort in turn. The threshold was the 90th percentile of out-of-fold scores of training
controls, which targets 90% specificity, as in [1]. Held-out AUROC was 0.70–0.86 for CRC, 0.66–0.85 for IBD, 0.58–0.69 for
T2D and 0.54–0.65 for adenoma (Table S1).

At the new site, the realised FPR ranged from 0.04 to 0.59 with LASSO and from 0.00 to 0.73 with random forest (Figure 1,
Figure S1). In 22 of 32 cohort–classifier pairs (69%), the FPR was outside 0.05–0.15, that is, more than half the target
away. The pattern differed by disease. In IBD, T2D and adenoma, FPRs differed between cohorts far more than sampling
noise allows (chi-square test of equal proportions, P from 6 × 10⁻³ to 3 × 10⁻¹¹⁰; Table S2). In CRC, the three external cohorts did not
differ from each other (P = 0.12), but all three over-called: FPR 0.11–0.28 with LASSO and 0.13–0.30 with random forest.
Errors ran both ways. Thresholds were too strict in Karlsson 2013 and MetaCardis (FPR 0.00–0.05) and far too loose in Qin
2012 (0.59–0.73) and HMP2 (0.22–0.41). A single global correction could not fix both.

One referee suggested that part of this drift came from our pipeline: the threshold came from fold models, while targets
were scored by a model refitted on all training cohorts. Scoring targets with the same fold models did not reduce the
drift (75% of pairs out of band; Table S6).

## AUROC DOES NOT PREDICT THE ERROR, BECAUSE HEALTHY PEOPLE DIFFER BETWEEN SITES

Post-hoc checks clarify what moves (Table S4). AUROC did not predict the size of the FPR error (Spearman ρ = −0.18, P =
0.31). A cohort with high AUROC was no safer. The two classifiers erred in the same direction at the same site (ρ = 0.69,
P = 0.003), so the drift is a property of the site, not of one model. What moved was the score distribution of controls.
A pure change in disease prevalence cannot change the FPR at a fixed threshold, because the FPR is computed among controls
only. Sequencing depth did not explain the shift (ρ = −0.02). How controls were defined did matter. MetaCardis "controls"
are mostly people with metabolic syndrome; restricted to its 234 healthy controls, the transferred threshold gave an FPR
of only 0.02 (LASSO) or 0.004 (random forest). HMP2 controls are symptomatic patients without IBD, the very group in which
an IBD stool test would be used, and there the FPR was highest. Geography, age, diet, medication and laboratory protocol
also differ between cohorts (Table S7). So the operating point is tied to who the local controls are and how their stool
was processed.

## CORRECTIONS WITHOUT SAME-SITE LABELS DO NOT FIX THE THRESHOLD

We next tried fixes that need no labelled data from the new site (Figure 2). Standardising each species within each
cohort, a simple location–scale batch correction [14], narrowed the spread but did not remove it: 28% of pairs were in band,
and the worst cohort reached an FPR of 0.32. Percentile normalisation against controls [15], using 20 local controls, kept
the LASSO FPR near target (0.09–0.12) but cut sensitivity to 0.12–0.24, and made the random forest far too strict (FPR
0.00–0.04; Table S8). Prevalence correction [16, 17] cannot help in principle: under its own assumption, the class score
distributions are unchanged, so the FPR-targeting threshold is the status quo. A mixture-based variant was unstable (SI).
Our own label-free site-shift mixture model reached the band in 66% of pairs; we report it as a negative result.

Labelled controls must also come from the right place. When 20 controls came from a different centre (MetaCardis:
Copenhagen, Leipzig, Paris) or a different external CRC cohort, the realised FPR ranged from 0.02 to 0.28 across site pairs,
and in the worst pair every calibration exceeded 0.15 (Figure 2, orange; Table S9). Even two Japanese CRC cohorts were
not interchangeable (FPR 0.16 when Yachida controls calibrated Thomas 2019c with LASSO).

## SAME-SITE CALIBRATION WORKS ON AVERAGE, BUT A SINGLE SITE NEEDS MORE THAN 20 CONTROLS

The method that worked is simple. A site collects n people confirmed to be free of the disease, scores them with the frozen
model, and sets the threshold at the ⌈(n + 1)(1 − α)⌉-th smallest score, for target FPR α. This split-conformal rule keeps
the expected FPR at or below α if the local controls resemble future controls at that site [18, 19]. With 20 same-site
controls, every feasible cohort–classifier pair had a mean FPR within band (20 of 20; 0.08–0.11; Figure 1). The spread of
cohort-mean FPR fell from 0.09 to 0.007 (CRC), 0.30 to 0.005 (T2D) and 0.075 to 0.008 (adenoma). This was our
pre-registered criterion, and it was met (the between-cohort part could not be evaluated for IBD, which had one
feasible cohort). It is, however, a best case. Calibration and evaluation controls were halves of
the same study, so the result largely confirms the theorem.

The practically important number is the spread for a single site. With 20 controls, only 46% of single calibrations
landed within 0.05–0.15, and 19% exceeded 0.15. Theory predicts this exactly: the realised FPR follows a Beta distribution
whose 95% range is 0.01–0.26 for n = 19. The range narrows to 0.05–0.17 for n = 99 and to 0.06–0.15 for n = 199, and the
large cohorts confirmed these ranges (Figure 3B; Table S10). The rule with a 95% guarantee that the FPR stays at or below α
[20] needs at least 29 controls. In our data it gave an FPR of about 0.03 and a sensitivity of only 0.08, so it is too
conservative at small n.

In a screening programme, prevalence is low. The 90th percentile of unlabelled screened samples then estimates the
control quantile almost directly, because cases make up only a few per thousand. In simulated pools at 0.5% prevalence,
this label-free rule gave cohort-mean FPRs of 0.10–0.17 (Table S11). Its precision is limited by the number of distinct
people in the pool, as for labelled controls. A programme could therefore calibrate on its first few hundred screened
people instead of recruiting colonoscopy-confirmed controls. It must still watch for drift in who is screened.

What does this mean for CRC screening? The numbers below are illustrative, because case–control cohorts are not screening
populations. At an assumed prevalence of 0.5%, the transferred LASSO threshold produced 112–280 unnecessary colonoscopies
per 1,000 people screened in the three external cohorts. Calibration on 20 same-site controls averaged 99, but with a 95%
range of 0 to about 300 for a single site, and missed cancers rose from 1.3–2.3 to 1.5–3.3 per 1,000 (Figure 3A).
Positivity among Yachida adenoma carriers fell from 24–28% to 11–13%, so non-cancer positivity in a real screening
population would exceed the nominal 10%. Whether such a test can compete with or complement faecal immunochemical testing
is a separate question that these data cannot answer [6].

## CONCLUSION

Cross-cohort AUROC hides a practical failure: the decision threshold of a gut-microbiome classifier does not travel, and
the error is driven by who the local controls are. We suggest three steps.
(i) Studies should report the realised FPR and sensitivity at a pre-fixed threshold for each held-out cohort, alongside AUROC.
(ii) Before use, a site should set the threshold on its own data: about 100 labelled local controls for a single-site FPR
within roughly 0.05–0.17, or, at screening prevalence, a pilot pool of a few hundred unlabelled screened people. Twenty
controls fix the average but not the individual site.
(iii) Feature-level batch correction, prevalence correction and controls from another site should not be relied on to set
the operating point.
Our study has limits. All cohorts are case–control studies. We used one profiler, two classifier families and two simple
feature corrections; dedicated tools such as DEBIAS-M [21] and MMUPHin [22] remain to be tested. Temporal drift within a
site was not testable. T2D and adenoma classifiers were weak. Only one IBD cohort had enough controls for the 20-control
rule. Four adenoma cohorts were CRC development cohorts, although adenoma cases were never used in development. Code and
all per-cohort scores are public.

## METHODS

Full methods, the pre-registered protocol, deviations and all supplementary tables are in the Supporting Information.

## AUTHOR CONTRIBUTIONS

[To be completed by the authors.]

## ACKNOWLEDGMENTS

We thank the investigators of the original cohorts and the curatedMetagenomicData team.

## CONFLICT OF INTEREST STATEMENT

[To be completed by the authors.]

## FUNDING

[To be completed by the authors.]

## ETHICS STATEMENT

This study re-analysed publicly available, de-identified data. No new samples were collected.

## AI USE STATEMENT

[To be completed by the authors: describe the use of AI assistance in analysis code and drafting.]

## DATA AVAILABILITY STATEMENT

Profiles and metadata are from curatedMetagenomicData (Bioconductor ExperimentHub; release 2021-03-31, MetaCardis
2022-10-19). Code, the frozen protocol, per-cohort scores and all results: [GitHub repository URL and Zenodo DOI to be added].

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts for cross-stage and strain-level reproducible microbial biomarkers of colorectal cancer. *Nat Med*. 2025;31:2416–2429. https://doi.org/10.1038/s41591-025-03693-9
4. Mei Z, Wang F, Bhosle A, et al. Strain-specific gut microbial signatures in type 2 diabetes identified in a cross-cohort analysis of 8,117 metagenomes. *Nat Med*. 2024;30:2265–2276. https://doi.org/10.1038/s41591-024-03067-7
5. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
6. Selby K, Jensen CD, Lee JK, et al. Influence of varying quantitative fecal immunochemical test positivity thresholds on colorectal cancer detection: a community-based cohort study. *Ann Intern Med*. 2018;169:439–447. https://doi.org/10.7326/M18-0244
7. Roschewitz M, Khara G, Yearsley J, et al. Automatic correction of performance drift under acquisition shift in medical image classification. *Nat Commun*. 2023;14:6608. https://doi.org/10.1038/s41467-023-42396-y
8. Van Calster B, Steyerberg EW, Wynants L, van Smeden M. There is no such thing as a validated prediction model. *BMC Med*. 2023;21:70. https://doi.org/10.1186/s12916-023-02779-w
9. Zhang Y, Cidan Y, Xu J, Li B. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. *Front Microbiol*. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707
10. Mirzayi C, Renson A, Genomic Standards Consortium, et al. Reporting guidelines for human microbiome research: the STORMS checklist. *Nat Med*. 2021;27:1885–1892. https://doi.org/10.1038/s41591-021-01552-x
11. Ozarda Y, Higgins V, Adeli K. Verification of reference intervals in routine clinical laboratories: practical challenges and recommendations. *Clin Chem Lab Med*. 2018;57:30–37. https://doi.org/10.1515/cclm-2018-0059
12. Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
13. Beghini F, McIver LJ, Blanco-Míguez A, et al. Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife*. 2021;10:e65088. https://doi.org/10.7554/eLife.65088
14. Wang Y, Lê Cao KA. Managing batch effects in microbiome data. *Brief Bioinform*. 2020;21:1954–1970. https://doi.org/10.1093/bib/bbz105
15. Gibbons SM, Duvallet C, Alm EJ. Correcting for batch effects in case-control microbiome studies. *PLoS Comput Biol*. 2018;14:e1006102. https://doi.org/10.1371/journal.pcbi.1006102
16. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. *Neural Comput*. 2002;14:21–41. https://doi.org/10.1162/089976602753284446
17. Godau P, Kalinowski P, Christodoulou E, et al. Navigating prevalence shifts in image analysis algorithm deployment. *Med Image Anal*. 2025;102:103504. https://doi.org/10.1016/j.media.2025.103504
18. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, Wasserman L. Distribution-free predictive inference for regression. *J Am Stat Assoc*. 2018;113:1094–1111. https://doi.org/10.1080/01621459.2017.1307116
19. Bates S, Candès E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p-values. *Ann Stat*. 2023;51:149–178. https://doi.org/10.1214/22-AOS2244
20. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
21. Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol*. 2025;10:897–911. https://doi.org/10.1038/s41564-025-01954-4
22. Ma S, Shungin D, Mallick H, et al. Population structure discovery in meta-analyzed microbial communities and inflammatory bowel disease using MMUPHin. *Genome Biol*. 2022;23:208. https://doi.org/10.1186/s13059-022-02753-4

## FIGURE LEGENDS

**Figure 1. Transferred decision thresholds miss their target false-positive rate at new sites.** Each row is one
held-out cohort; the classifier is LASSO logistic regression (random forest: Figure S1). The x-axis is the realised
false-positive rate (FPR) among held-out controls; the target is 0.10 (dashed line) and the grey band is 0.05–0.15.
Blue circles: threshold from training cohorts (status quo). Orange squares: within-cohort feature standardisation, then the
training threshold. Green diamonds: threshold from 20 labelled controls of the same cohort (conformal rule), shown where the
cohort had at least 40 controls. Values are means over 200 random splits of each cohort's controls into calibration and
evaluation halves. CRC models were trained on eight development cohorts; other diseases use leave-one-cohort-out.

**Figure 2. Only labelled controls from the deployment site restore the operating point.** (A) Cohort-mean realised FPR
for each method (dot = cohort × classifier; black bar = median). (B) Share of single calibrations with FPR above 0.15. (C)
Mean sensitivity. Blue: no labelled local data. Orange: 20 labelled controls from a different centre or cohort (post hoc;
MetaCardis centres and the three external CRC cohorts; dot = site pair). Green: labelled controls from the same cohort.
Target FPR 0.10. Same-site methods are shown only for cohorts with enough controls. Site-shift mixture: 20 splits per cohort.

**Figure 3. Consequences for CRC screening and the size of the local control set.** (A) Unnecessary colonoscopies per 1,000
people screened at an assumed CRC prevalence of 0.5% (illustrative; case–control data), for the three external CRC
cohorts and the LASSO classifier. Points are means; bars are 95% ranges over 200 calibration/evaluation splits. Numbers
on the right give mean missed cancers per 1,000. (B) Realised FPR of the conformal rule against the number of same-site
controls n. Shaded band: theoretical 95% range for a single site (Beta distribution); line: expected FPR; points and bars:
observed mean and 95% range in the three largest cohorts (MetaCardis, Yachida, Qin; both classifiers).
