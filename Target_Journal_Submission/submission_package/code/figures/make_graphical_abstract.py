import os, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
INK, INK2, BLUE, ORANGE, BG = "#0b0b0b", "#52514e", "#2a78d6", "#eb6834", "#f4f3ef"
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(9.6, 4.8)); ax.set_xlim(0, 96); ax.set_ylim(0, 48); ax.axis("off")
def box(x, w, title, lines, accent):
    ax.add_patch(FancyBboxPatch((x, 5), w, 33, boxstyle="round,pad=0.6,rounding_size=2", fc=BG, ec=accent, lw=1.6))
    ax.text(x + w / 2, 36, title, ha="center", va="top", fontsize=10.5, fontweight="bold", color=accent)
    y = 30
    for t, big in lines:
        ax.text(x + w / 2, y, t, ha="center", va="top", fontsize=11.5 if big else 7.8, color=INK if big else INK2,
                fontweight="bold" if big else "normal"); y -= 4.6 if big else 3.6
box(3, 27, "1  The problem", [("0–75%", True), ("false-positive rate at 16 sites", False), ("(cut-off set for 10%)", False),
                              ("2.3×", True), ("heart failure flagged", False), ("vs healthy, same site", False)], ORANGE)
box(34.5, 27, "2  The biology", [("Oral-origin taxa", True), ("F. nucleatum, S. oralis, V. parvula", False),
                               ("shared by cancer and chronic disease", False), ("Common drugs", True),
                               ("PPIs raise the oral component", False), ("metformin raises score (exploratory)", False)], INK2)
box(66, 27, "3  The fix", [("Colonoscopy results", True), ("of test-positives only", False), ("no extra labelling", False),
                           ("0.6% vs 49%", True), ("site-months above target", False), ("per-group · guarantee · cutoffguard", False)], BLUE)
for x0 in (30.4, 62):
    ax.add_patch(FancyArrowPatch((x0, 19), (x0 + 3.2, 19), arrowstyle="-|>", mutation_scale=14, color=INK2, lw=1.4))
ax.text(48, 46, "Gut microbiome cancer tests: where and whom you screen sets the false-alarm rate", ha="center", va="top",
        fontsize=12.5, fontweight="bold", color=INK)
ax.text(48, 1.5, "32 public cohorts · pre-registered locked test · LASSO and random forest", ha="center", fontsize=8, color=INK2)
fig.savefig(os.path.join(OUT, "Graphical_Abstract.png"), dpi=300, bbox_inches="tight"); fig.savefig(os.path.join(OUT, "Graphical_Abstract.pdf"), bbox_inches="tight")
