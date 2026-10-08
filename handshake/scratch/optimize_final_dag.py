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

def evaluate_clearance(t_params):
    min_overall_clearance = 999.0
    results = {}
    for (u, v), t in t_params.items():
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        bx = (1 - t) * x1 + t * x2
        by = (1 - t) * y1 + t * y2
        w = weights[(u, v)]
        
        # Check distance to all other edges
        min_other = 999.0
        closest_other = None
        for (ou, ov) in edges:
            if (ou, ov) == (u, v):
                continue
            ox1, oy1 = nodes[ou]
            ox2, oy2 = nodes[ov]
            d = pt_to_seg_dist(bx, by, ox1, oy1, ox2, oy2)
            if d < min_other:
                min_other = d
                closest_other = (ou, ov)
        results[(u, v)] = (w, bx, by, min_other, closest_other)
        if min_other < min_overall_clearance:
            min_overall_clearance = min_other
    return min_overall_clearance, results

# Let's test candidate t_params
candidate_t = {
    ("S", "A"): 0.45,
    ("S", "B"): 0.45,
    ("S", "C"): 0.22,  # near S
    ("A", "C"): 0.50,
    ("A", "D"): 0.18,  # near A
    ("B", "D"): 0.45,
    ("B", "E"): 0.22,  # near B
    ("C", "E"): 0.50,
    ("C", "F"): 0.24,  # near C
    ("D", "E"): 0.24,  # near D
    ("D", "F"): 0.50,
    ("D", "T"): 0.25,  # near D, far before E->F and F->T
    ("E", "F"): 0.50,
    ("E", "T"): 0.50,
    ("F", "T"): 0.55,  # centered on F->T
}

min_c, res = evaluate_clearance(candidate_t)
print(f"Minimum overall clearance: {min_c:.3f}\n")
for (u, v), (w, bx, by, d, other) in res.items():
    print(f"Badge {w:2d} on {u}->{v} at ({bx:.2f}, {by:.2f}): clearance = {d:.3f} to {other[0]}->{other[1]}")
