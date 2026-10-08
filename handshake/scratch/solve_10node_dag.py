import math
from PIL import Image, ImageDraw, ImageFont

# 10 Nodes layout across 5 distinct columns:
# Col 0: S (x=220, y=700)
# Col 1: A (x=680, y=380), B (x=680, y=1020)
# Col 2: C (x=1150, y=260), D (x=1150, y=700), E (x=1150, y=1140)
# Col 3: F (x=1620, y=320), G (x=1620, y=700), H (x=1620, y=1080)
# Col 4: T (x=2150, y=700)

node_pos = {
    'S': (220, 700),
    'A': (680, 380),
    'B': (680, 1020),
    'C': (1150, 260),
    'D': (1150, 700),
    'E': (1150, 1140),
    'F': (1620, 320),
    'G': (1620, 700),
    'H': (1620, 1080),
    'T': (2150, 700)
}

# 20 Directed edges with weights:
# Notice: no edge C->D or D->E or C->E, which eliminates any collinear vertical edge overlaps!
# The bypass A->F flies cleanly between C and D!
# The bypass S->D flies cleanly between A and B!
# Lateral intra-stage edges F->G and G->H connect vertically within Col 3!
edges_data = [
    # (u, v, weight, t_pos, (offset_x, offset_y))
    ('S', 'A', 16, 0.45, (0, -22)),
    ('S', 'B', 19, 0.45, (0, 22)),
    ('S', 'D', 15, 0.35, (0, -20)),
    ('A', 'C', 11, 0.45, (-15, -18)),
    ('A', 'D', 24, 0.42, (15, 12)),
    ('A', 'F', 31, 0.28, (0, -22)),
    ('B', 'D', 17, 0.42, (15, -12)),
    ('B', 'E', 28, 0.45, (-15, 18)),
    ('C', 'F', 23, 0.45, (0, -22)),
    ('D', 'F', 20, 0.42, (-12, -15)),
    ('D', 'G', 26, 0.45, (0, -20)),
    ('D', 'H', 22, 0.42, (-12, 15)),
    ('E', 'G', 18, 0.45, (12, -15)),
    ('E', 'H', 25, 0.45, (0, 22)),
    ('E', 'T', 34, 0.32, (15, 20)),
    ('F', 'G', 13, 0.50, (24, 0)),
    ('F', 'T', 27, 0.45, (15, -18)),
    ('G', 'H', 15, 0.50, (24, 0)),
    ('G', 'T', 29, 0.45, (0, -20)),
    ('H', 'T', 21, 0.45, (15, 18))
]

edges_dict = {(u, v): w for u, v, w, t, off in edges_data}
nodes = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T']

adj = {u: [] for u in nodes}
for (u, v), w in edges_dict.items():
    adj[u].append((v, w))

all_paths = []
def dfs(curr, path, length):
    if curr == 'T':
        all_paths.append((length, path))
        return
    for nxt, w in adj[curr]:
        dfs(nxt, path + [nxt], length + w)

dfs('S', ['S'], 0)
all_paths.sort(key=lambda x: x[0], reverse=True)

print(f'Total paths S -> T: {len(all_paths)}')
print('Top 12 longest paths:')
for l, p in all_paths[:12]:
    print(f'  {l} ms: {" -> ".join(p)}')

print('\nDP Longest Path Calculation:')
topo_order = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T']
L = {u: 0 for u in topo_order}
pred = {u: [] for u in topo_order}

for u in topo_order:
    for v, w in adj[u]:
        cand = L[u] + w
        pred[v].append((u, w, cand))
        if cand > L[v]:
            L[v] = cand

for u in topo_order:
    preds_str = ", ".join([f"{pu} + {pw} = {pc}" for pu, pw, pc in pred[u]])
    print(f"L({u}) = {L[u]}  [Predecessors: {preds_str}]")
