# Editor report — Reviewer 3 (handling editor, iMeta), manuscript_v13.md

**Role:** handling editor — clarity, fit for iMeta readers, reproducibility, ethics, comparison with what iMeta publishes.
**Overall score:** 8 / 10.
**Decision for an iMeta Letter:** **Minor revision** (accept in principle; the concerns below are fixable without new experiments).

## Summary and fit

This is a strong fit for an iMeta Letter. It takes a question the field has not asked — how many *healthy* people a
fixed-cut-off gut-microbiome test flags across populations — and answers it at a scale (28 classifiers × 36 healthy
populations, 20 countries) and with a rigor (pre-committed plans, falsified hypotheses, clustered CIs, a corrected
bootstrap erratum, a released tool) that sits at or above the top quartile of recent iMeta Letters on 9 of 10 scorecard
dimensions (total 78/100, equal to the strongest benchmark Letter). It reads in the house style: "To the Editor,"
→ burden → gap → "Here we…" with three numbers, ALL-CAPS finding-sentence headings, a one-line Methods pointer, a
detailed data-availability statement, and a reusable resource (closest analogues: imt2.212, imt2.70192, imt2.70088,
imt2.70011). Main text ~2,340 words sits mid-band for a Letter. The honesty about what failed (G3, B3, the whole v6c
generalisation, the geography/distance non-replication) is exactly the reproducibility culture iMeta wants to reward and
is itself part of the contribution.

The reason this is minor rather than clean is that the single most quotable claim in the title is stronger than the
evidence behind it, the clinical cost of the recommended fix is understated relative to its prominence, and the
reproducibility story — the paper's own thesis — cannot be checked because the repository is a placeholder.

## MAJOR concerns

1. **The repository and all released artifacts are placeholders at review.** The Data Availability statement and abstract
   promise the code, analysis plans, per-person scores, duplicate list, per-population FPR atlas, and `fprcal` at
   "[GitHub repository URL and Zenodo DOI to be added]." For a paper whose central argument is that microbiome test
   results must be locally verifiable and reproducible, and whose scorecard strength rests on openness, these must be
   live, versioned (Zenodo DOI) and citable *before* acceptance so the atlas, scores and tool can be independently run.
   *Fix:* deposit to GitHub + Zenodo, cite the DOI, and confirm the shipped atlas classifiers reproduce Table S1a AUROCs.
   (The local tool copy passes its 12 tests and the CLI behaves as documented, so this is a deposition step, not a build
   problem.)

2. **The title's second clause over-generalises a result that did not generalise.** "Pooled training can turn a region's
   normal microbiome into a disease signal" is demonstrated for the GMWI2 *recipe* (v6b: East-Asian−other gap 0.52,
   balancing −88%), but (a) the B2 balancing CI is 41–149% and *includes values below* the pre-stated 50% criterion
   (6% of draws), and (b) the attempt to carry balancing to the five multi-cohort disease classifiers (v6c) **failed on
   the FPR scale** and is honestly labelled post hoc — C2 and C3 both failed, FPR moved *away* from target (CRC
   0.04→0.33, T2D 0.12→0.54), and the logit-τ drop is a scale artefact. The mechanism is real and well-evidenced; the
   implied *fix* is not. *Fix:* temper the title (e.g. drop "turn … into a disease signal" to a mechanism statement) and
   state in the abstract and the WHY section that country-balancing is a training-time *diagnostic* of one confounder,
   not a deployment fix, and that it did not reduce FPR heterogeneity for the disease classifiers.

3. **The clinical cost of the recommended deployment fix is understated.** The Letter recommends sites recalibrate the
   cut-off locally for screening, but the price is severe and appears only briefly: sensitivity falls from 0.46 to
   0.21–0.23 when 1–10% of the burn-in group are patients (even 100 *labelled* local controls give only 0.245), and many
   of the 28 classifiers already have very low training sensitivity (adenoma 0.24, IGT 0.14, fatty_liver 0.08, T2D 0.21;
   7/28 have AUROC < 0.6, 3 < 0.5). For such tests a locally recalibrated cut-off can be near-useless clinically.
   Combined with the fact that **every site-level result is retrospective hold-out, with no prospective test**, the
   recommendation needs a clearer boundary. *Fix:* state prominently that the burn-in fix is for high-specificity,
   adequately sensitive screening tests in near-healthy intake only, that it trades sensitivity for FPR control, and that
   prospective validation is still required before clinical use.

