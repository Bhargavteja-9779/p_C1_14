---
title: "Gut microbiome colorectal cancer classifiers lose specificity across sites and patient groups, and local recalibration restores it"
---

**Article type:** Letter (Short Communication)

**Running title:** Specificity of microbiome cancer classifiers in deployment

**Authors:** P N Bhargav Teja^1^, [Second Author]^1,\*^

^1^ Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India

\* **Correspondence:** [Second Author], Vellore Institute of Technology, Vellore 632014, Tamil Nadu, India. Email: [corresponding author email]

**ORCID:** P N Bhargav Teja: [ORCID]; [Second Author]: [ORCID]

**Keywords:** gut microbiome; colorectal cancer; diagnostic specificity; external validation; metformin; recalibration; verification bias

---

## Graphical abstract summary (≤100 words)

Stool metagenomic classifiers for colorectal cancer are validated by AUROC, but a deployed test works at one cut-off. In 16 held-out sites, cut-offs set for 90% specificity gave false-positive rates from 0% to 75%. False positives also differed between patient groups: they rose with severe disease (cirrhosis, atherosclerosis) through oral-origin taxa, and in a locked cardiometabolic cohort largely with medication, especially metformin. Simple local recalibration restored the intended specificity. A rule that uses only colonoscopy results of test-positive people adds recovery from drift, per-group control and a high-confidence option. It is released as the tool cutoffguard.

---

To the Editor,

Stool metagenomic classifiers detect colorectal cancer (CRC) with an area under the ROC curve (AUROC) of about 0.8 across countries [1, 2]. A test in use, however, reports positive or negative at one cut-off, usually chosen on published case-control cohorts to give a target specificity such as 90%. Two kinds of shift can break that specificity. First, sites differ in sequencing, diet and population, the familiar batch effect [3]. Second, the people tested differ. Earlier work showed that CRC signatures also fire in samples from other diseases [2, 4] and that many microbiome changes are shared across diseases [5]. Programmes that use the fecal immunochemical test (FIT) already set positivity cut-offs locally [6]. Microbiome classifier studies, in contrast, rarely report the specificity that a fixed cut-off actually achieves at a new site or in specific patient groups. How to restore it without a new labelled study is also unclear.

Here, we audited this in 32 public cohorts from curatedMetagenomicData [7] (Table S1). All methods and endpoints were fixed in a protocol, frozen in a time-stamped commit before 16 held-out sites were analysed once. A later medication analysis was frozen the same way before it was run. We report three findings. Specificity did not travel across sites. Excess false positives concentrated in some patient groups, through two different routes. Local recalibration restored the intended specificity, and a rule based on colonoscopy outcomes of test-positive people added robustness that matters in practice.

## CUT-OFFS SET ON PUBLISHED COHORTS DO NOT HOLD AT NEW SITES

We trained L1-penalised logistic regression (LASSO) and random forest classifiers with fixed settings. Each cut-off was set at 90% specificity on out-of-fold source controls (Methods S2–S3). We applied them to three external CRC sites, after training on eight development cohorts, and by leave-one-cohort-out to IBD (4 cohorts), type 2 diabetes (T2D; 4) and adenoma (5) (Figure 1A). The realised false-positive rate (FPR) ranged from 0.00 to 0.75 (Figure 1B). It exceeded the 10% target by more than two percentage points in 12 of 22 site–model pairs in the 11 fully independent sites, and in 15 of 32 pairs when the adenoma sites are included (their controls overlap with development cohorts). Sensitivity moved with the FPR, so AUROC-based validation does not reveal the problem. Label-free site-wise standardisation of features, a simple batch correction, reduced this spread but did not remove it. In development cohorts, sites above 0.12 fell from 50% to 25% for LASSO, and random forest did not improve (Table S7).

## WHICH PATIENTS ARE OVER-FLAGGED DEPENDS ON DISEASE SEVERITY AND MEDICATION

We compared the CRC score of people with other conditions with that of controls from the same cohort (Figure 1C). In development cohorts, the score was much higher in liver cirrhosis [8] (+1.30 logit after adjustment for age, BMI and sex; 95% CI 0.99–1.60; test-positive 52% vs 8%) and atherosclerotic cardiovascular disease [9] (+0.87, 0.62–1.12). Effects were small for hypertension (+0.33) and absent for fatty liver, asthma and schizophrenia. Inside three CRC cohorts, colonoscopy-negative controls with recorded hypertension, fatty liver, T2D or hypercholesterolaemia were not flagged more often than healthy controls (4% vs 16%; adjusted score difference −0.19, −0.60 to 0.21). Mild cardiometabolic labels therefore do not drive false positives.

