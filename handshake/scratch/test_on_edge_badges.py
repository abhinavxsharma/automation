import math
from pathlib import Path
import matplotlib.pyplot as plt

nodes = {
    "S": (0.0, 2.0),
    "A": (1.8, 3.6),
    "B": (1.8, 0.4),
    "C": (3.4, 2.9),
    "D": (3.4, 1.0),
    "E": (5.0, 2.7),
    "F": (5.0, 0.9),
    "T": (6.6, 2.0),
}

edges = [
    ("S", "A"), ("S", "B"), ("S", "C"),
    ("A", "C"), ("A", "D"),
    ("B", "D"), ("B", "E"),
    ("C", "E"), ("C", "F"),
    ("D", "E"), ("D", "F"), ("D", "T"),
    ("E", "F"), ("E", "T"),
    ("F", "T"),
]

weights = {
    ("S", "A"): 14, ("S", "B"): 18, ("S", "C"): 11,
    ("A", "C"): 9,  ("A", "D"): 22,
    ("B", "D"): 15, ("B", "E"): 26,
    ("C", "E"): 17, ("C", "F"): 21,
    ("D", "E"): 12, ("D", "F"): 19, ("D", "T"): 28,
    ("E", "F"): 8,  ("E", "T"): 24,
    ("F", "T"): 20,
}

# Optimized t-parameters along each edge:
t_params = {
    ("S", "A"): 0.50,  # midpoint of S->A
    ("S", "B"): 0.50,  # midpoint of S->B
    ("S", "C"): 0.28,  # (0.95, 2.25) well before A->D
    ("A", "C"): 0.50,  # midpoint of A->C
    ("A", "D"): 0.20,  # (2.12, 3.08) near A, well above S->C
    ("B", "D"): 0.25,  # (2.20, 0.55) near B, well separated from B->E
    ("B", "E"): 0.28,  # (2.70, 1.04) near B, well separated from B->D
    ("C", "E"): 0.50,  # midpoint of C->E
    ("C", "F"): 0.22,  # (3.75, 2.46) near C, well above crossings
    ("D", "E"): 0.22,  # (3.75, 1.37) near D, well below crossings
    ("D", "F"): 0.38,  # (4.01, 0.96) near D, separated from D->T
    ("D", "T"): 0.36,  # (4.55, 1.36) separated from D->F and F->T
    ("E", "F"): 0.25,  # (5.00, 2.25) near E, well above D->T
    ("E", "T"): 0.50,  # midpoint of E->T
    ("F", "T"): 0.55,  # (5.88, 1.50) midpoint of F->T
}

fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

node_r = 0.26

# Draw directed edges
for (u, v) in edges:
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    ux = dx / dist
    uy = dy / dist
    
    sx = x1 + node_r * ux
    sy = y1 + node_r * uy
    ex = x2 - node_r * ux
    ey = y2 - node_r * uy
    
    ax.annotate(
        "", xy=(ex, ey), xytext=(sx, sy),
        arrowprops=dict(
            arrowstyle="-|>",
            lw=2.2,
            color="#1e3a8a",
            mutation_scale=18,
            shrinkA=0,
            shrinkB=0,
        ),
        zorder=3
    )

# Draw badges centered directly ON each edge
for (u, v) in edges:
    w = weights[(u, v)]
    t = t_params[(u, v)]
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    
    bx = (1 - t) * x1 + t * x2
    by = (1 - t) * y1 + t * y2
    
    bbox = dict(
        boxstyle="round,pad=0.25",
        fc="#ffffff",
        ec="#1e3a8a",
        lw=1.4,
        alpha=1.0
    )
    ax.text(
        bx, by, str(w),
        fontsize=11.5,
        fontweight="bold",
        color="#b91c1c",
        ha="center",
        va="center",
        bbox=bbox,
        zorder=5
    )

# Draw nodes
for nd, (x, y) in nodes.items():
    circ = plt.Circle((x, y), node_r, color="#fef9c3", ec="#0f172a", lw=2.4, zorder=6)
    ax.add_patch(circ)
    ax.text(
        x, y, nd,
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        color="#0f172a",
        zorder=7
    )

ax.set_xlim(-0.6, 7.2)
ax.set_ylim(-0.2, 4.2)
ax.axis("off")
fig.tight_layout()

# Save to scratch and also update workspace/lumiere_submission_ready/diagram.png
out_scratch = Path("scratch/dag_on_edge.png")
fig.savefig(out_scratch, format="png", bbox_inches="tight", facecolor="white")

out_workspace = Path("workspace/lumiere_submission_ready/diagram.png")
fig.savefig(out_workspace, format="png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Generated clean on-edge DAG diagram at {out_scratch} and {out_workspace}")
