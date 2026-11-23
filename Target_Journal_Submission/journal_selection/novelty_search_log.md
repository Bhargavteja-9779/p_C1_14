# STEP 3 - Novelty search log: label-free operating-point transfer for microbiome classifiers

Date: 2026-11-23. Sources: OpenAlex API (`/works?search=`), PubMed E-utilities (esearch/esummary/efetch), arXiv API,
Crossref (`query.bibliographic`). ScienceDirect blocked. Every entry in `novelty_map.csv` (64 rows) was returned
by one of these APIs with the DOI / arXiv id shown; abstracts of the closest works were read via OpenAlex/PubMed,
and the UPA paper (Roschewitz 2023) full text was checked on nature.com for its prevalence assumption.
One entry (Zhang K 2013, ICML) has an OpenAlex record but no DOI.

## 1. Queries run (hit counts = total matches reported by the API)

### OpenAlex (relevance-ranked, top 8 inspected each)
| # | Query | Hits |
|---|---|---|
| 1 | microbiome classifier cross-study validation colorectal cancer | 6,811 |
| 2 | meta-analysis fecal metagenomes colorectal cancer microbial signatures | 4,052 |
| 3 | machine learning meta-analysis colorectal cancer metagenomes | 1,957 |
| 4 | machine learning metagenomics disease prediction Pasolli | 1,309 |
| 5 | MMUPHin meta-analysis microbiome batch correction | 114 |
| 6 | ConQuR batch effects microbiome conditional quantile regression | 83 |
| 7 | percentile normalization case-control microbiome batch effects | 948 |
| 8 | microbiome classifier decision threshold transfer cohort | 3,286 (no relevant hit in top 8) |
| 9 | microbiome classifier calibration external validation specificity | 3,202 (no relevant hit) |
| 10 | microbiome diagnostic classifier site shift operating point | 3,394 (no relevant hit) |
| 11 | gut microbiome classifier generalizability across populations | 9,547 (no relevant hit) |
| 12 | domain adaptation microbiome disease classification | 19,492 (GDmicro only) |
| 13 | transfer learning microbiome cross-cohort prediction | 9,142 |
| 14 | microbiome signature reproducibility across cohorts batch effect classifier performance | 1,507 |
| 15 | batch effect correction improves microbiome classifier cross-study prediction | 1,987 |
| 16 | tabular foundation models microbiome distribution shift | 872 |
| 17 | microbiome machine learning prevalence screening positive predictive value low prevalence | 7,996 (no relevant hit) |
| 18 | microbiome multicenter validation colorectal cancer classifier independent cohort specificity | 1,440 (no relevant hit) |
| 19 | Saerens title / Lipton title / Alexandari title / Garg 2020 title / RLLS title | verification queries |
| 20 | Quantifying counts and costs via classification (Forman) | verification |
| 21 | Conformal prediction under covariate shift | 15,069 |
| 22 | Distribution-free UQ for classification under label shift | verification |
| 23 | test-time adaptation decision threshold false positive rate distribution shift | 70,633 (no relevant hit) |
| 24 | operating point transfer medical imaging distribution shift | 228,936 (surveys only) |
| 25 | unsupervised threshold adaptation unlabeled target domain classifier | 14,465 (generic UDA) |
| 26 | recalibration without labels unlabeled test data mixture model scores | 592 (Welinder 2013, Ziegler 2019) |
| 27 | classifier score distribution mixture model estimate prevalence unlabeled | 2,147 |
| 28 | updating clinical prediction models recalibration logistic Steyerberg | 1,741 |
| 29 | calibration hierarchy risk prediction models Van Calster | 2,172 |
| 30 | calibration Achilles heel predictive analytics | 3,971 |
| 31 | validation of clinical prediction models new setting updating methods | 311,013 |
| 32 | transfer of diagnostic test cut-off between populations specificity | 165,780 |
| 33 | ROC curve estimation without gold standard mixture model biomarker | 2,719 |
| 34 | estimating sensitivity specificity absence of gold standard finite mixture | 14,081 |
| 35 | unsupervised score normalization speaker verification domain mismatch threshold calibration | 336 (Cumani 2020/2023) |
| 36 | Neyman-Pearson classification distribution shift false positive rate control | 1,243 |
| 37 | threshold selection label shift target false positive rate guarantee | 46,726 (no relevant hit) |
| 38 | calibration transfer gap recalibration parameters distribution shift | 10,308 |
| 39 | unsupervised recalibration | 8,510 |
| 40 | semisupervised classifier evaluation recalibration mixture | 126 |
| 41 | label shift medical diagnosis prevalence adjustment deployment | 17,684 |
| 42 | prevalence shift medical image classification deployment | 36,404 (Godau 2023/2025, Roschewitz 2023) |
| 43 | external validation decision threshold sensitivity specificity drift hospital | 9,602 |
| 44 | calibration drift sites threshold machine learning model deployment | 13,949 |
| 45 | Domain adaptation under target and conditional shift | 124,324 (Zhang 2013, Kirchmeyer 2021) |
| 46 | mixture proportion estimation positive unlabeled | 9,002 |
| 47 | generalized label shift domain adaptation | 188,712 |
| 48 | unsupervised prediction alignment score distribution matching recalibration | 1,062 (no new hit) |
| 49 | binormal mixture model classifier scores unlabeled data operating point | 9 |
| 50 | recalibration in the large intercept update prevalence new population | 1,507 |
| 51 | fecal immunochemical test cut-off differs between populations positivity rate | 1,021 |
| 52 | Generative modelling for unsupervised score calibration Brummer | 108 |
| 53 | AI mammography operating point threshold local calibration recall rate new site | 189 (no method paper) |
| 54 | artificial intelligence breast screening threshold adjustment different population recall rate | 4,397 (clinical evaluations only) |
| 55 | domain shift score distribution location scale transformation adaptation unlabeled | 6,912 (no relevant hit) |
| 56 | threshold recalibration deployment unlabeled data clinical AI sensitivity specificity guarantee | 168 (Dolin 2025) |
| 57 | gene expression signature classifier cross-platform cutoff calibration new site | 853 (no relevant hit) |
| 58 | transcriptomic diagnostic classifier cross-site threshold harmonization unlabeled | 156 (no relevant hit) |
| 59 | unsupervised adaptation decision threshold prior and conditional shift scores | 10,068 (generic UDA) |
| 60 | conformal risk control / Learn then test / Tasche / Vergouwe closed testing | verification |

