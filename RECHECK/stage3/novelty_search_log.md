# Novelty search log — stage 3 hostile prior-art search

Date run: 2026-11-23 (all queries on this date). Searcher: automated agent (Claude), curl to public APIs + web search.

## Databases / channels used
- OpenAlex works API (`filter=title_and_abstract.search:`; sorted by relevance; top 10 inspected per query). OpenAlex indexes Crossref, PubMed, arXiv, bioRxiv/medRxiv, SSRN, Zenodo, OSF, IEEE/ACM/Springer/Elsevier/Wiley/T&F/OUP/Nature content, so it serves as the Google-Scholar-like layer over those publishers.
- arXiv API (`export.arxiv.org/api/query`, relevance sort, top 12) incl. 2025-2026 preprints.
- Crossref REST API (`/works/{doi}`) for DOI/metadata verification of every DOI row.
- arXiv API `id_list` for verification of every arXiv row.
- Europe PMC full-text XML (Wirbel 2019, PMC7984229) to verify the fixed-FPR analysis claim.
- Web search (general engine) for: microbiome threshold recalibration; unsupervised mixture-based threshold adaptation; patent search (Google Patents / USPTO); SSRN title check. Publisher/landing pages fetched: PMLR (Zhang 2013), ICLR virtual site (Gal 2025), Google Patents (US8934722B2).
- Not separately queried by native interface (no API access): IEEE Xplore, ACM DL, ScienceDirect, Springer, Wiley, T&F, Oxford Academic, Nature portal, Papers With Code, GitHub. Their content was reached through OpenAlex/Crossref indexing and web search; this is a limitation.

## Queries and hit counts
Counts = total matching records reported by the API (OpenAlex title+abstract search; arXiv all-field search). Top 10-12 of each were screened by title, promising ones by abstract.

