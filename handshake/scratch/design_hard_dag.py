def solve_dag(edges):
    adj = {}
    nodes = set()
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)
        if u not in adj:
            adj[u] = []
        adj[u].append((v, w))
        
    # Topological sort (DFS)
    visited = set()
    order = []
    def dfs(u):
        visited.add(u)
        for v, w in adj.get(u, []):
            if v not in visited:
                dfs(v)
        order.append(u)
        
    for n in nodes:
        if n not in visited:
            dfs(n)
    topo = order[::-1]
    
    L = {n: 0 for n in topo}
    parent = {n: None for n in topo}
    
    for u in topo:
        for v, w in adj.get(u, []):
            if L[u] + w > L[v]:
                L[v] = L[u] + w
                parent[v] = u
                
    # Reconstruct critical path
    crit_path = []
    curr = 'T'
    while curr:
        crit_path.append(curr)
        curr = parent[curr]
    crit_path = crit_path[::-1]
    
    # Enumerate all paths S to T
    all_paths = []
    def find_paths(u, cur_len, path):
        if u == 'T':
            all_paths.append((cur_len, list(path)))
            return
        for v, w in adj.get(u, []):
            path.append(v)
            find_paths(v, cur_len + w, path)
            path.pop()
            
    find_paths('S', 0, ['S'])
    all_paths.sort(key=lambda x: x[0], reverse=True)
    
    return L, crit_path, all_paths

edges_candidate = [
    ('S', 'A', 16),
    ('S', 'B', 19),
    ('S', 'C', 12),
    ('S', 'D', 15),
    ('A', 'C', 11),
    ('A', 'D', 24),
    ('A', 'F', 31), # long bypass
    ('B', 'D', 17),
    ('B', 'E', 28),
    ('C', 'E', 14),
    ('C', 'F', 23),
    ('D', 'F', 20),
    ('D', 'G', 26),
    ('D', 'H', 22),
    ('E', 'G', 18),
    ('E', 'H', 25),
    ('E', 'T', 34), # long bypass
    ('F', 'G', 13), # lateral
    ('F', 'T', 27),
    ('G', 'H', 15), # lateral
    ('G', 'T', 29),
    ('H', 'T', 21)
]

L, crit_path, all_paths = solve_dag(edges_candidate)
print("Node maximum latencies:")
for k in ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T']:
    print(f"  L({k}) = {L[k]}")
print(f"\nCritical path: {' -> '.join(crit_path)} = {L['T']}")
print(f"\nTop 12 paths from S to T:")
for length, p in all_paths[:12]:
    print(f"  {' -> '.join(p)} = {length}")
print(f"\nTotal paths from S to T: {len(all_paths)}")
