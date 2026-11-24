# Stage 2 - Problem story re-check (2026-11-23)

## 1. Is the problem real? Person, setting, cost
- **Person:** the laboratory director or screening-programme lead who must fix the positivity cut-off of a stool test at
  their own site; downstream, the endoscopy unit that receives the positives.
- **Setting:** a published microbiome classifier (trained on public case-control cohorts) adopted at a new hospital/country.
- **Cost (verified citations, see stage6/):**
  - CRC: ~1.9 million new cases and ~0.9 million deaths in 2020 [Sung 2021, CA Cancer J Clin, 10.3322/caac.21660].
  - For the stool test already in use (FIT), programmes choose different cut-offs, and accuracy depends strongly on the
    cut-off [Selby 2019, Gastroenterology, 10.1053/j.gastro.2019.08.023]; cut-offs used by programmes worldwide differ and
    give very different performance [eClinicalMedicine 2026, 10.1016/j.eclinm.2026.103835]; faecal-haemoglobin
    distributions differ between populations, so programmes must study their own distribution
    [Fraser 2015, J Med Screen, 10.1177/0969141315597017]. => cut-off choice is a real, site-level decision with
    colonoscopy-workload consequences. (Exact wording of each source checked in Stage 6.)
  - A false positive consumes a colonoscopy; a false negative delays diagnosis. We do NOT claim a monetary cost; we report
    counts per 1,000 people tested (illustrative prevalence).
- **Honest limit:** no microbiome CRC test is in routine use today; the problem is forward-looking (deployment readiness).

## 2. What changed in the field (searched again; see stage3/novelty_search_log.md)
- Roschewitz 2023 (Nat Commun) showed, in imaging, that sensitivity/specificity drift although AUROC holds and proposed
  label-free prediction alignment -> must be cited and used as a baseline (added as M7).
- CRC-TrustBench 2026 (Front Microbiol) studied calibration/conformal coverage across CRC metagenomic cohorts; it reports
  coverage below target but not realised FPR at a fixed cut-off, nor site-level threshold re-estimation.
- Qiu 2026 (Biometrics, SACSIM): FPR-constrained rules adapted with unlabeled target data (covariate model).
- Indirect reference-interval methods (lab medicine) estimate healthy-population cut-offs from unlabeled mixed data -
  the conceptual precedent of our mixture estimator.
- Wirbel 2019 already fixed a 10% FPR cut-off on training controls (used to test disease specificity on other diseases).
=> The label-free mixture estimator cannot be sold as a new method class. Reposition (see Stage 4).

## 3. One-paragraph story (final wording depends on Stage 5 numbers; filled in at Stage 7)
"Laboratories that adopt a published gut-microbiome test must fix its positivity cut-off for their own population. If the
cut-off flags more healthy people than planned, colonoscopy capacity is wasted; if fewer, cancers are missed. Current
microbiome classifiers are validated across cohorts with AUROC, which says nothing about the cut-off. We measure how the
cut-off behaves at held-out cohorts of four diseases and compare every practical way to re-set it, from doing nothing,
through label-free methods, to testing a few known-healthy local samples. [RESULT: realised FPR spread; which fix works;
how many local controls are needed.]"

## 4. First-page check
Done at Stage 7 against the final manuscript.