### PubMed (exact boolean)
| Query | Hits | Relevant |
|---|---|---|
| `microbiome[tiab] AND (classifier OR "machine learning") AND (threshold OR cut-off OR cutoff) AND (cohort OR external validation)` | 42 | 0 on threshold transfer |
| `microbiome[tiab] AND (calibration[tiab] OR recalibration[tiab]) AND (classifier OR "machine learning" OR "random forest")` | 30 | 1 (CRC-TrustBench 2026) |
| `microbiome[tiab] AND "label shift"` | **0** | - |
| `microbiome[tiab] AND ("operating point" OR "decision threshold")` | **2** | 0 (periodontology reviews) |
| `microbiome[tiab] AND "domain adaptation"` | 5 | DEBIAS-M, GDmicro |
| `("label shift" OR "prior shift" OR "prevalence shift") AND (threshold OR calibration)` | 11 | Godau 2025 |
| `metagenom*[tiab] AND classifier AND specificity AND "cross-cohort"` | 11 | CRC-TrustBench; Mei 2024 |

### arXiv API
| Query | Hits |
|---|---|
| `abs:"label shift" AND abs:threshold` | 13 (none on FPR-target transfer) |
| `abs:"false positive rate" AND abs:"distribution shift" AND abs:unlabeled` | 0 |
| `abs:"operating point" AND abs:shift AND abs:unlabeled` | 1 (audio deepfake, irrelevant) |
| `abs:"unsupervised calibration" AND abs:scores` | 2 (Brummer 2013 = ICASSP 2014) |
| `abs:microbiome AND abs:"distribution shift"` | 1 (Perciballi 2026) |
| `abs:"label shift" AND abs:"conditional shift" AND abs:scores` | 0 |
| (two further queries timed out on the arXiv API and were not retried) | - |

### Crossref
Verification of Wang & Le Cao 2019 (Brief Bioinform, 10.1093/bib/bbz105), Steyerberg 2019 book (10.1007/978-3-030-16399-0),
Zhang 2013 (only the 2014 book-chapter reprint has a DOI: 10.1201/b17558-22).

## 2. The closest 5 works and exactly how our idea differs