In the locked MetaCardis cohort [10], our pre-specified test found higher scores in heart failure (+0.33, 0.14–0.51) and T2D (+0.36, 0.26–0.46; both Holm-adjusted p < 0.01). Coronary artery disease and prediabetes showed no increase. In a second T2D cohort the increase was significant only for random forest, and a third showed none (Table S3). Because these groups differ in country and medication, we then added both to the model (post hoc). The heart-failure effect persisted (+0.28, 0.06–0.51). The T2D effect largely disappeared (+0.11, −0.03 to 0.24). Within T2D, metformin users were test-positive 2.4 times as often as non-users (20.5% vs 8.5%; adjusted +0.44, p < 10^−6^), and non-users were flagged at the control rate (10.3%). Metformin strongly reshapes the gut microbiome [11]. A smaller cohort showed the same direction, but two cohorts with few users did not (Table S6), so this finding is exploratory.

Decomposing each score gap into species contributions showed two routes (Figure 1D; Methods S5). In cirrhosis and atherosclerotic disease, 78–83% of the gap came from oral-origin taxa that are also hallmark CRC markers, such as *Streptococcus oralis*, *Fusobacterium nucleatum*, *Veillonella parvula* and *Gemella morbillorum* [1, 2, 12]. Removing such shared species from the signature cost cancer detection (AUROC 0.76 to 0.72) before it removed the excess (Table S4). In locked heart failure and T2D, and for metformin, oral taxa contributed little (≤0.05 logit). Depleted commensal fermenters and enriched taxa such as Enterobacterales dominated instead. Our pre-specified medication analysis supports the oral route: proton-pump inhibitors, which carry oral taxa into the gut [13], raised the oral part of the score (+0.18, 0.14–0.21). Their effect on the total LASSO score was not significant (+0.04, p = 0.24), so that primary hypothesis was not supported. The over-flagged groups therefore differ between settings and cannot be fully predicted in advance.

## LOCAL RECALIBRATION RESTORES THE INTENDED SPECIFICITY

We simulated deployments in which each held-out cohort played the role of a site with known true FPR and sensitivity (Methods S4). We compared four cut-off rules (Figure 2):
- the source cut-off;
- the local quantile of unlabelled scores, which assumes nobody has the disease;
- a prevalence-bounded quantile, which corrects that quantile with an upper bound on prevalence, a label-free variant of outlier tests on contaminated reference data [14];
- verified-positive recalibration.

Verified-positive recalibration uses the fact that in screening, test-positive people undergo colonoscopy, so their true status becomes known. This one-sided feedback is the classic verification-bias setting [15] and resembles "apple tasting" in online learning [16]. Above any candidate cut-off, false positives are counted exactly. Unverified people are counted as possible false positives, and the prevalence bound limits the number of controls. The rule takes the lowest cut-off whose bounded FPR stays at or below the target. It updates monthly and restarts after a month with more false positives than chance allows (drift alarm). If within-site controls are exchangeable and prevalence stays below the bound, the expected FPR is at most the target, for any history of referral, attendance or delay (Proposition S1). A high-confidence option bounds the probability that the FPR exceeds the target instead (Methods S7). Unlike label-free threshold adaptation under prevalence shift [17, 18] or Neyman–Pearson rules that need labelled local controls [19], the rule needs neither a model of the shift nor extra labelling. It does need follow-up of positives.

At stable sites, every local rule removed most of the error (Figure 2A). The source cut-off kept a mean FPR of 0.17, with 49% of site-months above 0.12. Verified-positive recalibration gave 0.085 and 0.6%, with sensitivity within 0.015 of an oracle cut-off set on the site's true controls (95% CI −0.021 to −0.009). The pre-specified comparison favoured it over the source cut-off (difference in months above 0.12: −0.46, −0.66 to −0.20; p = 0.011) and over the local quantile (p = 2.5 × 10^−7^). Its advantage over the prevalence-bounded quantile (p = 0.049) came from small sites and vanished at the nine cohorts with at least 40 controls (FPR 0.090 vs 0.083; p = 0.72). The verified-positive rule helped in three situations:
- **Upward score drift**, for example a new kit lot. After a +0.5 logit drift, its alarm restored the FPR within one to two months, while the label-free rules stayed high (months 10–12: 0.086 vs 0.154; Figure 2B).
- **Higher prevalence.** At 10% prevalence, the prevalence-bounded rule became conservative (CRC sensitivity 0.44 vs 0.52).
- **Patient groups.** At MetaCardis, pooled recalibration kept the overall FPR at 0.095, but heart failure stayed at 0.21 and T2D at 0.14. Running the rule within recorded groups brought every group to 0.08–0.09 (Figure 2C). In over-flagged groups this raises the cut-off, which lowers sensitivity, because comorbid CRC patients did not score higher (Table S8).

