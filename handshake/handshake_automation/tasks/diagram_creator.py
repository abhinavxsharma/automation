"""Generates self-authored graduate-level engineering diagrams."""

import random
from pathlib import Path

import matplotlib.pyplot as plt


def create_beam_diagram(out_path: str | Path) -> dict[str, float | str]:
    """Generate loaded beam diagram with random spans and loads."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    p1, p2 = random.randint(15, 35), random.randint(30, 60)
    w = random.randint(8, 20)
    l1, l2, l3 = random.randint(2, 4), random.randint(2, 5), random.randint(2, 4)

    fig, ax = plt.subplots(figsize=(8, 3.5), dpi=300)
    ax.plot([0, l1 + l2 + l3], [0, 0], "k-", lw=4)  # Main beam
    # Supports
    ax.plot([l1], [-0.15], "k^", ms=12)  # Pin support at B
    ax.plot([l1 + l2], [-0.15], "ko", ms=10)  # Roller support at C
    # Point loads
    ax.annotate(f"{p1} kN", xy=(0, 0), xytext=(0, 0.8), arrowprops={"facecolor": "crimson", "shrink": 0.05, "width": 2})
    ax.annotate(f"{p2} kN", xy=(l1 + l2 / 2, 0), xytext=(l1 + l2 / 2, 0.8), arrowprops={"facecolor": "crimson", "shrink": 0.05, "width": 2})
    # Distributed load
    ax.axvspan(l1, l1 + l2, ymin=0.48, ymax=0.65, alpha=0.25, color="purple")
    ax.text(l1 + l2 / 2, 0.35, f"w = {w} kN/m", ha="center", fontsize=10, color="purple")

    ax.set_xlim(-1, l1 + l2 + l3 + 1)
    ax.set_ylim(-0.8, 1.2)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, format="png", bbox_inches="tight")
    plt.close(fig)
    return {"path": str(path), "p1": p1, "p2": p2, "w": w, "l1": l1, "l2": l2, "l3": l3}


def create_circuit_diagram(out_path: str | Path) -> dict[str, float | str]:
    """Generate high-contrast analog circuit schematic plot."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    r1, r2 = random.randint(50, 150), random.randint(50, 150)
    vdd = random.choice([12, 15, 18, 24])

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    ax.plot([1, 1, 3, 3, 1], [1, 3, 3, 1, 1], "k-", lw=2)  # Loop
    ax.plot([2], [3], "ks", ms=10)  # R1
    ax.text(2, 3.2, f"R1 = {r1} kΩ", ha="center")
    ax.plot([3], [2], "ks", ms=10)  # R2
    ax.text(3.3, 2, f"R2 = {r2} kΩ", va="center")
    ax.text(0.8, 2, f"Vdd = {vdd} V", ha="right")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, format="png", bbox_inches="tight")
    plt.close(fig)
    return {"path": str(path), "r1": r1, "r2": r2, "vdd": vdd}
