# Novelty / prior-art search log: operating-point drift of gut-microbiome classifiers

Search date: **2026-11-23** (all queries). Companion table: `novelty_map.csv` (50 rows. 49 checked against the record, abstract or full text; one, the MICCAI 2023 Godau paper, has only its record checked, as noted in its row).

Sources: OpenAlex API (`api.openalex.org/works?search=`), PubMed E-utilities (esearch/esummary/efetch), arXiv API (`export.arxiv.org/api/query`), WebSearch (extended/standard), and WebFetch of PMC full texts.
Europe PMC and the NCBI ID converter returned errors from this sandbox. ScienceDirect was not used (blocked).
"Hits" means the total the engine reported. OpenAlex totals are full-text relevance counts, so they are inflated, and only the top 8 hits were screened per query.

## 1. Queries run

### Cluster 1: threshold / operating-point transfer and specificity drift
| # | Source | Query | Hits | Relevant finds |
|---|---|---|---|---|
| 1 | OpenAlex | microbiome classifier threshold specificity cross-cohort | 10,447 | Shi 2026 bioRxiv (OSCC transportability); Chakravarthy 2026 (AD LOCO); Duvallet 2017 |
| 2 | OpenAlex | microbiome classifier decision threshold transfer cohorts | 3,307 | same as above; nothing on thresholds |
| 3 | OpenAlex | operating point drift classifier external validation sites | 21,420 | generic calibration-drift papers only |
| 4 | WebSearch (ext.) | gut microbiome classifier fixed threshold specificity varies across cohorts colorectal cancer external validation | 10 links | Wang X 2026 AJTR narrative review ("cut-off must be fixed ... without retuning"); no study measuring cross-cohort specificity at a fixed cutoff |
| 5 | WebSearch (ext.) | site-specific decision threshold recalibration AI model unlabeled data target false positive rate deployment | 9 links | PU-learning ROC recovery (Jain 2017); nothing established |
| 6 | PubMed | microbiome[tiab] AND (classifier OR "machine learning") AND (threshold OR cutoff OR "cut-off") AND (cohort* OR "external validation") AND specificity[tiab] | 4 | none relevant |
| 7 | PubMed | microbiome[tiab] AND "operating point" | 1 | none relevant |
| 8 | PubMed | microbiome[tiab] AND (classifier OR "machine learning") AND (recalibration OR calibration[tiab]) AND (cohort OR study) AND transfer* | **0** | none: a gap in the literature |
| 9 | PubMed | ("decision threshold" OR "classification threshold") AND (recalibrat* OR local OR site*) AND ("external validation" OR deployment) AND machine learning | 7 | none relevant |
| 10 | arXiv | abs:label AND abs:shift AND abs:threshold AND abs:unlabeled | 33 | **Zhou & Wang 2026** (threshold-transfer audit, speech deepfakes); **Yilmaz & Heckel 2022**; Garg 2022 ATC; Asiaee 2026 |
| 11 | arXiv | "operating point" AND "distribution shift" AND unlabeled (phrase) | 0 | n/a |
| 12 | WebSearch | Roschewitz Glocker automatic correction of performance drift ... unsupervised prediction alignment | 10 links | **Roschewitz 2023 Nat Commun (UPA)**: PMC full text read |

