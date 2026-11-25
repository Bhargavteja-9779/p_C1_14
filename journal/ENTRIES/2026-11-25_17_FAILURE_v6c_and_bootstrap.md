# 2026-11-25 — FAILURE / CORRECTION (session festive-cori, after merging trusting-mayer)
Review round 10 (statistics) found two wrong cluster bootstraps and a mislabelled plan. Corrected (corrected_boot_v13.py,
post hoc, original files kept):
- v6c CI −0.23/−0.03 -> −0.22/−0.01 (barely excludes 0). Level-free spread (MAD of FPR) fell in only 2/5 tests and
  mean |FPR−0.10| rose 0.150 -> 0.249. The "balancing generalises to disease classifiers" claim is withdrawn; v6c is
  post hoc (plan committed with its results).
- v6b CI 54–121% -> 41–149%; point estimate 88% unchanged.
LESSON: a logit-scale tau reduction can come from FPR levels moving towards 0.5; always check a level-free measure.
Manuscript v13 + SI v13 written; audit 161/161; round-10 response written.
