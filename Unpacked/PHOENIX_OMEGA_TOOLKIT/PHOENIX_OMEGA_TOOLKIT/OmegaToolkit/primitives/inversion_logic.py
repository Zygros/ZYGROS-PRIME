"""Inversion logic primitives."""

from typing import List

def list_failure_modes(goal: str) -> List[str]:
    """Naive generator of failure questions for a given goal string."""
    return [
        f"What guarantees failure for: {goal}?",
        f"What sabotages progress toward: {goal}?",
        f"What are the most likely blockers to: {goal}?"
    ]
