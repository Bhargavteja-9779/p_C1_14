# 2026-11-28 SURPRISE: part of the LASSO over-flagging is a refit/cut-off mismatch

OBSERVATION. A blind statistics reviewer (r19) noticed that the atlas cut-off comes from out-of-fold control scores,
while healthy populations were scored with the model refitted on all training data. Plan v4 P7 had checked this only
for the three-disease analysis.

ATTEMPT. Post hoc, I refitted all 28 classifiers exactly as atlas_v5.py did (scores reproduced to 9e-16) and rescored
the same people with the mean logit of the cross-validation fold models (`v5/posthoc_r19_foldmodel.py`).

RESULT. The main finding survives: 70% of classifier-population pairs lie outside 0.05-0.15 under both scorings, and
26 of 28 classifiers keep I2 >= 0.5 (median 0.92). But the extremes shrink for LASSO: pairs above 0.25 fall from 26% to
15%, pooled fatty-liver FPR from 0.26 to 0.01, impaired glucose tolerance from 0.42 to 0.29. RF barely moves.

TURN. The headline no longer rests on the share above 0.25 or on the 0-87% extreme. The title now uses the robust
out-of-band share, the main text reports the mismatch, and the conclusion adds a recommendation that developers score
their cut-off with the model they release.
