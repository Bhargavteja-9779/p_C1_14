# Journal comparison (internal)

Method: received->accepted days measured from (a) Crossref `assertion` metadata (Springer Nature, BMC, Nature Portfolio,
Taylor & Francis, Wiley/IET deposit these) and (b) PubMed `<History>` dates (Elsevier, OUP and other biomedical titles).
Pass rule: median well under 72 AND 75th percentile <= 72, on research articles.

Coverage: ~120 hand-picked journals + an automatic screen of 1,378 non-Elsevier journals of approved publishers with
OpenAlex 2-year mean citedness > 4.5 (941 had dates; 40 random articles each) + a PubMed screen of 1,171 Elsevier/IEEE
journals (299 had dates). MDPI was excluded by design. Raw outputs: `raw/`.

## Main finding
Very few Q1 research journals meet a 72-day 75th percentile. Fast medians are common only among letters, reviews and
invited content. After filtering to research articles, these were the only realistic candidates:

| Journal | Publisher | Article type | n | Median | P75 | Verdict |
|---|---|---|---|---|---|---|
| iMeta | Wiley | Short Communication (Letter) | 67 | 33 | 52 | PASS - **selected** |
| iMeta | Wiley | Research Article | 73 | 56 | 86 | fail P75 |
| Diabetes & Metabolism | Elsevier Masson | Original research | 81 | 46 | 57 | PASS, but clinical scope (ML-methods papers absent); IF ~4.7-5.8 (UNVERIFIED) |
| Ophthalmology and Therapy | Springer (Adis) | Original research | 304 | 52 | 70 | PASS, but likely Q2 and drug/clinical scope |
| Critical Care | BMC | research only | 371 | 66 | 85 | fail (all items incl. letters: 51/69) |
| J King Saud Univ - CIS | Springer | all | 100 | 67.5 | 85 | fail |
| Energy Informatics | Springer | all | 99 | 68 | 87 | fail (+ quartile doubtful) |
| Intensive Care Medicine | Springer | research | 185 | 63 | 92 | fail |
| Resuscitation | Elsevier | research | 347 | 65 | 85 | fail |
| Cardiovascular Diabetology | BMC | research | 398 | 64 | 92 | fail |
| Virtual & Physical Prototyping | T&F | all | 100 | 65 | 89 | fail |
| Journal of Medical Economics | T&F | all | 95 | 57 | 82 | fail |
| Talanta / Anal Chim Acta / Spectrochim Acta A | Elsevier | research | 40 each | 62-68 | 87-90 | fail |
| Water Research, STOTEN, J Hazard Mater, Bioresour Technol, Environ Res | Elsevier | research | 112-120 | 78-110 | 106-147 | fail |
| Computing/AI journals (KBS-like, EAAI, Neural Netw, CIBM, CMPB, AIIM, JBI, JAMIA, Bioinformatics, Brief Bioinform, J Big Data, Complex Intell Syst, NCAA, ...) | various | research | ~100 each | 115-293 | 160-398 | all fail |

Rejected for other reasons: "Trends in ..." and Lancet family (review/commissioned content; Lancet research p75 > 100);
Obesity Pillars / Metabolism Open (JCR Q1 status doubtful); Asian J Civil Eng (36/71 but not Q1 and integrity concerns).

## Why iMeta over Diabetes & Metabolism
Scientific fit beats speed and IF. Our work is computational microbiome diagnostics. iMeta regularly publishes such work,
including as Letters. Diabetes & Metabolism publishes clinical cohort work and almost no ML-methods papers (checked
30 recent ML/CGM-related items). iMeta also has a far higher citation impact.

**Unmet / partially met rule:** the full Research Article format at iMeta fails the P75 rule; we therefore commit to the
Short Communication format, which passes. JCR quartile/JIF could not be verified directly (UNVERIFIED).
