"""Command line: cutoffguard --history history.csv [--alpha 0.1 --pi-max 0.05 --group-col group]
history.csv columns: month, score, verified (0/1: referred and outcome known), label (0/1, blank if unverified),
optional group column. Prints the cut-off to use next month (overall or per group)."""
import argparse, numpy as np, pandas as pd
from .core import verified_positive_threshold
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--history", required=True); ap.add_argument("--alpha", type=float, default=0.10)
    ap.add_argument("--pi-max", type=float, default=0.05); ap.add_argument("--group-col", default=None)
    ap.add_argument("--delta", type=float, default=None, help="high-confidence option: P(FPR > alpha) <= delta")
    a = ap.parse_args(); d = pd.read_csv(a.history); d["label"] = d["label"].fillna(0)
    groups = [(None, d)] if a.group_col is None else list(d.groupby(a.group_col))
    for g, q in groups:
        t = verified_positive_threshold(q.score.values, q.verified.astype(bool).values, q.label.values, a.alpha, a.pi_max, a.delta)
        print(f"{'all' if g is None else g}\tnext_cutoff={t:.6g}\tn={len(q)}\tverified_cases={int((q.verified.astype(bool) & (q.label == 1)).sum())}")
if __name__ == "__main__": main()
