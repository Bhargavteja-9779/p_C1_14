# Cover letter

[Date]

To the Editors, *iMeta*

Dear Editors,

We submit our Letter, "Gut-microbiome disease classifiers flag 0–87% of healthy people at the same cut-off, depending on
the population", for consideration in *iMeta*.

Gut-microbiome classifiers are validated by AUROC across cohorts, but a test in use needs one cut-off, and its
false-positive rate decides how many healthy people are referred for follow-up, for example to colonoscopy. We measured
that rate for 28 classifiers of 14 diseases in every eligible healthy adult population in curatedMetagenomicData
(36 populations, 6,525 people, 20 countries). At a cut-off set for a 10% false-positive rate, the realised rate ranged
from 0% to 87% (populations of at least 100 people), far beyond sampling noise for every classifier, and AUROC did not
predict the spread.

The Letter makes three contributions:
- **An atlas.** A cross-disease, cohort-by-cohort map of the false-positive rate of fixed-cut-off microbiome
  tests in healthy general populations, with heterogeneity statistics and prediction intervals for a new population.
- **An audit of two released indices.** In its own East Asian training studies, the Gut Microbiome Wellness Index 2
  labelled a median of 64% of healthy people per study as non-healthy, against 12% elsewhere, and a pre-specified audit
  of its predecessor, the Gut Microbiome Health Index, found the same pattern in a second model trained largely on the
  same studies (67% vs 21%). Retraining the published GMWI2 recipe reproduced
  the effect and linked it to the geographic make-up of the training data; we state clearly that this is a property of
  the models, not evidence about East Asian microbiomes. GMHI could not be transferred to newer profiles, and on the
  same samples the share flagged rose from 23% to 43% between profiler versions (post hoc).
- **A practical check for sites.** A known order-statistic rule applied to 100 unlabelled local people cut the
  false-positive-rate error by 62% within sites in retrospective non-random splits, failed across sites, and costs
  sensitivity. We release the atlas, the 14 LASSO classifiers and these procedures as a tested Python tool (fprcal).

We believe the work suits *iMeta*'s readership in microbiome data science and translation: it changes what benchmark
papers should report (the false-positive rate per held-out population, next to AUROC), what developers should check
(the geographic case mix of training data) and what a site should do before using a published cut-off.

All data are public. Confirmatory analyses followed time-stamped plans committed before they were run; we report the
hypotheses that failed and label every post hoc analysis. Code, plans, per-person scores, figure source data and the
tool are available at [GitHub URL; Zenodo DOI], and a fresh-clone rerun reproduces every result file.
[Before submission: confirm that the GMWI2 and GMHI developers were sent the audits and given the opportunity to comment.]

This manuscript has not been published and is not under consideration elsewhere. All authors approved the submission.
[Competing interests: authors to confirm.]

Suggested reviewers: [authors to add, e.g. experts in microbiome diagnostics and diagnostic-test evaluation with no
conflict of interest].

Sincerely,

[Corresponding author name, affiliation, email]
