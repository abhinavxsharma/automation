from pathlib import Path

import matplotlib.pyplot as plt

# Node positions tailored for clear DAG readability with crossing links
nodes = {
    "S": (0.0, 2.0),
    "A": (1.8, 3.4),
    "B": (1.8, 0.6),
    "C": (3.4, 2.8),
    "D": (3.4, 1.2),
    "E": (5.0, 2.6),
    "F": (5.0, 1.4),
    "T": (6.6, 2.0),
}

edges_weights = {
    ("S", "A"): 14,
    ("S", "B"): 18,
    ("S", "C"): 11,
    ("A", "C"): 9,
    ("A", "D"): 22,
    ("B", "D"): 15,
    ("B", "E"): 26,
    ("C", "E"): 17,
    ("C", "F"): 21,
    ("D", "E"): 12,
    ("D", "F"): 19,
    ("D", "T"): 28,
    ("E", "F"): 8,
    ("E", "T"): 24,
    ("F", "T"): 20,
}

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

for (u, v), w in edges_weights.items():
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    dx, dy = x2 - x1, y2 - y1
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops={"arrowstyle": "-|>", "lw": 1.8, "shrinkA": 15,
                    "shrinkB": 15, "color": "#1a365d", "mutation_scale": 16},
    )
    # Position label slightly offset from midpoint
    mx = (x1 + x2) / 2 + 0.07 * dy
    my = (y1 + y2) / 2 - 0.07 * dx
    ax.text(mx, my, str(w), fontsize=10, fontweight="bold",
            color="#991b1b", ha="center", va="center",
            bbox={"fc": "white", "ec": "#d1d5db", "pad": 1.5, "boxstyle": "round,pad=0.2"})

for nd, (x, y) in nodes.items():
    circ = plt.Circle((x, y), 0.28, color="#fef3c7", ec="#1e293b", lw=2.2, zorder=5)
    ax.add_patch(circ)
    ax.text(x, y, nd, fontsize=12, fontweight="bold",
            ha="center", va="center", color="#0f172a", zorder=6)

ax.set_xlim(-0.6, 7.2)
ax.set_ylim(-0.1, 4.1)
ax.axis("off")
fig.tight_layout()
out_file = Path("scratch/dag_critical_path.png")
fig.savefig(out_file, format="png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved DAG diagram to {out_file}")
