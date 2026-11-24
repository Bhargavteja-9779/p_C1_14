---
title: "Microbiome colorectal cancer tests lose specificity at new sites; local recalibration restores it"
---

**Article type:** Letter (Short Communication)

**Running title:** Specificity of microbiome tests at new sites

**Authors:** P N Bhargav Teja^1^, [Second Author]^1,\*^

^1^ Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India

\* **Correspondence:** [Second Author], Vellore Institute of Technology, Vellore 632014, Tamil Nadu, India. Email: [corresponding author email]

**ORCID:** P N Bhargav Teja: [ORCID]; [Second Author]: [ORCID]

**Keywords:** gut microbiome; colorectal cancer; diagnostic specificity; external validation; metformin; recalibration; verification bias

---

## Graphical abstract summary (≤100 words)

Stool microbiome tests for colorectal cancer are judged by AUROC, but in use they work at a single cut-off. We asked whether a cut-off set for 90% specificity on published cohorts keeps that specificity elsewhere. At 11 colorectal cancer sites, false-positive rates ranged from 0% to 37%, far beyond sampling noise. People with cirrhosis or atherosclerosis were over-flagged through oral-origin marker taxa; in a diabetes cohort the excess tracked metformin use (exploratory). Resetting the cut-off locally from unlabelled scores restored specificity at stable sites. A rule that uses only colonoscopy results of test-positive people also recovered from large score drift. Both are released as cutoffguard.

---

To the Editor,

Stool metagenomic tests detect colorectal cancer (CRC) with an area under the ROC curve (AUROC) of about 0.8 across countries [1, 2]. In use, however, a test reports positive or negative at one cut-off, usually chosen on published case-control cohorts to give a target specificity such as 90%. For the fecal immunochemical test (FIT), screening programmes already set positivity cut-offs locally [6]; microbiome tests have no equivalent practice. Two kinds of shift can break the specificity of a fixed cut-off. First, sites differ in sequencing, diet and population, the familiar batch effect [3]. Second, the people tested include patients with other diseases or drugs that change the gut microbiome; CRC signatures are known to fire in samples from other diseases [2, 4], and many microbiome changes are shared across diseases [5]. Microbiome studies rarely report the specificity a fixed cut-off actually achieves at a new site or in specific patient groups, or how to restore it without a new labelled study.

Here, we audited this in 32 public cohorts from curatedMetagenomicData [7] (Table S1). Methods and endpoints were fixed in a protocol, frozen in a time-stamped commit before the held-out sites were analysed once; a pilot before the data lock had evaluated the source cut-off at all 11 CRC cohorts, including the three later held-out CRC sites. A medication analysis was frozen the same way before it was run, and post hoc analyses are labelled as such. A cut-off set for 90% specificity on published cohorts gave false-positive rates above target at about half of the new CRC sites, and resetting it locally restored the intended specificity.

## CUT-OFFS SET ON PUBLISHED COHORTS DO NOT HOLD AT NEW CRC SITES

We trained L1-penalised logistic regression (LASSO) and random forest classifiers with fixed settings and set the cut-off at 90% specificity on out-of-fold source controls (Methods S2–S3). We audited this cut-off at all 11 CRC cohorts: three locked external sites (models trained on eight development cohorts) and the eight development cohorts by leave-one-cohort-out. Because the audit evaluates a fixed cut-off and involves no method choice, development cohorts are valid audit sites. The realised false-positive rate (FPR) ranged from 0.00 to 0.37 (Figure 1B). It exceeded 0.12 at 6 of 11 sites for each classifier, and the exact 95% confidence interval excluded the 10% target at four to five sites. The spread was far beyond sampling noise (overdispersion χ² = 102 on 11 df, p < 10^−15^; between-site SD of the logit FPR 0.58–0.65). Because sensitivity rose and fell with the FPR, the AUROC alone would not reveal this. The same failure occurred for classifiers of other diseases (IBD and T2D sites: FPR 0.00–0.75; Table S2). Label-free site-wise standardisation of features, a simple batch correction, reduced but did not remove the spread (post hoc, development sites above 0.12: LASSO 50% to 25%, random forest 38% to 25%; Table S7).

## OVER-FLAGGED PATIENT GROUPS DIFFER BETWEEN SETTINGS

We compared the CRC score of people with other conditions with that of controls from the same cohort (Figure 1C). In development cohorts, the score was much higher in liver cirrhosis [8] (+1.30 logit after adjustment for age, BMI and sex; 95% CI 0.99–1.60; test-positive 52% vs 8%) and atherosclerotic cardiovascular disease [9] (+0.87, 0.62–1.12). Effects were small for hypertension (+0.33) and absent for fatty liver, asthma and schizophrenia. In a post hoc check inside three CRC cohorts, colonoscopy-negative controls with recorded hypertension, fatty liver, T2D or hypercholesterolaemia were not flagged more often than healthy controls (4% vs 16%; adjusted score difference −0.19, −0.60 to 0.21). Mild cardiometabolic labels were therefore not associated with more false positives in these cohorts.

