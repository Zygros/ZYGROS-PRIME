"""Entropy mitigation / antifragility primitives."""

from typing import Dict, Any

def post_mortem(context: str, error: Exception) -> Dict[str, Any]:
    """Return a structured post-mortem record for a failure."""
    return {
        "context": context,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "corrective_actions": [
            "Review logs",
            "Identify root cause",
            "Patch process and system"
        ],
    }
