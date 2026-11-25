# Analysis plan v6b — mechanism test: geographic case-mix confounding. Written 2026-11-25 BEFORE running.

## Motivation (from post hoc v6 findings, labelled exploratory there)
Published GMWI2 cut-off flags 25-84% of healthy East Asian training samples vs 0-40% elsewhere (developers' own scores);
East Asian samples are 62% of non-healthy but 20% of healthy training samples (OR 6.7). Taxa with "non-healthy" weights
(B. plebeius, B. coprocola, B. stercoris, Lachnoclostridium) are far more prevalent in East Asian healthy guts.
Mechanism hypothesis M: when a health/disease classifier is trained on pooled studies whose healthy:non-healthy ratio
differs by country, population-typical commensals are learned as disease markers, which creates population-specific
false-positive rates. Intervention: case-mix balancing (sample weights so that, within every country, healthy and
non-healthy carry equal total weight) should remove the population-specific excess at little cost in discrimination.

## Data
curatedMetagenomicData (local cache, 61 studies), adult/senior stool, one sample per subject, v4 de-duplication.
Healthy = study_condition "control" and disease "healthy". Non-healthy = study_condition in {IBD, T2D, CRC, IGT, CAD,
ACVD, adenoma, cirrhosis, hypertension, HF, AS, schizophrenia, fatty_liver, ME/CFS, migraine, PD, T1D, melanoma, BD,
asthma} (diseases; infections, treatments and procedures excluded). Countries from metadata; East Asia = CHN, JPN, KOR.

## Models (GMWI2 recipe, fixed before running)
Features: presence (relative abundance/100 > 1e-5) of every MetaPhlAn3 clade (all ranks) present in >= 1% of training
samples. L1 logistic regression, C = 0.03 (as in GMWI2), liblinear, class_weight balanced. Cut-off: decision > 0 = healthy.
- NAIVE: unweighted pooled training (GMWI2 practice).
- BALANCED: sample weight = 1 / (number of training samples with the same country and label), renormalised.
Evaluation: leave-one-study-out (each study held out once; model trained on all other studies).

## Endpoints and hypotheses (falsifiers)
Per held-out study with >= 20 healthy people: FPR = share of healthy flagged non-healthy (decision < 0).
- B1 (mechanism reproduced): NAIVE median FPR of East Asian studies minus median of other studies >= 0.15.
  FALSIFIED if < 0.15 (then the case-mix explanation is not supported in cMD).
- B2 (intervention): BALANCED reduces that East-Asia gap by >= 50% relative to NAIVE.
- B3 (cost): pooled leave-one-study-out AUROC (healthy vs non-healthy over all held-out samples) of BALANCED is no more
  than 0.03 below NAIVE.
- B4 (heterogeneity): DerSimonian-Laird tau of logit FPR across held-out healthy studies is lower for BALANCED than NAIVE.
Uncertainty: study-clustered bootstrap (2,000) for the gap difference and AUROC difference.
