# FINAL REPORT — status 2026-11-24

**Status: submission-ready draft (manuscript v10); two quality gates not met (G3 novelty score, G4 batch-correction
comparator). Paused for the authors' decision; see "What a human must do".**
Branch `claude/trusting-mayer-1ipvjz`. Package: `Target_Journal_Submission/submission_v10/`.

## The paper in one paragraph
"Gut-microbiome disease tests miss their stated false-positive rate in many healthy populations and should be verified
and recalibrated at the site of use" (iMeta, Short Communication).

We set six standard classifiers (CRC, IBD and T2D; LASSO and RF) to a 10% false-positive rate (FPR). We then applied
them to 6,525 healthy adults in 36 general-population cohorts from 20 countries, after removing 119 people duplicated
across cohorts.
- **Heterogeneity.** The FPR varied far more between populations than chance allows (I² 70–95%). The 95% prediction
  interval for a new population ran from 0.01–0.22 (CRC LASSO) to 0.01–0.63 (IBD LASSO).
- **Taxa.** A few taxa carried each population's score shift. The IBD test over-flagged Asian populations through
  lower "health-marker" taxa learned from Western cohorts. The T2D LASSO test over-flagged non-westernised populations
  (post hoc).
- **Borrowed corrections did not fix it.** These were cut-offs from other cohorts, including same-country cohorts; a
  pooled reference; a ComBat-style feature alignment; and control augmentation. Augmentation had no overall gain and
  helped mainly when the same population was in the pool.
- **Local burn-in.** A label-free burn-in on 100 people at the same site halved the average FPR error under within-site
  non-random splits. The pre-specified accession-order design gave a Holm-adjusted P of 0.022 over 34 tests. The
  burn-in did not reduce the risk of an FPR above 0.15, and it failed across sites.
- **Hypotheses that failed are reported.** The pre-stated pooled non-random hypothesis (≥ 50% error reduction) was not
  supported (48%; Holm-adjusted P = 0.059).

## Gates (Section 7)
| Gate | Status | Evidence |
|---|---|---|
| G1 Journal | partial | iMeta Letter: received→accepted median 33 d, P75 52 d (n = 67, PubMed history; `journal_selection/`). The Q1 rank and JIF come from secondary sources only; JCR was not reachable (UNVERIFIED). |
| G2 Prior art | pass | 85-record + 50-record novelty maps (RECHECK/stage3, journal_selection); claim → closest prior work → difference tables in reviews r3–r8; 31 references Crossref-checked |
| G3 Novelty ≥ 20/25 | **fail** | Honest self-score 17/25 (differentiation 3, mechanism 3, evidence 3, breadth 4, significance 4). Novelty reviewers scored 8/10 but agree the burn-in rule is not new and the contribution is empirical. |
| G4 Baselines | **partial** | Training cut-off, pooled reference, country reference, ComBat-style alignment, control augmentation and labelled local controls were all run. DEBIAS-M, MMUPHin and ConQuR were not run; the DEBIAS-M environment install was refused by the session permission system. |
| G5 Main result | partial | Burn-in vs training cut-off, within site: 12/13 populations better, Holm-adjusted P = 0.022 (34-test family). Not met: the pre-stated pooled hypothesis (48% < 50%), tail risk unchanged, and the 7-population locked tests are not Holm-significant. SEEDS_CONFIRM does not apply: the design is deterministic, with a locked cohort split. |
| G6 Ablation | n/a / partial | Burn-in vs strict burn-in vs labelled controls; mis-specified prevalence bound |
| G7 Generalization | pass, with limits stated | 3 diseases × 2 models × 32–35 populations; non-random and cross-site designs; cross-site failure reported |
| G8 Leakage | pass | Global dedup (r > 0.99; sensitivity at r > 0.95 changes nothing); locked split |
| G9 Reproducibility | pass | Fresh clone of commit 17a8371, all 19 result scripts from an empty results/ folder: 30/30 result files identical to the committed ones (`logs/repro_full_2026-11-24.log`). The later r7_posthoc.py (Table S15) is a 1-line derivation from ppv_v4.csv, which was reproduced. |
| G10 Review | pass | Rounds 7 and 8: three fresh reviewers each, all minor revision, no MAJOR (8/8/8; 7/8/8) |
| G11 Number audit | pass (lenient) | `scripts/audit_numbers.py`: 181/181 numbers of v10 match a result-file value |

## Compute
CPU only (4 cores, no GPU). Cycle 4 used about 1.5 h of wall-clock analysis compute. Earlier cycles were not logged
(UNVERIFIED but small). This is far below the 15 h per-cycle and 120 h global ceilings.

## Review history (cycle 4)
| Round | Statistics | Novelty | Editor | Result |
|---|---|---|---|---|
| r2 (v3) | major | — | borderline | → v4 |
| r3 (v4) | 7 minor | 6 major | 5 major | → v5 |
| r4 (v5) | did not finish (usage limit) | 8 minor | 7 minor | → v6 |
| r5 (v6) | 7 minor | 8 minor | 7.5 minor | → v7 |
| r6 (v7) | 7 minor | 8 minor | 7.5 minor | → v8 |
| r7 (v8) | 8 minor | 8 minor | 8 minor | no MAJOR → v9 |
| r8 (v9) | 7 minor | 8 minor | 8 minor | no MAJOR → v10 |

Every round has its reports and a response table in `Target_Journal_Submission/reviews/`.

## What a human must do
1. Fill in the placeholders: second and corresponding author, contributions, conflicts of interest, funding, AI-use
   statement, GitHub URL and Zenodo DOI. Earlier author metadata, from the parallel branch: first author P N Bhargav
   Teja (VIT Vellore); funding none; competing interests none. Please confirm these apply to this paper.
2. Decide on DEBIAS-M. Either allow a Python 3.11 + CPU-torch environment, or run it locally. It would close G4 and is
   the comparator reviewers asked for most.
3. Verify iMeta's JCR rank and the current author guidelines; the journal pages could not be reached from the build
   environment.
4. Choose: submit v10 as is, or fund another cycle aimed at G3. Options for that cycle:
   - outcome-confirmed (labelled) recalibration over time;
   - a second profiler;
   - a held-out time-ordered cohort.

## Where everything is
- Manuscript and package: `Target_Journal_Submission/submission_v10/` (docx, md, figures, SI, tables, highlights, cover letter)
- Analysis: `Target_Journal_Submission/code/experiments/atlas/v4/` (README with run order; protocol_v4.md with deviations)
- Reviews and responses: `Target_Journal_Submission/reviews/`
- Research diary: `journal/ENTRIES/`; decisions: `state/decisions.md`; variants: `state/variants_tried.csv`
- Resume: `HANDOFF.md`, `BOOTSTRAP_PROMPT.txt`