### Cluster 2: cross-cohort microbiome meta-analyses
| # | Source | Query | Hits | Relevant finds |
|---|---|---|---|---|
| 13 | OpenAlex | colorectal cancer metagenome classifier specificity cohort leave-one-cohort-out | 374 | Wirbel 2019, Thomas 2019, Dai 2018, Wu 2021, Mei 2024 |
| 14 | OpenAlex | gut microbiome cross-cohort meta-analysis colorectal cancer signatures | 9,620 | Thomas 2019, Wirbel 2019 |
| 15 | PubMed | metagenom*[tiab] AND colorectal AND "leave-one-study-out" OR "leave-one-cohort-out" AND colorectal | 3 | **CRC-TrustBench 2026** (Front Microbiol) |
| 16 | OpenAlex | Piccinno colorectal cancer metagenomes cohorts | 5 shown | Piccinno 2025 Nat Med (18 cohorts) |
| 17 | OpenAlex | machine learning meta-analysis metagenomics Pasolli 2016 PLoS Computational Biology | 565 | Pasolli 2016 |
| 18 | OpenAlex | SIAMCAT machine learning microbiome | 237 | Wirbel 2021 Genome Biol |
| 19 | OpenAlex | curatedMetagenomicData / Accessible, curated metagenomic data through ExperimentHub | 281 / 404 | Pasolli 2017 Nat Methods (data source) |
| 20 | WebFetch (PMC7984229) | Wirbel 2019 full text: thresholds/FPR | n/a | cutoff set to **FPR 0.1 on training controls**; FPR on other diseases 0.09-0.13; study-to-study FPR in Fig. 3 (figure only) |
| 21 | WebFetch (PMC9533319) | Thomas 2019 full text | n/a | AUC only for LODO; sens/spec only vs FOBT over many thresholds |
| 22 | WebFetch (PMC12283368) | Piccinno 2025 full text | n/a | AUC only (LODO 0.71-0.97) |
| 23 | WebFetch (PMC13650428) | CRC-TrustBench full text | n/a | fixed 0.5 threshold; Platt fitted on internal partition; no per-cohort specificity, no target-site re-thresholding |
| 24 | OpenAlex | microbiome ML universal signature specificity ... / fecal metagenomic classifier combined FIT ... | 417 / 419 | Kartal 2022 Gut (high-specificity PDAC signature) |

### Cluster 3: batch-effect correction for prediction
| # | Source | Query | Hits | Relevant finds |
|---|---|---|---|---|
| 25 | OpenAlex | batch effect microbiome prediction cross-study | 12,512 | ConQuR 2022, **DEBIAS-M 2025**, PLSDA-batch 2023 |
| 26 | OpenAlex | MMUPHin meta-analysis microbiome | 180 | Ma 2022 Genome Biol |
| 27 | OpenAlex | percentile normalization case-control microbiome | 4,766 | Gibbons 2018 |
| 28 | OpenAlex | Managing batch effects in microbiome data (Wang Le Cao) | 14,942 | Wang & Le Cao 2020; Foxx & Rivers 2025 iMetaOmics |
| 29 | OpenAlex | domain adaptation microbiome disease prediction cross-study | 13,389 | DEBIAS-M; "leveraging scheme" 2023 |
| 30 | PubMed | DEBIAS-M | 2 | preprint + Nat Microbiol 2025 |

None of these methods evaluates the operating point; all report AUC or association power.

