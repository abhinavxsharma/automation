"""Matplotlib rendering helpers for directed graph diagrams."""

import matplotlib.pyplot as plt

_R = 0.30


def draw_dag_graph(ax, nodes, edges_config) -> None:
    """Draw nodes and directed edges with custom offset weight labels."""
    for (u, v), (w, t, off) in edges_config.items():
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        dx, dy = x2 - x1, y2 - y1
        dist = (dx**2 + dy**2) ** 0.5
        ux, uy = dx / dist, dy / dist
        sx, sy = x1 + _R * ux, y1 + _R * uy
        ex, ey = x2 - _R * ux, y2 - _R * uy
        ax.annotate(
            "", xy=(ex, ey), xytext=(sx, sy),
            arrowprops={
                "arrowstyle": "-|>", "lw": 2.2, "shrinkA": 0, "shrinkB": 0,
                "color": "#1e3a8a", "mutation_scale": 22,
            },
            zorder=3,
        )
        lx = x1 + t * dx + off * (-dy) / dist * 1.5
        ly = y1 + t * dy + off * (dx) / dist * 1.5
        bbox = {"boxstyle": "round,pad=0.25", "fc": "white",
                "ec": "#94a3b8", "lw": 1.0, "alpha": 0.98}
        ax.text(lx, ly, str(w), fontsize=11, fontweight="bold",
                color="#b91c1c", ha="center", va="center",
                bbox=bbox, zorder=4)
    for nd, (x, y) in nodes.items():
        circ = plt.Circle((x, y), _R, color="#fef9c3",
                          ec="#0f172a", lw=2.2, zorder=5)
        ax.add_patch(circ)
        ax.text(x, y, nd, fontsize=13, fontweight="bold",
                ha="center", va="center", color="#0f172a", zorder=6)


