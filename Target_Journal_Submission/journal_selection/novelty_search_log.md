# STEP 3 - Novelty search log (label-free operating-point transfer for microbiome classifiers)

Search date: 2026-11-24 (all queries). Companion table: `novelty_map.csv` (76 rows; every DOI resolved via
Crossref `api.crossref.org/works/{doi}` or, for arXiv/DataCite DOIs, OpenAlex `api.openalex.org/works/doi:{doi}`;
0 UNVERIFIED). Tools: OpenAlex search API, Crossref bibliographic query, arXiv export API, PubMed E-utilities.
WebSearch/Google Scholar was not used. OpenAlex hit counts are full-text relevance matches, so large counts mean
"loose match", not that many papers are relevant. The top 12 results per query were screened by title, and abstracts
were read for every candidate threat.

## 1. Queries run

### OpenAlex (`/works?search=`, top 12 screened; filter `from_publication_date:2015-01-01` unless noted)
| # | Query | Hits | Relevant finds |
|---|---|---|---|
| 1 | microbiome classifier decision threshold new cohort specificity | 5,793 | Li 2025 Gut Microbes best practices; Chakravarthy 2026 |
| 2 | microbiome classifier cross-cohort calibration | 2,589 | Shi 2026 bioRxiv (OSCC thresholds fail) |
| 3 | colorectal cancer metagenomic classifier threshold specificity cohorts | 1,856 | Thomas/Wirbel 2019; **Bao 2026 Zenodo (threshold transportability, CRC)** |
| 4 | microbiome machine learning batch effect cross-study prediction | 5,729 | DEBIAS-M 2025; PLSDA-batch 2023 |
| 5 | microbiome domain adaptation classifier cross-study | 7,602 | GDmicro 2023; DEBIAS-M |
| 6 | microbiome batch correction prediction transfer learning | 2,335 | Han 2024 review; BRIDGE-KO 2026 |
| 7 | label shift microbiome | 73,091 | none relevant |
| 8 | prevalence shift microbiome diagnostic | 40,973 | none relevant |
| 9 | gut microbiome colorectal cancer screening FIT combination specificity | 2,822 | CRCbiome; FIT-cartridge studies |
| 10 | unsupervised threshold adaptation domain shift | 48,954 | generic UDA only |
| 11 | threshold transfer label-free new site | 245,308 | noise |
| 12 | unsupervised recalibration classifier scores new population without labels (from 2000) | 1,622 | **Ziegler 2019 URC**; Calibration Transfer Gap 2026 |
| 13 | estimating false positive rate unlabeled target domain | 23,829 | PU-learning literature |
| 14 | Neyman-Pearson classification label shift | 1,774 | Tong 2018; Scott 2018; Kalan 2026; **Qiu 2026 SACSIM** |
| 15 | decision threshold adaptation unlabeled test data prior shift | 11,332 | Sipka 2022 |
| 16 | score normalization speaker verification unsupervised mixture | 4,078 | **Guo 2008 double-Gauss unsupervised normalisation**; Cumani 2020 |
| 17 | unsupervised score calibration mixture model speaker recognition | 1,191 | **Brummer & Garcia-Romero 2014**; Cumani 2020/2023 |
| 18 | class-conditional score distribution shift mixture model test scores | 47,440 | Arampatzis 2010 (IR score distributions) |
| 19 | operating point transfer clinical prediction model new hospital threshold | 45,698 | Davis 2020 |
| 20 | microbiome threshold specificity external validation operating point | 9,085 | none relevant |
| 21 | test-time adaptation decision threshold medical | 225,824 | TTA surveys only |
| 22 | unsupervised calibration of score distribution two-component mixture | 15,130 | Brummer 2014 again |
| 23 | quantification class prior estimation mixture scores | 76,213 | **DyS (Maletzke 2019)** |
| 24 | ROC analysis without truth mixture model (no date filter) | 13,274 | Gao 2023 ssROC; (Henkelman 1990 found via Crossref) |
| 25 | estimating sensitivity specificity without gold standard mixture model continuous test | 82,466 | latent-class literature |
| 26 | serology cutoff mixture model seropositivity threshold | 379 | White 2025 JID |
| 27 | site-specific threshold AI deployment mammography operating point recalibration | 97 | none directly relevant |
| 28 | unsupervised threshold calibration deployment new site machine learning medical | 3,690 | Li 2026 MedIA (performance estimation) |
| 29 | label shift adaptation medical diagnosis prevalence unlabeled | 1,996 | Lipton 2018 |
| 30 | maximum likelihood label shift bias-corrected calibration | 36,018 | Alexandari 2019; Garg 2020; LaSCal 2024 |
| 31 | average thresholded confidence predict accuracy unlabeled | 28,214 | Garg 2022 ATC |
| 32 | Calibration and threshold transportability of omics classifiers across cohorts (2023+) | 1,300 | only the Zenodo deposit (manuscript not indexed) |
| 33 | threshold transportability classifier cohorts (2023+) | 19,846 | several 2026 "threshold transport" papers (vascular, wrist fracture, sepsis) |
| 34 | calibration transportability microbiome classifier (2023+) | 2,153 | Shi 2026 |
| 35 | fixed threshold performance metagenomic classifier external cohort calibration (2023+) | 205 | **CRC-TrustBench 2026** |

