import math
from pathlib import Path
import matplotlib.pyplot as plt

# 8 nodes with optimized positions for maximum edge clearance
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

# (u, v): (weight, t_param along edge, perpendicular offset)
# We can use t_param and optional perp offset to ensure badges sit unambiguously on their own edge.
# Even with zero perp offset (directly on the edge line), let's find t_params that maximize distance to other edges.
edges_config = {
    ("S", "A"): (14, 0.45),
    ("S", "B"): (18, 0.45),
    ("S", "C"): (11, 0.20),  # near S: x~0.92, y~2.68
    ("A", "C"): (9,  0.50),  # midpoint of A->C: x~3.40, y~4.10
    ("A", "D"): (22, 0.15),  # near A: x~2.56, y~3.89 (FAR above S->C)
    ("B", "D"): (15, 0.45),  # midpoint of B->D: x~3.28, y~0.67
    ("B", "E"): (26, 0.18),  # near B: x~3.06, y~1.01 (FAR from crossings)
    ("C", "E"): (17, 0.50),  # midpoint of C->E: x~5.80, y~3.80
    ("C", "F"): (21, 0.22),  # near C: x~5.13, y~3.18 (FAR above D->E)
    ("D", "E"): (12, 0.22),  # near D: x~5.13, y~1.62 (FAR below C->F and B->E)
    ("D", "F"): (19, 0.50),  # midpoint of D->F: x~5.80, y~1.00
    ("D", "T"): (28, 0.20),  # near D: x~5.56, y~1.28 (way back from T, far from F->T!)
    ("E", "F"): (8,  0.50),  # midpoint of E->F: x~7.00, y~2.40
    ("E", "T"): (24, 0.50),  # midpoint of E->T: x~8.20, y~3.10
    ("F", "T"): (20, 0.60),  # near T on F->T: x~8.44, y~1.84 (28 is at x=5.56, miles away!)
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

badge_pos = {}
for (u, v), (w, t) in edges_config.items():
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    bx = (1 - t) * x1 + t * x2
    by = (1 - t) * y1 + t * y2
    badge_pos[(u, v)] = (bx, by, w)

print("=== CHECKING CLEARANCES WITH NEW LAYOUT ===")
min_overall = 999.0
for (u, v), (bx, by, w) in badge_pos.items():
    min_dist = 999.0
    nearest = None
    for (ou, ov) in edges_config:
        if (ou, ov) == (u, v):
            continue
        x1, y1 = nodes[ou]
        x2, y2 = nodes[ov]
        d = pt_to_seg_dist(bx, by, x1, y1, x2, y2)
        if d < min_dist:
            min_dist = d
            nearest = (ou, ov)
    if min_dist < min_overall:
        min_overall = min_dist
    print(f"Badge {w:2d} on {u}->{v} at ({bx:.2f}, {by:.2f}): nearest {nearest[0]}->{nearest[1]} dist = {min_dist:.3f}")

print(f"\nMinimum clearance across all badges: {min_overall:.3f}")
assert min_overall >= 0.25, f"Clearance too small: {min_overall}"
print("PERFECT CLEARANCES ACHIEVED!")