## MINOR concerns

1. **Title length and shape.** 22 words in two clauses; the most visible iMeta Letters run 5–10 words. Consider a shorter
   finding-or-resource title (e.g. "Gut-microbiome disease tests flag healthy people at population-specific rates").
2. **Figure count/overview.** Three main figures vs the Letter norm of two; confirm iMeta allows three, or consider
   folding Fig 2C/D or Fig 3C into SI. More importantly, add a small study-design/fixed-threshold schematic (as panel
   Fig 1A or an inset) — the iMeta Fig-1 convention is an overview schematic, and its absence is why Fig 1 scores at,
   not above, benchmark on visual story.
3. **"14 tests" vs "28 classifiers."** The abstract leads with "28 disease classifiers," the body with "14 diseases /
   28 classifiers (LASSO + RF)," and Fig 1 shows "14 LASSO tests." Define the 14-vs-28 relationship once, up front, and
   use it consistently; a reader can otherwise think the sample is doubled.
4. **Numerical consistency for the GMWI2 training FPR.** Body line 73 cites "5,514 people in the 44 studies with ≥20
   healthy people"; SI S6.1 cites 5,547 healthy training samples (α = 0.208). Reconcile which denominator the 20.8%
   (0.208) uses, or state both explicitly.
5. **Pre-specification transparency.** The v6b case-mix plan is committed in the *same* commit as the v6 GMWI2 results
   (though git confirms it predates the v6b results file by ~6 min). A one-line note in S5/S6 that the v6b plan commit
   contains no v6b results would remove any ambiguity; the v6c post-hoc labelling is already exemplary.
6. **Seven null classifiers.** Including 7 classifiers with AUROC < 0.6 (3 < 0.5) is defensible (the restriction to
   AUROC ≥ 0.65 changes nothing), but say in one line *why* they are kept (they are published-style research models and
   the point is that FPR heterogeneity is not an artefact of weak models) so readers do not read it as padding.
7. **Reference count** (23) is in the Letter range; fine. Placeholder author/funding/AI-use/contribution blocks are
   acceptable at review but must be completed.

## Figure comments

- **Figure 1.** Excellent, information-dense headline figure. Panel B (14×36 FPR atlas heatmap) is the right visual
  template and the diverging log scale centred on 0.10 works. Issues: (i) column labels (study codes) are small and will
  be hard to read at print column width — enlarge or move some to SI; (ii) add the design/test schematic noted above;
  (iii) panel D's title "Better AUROC ≠ portable FPR" is a conclusion embedded in a panel label — keep the claim in the
  caption and label the panel neutrally.
- **Figure 2.** Clear and persuasive; the A→B→C→D logic (own training data → unseen populations → taxa → retraining)
  tells the mechanism story well. Ensure panel D makes explicit, in the caption, that "country-balanced" is the v6b
  weighting (not the v6c weighting discussed for the disease classifiers), to avoid conflation with MAJOR 2.
- **Figure 3.** Good. Panel titles again embed conclusions ("Burn-in better in 28/28", "Balancing removes 88% of the
  gap" on Fig 2D); acceptable house style but verify against iMeta panel-title norms. Panel D (sensitivity price) is the
  most policy-relevant panel and is currently the least prominent — given MAJOR 3, consider enlarging it or moving its
  message earlier. All panels legible.

## Ethics / reproducibility

Ethics statement (reanalysis of public de-identified data; original approvals cited) is appropriate; no new approval
needed. Reproducibility practice is a model for iMeta (versioned inputs with checksums, committed plans, failed-attempt
log, corrected-bootstrap erratum) — contingent entirely on MAJOR 1 being resolved so it can be verified.

## Recommendation

Accept as an iMeta Letter after a **minor revision** that (1) deposits and cites the repository/tool, (2) tempers the
title and the "fix" framing to match the evidence, and (3) foregrounds the sensitivity cost and retrospective nature of
the site-level recommendation. None of these require new analysis.