### OpenAlex journal-restricted (2023-2026; ISSN filter), 3 queries each
"classifier threshold cohort generalization" / "cross-cohort diagnostic model specificity calibration" / "batch effect machine learning prediction cohorts":
iMeta 2 / 7 / 13; Microbiome 8 / 4 / 16; Gut Microbes 6 / 17 / 25; Bioinformatics 31 / 13 / 58; Briefings in Bioinformatics 74 / 40 / 146.
Nothing on operating-point transfer. Relevant items: Li 2025 Gut Microbes (benchmark by AUC), BRIDGE-KO 2026 Brief Bioinform,
iMeta 2024 periodontitis signature (AUROC-based).

### arXiv export API (abstract/all-field boolean)
| Query | Hits | Relevant |
|---|---|---|
| all:"threshold" AND all:"label shift" AND all:"unlabeled" | 3 | none |
| abs:"unsupervised calibration" AND abs:mixture | 0 | - |
| abs:"false positive rate" AND abs:"distribution shift" AND abs:"unlabeled" | 0 | - |
| abs:microbiome AND abs:"distribution shift" | 1 | Perciballi 2026 (tabular FMs) |
| abs:microbiome AND abs:"domain adaptation" | 1 | not relevant |
| abs:"Neyman-Pearson" AND abs:"shift" | 11 | Kalan 2026; Scott 2018 |
| abs:"operating point" AND abs:"unlabeled" AND abs:shift | 1 | audio deepfake (not relevant) |
| abs:"score normalization" AND abs:unsupervised | 6 | not relevant |
| abs:"label shift" AND abs:"conformal" | 12 | Podkopaev 2021; Lee 2026 |
| abs:"decision threshold" AND abs:"domain shift" AND abs:medical | 0 | - |

### PubMed (esearch, title/abstract)
| Query (abridged) | Hits | Relevant |
|---|---|---|
| microbiome AND (classifier OR ML) AND threshold AND cohort AND specificity AND (transfer OR external OR cross-cohort) | 1 | respiratory microbiome mortality (not relevant) |
| microbiome AND calibration AND (cross-cohort OR LOSO OR cross-study) | 1 | **CRC-TrustBench** |
| (metagenom* OR microbiome) AND (label/prior/prevalence/dataset/distribution shift) | 1 | not relevant |
| (decision threshold OR cut-off OR operating point) AND (unlabeled OR without labels) AND (adapt* OR recalibrat*) | **0** | - |
| microbiome AND colorectal AND "fecal immunochemical" AND (classifier OR model) AND specificity | 2 | Wang 2026 review |
| "curatedMetagenomicData" | 11 | none on thresholds |
| microbiome AND (batch correction OR batch effect) AND (prediction OR classifier) | 6 | DEBIAS-M; Chakravarthy 2026 |
| "model updating" AND recalibration AND external validation AND threshold | 8 | clinical recalibration examples |

Crossref bibliographic lookups were also used to resolve DOIs: Guillory 2021 DoC (ICCV), Liang 2017 (CCR), Chen 2022 SEES, and the Bao 2026 manuscript (not found).

## 2. The five closest threats (frank assessment)

