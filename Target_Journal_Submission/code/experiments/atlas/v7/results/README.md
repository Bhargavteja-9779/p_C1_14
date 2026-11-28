# Plan v7 (GMHI) results: which file is authoritative

- `gmhi_results.json` is the output of the pre-specified run (`run_gmhi.py`). Two of its fields are **superseded**:
  - `Q2` (r = 0.803, n = 101, "pass"): the planned accession matching met only 2 studies, because the developers record
    BioSample accessions and curatedMetagenomicData records sample names and run accessions. The corrected Q2 is in
    `posthoc_gmhi_matching.json` (r = 0.795, n = 2,190, 19 studies: **failed**). Under the plan, H3–H6 are therefore
    not interpreted; their values in `gmhi_results.json` are kept only for completeness.
  - `Q2.missing_species_in_cMD`: computed from the first study file only (a bug). Across all 61 studies, 4 of 7
    health-prevalent and 13 of 43 health-scarce species are missing (see `posthoc_gmhi_names.py`, SI S7).
- H1 and H2 (developers' own data) in `gmhi_results.json` are unaffected and are the reported results.
- Overlap with GMWI2 training data: `posthoc_gmhi_gmwi2_overlap.json`.
- Profiler-version shift per study (Figure S2B, Table S27): `gmhi_profiler_shift_perstudy.csv`.
