import math

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

# For each edge, search for best t in [0.20, 0.80] and offset in [-0.15, 0.15]
# such that distance to all OTHER edges is maximized, and distance to own edge is <= 0.05
best_config = {}

for (u, v) in edges:
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    norm_x = -dy / dist
    norm_y = dx / dist
    
    best_t = 0.5
    best_off = 0.0
    max_min_clearance = -1.0
    
    # Try different t and small offsets
    for ti in range(20, 81, 2):
        t = ti / 100.0
        for oi in range(-12, 13, 2):
            off = oi / 100.0
            bx = (1 - t) * x1 + t * x2 + off * norm_x
            by = (1 - t) * y1 + t * y2 + off * norm_y
            
            # Check distance to node centers (don't overlap nodes!)
            node_dist = min(math.hypot(bx - nx, by - ny) for nx, ny in nodes.values())
            if node_dist < 0.45:
                continue
                
            # Check clearance to all other edges
            min_c = 999.0
            for (ou, ov) in edges:
                if (ou, ov) == (u, v):
                    continue
                ox1, oy1 = nodes[ou]
                ox2, oy2 = nodes[ov]
                d = pt_to_seg_dist(bx, by, ox1, oy1, ox2, oy2)
                if d < min_c:
                    min_c = d
                    
            if min_c > max_min_clearance:
                max_min_clearance = min_c
                best_t = t
                best_off = off
                
    best_config[(u, v)] = (best_t, best_off, max_min_clearance)

print("OPTIMAL CONFIGURATION:")
for (u, v), (t, off, c) in best_config.items():
    w = weights[(u, v)]
    print(f"Edge {u:1s}->{v:1s} (w={w:2d}): t={t:.2f}, off={off:+.2f}, clearance={c:.3f}")

min_overall = min(c for _, _, c in best_config.values())
print(f"\nMinimum overall clearance across ALL edges: {min_overall:.3f}")