1. **Roschewitz et al. 2023, Nat Commun, "Automatic correction of performance drift under acquisition shift" (UPA)**
   (10.1038/s41467-023-42396-y). Label-free; maps target scores onto the reference score distribution by quantile
   matching so that sensitivity/specificity at the original operating point are kept (mammography, histopathology).
   *Difference:* the paper states "in UPA we assume that the prevalence is (roughly) preserved between reference and
   target domains" and says it is not designed for prevalence shift. Case fractions differ widely between microbiome
   case-control cohorts (exact range to be tabulated from sampleMetadata), and screening prevalence is about 1%. Under prevalence change, UPA is in effect our "local quantile"
   baseline: it confounds a shift in case mix with a shift in scores. Our model estimates the score shift (a, b) and the
   prevalence pi jointly. It also targets specificity, which needs only the control component. This is the most important
   neighbour and must be cited and run as a baseline (quantile alignment = UPA-style).
2. **Godau et al. 2023 MICCAI / 2025 Med Image Anal, "Navigating prevalence shifts"** (10.1016/j.media.2025.103504).
   Label-free prevalence estimation followed by re-setting the threshold and calibration, across 30 imaging tasks.
   *Difference:* this assumes pure prior shift, with p(score | class) unchanged. That is the Saerens/MLLS assumption, and our
   pilot drift contradicts it (realised specificity varies 0.72-1.00 even though specificity does not depend on
   prevalence). Our method adds the class-conditional location-scale site shift. This pair (UPA = shift only;
   Godau = prevalence only) is the gap our method fills.
3. **Brummer et al. 2014 ICASSP "Generative modelling for unsupervised score calibration"; Cumani et al.
   2020/2023 TASLP** (10.1109/icassp.2014.6853884; 10.1109/taslp.2020.3040103; 10.1109/taslp.2023.3282096).
   Two-component generative models (GMM, generalized-hyperbolic or variance-gamma) fitted to unlabeled speaker-verification
   scores, estimating both class score distributions and the target proportion without labels.
   *Difference:* these are the closest in method. They fit parametric class shapes from scratch on the target. We instead
   transport the empirical (nonparametric) source class-conditional shapes through a shared affine map and estimate only
   (a, b, pi). That is 3 parameters and is identifiable at small n (a microbiome cohort has 50-600 samples, against
   thousands of speaker trials). The aim is also different: a specificity-controlled cut-off rather than LLR calibration.
   No medical or omics use was found. Reviewers from ML/speech could say "this is Brummer 2014 applied to microbiome",
   so the paper must claim the transport, the small-n identifiability and the clinical protocol as its contribution,
   not the idea of a mixture.
4. **Zhang, Scholkopf, Muandet & Wang 2013 ICML "Domain adaptation under target and conditional shift"** (PMLR v28; no DOI),
   with Kirchmeyer et al. 2021 (arXiv:2110.15057). Theory and kernel methods for joint prior shift plus location-scale
   conditional shift (Zhang) or an OT map (Kirchmeyer) in feature space.
   *Difference:* our assumption (location-scale conditional shift + target shift) is Zhang's "LS-GeTarS" assumption applied in
   1-D score space to a fixed black-box classifier, without retraining. We must cite it as the theory precedent and
   inherit its identifiability argument. The new part is the 1-D score-space version, the operating-point objective and
   the microbiome evaluation.
5. **Welinder et al. 2013 CVPR "Semisupervised classifier evaluation and recalibration" (SPE)** (10.1109/cvpr.2013.419).
   Generative mixture model of classifier scores on a new dataset to estimate performance curves (and recalibrate) using
   few labels. *Difference:* it re-estimates parametric class shapes on the target with a few labels and has no
   source-to-target transport. It is still a direct precedent for "estimate the ROC/operating point on a new dataset from score
   mixtures", and is a candidate semi-supervised comparator for our "few local controls" arm.

Close in the application area (not the method): **CRC-TrustBench (Zhang Y et al. 2026, Front Microbiol,
10.3389/fmicb.2026.1971707)**. This is a LOSO/LOCO CRC benchmark. It reports that Platt calibration only modestly
helps and that conformal-style coverage falls below 90/95% targets across countries. It confirms the failure but offers no
label-free operating-point method and does not report realised specificity at a target. It must be cited as the most
recent microbiome paper on probability reliability. **Wirbel 2019** and **Gibbons 2018** (percentile normalisation to
local controls, which needs labelled controls) are the closest earlier microbiome works.

## 3. Verdict

