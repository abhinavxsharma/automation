"""Builds Lumière task artifacts from computed DAG critical path results."""

from typing import Any

_PROMPT = (
    "The figure shows a task-dependency directed acyclic graph (DAG) "
    "representing a parallel computation pipeline. Tasks are nodes "
    "$S, A, B, C, D, E, F, T$, where $S$ is entry and $T$ is terminal. "
    "Directed edges $(u, v)$ represent precedence with latency in "
    "milliseconds ($\\text{ms}$). Assuming tasks start immediately once all "
    "predecessors complete, determine the critical path duration (maximum "
    "latency from $S$ to $T$). Answer in ms as a 2 significant figure "
    "number without units. Intermediate calculations to 6 significant "
    "figures. Unstated constants to 4 significant figures."
)


def _build_artifacts(weights, edges, best_dist, best_path,
                     all_paths) -> dict[str, Any]:
    """Assemble prompt, solution, distractors, and justifications."""
    desc = (
        f"Directed acyclic graph with entry S, terminal T. 8 nodes, "
        f"{len(edges)} directed edges with latency labels (ms). "
        "Crossing edges: (S,C) crosses (A,D); (B,E) crosses (A,D); "
        "(C,F) crosses (D,E); (D,T) crosses (E,F)."
    )
    sol = _build_solution(best_dist, best_path)
    d_set = {str(d) for d, _ in all_paths if d != best_dist}
    distractors = [d for d in ["75", "73", "72", "68", "64"] if d in d_set]
    just = (
        "Both models failed to trace the directed topological critical "
        "path of the graph. The crossing edges caused models to misread "
        "connections or overlook the optimal sub-path detour $D \\to E "
        "\\to F$ ($12+8=20\\text{ ms}$) in favor of $D \\to F$ ($19\\text{ "
        "ms}$) or $D \\to T$ ($28\\text{ ms}$)."
    )
    return {
        "prompt": _PROMPT, "gtfa": str(best_dist), "image_description": desc,
        "solution": sol, "distractors": distractors,
        "answer_format": "Integer", "decimal_places": 0,
        "failure_category": "Topological", "failure_justification": just,
    }


def _build_solution(best_dist: int, best_path: list[str]) -> str:
    """Build numbered step-by-step solution string."""
    p_str = " \\to ".join(best_path)
    lines = [
        "Step 1: Identify all 8 nodes and directed edge latencies (ms).",
        "Step 2: Trace candidate directed paths from source $S$ to $T$.",
        "Step 3: Evaluate path $S \\to A \\to D$: latency is $14+22=36\\text{ ms}$.",
        (f"Step 4: Continue along ${p_str}$: critical path is "
         f"${best_dist}\\text{{ ms}}$."),

        f"Step 5: Ground Truth Final Answer is {best_dist}.",
    ]
    return "\n".join(lines)
