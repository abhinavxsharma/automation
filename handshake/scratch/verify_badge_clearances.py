import math
from pathlib import Path
import matplotlib.pyplot as plt

# 8 nodes with good spacing
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

# 15 edges with optimal t-parameters along each edge to avoid crossings and other edges
# Format: (u, v): (weight, t_param)
edges_config = {
    ("S", "A"): (14, 0.50),
    ("S", "B"): (18, 0.50),
    ("S", "C"): (11, 0.25),  # near S, far from A->D
    ("A", "C"): (9,  0.50),
    ("A", "D"): (22, 0.22),  # near A, far from S->C
    ("B", "D"): (15, 0.50),
    ("B", "E"): (26, 0.25),  # near B, far from A->D and C->F
    ("C", "E"): (17, 0.50),
    ("C", "F"): (21, 0.25),  # near C, far from D->E
    ("D", "E"): (12, 0.75),  # near E, far from C->F and B->E
    ("D", "F"): (19, 0.50),
    ("D", "T"): (28, 0.30),  # near D, far from E->F and F->T
    ("E", "F"): (8,  0.50),
    ("E", "T"): (24, 0.50),
    ("F", "T"): (20, 0.55),  # centered on F->T
}

def pt_to_seg_dist(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    l2 = dx*dx + dy*dy
    if l2 == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / l2))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

# Measure badge positions and distances to all other segments
badge_pos = {}
for (u, v), (w, t) in edges_config.items():
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    bx = (1 - t) * x1 + t * x2
    by = (1 - t) * y1 + t * y2
    badge_pos[(u, v)] = (bx, by, w)

print("Verifying badge clearances to non-parent edges:")
all_clear = True
for (u, v), (bx, by, w) in badge_pos.items():
    # Distance to own edge is 0 (it sits exactly on own edge)
    min_other_dist = 999.0
    nearest_other = None
    for (ou, ov) in edges_config:
        if (ou, ov) == (u, v):
            continue
        x1, y1 = nodes[ou]
        x2, y2 = nodes[ov]
        d = pt_to_seg_dist(bx, by, x1, y1, x2, y2)
        if d < min_other_dist:
            min_other_dist = d
            nearest_other = (ou, ov)
    print(f"Badge {w:2d} on {u}->{v} is at ({bx:.2f}, {by:.2f}); nearest other edge is {nearest_other[0]}->{nearest_other[1]} with clearance = {min_other_dist:.3f}")
    if min_other_dist < 0.20:
        print(f"  WARNING: Clearance too tight for {w} on {u}->{v} to {nearest_other}!")
        all_clear = False

print("\nAll badges have clear margin:", all_clear)