We then removed the resampling. At the two largest locked sites, each real sample entered once in random order, and the FPR was measured on controls not yet seen (Figure 2D). The standard rule kept the mean FPR on target (0.094), but single months exceeded 0.12 in 19% of cases. The high-confidence option reduced this to 5% (mean FPR 0.071). The costs are a burn-in month with about 27% of people referred, and lower sensitivity wherever the source cut-off had been too liberal. At CRC sites, compared with the source cut-off, the rule avoided 83 false-positive referrals per 1,000 people screened, but missed 1.1 more cancers per 1,000 (sensitivity 0.52 vs 0.64). After a downward drift, all rules became too strict for the rest of the simulated period (Table S2c).

## CONCLUSION

A microbiome CRC test does not keep its specificity when it moves to a new site or to a different patient mix. Excess false positives can come from severe disease through oral taxa, or from drugs such as metformin. Local recalibration is therefore needed. A rule that uses only colonoscopy outcomes recovers from drift, controls the FPR within groups and offers a high-confidence version. We release it as the open-source package cutoffguard. Our deployments were simulated from case-control cohorts, colonoscopy was treated as a perfect reference, and the medication findings rest mainly on one cohort. We recommend that microbiome test studies report the realised specificity at each external site and in major patient groups, check common medications, and plan outcome-based recalibration before deployment.

## METHODS

Detailed methods, Proposition S1 with proof, and Supporting Information references are provided in the Supporting Information. All code, the frozen protocols, the full development log and the cutoffguard package are openly available (see Data Availability Statement).

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

All data analysed are publicly available from the curatedMetagenomicData Bioconductor package (ExperimentHub; releases 2021-03-31, 2022-04-13 and 2022-10-19). The analysis code, the frozen protocols with file hashes, the development log and the cutoffguard package are available at [GitHub repository URL] and archived at [Zenodo DOI]. Supplementary materials (methods, figures, tables, graphical abstract, slides, videos, Chinese translated version and update materials) may be found in the online DOI or iMeta Science http://www.imeta.science/.

## REFERENCES

