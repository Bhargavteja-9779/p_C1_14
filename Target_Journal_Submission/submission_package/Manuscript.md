---
title: "Gut microbiome cancer tests mistake chronic disease for cancer, and routine colonoscopy outcomes can reset their cut-offs"
---

**Article type:** Letter (Short Communication)

**Running title:** Resetting microbiome test cut-offs at new sites

**Authors:** P N Bhargav Teja^1^, [Second Author]^1,\*^

^1^ Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India

\* **Correspondence:** [Second Author], Vellore Institute of Technology, Vellore 632014, Tamil Nadu, India. Email: [corresponding author email]

**ORCID:** P N Bhargav Teja: [ORCID]; [Second Author]: [ORCID]

**Keywords:** gut microbiome; colorectal cancer screening; diagnostic threshold; specificity; comorbidity; verification bias; distribution shift; conformal prediction

---

## Highlights

- Cut-offs of gut microbiome disease classifiers, set to give 90% specificity on published cohorts, gave false-positive rates from 0% to 75% at 16 new sites.
- The cancer score was higher in people with heart failure and type 2 diabetes than in healthy people at the same site; in development cohorts, cirrhosis and atherosclerotic cardiovascular disease showed the largest effects. Oral-origin taxa that mark colorectal cancer drove most of this excess.
- A recalibration rule that uses only the outcomes of routine colonoscopy kept the false-positive rate on target, and a per-group version removed the excess false alarms in people with chronic disease.

## Graphical abstract summary (≤100 words)

Stool microbiome tests for colorectal cancer are trained on case-control cohorts and validated by AUROC. We show that the cut-off chosen on published cohorts does not carry to a new screening site and that the test flags people with chronic disease, such as heart failure and type 2 diabetes, more often than healthy people. Oral-origin taxa shared between cancer and chronic disease explain much of this. We propose a recalibration rule that uses only colonoscopy outcomes of test-positive people, which every screening programme already collects. In locked tests it kept false alarms on target and removed the excess in chronic disease.

---

To the Editor,

Colorectal cancer (CRC) caused about 1.9 million new cases and 0.9 million deaths worldwide in 2020 [1]. Screening reduces deaths, but colonoscopy capacity is limited, and every false-positive test uses a colonoscopy slot and exposes a person to a small risk of harm. Stool metagenomic classifiers detect CRC with an area under the ROC curve (AUROC) of about 0.8 across countries [2–4], and similar classifiers exist for many other diseases [5–7]. A test that is used in a programme, however, does not report an AUROC. It reports positive or negative at one fixed cut-off. That cut-off is usually chosen on published case-control cohorts to give a target specificity, such as 90%. Whether the specificity holds at a new site is rarely checked. In fecal immunochemical testing, programmes already know that positivity cut-offs must be set locally [8, 9].

Two things can move the false-positive rate (FPR) at a new site. First, the site itself differs from the source cohorts in sequencing, diet and population, which is the familiar batch or site effect [10]. Second, the people who are screened differ. Screening-age populations carry a high load of cardiometabolic, liver and inflammatory disease, and many microbiome changes are shared across diseases rather than specific to one [5, 11]. If a CRC test reacts to these shared changes, its false alarms will fall disproportionately on people who already have chronic disease.

Here, we measured both effects in 30 public cohorts from curatedMetagenomicData [12], including 16 locked test sites (Table S1). We fixed all methods and endpoints in a protocol before touching the locked test cohorts. We found that source-derived cut-offs missed their target at nearly half of the sites. CRC tests flagged people with heart failure and type 2 diabetes more often than healthy people at the same site. We then propose a simple recalibration rule that uses only what a screening programme already observes: the colonoscopy outcomes of people who test positive.

## CUT-OFFS CHOSEN ON PUBLISHED COHORTS DO NOT HOLD AT NEW SITES

We trained L1-penalised logistic regression (LASSO) and random forest classifiers with fixed settings and set the cut-off at 90% specificity on out-of-fold source controls (Supporting Information, Methods S2–S3). We applied them to three external CRC sites (classifiers trained on eight development cohorts) and, by leave-one-cohort-out, to four IBD, four type 2 diabetes (T2D) and five adenoma cohorts (Table S1). The realised FPR at the new site ranged from 0.11 to 0.28 for CRC, 0.02 to 0.41 for IBD, 0.00 to 0.75 for T2D and 0.00 to 0.26 for adenoma (Figure 1A). In 15 of 32 site–model pairs (47%), the FPR was more than two percentage points above the 10% target. In a pilot analysis across all 11 CRC cohorts, this spread exceeded binomial sampling noise (overdispersion test, p = 2 × 10^−7^ for random forest; Methods S1). AUROC-only validation would not reveal this failure, because AUROC does not depend on the cut-off.