1. **Brummer & Garcia-Romero 2014, ICASSP, "Generative modelling for unsupervised score calibration"** (plus Cumani 2021/2023 TASLP and Guo 2008 ISCSLP).
   They fit a 2-component model to UNLABELED target scores with an unknown target proportion and get an affine calibration, which then sets the decision threshold.
   This is our mechanism: an affine map, a two-class score mixture, an unknown prior and maximum likelihood on unlabeled scores. Cumani 2023 models the score distributions under *domain mismatch* specifically.
   **Verdict: "affine score shift + mixture ML on unlabeled scores" is NOT new as a method.** It is established in speaker verification (unsupervised calibration and score normalisation), and in IR score-distribution thresholding (Arampatzis 2010) and ROC-without-truth (Henkelman 1990).
   What remains different in ours: (i) the component shapes are anchored to the *source* class-conditional score densities (nonparametric KDE), not a parametric Gaussian family; (ii) the decision target is a fixed specificity/FPR rather than Bayes-cost calibration; (iii) multi-site biomedical evaluation with low-prevalence and small-n regimes.
   These differences are modest. We must cite this line, and we cannot call the estimator novel.
2. **Qiu, Zhao & Zheng 2026, Biometrics, SACSIM.** It adapts Neyman-Pearson (FPR-constrained) decision rules to a target population using a small unlabeled target sample plus labelled source data and minimal auxiliary information, with early cancer detection as the motivating example.
   This is the closest statistical-methods threat to the "label-free, FPR-controlled threshold transfer" problem.
   It differs from ours: it uses a semiparametric single-index model on covariates (needing auxiliary information), not a score-level black-box map; it was evaluated on simulations and one prostate cancer study; and it has no multi-site benchmark.
   A reviewer from statistics will know it. We must cite it and discuss why a score-only, model-agnostic method is still needed (frozen vendor models; high-dimensional compositional features).
3. **CRC-TrustBench (Zhang et al. 2026, Front Microbiol).** It uses 15 CRC studies and 10 countries with LOSO/LOCO, and evaluates Platt calibration, conformal-style sets and abstention "without outer-test labels". It reports that conformal coverage falls below target under study shift.
   It is the same problem space and disease, and it already makes the "AUROC hides reliability failure" argument for CRC metagenomes. It does *not* re-set thresholds for a target specificity, and it uses no unlabeled target data for adaptation.
   **Our "protocol change" message is partly pre-empted. Our contribution must be the remedy, plus the FPR/colonoscopy decision framing.**
4. **Bao et al. 2026, Zenodo software deposit "Calibration and threshold transportability of omics classifiers across cohorts".** It covers CRC metagenomic and TB transcriptomic cohorts: calibration, fixed-threshold performance, prediction-set coverage and labelled local intercept updating.
   The manuscript was not found in OpenAlex, Crossref or PubMed and is likely under review. Its title alone pre-empts "threshold transportability of CRC microbiome classifiers" as a problem statement.
   Its remedy is labelled intercept updating. Unless the hidden manuscript also has an unlabeled method, our label-free transfer stays distinct. **Re-check before submission.**
5. **Saerens 2002 / Alexandari 2020 MLLS-BCTS / DyS (Maletzke 2019) quantification.** Fitting target scores as a mixture of source class-conditional score distributions is exactly DyS/HDy quantification, but with no shift of the components.
   Our model is DyS plus an affine site map plus threshold mapping. Saerens EM is already a baseline. **MLLS with bias-corrected calibration (Alexandari) and DyS/HDy should be added as baselines**, because reviewers from ML will expect the strongest label-shift estimators.

Runner-up threats:
- Zheng 2026 PLoS One (sepsis transcriptomics) shows that *unlabeled external-cohort feature standardisation* rescues fixed thresholds. This is a simple label-free competitor that we must include as a baseline: per-site feature standardisation or rank normalisation, then the source threshold.
- Gibbons 2018 percentile normalisation (needs labelled local controls).
- DEBIAS-M 2025 (unlabeled-capable feature-level debiasing, AUROC-evaluated).
- Shi 2026 bioRxiv (OSCC thresholds fail in 2 of 3 cohorts).
- Wirbel 2019 (already reports cross-study FPR at a 10% FPR cutoff).

No paper was found that performs **unsupervised threshold/operating-point adaptation for microbiome classifiers**. PubMed for unlabeled threshold adaptation returned 0 hits, and microbiome plus label/prior shift returned no relevant hits. The key novelty threat (bucket 7) is not realised, but the space is closing fast: four 2026 papers or deposits address threshold or calibration transport for omics or microbiome classifiers.

## 3. Novelty scorecard (1 = done before, 5 = clearly new)