### Cluster 4: label shift, unsupervised threshold adaptation, conformal/NP, clinical updating
| # | Source | Query | Hits | Relevant finds |
|---|---|---|---|---|
| 31 | OpenAlex | label shift estimation unlabeled target prior adjustment | 17,774 | Garg 2020, Lipton 2018 |
| 32 | OpenAlex | EM algorithm adjusting outputs classifier new a priori probabilities | 7,303 | Saerens 2002 |
| 33 | OpenAlex | Maximum likelihood with bias-corrected calibration ... label shift | 844 | Alexandari 2020; LaSCal 2024 |
| 34 | OpenAlex | Deployment of image analysis algorithms under prevalence shifts | 45,374 | **Godau 2023 MICCAI / 2025 MedIA** |
| 35 | PubMed | ("label shift" OR "prior shift" OR "prevalence shift") AND (classifier OR "machine learning") | 20 | Godau 2025; "Mind your prevalence!" 2024 |
| 36 | OpenAlex | unsupervised threshold adaptation target false positive rate | 31,602 | off-topic (object detection) |
| 37 | OpenAlex | threshold selection under prior shift unlabeled | 24,835 | PU-learning prior shift papers; Garg 2022 ATC |
| 38 | OpenAlex | conformal prediction covariate shift | 16,155 | Tibshirani 2019 |
| 39 | OpenAlex | Distribution-free uncertainty quantification for classification under label shift | 96,249 | Podkopaev & Ramdas 2021 |
| 40 | OpenAlex | conformal Neyman-Pearson false positive rate guarantee calibration set | 196 | conformal selection; Angelopoulos & Bates intro |
| 41 | OpenAlex | Testing for outliers with conformal p-values | 88,859 | Bates 2023 Ann Stat |
| 42 | OpenAlex | Neyman-Pearson classification threshold order statistic | 3,603 | **Tong 2018 Sci Adv (NP umbrella)** |
| 43 | arXiv | abs:Neyman AND abs:Pearson AND abs:shift | 12 | **Kalan 2025** (NP under null+alternative shift); Scott 2018 |
| 44 | arXiv | "Neyman-Pearson" AND "label shift" / "Neyman-Pearson" AND "domain adaptation" | 0 / 1 | Scott 2018 |
| 45 | WebSearch | estimating ROC curve without gold standard mixture model unlabeled test scores | 10 links | Henkelman 1990; ssROC 2023; Jain 2017 PU |
| 46 | OpenAlex | Exact prevalence regions finite-sample | 20,608 | Hosseini 2026 |
| 47 | OpenAlex | clinical prediction model updating recalibration new setting | 10,130 | Janssen 2008; Binuya 2022; Davis 2020 calibration drift |
| 48 | OpenAlex | calibration prediction models Van Calster hierarchy | 2,239 | Van Calster 2016, Huang 2020 tutorial |
| 49 | OpenAlex | Minimum sample size for external validation ... binary outcome | 37,495 | Riley 2021; Riley 2024 BMJ series |
| 50 | OpenAlex | External validation ... big datasets heterogeneity | 24,534 | Riley 2016; Van Calster 2023; Sperrin 2022 |
| 51 | OpenAlex | Variation of a test's sensitivity and specificity with disease prevalence | 575,965 | Leeflang 2013 CMAJ; Brenner & Gefeller 1997 |

### Cluster 5: clinical-lab local cut-off practice
| # | Source | Query | Hits | Relevant finds |
|---|---|---|---|---|
| 52 | OpenAlex | reference interval verification 20 samples local population | 338,796 | Ozarda 2018 CCLM; Tate 2015 Clin Chem |
| 53 | PubMed | "reference interval" AND (verification OR transference) AND CLSI | 39 | CALIPER; transference studies |
| 54 | OpenAlex | FIT cut-off positivity rate countries colorectal screening | 5,265 | country-specific FIT cut-off papers |
| 55 | OpenAlex | Effect of sex age and positivity threshold on FIT accuracy | 803 | Selby 2019 Gastro; Selby 2018 Ann Intern Med; JNCI 2025 |
| 56 | OpenAlex | faecal immunochemical test positivity rate variation screening programmes Europe | 1,214 | guidelines, programme reports |
| 57 | OpenAlex | multitarget stool DNA test specificity | 2,358 | Imperiale 2014/2024 NEJM (context, not tabulated) |

### Cluster 6: iMeta and recent microbiome papers (2023-2026)
| # | Source | Query | Hits | Relevant finds |
|---|---|---|---|---|
| 58 | OpenAlex (filter ISSN 2770-596X = iMeta) | machine learning cohort diagnostic | 25 | Degregori 2026 AI-readiness audit; Geng 2024 periodontitis signature |
| 59 | OpenAlex (iMeta) | classifier validation / colorectal cancer microbiome / batch effect / generalization | 69 / 76 / 66 / 9 | nothing on thresholds or operating points |
| 60 | PubMed | gut microbiome AND colorectal cancer AND diagnostic AND iMeta[journal] | 1 | not relevant |
| 61 | OpenAlex | microbiome machine learning generalization across populations iMeta | 85 | none relevant |