1. Wirbel J, Pyl PT, Kartal E, Zych K, Kashani A, Milanese A, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. *Nat Med*. 2019;25:679–689. https://doi.org/10.1038/s41591-019-0406-6
2. Thomas AM, Manghi P, Asnicar F, Pasolli E, Armanini F, Zolfo M, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. *Nat Med*. 2019;25:667–678. https://doi.org/10.1038/s41591-019-0405-7
3. Wang Y, Lê Cao KA. Managing batch effects in microbiome data. *Brief Bioinform*. 2020;21:1954–1970. https://doi.org/10.1093/bib/bbz105
4. Wirbel J, Zych K, Essex M, Karcher N, Kartal E, Salazar G, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. *Genome Biol*. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1
5. Duvallet C, Gibbons SM, Gurry T, Irizarry RA, Alm EJ. Meta-analysis of gut microbiome studies identifies disease-specific and shared responses. *Nat Commun*. 2017;8:1784. https://doi.org/10.1038/s41467-017-01973-8
6. Selby K, Levine EH, Doan C, Gies A, Brenner H, Quesenberry C, et al. Effect of sex, age, and positivity threshold on fecal immunochemical test accuracy: a systematic review and meta-analysis. *Gastroenterology*. 2019;157:1494–1505. https://doi.org/10.1053/j.gastro.2019.08.023
7. Pasolli E, Schiffer L, Manghi P, Renson A, Obenchain V, Truong DT, et al. Accessible, curated metagenomic data through ExperimentHub. *Nat Methods*. 2017;14:1023–1024. https://doi.org/10.1038/nmeth.4468
8. Qin N, Yang F, Li A, Prifti E, Chen Y, Shao L, et al. Alterations of the human gut microbiome in liver cirrhosis. *Nature*. 2014;513:59–64. https://doi.org/10.1038/nature13568
9. Jie Z, Xia H, Zhong SL, Feng Q, Li S, Liang S, et al. The gut microbiome in atherosclerotic cardiovascular disease. *Nat Commun*. 2017;8:845. https://doi.org/10.1038/s41467-017-00900-1
10. Fromentin S, Forslund SK, Chechi K, Aron-Wisnewsky J, Chakaroun R, Nielsen T, et al. Microbiome and metabolome features of the cardiometabolic disease spectrum. *Nat Med*. 2022;28:303–314. https://doi.org/10.1038/s41591-022-01688-4
11. Forslund K, Hildebrand F, Nielsen T, Falony G, Le Chatelier E, Sunagawa S, et al. Disentangling type 2 diabetes and metformin treatment signatures in the human gut microbiota. *Nature*. 2015;528:262–266. https://doi.org/10.1038/nature15766
12. Schmidt TS, Hayward MR, Coelho LP, Li SS, Costea PI, Voigt AY, et al. Extensive transmission of microbes along the gastrointestinal tract. *eLife*. 2019;8:e42693. https://doi.org/10.7554/eLife.42693
13. Imhann F, Bonder MJ, Vich Vila A, Fu J, Mujagic Z, Vork L, et al. Proton pump inhibitors affect the gut microbiome. *Gut*. 2016;65:740–748. https://doi.org/10.1136/gutjnl-2015-310376
14. Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. *Proc Mach Learn Res*. 2025;267. https://doi.org/10.48550/arXiv.2502.04807
15. Begg CB, Greenes RA. Assessment of diagnostic tests when disease verification is subject to selection bias. *Biometrics*. 1983;39:207–215. https://doi.org/10.2307/2530820
16. Helmbold DP, Littlestone N, Long PM. Apple tasting. *Inf Comput*. 2000;161:85–139. https://doi.org/10.1006/inco.2000.2870
17. Godau P, Kalinowski P, Christodoulou E, Reinke A, Tizabi M, Ferrer L, et al. Navigating prevalence shifts in image analysis algorithm deployment. *Med Image Anal*. 2025;102:103504. https://doi.org/10.1016/j.media.2025.103504
18. Qiu Y, Zhao Y, Zheng Y. Shift-adjusted Neyman–Pearson classifiers via single index modeling (SACSIM). *Biometrics*. 2026;82:ujag138. https://doi.org/10.1093/biomtc/ujag138
19. Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv*. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659

## FIGURE LEGENDS

**Figure 1. Specificity of microbiome CRC classifiers across sites and patient groups.** (A) Study design. (B) Realised false-positive rate at each held-out site when the cut-off is set for 90% specificity on source cohorts (dashed line, target). Filled circles, LASSO; open squares, random forest; markers jittered vertically. Adenoma sites share controls with development cohorts. (C) Difference in CRC-test score (logit, LASSO, 95% CI) between condition groups and controls of the same cohort. Open, development cohorts, adjusted for age, BMI and sex. Filled blue, locked MetaCardis cohort, adjusted for sex, then country, then medications (PPI, metformin, statin, aspirin, beta-blocker). Orange, colonoscopy-negative controls with recorded cardiometabolic comorbidity vs healthy controls inside three CRC cohorts (site fixed effects; age, BMI, sex). (D) Species-level decomposition of the score gaps: enriched oral-origin taxa, depleted commensal fermenters and other taxa (development: cirrhosis, atherosclerotic disease; locked: heart failure, T2D, and metformin users vs non-users within T2D, exploratory).

**Figure 2. Local recalibration restores the intended specificity.** (A) True false-positive rate by month in simulated deployments at the 11 CRC, IBD and T2D held-out sites (1% prevalence; two classifiers; 200 streams each). Lines, means; band, 10th–90th percentile for verified-positive recalibration; dotted line, target. (B) The same after all scores shift by +0.5 logit from month 7. (C) False-positive rate by recorded condition at the locked MetaCardis site (months 7–18, LASSO) for the source cut-off, pooled recalibration and per-group recalibration. (D) Without resampling: at the two largest held-out sites, each sample entered once in random order, and the false-positive rate was measured on controls not yet seen (months ≥3; 300 random orders, 1% and 5% prevalence). Bars, share of months above 12%; labels, mean false-positive rate.