## CRC TESTS RAISE THE CANCER SCORE IN CHRONIC DISEASE

We applied the CRC classifier, trained only on the development CRC cohorts, to cohorts of people with other conditions and compared each condition group with healthy controls from the same cohort. This within-cohort comparison removes the site effect. In seven development cohorts, the cancer score was higher in every condition (Figure 1B). The largest effects were in liver cirrhosis (52% vs 8% test-positive; score difference +1.30 logit after adjustment for age, BMI and sex, 95% CI 0.99–1.60) and atherosclerotic cardiovascular disease (52% vs 19%; +0.87, 0.62–1.12). Hypertension (+0.33) and ME/CFS (+0.39) also showed significant increases.

We then tested this pre-specified hypothesis once in locked cohorts that no CRC model had touched (Figure 1B, Table S3). In MetaCardis [13], people with heart failure were test-positive 2.3 times as often as controls, and the adjusted score increase was significant after Holm correction for both classifiers (LASSO +0.33, 95% CI 0.14–0.51). People with T2D were test-positive 1.7 (LASSO) to 3.1 (random forest) times as often (+0.35, 0.25–0.45; Holm-adjusted p < 10^−4^). T2D in a second cohort [14] was significant for random forest (+0.35, Holm p = 0.0002), with a nominal effect for LASSO. Coronary artery disease and prediabetes in MetaCardis, and T2D in a small Swedish cohort, showed no increase. In IBD, the score increase was nominally significant in one cohort but did not survive correction. The hypothesis was therefore partly supported. The effect is real for heart failure and T2D, and it is smaller in the locked cohorts than in the development cohorts.

## SHARED ORAL-ORIGIN TAXA EXPLAIN WHY THE SIGNATURE CANNOT SIMPLY BE CLEANED

To see why the test reacts to chronic disease, we split each condition's score increase into species contributions (Figure 1C, Methods S5; exploratory, development cohorts). Two routes emerged. In cirrhosis, atherosclerotic disease and fatty liver, 78–100% of the increase came from enrichment of oral-origin taxa, including *Streptococcus oralis*, *Fusobacterium nucleatum*, *Veillonella parvula*, *Gemella morbillorum* and *Peptostreptococcus*. These are among the best-known CRC markers [2, 3], and oral-to-gut transmission is common in disease [15, 16]. In hypertension, 81% came from depletion of fibre-fermenting commensals such as *Eubacterium eligens* and *Roseburia*. Removing the species shared with other conditions from the signature lowered cancer detection (AUROC 0.76 to 0.72) before it removed the excess false alarms (Table S4). Adding other-disease controls to the training data [3] lowered false alarms overall but kept the gap between groups. The signal that makes the test good at finding cancer is partly the same signal that makes it fire in chronic disease. This argues for fixing the cut-off where the test is used, rather than only in the signature.

## ROUTINE COLONOSCOPY OUTCOMES RESET THE CUT-OFF AT EACH SITE

A screening programme does not observe labels for all tested people. It does observe the colonoscopy result of every person who tests positive. This one-sided feedback is the classic verification-bias setting [17] and resembles "apple tasting" in online learning [18]. We used it directly. Above any candidate cut-off, the number of false positives can be counted exactly from colonoscopy outcomes. People who were not verified are counted as possible false positives, and an upper bound on prevalence, which programmes know, bounds the number of controls. The rule chooses the lowest cut-off whose bounded FPR stays at or below the target, with a finite-sample correction (Methods S3). It starts with one liberal "burn-in" month, updates monthly, and restarts its data window when a month shows more false positives than chance allows (drift alarm).

We simulated 12-month deployments in which each locked cohort played the role of a screening site with known true FPR and sensitivity (Methods S4). Using the source cut-off as the status quo, the FPR stayed at 0.17 on average, and 49% of site-months exceeded 0.12. With verified-positive recalibration, the FPR settled at 0.085 from month 2, and 0.6% of site-months exceeded 0.12 (Figure 2A). The pre-specified primary comparison favoured the new rule over the source cut-off (difference in the share of months above 0.12: −0.46, 95% CI −0.66 to −0.20; p = 0.011). It also favoured the new rule over a local quantile of unlabelled scores (−0.10, p = 2.5 × 10^−7^) and over a prevalence-bounded quantile (−0.04, p = 0.049). Sensitivity was within 0.015 of an oracle cut-off set on the site's true controls (95% CI −0.021 to −0.009; non-inferior at a 0.05 margin). At 1% prevalence, the rule avoided 83 unnecessary colonoscopies per 1,000 people screened per year at the CRC sites. It missed 1.1 more cancers per 1,000, because the source cut-off was too liberal there (Figure 2D).