In the locked MetaCardis cohort [10], our pre-specified test (adjusted for sex) found higher scores in heart failure (+0.33, 0.14–0.51) and T2D (+0.35, 0.25–0.45; both Holm-adjusted p < 0.01). Coronary artery disease and prediabetes showed no increase. In a second T2D cohort the increase was significant only for random forest, and a third showed none (Table S3). Because these groups differ in country and medication, we then added both to the model (post hoc). The heart-failure effect was attenuated: it remained significant for LASSO (+0.28, 0.06–0.50) but not for random forest (+0.13, p = 0.11), nor in a complete-case analysis that also adjusted for age and BMI (n = 1,310; Table S9). The T2D effect largely disappeared (+0.11, −0.02 to 0.24). Metformin strongly reshapes the gut microbiome [11]. Within T2D, metformin users were test-positive 2.4 times as often as non-users (20.5% vs 8.5%; adjusted +0.44, p < 10^−6^), and non-users were flagged at a rate similar to controls (10.3%). A smaller cohort showed the same direction, but two cohorts with few users did not (Table S6), so this finding is exploratory.

Decomposing each score gap into species contributions (exploratory; Methods S5) showed two routes (Figure 1D). In cirrhosis and atherosclerotic disease, 78–83% of the gap came from oral-origin taxa that are also hallmark CRC markers, such as *Streptococcus oralis*, *Fusobacterium nucleatum*, *Veillonella parvula* and *Gemella morbillorum* [1, 2, 12]. Removing such shared species from the signature cost cancer detection (AUROC 0.76 to 0.72) before it removed the excess (Table S4). In locked heart failure and T2D, and for metformin, oral taxa contributed little (≤0.05 logit). Depleted commensal fermenters and other enriched taxa dominated instead (Table S9b). Our pre-specified medication analysis supports the oral route: proton-pump inhibitors, which carry oral taxa into the gut [13], raised the oral part of the score (+0.18, 0.14–0.21). Their effect on the total LASSO score was not significant (+0.04, p = 0.24), so that primary hypothesis was not supported. The over-flagged groups therefore differ between settings and cannot be fully predicted in advance.

## LOCAL RECALIBRATION RESTORES SPECIFICITY; COLONOSCOPY FEEDBACK HELPS UNDER DRIFT

We simulated 12-month deployments in which each cohort played the role of a screening site with known true FPR and sensitivity (Methods S4), and compared four cut-off rules: the source cut-off; the local quantile of unlabelled scores, which assumes nobody has the disease; a prevalence-bounded quantile, which corrects that quantile with an upper bound on prevalence, in the spirit of outlier tests on contaminated reference data [14]; and verified-positive recalibration. In screening, people who test positive have a colonoscopy, so their true status becomes known, the classic verification-bias setting [15] that resembles "apple tasting" in online learning [16]. The verified-positive rule counts confirmed false positives above each candidate cut-off, treats everyone not yet confirmed as a possible false positive, and picks the lowest cut-off whose worst-case FPR is at or below the target. It updates monthly, starts with one deliberately liberal month to collect verified outcomes, and restarts when a month has more false positives than chance allows. If controls at a site are exchangeable and prevalence stays below the bound, the expected FPR is at most the target, whatever the referral, attendance or delay (Proposition S1). Unlike threshold adaptation under prevalence shift [17, 18] or Neyman–Pearson rules that need labelled local controls [19], neither local rule needs a model of the shift or extra labelling.

At the 11 CRC sites (1% prevalence; post hoc), the source cut-off kept a mean FPR of 0.14, with 55% of site-months above 0.12 (Figure 2A). All local rules removed most of this error: local quantile 0.11 (21% of months above 0.12), prevalence-bounded quantile 0.10 (13%) and verified-positive 0.083 (0.3%), with sensitivity 0.50 against 0.52 for an oracle cut-off set on each site's true controls. In the pre-specified analysis across all 16 held-out sites, the verified-positive rule beat the source cut-off (difference in months above 0.12: −0.46, 95% CI −0.66 to −0.20; p = 0.011; significant for CRC but not separately for IBD, T2D or adenoma) and the local quantile (p = 2.5 × 10^−7^), with sensitivity within 0.015 of the oracle. Its advantage over the prevalence-bounded quantile (p = 0.049) came from sites with few controls: at the nine cohorts with at least 40 controls (post hoc), the two rules were equivalent (FPR 0.090 vs 0.083; p = 0.72), and even the comparison with the source cut-off was no longer significant (p = 0.074), because the source cut-off was too strict at some large sites. We then removed the resampling (post hoc; Figure 2D): at three large held-out sites, each sample entered once in random order and the FPR was measured on controls not yet seen; at MetaCardis, controls also entered country by country, a real site shift. All local rules kept the mean FPR near target, but single months exceeded 0.12 often (prevalence-bounded 15%, verified-positive 18% in random order). High-confidence versions of both rules, added after the locked analysis, reduced this to 3–5% in random order and 12–17% under the country shift, at mean FPRs of 0.06–0.07. At stable, well-sampled sites, therefore, a label-free prevalence-bounded quantile with the high-confidence option is sufficient.

