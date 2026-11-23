# Journal Level Profile - iMeta (from journal_benchmark.csv, 25 papers 2024-2026: 11 Letters, 14 Research Articles)

Caveat: Letters keep methods in Supporting Information, which was not read; several cells are NA/UNVERIFIED.
In 2024 iMeta short-format papers were indexed as "Journal Article" (e.g. the periodontitis signature paper).

| Dimension | Median (IQR) all | Letters | Research Articles | **Our target (>= median, aim top quartile)** |
|---|---|---|---|---|
| Cohorts / datasets | 5 (2-13) | 3 (2-6) | 9 (2-17) | **>= 20 cohorts, 4 diseases** (top quartile) |
| Baselines compared | 0 (0-1) | ~0 | 0 (0-3); max 14 | **>= 6 calibration baselines + 3 classifier families** (top quartile) |
| Seeds / repeats | reported by 7/25 | rarely | 1 study with 100x5-fold | **>= 10 seeds + 1,000 resamples per scenario** |
| Ablation | 12% | 0% | 3/14 | **yes, every component** |
| Cross-dataset / external test | 52% | 5/11 | 8/14 | **yes: leave-one-cohort-out + locked external diseases** |
| Code available | 92% | - | - | **yes, full pipeline + run_all.py** |
| Real-world / deployment evidence | rare | - | - | **yes: outcomes per 1,000 screened at realistic prevalence** |
| Statistics | mostly simple tests (Wilcoxon, AUC CIs) | | | **paired bootstrap CIs, permutation, Holm correction, effect sizes** |

## Typical novelty claimed
Tools/platforms (new software), signatures validated across public cohorts, benchmarks, and new biological findings.
ML Letters claim a new predictive framework plus a biological insight. Method papers rarely include ablations.

## Applied vs theoretical
Strongly applied. Theory is uncommon; a clear mechanism/explanation plus practical tool is valued.

## Format targets (Letter / Short Communication)
- Main text ~2,100 words (observed 1,907-2,503; guideline 1,500-3,000).
- Exactly 2 multi-panel figures in all 11 Letters observed (guideline allows 1-3); no tables in main text.
- ~20 references (looks like a cap).
- No abstract; short graphical-abstract summary (~100 words). No highlights.
- Methods in Supporting Information (unlimited).
