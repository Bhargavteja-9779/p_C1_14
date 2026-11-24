#!/bin/bash
# Builds submission_package/ and iMeta_submission_package.zip from the project files.
set -e; cd "$(dirname "$0")"; PK=submission_package; SC=/tmp/claude-0/-home-user-p-C1-14/372e04e0-1747-54b9-aac3-4c81ea760030/scratchpad
mkdir -p $SC; rm -rf $PK && mkdir -p $PK/figures $PK/code
cp code/figures/out/Figure1.{pdf,png} code/figures/out/Figure2.{pdf,png} code/figures/out/Graphical_Abstract.{pdf,png} $PK/figures/
cd manuscript
python3 -c "
s=open('manuscript.md').read()
s+='\n\n## FIGURES\n\n![Figure 1](../code/figures/out/Figure1.png){width=16cm}\n\n![Figure 2](../code/figures/out/Figure2.png){width=16cm}\n'
open('$SC/ms_build.md','w').write(s)
si=open('SI_methods.md').read()+'\n\n'+open('SI_tables.md').read()
open('$SC/si_build.md','w').write('---\ntitle: \"Supporting Information\"\n---\n\n'+si)"
pandoc $SC/ms_build.md --resource-path=. -o ../$PK/Manuscript.docx
pandoc $SC/si_build.md -o ../$PK/Supporting_Information.docx
pandoc cover_letter.md -o ../$PK/Cover_Letter.docx
cp manuscript.md ../$PK/Manuscript.md; cd ..
C=$PK/code; mkdir -p $C/src $C/scripts $C/pilot $C/experiments/dev $C/experiments/final/results $C/experiments/addendum_results $C/figures
cp code/src/*.py $C/src/; cp code/pilot/pilot_threshold_transfer.py $C/pilot/
cp code/figures/make_figures.py code/figures/make_si_tables.py code/figures/make_graphical_abstract.py $C/figures/
cp code/experiments/{protocol.md,data_lock.md,protocol_freeze_hashes.txt,protocol_addendum_drugs.md,addendum_drugs.py,addendum_metformin_explore.py,addendum_results_dev.log,addendum_results_confirm.log,addendum_metformin_explore.log} $C/experiments/
cp code/experiments/novelty_escalation_log.md $C/experiments/development_log.md
cp code/experiments/addendum_results/*.csv $C/experiments/addendum_results/
cp code/experiments/dev/*.py code/experiments/dev/*.log code/experiments/dev/explore_v7b_fits.csv code/experiments/dev/explore_v9_contrib.csv code/experiments/dev/explore_v9_constrained.csv code/experiments/dev/explore_v9b_axes.csv $C/experiments/dev/
cp code/experiments/final/{run_final.py,analyze_final.py,analyze_final.log,RESULTS_locked.md} $C/experiments/final/
cp code/experiments/final/results/{partB_positivity.csv,partB_regression.csv,partB_adjusted_holm.csv,oneshot.csv.gz,run_info.json,summary.txt} $C/experiments/final/results/
mkdir -p $C/cutoffguard && cp -r code/cutoffguard/{cutoffguard,tests,pyproject.toml,README.md} $C/cutoffguard/
find $C -name "__pycache__" -prune -exec rm -rf {} + ; find $C -name "*.egg-info" -prune -exec rm -rf {} +
cp packaging/fetch_cmd.py $C/scripts/; cp packaging/requirements.txt packaging/README_code.md $C/; mv $C/README_code.md $C/README.md
cp packaging/SUBMISSION_CHECKLIST.md $PK/
for f in $C/experiments/dev/*.log $C/experiments/*.log $C/experiments/final/*.log; do sed -i '/RuntimeWarning/d; /a, lb, lp = p; b = np.exp/d; /Ct\["n_pos"\]/d' $f; done
rm -f iMeta_submission_package.zip && zip -qr iMeta_submission_package.zip $PK && ls -la iMeta_submission_package.zip
