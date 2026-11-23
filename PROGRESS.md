# PROGRESS (resume file)

Any agent continuing this work: read this file first, then `git log`. Work happens on branch
`claude/hopeful-carson-p4zvqk` (earlier: `claude/dreamy-clarke-rldxev`). All deliverables live in `Target_Journal_Submission/`.
Commit + push after every phase (auto-save).

## Environment notes
- data_cache/ is NOT committed. Rebuild: download https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3 to
  /tmp/claude-0/eh/eh.sqlite3; sampleMetadata.rda from raw.githubusercontent.com/waldronlab/curatedMetagenomicData/master/data/
  -> data_cache/sampleMetadata.csv (pyreadr); then `cd data_cache && python3 ../fetch_cmd.py <studies>` (MetaCardis: pass
  `2022-10-19.MetaCardis_2020_a.relative_abundance`). Takes ~3 min.
- 4 CPU, 15 GB RAM, no GPU. Python 3.13. ScienceDirect HTML blocked (403); Crossref, OpenAlex, arXiv, UCI, PhysioNet, Zenodo, HF reachable.

## Phase log
- [x] Phase -1: repo skeleton created (2026-11-23)
- [x] STEP 0: journal landscape + 72-day evidence
- [x] STEP 1: benchmark 25 papers, level profile, style notes
- [x] STEP 2: real-life problem discovery
- [ ] STEP 3: novelty map + scorecard
- [ ] Protocol pre-registration
- [ ] First working version
- [ ] Novelty escalation loop (D6)
- [ ] Final experiments
- [ ] Manuscript
- [ ] Reviews 1-11
- [ ] Final package

## Decisions (with reasons)
- 2026-11-23 STEP 0 (in progress): Measured received->accepted days from Crossref assertions (Springer/T&F/Wiley/IET) and
  PubMed history (Elsevier/OUP/biomed). ~95 hand-picked journals + automatic screen of 1378 non-Elsevier journals
  (OpenAlex 2yr citedness>4.5) + PubMed screen of Elsevier/IEEE journals. Raw files in journal_selection/raw/.
  Key finding: nearly no Q1 journal has p75<=72 for full research articles. Letters/short reports inflate speed.
  Research-only checks: Critical Care 66/85 (fail), iMeta research article 56/86 (fail), iMeta Letter 33/52 (pass),
  Ophthalmology & Therapy 52/70 (pass, but likely Q2 + clinical scope).
- 2026-11-23 STEP 0 DONE: iMeta (Wiley), Short Communication format (Letter median 33 d, P75 52 d; Research Article fails P75=86).
  See journal_selection/selected_journal.md.
- STEP 1 DONE (journal_benchmark.csv, level profile, style notes).
- STEP 2 lead topic: operating-point (decision threshold) transfer of gut-microbiome disease classifiers to new sites.
  Data: curatedMetagenomicData via ExperimentHub (fetch_cmd.py -> data_cache/ra/*.csv, data_cache/sampleMetadata.csv; not committed).
  Cohorts: CRC 11, IBD 4, T2D 4 (incl. MetaCardis 2022 release), adenoma 5.
  PILOT (code/pilot/pilot_threshold_transfer.py): LOSO over 11 CRC cohorts, threshold set for 90% specificity on training
  out-of-fold controls. Realised specificity per held-out cohort: LASSO 0.79-1.00, RF 0.72-1.00; overdispersion vs binomial
  chi2 p=0.004 (LASSO), p=2e-7 (RF). => threshold drift is real, not sampling noise. Mean AUC LASSO 0.78, RF 0.82.
- STEP 3 running (background agent writing novelty_map.csv + novelty_search_log.md).
- 2026-11-23 (session 2): container reset; data cache rebuilt; STEP 3 novelty search re-run (previous run never committed);
  dev round 1 (code/experiments/dev/explore_v1.py) running on the 8 DEV CRC cohorts only.
- 2026-11-23 AUTHOR DECISIONS (fixed, do not change): code available on request; no funding; no competing interests.
  Wording in Target_Journal_Submission/manuscript/back_matter.md — use verbatim.
- 2026-11-23 AUTHOR DECISION: round 2 direction = HYBRID (few labelled local controls + unlabelled pool). Author asked
  for maximal strengthening against desk rejection. Desk-rejection-proofing plan (all on DEV cohorts until frozen):
  1. Hybrid v2 = location-scale transport of source control/case score shapes, (a, b) anchored by k labelled local
     controls, unlabelled pool adds information, soft Beta prior on deployment prevalence (mean 0.01, strength 10),
     threshold from the posterior-predictive (Laplace-averaged) FPR, not plug-in. Simulation: plug-in biased
     (FPR 0.15-0.19 at target 0.10 with k=5-10); predictive + prior error 0.02-0.04; misspecified prevalence errs
     conservative (lower FPR) = clinically safe direction.
  2. Baselines (all): source threshold, local quantile, Saerens EM, UPA alignment (Roschewitz 2023), free 2-comp GMM,
     site-shift v1, label-free+prior, conformal k controls, plain quantile k controls, predictive controls-only.
  3. Headline metric: "labelled controls saved" at equal FPR error vs conformal; plus MAE, violation rate P(FPR>0.15),
     sensitivity; clinical: extra colonoscopies / missed cancers per 1,000 screened.
  4. Diagnostic + abstain rule: goodness-of-fit of labelled controls to the transported source shape; abstain/fall back
     to conformal when it fails.
  5. Identifiability proposition (pool-only location-scale + prior shift is unidentifiable; >=2 labelled controls fix it)
     + formal simulation study with known truth.
  6. Robustness: targets alpha in {0.05, 0.10, 0.20}; classifiers LASSO, RF (+ one more); prevalence misspecification.
  7. Generalisation on LOCKED sets once, after freeze: 3 external CRC cohorts, IBD, T2D, adenoma.
  8. Practical guidance: number of labelled controls needed for +/-0.03 FPR.
