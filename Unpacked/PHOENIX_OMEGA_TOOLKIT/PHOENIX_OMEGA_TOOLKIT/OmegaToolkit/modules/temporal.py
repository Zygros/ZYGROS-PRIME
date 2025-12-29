"""Temporal & Resource Governance module."""

from typing import List, Dict

def pareto_fractal(tasks: List[str]) -> Dict[str, List[str]]:
    """Return a coarse partitioning of tasks by notional impact tiers."""
    if not tasks:
        return {"top_4_percent": [], "top_20_percent": [], "rest": []}
    n = len(tasks)
    top_20 = max(1, n // 5)
    top_4 = max(1, top_20 // 5)
    return {
        "top_4_percent": tasks[:top_4],
        "top_20_percent": tasks[:top_20],
        "rest": tasks[top_20:],
    }