**Bottom line from searching:** no paper in iMeta, or any microbiome paper found, tabulates realised specificity per held-out cohort at a pre-fixed cutoff, tests whether it is overdispersed, or proposes a site-level re-thresholding rule. The closest microbiome papers are Wirbel 2019 (it used a training-set FPR=0.1 cutoff) and CRC-TrustBench 2026 (calibration and conformal under LOSO). Outside microbiome, the methodological pieces all exist.

---

## 2. Closest prior work (top 5)

1. **Roschewitz et al. 2023, Nat Commun, "Automatic correction of performance drift under acquisition shift" (UPA).**
   - Label-free CDF matching of target scores to the reference score distribution restores the intended sensitivity/specificity, with 250-1000 unlabeled cases.
   - This is our "local quantile" candidate, already published in a high-profile journal.
   - Its stated limitation is our opening: it *assumes prevalence is preserved*, and microbiome cohorts vary hugely in case:control ratio.
2. **Wirbel et al. 2019, Nat Med** (plus Wirbel 2021 SIAMCAT).
   - Same microbiome setting and the same operating-point design: the cutoff is fixed at FPR=0.1 on training controls and FPR is reported on transferred cohorts and other diseases.
   - What they did not do: tabulate per-cohort specificity on held-out CRC controls, test overdispersion, or offer a site-level remedy.
   - An editor familiar with the field will say "Wirbel already reported FPR at 10%". We must show what is new beyond that.
3. **Godau et al. 2025, MedIA (and MICCAI 2023), "Navigating prevalence shifts".**
   - Estimates deployment prevalence from unlabeled data, then adjusts calibration and decision threshold without annotations, across 30 tasks.
   - This is our "EM label-shift prior adjustment then re-threshold" workflow, in imaging.
4. **Tong, Feng & Li 2018, Sci Adv (NP umbrella), with Bates et al. 2023, Ann Stat (conformal outlier p-values).**
   - An order statistic of n held-out class-0 scores gives a threshold with P(FPR > alpha) <= delta. The minimum is n >= log(delta)/log(1-alpha), i.e. **29 controls for 90% specificity at 95% confidence**.
   - Bates 2023 adds calibration-conditional FPR bounds.
   - This is exactly our "conformal/order-statistic threshold from n local controls". Method novelty for it is zero.
5. **Zhou & Wang 2026, arXiv, "When EER hides deployment failure"** (plus Yilmaz & Heckel 2022, unlabeled conformal-threshold prediction).
   - Same thesis in another field: discrimination metrics (EER, which plays the role AUROC plays for us) hide transferred-threshold failure.
   - It proves monotone score transforms cannot fix discrimination, and shows label-free corrections collapse at extreme or unknown priors.
   - This pre-empts the framing and is a direct warning for our site-shift mixture model.

Runners-up: CRC-TrustBench 2026 (microbiome, LOSO calibration and conformal coverage failure); Kalan 2025 (NP transfer under shift of both classes); Saerens 2002 / Alexandari 2020 (EM/MLLS); Van Calster 2023 ("no such thing as a validated model": heterogeneity across sites is expected); Leeflang 2013 (specificity varies with setting); Ozarda 2018 / CLSI EP28 (local verification with about 20 samples).

---

## 3. Novelty verdict

**Already done (do not claim):**
- *Thresholds drift across sites.* This is established in general clinical prediction (Van Calster 2023, Leeflang 2013), imaging (Roschewitz 2023, Godau 2025) and speech (Zhou 2026). In microbiome, Wirbel 2019/2021 already used training-calibrated FPR cutoffs and noted specificity loss under naive transfer.
- *Label-free re-thresholding by quantile/CDF matching* (UPA) and *by EM prior estimation* (Saerens; Alexandari; Godau).
- *Finite-sample FPR control from n controls* (NP umbrella; conformal outlier testing), and the lab-medicine practice of verifying a cut-off with about 20 local reference samples (CLSI EP28).
- *Per-1,000-screened harm translation*: standard in FIT threshold work (Selby 2018/2019).

