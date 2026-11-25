# Response to review round 1 (manuscript v0.2 -> v0.3)

Decision taken with the author: keep a methods angle and add post-hoc experiments, clearly labelled exploratory,
rather than only reframing. New code: `code/experiments/posthoc/explore_r1.py`, `code/analysis/posthoc_r1.py`;
results: `results/posthoc_r1_tables.md` (SI Tables S3-S4).

## Shared major points (all three reviewers)

| Issue | Change |
|---|---|
| Rank rule is a known method (tolerance limit, NP umbrella, contaminated conformal, indirect reference intervals) | Novelty claim dropped. Main text and Note S1 now say "we do not claim the rule as new" and cite Wilks, Tong 2018, Yao 2023, Bashari 2025, Jones 2018. Contribution restated as: evidence that thresholds fail, that ML label-free fixes fail, that the classical local rule works with real small pools, and where the pool must come from. |
| Locked result holds by construction (within-cohort exchangeable pools); cross-study failure not reported | New post-hoc E3 (pool from another cohort, all locked tasks, both models) and E5 (pool from another centre of MetaCardis, same protocol and sequencer). Rule fails in both (RMSE 0.158 and 0.067 vs 0.009 same centre). New section "The samples must come from the same site"; title, highlights and conclusion changed accordingly. Locked section now states that exchangeability held by design. |
| pi = 1% contains no cases in 13/16 pairs | Disclosed in SI (Evaluation design, deviation 1) and main text. Post-hoc E1 draws K ~ Binomial(n, pi) up to 20%: rule RMSE 0.030-0.052. Label-free comparison in main text now quoted at pi = 0 and pi = 20%. |
| Gain over naive pool quantile is small; local quantile hidden | Local quantile now in Figure 2A/2B/2C and in text (difference -0.017, CI -0.028 to -0.008; E2: 7-10% vs 4% of deployments above 15% FPR at n = 100-200). |
| Metric hides single-deployment misses | Per-deployment results in Figure 2A and text (FPR > 15% in 14% / 20% / 33% / 39% of deployments for rank rule / 10 controls / pool quantile / training cut-off); Table S3. |
| Small locked pools vs "few hundred samples" recommendation | Post-hoc E2 with pools 25-500 in the three cohorts with >= 150 controls (Figure 2C). |
| Strict version abstains in half; alpha = 0.05 omitted | Both reported in the main text (abstention 50% for strict version; 31% for the rank rule at alpha 0.05 with small pools). |

## Statistics reviewer

| # | Change |
|---|---|
| M3 Note S1 ties wrong; random K; loose proof | Note S1 rewritten: one-line argument (t >= r-th largest of n - K pool controls), exchangeability conditional on K stated, bounds with + P(K > m), ties: `>= t` is anti-conservative; strict `> t` or jitter recommended; post-hoc E1 shows tie handling changes no result at 3 decimals. Sample-size grid and slack stated. |
| M4 dependent units; bootstrap not as pre-registered; ctrl10 claim | Main-text CIs now clustered by cohort-task; Wilcoxon at cohort-task level (n = 16); Holm. Deviation disclosed. "Came close" replaced by TOST equivalence (margin 0.02, P = 0.0002). The unit-level P = 0.048 is no longer cited. |
| M6 "AUROC stays acceptable" | Removed. Text now separates weak tasks (T2D, adenoma; AUROC 0.54-0.69) from AUROC >= 0.70 pairs (FPR 0.02-0.39) and external CRC (0.11-0.30). |
| M7 adenoma controls reused | Sensitivity analysis without adenoma (Table S3); conclusions unchanged; stated in text. |

## Domain/novelty reviewer

| # | Change |
|---|---|
| Missed prior work | Added Tong 2018, Yao 2023, Bashari 2025, Jones 2018, Toes-Zoutendijk 2017, Imperiale 2014, Gibbons 2018, DEBIAS-M (Austin 2025). Not added yet: Bao 2026 Zenodo deposit, Shi 2026 bioRxiv, CrcBiomeScreen preprint, Cumani 2021, DyS - to decide in round 2 (preprints/deposits). |
| "Nobody has checked" ignores Wirbel 2019 | Rewritten: meta-analyses reported specificity at fixed cut-offs [Wirbel 2019]; the open question is restoring the FPR without labels and where the pool must come from. |
| CRC-TrustBench and SACSIM mis-described | CRC-TrustBench now "benchmarks study cross-study transfer"; SACSIM: "adapted to a new site from an unlabelled sample when shift-explaining covariates are measured". |
| Screening realism (symptomatic cases, advanced adenomas > 5%, 10% target unrealistic, GLOBOCAN for prevalence) | Limitations expanded; 5% target discussed with FIT positivity [Toes-Zoutendijk]; prevalence source changed to Imperiale 2014 (0.7% in average-risk screening). GLOBOCAN reference removed. |
| Reference metadata | Alexandari -> PMLR 119:222-232; Brümmer pages 1680-1684; "Lê Cao". |
| Language ("honest answer", "keeps the promise") | Removed. |
| Feature-level batch correction not tested | Stated as not tested, with citations. |

## Editor

| # | Change |
|---|---|
| Length below 1,500 words | Main text now ~1,550 words. |
| No figure legends | Added. |
| No graphical abstract; running title > 40 chars; keywords; highlights | Graphical abstract text, running title ("Local cut-offs for microbiome tests", 35 characters), keywords and highlights added. |
| Funding / CRediT / code URL / title page | Placeholders remain; need author input. |
| Dev results presented as locked | Figure 1C dev panel removed; all post-hoc and dev material labelled. |
| Structured abstract question | Open: ask editorial office. |

## Still open for round 2

- Preprint/deposit prior work (Bao 2026, Shi 2026, CrcBiomeScreen) - decide whether to cite.
- Author-only items: CRediT, funding, GitHub URL + archived DOI, title page.
