"""CLI: python -m fprcheck --scores scores.txt [--alpha 0.1] [--pi-max 0.01] [--pac]"""
import argparse, numpy as np
from . import burnin_cutoff, burnin_k, pac_k, prob_fpr_above
a = argparse.ArgumentParser(description=__doc__); a.add_argument("--scores", required=True, help="one score per line (burn-in, unlabelled)")
a.add_argument("--alpha", type=float, default=0.10); a.add_argument("--pi-max", type=float, default=0.0); a.add_argument("--pac", action="store_true")
o = a.parse_args(); s = np.loadtxt(o.scores, ndmin=1); n = len(s)
k = pac_k(n, o.alpha, o.pi_max) if o.pac else burnin_k(n, o.alpha, o.pi_max); t = burnin_cutoff(s, o.alpha, o.pi_max, o.pac)
print(f"n={n} k={k} cutoff={t}"); print(f"P(population FPR > 0.15 | exchangeable) = {prob_fpr_above(0.15, n, k):.3f}" if k <= n else "infeasible: flag nobody")