- **Problem (threshold/specificity drift of microbiome diagnostics across cohorts): novel as a framed, quantified
  problem.** PubMed returns 0 hits for microbiome + "label shift" and 2 irrelevant hits for microbiome + "operating
  point"/"decision threshold". Microbiome cross-cohort papers (Pasolli, Wirbel, Thomas, Li 2023/2025, Piccinno 2025,
  DEBIAS-M, MMUPHin, ConQuR) evaluate AUROC. CRC-TrustBench (2026) is the only paper on probability reliability, and it does not
  address a fixed specificity target. Overlap here: low-medium.
- **Method (label-free, score-level joint location-scale + prior-shift mixture with transported source shapes): partially
  novel.** The ingredients exist in separate places: UPA (shift, no prevalence change), Godau/Saerens/MLLS (prevalence,
  no shift), Brummer/Cumani (unsupervised generative score mixtures in speech), Zhang 2013 (theory of LS conditional +
  target shift). We found no paper that combines (i) a transported nonparametric source score shape, (ii) an affine site map
  and (iii) prevalence by ML to set a specificity-targeted threshold for a fixed clinical classifier, and none in microbiome
  or omics diagnostics. Overlap: medium-high for the method family, low for the specific combination and the domain.
- **Overall:** the label-free operating-point transfer angle is **novel for microbiome diagnostics** (no direct
  prior art found). It is **not** novel as a general ML idea, so the paper must be framed as a deployment protocol plus a
  method adapted to small cohorts, with UPA and Godau-style prevalence adjustment as named baselines alongside the four
  already planned.

## 4. Scorecard (0-10)

| Criterion | Score | Reason |
|---|---|---|
| Novelty | 6.5 | New for microbiome/omics diagnostics; the method family exists (UPA, Brummer/Cumani, Zhang 2013) |
| Real-world relevance | 8 | Real decision (cut-off at a new lab); pilot shows specificity 0.72-1.00 across 11 CRC cohorts; colonoscopy capacity; FIT programmes already re-set cut-offs from positivity rates (Toes-Zoutendijk 2016) |
| Feasibility on 4 CPU, no GPU | 9 | 1-D score mixtures, LASSO/RF on precomputed MetaPhlAn profiles; minutes per LOSO sweep |
| Risk of "just recalibrate locally" rejection (10 = high risk) | 6 | Youssef 2023 Nat Med argues for recurring local validation. Answer: setting a 90%-specificity threshold needs about 100+ labelled controls per site for a tight bound (Learn-then-test/NP order statistics), while unlabeled stool samples arrive at no cost; we must show the label-free method matches or beats a conformal threshold from n = 10-30 local controls, or combines with it |

## 5. Suggested escalations (overlap is medium-high on method)

1. **Mandatory baselines added:** (a) UPA-style quantile alignment (Roschewitz 2023), (b) Godau-style prevalence-aware
   re-thresholding (MLLS/EM priors, then a threshold at the target specificity), (c) Brummer-style free 2-component GMM on target
   scores. Win, or explain when each fails: UPA fails under prevalence change, Godau fails under score shift, a free GMM fails at small n.
2. **Identifiability and uncertainty result:** state the conditions under which (a, b, pi) are identifiable from target
   scores alone, following Zhang 2013's LS-GeTarS. Give a bootstrap or profile-likelihood CI on realised specificity, and a
   **diagnostic/abstain rule** for when the affine-shift assumption is rejected (goodness of fit of the transported mixture).
3. **Hybrid label-efficient variant:** combine the mixture prior with a few local controls (Bayesian or shrinkage). This answers
   "just recalibrate locally" by showing that k labelled controls plus the unlabeled scores beat k controls alone. Report a
   label-savings curve, i.e. how many controls the label-free method is worth.
4. **Deployment-relevant endpoints:** realised FPR deviation from target; unnecessary colonoscopies and missed cancers per
   1,000 at screening prevalence (about 1%). Also a protocol recommendation: report realised specificity per held-out cohort
   at a pre-set target, not only AUROC.
5. **Breadth:** CRC (11 cohorts) + IBD (4) + T2D (4) + adenoma as a hard case. Optionally add CRC-TrustBench/Piccinno-style
   cohorts and test across profilers (MetaPhlAn versions) to show shift that is acquisition-like, not only cohort-like.
6. **Positioning sentence for the cover letter:** "Prior label-free operating-point corrections assume either an
   unchanged prevalence (UPA) or unchanged class-conditional scores (prevalence-shift adjustment); microbiome cohorts
   violate both, and we show a joint model is needed and sufficient."
