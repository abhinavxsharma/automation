"""Generate optimized DAG diagram with crisp visible arrowheads and clear labels."""
from pathlib import Path

import matplotlib.pyplot as plt

nodes = {
    "S": (0.0, 2.0),
    "A": (1.6, 3.4),
    "B": (1.6, 0.6),
    "C": (3.2, 2.7),
    "D": (3.2, 1.1),
    "E": (4.8, 2.9),
    "F": (4.8, 1.1),
    "T": (6.4, 2.0),
}

# (u, v): (weight, label_t_param, offset_multiplier)
# t_param: 0.0 is u, 1.0 is v. Using 0.4 - 0.6 places labels away from node circles.
edges_config = {
    ("S", "A"): (14, 0.50, 0.12),
    ("S", "B"): (18, 0.50, -0.12),
    ("S", "C"): (11, 0.38, 0.10),
    ("A", "C"): (9, 0.50, 0.10),
    ("A", "D"): (22, 0.40, -0.12),   # crosses S->C
    ("B", "D"): (15, 0.50, -0.10),
    ("B", "E"): (26, 0.35, 0.14),    # crossing diagonal
    ("C", "E"): (17, 0.50, 0.10),
    ("C", "F"): (21, 0.40, -0.12),   # crosses D->E
    ("D", "E"): (12, 0.60, 0.12),
    ("D", "F"): (19, 0.50, -0.10),
    ("D", "T"): (28, 0.70, -0.12),   # long lower link
    ("E", "F"): (8, 0.50, 0.10),     # vertical link
    ("E", "T"): (24, 0.50, 0.12),
    ("F", "T"): (20, 0.50, -0.12),
}

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

for (u, v), (w, t, off) in edges_config.items():
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    dx, dy = x2 - x1, y2 - y1
    dist = (dx**2 + dy**2)**0.5

    # Draw directed arrow with sharp, distinct arrowhead
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            lw=2.0,
            shrinkA=16,
            shrinkB=16,
            color="#1e3a8a",
            mutation_scale=18,
        ),
    )

    # Position label at fraction t along the link, offset perpendicular
    lx = x1 + t * dx + off * (-dy) / dist * 1.5
    ly = y1 + t * dy + off * (dx) / dist * 1.5

    ax.text(
        lx, ly, str(w), fontsize=10, fontweight="bold",
        color="#b91c1c", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#94a3b8", lw=0.8, alpha=0.95),
        zorder=4
    )

for nd, (x, y) in nodes.items():
    circ = plt.Circle((x, y), 0.28, color="#fef9c3", ec="#0f172a", lw=2.2, zorder=5)
    ax.add_patch(circ)
    ax.text(x, y, nd, fontsize=12, fontweight="bold",
            ha="center", va="center", color="#0f172a", zorder=6)

ax.set_xlim(-0.6, 7.0)
ax.set_ylim(-0.1, 4.1)
ax.axis("off")
fig.tight_layout()
out_file = Path("scratch/dag_critical_path_v2.png")
fig.savefig(out_file, format="png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Generated clean DAG diagram: {out_file}")