| Dimension | Score | Rationale |
|---|---|---|
| Problem novelty | **3/5** | That operating points drift across microbiome cohorts is documented by Wirbel 2019 (cross-study FPR), CRC-TrustBench 2026, Bao 2026 and Shi 2026. The *label-free* specificity-targeted version for microbiome is unaddressed. |
| Method novelty | **2/5** | Unlabeled affine score calibration via a two-class mixture exists (Brummer 2014; Cumani 2021/2023; Guo 2008). Mixture-of-source-score quantification exists (DyS). NP adaptation with unlabeled target exists (SACSIM 2026). Our only new pieces are anchoring to source KDE components under an affine site map and mapping a specificity target, which is a recombination. |
| Evaluation novelty | **4/5** | No existing benchmark measures realised specificity versus target across 11 CRC + 4 IBD + 4 T2D cohorts with label-free methods, prevalence sweeps (case-control to screening ~1%), the n-labelled-controls tradeoff, and colonoscopies per 1,000. |
| Practical value | **4/5** | It answers a real lab decision (cut-off at a new site without collecting outcomes). Pilot overdispersion (p=2e-7) shows the problem is real. The value depends on beating the simple local-quantile and local-standardisation baselines. |

## 4. Recommendations: what is genuinely new and what is already done

Already done (do NOT claim as new):
- An affine (a + b*score) target-score transform estimated by mixture ML on unlabeled scores. This is "unsupervised score calibration" or "unsupervised score normalisation" in speaker verification (Brummer 2014; Cumani 2021/2023; Guo 2008), and Z/T-norm when labels are present (Auckenthaler 2000).
- Prior/prevalence estimation from unlabeled scores (Saerens EM, BBSE, MLLS-BCTS, DyS/HDy quantification).
- Label-free FPR-constrained rule adaptation in general (SACSIM 2026; Scott 2018 generalized NP for domain adaptation).
- Documenting that thresholds or calibration fail across microbiome/omics cohorts (Wirbel 2019; CRC-TrustBench 2026; Bao 2026; Shi 2026).
- Labelled local recalibration (Steyerberg 2004; Janssen 2008) and NP order-statistic thresholds from local controls (Tong 2018), which is our conformal baseline.

Plausibly new (where to put the paper's weight):
1. **Identifiability and failure diagnostics.** When is an affine site shift *plus* a prevalence change jointly identifiable from unlabeled scores? Low prevalence (screening ~1%) makes the case component nearly invisible. A goodness-of-fit or self-check that tells the lab "do not trust the adapted threshold; collect n controls instead" would be new, because Brummer/Cumani do not deliver a deployment abstention rule.
2. **A finite-sample specificity guarantee under the site-shift model**, e.g. a bootstrap or profile-likelihood upper confidence bound on the realised FPR. This differs from point calibration and from SACSIM's covariate-based approach.
3. **Hybrid label-efficient rule.** Combine the unlabeled mixture fit with k labelled local controls (k = 0, 5, 10, 20) and show how many controls the unlabeled pool saves versus pure conformal/NP. This fills the documented gap between unlabeled-only and labelled-only methods.
4. **Decision-level evaluation**: realised specificity error, unnecessary colonoscopies and missed cancers per 1,000 at screening prevalence, across 3 diseases and about 19 cohorts. Frame the paper as the first label-free operating-point transfer benchmark for microbiome diagnostics.
5. Optional: per-class shift (a0, b0 for controls and a1, b1 for cases) or a monotone (non-affine) transport, with model selection. This generalises the speaker-verification tied models.

Mandatory additional baselines (so reviewers cannot say "simpler method would do"):
- Per-site unlabeled feature standardisation or rank normalisation, then the source threshold (Zheng 2026).
- MLLS with bias-corrected calibration (Alexandari 2020).
- DyS/HDy mixture quantification without shift (Maletzke 2019).
- Parametric 2-Gaussian unsupervised calibration (Brummer 2014). This is a direct ablation of our source-anchored components.
- Optionally ATC-style estimated specificity (Garg 2022), and DEBIAS-M preprocessing as an orthogonal add-on.

Pre-submission watch items:
- Re-search for the Bao et al. manuscript (Zenodo 10.5281/zenodo.23236394 accompanies it).
- Re-search for CRC-TrustBench follow-ups.
- Run new OpenAlex queries "unsupervised threshold" + microbiome / metagenom* in the month before submission.