The rule was robust to 70% colonoscopy attendance, 5% of cancers missed at colonoscopy, one-month delays in results, misspecified prevalence, batch sizes of 50–200 per month, and 5% or 20% targets (FPR on target, ≤3% of months above target + 0.02; Table S2). After a sudden score drift of +0.5 logit, the drift alarm brought the FPR back to 0.09 within three months, while the other rules stayed high (Figure 2B). With all stresses combined, recovery was slower (FPR 0.10, but 20% of months above 0.12 by months 13–18).

## RECALIBRATING PER GROUP REMOVES THE EXCESS FALSE ALARMS IN CHRONIC DISEASE

A pooled rule gets the overall FPR right by averaging over people. At MetaCardis (locked), the pooled rule kept the overall FPR at 0.095, yet people with heart failure had an FPR of 0.21 and people with T2D 0.14, while controls fell to 0.08 (Figure 2C). Running the same rule separately within recorded comorbidity groups brought every group to 0.08–0.09 at the same overall FPR (0.092). The trade-off is explicit. In the over-flagged groups the cut-off rises, so sensitivity for cancer in those groups is lower in our proxy analysis (heart failure 0.36 vs 0.45 for the pooled rule). Whether to equalise false alarms or sensitivity across groups is a policy choice. The rule makes that choice visible and controllable, instead of leaving it hidden in a single cut-off.

## CONCLUSION

The same gut microbiome test can produce very different false-alarm rates depending on where it is used and on whom. Part of the reason is biological: hallmark CRC taxa also rise in chronic diseases that are common at screening age. We show that programmes can keep the false-positive rate on target, overall and within patient groups, using only colonoscopy outcomes they already collect. Our study has limitations. Deployment was simulated from case-control cohorts, not run in a real programme. Colonoscopy was treated as a perfect reference. Comorbidity groups were defined by study labels. The sensitivity in comorbid groups was estimated from a proxy. Microbiome test studies should report realised specificity at each external site, check false alarms in common chronic diseases, and plan for local, outcome-based recalibration before deployment.

## METHODS

Detailed methods are provided in the Supporting Information. All code, the frozen protocol and development log are openly available (see Data Availability Statement).

## AUTHOR CONTRIBUTIONS

**P N Bhargav Teja:** Conceptualization; data curation; formal analysis; methodology; software; validation; visualization; writing—original draft; writing—review and editing. **[Second Author]:** Conceptualization; supervision; methodology; writing—review and editing. All authors have read the final manuscript and approved it for publication.

## ACKNOWLEDGMENTS

We thank the investigators of the original cohort studies and the curatedMetagenomicData team for making uniformly processed data publicly available.

## CONFLICT OF INTEREST STATEMENT

The authors declare no conflicts of interest.

## FUNDING

This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors.

## ETHICS STATEMENT

This study used only publicly available, de-identified data from previously published studies, which obtained ethics approval and informed consent as described in the original publications. No new ethics approval was required.

## DECLARATION OF AI-ASSISTED TECHNOLOGIES

During the preparation of this work, the authors used an AI-based assistant (Claude, Anthropic) to help write analysis code and draft and edit text. The authors reviewed, verified and edited all code, results and text and take full responsibility for the content of the publication.

## DATA AVAILABILITY STATEMENT

All data analysed are publicly available from the curatedMetagenomicData Bioconductor package (ExperimentHub; releases 2021-03-31 and 2022-10-19). The scripts used for the analysis, the frozen analysis protocol and file hashes, and the development log are available at [GitHub repository URL, to be added before submission]. Supplementary materials (methods, figures, tables, graphical abstract, slides, videos, Chinese translated version and update materials) may be found in the online DOI or iMeta Science http://www.imeta.science/.

## REFERENCES