| Source | Query | Hits |
|---|---|---|
| OpenAlex (title+abstract) | microbiome classifier decision threshold cohort | 2 |
| OpenAlex (title+abstract) | microbiome cross-cohort classifier specificity transfer | 9 |
| OpenAlex (title+abstract) | colorectal cancer metagenomic classifier leave-one-study-out | 3 |
| OpenAlex (title+abstract) | gut microbiome diagnostic false positive rate external validation | 1 |
| OpenAlex (title+abstract) | microbiome classifier calibration cohort | 11 |
| OpenAlex (title+abstract) | microbiome domain adaptation disease prediction | 6 |
| OpenAlex (title+abstract) | microbiome batch effect correction meta-analysis classifier | 0 |
| OpenAlex (title+abstract) | AI-readiness microbiome audit | 2 |
| OpenAlex (title+abstract) | indirect reference interval mixture model | 53 |
| OpenAlex (title+abstract) | refineR reference interval | 148 |
| OpenAlex (title+abstract) | kosmic reference interval | 36 |
| OpenAlex (title+abstract) | truncated maximum likelihood reference interval | 41 |
| OpenAlex (title+abstract) | label shift estimation black box | 61 |
| OpenAlex (title+abstract) | class prior estimation unlabeled EM | 2 |
| OpenAlex (title+abstract) | quantification learning prevalence estimation | 110 |
| OpenAlex (title+abstract) | threshold recalibration prior shift | 35 |
| OpenAlex (title+abstract) | unsupervised recalibration clinical prediction model | 8 |
| OpenAlex (title+abstract) | operating point transfer external validation | 287 |
| OpenAlex (title+abstract) | decision threshold transportability | 2354 |
| OpenAlex (title+abstract) | threshold shift new site classifier specificity | 48 |
| OpenAlex (title+abstract) | unsupervised prediction alignment performance drift | 16 |
| OpenAlex (title+abstract) | label shift adaptation expectation maximization prior | 5 |
| OpenAlex (title+abstract) | adjusting outputs of a classifier to new a priori probabilities | 8 |
| OpenAlex (title+abstract) | conformal prediction label shift | 233 |
| OpenAlex (title+abstract) | Neyman-Pearson classification label shift | 3 |
| OpenAlex (title+abstract) | false positive rate control distribution shift | 325 |
| OpenAlex (title+abstract) | calibration drift clinical prediction model | 257 |
| OpenAlex (title+abstract) | logistic recalibration model updating external validation | 58 |
| OpenAlex (title+abstract) | score normalization speaker verification | 308 |
| OpenAlex (title+abstract) | Z-norm T-norm score normalization | 45 |
| OpenAlex (title+abstract) | biometric score normalization unsupervised adaptation | 1 |
| OpenAlex (title+abstract) | anomaly detection threshold selection unlabeled | 7 |
| OpenAlex (title+abstract) | mixture model threshold selection unlabeled scores | 3 |
| OpenAlex (title+abstract) | two-component mixture classifier scores unlabeled test | 2 |
| OpenAlex (title+abstract) | test-time adaptation threshold | 2823 |
| OpenAlex (title+abstract) | fecal immunochemical test threshold positivity rate population | 60 |
| OpenAlex (title+abstract) | FIT cut-off sensitivity specificity across populations | 78 |
| OpenAlex (title+abstract) | meta-analysis fecal metagenomes colorectal cancer microbial signatures | 6 |
| OpenAlex (title+abstract) | metagenomic analysis colorectal cancer datasets cross-cohort | 15 |
| OpenAlex (title+abstract) | machine learning meta-analysis microbiome classification | 35 |
| OpenAlex (title+abstract) | meta-analysis gut microbiome studies disease-specific shared responses | 41 |
| OpenAlex (title+abstract) | gut microbiome health index | 1659 |
| OpenAlex (title+abstract) | MMUPHin meta-analysis microbiome | 2 |
| OpenAlex (title+abstract) | ConQuR batch effects microbiome | 2 |
| OpenAlex (title+abstract) | percentile normalization microbiome case-control | 2 |
| OpenAlex (title+abstract) | PLSDA-batch microbiome | 2 |
| OpenAlex (title+abstract) | curatedMetagenomicData | 34 |
| OpenAlex (title+abstract) | SIAMCAT machine learning microbiome | 9 |
| OpenAlex (title+abstract) | generalizability microbiome classifier external cohorts | 10 |
| OpenAlex (title+abstract) | prevalence shift medical image deployment | 59 |
| OpenAlex (title+abstract) | domain adaptation under target and conditional shift | 185 |
| OpenAlex (title+abstract) | maximum likelihood bias-corrected calibration label shift | 6 |
| OpenAlex (title+abstract) | distribution-free uncertainty quantification label shift | 56 |
| OpenAlex (title+abstract) | conformal prediction under covariate shift weighted | 54 |
| OpenAlex (title+abstract) | updating methods clinical prediction models | 2871 |
| OpenAlex (title+abstract) | calibration hierarchy | 7164 |
| OpenAlex (title+abstract) | reference limits mixed population Hoffmann method | 13 |
| OpenAlex (title+abstract) | Bhattacharya method reference interval | 77 |
| OpenAlex (title+abstract) | estimating ROC curve without gold standard mixture model | 4 |
| OpenAlex (title+abstract) | sensitivity specificity estimation without gold standard finite mixture | 0 |
| OpenAlex (title+abstract) | predicting out-of-distribution performance unlabeled data confidence threshold | 4 |
| OpenAlex (title+abstract) | unsupervised performance estimation deployed classifier label shift | 1 |
| OpenAlex (title+abstract) | location-scale transformation class conditional domain adaptation | 0 |
| OpenAlex (title+abstract) | Neyman-Pearson classification covariate shift | 2 |
| OpenAlex (title+abstract) | Neyman-Pearson umbrella algorithm | 13 |
| OpenAlex (title+abstract) | specificity drift external validation cancer screening AI | 6 |
| OpenAlex (title+abstract) | threshold adjustment new hospital deployment unlabeled | 0 |
| OpenAlex (title+abstract) | site-specific threshold calibration multi-site | 149 |
| OpenAlex (title+abstract) | prevalence adjustment positive predictive value deployment threshold | 15 |
| OpenAlex (title+abstract) | quantification adjusted classify and count | 164 |
| OpenAlex (title+abstract) | histogram matching score distribution alignment recalibration | 0 |
| OpenAlex (title+abstract) | microbiome prediction model external validation calibration threshold | 7 |
| OpenAlex (title+abstract) | stool metagenomic colorectal cancer screening specificity | 21 |
| OpenAlex (title+abstract) | multi-cohort gut microbiome colorectal adenoma classifier validation | 2 |
| OpenAlex (title+abstract) | microbiome transfer learning cross-cohort disease classification | 11 |
| OpenAlex (title+abstract) | microbiome classifier batch effect prediction performance cross-study | 0 |
| OpenAlex (title+abstract) | unsupervised score calibration speaker recognition | 8 |
| OpenAlex (title+abstract) | generative modelling unsupervised score calibration | 25 |
| OpenAlex (title+abstract) | unsupervised calibration domain mismatch speaker verification | 1 |
| OpenAlex (title+abstract) | adaptive score normalization speaker verification domain | 9 |
| OpenAlex (title+abstract) | face verification threshold domain shift unlabeled | 1 |
| OpenAlex (title+abstract) | estimating error rates unlabeled data mixture scores | 3 |
| OpenAlex (title+abstract) | semi-supervised class prior estimation mixture proportion | 1 |
| OpenAlex (title+abstract) | mixture proportion estimation | 1246 |
| OpenAlex (title+abstract) | positive-unlabeled learning class prior estimation | 48 |
| OpenAlex (title+abstract) | label shift medical prevalence diagnostic test adaptation | 4 |
| OpenAlex (title+abstract) | Saerens adjusting outputs classifier new a priori probabilities | 0 |
| OpenAlex (title+abstract) | EM algorithm prior probability shift calibration | 0 |
| OpenAlex (title+abstract) | risk control conformal false positive rate guarantee classification threshold | 1 |
| OpenAlex (title+abstract) | learn then test risk control | 4932 |
| OpenAlex (title+abstract) | dataset shift clinical machine learning | 1649 |
| OpenAlex (title+abstract) | external validation heterogeneity prediction models multicenter | 461 |
| OpenAlex (title+abstract) | cross-domain alignment of decision thresholds electronic health records | 5 |
| OpenAlex (title+abstract) | unlabeled target decision threshold alignment clinical | 4 |
| OpenAlex (title+abstract) | threshold adaptation unlabeled target domain medical classifier | 0 |
| OpenAlex (title+abstract) | microbiome specificity false positive cohort heterogeneity colorectal | 2 |
| arXiv API | all:"label shift" AND all:threshold | total ['15'] |
| arXiv API | all:microbiome AND all:threshold AND all:cohort | total ['1'] |
| arXiv API | all:"operating point" AND all:shift AND all:unlabeled | total ['1'] |
| arXiv API | all:"score normalization" AND all:unsupervised | total ['6'] |
| arXiv API | all:"Neyman-Pearson" AND all:shift | total ['11'] |
| arXiv API | all:"decision threshold" AND all:"distribution shift" | total ['9'] |
| arXiv API | all:microbiome AND all:"domain adaptation" | total ['1'] |
| Web search | microbiome classifier decision threshold specificity new cohort recalibration unlabeled | 10 shown; none on label-free threshold re-estimation for microbiome |
| Web search | unsupervised threshold adaptation new site mixture model classifier scores linear shift maximum likelihood unlabeled target | 10 shown; GMM-threshold papers in object detection/open-set DA only |
| Web search | "Threshold Transportability and Post-Training Threshold Adaptation in Clinical Tabular AI" | led to arXiv 2511.18030 and ICLR 2025 Gal et al. |
| Web search (patents) | patent adjusting classifier decision threshold deployment site unlabeled score distribution mixture model specificity | US8934722B2 (Given Imaging), US9031897 (reweighting, not thresholds) |

