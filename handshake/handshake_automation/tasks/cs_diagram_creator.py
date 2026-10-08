"""Generates adversarial DAG diagrams that stump VLMs on critical path reasoning."""

from pathlib import Path

import matplotlib.pyplot as plt

from handshake_automation.tasks.graph_renderer import draw_dag_graph

_NODES = {
    "S": (0.0, 2.0), "A": (1.6, 3.4), "B": (1.6, 0.6),
    "C": (3.2, 2.7), "D": (3.2, 1.1), "E": (4.8, 2.9),
    "F": (4.8, 1.1), "T": (6.4, 2.0),
}
_EDGES_CONFIG = {
    ("S", "A"): (14, 0.50, 0.12), ("S", "B"): (18, 0.50, -0.12),
    ("S", "C"): (11, 0.38, 0.10), ("A", "C"): (9, 0.50, 0.10),
    ("A", "D"): (22, 0.40, -0.12), ("B", "D"): (15, 0.50, -0.10),
    ("B", "E"): (26, 0.35, 0.14), ("C", "E"): (17, 0.50, 0.10),
    ("C", "F"): (21, 0.40, -0.12), ("D", "E"): (12, 0.60, 0.12),
    ("D", "F"): (19, 0.50, -0.10), ("D", "T"): (28, 0.70, -0.12),
    ("E", "F"): (8, 0.50, 0.10), ("E", "T"): (24, 0.50, 0.12),
    ("F", "T"): (20, 0.50, -0.12),
}


def create_network_flow_diagram(out_path: str | Path) -> dict:
    """Generate adversarial directed acyclic graph diagram."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    draw_dag_graph(ax, _NODES, _EDGES_CONFIG)
    ax.set_xlim(-0.6, 7.0)
    ax.set_ylim(-0.1, 4.1)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    info = {"path": str(path), "supertype": "Computer Science",
            "subtype": "Algorithms & Complexity"}
    info.update({f"w_{u}{v}".lower(): w for (u, v), (w, _, _) in _EDGES_CONFIG.items()})
    info["nodes"] = list(_NODES.keys())
    info["edges"] = list(_EDGES_CONFIG.keys())
    return info
