# PROGRESS (resume file)

Any agent continuing this work: read this file first, then `git log`. Work happens on branch
`claude/kind-ramanujan-tiui92` (earlier: `claude/dreamy-clarke-rldxev`, same history). All deliverables live in `Target_Journal_Submission/`.
Commit + push after every phase (auto-save).

## Environment notes
- 4 CPU, 15 GB RAM, no GPU. Python 3.13. ScienceDirect HTML blocked (403); Crossref, OpenAlex, arXiv, UCI, PhysioNet, Zenodo, HF reachable.

## Rebuilding the data cache in a fresh container
```
pip install scikit-learn pandas scipy pyreadr matplotlib statsmodels
mkdir -p /tmp/claude-0/eh && curl -o /tmp/claude-0/eh/eh.sqlite3 https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3
mkdir data_cache && cd data_cache
curl -L -o sm.rda https://raw.githubusercontent.com/waldronlab/curatedMetagenomicData/devel/data/sampleMetadata.rda  # -> sampleMetadata.csv via pyreadr
python ../Target_Journal_Submission/code/scripts/fetch_cmd.py <comma-separated studies; MetaCardis as 2022-10-19.MetaCardis_2020_a.relative_abundance>
```

## Phase log
- [x] Phase -1: repo skeleton created (2026-11-23)
- [x] STEP 0: journal landscape + 72-day evidence
- [x] STEP 1: benchmark 25 papers, level profile, style notes
- [x] STEP 2: real-life problem discovery
- [x] Data lock (code/experiments/data_lock.md)
- [x] STEP 3: novelty map + scorecard
- [x] Protocol pre-registration (code/experiments/protocol.md, commit ea2f3f7)
- [x] First working version / D6 rounds 1-2 (dev only)
- [x] Final experiments: locked run done (code/experiments/final/results_locked.md) - success criterion MET
- [x] Manuscript draft v1 (manuscript/manuscript.md, 1,7xx words; supporting_information.md; si_tables.md; figures/)
- [ ] Reviews 1-11 (round 1 done: 4 reports in reviews/, response in reviews/round1_response.md, manuscript v2)
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
- STEP 1 running (background agent writing journal_benchmark.csv + benchmark_raw_notes.md).
- STEP 2 lead topic: operating-point (decision threshold) transfer of gut-microbiome disease classifiers to new sites.
  Data: curatedMetagenomicData via ExperimentHub (fetch_cmd.py -> data_cache/ra/*.csv, data_cache/sampleMetadata.csv; not committed).
  Cohorts: CRC 11, IBD 4, T2D 4 (incl. MetaCardis 2022 release), adenoma 5.
  PILOT (code/pilot/pilot_threshold_transfer.py): LOSO over 11 CRC cohorts, threshold set for 90% specificity on training
  out-of-fold controls. Realised specificity per held-out cohort: LASSO 0.79-1.00, RF 0.72-1.00; overdispersion vs binomial
  chi2 p=0.004 (LASSO), p=2e-7 (RF). => threshold drift is real, not sampling noise. Mean AUC LASSO 0.78, RF 0.82.
- STEP 3 running (background agent writing novelty_map.csv + novelty_search_log.md).
- 2026-11-23 (session 2): container was fresh; rebuilt data cache (recipe above). STEP 3 background agent from session 1 left no files -> re-running. Dev rounds 1-2 done (see code/experiments/novelty_escalation_log.md). STEP 3 done. NEXT: write protocol pre-registration, then locked-cohort run.
- 2026-11-23 Locked run done, no deviations. Status quo out-of-band in 69% of pairs; conformal n=20 in band 100%. NEXT: figures + manuscript (Short Communication, <=3000 words, <=3 figs).
- 2026-11-23 Manuscript v1 drafted. Post-hoc: AUROC does not predict FPR error (rho -0.18); control-score shift does (rho 0.80). NEXT: Reviews 1-11 (independent reviewer agents), citation audit, final package.
- 2026-11-23 Review round 1 done -> manuscript v2. Key change: recommendation ~100 same-site controls (20 fixes mean only); other-site controls fail; pool quantile valid at screening prevalence. NEXT: review round 2 on v2.

## RESUME HERE (handoff written 2026-11-23, end of session 2)
State: manuscript v2 done after review round 1 (commit ddb3b9d+). Branch `claude/kind-ramanujan-tiui92`.
1. Fresh container: run the "Rebuilding the data cache" recipe above (≈5 min), plus `pip install -r Target_Journal_Submission/code/requirements.txt`.
   data_cache/ is NOT in git; all locked results (locked_rows.csv.gz, scores/*.npz, *.txt) ARE in git, so figures/tables
   can be rebuilt without re-running the locked run: `cd Target_Journal_Submission/code/experiments/final && python3 make_figures.py && python3 make_si_tables.py`.
   Do NOT re-run run_locked.py (pre-registered, run once).
2. Key files: manuscript/manuscript.md (v2), supporting_information.md, si_tables.md, figures/; reviews/ (round-1 reports,
   round1_response.md); code/experiments/protocol.md (+Deviations); code/experiments/final/*.py (post-hoc scripts listed in SI).
3. NEXT: review round 2 on v2 (fresh editor/statistics/domain reviewers + citation re-check), then rounds up to 11,
   then final package (docx/LaTeX per iMeta, graphical abstract image, cover letter, Zenodo).
4. Open items (limitations / needs authors): MMUPHin/ConQuR/DEBIAS-M, SIAMCAT pipeline, boosting model, 2nd profiler,
   CD/UC split, temporal drift, FIT benchmark; placeholders (authors, contributions, COI, funding, AI statement, GitHub/Zenodo);
   iMeta JIF/quartile unverified in JCR.


## RESUME HERE (handoff written 2026-11-24, session 3, branch `claude/beautiful-goldberg-37nqmw`)
This branch MERGES both earlier lines (kind-ramanujan manuscript v2; quirky-mayer RECHECK with the leakage fix:
ThomasAM_2019_c duplicates YachidaS_2019 and is removed everywhere). The paper was REFRAMED (novelty escalation round 3).

### New story (manuscript: Target_Journal_Submission/manuscript/manuscript_v3.md, figures_v3/)
"The false-positive rate of a gut-microbiome test belongs to the population, not to the test."
1. Atlas: CRC/IBD/T2D classifiers (LASSO, RF; cut-off = 90th pct of LOCO training-control scores) applied to 8,329 healthy
   adults, 60 cohorts, 28 countries never seen in training. FPR 0-56% (LASSO CRC), 0-87% (RF CRC); 61-69% of populations
   outside 0.05-0.15; pooled FPR looks fine (0.05/0.12/0.14).
2. Cohort effect: ICC 0.20-0.42, unchanged by age/sex/BMI/depth/diversity (A4 confirmed). A2 (shared propensity) and
   A3 (non-westernised over-flagged by CRC test) FALSIFIED - reported.
3. Fixes that fail (dev + locked): healthy-context residual, pooled atlas reference, composition-matched reference,
   control augmentation (Wirbel 2021; post hoc, locked: 0.066 vs 0.070, P=0.69).
4. Label-free burn-in self-calibration (k = ceil((N+1)(1-alpha(1-pi_max)))) + PAC variant: LOCKED pre-stated criterion MET
   (N=100: P(FPR>.15)=0.085, error -54% vs status quo, PAC P(FPR>.10)=0.045). Exact beta-binomial law matches observed.
Key files: code/experiments/atlas/{protocol_atlas.md, protocol_deploy.md, atlas_split.md, results_locked_v3.md,
novelty_escalation_r3.md (all ideas tried, scorecard 24/30), atlas_run.py, analyse_a4.py, deploy_eval.py,
summarise_deploy.py, control_augmentation.py, make_figures_v3.py, dev/explore_r1.py, dev/explore_r2.py, results/}.
Do NOT re-run deploy_eval.py locked (pre-registered, run once). Prior-art positioning: Wirbel 2021 Genome Biol (control
augmentation, >2-fold FPR), Hiseni 2026 Gut Microbes (6 countries), Bashari ICML 2025, refineR/kosmic - all in refs.

### Journal
iMeta Short Communication primary. User (2026-11-24): "any Frontiers journal also fine" -> Frontiers in Microbiology
(median 59 d / P75 79 d) is the full-length fallback (journal_selection/selected_journal.md).

### Rebuild data in a fresh container
pip install scikit-learn==1.9.1 pandas scipy matplotlib pyreadr statsmodels; run the recipe above for sampleMetadata +
ExperimentHub sqlite; then fetch the case-control cohorts listed above PLUS the healthy cohorts in
code/experiments/atlas/healthy_studies.txt (BedarfJR_2017, PehrssonE_2016 are missing from the 2021-03-31 release - fine).
export CMD_CACHE=<repo>/data_cache. Then `cd code/experiments/atlas && python3 -W ignore atlas_run.py && python3 covars.py`
regenerates results/atlas_rows.csv.gz (gitignored? no - committed) as needed.

### NEXT
1. Review round 2: EDITOR report received (reviews/review_r2_01_editor_v3.md - act on items 1-9). Statistics and domain reports NOT received - re-run those two.
   Anticipated issues: small-n cohorts inflating spread (estimate random-effects tau / compare with binomial noise);
   non-general-population "controls" (VincentC_2016 hospital, RaymondF_2016 antibiotics, LokmerA_2019, FerrettiP_2018
   mothers) -> sensitivity analysis on strict general-population subset; possible duplicated subjects across cohorts;
   taxa driving over-flagging (atlas_coefs.csv).
2. Supporting Information v3 (started: results/tableS1_cohorts.md); Tables S2 (ICC), S3 (dev fix attempts), S4
   (deploy summary), S5 (earlier case-control analysis summary), S6 (control augmentation).
3. Further review rounds, citation audit of v3, final package (iMeta docx, cover letter, graphical abstract).