Notes on noise: OpenAlex full-text-style matching returns many irrelevant hits for broad queries (e.g. "test-time adaptation threshold" 2,823; "decision threshold transportability" 2,354); only top-ranked records were screened. Several highly relevant items are very recent (2025-2026) grey literature (SSRN, Zenodo, OSF, bioRxiv) — included because they are close, flagged as such.

## Result
85 verified rows written to `novelty_map.csv` (closeness 0-5). Two rows lack a DOI and are marked UNVERIFIED in the doi column (Zhang 2013 ICML — PMLR proceedings, verified via OpenAlex + PMLR page; Gal 2025 ICLR — verified via ICLR virtual page only). Two SSRN rows (Chakraborty 2026, Promjiraprawat 2026) are verified by Crossref metadata but their abstracts were not retrievable, so their content claims rest on the title only.

## CLOSE-CALL section

### (i) Papers studying threshold / operating-point transfer of microbiome classifiers
1. **Wirbel et al. 2019, Nat Med (10.1038/s41591-019-0406-6).** Verified in full text: LOSO CRC models "calibrated to have a false-positive rate (FPR) of 0.1" on training controls; realised FPR then measured on *other-disease* cohorts to test disease specificity. So fixed-operating-point evaluation of cross-cohort microbiome classifiers is not new per se. **What remains new:** Wirbel did not quantify the cohort-to-cohort dispersion of realised specificity on held-out CRC cohorts' own controls, did not test it against binomial noise (overdispersion), did not frame threshold non-transfer as a failure distinct from AUROC transfer, and did not re-estimate thresholds. Our (a) must cite this and be framed as an extension.
2. **Zhang et al. 2026, CRC-TrustBench, Front Microbiol (10.3389/fmicb.2026.1971707).** LOSO/LOCO CRC metagenomic benchmark (15 studies) with Platt calibration, conformal-style coverage and abstention "evaluated without outer-test labels"; finds conformal coverage falls below targets. **Overlap:** shows probability-reliability non-transfer in exactly our data type. **What remains new:** no fixed-specificity realised FPR/sensitivity per cohort, no outcomes per 1,000, no label-free target-score threshold re-estimation (their methods are calibrated on source data).
3. **Gupta 2020 GMHI / Chang 2024 GMWI2** apply one universal fixed cut-off across cohorts but do not analyse its per-cohort drift. **Shi 2026 (oral, bioRxiv)**, **Li 2023 (20 diseases)**, **Li 2025 (best practices)**, **Piccinno 2025**, **Kubinski 2022**, **Tower 2026 (Zenodo; label-free predictor of AUC gap)** all evaluate transport with AUROC only.
4. No paper found that re-estimates a microbiome classifier's decision threshold at a new cohort from unlabeled samples. Nothing found on Papers-with-Code/GitHub-indexed work either (searched via web).

