# STEP 3 - Novelty search log

Date of all searches: 2026-11-23. Companion table: `novelty_map.csv` (75 items, ids N01-N75).

## Databases / tools
- Web search (general engine; "standard" and "extended" modes).
- OpenAlex API (`api.openalex.org/works?search=...`, incl. source filters for iMeta ISSN 2770-596X and Microbiome ISSN 2049-2618, from 2022-01-01).
- Crossref API (`api.crossref.org/works?query.bibliographic=` for DOI look-up; `api.crossref.org/works/<doi>` for verification).
- DataCite API (`api.datacite.org/dois/<doi>`) to verify arXiv DOIs (10.48550/*), which Crossref does not hold.
- arXiv API: attempted, returned "Rate exceeded" (no results used). PubMed reached indirectly via web search (SACSIM PubMed record 42573999).
- ScienceDirect HTML not used (blocked).

## Queries run (hits = engine-reported count or results inspected)
| # | Database | Query | Hits / inspected | Kept |
|---|---|---|---|---|
| 1 | Web (extended) | microbiome classifier decision threshold specificity transfer across cohorts colorectal cancer recalibration | 10 | 4 (Tsai 2025, Wang 2026 review, Sun 2026 Meta-iTL, Zhang 2025) |
| 2 | Web (extended) | unsupervised threshold adaptation unlabeled target scores mixture model location-scale shift classifier operating point | 10 | 1 (Niekurzak 2026); GMM-based source-free UDA judged off-topic |
| 3 | Web | FIT faecal immunochemical test hemoglobin threshold positivity rate varies between screening programmes | 10 | 2 (Young 2024, Selby 2019) |
| 4 | Web (extended) | recalibration clinical prediction model new hospital without outcome labels unlabeled data prevalence estimation | 10 | 4 (CaDC, Tuwani 2023, Swaminathan 2025, Janssen 2008) |
| 5 | Web (extended) | arXiv adapting decision threshold under distribution shift without labels false positive rate control target domain | 10 | 3 (Fluhmann 2025, Leong 2026, class-wise OOD thresholds noted only) |
| 6 | Web | iMeta OR Microbiome journal 2024 2025 generalizability microbiome diagnostic model external validation batch effect deployment | 10 | 1 (Kubinski 2022) |
| 7 | Web | Wirbel 2019 meta-analysis fecal metagenomes CRC false positive rate 10% cross-study specificity | 10 | 1 (Wirbel 2019 confirmed) |
| 8 | Web | serology cut-off finite mixture model without gold standard seroprevalence specificity threshold | 10 | 3 (Kafatos 2016, Bouman 2021, Swart 2021) |
| 9 | Web (extended) | "label shift" "test-time" binary classifier threshold adjustment unlabeled medical imaging prevalence shift operating point | 9 | 1 (Ma 2022 MICCAI) |
| 10 | arXiv API | 5 boolean queries (threshold+unlabeled+specificity+shift; location-scale+label shift; conditional shift+location-scale; Neyman-Pearson+shift; microbiome+threshold+cohort) | rate-limited, 0 | 0 |
| 11 | OpenAlex | unsupervised threshold adaptation unlabeled specificity shift | 13,899 (top 10 inspected) | 0 (generic UDA) |
| 12 | OpenAlex | location-scale conditional shift label shift domain adaptation | 41,927 (10) | 2 (RLLS, Vega & Greiner 2022) |
| 13 | OpenAlex | Neyman-Pearson classification label shift | 1,796 (10) | 4 (Tong 2018, Scott 2019, Kalan 2026, **Qiu 2026 SACSIM**) |
| 14 | OpenAlex | microbiome classifier threshold cross-cohort specificity | 10,447 (10) | 2 (Duvallet 2017, Chakravarthy 2026) |
| 15 | OpenAlex | operating point transfer classifier new site unlabeled | 9,217 (10) | 0 |
| 16 | OpenAlex | label-free estimation clinically relevant performance metrics | 58,011 (10) | 2 (Fluhmann 2025, Lee 2024) |
| 17 | OpenAlex | decision threshold recalibration prevalence shift without labels | 4,141 (10) | 2 (**Godau 2023, Godau 2025**) |
| 18 | OpenAlex | mixture model diagnostic test cut-off without gold standard | 35,972 (10) | 2 (Swart 2021, Habibzadeh 2023) |
| 19 | Web (extended) | Neyman-Pearson classifier target population unlabeled sample shift adjustment early cancer detection | 9 | confirmed SACSIM details |
| 20 | Web (extended) | gut microbiome diagnostic classifier fixed cutoff external validation specificity drop new cohort calibration iMeta 2025 | 10 | 2 (Li 2023 Gut Microbes, Li 2025 best practices) |
| 21 | OpenAlex (iMeta, 2022+) | machine learning diagnostic cross-cohort / classifier generalization batch | 21 + 5 | 3 (Geng 2024, Liu 2026, Degregori 2026) |
| 22 | OpenAlex (Microbiome, 2022+) | same two queries | 33 + 4 | 3 (Nychas 2025, Karwowska 2025, Zhu 2023) |
| 23 | Crossref bibliographic | 12 title look-ups (Li 2023, Zhang 2025, Wang 2026, CaDC, Swaminathan, Selby, Zhang 2013, DoC, PLSDA-batch, refineR, Jones 2018, Henkelman 1990) | 3 each | DOIs resolved |

Remaining items (Saerens, BBSE, MLLS, Garg 2020/2022, Tibshirani 2019, Podkopaev & Ramdas, ComBat, MMUPHin, ConQuR, Gibbons, Steyerberg, Van Calster, Riley, Debray, Forman, Gonzalez, etc.) were added from known canonical literature and verified by DOI.

## DOI verification
- 73 DOIs checked: 57 via Crossref `works/<doi>` (title similarity to our record >= 0.72, all manually confirmed; one 429 rate-limit retried successfully), 16 arXiv DOIs via DataCite. All resolved.
- 2 items have no DOI (Zhang et al. 2013 ICML/PMLR; NannyML CBPE docs); their URLs return HTTP 200 and are marked "DOI UNVERIFIED" in the CSV.
- First-author names were corrected from registry metadata (e.g., the Frontiers IBD benchmark is Kubinski 2022; the SIAMCAT-style CRC transfer-learning paper is Sun 2026; the fixed-cut-off serology paper is Kafatos 2016).
- Caveat: for most items the assessment is based on title + abstract (OpenAlex/Crossref/web snippets); full texts of Wirbel 2019, Thomas 2019, SACSIM, CaDC and Godau 2025 were not read in full and should be checked before the manuscript's related-work section is finalised.

## Novelty scorecard

Scale: 5 = no close prior art found; 3 = clear prior art exists in an adjacent field, our version is a new combination/application; 1 = already done.

### C1. Problem framing: operating-point (threshold) transfer for microbiome diagnostics - rating 4/5
- Closest prior art: Wirbel 2019 and Thomas 2019 (set thresholds at a fixed FPR on training data and report cross-study AUROC/specificity, but do not study per-site realised specificity or fix it); Tsai 2025 (Gut Pathogens; anecdotal external specificity 0.96 vs 0.21 in different tasks); Wang 2026 review (AJTR) explicitly recommends prespecified thresholds and intercept recalibration when prevalence differs; Godau 2025 frames the same "prevalence shift breaks thresholds" problem for medical imaging.
- Justification: no microbiome paper found that (i) quantifies between-site dispersion of realised specificity at a fixed target and (ii) proposes a transfer method. Not a 5 because the general concern (thresholds/calibration do not transport) is well established in clinical prediction (Steyerberg, Riley 2016, Van Calster) and imaging (Godau), and FIT programmes already treat cut-offs as site-specific (Young 2024).

### C2. Site-shift mixture model (affine score shift + transported class shapes + prevalence, ML on unlabeled target scores) - rating 2.5/5 (method) / 3.5/5 (as applied)
- Closest prior art (HIGH overlap):
  - Zhang et al. 2013 (ICML) "target and conditional shift": jointly estimates prior shift and a location-scale conditional shift from unlabeled target data. Conceptually the same shift model; theirs is on features with kernel mean matching, aimed at accuracy.
  - Saerens 2002 / Alexandari 2020 (MLLS) / mixture-model quantifiers (HDy in Gonzalez 2017): ML/EM on unlabeled target outputs with class-conditional score distributions transported from source. Our model = MLLS + an affine nuisance on the score.
  - Qiu, Zhao & Zheng 2026 (Biometrics, SACSIM): adapts a Neyman-Pearson (type-I constrained) decision rule to a target population with a small unlabeled target sample, for early cancer detection. Same goal (label-free NP threshold transfer), different machinery (single-index model, density ratios on features, auxiliary prevalence info).
  - Godau 2023/2025: estimate deployment prevalence label-free, then re-set threshold; pure prevalence shift.
  - Shashikumar 2023 (CaDC): label-free calibration-shift correction at a new hospital to hit a target PPV.
  - Mixture-model cut-offs without gold standard (Henkelman 1990; Kafatos 2016; Bouman 2021 uses control/case reference distributions = transported shapes).
- Justification: every ingredient exists; the specific 1-D score-level "a + b*score, transported shapes, prevalence free" model aimed at a specificity target appears not to be published as such, but a reviewer can reasonably call it "Zhang 2013 / MLLS restricted to one dimension". Identifiability (a, b, prevalence jointly from one unlabeled mixture) is a known weakness (Vega & Greiner 2022 note unidentifiability of affine shifts unsupervised). Novelty must come from the empirical demonstration (where pure label-shift EM and local quantile fail, where the mixture helps) rather than from the method alone. We must cite Zhang 2013, MLLS, SACSIM and Godau prominently and benchmark against Saerens/MLLS.

### C3. Evaluation protocol: realised FPR/specificity per held-out site and per-1000-screened harms under prevalence shift - rating 3.5/5
- Closest prior art: Godau 2025 (prevalence-aware assessment for imaging); decision-curve/net benefit (Vickers & Elkin 2006); Selby 2019 and FIT programme reporting (positivity, colonoscopies per screened); Riley 2016 (between-cluster heterogeneity of performance); Leeflang 2013 (Se/Sp vary with setting).
- Justification: per-site realised-specificity dispersion with an overdispersion test, plus harms per 1000 at screening prevalence, is not done in microbiome ML (which reports LOSO AUROC). Components are standard in clinical epidemiology; novelty is in the domain and in replacing AUROC-only LOSO.

### C4. Label-free vs few-labelled-control comparison (how many local controls beat label-free) - rating 3.5/5
- Closest prior art: Tong 2018 NP umbrella algorithm (order-statistic threshold from n class-0 samples; gives the minimum n for a high-probability FPR guarantee, ~45 controls for 90% specificity at 95% confidence); Bates 2023 conformal p-values; Gibbons 2018 percentile normalisation uses local controls at feature level; Steyerberg 2004 sample size for updating; Kalan 2026 (transfer NP with labelled target data); SACSIM (unlabeled).
- Justification: the conformal baseline itself is not novel. A head-to-head "label-free mixture vs n labelled local controls vs both" crossover analysis for diagnostics deployment was not found; this is a practical contribution for lab directors (how many controls to collect). Moderate novelty.

### Flags (things that already do what we propose)
1. **SACSIM (Qiu et al., Biometrics 2026)** - label-free adaptation of an NP (fixed type-I error) cancer-detection rule using a small unlabeled target sample. Directly overlapping goal; must be cited and differentiated (feature-level density ratio + auxiliary info vs our score-level shift model; no multi-site real-data benchmark of realised specificity).
2. **Zhang et al. 2013** - location-scale conditional shift + prior shift estimated from unlabeled target data. Our model is its 1-D score-level special case.
3. **Godau et al. 2023/2025** - label-free prevalence estimation then threshold re-adjustment (imaging). Our differentiator is that drift in our pilot occurs in CONTROLS' score distribution (specificity changes), which pure prevalence correction cannot fix.
4. **CaDC (Shashikumar 2023)** - label-free calibration-shift correction to a target PPV at new hospitals.
5. Microbiome threshold drift: no paper found that systematically reports it; only anecdotal external specificity values (Tsai 2025; Wirbel 2019/Thomas 2019 report specificity at fixed FPR in held-out studies) and a 2026 narrative review recommending recalibration. This remains our strongest novelty claim.

Overall: the problem framing and evaluation in microbiome diagnostics are reasonably novel; the mixture model is an incremental specialisation of known label-shift/conditional-shift estimators and should be presented as a pragmatic, well-tested tool rather than a new statistical method. Suggested D6 escalation: add a guarantee (e.g., a conservative upper confidence bound on realised FPR from the mixture fit, or a hybrid that uses unlabeled data plus k controls to shrink the conformal requirement), which none of the found prior art provides for score-level shifts.
