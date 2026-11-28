#!/usr/bin/env python3
"""Rebuild every figure in the v22 submission package from its script and compare pixel by pixel with the package
PNG. usage: python scripts/check_figures_v22.py  (writes logs/check_figures_v22.txt)"""
import os, subprocess, sys, numpy as np
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = os.path.join(R, "Target_Journal_Submission/code/experiments/atlas")
M = os.path.join(R, "Target_Journal_Submission/manuscript"); P = os.path.join(R, "Target_Journal_Submission/submission_final_v22/figures")
jobs = [("v5/make_fig_atlas_v21.py", "figures_v21/figure1_atlas.png", "figure1_atlas.png"),
        ("v6/make_fig_gmwi2_v21.py", "figures_v21/figure2_published_test.png", "figure2_published_test.png"),
        ("v5/make_fig_site_v22.py", "figures_v22/figure3_site.png", "figure3_site.png"),
        ("v5/make_fig_site_v22.py", "figures_v22/figureS1_site_methods.png", "figureS1_site_methods.png"),
        ("v7/make_fig_gmhi_v17.py", None, "figureS2_gmhi.png"),
        ("make_graphical_abstract_v21.py", "graphical_abstract/graphical_abstract_v21.png", "graphical_abstract_v21.png")]
out = []; ok = True
for script, built, pkg in jobs:
    sp = os.path.join(A, script); subprocess.run([sys.executable, os.path.basename(sp)], cwd=os.path.dirname(sp), check=True, capture_output=True)
    if built is None:
        import glob; c = sorted(glob.glob(os.path.join(M, "**", pkg), recursive=True), key=os.path.getmtime); built = os.path.relpath(c[-1], M)
    a = np.asarray(Image.open(os.path.join(M, built)).convert("RGB")); b = np.asarray(Image.open(os.path.join(P, pkg)).convert("RGB"))
    same = a.shape == b.shape and int(np.abs(a.astype(int) - b.astype(int)).max()) == 0; ok &= same
    out.append(f"{pkg:32s} {'IDENTICAL' if same else 'DIFFERENT'}  ({script} -> {built})")
open(os.path.join(R, "logs/check_figures_v22.txt"), "w").write("\n".join(out) + "\n"); print("\n".join(out)); sys.exit(0 if ok else 1)
