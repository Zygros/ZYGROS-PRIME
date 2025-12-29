"""Entropy Mitigation module."""

from .primitives import antifragility

def handle_failure(context: str, error: Exception) -> str:
    """Invoke antifragile post-mortem and return a human-readable summary."""
    report = antifragility.post_mortem(context, error)
    return (
        f"Post-mortem for {context}: {report['error_type']} - {report['error_message']}\n"
        f"Corrective actions: {', '.join(report['corrective_actions'])}"
    )