### (ii) Decision threshold / reference limit estimated from unlabeled mixed target data with a parametric shift + mixture model
1. **Indirect reference-interval methods, lab medicine** — Arzideh 2007 (TML precursor, 10.1515/CCLM.2007.250), Zierk 2020 kosmic (10.1038/s41598-020-58749-2), Ammer 2021 refineR (10.1038/s41598-021-95301-2), Hoffmann 2024 GMM verification (10.1515/labmed-2024-0118), Hepp 2022 MDN (10.1186/s12859-022-04846-0), Hoffmann 2026 review, RIbench 2022. These estimate the healthy-population quantile (i.e., a cut-off with a target specificity of 97.5%) from unlabeled mixed routine data with a parametric (Box-Cox/power-normal) healthy component, and Hoffmann explicitly uses this to *verify a transferred limit at a local laboratory*. **This is the same core idea as (b)**: set a fixed-specificity threshold at a new site from unlabeled healthy+diseased data via a mixture. **What remains new for us:** (1) the variable is a learned classifier score rather than an analyte; (2) class-shape information is transported from a labelled source cohort and linked to the target through a site-shift map a+b·s (semi-parametric), instead of an assumed parametric healthy family with no source; (3) the disease component is also modelled (transported), giving the target prevalence and sensitivity as by-products; (4) head-to-head comparison with EM prior adjustment and few-control conformal thresholds on real multi-cohort data. These are incremental, application-level differences; the paper must cite this literature as the direct conceptual precedent.
2. **Unsupervised score calibration, speaker verification** — Brümmer & Garcia-Romero 2014 (10.1109/icassp.2014.6853884): 2-component GMM fitted to unlabeled trial scores to calibrate accept/reject decisions; Cumani 2019 (Interspeech) and Cumani 2021 TASLP (10.1109/taslp.2020.3040103): non-Gaussian generative score mixtures for unsupervised linear calibration. Z-norm/T-norm (Auckenthaler 2000) apply affine score maps from known-negative cohorts. **This is essentially (b) in another field**: maximum-likelihood fit of a two-class mixture to unlabeled scores yields an affine (linear) calibration. **What remains new:** use of empirical source class shapes rather than parametric families; explicit fixed-FPR operating-point target rather than LLR calibration; biomedical multi-cohort validation and comparison against label-shift EM and conformal baselines.
3. **Label-shift / generalized target shift, ML** — Saerens 2002 EM, Alexandari 2020, Lipton 2018, Garg 2020: prior-only (class conditionals fixed) so they cannot move FPR at a fixed cut-off. **Zhang et al. 2013 (ICML)**: generalized target shift with location-scale transformation of class-conditionals plus prior change, estimated from unlabeled target — the closest ML formalism to our a+b·s model (in feature space via kernel mean matching). **What remains new:** score-level 1-D likelihood estimator aimed at an operating point; otherwise the modelling assumption is anticipated.
4. **Label-free operating-point correction, medical AI** — **Roschewitz 2023 Nat Commun (UPA)**: shows sensitivity/specificity drift under acquisition shift even when AUROC generalises and corrects it label-free by aligning target score distribution to source. This anticipates both the *framing of (a)* (operating-point failure distinct from AUROC) and the *goal of (b)*. **What remains new:** UPA assumes unchanged prevalence (whole-CDF alignment conflates prevalence change with score shift); our mixture separates them. Microbiome domain is new. **Qiu, Zhao, Zheng 2026 Biometrics (SACSIM)**: adapts Neyman-Pearson (FPR-constrained) rules to a target population using a small unlabeled target sample plus auxiliary information — same aim as (b) in biostatistics, different model (single-index covariate model). **Godau 2023/2025**: label-free prevalence-aware threshold adjustment (prior shift only). **Gal 2025 ICLR**: label-free cross-domain threshold alignment for EHR via representation learning. **Kalan 2025**: NP transfer with both null and alternative shift (needs target labels). **Li 2026 Mathematics**: theory showing fixed cut-off keeps FPR under pure prior shift — our empirical finding that FPR does not transport contradicts the pure-prior-shift assumption and is consistent with conditional shift.
5. **Patent US8934722B2 (Peleg & Krupnik, Given Imaging, 2015)**: claims adjusting classifier thresholds to conform to a received set of unlabeled images. Relevant if any patent claim is contemplated for (b); generic, no mixture model.

