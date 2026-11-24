# Review round 3 (manuscript_v4) — Statistical referee

**Score: 7/10. Decision: MINOR REVISION.**

Every number in the text matches the v4 result files. Git history shows protocol_v4.md committed before any v4 result. Recomputed with fold-model scores, the DerSimonian–Laird I² stays at 0.70–0.95, so the core atlas finding holds. Check scripts: /tmp/claude-0/r3_stats/.

## Concerns

**1. MAJOR — The A5 comparison ("labelled local controls put 100% in band") is an artefact of the design.** In hypotheses_v4.py, the local arm averages FPR over 200 random splits before testing the band. So the 100% is guaranteed. The country arm instead uses one realised FPR per population and includes populations of n = 20. Per draw, only 77–79% are in band. On the same n ≥ 120 populations, the country arm gives 62% / 75% / 0% (LASSO CRC/IBD/T2D) and 12% / 88% / 29% (RF), on only 7–8 populations. So the country reference is not uniformly worse. *Resolve:* compare both arms on the same populations with the same per-deployment metric. Report a population-level paired test. Rewrite "did no better" to say per test which arm wins.

**2. MAJOR — The 48% for "all within-site designs" includes the cross-site design.** In H-NX1 (summary_v4.json, NX1_pooled N100: 228 units = 126 covariate + 30 sub-site + 72 accession), the sub-site transfers are included. The text calls the 48% a "within-site" figure, yet two paragraphs earlier it calls sub-sites "a different place". If the sub-sites are removed, the reduction is about 57%. The pre-stated hypothesis failed only because of the 30 sub-site units from 2 studies. Reporting it as not supported is correct. The label is wrong, though, and the "local means local" story leans on two studies plus a null neighbour result (9 populations, P = 0.57). *Resolve:* describe H-NX1 as pre-specified, with its sub-site component. Report each design separately with its population count. Do not redefine H-NX1 after the fact. Soften "only if those people come from the same site" to "failed in the two multi-site studies and showed no gain across neighbouring cohorts".

**3. MAJOR — Under random splits, the burn-in arm does not depend on the data.** BURN's error depends only on ranks, N and M (MAD 0.029–0.033 in every subset). So "BURN vs SRC" under random splits (strict P = 0.001, the strongest Holm survivor) only restates that SRC is miscalibrated beyond binomial noise. That is the atlas finding again, not evidence that the burn-in works. Yet the highlights ("halves the error") and the Holm narrative lead with it. *Resolve:* treat the non-random designs as the primary evidence for the burn-in and present the random-split comparison as a benchmark. Remove the random-split P values from the confirmatory family, or label them as such.

**4. MAJOR — The conclusion over-claims against control augmentation.** "Borrowed references do not [restore it]" conflicts with the data. Burn-in vs augmentation is better in 4 of 7 populations, P = 0.22, with a bootstrap CI from 7 clusters. Augmentation fixes IBD (0.103→0.064). The augmentation pool also included non-strict cohorts, and the two methods were scored on different people. *Resolve:* state that the comparison is inconclusive. Rerun augmentation with a strict-only pool. Evaluate both methods on identical evaluation people.

**5. MINOR — The "general-population" label is too broad.** The strict set includes control arms of disease case–control studies: GuptaA (n = 29), YachidaS, QinJ_2012, ThomasAM_2018b, JieZ, LiJ, YeZ, QinN, ZhuF and others. Three of the five "Asian over-flagged" IBD populations are case–control controls. *Resolve:* flag the recruitment type in Table S1. Report the heterogeneity statistics for true population cohorts separately.

**6. MINOR — The headline range is not size-filtered.** The graphical abstract's "0% to 76%" uses cohorts of n = 29–35 (GuptaA 0.76 RF; 0% in Bengtsson-Palme n = 35). That contradicts the round-2 fix. *Resolve:* use the n ≥ 100 range, or the 10th–90th percentile.

**7. MINOR — The fold-model check needs fuller reporting.** "At most 0.04" is true for the pooled FPR. The example given (CRC LASSO, 0.044 vs 0.037) is the smallest change, though. T2D LASSO drops 0.134→0.097. Per-population changes reach 0.14 (Obregon-Tito 0.31→0.17; LifeLinesDeep T2D RF, n = 1,117, 0.21→0.14). *Resolve:* report the largest pooled and per-population changes. Rerun BURN-vs-SRC with fold-model SRC as a sensitivity analysis.

**8. MINOR — Small reporting errors.**
- (a) "P < 10⁻¹⁰": CRC RF Q P = 5.5×10⁻¹⁰.
- (b) "Pooled over people … (random-effects estimates)" mixes two estimators; the raw pooled values differ (e.g. T2D RF 0.076 vs RE 0.061).
- (c) Deviation D2: the "strict" random-split design does not apply person-level filters, so state this next to "11 strict-set populations".
- (d) The three cycle-3 fixes (PCA adjustment, nearest-population reference, AUROC 0.76→0.61–0.68) were not rerun on de-duplicated data. Table S3 gives no numbers. Rerun them or say so.
- (e) The Holm family (11 tests "reported in the main text") was defined after the results. It omits, for example, BURN–ALIGN in the strict set and the A2 correlations. State the family rule.

**9. MINOR — The contaminated burn-in rests on 3 cohorts.** The analysis uses 6 units with π_max = π, which is never mis-specified. *Resolve:* add a run with mis-specified π_max (e.g. π_max = 0.01, π = 0.05, already in deploy_v4_cc_summary). Note the limited generality.

## Verified as correct
Counts, heterogeneity, n ≥ 100 ranges, covariates, A2/A3, taxon correlations (recomputed), stress-test numbers, ALIGN, augmentation, sensitivity/PPV and Holm-adjusted values.
