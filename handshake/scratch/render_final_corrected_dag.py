import math
from pathlib import Path
import matplotlib.pyplot as plt

nodes = {
    "S": (0.0, 2.4),
    "A": (2.2, 4.4),
    "B": (2.2, 0.4),
    "C": (4.6, 3.8),
    "D": (4.6, 1.0),
    "E": (7.0, 3.8),
    "F": (7.0, 1.0),
    "T": (9.4, 2.4),
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

t_params = {
    ("S", "A"): 0.45,
    ("S", "B"): 0.45,
    ("S", "C"): 0.22,  # near S, far before crossing with A->D
    ("A", "C"): 0.50,  # midpoint of A->C
    ("A", "D"): 0.18,  # near A, far above S->C crossing
    ("B", "D"): 0.45,  # midpoint of B->D
    ("B", "E"): 0.22,  # near B, far from all crossings
    ("C", "E"): 0.50,  # midpoint of C->E
    ("C", "F"): 0.24,  # near C, far above D->E crossing
    ("D", "E"): 0.24,  # near D, far below C->F crossing
    ("D", "F"): 0.50,  # midpoint of D->F
    ("D", "T"): 0.25,  # near D, completely isolated from F->T
    ("E", "F"): 0.50,  # midpoint of E->F
    ("E", "T"): 0.50,  # midpoint of E->T
    ("F", "T"): 0.55,  # on F->T, well separated from 28
}

fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

node_r = 0.30

# 1. Draw directed edges with clean arrows
for (u, v) in edges:
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    ux = dx / dist
    uy = dy / dist
    
    # Trim arrows to perimeter of nodes
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
            mutation_scale=20,
            shrinkA=0,
            shrinkB=0,
        ),
        zorder=3
    )

# 2. Draw badges centered directly ON each edge
for (u, v) in edges:
    w = weights[(u, v)]
    t = t_params[(u, v)]
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    
    bx = (1 - t) * x1 + t * x2
    by = (1 - t) * y1 + t * y2
    
    bbox = dict(
        boxstyle="round,pad=0.28",
        fc="#ffffff",
        ec="#64748b",
        lw=1.3,
        alpha=1.0
    )
    ax.text(
        bx, by, str(w),
        fontsize=12,
        fontweight="bold",
        color="#b91c1c",
        ha="center",
        va="center",
        bbox=bbox,
        zorder=5
    )

# 3. Draw nodes with pure BLACK outline
for nd, (x, y) in nodes.items():
    circ = plt.Circle((x, y), node_r, color="#fef9c3", ec="#000000", lw=2.5, zorder=6)
    ax.add_patch(circ)
    ax.text(
        x, y, nd,
        fontsize=14,
        fontweight="bold",
        ha="center",
        va="center",
        color="#000000",
        zorder=7
    )

ax.set_xlim(-0.7, 10.1)
ax.set_ylim(-0.2, 5.0)
ax.axis("off")
fig.tight_layout()

out_scratch = Path("scratch/dag_final_corrected.png")
fig.savefig(out_scratch, format="png", bbox_inches="tight", facecolor="white")

out_workspace = Path("workspace/lumiere_submission_ready_v2/diagram.png")
out_workspace.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_workspace, format="png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Generated clean on-edge DAG diagram with black outlines at {out_scratch} and {out_workspace}")