**Genuinely new (defensible):**
1. **Microbiome-specific evidence:** the first systematic per-cohort table of realised specificity at a pre-fixed 90%-specificity cutoff across curatedMetagenomicData CRC/adenoma/IBD/T2D LOCO splits, with a formal overdispersion test (beta-binomial / random-effects tau^2 against binomial). None of the AUC-only meta-analyses report this (Thomas 2019, Piccinno 2025, Pasolli 2016, CRC-TrustBench), and Wirbel shows FPR only in figures and not per held-out cohort's own controls.
2. **A head-to-head benchmark in small, case-control-enriched cohorts** of UPA-style quantile, EM/MLLS, a location-scale "site-shift mixture", and the NP/conformal n-control threshold.
   - This is where existing methods have not been tested, and where their assumptions are violated in opposite directions: UPA assumes equal prevalence; EM assumes no p(x|y) shift.
   - A pure label shift cannot change FPR at all. So **observed specificity drift is itself evidence of class-conditional (site) shift, which defeats EM-only correction.** This is a crisp, publishable logical point for this audience.
3. **The site-shift mixture model** (target score = a + b * source score with transported class shapes, ML fit on unlabeled scores). This is a mild extension of Henkelman-type mixture ROC and "generalized label shift".
   - It is new as a named tool, but its identifiability is fragile (Garg 2022's impossibility result; Zhou 2026's failures at extreme priors).
   - Expect it to work only with moderate prevalence and clear bimodality. Report its failures honestly.

**Risk that an editor says "just recalibrate": high for contribution 2 framed as a method paper, moderate overall.**
- Mitigations: (i) frame the paper as a *reporting/protocol* problem plus *evidence*, not a new algorithm; (ii) state explicitly why recalibration (Janssen 2008; Van Calster 2019) needs labelled local cases *and* controls, while screening sites can collect controls (colonoscopy-negative) or unlabeled samples cheaply; (iii) show that label-free guarantees are impossible without a shift assumption, and present the n-control rule as the only assumption-light option, giving the minimum n and the realised-specificity distribution after the fix.
- Also cite the AJTR 2026 review's "never retune" stance and reconcile it: fix the threshold-*setting rule* (pre-specified local verification), not the threshold *value*.

**A better angle I spotted: a prevalence bound plus a local-verification protocol.**
- In true screening, prevalence pi of the target condition is low: CRC about 0.5-1%, advanced neoplasia about 5-10%.
- Setting the threshold at the (1-alpha) quantile of *unlabeled* screening samples gives FPR = (alpha - pi*TPR)/(1-pi). That lies in [(alpha-pi)/(1-pi), alpha/(1-pi)], a distribution-free bound with no shift model needed.
- So in low-prevalence screening, the "local unlabeled quantile" is nearly exact. In case-control cMD cohorts (pi about 0.5) it is badly biased, which explains why UPA-like methods look poor in curated data and assume equal prevalence.
- I did not find this bound stated in the microbiome or UPA literature (it is elementary, so it may be folklore in the quantification literature). Combined with the n=29/59-controls NP rule and a CLSI-EP28-style verification protocol, it gives a short, practical, iMeta-suited message: "Report specificity at a fixed cutoff per cohort; at deployment, re-set the cutoff with either >=29 colonoscopy-negative local controls (exact guarantee) or >=N unlabeled screening samples (bounded error when pi is small)."

---

## 4. Novelty scorecard (1 = weak, 5 = strong)

