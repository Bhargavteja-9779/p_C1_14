# 2026-11-25 — BREAKTHROUGH (cycle 6): a published test, its own data, and a mechanism
OBSERVATION: r9 scorecard said significance 7 < P75 8 because our 28 classifiers are research models. Novelty self-score 17/25.
ATTEMPT: plan v6 (committed before scoring): external test of the PUBLISHED GMWI2 (Chang 2024 Nat Commun; bioconda 1.6).
Coefficients extracted with a whitelisted unpickler; identical to the paper's Supplementary Data 3 (95/95).
QC: our GMWI2 vs published GMWI2 on 704 overlapping samples r = 0.991, same call 98.4%.
RESULT (pre-specified): developer-stated FPR 0.208. Unseen strict populations: FPR 0-0.54, I2 0.92 (G1 supported); 80% outside
[0.10, 0.31] vs 9% expected (P = 6e-13, G2 supported); seen populations NOT better (G3 falsified); within-site burn-in -79%
(95% CI 64-85%, 11/13 populations, G4 supported).
SURPRISE (post hoc, developers' own published scores only): among GMWI2's 5,514 healthy TRAINING samples (44 studies) the
published cut-off labels 0-84% "non-healthy" by study (I2 0.96). All 8 studies > 50% are East Asian. EA median 0.64 vs 0.12
(MW P = 5e-7). Drivers: B. plebeius (EA 72% vs 18% presence), B. coprocola, B. stercoris, Lachnoclostridium carry
"non-healthy" weights. Case-mix: EA = 62% of non-healthy vs 20% of healthy training samples (OR 6.7).
HYPOTHESIS -> TEST (plan v6b, committed before running): geographic case-mix confounding. GMWI2-recipe model trained from
scratch on cMD, leave-one-study-out: NAIVE EA gap 0.52 (B1 supported); country-balanced weights cut gap 88% (CI 54-121%, B2
supported); pooled AUROC -0.040 (CI -0.12 to 0.02; B3 NOT supported, margin was 0.03); tau 1.16 -> 0.81 (B4 supported).
TURN: the paper can now say why some population-specific false-positive rates arise (pooled case-mix confounding), show
it in a published tool's own data, and show the training-time fix, alongside the deployment-time fix (burn-in).
