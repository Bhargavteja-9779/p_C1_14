# Revision log (internal review loop)

## Round 1 (2026-11-24)
- New post hoc analysis P1: comorbidity inside CRC colonoscopy cohorts -> mild cardiometabolic labels NOT over-flagged;
  comorbid CRC cases do not score higher. Claims to be narrowed to severe/systemic disease and drug exposure.
- Independent editor and reviewer reports: reviews/round1_editor.md, reviews/round1_reviewer.md (pending).
- Editor (15% send-to-review) and expert reviewer (major revision) reports received.
- New analyses: P2 MetaCardis + country + drugs (HF persists +0.28; T2D -> +0.11, n.s.), locked decomposition (not oral);
  P3 no-resampling stream (vp 19% months > 0.12; new high-confidence option 5%); P4 downward drift (all rules too strict),
  sites >= 40 controls (vp ~ prevalence-bounded); D10 batch correction (reduces, does not remove drift).
- Rewrite (rev2): single story; title 18 words, no Highlights, 19 references (+ SI references), study-design panel, fixed
  Fig 1B clipping, Fig 2A site count, Fig 2D replaced by no-resampling result; honest comparison with label-free rule;
  corrected adjustment wording; within-CRC null reported; PPI primary reported as not supported; Proposition S1 scope
  narrowed (marginal; t* = inf; drift corollary not proven); pilot exposure disclosed; Table S2b month filter fixed;
  Table S1 completed; cutoffguard gains delta option + test.

## Round 2 (2026-11-24)
- Fresh editor: 35% send-to-review (60-65% if CRC-focused, noise addressed, rule not oversold). Reviewer: light major revision.
- New analyses: P5 CRC audit (11 CRC sites; chi2 = 102, p < 1e-15; tau 0.58-0.65), P6 CRC-only deployment, P3b improved
  no-resampling evaluation (25/month, 3 large sites, MetaCardis country-ordered real shift; high-confidence comparator for
  the label-free rule) -> label-free high-confidence rule as good as or better than verified-positive at stable sites.
- Rewrite (rev3): title "Microbiome colorectal cancer tests lose specificity at new sites; local recalibration restores it";
  CRC-centred evidence; pilot exposure disclosed in the main text; post hoc labels; HF result per model; CIs re-rounded;
  locked T2D estimate; >= 40-control source comparison (p = 0.074); per-disease note; method claim narrowed (label-free rule
  sufficient at stable sites; verified-positive for drift/higher prevalence); code change after freeze disclosed (S7c);
  cutoffguard adds prevalence_bounded_threshold; figures: CRC audit with exact CIs, fully adjusted forest, sensitivity row,
  honest no-resampling panel; graphical abstract without PPI claim.