| Contribution | Novelty | Practical value | Evidence strength (current) | One-line reasons |
|---|---|---|---|---|
| C1. Quantify operating-point drift across cohorts as a reporting/protocol gap | **3** | **4** | **3** | Novelty: not reported per cohort in any microbiome meta-analysis, but the concept is known (Wirbel 2019, Van Calster 2023, Leeflang 2013). Value: directly matters for screening referrals. Evidence: the range 0.72-1.00 is suggestive, but cohort control n is small (about 20-60), so the overdispersion claim needs a beta-binomial test and per-disease replication. |
| C2a. Label-free re-thresholding (local quantile / EM prior / site-shift mixture) | **2** | **3** | **2** | Novelty: UPA (quantile) and Godau (EM + threshold) already exist, and the mixture model is a modest extension. Value: useful only with assumptions that are hard to check. Evidence: identifiability is fragile at small n and extreme priors (Garg 2022, Zhou 2026), and no guarantee is possible without a shift model. |
| C2b. Few-labelled-local-controls threshold with FPR guarantee (NP / conformal order statistic) | **2** (method) / **4** (in microbiome) | **5** | **4** | Novelty: the method is textbook (Tong 2018, Bates 2023), but no one has applied it to microbiome tests. Value: an exact, assumption-light guarantee with a simple n rule (29 controls for 90% spec at 95% confidence). Evidence: guaranteed by theory, and easy to demonstrate empirically on held-out cMD controls. |
| C3. Translate to unnecessary colonoscopies / missed cancers per 1,000 screened | **2** | **4** | **3** | Novelty: standard in FIT/DTA work (Selby 2018/2019). Value: makes the result legible to clinicians and editors. Evidence: depends on an assumed screening prevalence and on case-control sensitivity, so it is a scenario analysis, not observed data. |
| C4 (suggested). Prevalence bound for unlabeled-quantile thresholds plus an EP28-style local-verification protocol | **3-4** | **5** | **3** | Novelty: no microbiome or UPA paper found stating it (the bound is elementary, so check the quantification literature before claiming it). Value: explains when label-free methods work (low-prevalence screening) and when they fail (case-control data), giving an actionable protocol. Evidence: provable and checkable by simulation and cMD resampling. |
| C5 (suggested). "Specificity drift implies class-conditional shift" diagnostic (FPR is invariant under pure label shift) | **3** | **3** | **4** | Novelty: known in ML theory (Lipton 2018; Asiaee 2026) but never used as a diagnostic in microbiome. Value: tells users that EM/prevalence correction cannot fix what they observe. Evidence: logically exact, and the drift data provide the empirical test. |

**Overall recommendation:**
- Position the paper as a Short Communication on *evidence + protocol*: C1 + C5 + C2b + C4, with C3 as an illustration.
- Present the label-free methods (C2a) as benchmarked baselines with honest failure modes, not as the headline method.
- Run DEBIAS-M / MMUPHin as "fix-the-features" baselines, to pre-empt the reviewer question "doesn't batch correction solve this?".
- Cite and distinguish UPA, Godau, Wirbel 2019, the NP umbrella and Zhou 2026 explicitly in the introduction.

## 5. Caveats on this search
- ScienceDirect and Europe PMC were not reachable, and Google Scholar was not used. Conference proceedings (MICCAI/ICML/NeurIPS) were checked only through OpenAlex/arXiv.
- CLSI EP28-A3c itself (paywalled standard) was not opened. The 120-establish / 20-verify figures are the standard's widely cited numbers, cited via Ozarda 2018.
- Four items are preprints (Shi 2026 bioRxiv; Zhou 2026, Kalan 2025 and Asiaee 2026 on arXiv) and may change.
- Full texts of Wirbel 2019, Thomas 2019, Piccinno 2025 and CRC-TrustBench were read only up to the first 100k characters. Supplementary tables were not inspected, so per-cohort specificity could exist in a supplement. Check the Wirbel 2019 Extended Data and the CRC-TrustBench supplement before claiming "never reported".