### Honest bottom line per contribution
- (a) Operating-point non-transfer as distinct from AUROC: **anticipated generically** (Roschewitz 2023; Shahid 2026 site-wise conformal violation; Promjiraprawat 2026; Chakraborty 2026; FIT literature) and **partially in microbiome** (Wirbel 2019 fixed-FPR cut-off, CRC-TrustBench 2026 calibration/coverage). Not found: a systematic quantification of realised specificity dispersion across held-out microbiome cohorts with an overdispersion test, across diseases. Remains new, but as a domain-specific empirical contribution.
- (b) Label-free threshold re-estimation via affine site-shift mixture: **the core idea exists in other fields** (indirect reference intervals; unsupervised score calibration in speaker verification; GeTarS location-scale; UPA; SACSIM). Remaining novelty is the specific semi-parametric variant (source-transported empirical class shapes + affine shift + prior, by ML), its application to microbiome classifiers, and the head-to-head benchmark. Claim it as an adaptation/benchmark, not a new method class.
- (c) Evaluation protocol (realised FPR/sensitivity at fixed operating point, outcomes per 1,000 screened): per-1,000 reporting is standard in diagnostic-accuracy/GRADE practice and fixed-threshold reporting is standard in clinical validation; **new only as a recommendation for microbiome ML benchmarks**, where we found no paper adopting it.
