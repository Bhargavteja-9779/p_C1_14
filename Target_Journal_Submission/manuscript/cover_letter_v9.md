# Cover letter (draft for manuscript v9)

[Date]

To the Editors, *iMeta*

Dear Editors,

We submit our Short Communication, "Gut-microbiome disease tests miss their stated false-positive rate in many
healthy populations and should be recalibrated at the site of use", for consideration in *iMeta*.

Gut-metagenome classifiers for colorectal cancer, inflammatory bowel disease and type 2 diabetes are usually validated
by AUROC across cohorts. In use, however, a test needs a fixed cut-off, and its false-positive rate decides how many
healthy people are sent for follow-up. We applied six standard classifiers to 6,525 healthy adults from 36 public
cohorts in 20 countries. A cut-off set for a 10% false-positive rate flagged 0% to 62% (LASSO), and the between-cohort
heterogeneity was large (I² 70–95%). Pooled validation hides this.

The paper makes three contributions:
- It measures, cohort by cohort, how far the false-positive rate of fixed-cut-off microbiome tests moves in general
  healthy populations, with prediction intervals.
- It shows which taxa shift the scores of the most over-flagged populations.
- It compares corrections head to head. Cut-offs borrowed from other cohorts did not restore the target. A label-free
  burn-in on 100 people from the same site halved the average error but did not remove the risk of a high
  false-positive rate at a given site, and it failed across sites.

We think the work fits *iMeta*'s interest in microbiome data science with practical consequences. Its message for
benchmark design and for sites adopting published classifiers is direct: report the false-positive rate per cohort,
and check the cut-off locally.

All data are public (curatedMetagenomicData). Analysis plans were written before each analysis and are kept, with code,
per-person scores and all results, in a public repository [URL and Zenodo DOI to be added]. A full rerun from a fresh
clone reproduces every result file. We report every hypothesis we tested, including those that failed.

This manuscript has not been published and is not under consideration elsewhere. All authors approved the submission.
The authors declare no competing interests [authors to confirm].

Sincerely,

[Corresponding author name, affiliation, email — to be completed by the authors]
