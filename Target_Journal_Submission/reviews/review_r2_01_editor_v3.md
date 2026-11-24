# Review round 2 (on manuscript_v3) - Editor screening report (independent reviewer agent, 2026-11-24)

Decision: SEND TO REVIEW (borderline). Fix items 1-4 before submission.

Novelty: per-population scale, cohort-level ICC partition, locked head-to-head vs control augmentation are new.
FPR inflation itself is known (Wirbel 2021, ~2x). Burn-in rule = adaptation of conformal/NP/indirect RIs, not a methods advance.

Major weaknesses and fixes:
1. Guarantee validation is circular: random splits within a cohort are exchangeable by construction, so Fig 3A fit is
   expected. Reframe as code calibration check; add exchangeability-breaking test (time/batch-ordered burn-in, or burn-in
   on one sub-study, evaluate on another: TettAJ_2019 a/b/c, HMP visits). Delete "people within a cohort behave as exchangeable".
2. Pre-specification gaps: A5 (labelled local controls >=90% in band at n=100; country-matched reference fails) never
   reported; A4 protocol named age/sex/BMI/depth only (paper adds Shannon, richness) - report as-specified model; protocol
   says 62 cohorts/~10,000/25 countries vs paper 60/8,329/28 - add CONSORT-style flow.
3. "Explained none" is false: covariates cut between-cohort variance 38-39% for IBD; ICC models use only 28/38/36 cohorts.
   Write "little and inconsistently"; give counts; fix sign wording "-24% to +39%".
4. Non-healthy "controls" (hospital patients; metabolic-disease controls) inflate spread -> sensitivity analysis on
   population-based/explicitly healthy cohorts + table of recruitment context.
5. Head-to-head burn-in vs augmentation (0.039 vs 0.066, P=0.0004, 34/50) is buried -> put in Fig 2B; state post hoc and DEV-only augmentation.
6. Fig 2B confounded: population set changes with N -> fixed set (n>=220) or per-population lines.
7. Sensitivity cost understated (0.46 -> 0.22): show FPR+sensitivity together, PPV at 0.5-1% prevalence; discuss whether
   correct FPR is the right target; explain status-quo FPR 0.29 (case-control locked) vs 0.05 pooled CRC atlas.
8. Generality: one profiler, two classifiers, no batch-correction comparator -> test MMUPHin/ComBat or DEBIAS-M on locked
   split, or drop "nothing short of it works".
9. Format: workflow schematic panel in Fig 1; CONCLUSION and ACKNOWLEDGMENTS sections; 95% CIs on headline numbers.

Title suggestion: "Gut-microbiome disease classifiers miss their specificity in most new populations" (current title
over-states: the paper shows test x population). Abstract: drop "sold with one specificity"; "distribution-free guarantee
on expected FPR assuming later patients resemble the burn-in group"; add augmentation result and sensitivity cost.
First paragraph: clinical stakes -> gap -> "Here, we..." with three headline numbers.

Over-claims: "explained none"; "nothing short of it works"; "first ~100 people tested" (random subsamples used);
"exact" guarantee (expected FPR only; PAC variant gives probability bound; N=25 mean FPR 0.077); 87% is RF (LASSO 0-56%);
"ten-fold" unstable -> use 10th-90th percentile spread; screening framing (IBD/T2D have no screening use); check Table S3
exists; call protocols "pre-specified analysis plans", not pre-registration (internal, same-day).
