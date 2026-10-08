"""Simulation of DAG critical path to verify GTFA and model difficulty."""
from collections import defaultdict

# 8 nodes: S, A, B, C, D, E, F, T
# All edges directed strictly forward in topological order:
# Topological order: S, A, B, C, D, E, F, T
edges_weights = {
    ("S", "A"): 14,
    ("S", "B"): 18,
    ("S", "C"): 11,
    ("A", "C"): 9,
    ("A", "D"): 22,
    ("B", "D"): 15,
    ("B", "E"): 26,   # crosses A->D / C->D
    ("C", "E"): 17,
    ("C", "F"): 21,   # crosses D->E
    ("D", "E"): 12,
    ("D", "F"): 19,
    ("D", "T"): 28,   # long crossing link
    ("E", "F"): 8,
    ("E", "T"): 24,
    ("F", "T"): 20,
}

# Compute all paths from S to T and their lengths:
adj = defaultdict(list)
for (u, v), w in edges_weights.items():
    adj[u].append((v, w))

all_paths = []
def dfs(u, path, dist):
    if u == "T":
        all_paths.append((dist, path))
        return
    for v, w in adj[u]:
        dfs(v, path + [v], dist + w)

dfs("S", ["S"], 0)
all_paths.sort(reverse=True)
print(f"Total paths from S to T: {len(all_paths)}")
print("All paths:")
for dist, p in all_paths:
    print(f"  Length {dist}: {' -> '.join(p)}")