The verified-positive rule helped mainly where label-free rules cannot. After a pre-specified upward drift of all scores by 0.5 logit, for example from a new kit lot, its alarm restored the FPR within two months, while the label-free rules stayed high (months 10–12: 0.086 vs 0.154; Figure 2B). At 10% prevalence, the prevalence-bounded rule became conservative (CRC sites: sensitivity 0.44 vs 0.52). And at MetaCardis, where the CRC test was applied to a cardiometabolic cohort, pooled recalibration kept the overall FPR at 0.095, but heart failure stayed at 0.21 and T2D at 0.14; running a local rule within recorded groups brought every group to 0.08–0.09 (Figure 2C), and the label-free rule did so as well as the verified-positive rule (post hoc; Table S11). Because comorbid CRC patients did not score higher (Table S8), per-group recalibration raises the cut-off and lowers sensitivity in over-flagged groups. The verified-positive rule costs one liberal first month, in which about 27% of people are referred, and it lowers sensitivity wherever the source cut-off had been too liberal: at the locked CRC sites it avoided 83 false-positive referrals per 1,000 people screened but missed 1.1 more cancers per 1,000 (sensitivity 0.52 vs 0.64). After a downward drift, all rules stayed too strict for the rest of the simulated period (post hoc; Table S2c).

## CONCLUSION

The specificity of a microbiome CRC test does not travel: it changes with the site and, in some settings, with the patients tested, through severe disease and oral-origin taxa or possibly through metformin (one cohort). Local recalibration is therefore needed. At stable, well-sampled sites a label-free local quantile with a prevalence bound, in its high-confidence form, suffices; a rule that uses only colonoscopy results of test-positive people adds recovery from large upward drift and robustness to higher prevalence. Both rules, and a site audit, are released as the open-source package cutoffguard. Our deployments were simulated from case-control cohorts with small control sets; the pilot had seen the three held-out CRC sites; colonoscopy was treated as a perfect reference; all rules stayed too strict after downward drift; and the medication findings rest mainly on one cohort. We recommend that microbiome test studies report the realised specificity at each external site and in major patient groups, check common medications, and plan local, outcome-based recalibration before deployment.

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

**Figure 1. Specificity of a fixed microbiome CRC test cut-off across sites and patient groups.** (A) Study design. (B) False-positive rate at each of 11 CRC sites (exact 95% CI) when the cut-off is set for 90% specificity on source cohorts (dashed line, target); development cohorts by leave-one-cohort-out (grey), locked external sites (black); circles, LASSO; squares, random forest; n, number of controls. IBD, T2D and adenoma sites are shown in Table S2. (C) Difference in CRC-test score (logit, LASSO, 95% CI) between condition groups and controls of the same cohort, fully adjusted: development cohorts (open) for age, BMI and sex; locked MetaCardis (filled circles) for sex, country and medications (PPI, metformin, statin, aspirin, beta-blocker; post hoc; progressive adjustment in Table S9); colonoscopy-negative controls with recorded cardiometabolic comorbidity vs healthy controls inside three CRC cohorts (diamond; site fixed effects, age, BMI, sex). (D) Species-level decomposition of score gaps into enriched oral-origin taxa (a priori genus list, Methods S5), depleted commensal fermenters and other taxa; development (cirrhosis, atherosclerotic disease) and locked MetaCardis (heart failure, T2D, and metformin users vs non-users within T2D, exploratory).

**Figure 2. Local recalibration restores the intended specificity; colonoscopy feedback helps under drift.** (A) True false-positive rate (top) and sensitivity (bottom) by month in simulated deployments at the 11 CRC sites (1% prevalence; two classifiers; 100 streams each; post hoc). Lines, means; band, 10th–90th percentile for verified-positive recalibration; dotted line, target. (B) Locked CRC, IBD and T2D sites after all scores shift by +0.5 logit from month 7 (pre-specified). (C) The CRC test applied at the locked MetaCardis site: false-positive rate by recorded condition (months 7–18, LASSO) for the source cut-off, pooled recalibration and per-group recalibration. (D) Without resampling (post hoc): share of months (≥3) with false-positive rate above 12%, measured on controls not yet seen, when each sample enters once (left bars: random order at Yachida 2019 [CRC test], MetaCardis and Qin 2012 [T2D test], 25 per month, 1% and 5% prevalence, 200 orders; right bars: MetaCardis controls entering country by country, 5% prevalence, all six country orders). Hatched, high-confidence versions (δ = 0.10), added after the locked analysis.
