# Stage 1 - Journal re-verification (2026-11-23)

Decision: **KEEP iMeta (Wiley), Short Communication ("Letter") format.** No alternative found that has equal or higher
impact factor, better scope fit and passes the 72-day test (the first run's screen of ~1,400 journals found almost no Q1
journal whose *full research articles* pass P75<=72 d; iMeta Letters pass with a large margin).

| Item | First run | Re-check | Status |
|---|---|---|---|
| JIF | 24-44 (secondary) | 2025 JIF **44.4** (JCR released 18 Jun 2026) per XIA & HE Publishing analysis of the JCR release and impactfactorforjournal.com; SciJournal reports 24.31 (conflict). | **UNVERIFIED in Clarivate JCR** (no access). Every source puts it far above Q1 cut-offs. |
| Quartile / category | Q1 Microbiology, Biotechnology (secondary) | LetPub/SciJournal: Q1 Microbiology; Q1 Biotechnology | UNVERIFIED in JCR |
| Indexing | SCIE, PubMed, DOAJ | ISSN portal lists Web of Science; DOAJ record updated Mar 2026; PubMed indexed (162 dated items) | verified (ISSN portal, DOAJ API, PubMed) |
| APC | up to 5,500 USD | **DOAJ API now: 4,960 USD / 4,130 GBP / 4,760 EUR** | verified via DOAJ API; first-run value was out of date -> corrected |
| Author guidelines | 403 | Wiley pages still 403 from this environment | UNVERIFIED (format rules kept from first-run benchmark of 11 published Letters) |
| Integrity | none found | Crossref update records for ISSN 2770-596X: 12 updates = 11 corrections + 1 expression of concern (10.1002/imt2.255), **0 retractions**. Web search: no on-hold/delisting/early-warning notice found. Not MDPI. | verified (Crossref), web search limitation noted |

## Received -> accepted (PubMed History; script `code/scripts/imeta_by_type.py`, output `stage1/imeta_acceptance_recheck.csv`)
| Set | n | median | P75 | P90 | max | share > 72 d |
|---|---|---|---|---|---|---|
| Letters, published 2025-06-01..2026-11-22 | 67 | 33 | 51.5 | 78 | 102 | 13% |
| Letters, accepted in last 6 months (>= 2026-05-23) | 20 | 32.5 | 45.5 | 58 | 80 | 5% |
| Research Articles, all | 73 | 56 | 86 | 120 | 229 | 34% |
| Research Articles, last 6 months | 22 | 58 | 78.25 | 91 | 128 | 32% |

Re-computation reproduces the first run except P75 for Letters (first run wrote 52; exact value 51.5 - rounding, corrected).
Letters pass (median well under 72, P75 < 72). Research Articles fail -> the paper must stay a Short Communication.
Caveat: survivorship (only accepted papers), PubMed "received" may be the revised-system date.

## 10 newest papers - level update
Newest Letters (Oct-Nov 2026) include a consortium PRISMA audit of 2,896 microbiome studies ("A decade-scale audit of
microbiome AI-readiness", 10.1002/imt2.70192), strain-level meta-analysis + 30-strain inoculation experiments, and
multi-omics trait mapping. Expected level has not dropped; computational Letters succeed when they (i) cover many cohorts,
(ii) give one clear, reusable finding, (iii) give a practical recommendation. The AI-readiness audit is about metadata
availability, not decision thresholds -> no overlap, but it is a relevant citation (same journal, same audience).
Level-profile update: add "a practical recommendation/standard for the field" as an expected element.
