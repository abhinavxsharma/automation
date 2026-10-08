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

# The optimized parameters
config = {
    ("S", "A"): (0.66, 0.12),
    ("S", "B"): (0.54, -0.12),
    ("S", "C"): (0.46, -0.12),
    ("A", "C"): (0.52, 0.12),
    ("A", "D"): (0.62, -0.12),
    ("B", "D"): (0.74, -0.12),
    ("B", "E"): (0.56, 0.12),
    ("C", "E"): (0.50, 0.12),
    ("C", "F"): (0.22, -0.12),
    ("D", "E"): (0.36, -0.06),
    ("D", "F"): (0.66, -0.12),
    ("D", "T"): (0.66, 0.12),
    ("E", "F"): (0.34, 0.12),
    ("E", "T"): (0.44, 0.12),
    ("F", "T"): (0.28, -0.12),
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
    
    # Clip start and end by node radius
    sx = x1 + node_r * ux
    sy = y1 + node_r * uy
    ex = x2 - node_r * ux
    ey = y2 - node_r * uy
    
    ax.annotate(
        "", xy=(ex, ey), xytext=(sx, sy),
        arrowprops=dict(
            arrowstyle="-|>",
            lw=2.0,
            color="#1e3a8a",
            mutation_scale=18,
            shrinkA=0,
            shrinkB=0,
        ),
        zorder=3
    )

# Draw badges and short leader indicators if offset
for (u, v) in edges:
    w = weights[(u, v)]
    t, off = config[(u, v)]
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    norm_x = -dy / dist
    norm_y = dx / dist
    
    # Point on edge
    on_edge_x = (1 - t) * x1 + t * x2
    on_edge_y = (1 - t) * y1 + t * y2
    
    # Badge center
    bx = on_edge_x + off * norm_x
    by = on_edge_y + off * norm_y
    
    # Leader tick connecting badge center to edge
    if abs(off) > 0.02:
        ax.plot([on_edge_x, bx], [on_edge_y, by], color="#94a3b8", lw=1.2, ls=":", zorder=4)
        ax.plot([on_edge_x], [on_edge_y], marker="o", color="#1e3a8a", markersize=3.5, zorder=4)
        
    bbox = dict(
        boxstyle="round,pad=0.28",
        fc="#ffffff",
        ec="#1e3a8a",
        lw=1.3,
        alpha=1.0
    )
    ax.text(
        bx, by, str(w),
        fontsize=11,
        fontweight="bold",
        color="#dc2626",
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

out_path = Path("scratch/dag_clean_v1.png")
fig.savefig(out_path, format="png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Generated clean DAG diagram at {out_path}")
