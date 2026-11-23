# PROGRESS (resume file)

Any agent continuing this work: read this file first, then `git log`. Work happens on branch
`claude/dreamy-clarke-rldxev`. All deliverables live in `Target_Journal_Submission/`.
Commit + push after every phase (auto-save).

## Environment notes
- 4 CPU, 15 GB RAM, no GPU. Python 3.13. ScienceDirect HTML blocked (403); Crossref, OpenAlex, arXiv, UCI, PhysioNet, Zenodo, HF reachable.

## Phase log
- [x] Phase -1: repo skeleton created (2026-11-23)
- [ ] STEP 0: journal landscape + 72-day evidence
- [ ] STEP 1: benchmark 25 papers, level profile, style notes
- [ ] STEP 2: real-life problem discovery
- [ ] STEP 3: novelty map + scorecard
- [ ] Protocol pre-registration
- [ ] First working version
- [ ] Novelty escalation loop (D6)
- [ ] Final experiments
- [ ] Manuscript
- [ ] Reviews 1-11
- [ ] Final package

## Decisions (with reasons)
- 2026-11-23 STEP 0 (in progress): Measured received->accepted days from Crossref assertions (Springer/T&F/Wiley/IET) and
  PubMed history (Elsevier/OUP/biomed). ~95 hand-picked journals + automatic screen of 1378 non-Elsevier journals
  (OpenAlex 2yr citedness>4.5) + PubMed screen of Elsevier/IEEE journals. Raw files in journal_selection/raw/.
  Key finding: nearly no Q1 journal has p75<=72 for full research articles. Letters/short reports inflate speed.
  Research-only checks: Critical Care 66/85 (fail), iMeta research article 56/86 (fail), iMeta Letter 33/52 (pass),
  Ophthalmology & Therapy 52/70 (pass, but likely Q2 + clinical scope).
