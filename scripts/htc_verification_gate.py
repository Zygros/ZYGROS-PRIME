#!/usr/bin/env python3
"""Deterministic Hyperbolic/Hyperblog Time Chamber verification gate.

This tool does not promote a claim merely because it is documented. It assigns
an evidence state from repository-observable facts and performs reproducible
mathematical/hash checks when the required artifacts are present.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CLAIMS = [
    ("Architecture-first AGI thesis", "documented", "README.md"),
    ("Ω-PRIME recursive verification", "documented", "README.md"),
    ("Phoenix self-improvement experiment", "documented", "README.md"),
    ("Cryptographic provenance", "documented", "docs/PROVENANCE.md"),
    ("S+ readiness gate", "executable", "scripts/splus_check.py"),
    ("Independent benchmark validation", "not_verified", None),
    ("Physical zero-latency communication", "not_verified", None),
    ("Infinite physical coherence", "not_verified", None),
    ("10^(10^100) executed iterations", "not_verified", None),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    phi = (1 + math.sqrt(5)) / 2
    checks = {
        "phi_definition": math.isclose(phi, 1.618033988749895, rel_tol=0, abs_tol=1e-15),
        "two_pow_26": 2**26 == 67_108_864,
        "required_provenance": (ROOT / "docs/PROVENANCE.md").exists(),
        "splus_gate": (ROOT / "scripts/splus_check.py").exists(),
    }

    evidence = []
    for name, state, artifact in CLAIMS:
        present = bool(artifact and (ROOT / artifact).exists())
        evidence.append({
            "claim": name,
            "declared_state": state,
            "artifact": artifact,
            "artifact_present": present,
            "status": "repository_observed" if present else ("explicitly_unverified" if state == "not_verified" else "missing_artifact"),
        })

    result = {
        "protocol": "HTC-VERIFICATION-GATE-2026-08-29",
        "principle": "execute -> measure -> scrutinize -> classify -> preserve",
        "checks": checks,
        "evidence": evidence,
        "hashes": {},
    }

    for rel in ("README.md", "SPLUS.md", "docs/PROVENANCE.md", "scripts/splus_check.py"):
        p = ROOT / rel
        if p.exists():
            result["hashes"][rel] = sha256(p)

    result["pass"] = all(checks.values())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