1. Sung H, Ferlay J, Siegel RL, Laversanne M, Soerjomataram I, Jemal A, et al. Global cancer statistics 2020: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries. *CA Cancer J Clin*. 2021;71:209–249. https://doi.org/10.3322/caac.21660
2. Wirbel J, Pyl PT, Kartal E, Zych K, Kashani A, Milanese A, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
3. Thomas AM, Manghi P, Asnicar F, Pasolli E, Armanini F, Zolfo M, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
4. Zeller G, Tap J, Voigt AY, Sunagawa S, Kultima JR, Costea PI, et al. Potential of fecal microbiota for early-stage detection of colorectal cancer. *Mol Syst Biol*. 2014;10:766. https://doi.org/10.15252/msb.20145645
5. Duvallet C, Gibbons SM, Gurry T, Irizarry RA, Alm EJ. Meta-analysis of gut microbiome studies identifies disease-specific and shared responses. *Nat Commun*. 2017;8:1784. https://doi.org/10.1038/s41467-017-01973-8
6. Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. *PLoS Comput Biol*. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977
7. Li M, Liu J, Zhu J, Wang H, Sun C, Gao NL, et al. Performance of gut microbiome as an independent diagnostic tool for 20 diseases: cross-cohort validation of machine-learning classifiers. *Gut Microbes*. 2023;15:2205386. https://doi.org/10.1080/19490976.2023.2205386
8. Selby K, Levine EH, Doan C, Gies A, Brenner H, Quesenberry C, et al. Effect of sex, age, and positivity threshold on fecal immunochemical test accuracy: a systematic review and meta-analysis. *Gastroenterology*. 2019;157:1494–1505. https://doi.org/10.1053/j.gastro.2019.08.023
9. Young GP, Rabeneck L, Winawer SJ. Fecal immunochemical test positivity thresholds: an international survey of population-based screening programs. *Dig Dis Sci*. 2024. https://doi.org/10.1007/s10620-024-08664-7
10. Wang Y, Lê Cao KA. Managing batch effects in microbiome data. *Brief Bioinform*. 2020;21:1954–1970. https://doi.org/10.1093/bib/bbz105
11. Wirbel J, Zych K, Essex M, Karcher N, Kartal E, Salazar G, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
12. Pasolli E, Schiffer L, Manghi P, Renson A, Obenchain V, Truong DT, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
13. Fromentin S, Forslund SK, Chechi K, Aron-Wisnewsky J, Chakaroun R, Nielsen T, et al. Microbiome and metabolome features of the cardiometabolic disease spectrum. *Nat Med*. 2022;28:303–314. https://doi.org/10.1038/s41591-022-01688-4
14. Forslund K, Hildebrand F, Nielsen T, Falony G, Le Chatelier E, Sunagawa S, et al. Disentangling type 2 diabetes and metformin treatment signatures in the human gut microbiota. *Nature*. 2015;528:262–266. https://doi.org/10.1038/nature15766
15. Qin N, Yang F, Li A, Prifti E, Chen Y, Shao L, et al. Alterations of the human gut microbiome in liver cirrhosis. *Nature*. 2014;513:59–64. https://doi.org/10.1038/nature13568
16. Schmidt TS, Hayward MR, Coelho LP, Li SS, Costea PI, Voigt AY, et al. Extensive transmission of microbes along the gastrointestinal tract. *eLife*. 2019;8:e42693. https://doi.org/10.7554/eLife.42693
17. Begg CB, Greenes RA. Assessment of diagnostic tests when disease verification is subject to selection bias. *Biometrics*. 1983;39:207–215. https://doi.org/10.2307/2530820
18. Helmbold DP, Littlestone N, Long PM. Apple tasting. *Inf Comput*. 2000;161:85–139. https://doi.org/10.1006/inco.2000.2870
19. Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. *Proc Mach Learn Res*. 2025;267. https://doi.org/10.48550/arXiv.2502.04807
20. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659
21. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. *Neural Comput*. 2002;14:21–41. https://doi.org/10.1162/089976602753284446
22. Jie Z, Xia H, Zhong SL, Feng Q, Li S, Liang S, et al. The gut microbiome in atherosclerotic cardiovascular disease. *Nat Commun*. 2017;8:845. https://doi.org/10.1038/s41467-017-00900-1

## FIGURE LEGENDS

**Figure 1. Microbiome test cut-offs do not transfer, and the CRC test reacts to chronic disease.** (A) Realised false-positive rate at each new site when the cut-off is set for 90% specificity on source cohorts (dashed line: intended 10%). External CRC sites (classifiers trained on eight development cohorts) and leave-one-cohort-out sites for IBD, type 2 diabetes and adenoma; filled circles, LASSO; open squares, random forest. (B) Difference in CRC-test score (logit) between each condition and healthy controls of the same cohort, adjusted for age, BMI and sex where recorded (95% CI). Open circles, development cohorts; filled circles, locked test cohorts analysed once under the frozen protocol (LASSO shown; random forest in Table S3). (C) Species-level decomposition of the score gap in development cohorts (exploratory): contributions of enriched oral-origin taxa, depleted commensal fermenters and other taxa; black bars, net gap.

**Figure 2. Verified-positive recalibration keeps false alarms on target at each site and within patient groups.** (A) True false-positive rate by month in simulated deployments at the 16 locked sites (two classifiers, 1% prevalence, 200 streams each); lines, means; band, 10th–90th percentile for the proposed rule; dotted line, 10% target. (B) Same after a +0.5 logit drift of all scores from month 7; the drift alarm restarts the recalibration window. (C) False-positive rate by recorded condition at the locked MetaCardis site (months 7–18, LASSO) for the source cut-off, the pooled recalibration and the per-group recalibration. (D) Unnecessary colonoscopy referrals per 1,000 people screened over 12 months at 1% prevalence for the source cut-off and the proposed rule; missed cancers per 1,000 are shown below each disease.
