"""Ground-truth DAG critical path solver for adversarial graph tasks."""

from collections import defaultdict
from typing import Any

from handshake_automation.tasks.artifact_builder import _build_artifacts


def _find_critical_path(weights: dict[tuple[str, str], int],
                        source: str = "S", sink: str = "T"):
    """Find all paths and longest path (critical path) from source to sink."""
    adj = defaultdict(list)
    for (u, v), w in weights.items():
        adj[u].append((v, w))
    all_paths = []

    def dfs(u, path, dist):
        if u == sink:
            all_paths.append((dist, path))
            return
        for v, w in adj[u]:
            dfs(v, path + [v], dist + w)

    dfs(source, [source], 0)
    all_paths.sort(reverse=True)
    return all_paths[0][0], all_paths[0][1], all_paths


def solve_network_flow_task(info: dict[str, Any]) -> dict[str, Any]:
    """Compute exact critical path and return complete Lumière artifacts."""
    edges = info.get("edges", [])
    weights = {(u, v): int(info.get(f"w_{u}{v}".lower(), 0)) for u, v in edges}
    best_dist, best_path, all_paths = _find_critical_path(weights)
    return _build_artifacts(weights, edges, best_dist, best_path, all_paths)

