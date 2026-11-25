# Locked final run: execution record

- 2026-11-24 22:52 UTC: `run_final.py lasso` and `run_final.py rf` launched once each (protocol frozen at commit 73f827d).
- LASSO finished 2026-11-25 00:07 UTC (16 cohort-task pairs).
- RF: the container restarted after 15 of 16 cohorts were written (per-cohort checkpoint in final_rf.csv).
  The last cohort (adenoma, ZellerG_2014) was completed with `resume_final.py rf`, which replays the global rng
  (default_rng(2026); two permutations per replicate, sizes from the run log) so the remaining cohort received the
  same splits an uninterrupted run would have used. Model fitting is seeded (random_state=0).
- Verification of the resume mechanism (before using it on RF): LASSO output truncated to 15 cohorts in a scratch copy
  and resumed; the result was identical to the uninterrupted LASSO run (256,000 rows, DataFrame.equals = True).
- No locked cohort was analysed twice for decision-making; no protocol change followed the results.
